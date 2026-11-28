"""Tests for lantern/cases.py: held-out loading. Uses a temporary LANTERN_HELDOUT, never ../lantern-heldout."""
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures  # noqa: E402

from lantern import cases  # noqa: E402


class HeldOutLoading(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = os.path.join(self.tmp.name, "h001")
        os.makedirs(d)
        c = fixtures.case()
        for name, content in (("meta.json", json.dumps({**c["meta"], "case_id": "h001"})),
                              ("bundle.json", json.dumps(c["bundle"])), ("referral.txt", c["note"]),
                              ("label.json", json.dumps({"urgency": "urgent"}))):
            with open(os.path.join(d, name), "w") as fh:
                fh.write(content)
        self.env = mock.patch.dict(os.environ, {"LANTERN_HELDOUT": self.tmp.name})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_external_case_refused_without_final(self):
        with self.assertRaises(cases.HeldOutError):
            cases.load_case("h001")

    def test_external_case_loads_from_lantern_heldout_with_final(self):
        c = cases.load_case("h001", final=True)
        self.assertEqual(c["meta"]["case_id"], "h001")
        self.assertEqual(c["note"], fixtures.NOTE)
        self.assertNotIn("label", c)                       # the engine never gets the answer key

    def test_final_ids_include_the_external_set(self):
        self.assertIn("h001", cases.final_ids())

    def test_unknown_id_is_refused_not_a_file_error(self):
        with self.assertRaises(cases.HeldOutError):
            cases.load_case("zz999")

    def test_in_repo_heldout_refused_without_final(self):
        for cid in sorted(cases.heldout_ids())[:1]:
            with self.assertRaises(cases.HeldOutError):
                cases.load_case(cid)
            self.assertEqual(cases.case_dir(cid, final=True), os.path.join(cases.CASES, cid))

    def test_training_ids_never_include_heldout(self):
        self.assertFalse(set(cases.training_ids()) & cases.heldout_ids())
        self.assertFalse([c for c in cases.training_ids() if c.startswith("h")])
