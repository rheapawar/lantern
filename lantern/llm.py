"""The one LLM call: referral + chart context + pathway -> structured JSON for the case card.

The model only PICKS: tier ids, flag ids, fact ids, test ids, option ids, fit ids and source refs, all
from enums built per case from the pathway file and the retriever output. It never writes the plan.
Plain code (lantern/verifier.py) checks the answer afterwards; nothing here is trusted on its own.

    .venv/bin/python -m lantern.llm c001 --dry-run     # write the request only, no API call
    .venv/bin/python -m lantern.llm c001               # call the model once, save to runs/<run_id>/
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import time

import yaml

from lantern.cases import ROOT, load_case
from lantern.chart import load_map
from lantern.matcher import Chart, card_hints, routing, urgency_floor
from lantern.retriever import cited_refs, retrieve
from lantern.verifier import med_words

RUNS = os.path.join(ROOT, "runs")


def _load_yaml(path):
    with open(os.path.join(ROOT, path)) as fh:
        return yaml.safe_load(fh)


def load_config(path="config/llm.yaml"):
    return _load_yaml(path)


# --- what model sees -----------------------------------------------------------------------------

def _compact_context(context):
    """Chart context trimmed to what the model needs: found facts with refs, note-only and missing facts."""
    found, note_only, missing = [], [], []
    for f in context["facts"].values():
        if f["found"]:
            found.append({"id": f["id"], "text": f["text"], "items": [
                {k: it[k] for k in ("value", "unit", "date", "days_ago", "ref") if it.get(k) is not None}
                for it in f["items"]]})
        elif any(it.get("from_note") for it in f["items"]):
            note_only.append({"id": f["id"], "text": f["text"]})
        else:
            missing.append({"id": f["id"], "text": f["text"]})
    tests = [{"id": t["id"], "name": t["name"], "status": t["status"],
              "last": ({k: t["last"][k] for k in ("date", "ago", "ref") if k in t["last"]} if t["last"] else None),
              "valid_days": t["valid_days"], "redo_if": t["redo_if"]} for t in context["tests"]]
    return {"facts_found": found, "facts_from_note_only": note_only, "facts_not_in_chart": missing, "tests": tests}


def _flag_list(pathway):
    out = []
    for rid, r in pathway["reasons"].items():
        for key in ("red_flags", "urgent_flags", "soon_flags"):
            out += [{"id": f["id"], "reason": rid, "list": key, "text": f["text"]} for f in r.get(key, [])]
    return out


def build_request(pathway, case, context, floor, flag_hits, hints, routes, cfg):
    """{'system', 'user', 'schema'} for one case. Deterministic: same inputs -> same request."""
    reason = case["meta"]["reason"]
    r = pathway["reasons"][reason]
    with open(os.path.join(ROOT, cfg["prompt"])) as fh:
        system = fh.read().format(specialty=pathway["specialty"])
    options = [{"id": o, "text": pathway["options"][o]["text"],
                "decision_facts": pathway["options"][o].get("decision_facts", [])} for o in r["interim_options"]]
    payload = {
        "specialty": pathway["specialty"],
        "referral_reason": {"id": reason, "label": r["label"]},
        "referral_date": case["meta"]["referral_date"],
        "referral_note": {"ref": context["note_ref"], "text": case["note"]},
        "urgency_tiers": {t: pathway["tiers"][t] for t in pathway["tier_order"]},
        "urgency_floor": floor,
        "flags_fired_by_checklist": [{k: h[k] for k in ("id", "tier", "text", "why")} for h in flag_hits],
        "card_hints": hints,
        "routing_suggestions": routes,
        "decision_fact_groups": r.get("decision_facts", []),
        "chart_context": _compact_context(context),
        "interim_options": options,
        "fit_choices": {f: pathway["fits"][f] for f in r["fit_choices"]},
        "pathway_not_seen_examples": r.get("not_seen", []),
    }
    user = "Referral to prepare (JSON):\n" + json.dumps(payload, indent=1, ensure_ascii=False)
    return {"system": system, "user": user, "schema": output_schema(pathway, reason, context)}


def output_schema(pathway, reason, context):
    """JSON Schema with per-case enums, so model can only name things that exist."""
    r = pathway["reasons"][reason]
    s = lambda: {"type": "string"}
    enum = lambda vals: {"type": "string", "enum": sorted(set(vals))}
    fact_ids = enum(pathway["facts"])
    refs = enum(cited_refs(context))
    return {
        "type": "object",
        "properties": {
            "urgency": enum(pathway["tier_order"]),
            "urgency_reason": s(),
            "urgency_flags": {"type": "array", "items": enum(f["id"] for f in _flag_list(pathway))},
            "summary": s(),
            "facts": {"type": "array", "items": {
                "type": "object",
                "properties": {"fact": fact_ids, "ref": refs, "statement": s(), "quote": s()},
                "required": ["fact", "ref", "statement", "quote"]}},
            "tests": {"type": "array", "items": {
                "type": "object",
                "properties": {"test": enum(t["id"] for t in context["tests"]), "include": {"type": "boolean"},
                               "why": s(), "depends_on": {"type": "array", "items": fact_ids}},
                "required": ["test", "include", "why", "depends_on"]}},
            "options": {"type": "array", "items": {
                "type": "object",
                "properties": {"option": enum(r["interim_options"]), "relevant": {"type": "boolean"},
                               "why": s(), "depends_on": {"type": "array", "items": fact_ids}},
                "required": ["option", "relevant", "why", "depends_on"]}},
            "fit": enum(r["fit_choices"]),
            "fit_reason": s(),
            "missing_info": {"type": "array", "items": s()},
        },
        "required": ["urgency", "urgency_reason", "urgency_flags", "summary", "facts", "tests", "options",
                     "fit", "fit_reason", "missing_info"],
    }


def prepare(pathway, fmap, case, cfg):
    """Retriever + red-flag checklist + request for one case (no API call)."""
    m = case["meta"]
    context = retrieve(pathway, fmap, case["bundle"], m["referral_date"], m["reason"], case["note"])
    chart = Chart(case["bundle"], fmap, m["referral_date"])
    floor, hits = urgency_floor(pathway, case["note"], chart)
    hints = card_hints(pathway, m["reason"], case["note"], chart)
    routes = routing(pathway, m["reason"], case["note"], chart)
    request = build_request(pathway, case, context, floor, hits, hints, routes, cfg)
    return {"context": context, "floor": floor, "flags": hits, "hints": hints, "routes": routes, "request": request,
            "note": case["note"], "meds": med_words(fmap, pathway)}


# --- Providers ---------------------------------------------------------------------------------------

class QuotaExhausted(RuntimeError):
    """The account is out of quota (daily cap, no credit). Retrying won't help: stop the run, resume later."""


