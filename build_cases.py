"""Build cases/<id>/ from selection/shortlist.csv.

    python3 build_cases.py            # all 40
    python3 build_cases.py c001 c007  # some
    python3 build_cases.py --shortlist ../lantern-heldout/heldout_v2.csv --cases-dir ../lantern-heldout   # fresh held-out set (kept outside the repo)

Writes per case (re-runnable; never overwrites referral.txt or label.json):
  bundle.json        Synthea chart cut at the referral date + a ServiceRequest to cardiology
                     whose note is referral.txt (or a placeholder until it exists).  [gitignored]
  meta.json          What the loader needs: ids, reason, referral date. No answers, no hooks.
  chart_summary.md   What the PCP could see on the referral date + the writing plan from cases/plan.csv.
                     For whoever writes the note. Never shows the later diagnosis.
  label.json         Answer key template (only created if missing). Filled in by hand; see cases/NOTE_GUIDE.md.
Lantern itself may read only bundle.json, meta.json and referral.txt - never label.json or plan.csv.
"""
import csv
import json
import os
import sys

from lantern.chart import (active_conditions, add_service_request, check_no_future_dates, condition_matches,
                           current_meds, cut_at, days_between, load_bundle, load_map, med_matches,
                           observations, procedures, resources, res_date, _display)

ROOT = os.path.dirname(os.path.abspath(__file__))
PENDING = "REFERRAL NOTE PENDING - write cases/{cid}/referral.txt, then re-run build_cases.py"
LAB_FACTS = ["egfr", "potassium", "magnesium", "calcium", "hemoglobin", "ldl", "a1c", "tsh", "nt_probnp",
             "iron", "albumin", "liver_tests", "urine_albumin", "inr"]
VITAL_FACTS = ["systolic_bp", "diastolic_bp", "heart_rate", "weight"]
CONDITION_FACTS = ["hypertension", "diabetes", "hyperlipidemia", "heart_failure", "atrial_fibrillation",
                   "prior_mi_cad", "valve_disease", "prior_stroke_tia", "ckd", "copd", "liver_disease",
                   "sleep_apnea", "obesity", "thyroid_disease", "bleeding_history", "alcohol_use"]
MED_FACTS = ["bp_meds", "statin", "current_anticoagulant", "current_antiplatelet", "nsaid", "amlodipine",
             "diuretic", "rate_control_meds", "qt_meds", "hf_worsening_meds", "bp_raising_meds"]


def fmt_age(cutoff, d):
    n = days_between(d, cutoff)
    return "today" if n == 0 else (f"{n} d ago" if n < 60 else f"{n // 30} mo ago" if n < 730 else f"{n // 365} y ago")


def test_state(bundle, fmap, pathway, test_id, cutoff):
    """('not_in_synthea' | 'never' | 'done' | 'out_of_date', last_date or None)."""
    m = fmap["tests"].get(test_id, {})
    if not m:
        return "not_in_synthea", None
    dates = procedures(bundle, m.get("procedure_sct", [])) + [d for d, *_ in observations(bundle, m.get("loinc", []))]
    dates = sorted(d for d in dates if d)
    if not dates:
        return "never", None
    vd = pathway["tests"][test_id]["recency"]["valid_days"]
    return ("done" if vd is None or days_between(dates[-1], cutoff) <= vd else "out_of_date"), dates[-1]


def test_status(bundle, fmap, pathway, test_id, cutoff):
    state, last = test_state(bundle, fmap, pathway, test_id, cutoff)
    vd = pathway["tests"][test_id]["recency"]["valid_days"]
    return {"not_in_synthea": "not recorded in Synthea - never shows as done", "never": "never done",
            "done": f"DONE {last} ({fmt_age(cutoff, last) if last else ''}; window {vd or 'any'} d)",
            "out_of_date": f"out of date - last {last} ({fmt_age(cutoff, last) if last else ''}; window {vd} d) - stays pre-checked"}[state]


