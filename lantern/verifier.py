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
ERROR = "error"          # infrastructure failure (rate limit, timeout): rerun it, never score it as the model
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


# --- Facilitate, don't draft: no doses or treatment instructions in any free text ---------------------
# A dose ("20 mg") is allowed only if the same dose is already in the chart or the note. An instruction is a
# treatment verb (base or -ing form, never past tense) said as advice - at the start of a clause or after a
# recommending word - with a medicine word within 4 words after it. Questions ("whether...", "...?") are
# skipped: asking what a patient takes is not a plan. Medicine words: fhir_map med lists, the pathway's
# plan_check_terms, and the general words below.
DOSE = re.compile(r"\b(\d+(?:\.\d+)?)\s?(mg|mcg|µg|g|units?|iu|ml|meq|mmol)\b(?!\s*/)", re.I)
TREATMENT_VERBS = (r"start|starting|initiate|initiating|begin|beginning|increase|increasing|decrease|decreasing"
                   r"|reduce|reducing|stop|stopping|discontinue|discontinuing|hold|holding|titrate|titrating"
                   r"|uptitrate|uptitrating|switch|switching|add|adding|prescribe|prescribing|take|resume|resuming")
ADVICE_CUE = (r"should|must|recommend|recommends|recommended|consider|suggest|suggests|suggested|advise|advised"
              r"|please|plan to|needs? to|would|could")
GENERAL_MED_WORDS = ["medication", "medications", "medicine", "medicines", "meds", "dose", "dosage", "drug",
                     "drugs", "therapy", "tablet", "tablets", "pill", "pills", "prescription"]
QUESTION_START = re.compile(r"^\s*(whether|if|is|are|does|do|did|has|have|was|were|check whether|"
                            r"confirm whether|unclear whether|unknown whether)\b", re.I)
CLAUSE = re.compile(r"[^.;!?\n]+[.;!?\n]?")


def med_words(fmap, pathway):
    words = set(GENERAL_MED_WORDS) | set(pathway.get("plan_check_terms", []))
    for f in fmap["facts"].values():
        words |= set(f.get("meds", []))
    return sorted(words, key=len, reverse=True)


def _free_text(answer):
    """(field, text) for every free-text field the model writes."""
    out = [("summary", answer.get("summary", "")), ("urgency_reason", answer.get("urgency_reason", "")),
           ("fit_reason", answer.get("fit_reason", ""))]
    out += [(f"facts/{i}/statement", f.get("statement", "")) for i, f in enumerate(answer.get("facts", []))]
    out += [(f"tests/{t.get('test')}/why", t.get("why", "")) for t in answer.get("tests", [])]
    out += [(f"options/{o.get('option')}/why", o.get("why", "")) for o in answer.get("options", [])]
    out += [(f"missing_info/{i}", m) for i, m in enumerate(answer.get("missing_info", []))]
    return out


def _known_doses(context, note):
    texts = [note] + [str(it.get("value", "")) for f in context["facts"].values() for it in f["items"]]
    return {(float(m.group(1)), m.group(2).lower().rstrip("s")) for t in texts for m in DOSE.finditer(t)}


def plan_errors(answer, context, note, meds):
    """Errors for doses not in the chart/note and for treatment instructions in free text."""
    errs = []
    known = _known_doses(context, note)
    med = r"(?:" + "|".join(re.escape(m) for m in meds) + r")"
    instr = re.compile(r"(?:^\s*|\b(?:" + ADVICE_CUE + r")\s+(?:\w+\s+){0,2})(?:to\s+)?(" + TREATMENT_VERBS
                       + r")\b(?:\W+\w+){0,4}?\W+" + med + r"\b", re.I)
    for field, text in _free_text(answer):
        for m in DOSE.finditer(text):
            if (float(m.group(1)), m.group(2).lower().rstrip("s")) not in known:
                errs.append(f"{field}: dose '{m.group(0)}' is not in the chart or note - Lantern never suggests doses")
        for c in CLAUSE.findall(text):
            if c.strip().endswith("?") or QUESTION_START.match(c):
                continue
            m = instr.search(c)
            if m:
                errs.append(f"{field}: '{c.strip()[:80]}' reads as a treatment instruction - list facts and "
                            "options only; the specialist writes the plan")
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


def verify(answer, request, context, pathway, reason, floor, note, meds=None, fired_flags=()):
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

    # facilitate, don't draft
    errors += plan_errors(answer, context, note, meds or GENERAL_MED_WORDS + pathway.get("plan_check_terms", []))

    # warnings: checklist flags the model left out; tests left unticked that are not done / out of date
    for fid in [f for f in fired_flags if f not in answer["urgency_flags"]]:
        warnings.append(f"checklist flag '{fid}' fired but is not in urgency_flags (the card shows it anyway)")
    status = {t["id"]: t["status"] for t in context["tests"]}
    for t in answer["tests"]:
        if not t["include"] and status.get(t["test"]) in ("not_done", "out_of_date"):
            warnings.append(f"test '{t['test']}' is {status[t['test']].replace('_', ' ')} but left unticked")

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
    status: 'verified', 'needs_manual_review' (the model failed the checks twice) or 'error' (the API failed;
    rerun, don't score). attempts keep every raw answer and its check result."""
    request, context, floor = prep["request"], prep["context"], prep["floor"]
    attempts, feedback = [], None
    fired = [h["id"] for h in prep.get("flags", [])]
    for n in (1, 2):
        try:
            out = provider.call(request, feedback=feedback)
        except Exception as e:                       # the API gave up (retries exhausted, timeout, ...)
            attempts.append({"n": n, "error": f"{type(e).__name__}: {e}"})
            return {"status": ERROR, "answer": None, "urgency": floor, "warnings": [], "attempts": attempts}
        answer = parse(out.get("text"))
        check = verify(answer, request, context, pathway, reason, floor, prep["note"], prep.get("meds"), fired)
        attempts.append({"n": n, **{k: out.get(k) for k in ("model_version", "seconds", "usage", "text")},
                         "parsed": answer, "check": check})
        if check["ok"]:
            return {"status": VERIFIED, "answer": answer, "urgency": final_urgency(pathway, floor, answer),
                    "warnings": check["warnings"], "attempts": attempts}
        feedback = ("Your previous answer:\n" + (out.get("text") or "(empty)")
                    + "\n\nIt was rejected by the plain-code checks:\n" + "\n".join(f"- {e}" for e in check["errors"])
                    + "\n\nReturn the corrected answer: keep everything that was right and fix only these problems.")
    return {"status": NEEDS_REVIEW, "answer": None, "urgency": floor, "warnings": [], "attempts": attempts}
