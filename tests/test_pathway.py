"""Checks every pathways/<specialty>.json against the schema and its own cross-references.

Run:  python3 -m unittest discover -s tests -v
Needs: jsonschema, pyyaml.
"""
import glob
import json
import os
import re
import unittest

import jsonschema
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _load(path):
    with open(path) as fh:
        return yaml.safe_load(fh) if path.endswith(".yaml") else json.load(fh)


SCHEMA = _load(os.path.join(ROOT, "pathways", "schema.json"))
PATHWAYS = sorted(p for p in glob.glob(os.path.join(ROOT, "pathways", "*.json")) if not p.endswith("schema.json"))
FHIR_MAP = _load(os.path.join(ROOT, "config", "fhir_map.yaml"))
NOTE_METRICS = _load(os.path.join(ROOT, "config", "note_metrics.yaml"))
LOOKUP_KINDS = {"loinc", "procedure_sct", "conditions", "meds", "age", "sex", "smoking", "referral_text"}
REQUIRED_TIERS = ["emergent", "urgent", "soon", "routine"]
FLAG_LISTS = ["red_flags", "urgent_flags", "soon_flags", "card_hints"]


def conds(x):
    """Yield every leaf condition inside a match / only_if / if tree."""
    for k, v in x.items():
        if k in ("all", "any"):
            for c in v:
                yield from conds(c)
        elif k == "not":
            yield from conds(v)
        else:
            yield k, v