def plan_section(plan):
    if not plan:
        return []
    L = ["## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)", "",
         f"- **Tier the note should show:** {plan['planned_tier']}",
         f"- **Question type:** {plan['question_type']} (see the table in NOTE_GUIDE.md)",
         f"- **The note must convey:** {plan['note_must_convey']}",
         f"- **Include this negation:** {plan['include_negation'] or '-'}",
         f"- **Do NOT mention:** {plan['do_not_mention'] or '-'}" + (" (Lantern must find it in the chart)" if plan["do_not_mention"] else ""),
         f"- **Style:** {plan['style']}", ""]
    return L


def summary(row, bundle, fmap, pathway, plan=None):
    cutoff, reason = row["referral_date"], pathway["reasons"][row["reason"]]
    conds = active_conditions(bundle, cutoff)
    meds = current_meds(bundle, cutoff)
    L = [f"# {row['case_id']} - {reason['label']}", "",
         f"- Referral date (chart cut here): **{cutoff}** - visit: {row['referral_visit_type']}",
         f"- {row['age']} y, {row['sex']}" + (" - **HELD OUT** (score only at the end; don't tune on it)" if row["heldout"] == "True" else ""),
         f"- Hook(s) this case tests: {row['hooks'].replace(';', ', ') or 'none'}", ""]
    L += plan_section(plan)
    L += ["## Chart facts Lantern will look for", "", "| Fact | Found |", "|---|---|"]
    for f in CONDITION_FACTS:
        hit = condition_matches(conds, fmap["facts"][f].get("conditions", []))
        if hit:
            L.append(f"| {pathway['facts'][f]['text']} | {'; '.join(sorted(set(hit)))} |")
    for f in MED_FACTS:
        hit = med_matches(meds, fmap["facts"][f].get("meds", []))
        if hit:
            L.append(f"| {pathway['facts'][f]['text']} | {'; '.join(hit)} |")
    L += ["", "## Latest vitals and labs", "", "| Item | Value | Date |", "|---|---|---|"]
    for f in VITAL_FACTS + LAB_FACTS:
        obs = observations(bundle, fmap["facts"][f].get("loinc", []))
        if obs:
            d, v, u, name = obs[-1]
            L.append(f"| {pathway['facts'][f]['text']} | {round(v, 2) if isinstance(v, float) else v} {u or ''} | {d} ({fmt_age(cutoff, d)}) |")
    L += ["", f"## Tests first for {reason['label']} - already done?", ""]
    for t in reason["tests_first"]:
        cond = " (only if: " + json.dumps(t["only_if"]) + ")" if "only_if" in t else ""
        L.append(f"- {pathway['tests'][t['test']]['name']}: {test_status(bundle, fmap, pathway, t['test'], cutoff)}{cond}")
    L += ["", "## Flags you could write into the note", ""]
    for k, lab in (("red_flags", "EMERGENT"), ("urgent_flags", "URGENT"), ("soon_flags", "SOON")):
        for fl in reason.get(k, []):
            L.append(f"- {lab}: {fl['text']}")
    L += ["", "## Active problems (disorders; social 'findings' omitted)", ""]
    L += [f"- {n} (since {d})" for d, n in conds if "(finding)" not in n.lower()] or ["- none"]
    L += ["", "## Medicines prescribed in the last 365 days", ""]
    L += [f"- {n} (last {d})" for n, d in meds] or ["- none"]
    L += ["", "## Last 6 encounters", ""]
    encs = sorted(((res_date(e), _display((e.get("type") or [{}])[0]), (e.get("class") or {}).get("code", ""))
                   for e in resources(bundle, "Encounter")), reverse=True)[:6]
    L += [f"- {d} - {t} ({c})" for d, t, c in encs]
    return "\n".join(L) + "\n"


