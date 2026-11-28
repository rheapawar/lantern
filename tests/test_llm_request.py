"""Tests for the LLM request (no API calls): every training case builds a valid, leak-free request.

Held-out cases are never loaded here (overfitting guard, CLAUDE.md).
"""
import json
import os
import re
import unittest

from lantern.cases import HeldOutError, ROOT, heldout_ids, load_case, training_ids
from lantern.chart import load_map
from lantern.llm import load_config, output_schema, prepare, request_hash

with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
    PATHWAY = json.load(fh)
FMAP = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
CFG = load_config()
DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
# answer-key words that must never reach the model
LEAKS = ("later_dx", "answer_key", "acceptable_options", "acceptable_fits", "urgency_rationale", "planned_tier",
         "chart_hook_expectation", "heldout")


class Requests(unittest.TestCase):
    def test_heldout_cases_are_refused(self):
        for cid in sorted(heldout_ids())[:1]:
            with self.assertRaises(HeldOutError):
                load_case(cid)

    def test_every_training_case(self):
        ids = training_ids()
        if not ids:
            self.skipTest("no cases/*/bundle.json (gitignored) - run build_cases.py; nothing was checked")
        for cid in ids:
            case = load_case(cid)
            prep = prepare(PATHWAY, FMAP, case, CFG)
            req = prep["request"]
            cut = case["meta"]["referral_date"]
            text = req["system"] + req["user"]
            later = [d for d in DATE.findall(text) if d > cut]
            self.assertEqual([], later, f"{cid}: dates after the referral reached the prompt")
            for w in LEAKS:
                self.assertNotIn(w, text, f"{cid}: answer-key field '{w}' in the prompt")
            for name, prop in req["schema"]["properties"].items():
                for e in [prop] + [prop.get("items", {})] + list(prop.get("items", {}).get("properties", {}).values()):
                    if "enum" in e:
                        self.assertTrue(e["enum"], f"{cid}: empty enum in {name}")
            self.assertEqual(request_hash(req), request_hash(prepare(PATHWAY, FMAP, case, CFG)["request"]),
                             f"{cid}: request is not deterministic")

    def test_schema_offers_only_pathway_ids(self):
        case = load_case(training_ids()[0]) if training_ids() else None
        if case is None:
            self.skipTest("no cases")
        ctx = prepare(PATHWAY, FMAP, case, CFG)["context"]
        sch = output_schema(PATHWAY, case["meta"]["reason"], ctx)
        r = PATHWAY["reasons"][case["meta"]["reason"]]
        self.assertEqual(set(sch["properties"]["fit"]["enum"]), set(r["fit_choices"]))
        self.assertEqual(set(sch["properties"]["options"]["items"]["properties"]["option"]["enum"]),
                         set(r["interim_options"]))
        self.assertEqual(sch["properties"]["urgency"]["enum"], sorted(PATHWAY["tier_order"]))
        self.assertNotIn("plan", sch["properties"])          # the model never writes the plan
