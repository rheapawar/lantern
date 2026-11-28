#!/usr/bin/env python3
"""CHECKPOINTS ONLY: score the hidden 20% of the phrase bank. Prints numbers, never sentences.

    python3 tools/score_hidden_bank.py "engine v1 done"

Appends one line to runs/hidden_bank.log. If the visible bank passes but this score is much lower,
the rules were fitted to the visible bank. Don't fix rules from this file - write NEW general
sentences in tests/flag_cases.yaml for the kind of mistake you suspect.
"""
import datetime
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from lantern.matcher import urgency_floor  # noqa: E402

HELDOUT_DIR = os.environ.get("LANTERN_HELDOUT", os.path.join(os.path.dirname(ROOT), "lantern-heldout"))


def main():
    label = " ".join(sys.argv[1:]) or "(no label)"
    with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
        p = json.load(fh)
    with open(os.path.join(HELDOUT_DIR, "flag_cases_hidden.yaml")) as fh:
        bank = yaml.safe_load(fh) or {}
    tot = miss = fa = 0
    for fid, d in bank.items():
        for kind in ("fire", "quiet"):
            for s in d.get(kind, []):
                tot += 1
                hit = fid in {h["id"] for h in urgency_floor(p, s, None)[1]}
                miss += kind == "fire" and not hit
                fa += kind == "quiet" and hit
    line = (f"{datetime.date.today()}  {label}  pathway {p.get('version')}  "
            f"{tot} sentences  {miss} misses  {fa} false alarms  pass {100 * (tot - miss - fa) / max(tot, 1):.0f}%")
    os.makedirs(os.path.join(ROOT, "runs"), exist_ok=True)
    with open(os.path.join(ROOT, "runs", "hidden_bank.log"), "a") as fh:
        fh.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