def strict_schema(schema):
    """Copy of a JSON Schema with additionalProperties:false and every property required on each object
    (OpenAI strict structured outputs need both; our schema already requires every property)."""
    if isinstance(schema, dict):
        out = {k: strict_schema(v) for k, v in schema.items()}
        if out.get("type") == "object":
            out["additionalProperties"] = False
            out["required"] = sorted(out.get("properties", {}))
        return out
    if isinstance(schema, list):
        return [strict_schema(v) for v in schema]
    return schema


class GeminiProvider:
    def __init__(self, cfg):
        from dotenv import load_dotenv
        from google import genai
        load_dotenv(os.path.join(ROOT, ".env"))
        if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            raise RuntimeError("No GEMINI_API_KEY - add it to .env (see .env.example)")
        self.cfg, self.client = cfg, genai.Client()

    def call(self, request, feedback=None):
        from google.genai import errors, types
        contents = [request["user"]]
        if feedback:
            contents.append(feedback)          # previous answer + the verifier's errors (lantern/verifier.py)
        config = types.GenerateContentConfig(
            system_instruction=request["system"], response_mime_type="application/json",
            response_json_schema=request["schema"], seed=self.cfg.get("seed"),
            max_output_tokens=self.cfg.get("max_output_tokens"),
            **({"temperature": self.cfg["temperature"]} if self.cfg.get("temperature") is not None else {}))
        for attempt in range(self.cfg.get("max_retries", 5) + 1):
            t0 = time.time()
            try:
                resp = self.client.models.generate_content(model=self.cfg["model"], contents=contents, config=config)
            except (errors.ClientError, errors.ServerError) as e:
                if getattr(e, "code", None) == 429 and "per day" in str(e).lower():
                    raise QuotaExhausted(f"Gemini daily quota for {self.cfg['model']} used up: {str(e)[:300]}") from e
                retryable = getattr(e, "code", None) == 429 or isinstance(e, errors.ServerError)
                if not retryable or attempt == self.cfg.get("max_retries", 5):
                    raise
                time.sleep(min(60, 5 * 2 ** attempt))
                continue
            u = resp.usage_metadata
            return {"text": resp.text, "model_version": resp.model_version, "seconds": round(time.time() - t0, 1),
                    "usage": {"input": u.prompt_token_count, "output": u.candidates_token_count,
                              "thinking": u.thoughts_token_count} if u else None}