class PathwayFile(unittest.TestCase):
    path = None

    @classmethod
    def setUpClass(cls):
        if cls.path is None:
            raise unittest.SkipTest("base class")
        cls.p = _load(cls.path)
        cls.reasons = cls.p["reasons"]

    def sourced_items(self):
        """(where, item) for everything that must carry a source."""
        for rid, r in self.reasons.items():
            for k in FLAG_LISTS:
                for f in r.get(k, []):
                    yield f"{rid}.{k}.{f['id']}", f
            for t in r["tests_first"]:
                yield f"{rid}.tests_first.{t['test']}", t
            for g in r["decision_facts"]:
                yield f"{rid}.decision_facts[{g['group'][:30]}]", g
            for rr in r.get("routing_rules", []):
                yield f"{rid}.routing_rules.{rr['id']}", rr
        for oid, o in self.p["options"].items():
            yield f"options.{oid}", o
        for tid, t in self.p["tests"].items():
            yield f"tests.{tid}.recency", t["recency"]

    def all_conditions(self):
        for rid, r in self.reasons.items():
            for k in FLAG_LISTS:
                for f in r.get(k, []):
                    yield f"{rid}.{f['id']}", f["match"]
            for t in r["tests_first"]:
                if "only_if" in t:
                    yield f"{rid}.{t['test']}.only_if", t["only_if"]
            for rr in r.get("routing_rules", []):
                yield f"{rid}.{rr['id']}", rr["if"]

    # --- shape -------------------------------------------------------------
    def test_schema(self):
        errors = sorted(jsonschema.Draft202012Validator(SCHEMA).iter_errors(self.p), key=lambda e: list(e.path))
        self.assertEqual([], [f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors])

    # --- tiers and fits ----------------------------------------------------
    def test_tiers(self):
        self.assertEqual(self.p["tier_order"], REQUIRED_TIERS)
        self.assertEqual(set(self.p["tiers"]), set(REQUIRED_TIERS))

    def test_fits(self):
        fits = set(self.p["fits"])
        for rid, r in self.reasons.items():
            with self.subTest(reason=rid):
                self.assertLessEqual(set(r["fit_choices"]), fits)
                self.assertIn(r["subspecialty"], r["fit_choices"])
                for rr in r.get("routing_rules", []):
                    if rr["suggest_fit"] is not None:
                        self.assertIn(rr["suggest_fit"], r["fit_choices"], rr["id"])

    # --- sources -----------------------------------------------------------
    def test_every_item_has_a_known_source(self):
        known = set(self.p["sources"])
        for where, item in self.sourced_items():
            with self.subTest(item=where):
                self.assertIn("source", item, "missing source")
                self.assertIn(item["source"], known)
                if "stale_if_source" in item:
                    self.assertIn(item["stale_if_source"], known)
        for rid, r in self.reasons.items():
            self.assertLessEqual(set(r["sources"]), known, rid)

    # --- ids and references ------------------------------------------------
    def test_ids_unique(self):
        seen = {}
        for rid, r in self.reasons.items():
            for k in FLAG_LISTS + ["routing_rules"]:
                for f in r.get(k, []):
                    self.assertNotIn(f["id"], seen, f"{f['id']} in {rid} and {seen.get(f['id'])}")
                    seen[f["id"]] = rid

    def test_tests_exist(self):
        tests = set(self.p["tests"])
        for rid, r in self.reasons.items():
            with self.subTest(reason=rid):
                listed = [t["test"] for t in r["tests_first"]]
                self.assertLessEqual(set(listed), tests)
                self.assertEqual(len(listed), len(set(listed)), "duplicate test")
                self.assertLessEqual(set(r.get("tests_not_prechecked", [])), set(listed))

    def test_options_exist(self):
        for rid, r in self.reasons.items():
            self.assertLessEqual(set(r["interim_options"]), set(self.p["options"]), rid)

    def test_decision_facts_exist(self):
        facts = set(self.p["facts"])
        for rid, r in self.reasons.items():
            for g in r["decision_facts"]:
                self.assertLessEqual(set(g["facts"]), facts, f"{rid}: {g['group']}")
        for oid, o in self.p["options"].items():
            for g in o["decision_facts"]:
                self.assertLessEqual(set(g["facts"]), facts, oid)

    def test_option_facts_shown_by_reason(self):
        """Facilitate, don't draft: every fact an option depends on must be on the card for that reason."""
        for rid, r in self.reasons.items():
            shown = {f for g in r["decision_facts"] for f in g["facts"]}
            for oid in r["interim_options"]:
                needed = {f for g in self.p["options"][oid]["decision_facts"] for f in g["facts"]}
                with self.subTest(reason=rid, option=oid):
                    self.assertEqual(set(), needed - shown)

    def test_conditions_reference_real_facts_and_compile(self):
        facts = set(self.p["facts"])
        for where, c in self.all_conditions():
            for kind, v in conds(c):
                with self.subTest(cond=where, kind=kind):
                    if kind == "fact_present":
                        self.assertIn(v, facts)
                    elif kind in ("chart_obs", "fact_count"):
                        self.assertIn(v["fact"], facts)
                        if v.get("range"):
                            self.assertLess(v["range"][0], v["range"][1])
                    elif kind == "text_obs":
                        self.assertIn(v["fact"], NOTE_METRICS["metrics"], "text_obs fact missing from config/note_metrics.yaml")
                    elif kind == "text_regex":
                        re.compile(v)
                    elif kind == "text_any":
                        self.assertEqual(v, [s.lower() for s in v], "text_any phrases must be lowercase")

    # --- FHIR map ----------------------------------------------------------
    def test_fhir_map_covers_everything(self):
        for section in ("tests", "facts"):
            with self.subTest(section=section):
                self.assertEqual(set(self.p[section]) - set(FHIR_MAP[section]), set(), "missing from fhir_map")
                self.assertEqual(set(FHIR_MAP[section]) - set(self.p[section]), set(), "in fhir_map but unused")

    def test_fhir_map_lookup_kinds(self):
        for section in ("tests", "facts"):
            for k, v in FHIR_MAP[section].items():
                self.assertIsInstance(v, dict, k)
                self.assertLessEqual(set(v), LOOKUP_KINDS, k)


# One concrete TestCase per pathway file, so a future neurology.json is checked automatically.
for _path in PATHWAYS:
    _name = "Test_" + os.path.splitext(os.path.basename(_path))[0]
    globals()[_name] = type(_name, (PathwayFile,), {"path": _path})

if __name__ == "__main__":
    unittest.main()
