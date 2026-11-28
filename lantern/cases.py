"""Load a case for the engine: meta, cut bundle and referral note. Never label.json (that is the answer key).

Two kinds of held-out case, both refused unless final=True (overfitting guard, CLAUDE.md):
  - in-repo cases marked heldout=True in cases/plan.csv;
  - the fresh held-out set h001-h010, which lives OUTSIDE the repo in LANTERN_HELDOUT
    (default ../lantern-heldout, same layout as cases/: <id>/meta.json, bundle.json, referral.txt).
Nothing here reads, lists or even checks the held-out directory unless final=True.
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "cases")


class HeldOutError(PermissionError):
    pass


def heldout_dir():
    return os.environ.get("LANTERN_HELDOUT", os.path.join(os.path.dirname(ROOT), "lantern-heldout"))


def _read(path):
    with open(path) as fh:
        return fh.read()


def plan_rows():
    with open(os.path.join(CASES, "plan.csv")) as fh:
        return list(csv.DictReader(fh))


def heldout_ids():
    """In-repo held-out case ids (cases/plan.csv). The external set is never listed here."""
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


def final_ids():
    """Every held-out case for the final run: in-repo held-out + the external set. Lists the external
    directory, so call it only from the final run."""
    ids = sorted(heldout_ids())
    d = heldout_dir()
    if os.path.isdir(d):
        ids += sorted(c for c in os.listdir(d) if os.path.exists(os.path.join(d, c, "referral.txt"))
                      and os.path.exists(os.path.join(d, c, "bundle.json")))
    return ids


def case_dir(case_id, final=False):
    """Where a case lives. In-repo training cases need no flag; anything held out needs final=True."""
    in_repo = os.path.join(CASES, case_id)
    if case_id in heldout_ids():
        if not final:
            raise HeldOutError(f"{case_id} is held out; it is scored only in the final run (final=True)")
        return in_repo
    if os.path.isdir(in_repo):
        return in_repo
    if not final:
        raise HeldOutError(f"{case_id} is not a training case; held-out cases load only with final=True")
    return os.path.join(heldout_dir(), case_id)


def load_case(case_id, final=False):
    """{'id', 'meta', 'bundle', 'note'} - the only inputs the engine may see."""
    d = case_dir(case_id, final)
    return {"id": case_id, "meta": json.loads(_read(os.path.join(d, "meta.json"))),
            "bundle": json.loads(_read(os.path.join(d, "bundle.json"))),
            "note": _read(os.path.join(d, "referral.txt"))}
