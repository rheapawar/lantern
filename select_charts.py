#!/usr/bin/env python3
"""
Lantern: pick ~40 cardiology test cases from Synthea FHIR output.

Usage:
    python3 select_charts.py output/fhir            # writes selection/
    python3 select_charts.py output/fhir --seed 7   # different random picks

What it does:
  1. Reads every patient bundle and turns it into a simple timeline
     (conditions, labs, meds, primary care visits).
  2. Finds a referral visit for each patient (a primary care visit) and
     looks at the chart ONLY up to that date.
  3. Tags each chart: which referral reasons it fits, which hidden hooks
     it has, and whether a heart diagnosis appears 30-180 days later.
  4. Picks 8 cases per reason with balance rules, marks 2 per reason as
     held out, and writes:
        selection/shortlist.csv   - the picked cases, one row each
        selection/counts.txt      - how many charts matched every rule
        selection/all_tags.jsonl  - tags for every eligible chart (for debugging)

All rules live in the RULES section below so you can tweak them without
touching the logic. Every rule is a draft until a clinician reviews it.
"""

import argparse
import csv
import glob
import json
import os
import random
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

# =============================================================================
# RULES (edit these)
# =============================================================================

AGE_MIN, AGE_MAX = 40, 85
MIN_PCP_VISITS_2Y = 2          # primary care visits in the 2 years before referral
MAX_ACTIVE_DISORDERS = 10      # skip very messy charts
MED_ACTIVE_DAYS = 365          # a med counts as "current" if prescribed within this many days
LATER_DX_WINDOW = (30, 180)    # days after the referral visit for a "diagnosed later" case
CASES_PER_REASON = 8
HOLDOUT_PER_REASON = 2
MIN_HOOK_CASES_PER_REASON = 2  # try to include this many hook cases per reason
MAX_LATER_DX_PER_REASON = 3

# Primary care visit types (Synthea ambulatory encounter type names)
PCP_VISIT_TYPES = [
    "general examination of patient",
    "encounter for check up",
    "encounter for problem",
    "encounter for symptom",
    "follow-up encounter",
]

# Condition name fragments (lowercase, matched against the condition's display text)
COND = {
    "hypertension": ["hypertension"],
    "diabetes": ["diabetes mellitus type 2", "diabetes mellitus type 1", "due to type 2 diabetes", "due to diabetes"],
    "hyperlipidemia": ["hyperlipidemia", "hypertriglyceridemia", "hypercholesterolemia"],
    "afib": ["atrial fibrillation"],
    "heart_failure": ["heart failure"],
    "cad_mi": ["ischemic heart disease", "coronary heart disease", "coronary artery", "myocardial infarction"],
    "valve": ["valve stenosis", "valve regurgitation", "valve replacement"],
    "ckd": ["chronic kidney disease", "disorder of kidney due to diabetes"],
    "hypothyroid": ["hypothyroidism"],
}

# Medication name fragments (lowercase)
MEDS = {
    "bp_med": ["amlodipine", "lisinopril", "losartan", "hydrochlorothiazide", "metoprolol",
               "atenolol", "chlorthalidone", "valsartan", "carvedilol", "nifedipine",
               "diltiazem", "verapamil"],
    "statin": ["statin"],
    "anticoagulant": ["warfarin", "apixaban", "rivaroxaban", "dabigatran", "edoxaban"],
    "amlodipine": ["amlodipine"],
    "nsaid": ["ibuprofen", "naproxen"],
}

# Lab LOINC codes
LABS = {
    "a1c": ["4548-4"],
    "ldl": ["18262-6"],
    "total_chol": ["2093-3"],
    "egfr": ["33914-3", "62238-1"],
    "creatinine": ["38483-4", "2160-0"],
    "potassium": ["6298-4", "2823-3"],
    "tsh": ["3016-3"],
    "nt_probnp": ["33762-6", "71425-3"],
}
TSH_NORMAL = (0.4, 4.5)
POTASSIUM_LOW = 3.5
EGFR_LOW = 60

SMOKER_VALUES = ["current every day smoker", "current some day smoker"]

# Which future diagnosis maps to which referral reason (for diagnosed-later cases)
LATER_DX_TO_REASON = {
    "afib": "palpitations_afib",
    "heart_failure": "heart_failure_symptoms",
    "cad_mi": "chest_pain",
}

REASONS = ["chest_pain", "palpitations_afib", "heart_failure_symptoms",
           "abnormal_ecg", "hard_to_control_bp_chol"]


