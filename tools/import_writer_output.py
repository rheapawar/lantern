#!/usr/bin/env python3
"""Bring the clean writer's work back into the repo.

    python3 tools/import_writer_output.py                       # reads ../lantern-writer/out/
    python3 tools/import_writer_output.py --packet /some/dir

What it does:
  - phrase_bank.yaml: checks every flag id exists, then splits the sentences ~80/20 with a stable hash.
      80% -> tests/flag_cases.yaml               (the tuning set; tests/test_flag_cases.py runs it)
      20% -> ../lantern-heldout/flag_cases_hidden.yaml  (OUTSIDE the repo; tools/score_hidden_bank.py
                                                         scores it at checkpoints only)
  - out/notes/hNNN.txt -> ../lantern-heldout/hNNN/referral.txt
  - out/plan.csv       -> ../lantern-heldout/plan.csv
Everything held out lives outside the repo so the tuning chat can't grep it by accident.
Override the location with LANTERN_HELDOUT=/some/dir.
Prints counts only - never sentence or note text - so running it inside Claude Code doesn't leak them.
Then re-run build_cases.py for the held-out set so each bundle carries its note.
"""
import argparse
import csv
import hashlib
import json
import os
import shutil

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIDDEN_PCT = 20
HELDOUT_DIR = os.environ.get("LANTERN_HELDOUT", os.path.join(os.path.dirname(ROOT), "lantern-heldout"))


def hidden(sentence):
    return int(hashlib.sha256(sentence.strip().lower().encode()).hexdigest(), 16) % 100 < HIDDEN_PCT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", default=os.path.join(os.path.dirname(ROOT), "lantern-writer"))
    a = ap.parse_args()
    src = os.path.join(a.packet, "out")
    heldout = HELDOUT_DIR
    os.makedirs(heldout, exist_ok=True)

    with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
        p = json.load(fh)
    flag_ids = {f["id"] for r in p["reasons"].values()
                for k in ("red_flags", "urgent_flags", "soon_flags") for f in r.get(k, [])}

    bank_path = os.path.join(src, "phrase_bank.yaml")
    if os.path.exists(bank_path):
        with open(bank_path) as fh:
            bank = yaml.safe_load(fh) or {}
        unknown = set(bank) - flag_ids
        if unknown:
            raise SystemExit(f"phrase bank uses unknown flag ids: {sorted(unknown)}")
        missing = flag_ids - set(bank)
        visible, hid = {}, {}
        n_vis = n_hid = 0
        for fid, d in sorted(bank.items()):
            for kind in ("fire", "quiet"):
                for s in d.get(kind, []) or []:
                    tgt = hid if hidden(s) else visible
                    tgt.setdefault(fid, {"fire": [], "quiet": []})[kind].append(s)
                    n_hid += tgt is hid
                    n_vis += tgt is visible
        hdr = "# Written by a clean writer that never saw the matching rules. Tune against this file.\n" \
              "# Don't add sentences copied from referral notes. New sentences: write general ones.\n"
        with open(os.path.join(ROOT, "tests", "flag_cases.yaml"), "w") as fh:
            fh.write(hdr + yaml.safe_dump(visible, sort_keys=True, allow_unicode=True, width=1000))
        with open(os.path.join(heldout, "flag_cases_hidden.yaml"), "w") as fh:
            yaml.safe_dump(hid, fh, sort_keys=True, allow_unicode=True, width=1000)
        print(f"phrase bank: {len(bank)} flags, {n_vis} visible sentences, {n_hid} hidden"
              + (f"; NO sentences for {len(missing)} flags: {sorted(missing)}" if missing else ""))
    else:
        print("no out/phrase_bank.yaml yet")

    notes = sorted(f for f in os.listdir(os.path.join(src, "notes")) if f.endswith(".txt")) \
        if os.path.isdir(os.path.join(src, "notes")) else []
    for f in notes:
        cid = f[:-4]
        os.makedirs(os.path.join(heldout, cid), exist_ok=True)
        shutil.copy(os.path.join(src, "notes", f), os.path.join(heldout, cid, "referral.txt"))
    plan_src = os.path.join(src, "plan.csv")
    if os.path.exists(plan_src):
        with open(plan_src) as fh:
            rows = list(csv.DictReader(fh))
        bad = [r.get("case_id") for r in rows if r.get("planned_tier") not in p["tier_order"]]
        if bad:
            raise SystemExit(f"plan.csv: bad planned_tier for {bad}")
        shutil.copy(plan_src, os.path.join(heldout, "plan.csv"))
    print(f"notes imported: {len(notes)}; plan rows: {len(rows) if os.path.exists(plan_src) else 0}")
    print("next: python3 build_cases.py --shortlist selection/heldout_v2.csv --cases-dir ../lantern-heldout")


if __name__ == "__main__":
    main()
