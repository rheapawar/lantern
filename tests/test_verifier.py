"""Tests for lantern/verifier.py. Built on the committed fixture case (tests/fixtures.py), so they run on a
fresh clone; uses hand-made answers and a fake provider (no API calls)."""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures  # noqa: E402

from lantern.cases import ROOT  # noqa: E402
from lantern.chart import load_map  # noqa: E402
from lantern.llm import load_config, parse, prepare  # noqa: E402
from lantern.verifier import NEEDS_REVIEW, VERIFIED, call_and_verify, final_urgency, verify  # noqa: E402

with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
    PATHWAY = json.load(fh)
FMAP = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
PREP = prepare(PATHWAY, FMAP, fixtures.case(), load_config())
REASON = "chest_pain"
NOTE_REF = PREP["context"]["note_ref"]


def fact(fid, ref, statement, quote=""):
    return {"fact": fid, "ref": ref, "statement": statement, "quote": quote}


def valid_answer():
    ctx = PREP["context"]
    return {"urgency": PREP["floor"], "urgency_reason": "Worsening exertional chest tightness.",
            "urgency_flags": [h["id"] for h in PREP["flags"]], "summary": "Short summary.",
            "facts": [fact("hypertension", "Condition/htn", "Essential hypertension."),
                      fact("egfr", "Observation/egfr", "eGFR 13.4 on 2024-04-20."),
                      fact("systolic_bp", "Observation/bp", "BP 134/82, 9 months ago."),
                      fact("family_history", NOTE_REF, "Brother had a heart attack at 52.",
                           "Her brother had a heart attack at 52")],
            "tests": [{"test": t["id"], "include": True, "why": "x", "depends_on": []} for t in ctx["tests"]],
            "options": [{"option": o, "relevant": False, "why": "x", "depends_on": []}
                        for o in PATHWAY["reasons"][REASON]["interim_options"]],
            "fit": PATHWAY["reasons"][REASON]["fit_choices"][0], "fit_reason": "x", "missing_info": []}


class FakeProvider:
    def __init__(self, *texts):
        self.texts, self.feedback = list(texts), []

    def call(self, request, feedback=None):
        self.feedback.append(feedback)
        t = self.texts.pop(0)
        if isinstance(t, Exception):
            raise t
        return {"text": t, "model_version": "fake", "seconds": 0, "usage": None}


def check(answer):
    return verify(answer, PREP["request"], PREP["context"], PATHWAY, REASON, PREP["floor"], fixtures.NOTE)


def good():
    return copy.deepcopy(valid_answer())


def errors_with(answer, text):
    return [e for e in check(answer)["errors"] if text in e]


class Shape(unittest.TestCase):
    def test_fixture_floor_is_urgent(self):
        self.assertEqual(PREP["floor"], "urgent")

    def test_valid_answer_passes(self):
        self.assertEqual(check(good())["errors"], [])

    def test_not_json(self):
        self.assertFalse(check(None)["ok"])

    def test_missing_and_extra_tests(self):
        a = good()
        a["tests"].pop()
        self.assertTrue(errors_with(a, "missing"))
        a = good()
        a["tests"].append(dict(a["tests"][0]))
        self.assertTrue(errors_with(a, "more than once"))

    def test_option_not_in_pathway(self):
        a = good()
        a["options"][0]["option"] = "start_new_drug"
        self.assertFalse(check(a)["ok"])


