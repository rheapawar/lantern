"""Tests for lantern/retriever.py: chart context with citations, test status, and the referral-date cutoff.

Held-out cases are never read here (overfitting guard, CLAUDE.md).
"""
import csv
import json
import os
import unittest

from lantern.chart import load_map
from lantern.retriever import FutureDataError, ago, cited_refs, retrieve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(path):
    with open(path) as fh:
        return fh.read()


def _load(path):
    return json.loads(_read(path))


PATHWAY = _load(os.path.join(ROOT, "pathways", "cardiology.json"))
FMAP = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
REF = "2026-06-01"


def bundle(*rs):
    entries = []
    for i, r in enumerate(rs):
        r = {**r, "id": f"r{i}"}
        entries.append({"fullUrl": f"urn:uuid:r{i}", "resource": r})
    return {"resourceType": "Bundle", "entry": entries}


def obs(code, value, when):
    return {"resourceType": "Observation", "effectiveDateTime": when,
            "code": {"coding": [{"code": code}]}, "valueQuantity": {"value": value, "unit": "x"}}


PATIENT = {"resourceType": "Patient", "birthDate": "1960-06-02", "gender": "female"}
NOTE_SR = {"resourceType": "ServiceRequest", "authoredOn": REF}


class Synthetic(unittest.TestCase):
    def ctx(self, *rs, reason="chest_pain", note=""):
        return retrieve(PATHWAY, FMAP, bundle(PATIENT, NOTE_SR, *rs), REF, reason, note)

    def test_age_is_on_the_referral_date(self):
        self.assertEqual(self.ctx()["facts"]["age"]["items"][0]["value"], 65)   # birthday is the day after

    def test_every_item_is_cited(self):
        c = self.ctx({"resourceType": "Condition", "onsetDateTime": "2015-01-01",
                      "code": {"text": "Essential hypertension (disorder)"}}, obs("18262-6", 160, "2026-01-01"))
        self.assertTrue(c["facts"]["hypertension"]["found"])
        self.assertEqual(c["facts"]["ldl"]["items"][0]["ref"], "Observation/r3")
        for f in c["facts"].values():
            for it in f["items"]:
                self.assertIn("ref", it)
        self.assertIn("Observation/r3", cited_refs(c))

    def test_resolved_conditions_and_findings_are_not_facts(self):
        c = self.ctx({"resourceType": "Condition", "onsetDateTime": "2020-01-01", "abatementDateTime": "2020-02-01",
                      "code": {"text": "Chronic kidney disease stage 3 (disorder)"}},
                     {"resourceType": "Condition", "onsetDateTime": "2020-01-01",
                      "code": {"text": "Abnormal findings coronary (finding)"}})
        self.assertFalse(c["facts"]["ckd"]["found"])
        self.assertFalse(c["facts"]["prior_mi_cad"]["found"])

    def test_note_only_facts_point_at_the_referral(self):
        f = self.ctx()["facts"]["family_history"]
        self.assertFalse(f["found"])
        self.assertEqual(f["items"][0]["ref"], "ServiceRequest/r1")

    def test_test_status_uses_valid_days(self):
        vd = PATHWAY["tests"]["lipids"]["recency"]["valid_days"]
        inside = self.ctx(obs("18262-6", 120, "2026-05-01"))
        old = self.ctx(obs("18262-6", 120, "2020-05-01"))
        status = lambda c, t: next(x for x in c["tests"] if x["id"] == t)
        self.assertEqual(status(inside, "lipids")["status"], "done")
        self.assertEqual(status(old, "lipids")["status"], "out_of_date")
        self.assertGreater(status(old, "lipids")["last"]["days_ago"], vd)
        self.assertEqual(status(old, "lipids")["last"]["ago"], "6 years ago")   # shown with its age, still listed
        self.assertEqual(status(inside, "ecg")["status"], "not_done")
        self.assertEqual(status(inside, "ccta")["status"], "not_recorded_in_source")

    def test_prechecked_follows_the_pathway(self):
        c = self.ctx()
        pre = {t["id"]: t["prechecked"] for t in c["tests"]}
        not_pre = set(PATHWAY["reasons"]["chest_pain"].get("tests_not_prechecked", []))
        self.assertEqual({t for t, p in pre.items() if not p}, not_pre)
        self.assertEqual(len(pre), len(c["tests"]))                    # each test listed once

    def test_refuses_a_bundle_with_future_data(self):
        with self.assertRaises(FutureDataError):
            self.ctx(obs("18262-6", 120, "2026-06-02"))

    def test_ago(self):
        self.assertEqual([ago(0), ago(1), ago(12), ago(400), ago(1000)],
                         ["today", "1 day ago", "12 days ago", "13 months ago", "3 years ago"])


class TrainingCases(unittest.TestCase):
    """Every non-held-out case: retrieval works, nothing after the referral date, every citation is real."""

    def test_training_cases(self):
        with open(os.path.join(ROOT, "cases", "plan.csv")) as fh:
            plan = [r for r in csv.DictReader(fh) if r["heldout"] != "True"]
        checked = 0
        for row in plan:
            d = os.path.join(ROOT, "cases", row["case_id"])
            if not os.path.exists(os.path.join(d, "bundle.json")):
                continue
            meta = _load(os.path.join(d, "meta.json"))
            b = _load(os.path.join(d, "bundle.json"))
            c = retrieve(PATHWAY, FMAP, b, meta["referral_date"], meta["reason"],
                         _read(os.path.join(d, "referral.txt")))
            ids = {f"{e['resource']['resourceType']}/{e['resource'].get('id')}" for e in b["entry"]}
            self.assertLessEqual(cited_refs(c), ids, row["case_id"])
            for f in c["facts"].values():
                for it in f["items"]:
                    self.assertLessEqual(it.get("date") or "", meta["referral_date"], (row["case_id"], f["id"]))
            checked += 1
        if checked == 0:
            self.skipTest("no cases/*/bundle.json (gitignored) - run build_cases.py; nothing was checked")
        print(f"\n  retriever: {checked} training cases checked", end=" ")
