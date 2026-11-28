"""Load a case for the engine: meta, cut bundle and referral note. Never label.json (that is the answer key).

Held-out cases (cases/plan.csv heldout=True) are refused unless final=True, so tuning can't touch them
by accident (overfitting guard, CLAUDE.md).
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "cases")


class HeldOutError(PermissionError):
    pass


def _read(path):
    with open(path) as fh:
        return fh.read()


def plan_rows():
    with open(os.path.join(CASES, "plan.csv")) as fh:
        return list(csv.DictReader(fh))


def heldout_ids():
    return {r["case_id"] for r in plan_rows() if r["heldout"] == "True"}


def training_ids():
    """Non-held-out cases that have a bundle and a referral note."""
    out = []
    for r in plan_rows():
        d = os.path.join(CASES, r["case_id"])
        if r["heldout"] != "True" and os.path.exists(os.path.join(d, "bundle.json")) \
                and os.path.exists(os.path.join(d, "referral.txt")):
            out.append(r["case_id"])
    return out


def load_case(case_id, final=False):
    """{'id', 'meta', 'bundle', 'note'} - the only inputs the engine may see."""
    if case_id in heldout_ids() and not final:
        raise HeldOutError(f"{case_id} is held out; it is scored only in the final run (final=True)")
    d = os.path.join(CASES, case_id)
    return {"id": case_id, "meta": json.loads(_read(os.path.join(d, "meta.json"))),
            "bundle": json.loads(_read(os.path.join(d, "bundle.json"))),
            "note": _read(os.path.join(d, "referral.txt"))}