class Citations(unittest.TestCase):
    def test_unknown_ref(self):
        a = good()
        a["facts"][0]["ref"] = "Observation/made-up"
        self.assertTrue(errors_with(a, "Observation/made-up"))          # caught by the schema enum
        # ...and by the citation check itself, if the schema ever lacks the enum
        req = copy.deepcopy(PREP["request"])
        del req["schema"]["properties"]["facts"]["items"]["properties"]["ref"]["enum"]
        errs = verify(a, req, PREP["context"], PATHWAY, REASON, PREP["floor"], fixtures.NOTE)["errors"]
        self.assertTrue([e for e in errs if "does not exist" in e])

    def test_ref_from_another_fact(self):
        a = good()
        a["facts"][0]["ref"] = "Observation/ldl"          # hypertension citing the LDL lab
        self.assertTrue(errors_with(a, "is not a source of fact"))

    def test_right_record_wrong_number(self):
        a = good()
        a["facts"][1]["statement"] = "eGFR 90, normal kidney function."   # record says 13.4
        self.assertTrue(errors_with(a, "number 90"))

    def test_rounding_is_allowed(self):
        a = good()
        a["facts"].append(fact("ldl", "Observation/ldl", "LDL 130 mg/dL (129.7)."))
        self.assertEqual(check(a)["errors"], [])

    def test_wrong_date(self):
        a = good()
        a["facts"][1]["statement"] = "eGFR 13.4 on 2024-09-01."
        self.assertTrue(errors_with(a, "date 2024-09-01"))

    def test_numbers_from_another_fact(self):
        a = good()
        a["facts"][1]["statement"] = "eGFR 13.4; LDL 129.73."               # LDL is not on the eGFR record
        self.assertTrue(errors_with(a, "number 129.73"))

    def test_numbers_inside_text_values(self):
        a = good()
        a["facts"].append(fact("diabetes", "Condition/dm", "Type 2 diabetes since 2018."))
        a["facts"].append(fact("bp_meds", "MedicationRequest/lis", "On lisinopril 10 MG."))
        self.assertEqual(check(a)["errors"], [])


class NoteQuotes(unittest.TestCase):
    def test_note_citation_needs_a_quote(self):
        a = good()
        a["facts"][3]["quote"] = ""
        self.assertTrue(errors_with(a, "gives no quote"))

    def test_quote_must_be_in_the_note(self):
        a = good()
        a["facts"].append(fact("statin", NOTE_REF, "On a statin.", "she takes atorvastatin daily"))
        self.assertTrue(errors_with(a, "is not in the referral note"))

    def test_quote_matching_ignores_case_and_spacing(self):
        a = good()
        a["facts"][3]["quote"] = "her  BROTHER had a heart attack at 52"
        self.assertEqual(check(a)["errors"], [])

    def test_note_numbers_must_be_in_the_quote(self):
        a = good()
        a["facts"][3]["statement"] = "Brother had a heart attack at 55."
        self.assertTrue(errors_with(a, "number 55"))


class Urgency(unittest.TestCase):
    def test_below_floor_is_rejected(self):
        a = good()
        a["urgency"] = "routine"
        self.assertTrue(errors_with(a, "below the red-flag floor"))

    def test_below_own_flag_is_rejected(self):
        a = good()
        a["urgency_flags"] = [PATHWAY["reasons"][REASON]["red_flags"][0]["id"]]
        self.assertTrue(errors_with(a, "below flag"))

    def test_raising_is_allowed_and_final_urgency(self):
        a = good()
        a["urgency"] = "emergent"
        self.assertTrue(check(a)["ok"])
        self.assertEqual(final_urgency(PATHWAY, "urgent", {"urgency": "routine"}), "urgent")
        self.assertEqual(final_urgency(PATHWAY, "urgent", {"urgency": "emergent"}), "emergent")
        self.assertEqual(final_urgency(PATHWAY, "soon", None), "soon")

    def test_long_summary_is_only_a_warning(self):
        a = good()
        a["summary"] = "word " * 30
        c = check(a)
        self.assertTrue(c["ok"])
        self.assertTrue(c["warnings"])


class Retry(unittest.TestCase):
    def test_retry_fixes_it(self):
        bad = good()
        bad["urgency"] = "routine"
        p = FakeProvider(json.dumps(bad), json.dumps(good()))
        out = call_and_verify(p, PREP, PATHWAY, REASON, parse)
        self.assertEqual(out["status"], VERIFIED)
        self.assertEqual(len(out["attempts"]), 2)
        self.assertIn("below the red-flag floor", p.feedback[1])

    def test_two_failures_need_review_and_keep_the_floor(self):
        bad = good()
        bad["urgency"] = "routine"
        out = call_and_verify(FakeProvider(json.dumps(bad), "not json"), PREP, PATHWAY, REASON, parse)
        self.assertEqual(out["status"], NEEDS_REVIEW)
        self.assertEqual(out["urgency"], PREP["floor"])
        self.assertIsNone(out["answer"])

    def test_provider_error_needs_review(self):
        out = call_and_verify(FakeProvider(RuntimeError("quota")), PREP, PATHWAY, REASON, parse)
        self.assertEqual(out["status"], NEEDS_REVIEW)
        self.assertIn("quota", out["attempts"][0]["error"])