def fits(reason, t):
    """Does the chart (tags t, as of referral date) make this referral believable?"""
    risk = t["hypertension"] or t["diabetes"] or t["hyperlipidemia"] or t["smoker"]
    if reason == "chest_pain":
        return t["age"] >= 45 and risk
    if reason == "palpitations_afib":
        return True                                   # any adult
    if reason == "heart_failure_symptoms":
        return t["age"] >= 60 and (t["hypertension"] or t["cad_mi"] or t["valve"] or t["diabetes"])
    if reason == "abnormal_ecg":
        return True                                   # any adult
    if reason == "hard_to_control_bp_chol":
        return (t["hypertension"] and t["n_bp_meds"] >= 2) or (t["hyperlipidemia"] and t["statin"])
    return False


def hooks(reason, t):
    """Hidden facts that should change Lantern's answer for this reason."""
    h = []
    if reason == "chest_pain":
        if t["cad_mi"]: h.append("prior_mi_or_cad")
        if t["ckd"]: h.append("kidney_disease")
    elif reason == "palpitations_afib":
        if t["tsh_abnormal"]: h.append("abnormal_tsh")
        if t["afib"] and not t["anticoagulant"]: h.append("afib_no_blood_thinner")
    elif reason == "heart_failure_symptoms":
        if t["ckd"]: h.append("kidney_disease")
        if t["amlodipine"]: h.append("on_amlodipine")
    elif reason == "abnormal_ecg":
        if t["cad_mi"]: h.append("prior_mi_or_cad")
        if t["potassium_low"]: h.append("low_potassium")
    elif reason == "hard_to_control_bp_chol":
        if t["ckd"]: h.append("kidney_disease")
        if t["nsaid"]: h.append("regular_nsaid")
    return h

# =============================================================================
# Parsing helpers (you shouldn't need to edit below here)
# =============================================================================


def d(s):
    """FHIR date/dateTime string -> date."""
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00")[:19]).date() if "T" in s else date.fromisoformat(s[:10])


def display(cc):
    try:
        return (cc["coding"][0].get("display") or cc.get("text") or "").strip()
    except (KeyError, IndexError, TypeError):
        return (cc or {}).get("text", "") if isinstance(cc, dict) else ""


def code(cc):
    try:
        return cc["coding"][0].get("code")
    except (KeyError, IndexError, TypeError):
        return None


def any_frag(text, frags):
    t = text.lower()
    return any(f in t for f in frags)


def cond_match(name, key):
    """Condition matches a COND key. '(finding)' entries (e.g. abnormal imaging) are ignored."""
    return "(finding)" not in name.lower() and any_frag(name, COND[key])


def load_patient(path):
    b = json.load(open(path))
    p = {"file": os.path.basename(path), "conditions": [], "labs": [], "meds": [],
         "pcp_visits": [], "smoking": []}
    for e in b.get("entry", []):
        r = e.get("resource", {})
        rt = r.get("resourceType")
        if rt == "Patient":
            p["id"] = r.get("id")
            p["birth"] = d(r.get("birthDate"))
            p["sex"] = r.get("gender")
            p["deceased"] = d(r.get("deceasedDateTime"))
        elif rt == "Condition":
            p["conditions"].append({"name": display(r.get("code")),
                                    "onset": d(r.get("onsetDateTime")),
                                    "end": d(r.get("abatementDateTime"))})
        elif rt == "Observation":
            c = code(r.get("code"))
            when = d(r.get("effectiveDateTime"))
            if c == "72166-2":
                p["smoking"].append((when, display(r.get("valueCodeableConcept")).lower()))
            vq = r.get("valueQuantity")
            if vq and "value" in vq:
                p["labs"].append({"code": c, "when": when, "value": vq["value"]})
        elif rt == "MedicationRequest":
            name = display(r.get("medicationCodeableConcept")) if r.get("medicationCodeableConcept") else ""
            p["meds"].append({"name": name, "when": d(r.get("authoredOn"))})
        elif rt == "Encounter":
            if (r.get("class") or {}).get("code") == "AMB":
                tname = display((r.get("type") or [{}])[0]).lower()
                if any(v in tname for v in PCP_VISIT_TYPES):
                    p["pcp_visits"].append({"id": r.get("id"), "type": tname,
                                            "when": d((r.get("period") or {}).get("start"))})
    p["pcp_visits"].sort(key=lambda v: v["when"] or date.min)
    return p if p.get("birth") else None


def age_on(birth, on):
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def active_conditions(p, on):
    return [c for c in p["conditions"]
            if c["onset"] and c["onset"] <= on and (c["end"] is None or c["end"] > on)]