def label_template(row, bundle, fmap, pathway, plan):
    cutoff, reason = row["referral_date"], pathway["reasons"][row["reason"]]
    helper = {"note": "Generated from the cut chart to help labelling - not an answer.",
              "tests_first_status": {}}
    for t in reason["tests_first"]:
        state, last = test_state(bundle, fmap, pathway, t["test"], cutoff)
        helper["tests_first_status"][t["test"]] = state + (f" (last {last})" if last else "")
    hooks = [h for h in row["hooks"].split(";") if h]
    return {
        "case_id": row["case_id"], "status": "todo", "reason": row["reason"],
        "heldout": row["heldout"] == "True", "planned_tier": (plan or {}).get("planned_tier", ""),
        "planned_question_type": (plan or {}).get("question_type", "new_symptom_assessment"),
        "answer_key_only": {"hooks": hooks,
                            "later_dx": {"condition": row["later_dx"], "date": row["later_dx_date"]} if row["later_dx"] else None},
        "urgency": None, "urgency_flags": [], "urgency_rationale": "", "question_type": None,
        "tests_first": [], "acceptable_options": [], "decision_facts": [],
        "fit": None, "acceptable_fits": [],
        "chart_dependent": bool(hooks), "chart_hook_expectation": "",
        "helper": helper, "labeler": "", "reviewed_by": [], "notes": "",
    }


def build(row, fmap, pathway, plan=None, cases_dir=None):
    cid, cutoff = row["case_id"], row["referral_date"]
    d = os.path.join(cases_dir or os.path.join(ROOT, "cases"), cid)
    os.makedirs(d, exist_ok=True)
    full = load_bundle(os.path.join(ROOT, "output", "fhir", row["file"]))
    bundle, report = cut_at(full, cutoff)
    ref_path = os.path.join(d, "referral.txt")
    note = open(ref_path).read().strip() if os.path.exists(ref_path) else PENDING.format(cid=cid)
    add_service_request(bundle, cid, pathway["specialty"], cutoff, row["referral_visit_id"], note,
                        pathway["reasons"][row["reason"]]["label"])
    bad = check_no_future_dates(bundle, cutoff)
    if bad or report["dangling_refs"]:
        raise SystemExit(f"{cid}: refusing to write - future dates {bad[:3]} / dangling refs {report['dangling_refs'][:3]}")
    with open(os.path.join(d, "bundle.json"), "w") as fh:
        json.dump(bundle, fh)
    meta = {"case_id": cid, "specialty": pathway["specialty"], "reason": row["reason"], "referral_date": cutoff,
            "patient_id": row["patient_id"], "referral_visit_id": row["referral_visit_id"],
            "referral_note_written": os.path.exists(ref_path)}
    with open(os.path.join(d, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    with open(os.path.join(d, "chart_summary.md"), "w") as fh:
        fh.write(summary(row, bundle, fmap, pathway, plan))
    label_path = os.path.join(d, "label.json")
    if not os.path.exists(label_path):
        with open(label_path, "w") as fh:
            json.dump(label_template(row, bundle, fmap, pathway, plan), fh, indent=2)
            fh.write("\n")
    return cid, len(full["entry"]), len(bundle["entry"]), meta["referral_note_written"]


def main(ids, shortlist=None, cases_dir=None):
    fmap = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
    with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
        pathway = json.load(fh)
    with open(shortlist or os.path.join(ROOT, "selection", "shortlist.csv")) as fh:
        rows = [r for r in csv.DictReader(fh) if not ids or r["case_id"] in ids]
    cases_dir = os.path.join(ROOT, cases_dir) if cases_dir else os.path.join(ROOT, "cases")
    plan_path = os.path.join(cases_dir, "plan.csv")
    plans = {}
    if os.path.exists(plan_path):
        with open(plan_path) as fh:
            plans = {p["case_id"]: p for p in csv.DictReader(fh)}
    for r in rows:
        cid, n0, n1, has_note = build(r, fmap, pathway, plans.get(r["case_id"]), cases_dir)
        print(f"{cid}: {n0} -> {n1} resources, note {'yes' if has_note else 'pending'}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--shortlist", help="default selection/shortlist.csv")
    ap.add_argument("--cases-dir", help="default cases/ (relative to the repo root)")
    a = ap.parse_args()
    main(set(a.ids), a.shortlist, a.cases_dir)
