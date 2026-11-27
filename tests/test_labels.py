"""Checks cases/plan.csv and every cases/<id>/label.json against the schema and the pathway ids.

Labels with status 'todo' only need the right shape; 'done'/'reviewed' labels must be complete
and use real pathway ids. Run:  python3 -m unittest discover -s tests -v
"""
import csv
import glob
import json
import os
import unittest

import jsonschema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "cases")
STYLES = {"standard", "terse", "rambling", "econsult_4_fields"}
QUESTION_TYPES = None  # read from the label schema


def _json(path):
    with open(path) as fh:
        return json.load(fh)


SCHEMA = _json(os.path.join(CASES, "label.schema.json"))
QUESTION_TYPES = set(SCHEMA["properties"]["planned_question_type"]["enum"])
LABELS = sorted(glob.glob(os.path.join(CASES, "c*", "label.json")))


def pathway(specialty="cardiology"):
    return _json(os.path.join(ROOT, "pathways", f"{specialty}.json"))


class Labels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = pathway()
        cls.flag_ids = {f["id"] for r in cls.p["reasons"].values()
                        for k in ("red_flags", "urgent_flags", "soon_flags") for f in r.get(k, [])}
        with open(os.path.join(ROOT, "selection", "shortlist.csv")) as fh:
            cls.shortlist = {r["case_id"]: r for r in csv.DictReader(fh)}

    def test_every_shortlisted_case_has_a_label(self):
        have = {os.path.basename(os.path.dirname(p)) for p in LABELS}
        self.assertEqual(set(self.shortlist) - have, set(), "run build_cases.py")

    def test_plan(self):
        with open(os.path.join(CASES, "plan.csv")) as fh:
            plan = list(csv.DictReader(fh))
        self.assertEqual({r["case_id"] for r in plan}, set(self.shortlist))
        for r in plan:
            with self.subTest(case=r["case_id"]):
                self.assertIn(r["planned_tier"], self.p["tier_order"])
                self.assertIn(r["style"], STYLES)
                self.assertIn(r["question_type"], QUESTION_TYPES)
                self.assertEqual(r["reason"], self.shortlist[r["case_id"]]["reason"])
                self.assertTrue(r["note_must_convey"].strip())

    def test_labels(self):
        validator = jsonschema.Draft202012Validator(SCHEMA)
        counts = {}
        for path in LABELS:
            lab = _json(path)
            cid = os.path.basename(os.path.dirname(path))
            counts[lab.get("status")] = counts.get(lab.get("status"), 0) + 1
            with self.subTest(case=cid):
                errs = [f"{'/'.join(map(str, e.path))}: {e.message}" for e in validator.iter_errors(lab)]
                self.assertEqual([], errs)
                self.assertEqual(lab["case_id"], cid)
                self.assertEqual(lab["reason"], self.shortlist[cid]["reason"])
                self.assertEqual(lab["heldout"], self.shortlist[cid]["heldout"] == "True")
                # ids, checked whenever they are filled in (also on todo labels)
                if lab["urgency"] is not None:
                    self.assertIn(lab["urgency"], self.p["tier_order"])
                self.assertLessEqual(set(lab["urgency_flags"]), self.flag_ids)
                self.assertLessEqual(set(lab["tests_first"]), set(self.p["tests"]))
                self.assertLessEqual(set(lab["acceptable_options"]), set(self.p["options"]))
                self.assertLessEqual(set(lab["decision_facts"]), set(self.p["facts"]))
                for f in [lab["fit"]] + lab["acceptable_fits"]:
                    if f is not None:
                        self.assertIn(f, self.p["reasons"][lab["reason"]]["fit_choices"])
                if lab["status"] != "todo" and lab["chart_dependent"]:
                    self.assertTrue(lab["chart_hook_expectation"].strip(), "say what Lantern should do with the hook")
        print(f"\n  labels: {counts}", end=" ")


if __name__ == "__main__":
    unittest.main()