def ever_before(p, on, key):
    """Condition key present before date (active or historical, e.g. past heart attack)."""
    return any(c["onset"] and c["onset"] <= on and cond_match(c["name"], key) for c in p["conditions"])


def latest_lab(p, on, key):
    vals = [l for l in p["labs"] if l["code"] in LABS[key] and l["when"] and l["when"] <= on]
    return max(vals, key=lambda l: l["when"])["value"] if vals else None


def current_meds(p, on):
    lo = on - timedelta(days=MED_ACTIVE_DAYS)
    return [m for m in p["meds"] if m["when"] and lo <= m["when"] <= on]


def tag(p, ref_visit):
    on = ref_visit["when"]
    act = active_conditions(p, on)
    meds = current_meds(p, on)
    smoke = sorted([s for s in p["smoking"] if s[0] and s[0] <= on], key=lambda s: s[0])
    t = {
        "patient_id": p["id"], "file": p["file"], "sex": p["sex"],
        "age": age_on(p["birth"], on),
        "referral_date": on.isoformat(), "referral_visit_id": ref_visit["id"],
        "referral_visit_type": ref_visit["type"],
        "n_active_disorders": sum(1 for c in act if "(disorder)" in c["name"].lower()),
        "pcp_visits_2y": sum(1 for v in p["pcp_visits"] if on - timedelta(days=730) <= v["when"] <= on),
        "smoker": bool(smoke) and any(v in smoke[-1][1] for v in SMOKER_VALUES),
    }
    for key in COND:
        t[key] = ever_before(p, on, key) if key == "cad_mi" else any(cond_match(c["name"], key) for c in act)
    bp_names = {m["name"].lower() for m in meds if any_frag(m["name"], MEDS["bp_med"])}
    t["n_bp_meds"] = len({f for n in bp_names for f in MEDS["bp_med"] if f in n})
    for key in ["statin", "anticoagulant", "amlodipine", "nsaid"]:
        t[key] = any(any_frag(m["name"], MEDS[key]) for m in meds)
    for key in LABS:
        t["lab_" + key] = latest_lab(p, on, key)
    tsh, k, egfr = t["lab_tsh"], t["lab_potassium"], t["lab_egfr"]
    t["tsh_abnormal"] = tsh is not None and not (TSH_NORMAL[0] <= tsh <= TSH_NORMAL[1])
    t["potassium_low"] = k is not None and k < POTASSIUM_LOW
    if egfr is not None and egfr < EGFR_LOW:
        t["ckd"] = True
    t["has_recent_lab"] = any(l["when"] and on - timedelta(days=730) <= l["when"] <= on for l in p["labs"])
    return t


def eligible(t, p):
    on = d(t["referral_date"])
    return (AGE_MIN <= t["age"] <= AGE_MAX
            and (p["deceased"] is None or p["deceased"] > on)
            and t["pcp_visits_2y"] >= MIN_PCP_VISITS_2Y
            and t["has_recent_lab"]
            and t["n_active_disorders"] <= MAX_ACTIVE_DISORDERS)


