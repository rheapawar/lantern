"""Chart retriever (plain code): the chart context Lantern shows the specialist and the LLM.

Input:  a bundle already cut at the referral date, config/fhir_map.yaml, pathways/<specialty>.json,
        the referral reason and note.
Output: a dict with
  facts  - every pathway fact: what the chart (or the note) says, each item cited by its FHIR id
  tests  - the reason's tests_first (only_if applied): done / out of date / not done / not recorded in
           this data source, with the date and citation of the last result. `prechecked` is False only for
           the pathway's tests_not_prechecked. A test done inside its window stays listed; whether to
           untick it is the specialist's call (see redo_if).
Nothing here decides anything clinical: facts are context, tests_first come from the pathway file,
and `redo_if` (the pathway's stale_if) is shown for the specialist, never evaluated.

Referral-date cutoff: the bundle must already be cut (chart.cut_at). retrieve() checks again and
refuses a bundle with any later date, and drops any record dated after the referral as a second guard.
"""
from datetime import date

from lantern.chart import (_display, check_no_future_dates, condition_records, med_records,
                           observation_records, procedure_records, ref_of, resources)
from lantern.matcher import Chart, evaluate

SMOKING_LOINC = "72166-2"
RECENT_N = 3          # latest few readings per lab/vital, newest first, so trends are visible


class FutureDataError(ValueError):
    """The bundle holds data dated after the referral - never let it reach the engine."""


def _days(cutoff, d):
    return (date.fromisoformat(cutoff) - date.fromisoformat(d)).days if d else None


def ago(days):
    """'today', '12 days ago', '3 months ago', '2 years ago' - for the card."""
    if days is None:
        return "date unknown"
    if days == 0:
        return "today"
    if days < 60:
        return f"{days} day{'s' * (days != 1)} ago"
    if days < 730:
        return f"{round(days / 30.4)} months ago"
    return f"{round(days / 365.25)} years ago"


def _dated(items, cutoff):
    """Keep records dated on/before the cutoff (second guard); add days_ago."""
    out = []
    for it in items:
        if it.get("date") and it["date"] > cutoff:
            continue
        out.append({**it, "days_ago": _days(cutoff, it.get("date"))})
    return out


def _fact(fid, spec, text, bundle, cutoff, conds, meds, patient, note_ref):
    """One pathway fact -> {id, text, found, items[...]}; each item has a `ref` (FHIR id) to cite."""
    items = []
    if spec.get("age"):
        bd = patient.get("birthDate")
        if bd:
            b, c = date.fromisoformat(bd), date.fromisoformat(cutoff)
            age = c.year - b.year - ((c.month, c.day) < (b.month, b.day))
            items.append({"value": age, "unit": "years", "ref": ref_of(patient)})
    if spec.get("sex") and patient.get("gender"):
        items.append({"value": patient["gender"], "ref": ref_of(patient)})
    if spec.get("smoking"):
        obs = [r for r in resources(bundle, "Observation")
               if any(c.get("code") == SMOKING_LOINC for c in r.get("code", {}).get("coding", []))]
        obs = sorted(_dated([{"date": (r.get("effectiveDateTime") or "")[:10] or None,
                              "value": _display(r.get("valueCodeableConcept")), "ref": ref_of(r)} for r in obs],
                            cutoff), key=lambda x: x["date"] or "")
        items += obs[-1:]
    if spec.get("referral_text"):
        items.append({"value": "see referral note", "ref": note_ref, "from_note": True})
    frags = spec.get("conditions", [])
    if frags:
        items += [{"value": c["name"], "date": c["date"], "ref": c["ref"]} for c in conds
                  if "(finding)" not in c["name"].lower() and any(f in c["name"].lower() for f in frags)]
    frags = spec.get("meds", [])
    if frags:
        items += [{"value": m["name"], "date": m["date"], "ref": m["ref"]} for m in meds
                  if any(f in m["name"].lower() for f in frags)]
    if spec.get("loinc"):
        obs = _dated(observation_records(bundle, spec["loinc"]), cutoff)
        items += [{k: o[k] for k in ("value", "unit", "date", "ref", "display")} for o in reversed(obs[-RECENT_N:])]
    if spec.get("procedure_sct"):
        pr = _dated(procedure_records(bundle, spec["procedure_sct"]), cutoff)
        items += [{"value": p["display"], "date": p["date"], "ref": p["ref"]} for p in reversed(pr[-RECENT_N:])]
    for it in items:
        if it.get("date"):
            it["days_ago"] = _days(cutoff, it["date"])
    return {"id": fid, "text": text, "found": bool(items) and not all(i.get("from_note") for i in items),
            "items": items}


