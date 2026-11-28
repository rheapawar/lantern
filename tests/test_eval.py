"""Tests for eval.py on hand-made cards (built with the real build_card from the fixture case) and labels."""
import copy
import json
import os
import sys
import tempfile
import unittest

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import fixtures  # noqa: E402
from test_verifier import PATHWAY, PREP, valid_answer  # noqa: E402

import eval as ev  # noqa: E402
from lantern.card import build_card  # noqa: E402
from lantern.cases import ROOT  # noqa: E402

with open(os.path.join(ROOT, "config", "eval.yaml")) as fh:
    CFG = yaml.safe_load(fh)
PROV = {"run_id": "r", "created_at": "2026-11-28T00:00:00", "pathway_version": "x", "request_hash": "h1",
        "tokens": {"input": 100, "output": 10, "thinking": 5}}


def card(cid, status="verified", final=None, prep=None, **answer_changes):
    """final: the verified outcome's urgency (max(floor, model)); answer_changes edit the model's answer."""
    prep = prep or PREP
    ans = valid_answer()
    ans.update(answer_changes)
    outcome = {"status": status, "answer": ans if status == "verified" else None,
               "urgency": final or prep["floor"], "warnings": [], "attempts": []}
    c = build_card({**fixtures.case(), "id": cid}, prep, outcome, PATHWAY, PROV).model_dump(mode="json")
    return {"case_id": cid, "status": status, "request_hash": "h1", "card": c}


def label(**kw):
    base = {"urgency": "urgent", "fit": PATHWAY["reasons"]["chest_pain"]["fit_choices"][0], "acceptable_fits": [],
            "tests_first": [], "decision_facts": [], "acceptable_options": [], "chart_dependent": False,
            "answer_key_only": {"hooks": []}, "status": "draft", "labeler": "claude-draft (unreviewed)"}
    return {**base, **kw}


def run(recs, labels, manifest_cases=None):
    m = {"run_id": "r1", "cases": manifest_cases or {c: {} for c in recs}}
    with tempfile.TemporaryDirectory() as d:
        return ev.score(m, recs, labels, CFG, runs_root=d)


class Urgency(unittest.TestCase):
    def test_emergent_miss_is_the_first_line(self):
        s = run({"a": card("a")}, {"a": label(urgency="emergent")})
        self.assertEqual(s["metrics"]["emergent_missed"], ["a"])
        first = ev.render(s).splitlines()[0]
        self.assertTrue(first.startswith("**Emergent cases missed: 1 of 1**"), first)
        self.assertIn("FAIL", first)

    def test_under_and_over(self):
        s = run({"a": card("a"), "b": card("b", final="emergent", urgency="emergent")},
                {"a": label(urgency="emergent"), "b": label(urgency="urgent")})
        self.assertEqual(s["metrics"]["any_under_called"], ["a"])
        self.assertEqual(s["metrics"]["over_called"], ["b"])
        self.assertAlmostEqual(s["metrics"]["over_called_rate"], 0.5)

    def test_raised_above_floor_is_reported_separately(self):
        s = run({"a": card("a")}, {"a": label(urgency="urgent")})
        self.assertEqual(s["metrics"]["raised_above_floor"], [])            # echoing the floor adds nothing
        s = run({"a": card("a", final="emergent", urgency="emergent"), "b": card("b", final="emergent", urgency="emergent")},
                {"a": label(urgency="emergent"), "b": label(urgency="urgent")})
        verdicts = {x["case_id"]: x["verdict"] for x in s["metrics"]["raised_above_floor"]}
        self.assertEqual(verdicts, {"a": "right", "b": "over"})


class Statuses(unittest.TestCase):
    def test_manual_review_is_scored_as_a_miss(self):
        s = run({"a": card("a", status="needs_manual_review")},
                {"a": label(tests_first=["ecg"], acceptable_options=["er_precautions"], decision_facts=["egfr"])})
        m = s["metrics"]
        self.assertEqual(s["scored"], 1)
        self.assertEqual((m["tests_first_recall"], m["options_recall"], m["decision_facts_recall"]), (0, 0, 0))
        self.assertEqual(m["fit_correct_rate"], 0)
        self.assertEqual(m["needs_manual_review"], ["a"])

    def test_api_errors_are_not_scored(self):
        s = run({"a": card("a"), "b": card("b", status="error")}, {"a": label(), "b": label()},
                manifest_cases={"a": {}, "b": {}, "c": {}})
        self.assertEqual(s["scored"], 1)
        self.assertEqual([x["case_id"] for x in s["not_scored"]], ["b"])
        self.assertEqual(s["missing"], ["c"])


