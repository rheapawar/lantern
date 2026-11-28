"""Verifier (plain code): checks the LLM's answer before anything reaches a card.

A model can be argued out of a rule; this code can't. It never trusts the schema enforcement on the
model side - every check is re-done here.

Errors reject the answer (one retry with the errors, then "needs manual review"); warnings are shown.
Whatever the model says, the final urgency is max(floor, model urgency) - red flags can only raise it.
"""
import re
from datetime import date

import jsonschema

from lantern.retriever import cited_refs

NEEDS_REVIEW = "needs_manual_review"
VERIFIED = "verified"
SUMMARY_MAX_WORDS = 20


# --- Numbers in a statement must come from what it cites ---------------------------------------------
ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
NUMBER = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?![\d])|(?<![\w.])\d+(?:\.\d+)?")


def _norm(text):
    return " ".join(text.lower().split())


def _numbers(text):
    """[(value, decimals)] for every number written in `text` (1,750 -> 1750)."""
    out = []
    for m in NUMBER.finditer(text):
        raw = m.group(0).replace(",", "")
        out.append((float(raw), len(raw.split(".")[1]) if "." in raw else 0))
    return out


def _ref_sources(context):
    """ref -> list of items carrying it (one BP panel record holds both systolic and diastolic)."""
    out = {}
    for f in context["facts"].values():
        for it in f["items"]:
            out.setdefault(it["ref"], []).append(it)
    for t in context["tests"]:
        if t.get("last"):
            out.setdefault(t["last"]["ref"], []).append(t["last"])
    return out


def _allowed(items, cutoff):
    """Numbers a statement may contain when citing these items: values (and numbers inside text values
    like 'Diabetes mellitus type 2' or 'lisinopril 10 MG'), units, the record date and its age."""
    vals, dates = set(), set()
    for it in items:
        for k in ("value", "unit", "display"):
            v = it.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                vals.add(float(v))
            elif isinstance(v, str):
                vals |= {n for n, _ in _numbers(v)}
        d = it.get("date")
        if d:
            dates.add(d)
            y, mth, day = d.split("-")
            vals |= {float(y), float(mth), float(day)}
            days = (date.fromisoformat(cutoff) - date.fromisoformat(d)).days
            months, years = round(days / 30.4), days / 365.25
            vals |= {float(days), float(round(days / 7)), float(months), float(months - 1), float(months + 1),
                     float(int(years)), float(round(years))}
    return vals, dates


def _matches(n, decimals, vals):
    """n equals some allowed value as written to its own precision (129.73 may be written 129.7 or 130)."""
    tol = 10 ** -decimals
    return any(abs(n - v) < tol or round(v, decimals) == n for v in vals)


def check_statement(fact_item, context, sources, note, cutoff):
    """Errors for one cited fact: a note citation needs a real quote; every number in the statement must
    come from the cited record (within rounding), its date, or - for the note - the quote."""
    errs = []
    stmt, ref = fact_item["statement"], fact_item["ref"]
    if ref == context["note_ref"]:
        q = _norm(fact_item.get("quote") or "")
        if not q:
            return [f"cites the referral note but gives no quote - put the note's exact words in quote"]
        if q not in _norm(note):
            return [f"quote '{fact_item['quote'][:60]}' is not in the referral note"]
        vals, dates = {n for n, _ in _numbers(fact_item["quote"])}, set(ISO_DATE.findall(fact_item["quote"]))
        dates = {"-".join(d) for d in dates}
    else:
        vals, dates = _allowed(sources.get(ref, []), cutoff)
    for m in ISO_DATE.finditer(stmt):
        if m.group(0) not in dates:
            errs.append(f"date {m.group(0)} in the statement is not the date of {ref}")
    for n, dec in _numbers(ISO_DATE.sub(" ", stmt)):
        if not _matches(n, dec, vals):
            shown = int(n) if dec == 0 else n
            errs.append(f"number {shown} in the statement does not match {ref}"
                        + (" or the quote" if ref == context["note_ref"] else "") + " - copy values exactly")
    return errs


def _flag_tiers(pathway):
    tiers = {}
    for r in pathway["reasons"].values():
        for key, tier in (("red_flags", "emergent"), ("urgent_flags", "urgent"), ("soon_flags", "soon")):
            for f in r.get(key, []):
                tiers[f["id"]] = tier
    return tiers


def _exactly_once(got, want, kind):
    errs = []
    for x in sorted(set(want) - set(got)):
        errs.append(f"{kind} '{x}' is missing - return every listed {kind}")
    for x in sorted(set(got) - set(want)):
        errs.append(f"{kind} '{x}' is not in the list for this referral")
    for x in sorted({x for x in got if got.count(x) > 1}):
        errs.append(f"{kind} '{x}' appears more than once")
    return errs


