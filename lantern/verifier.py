"""Verifier (plain code): checks the LLM's answer before anything reaches a card.

A model can be argued out of a rule; this code can't. It never trusts the schema enforcement on the
model side - every check is re-done here.

Errors reject the answer (one retry with the errors, then "needs manual review"); warnings are shown.
Whatever the model says, the final urgency is max(floor, model urgency) - red flags can only raise it.
"""
import jsonschema

from lantern.retriever import cited_refs

NEEDS_REVIEW = "needs_manual_review"
VERIFIED = "verified"
SUMMARY_MAX_WORDS = 20


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


def verify(answer, request, context, pathway, reason, floor):
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

    # citations: the ref exists, and belongs to the fact it is cited for (the note may back any fact)
    refs = cited_refs(context)
    for i, f in enumerate(answer["facts"]):
        if f["ref"] not in refs:
            errors.append(f"facts/{i}: ref '{f['ref']}' does not exist in the chart context")
            continue
        own = {it["ref"] for it in context["facts"].get(f["fact"], {}).get("items", [])} | {context["note_ref"]}
        if f["ref"] not in own:
            errors.append(f"facts/{i}: ref '{f['ref']}' is not a source of fact '{f['fact']}'")

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
        check = verify(answer, request, context, pathway, reason, floor)
        attempts.append({"n": n, **{k: out.get(k) for k in ("model_version", "seconds", "usage", "text")},
                         "parsed": answer, "check": check})
        if check["ok"]:
            return {"status": VERIFIED, "answer": answer, "urgency": final_urgency(pathway, floor, answer),
                    "warnings": check["warnings"], "attempts": attempts}
        feedback = "\n".join(f"- {e}" for e in check["errors"])
    return {"status": NEEDS_REVIEW, "answer": None, "urgency": floor, "warnings": [], "attempts": attempts}