def _test(tid, pathway, fmap, bundle, cutoff, prechecked, why_source):
    t = pathway["tests"][tid]
    look = fmap["tests"].get(tid, {})
    rec = t.get("recency", {})
    out = {"id": tid, "name": t["name"], "prechecked": prechecked, "source": why_source,
           "valid_days": rec.get("valid_days"), "redo_if": rec.get("stale_if", [])}
    if not (look.get("loinc") or look.get("procedure_sct")):
        return {**out, "status": "not_recorded_in_source", "last": None}
    found = _dated(observation_records(bundle, look.get("loinc", [])), cutoff) if look.get("loinc") else []
    found += _dated(procedure_records(bundle, look.get("procedure_sct", [])), cutoff) if look.get("procedure_sct") else []
    found = [f for f in found if f.get("date")]
    if not found:
        return {**out, "status": "not_done", "last": None}
    last = max(found, key=lambda f: f["date"])
    last = {k: last.get(k) for k in ("date", "days_ago", "value", "unit", "display", "ref") if last.get(k) is not None}
    last["ago"] = ago(last["days_ago"])
    vd = rec.get("valid_days")
    status = "done" if vd is None or last["days_ago"] <= vd else "out_of_date"
    return {**out, "status": status, "last": last}


def retrieve(pathway, fmap, bundle, referral_date, reason, note=""):
    """Chart context for one referral. Raises FutureDataError if the bundle was not cut at the referral date."""
    bad = check_no_future_dates(bundle, referral_date)
    if bad:
        raise FutureDataError(f"{len(bad)} date(s) after the referral {referral_date}, e.g. {bad[0]}")
    patient = next(iter(resources(bundle, "Patient")), {})
    sr = next(iter(resources(bundle, "ServiceRequest")), None)
    note_ref = ref_of(sr) if sr else "referral"
    conds = condition_records(bundle, referral_date)
    meds = med_records(bundle, referral_date)

    facts = {}
    for fid, f in pathway["facts"].items():
        spec = fmap["facts"].get(fid)
        if spec is None:
            continue
        facts[fid] = _fact(fid, spec, f["text"], bundle, referral_date, conds, meds, patient, note_ref)

    r = pathway["reasons"][reason]
    chart = Chart(bundle, fmap, referral_date)
    tests = []
    not_pre = set(r.get("tests_not_prechecked", []))     # listed, but shown without a tick (e.g. cardiology picks one)
    for t in r.get("tests_first", []):
        if "only_if" in t and not evaluate(t["only_if"], note, chart, []):
            continue
        tests.append(_test(t["test"], pathway, fmap, bundle, referral_date, t["test"] not in not_pre, t.get("source")))

    return {"referral_date": referral_date, "reason": reason, "patient_ref": ref_of(patient) if patient else None,
            "note_ref": note_ref, "facts": facts, "tests": tests}


def cited_refs(context):
    """Every FHIR id the context offers - the verifier checks citations against this set."""
    refs = {context["note_ref"]}
    for f in context["facts"].values():
        refs |= {i["ref"] for i in f["items"]}
    for t in context["tests"]:
        if t.get("last"):
            refs.add(t["last"]["ref"])
    return refs
