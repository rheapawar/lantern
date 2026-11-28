"""Tests for lantern/verifier.py with hand-made answers and a fake provider (no API calls)."""
import copy
import json
import os
import unittest

from lantern.cases import ROOT, load_case, training_ids
from lantern.chart import load_map
from lantern.llm import load_config, parse, prepare
from lantern.verifier import NEEDS_REVIEW, VERIFIED, call_and_verify, final_urgency, verify

with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
    PATHWAY = json.load(fh)
FMAP = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
CFG = load_config()


def valid_answer(prep, reason):
    """A correct answer built from the case itself: cites real refs, every test/option once."""
    ctx = prep["context"]
    facts = [{"fact": f["id"], "ref": f["items"][0]["ref"], "statement": f["text"]}
             for f in ctx["facts"].values() if f["found"]][:3]
    return {"urgency": prep["floor"], "urgency_reason": "x", "urgency_flags": [h["id"] for h in prep["flags"]],
            "summary": "Short summary.", "facts": facts,
            "tests": [{"test": t["id"], "include": True, "why": "x", "depends_on": []} for t in ctx["tests"]],
            "options": [{"option": o, "relevant": False, "why": "x", "depends_on": []}
                        for o in PATHWAY["reasons"][reason]["interim_options"]],
            "fit": PATHWAY["reasons"][reason]["fit_choices"][0], "fit_reason": "x", "missing_info": []}


class FakeProvider:
    def __init__(self, *texts):
        self.texts, self.feedback = list(texts), []

    def call(self, request, feedback=None):
        self.feedback.append(feedback)
        t = self.texts.pop(0)
        if isinstance(t, Exception):
            raise t
        return {"text": t, "model_version": "fake", "seconds": 0, "usage": None}


@unittest.skipUnless(training_ids(), "no cases/*/bundle.json (gitignored) - run build_cases.py")
class Verifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # an urgent-floor case so 'below the floor' can be tested
        for cid in training_ids():
            case = load_case(cid)
            prep = prepare(PATHWAY, FMAP, case, CFG)
            if prep["floor"] == "urgent":
                cls.case, cls.prep, cls.reason = case, prep, case["meta"]["reason"]
                break

    def check(self, answer):
        return verify(answer, self.prep["request"], self.prep["context"], PATHWAY, self.reason, self.prep["floor"])

    def good(self):
        return copy.deepcopy(valid_answer(self.prep, self.reason))

    def test_valid_answer_passes(self):
        self.assertEqual(self.check(self.good())["errors"], [])

    def test_not_json(self):
        self.assertFalse(self.check(None)["ok"])

    def test_unknown_ref(self):
        a = self.good()
        a["facts"][0]["ref"] = "Observation/made-up"
        self.assertFalse(self.check(a)["ok"])

    def test_ref_from_another_fact(self):
        a = self.good()
        other = next(f for f in self.prep["context"]["facts"].values()
                     if f["found"] and f["id"] != a["facts"][0]["fact"]
                     and f["items"][0]["ref"] not in {i["ref"] for i in self.prep["context"]["facts"][a["facts"][0]["fact"]]["items"]})
        a["facts"][0]["ref"] = other["items"][0]["ref"]
        errs = self.check(a)["errors"]
        self.assertTrue(any("is not a source of fact" in e for e in errs), errs)

    def test_note_ref_backs_any_fact(self):
        a = self.good()
        a["facts"][0]["ref"] = self.prep["context"]["note_ref"]
        self.assertTrue(self.check(a)["ok"])

    def test_missing_and_extra_tests(self):
        a = self.good()
        a["tests"].pop()
        self.assertTrue(any("missing" in e for e in self.check(a)["errors"]))
        a = self.good()
        a["tests"].append(dict(a["tests"][0]))
        self.assertTrue(any("more than once" in e for e in self.check(a)["errors"]))

    def test_option_not_in_pathway(self):
        a = self.good()
        a["options"][0]["option"] = "start_new_drug"
        self.assertFalse(self.check(a)["ok"])

    def test_below_floor_is_rejected(self):
        a = self.good()
        a["urgency"] = "routine"
        self.assertTrue(any("below the red-flag floor" in e for e in self.check(a)["errors"]))

    def test_below_own_flag_is_rejected(self):
        a = self.good()
        red = PATHWAY["reasons"][self.reason]["red_flags"][0]["id"]
        a["urgency_flags"] = [red]
        self.assertTrue(any("below flag" in e for e in self.check(a)["errors"]))

    def test_raising_is_allowed_and_final_urgency(self):
        a = self.good()
        a["urgency"] = "emergent"
        self.assertTrue(self.check(a)["ok"])
        self.assertEqual(final_urgency(PATHWAY, "urgent", {"urgency": "routine"}), "urgent")
        self.assertEqual(final_urgency(PATHWAY, "urgent", {"urgency": "emergent"}), "emergent")
        self.assertEqual(final_urgency(PATHWAY, "soon", None), "soon")

    def test_long_summary_is_only_a_warning(self):
        a = self.good()
        a["summary"] = "word " * 30
        c = self.check(a)
        self.assertTrue(c["ok"])
        self.assertTrue(c["warnings"])

    def test_retry_fixes_it(self):
        bad = self.good()
        bad["urgency"] = "routine"
        p = FakeProvider(json.dumps(bad), json.dumps(self.good()))
        out = call_and_verify(p, self.prep, PATHWAY, self.reason, parse)
        self.assertEqual(out["status"], VERIFIED)
        self.assertEqual(len(out["attempts"]), 2)
        self.assertIn("below the red-flag floor", p.feedback[1])       # the errors were sent back

    def test_two_failures_need_review_and_keep_the_floor(self):
        bad = self.good()
        bad["urgency"] = "routine"
        out = call_and_verify(FakeProvider(json.dumps(bad), "not json"), self.prep, PATHWAY, self.reason, parse)
        self.assertEqual(out["status"], NEEDS_REVIEW)
        self.assertEqual(out["urgency"], self.prep["floor"])
        self.assertIsNone(out["answer"])

    def test_provider_error_needs_review(self):
        out = call_and_verify(FakeProvider(RuntimeError("quota")), self.prep, PATHWAY, self.reason, parse)
        self.assertEqual(out["status"], NEEDS_REVIEW)
        self.assertIn("quota", out["attempts"][0]["error"])