def later_dx_candidate(p):
    """First heart diagnosis that appears 30-180 days after a primary care visit, with none before."""
    best = None
    for key in LATER_DX_TO_REASON:
        onsets = sorted(c["onset"] for c in p["conditions"] if c["onset"] and cond_match(c["name"], key))
        if not onsets:
            continue
        dx = onsets[0]
        prior = [v for v in p["pcp_visits"]
                 if v["when"] and LATER_DX_WINDOW[0] <= (dx - v["when"]).days <= LATER_DX_WINDOW[1]]
        if prior:
            cand = (key, dx, prior[-1])          # last PCP visit before the diagnosis
            if best is None or dx < best[1]:
                best = cand
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fhir_dir")
    ap.add_argument("--out", default="selection")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    files = [f for f in glob.glob(os.path.join(args.fhir_dir, "*.json"))
             if not os.path.basename(f).startswith(("hospitalInformation", "practitionerInformation"))]
    counts = Counter()
    pool = defaultdict(list)      # reason -> list of candidate dicts
    all_tags = []

    for f in files:
        p = load_patient(f)
        if not p or not p["pcp_visits"]:
            counts["skipped: no birth date or no primary care visits"] += 1
            continue
        counts["patients read"] += 1

        # Diagnosed-later candidate gets its own referral date.
        ld = later_dx_candidate(p)
        if ld:
            key, dx, visit = ld
            t = tag(p, visit)
            if eligible(t, p) and not t[key]:       # must NOT already have that diagnosis
                reason = LATER_DX_TO_REASON[key]
                t.update(later_dx=key, later_dx_date=dx.isoformat(), reason=reason, hooks=hooks(reason, t))
                pool[reason].append(t)
                counts[f"diagnosed-later candidates: {key}"] += 1

        # Standard candidate: most recent primary care visit.
        t = tag(p, p["pcp_visits"][-1])
        if not eligible(t, p):
            counts["not eligible (age, visits, labs, or too many conditions)"] += 1
            continue
        counts["eligible charts"] += 1
        all_tags.append(t)
        for key in ["hypertension", "diabetes", "hyperlipidemia", "smoker", "afib", "heart_failure",
                    "cad_mi", "valve", "ckd", "statin", "anticoagulant", "amlodipine", "nsaid",
                    "tsh_abnormal", "potassium_low"]:
            if t[key]:
                counts[f"has: {key}"] += 1
        for reason in REASONS:
            if fits(reason, t):
                counts[f"fits: {reason}"] += 1
                h = hooks(reason, t)
                for x in h:
                    counts[f"hook: {reason} / {x}"] += 1
                pool[reason].append(dict(t, reason=reason, hooks=h, later_dx="", later_dx_date=""))

    # ---- Pick cases with balance rules ----
    used, picked = set(), []
    for reason in REASONS:
        cands = pool[reason][:]
        rng.shuffle(cands)
        chosen = []
        def take(filter_fn, limit):
            for c in cands:
                if len(chosen) >= CASES_PER_REASON or limit <= 0:
                    break
                if c["patient_id"] in used or not filter_fn(c):
                    continue
                # keep sexes roughly balanced
                sexes = Counter(x["sex"] for x in chosen)
                if sexes[c["sex"]] >= (CASES_PER_REASON // 2) + 1:
                    continue
                chosen.append(c); used.add(c["patient_id"]); limit -= 1
        take(lambda c: c["later_dx"], MAX_LATER_DX_PER_REASON)
        take(lambda c: c["hooks"] and not c["later_dx"], MIN_HOOK_CASES_PER_REASON)
        take(lambda c: not c["later_dx"], CASES_PER_REASON)
        if len(chosen) < CASES_PER_REASON:
            counts[f"SHORT: {reason} only has {len(chosen)} cases"] += 1
        # hold out: 2 per reason, prefer one hook case and one plain
        order = sorted(chosen, key=lambda c: (not c["hooks"], rng.random()))
        hold = {order[0]["patient_id"]} if order else set()
        for c in order[1:]:
            if len(hold) >= HOLDOUT_PER_REASON:
                break
            if not c["hooks"]:
                hold.add(c["patient_id"])
        for c in chosen:
            c["heldout"] = c["patient_id"] in hold
        picked += chosen

    # ---- Write outputs ----
    os.makedirs(args.out, exist_ok=True)
    cols = ["case_id", "reason", "heldout", "hooks", "later_dx", "later_dx_date", "age", "sex",
            "referral_date", "referral_visit_type", "file", "patient_id", "referral_visit_id",
            "hypertension", "diabetes", "hyperlipidemia", "smoker", "afib", "heart_failure", "cad_mi",
            "valve", "ckd", "n_bp_meds", "statin", "anticoagulant", "amlodipine", "nsaid",
            "lab_a1c", "lab_ldl", "lab_egfr", "lab_potassium", "lab_tsh", "lab_nt_probnp"]
    with open(os.path.join(args.out, "shortlist.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for i, c in enumerate(picked, 1):
            w.writerow(dict(c, case_id=f"c{i:03d}", hooks=";".join(c["hooks"])))
    with open(os.path.join(args.out, "all_tags.jsonl"), "w") as fh:
        for t in all_tags:
            fh.write(json.dumps(t) + "\n")

    summary = Counter()
    for c in picked:
        summary[c["reason"]] += 1
        summary["with a hook"] += bool(c["hooks"])
        summary["diagnosed later"] += bool(c["later_dx"])
        summary["held out"] += c["heldout"]
        summary[f"sex: {c['sex']}"] += 1
    lines = ["== Rule matches =="] + [f"{k:<60} {v}" for k, v in sorted(counts.items())]
    lines += ["", f"== Picked {len(picked)} cases =="] + [f"{k:<60} {v}" for k, v in sorted(summary.items())]
    text = "\n".join(lines)
    open(os.path.join(args.out, "counts.txt"), "w").write(text + "\n")
    print(text)
    print(f"\nWrote {args.out}/shortlist.csv, counts.txt, all_tags.jsonl")


if __name__ == "__main__":
    main()