"""Card contract (lantern/card.py) on the committed synthetic case - runs on a fresh clone, no API calls."""
import json
import os
import unittest

from lantern.card import Card, build_card, queue_sort_key
from lantern.cases import ROOT
from lantern.chart import load_map
from lantern.llm import load_config, prepare
from tests import fixtures

P = json.load(open(os.path.join(ROOT, "pathways", "cardiology.json")))
F = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
PROV = {"run_id": "test", "created_at": "2026-11-28T00:00:00", "pathway_version": P["version"], "model": "fake"}


class CardContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = fixtures.case()
        cls.prep = prepare(P, F, cls.case, load_config())
        r = P["reasons"][cls.case["meta"]["reason"]]
        ctx = cls.prep["context"]
        cls.answer = {
            "urgency": "emergent", "urgency_reason": "x", "urgency_flags": [], "summary": "s", "facts": [],
            "tests": [{"test": t["id"], "include": False, "why": "y", "depends_on": []} for t in ctx["tests"]],
            "options": [{"option": o, "relevant": True, "why": "z", "depends_on": []} for o in r["interim_options"]],
            "fit": r["fit_choices"][0], "fit_reason": "f", "missing_info": []}

    def card(self, outcome):
        c = build_card(self.case, self.prep, outcome, P, PROV)
        return Card.model_validate_json(c.model_dump_json())       # round-trips through JSON like the DB/API

    def test_verified_raise(self):
        c = self.card({"status": "verified", "answer": self.answer, "urgency": "emergent", "warnings": [],
                       "attempts": [{"n": 1}]})
        self.assertEqual((c.urgency.final, c.urgency.set_by, c.urgency.advise_er), ("emergent", "model", True))
        self.assertEqual(c.urgency.floor, self.prep["floor"])
        self.assertFalse(c.tests[0].include)
        self.assertTrue(c.tests[0].prechecked)          # code's pre-check survives the model's suggestion

    def test_review_and_error_fall_back_to_code(self):
        for status in ("needs_manual_review", "error"):
            c = self.card({"status": status, "answer": self.answer, "urgency": "emergent",
                           "attempts": [{"n": 1, "check": {"errors": ["bad ref"]}}]})
            self.assertEqual(c.urgency.final, self.prep["floor"])
            self.assertIsNone(c.urgency.model)
            self.assertIsNone(c.summary)
            self.assertTrue(all(t.include is None for t in c.tests))
            self.assertTrue(all(o.relevant is None for o in c.options))
            self.assertTrue(c.urgency.checklist_flags)          # flags always come from code

    def test_queue_order(self):
        v = self.card({"status": "verified", "answer": self.answer, "urgency": "emergent", "attempts": []})
        e = self.card({"status": "error", "attempts": []})
        self.assertLess(queue_sort_key(v, 1), queue_sort_key(e, 30))


if __name__ == "__main__":
    unittest.main()