class OpenAIProvider:
    """OpenAI Responses API with strict JSON-schema output. Data sent is synthetic (Synthea); store=False."""

    def __init__(self, cfg, client=None):
        self.cfg = cfg
        if client is None:
            from dotenv import load_dotenv
            from openai import OpenAI
            load_dotenv(os.path.join(ROOT, ".env"))
            if not os.environ.get("OPENAI_API_KEY"):
                raise RuntimeError("No OPENAI_API_KEY - add it to .env (see .env.example)")
            client = OpenAI(max_retries=0, timeout=cfg.get("timeout_seconds", 600))   # retries are ours, below
        self.client = client

    def call(self, request, feedback=None):
        import openai
        messages = [{"role": "user", "content": request["user"]}]
        if feedback:
            messages.append({"role": "user", "content": feedback})   # previous answer + the verifier's errors
        kwargs = {"model": self.cfg["model"], "instructions": request["system"], "input": messages, "store": False,
                  "max_output_tokens": self.cfg.get("max_output_tokens"),
                  "text": {"format": {"type": "json_schema", "name": "referral_card",
                                      "schema": strict_schema(request["schema"]), "strict": True}}}
        if self.cfg.get("reasoning_effort"):
            kwargs["reasoning"] = {"effort": self.cfg["reasoning_effort"]}
        if self.cfg.get("temperature") is not None:
            kwargs["temperature"] = self.cfg["temperature"]
        retries = self.cfg.get("max_retries", 5)
        for attempt in range(retries + 1):
            t0 = time.time()
            try:
                resp = self.client.responses.create(**kwargs)
            except openai.RateLimitError as e:
                if "insufficient_quota" in str(e):
                    raise QuotaExhausted(f"OpenAI account out of quota/credit: {str(e)[:300]}") from e
                if attempt == retries:
                    raise
            except (openai.InternalServerError, openai.APIConnectionError, openai.APITimeoutError):
                if attempt == retries:
                    raise
            else:
                u = resp.usage
                reasoning = (getattr(u.output_tokens_details, "reasoning_tokens", 0) or 0) if u else 0
                return {"text": resp.output_text, "model_version": resp.model, "seconds": round(time.time() - t0, 1),
                        "usage": {"input": u.input_tokens, "output": u.output_tokens - reasoning,
                                  "thinking": reasoning} if u else None,
                        "incomplete": getattr(resp.incomplete_details, "reason", None) if resp.status == "incomplete" else None}
            time.sleep(min(60, 5 * 2 ** attempt))


PROVIDERS = {"gemini": GeminiProvider, "openai": OpenAIProvider}


def make_provider(cfg):
    return PROVIDERS[cfg["provider"]](cfg)


def parse(text):
    """The model's JSON, or None if it isn't valid JSON (the verifier then rejects it)."""
    try:
        return json.loads(text) if text else None
    except json.JSONDecodeError:
        return None


# --- Runs --------------------------------------------------------------------------------------------

def new_run_id(cfg):
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + cfg["model"].replace("/", "_")


def request_hash(request):
    return hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()[:12]


def save(run_id, case_id, record):
    d = os.path.join(RUNS, run_id)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{case_id}.json"), "w") as fh:
        json.dump(record, fh, indent=1, ensure_ascii=False, default=str)
    return os.path.join(d, f"{case_id}.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case_id")
    ap.add_argument("--dry-run", action="store_true", help="write the request only, no API call")
    a = ap.parse_args()
    cfg = load_config()
    pathway = json.loads(open(os.path.join(ROOT, "pathways", "cardiology.json")).read())
    fmap = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
    case = load_case(a.case_id)
    prep = prepare(pathway, fmap, case, cfg)
    req = prep["request"]
    record = {"case_id": a.case_id, "config": cfg, "request_hash": request_hash(req), "floor": prep["floor"],
              "flags": prep["flags"], "request": req}
    run_id = ("dryrun-" if a.dry_run else "") + new_run_id(cfg)
    if not a.dry_run:
        out = make_provider(cfg).call(req)
        record["response"] = {**out, "parsed": parse(out["text"])}
    path = save(run_id, a.case_id, record)
    print(f"{a.case_id}: floor {prep['floor']}, request ~{(len(req['system']) + len(req['user'])) // 4} tokens -> {path}")
    if not a.dry_run:
        p = record["response"]["parsed"] or {}
        print(f"  model {out['model_version']}, {out['seconds']}s, usage {out['usage']}")
        print(f"  urgency {p.get('urgency')} | fit {p.get('fit')} | {p.get('summary')}")


if __name__ == "__main__":
    main()