def verify(answer, request, context, pathway, reason, floor, note):
    """{'ok', 'errors', 'warnings'} for one parsed answer (None = the model's text was not valid JSON)."""
    if not isinstance(answer, dict):
        return {"ok": False, "errors": ["answer is not a JSON object"], "warnings": []}
    errors, warnings = [], []

    v = jsonschema.Draft7Validator(request["schema"])
    for e in sorted(v.iter_errors(answer), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in e.path) or "(top level)"
        errors.append(f"schema: {where}: {e.message}")
    if errors:                       # shape is wrong; the checks below would only repeat it
        return {"ok": False, "errors": errors, "warnings": warnings}

    # citations: the ref exists and belongs to the fact (or is the note, with a real quote), and every
    # number in the statement comes from what it cites
    refs, sources = cited_refs(context), _ref_sources(context)
    for i, f in enumerate(answer["facts"]):
        if f["ref"] not in refs:
            errors.append(f"facts/{i}: ref '{f['ref']}' does not exist in the chart context")
            continue
        own = {it["ref"] for it in context["facts"].get(f["fact"], {}).get("items", [])} | {context["note_ref"]}
        if f["ref"] not in own:
            errors.append(f"facts/{i}: ref '{f['ref']}' is not a source of fact '{f['fact']}'")
            continue
        errors += [f"facts/{i} ({f['fact']}): {e}"
                   for e in check_statement(f, context, sources, note, context["referral_date"])]

    # every pathway item answered exactly once, nothing extra
    r = pathway["reasons"][reason]
    errors += _exactly_once([t["test"] for t in answer["tests"]], [t["id"] for t in context["tests"]], "test")
    errors += _exactly_once([o["option"] for o in answer["options"]], r["interim_options"], "option")
    for kind, items in (("test", answer["tests"]), ("option", answer["options"])):
        for it in items:
            bad = [f for f in it["depends_on"] if f not in pathway["facts"]]
            if bad:
                errors.append(f"{kind} '{it.get(kind)}': depends_on has unknown fact ids {bad}")
    if answer["fit"] not in r["fit_choices"]:
        errors.append(f"fit '{answer['fit']}' is not one of {r['fit_choices']}")

    # urgency never below the plain-code floor, nor below a flag the model itself names
    order = pathway["tier_order"]
    u = answer["urgency"]
    if order.index(u) > order.index(floor):
        errors.append(f"urgency '{u}' is below the red-flag floor '{floor}' - it may only be raised")
    tiers = _flag_tiers(pathway)
    for fid in answer["urgency_flags"]:
        if fid in tiers and order.index(u) > order.index(tiers[fid]):
            errors.append(f"urgency '{u}' is below flag '{fid}' ({tiers[fid]}) named in urgency_flags")

    if len(answer["summary"].split()) > SUMMARY_MAX_WORDS:
        warnings.append(f"summary is {len(answer['summary'].split())} words (max {SUMMARY_MAX_WORDS})")
    return {"ok": not errors, "errors": errors, "warnings": warnings}


def final_urgency(pathway, floor, answer):
    """max(floor, model urgency) in tier order; the floor alone when there is no usable answer."""
    order = pathway["tier_order"]
    u = answer.get("urgency") if isinstance(answer, dict) else None
    if u not in order:
        return floor
    return order[min(order.index(u), order.index(floor))]


def call_and_verify(provider, prep, pathway, reason, parse):
    """Call, verify, retry once with the errors. Returns the outcome record for the case.
    status: 'verified' or 'needs_manual_review'; attempts keep every raw answer and its check result."""
    request, context, floor = prep["request"], prep["context"], prep["floor"]
    attempts, feedback = [], None
    for n in (1, 2):
        try:
            out = provider.call(request, feedback=feedback)
        except Exception as e:                       # provider gave up (retries exhausted, refusal, ...)
            attempts.append({"n": n, "error": f"{type(e).__name__}: {e}"})
            break
        answer = parse(out.get("text"))
        check = verify(answer, request, context, pathway, reason, floor, prep["note"])
        attempts.append({"n": n, **{k: out.get(k) for k in ("model_version", "seconds", "usage", "text")},
                         "parsed": answer, "check": check})
        if check["ok"]:
            return {"status": VERIFIED, "answer": answer, "urgency": final_urgency(pathway, floor, answer),
                    "warnings": check["warnings"], "attempts": attempts}
        feedback = "\n".join(f"- {e}" for e in check["errors"])
    return {"status": NEEDS_REVIEW, "answer": None, "urgency": floor, "warnings": [], "attempts": attempts}