class Content(unittest.TestCase):
    def test_tests_options_facts_fit(self):
        tests = [{"test": t["id"], "include": t["id"] == "ecg", "why": "x", "depends_on": ["egfr"] if t["id"] == "ecg" else []}
                 for t in PREP["context"]["tests"]]
        opts = [{"option": o, "relevant": o == "er_precautions", "why": "x", "depends_on": []}
                for o in PATHWAY["reasons"]["chest_pain"]["interim_options"]]
        a = card("a", tests=tests, options=opts)
        lab = label(tests_first=["ecg", "a1c"], acceptable_options=["er_precautions", "review_bp_lipid_meds"],
                    decision_facts=["egfr", "hypertension", "smoking"])
        m = run({"a": a}, {"a": lab})["metrics"]
        self.assertEqual(m["tests_first_recall"], 0.5)
        self.assertEqual(m["tests_first_precision"], 1.0)
        self.assertEqual(m["options_recall"], 0.5)
        self.assertAlmostEqual(m["decision_facts_recall"], 2 / 3)     # egfr (depends_on) + hypertension (cited)
        self.assertEqual(m["fit_correct_rate"], 1.0)

    def test_acceptable_fit_counts(self):
        a = card("a", fit=PATHWAY["reasons"]["chest_pain"]["fit_choices"][1])
        lab = label(acceptable_fits=[PATHWAY["reasons"]["chest_pain"]["fit_choices"][1]])
        self.assertEqual(run({"a": a}, {"a": lab})["metrics"]["fit_correct_rate"], 1.0)

    def test_chart_dependent_hooks(self):
        lab = label(chart_dependent=True, answer_key_only={"hooks": ["kidney_disease"]})
        self.assertEqual(run({"a": card("a")}, {"a": lab})["metrics"]["chart_dependent_caught"], ["a"])  # egfr cited
        lab2 = label(chart_dependent=True, answer_key_only={"hooks": ["kidney_disease", "on_amlodipine"]})
        self.assertEqual(run({"a": card("a")}, {"a": lab2})["metrics"]["chart_dependent_caught"], [])    # all hooks needed

    def test_unmapped_hook_fails_loudly(self):
        with self.assertRaises(KeyError):
            run({"a": card("a")}, {"a": label(answer_key_only={"hooks": ["mystery_hook"]})})

    def test_citations_are_rechecked_on_the_saved_card(self):
        a = card("a")
        self.assertEqual(run({"a": a}, {"a": label()})["metrics"]["citations_valid_rate"], 1.0)
        bad = copy.deepcopy(a)
        bad["card"]["cited_facts"][0]["ref"] = "Observation/ldl"     # hypertension citing the LDL lab
        self.assertEqual(run({"a": bad}, {"a": label()})["metrics"]["citations_valid_rate"], 0.0)


class Determinism(unittest.TestCase):
    def test_same_code_different_request_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            same = {"git_commit": "c", "diff_hash": None, "prompt_hash": "p", "pathway_hash": "w",
                    "config_hash": "k", "fhir_map_hash": "f"}
            os.makedirs(os.path.join(d, "old"))
            with open(os.path.join(d, "old", "manifest.json"), "w") as fh:
                json.dump({**same, "run_id": "old", "cases": {"a": {"request_hash": "DIFFERENT"}}}, fh)
            out = ev.determinism({**same, "run_id": "new"}, {"a": card("a")}, d)
            self.assertEqual(out, [{"case_id": "a", "other_run": "old"}])
            out = ev.determinism({**same, "git_commit": "other", "run_id": "new"}, {"a": card("a")}, d)
            self.assertEqual(out, [])                                 # different code: not compared


class LabelWarning(unittest.TestCase):
    def test_draft_labels_are_flagged_on_the_scorecard(self):
        md = ev.render(run({"a": card("a")}, {"a": label()}))
        self.assertIn("unreviewed drafts", md)
