#!/usr/bin/env python3
"""Pick a FRESH held-out set (h001-h010) from charts not already used in selection/shortlist.csv.

    python3 tools/pick_new_heldout.py              # writes ../lantern-heldout/heldout_v2.csv (outside the repo: it holds later diagnoses)
    python3 tools/pick_new_heldout.py --seed 11

Why: the first 10 held-out notes were visible while the red-flag phrases were tuned, so their
score is no longer honest. These new cases get notes from a clean writer (see tools/make_writer_packet.py)
that has never seen pathways/cardiology.json.

Uses selection/all_tags.jsonl and the same fits()/hooks() rules as select_charts.py.
2 per reason; one with a hook and one plain when possible. Standard candidates only
(no diagnosed-later cases - all_tags.jsonl doesn't keep those).
"""
import argparse
import csv
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from select_charts import REASONS, fits, hooks  # noqa: E402

PER_REASON = 2
COLS = ["case_id", "reason", "heldout", "hooks", "later_dx", "later_dx_date", "age", "sex",
        "referral_date", "referral_visit_type", "file", "patient_id", "referral_visit_id",
        "hypertension", "diabetes", "hyperlipidemia", "smoker", "afib", "heart_failure", "cad_mi",
        "valve", "ckd", "n_bp_meds", "statin", "anticoagulant", "amlodipine", "nsaid",
        "lab_a1c", "lab_ldl", "lab_egfr", "lab_potassium", "lab_tsh", "lab_nt_probnp"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2027)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(ROOT), "lantern-heldout", "heldout_v2.csv"))
    args = ap.parse_args()
    rng = random.Random(args.seed)

    with open(os.path.join(ROOT, "selection", "shortlist.csv")) as fh:
        used = {r["patient_id"] for r in csv.DictReader(fh)}
    with open(os.path.join(ROOT, "selection", "all_tags.jsonl")) as fh:
        tags = [json.loads(line) for line in fh if line.strip()]

    picked = []
    for reason in REASONS:
        cands = [dict(t, reason=reason, hooks=hooks(reason, t)) for t in tags
                 if t["patient_id"] not in used and fits(reason, t)]
        rng.shuffle(cands)
        chosen = []
        for want_hook in (True, False):
            for c in cands:
                if len(chosen) >= PER_REASON or c["patient_id"] in used:
                    continue
                if bool(c["hooks"]) == want_hook:
                    chosen.append(c); used.add(c["patient_id"])
                    break
        for c in cands:                      # top up if a reason had no hook (or no plain) candidate
            if len(chosen) >= PER_REASON:
                break
            if c["patient_id"] not in used:
                chosen.append(c); used.add(c["patient_id"])
        if len(chosen) < PER_REASON:
            print(f"warning: {reason} only has {len(chosen)} unused candidates")
        picked += chosen

    with open(args.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for i, c in enumerate(picked, 1):
            w.writerow(dict(c, case_id=f"h{i:03d}", heldout=True, hooks=";".join(c["hooks"]),
                            later_dx="", later_dx_date=""))
    print(f"wrote {args.out}: {len(picked)} cases ({', '.join(sorted({c['reason'] for c in picked}))})")
    print("next: python3 build_cases.py --shortlist ../lantern-heldout/heldout_v2.csv --cases-dir ../lantern-heldout")


if __name__ == "__main__":
    main()
