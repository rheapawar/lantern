"""Tests for lantern/pipeline.py with a fake model on the committed fixture case (no API, no Synthea data)."""
import copy
import json
import os
import sys
import tempfile
import threading
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures  # noqa: E402
from test_verifier import PATHWAY, PREP, valid_answer  # noqa: E402

from lantern import pipeline  # noqa: E402
from lantern.card import Card, build_card  # noqa: E402
from lantern.cases import ROOT  # noqa: E402

CLEAN = {"git_commit": "abc123", "dirty": False, "diff_hash": None}
DIRTY = {"git_commit": "abc123", "dirty": True, "diff_hash": "d1ff"}


def loader(cid, final=False):
    c = fixtures.case()
    return {**c, "id": cid, "meta": {**c["meta"], "case_id": cid}}


class FakeModel:
    """Answers from a script per case: 'ok' -> a valid answer, 'api' -> raises (API failure)."""

    def __init__(self, script=None):
        self.script, self.calls, self.lock = script or {}, [], threading.Lock()

    def call(self, request, feedback=None):
        with self.lock:
            n = len(self.calls)
            self.calls.append(request)
        step = self.script.get(n, "ok")
        if step == "api":
            raise RuntimeError("429 RESOURCE_EXHAUSTED")
        return {"text": json.dumps(valid_answer()), "model_version": "fake-1", "seconds": 0,
                "usage": {"input": 10, "output": 5, "thinking": 0}}


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, ids, model, run_id="r1", state=CLEAN, **kw):
        return pipeline.run(ids, run_id, provider=model, loader=loader, state_fn=lambda: dict(state),
                            log=lambda *a: None, root=self.tmp.name, min_seconds=0, **kw)

    def saved(self, cid, run_id="r1"):
        with open(os.path.join(self.tmp.name, run_id, f"{cid}.json")) as fh:
            return json.load(fh)

    def test_saves_a_valid_card_with_request_hash(self):
        self.assertEqual(self.go(["f1"], FakeModel()), {"f1": "verified"})
        rec = self.saved("f1")
        card = Card.model_validate(rec["card"])                     # matches the contract
        self.assertEqual(card.provenance.request_hash, rec["request_hash"])
        with open(os.path.join(self.tmp.name, "r1", "manifest.json")) as fh:
            m = json.load(fh)
        self.assertEqual(m["cases"]["f1"]["request_hash"], rec["request_hash"])
        self.assertEqual(m["git_commit"], "abc123")

    def test_api_failure_is_error_and_resume_retries_only_it(self):
        model = FakeModel({0: "api"})
        out = self.go(["f1", "f2"], model)
        self.assertEqual(sorted(out.values()), ["error", "verified"])
        failed = next(c for c, s in out.items() if s == "error")
        model2 = FakeModel()
        out2 = self.go(["f1", "f2"], model2)
        self.assertEqual(out2, {"f1": "verified", "f2": "verified"})
        self.assertEqual(len(model2.calls), 1)                      # the verified case was not rerun
        self.assertEqual(self.saved(failed)["status"], "verified")

    def test_resume_refuses_when_the_prompt_changed(self):
        self.go(["f1"], FakeModel())
        mpath = os.path.join(self.tmp.name, "r1", "manifest.json")
        with open(mpath) as fh:
            m = json.load(fh)
        m["prompt_hash"] = "older-prompt"
        with open(mpath, "w") as fh:
            json.dump(m, fh)
        with self.assertRaises(pipeline.RunRefused) as e:
            self.go(["f1", "f2"], FakeModel())
        self.assertIn("prompt_hash", str(e.exception))

    def test_resume_refuses_a_different_commit(self):
        self.go(["f1"], FakeModel())
        with self.assertRaises(pipeline.RunRefused):
            self.go(["f1"], FakeModel(), state={**CLEAN, "git_commit": "def456"})

    def test_dirty_tree_refused_unless_allowed(self):
        with self.assertRaises(pipeline.RunRefused):
            self.go(["f1"], FakeModel(), state=DIRTY)
        self.go(["f1"], FakeModel(), run_id="r2", state=DIRTY, allow_dirty=True)
        with open(os.path.join(self.tmp.name, "r2", "manifest.json")) as fh:
            m = json.load(fh)
        self.assertTrue(m["dirty"])
        self.assertEqual(m["diff_hash"], "d1ff")

    def test_final_writes_nothing_inside_the_repo(self):
        heldout = tempfile.TemporaryDirectory()
        try:
            with mock.patch.dict(os.environ, {"LANTERN_HELDOUT": heldout.name}):
                pipeline.run(["h001"], "final-r1", final=True, provider=FakeModel(), loader=loader,
                             state_fn=lambda: dict(CLEAN), log=lambda *a: None, root=self.tmp.name, min_seconds=0)
            self.assertTrue(os.path.exists(os.path.join(heldout.name, "runs", "final-r1", "h001.json")))
            self.assertFalse(os.path.exists(os.path.join(ROOT, "runs", "final-r1")))
            self.assertFalse(os.path.exists(os.path.join(self.tmp.name, "final-r1")))
        finally:
            heldout.cleanup()

    def test_two_workers_share_one_rate_limit(self):
        inner = FakeModel()
        paced = pipeline.PacedProvider(inner, 0.15)
        threads = [threading.Thread(target=paced.call, args=({},)) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        gaps = [b - a for a, b in zip(paced.starts, paced.starts[1:])]
        self.assertEqual(len(paced.starts), 4)
        self.assertTrue(all(g >= 0.14 for g in gaps), gaps)


class CardContract(unittest.TestCase):
    PROV = {"run_id": "r", "created_at": "2026-11-28T00:00:00", "pathway_version": "x"}

    def outcome(self, **kw):
        return {"status": "verified", "answer": valid_answer(), "urgency": PREP["floor"], "warnings": [],
                "attempts": [], **kw}

    def test_mismatch_is_caught_before_saving(self):
        with self.assertRaises(Exception):
            build_card(fixtures.case(), PREP, self.outcome(urgency="critical"), PATHWAY, self.PROV)

    def test_advise_er_is_set_by_code(self):
        c = build_card(fixtures.case(), PREP, self.outcome(urgency="emergent"), PATHWAY, self.PROV)
        self.assertTrue(c.urgency.advise_er)
        prep = copy.deepcopy(PREP)
        prep["floor"] = "emergent"
        c = build_card(fixtures.case(), prep, {"status": "error", "attempts": []}, PATHWAY, self.PROV)
        self.assertTrue(c.urgency.advise_er)                       # even with no model answer
        self.assertEqual(c.urgency.final, "emergent")

    def test_unverified_card_has_no_model_fields(self):
        c = build_card(fixtures.case(), PREP, {"status": "needs_manual_review", "attempts": []}, PATHWAY, self.PROV)
        self.assertIsNone(c.summary)
        self.assertEqual(c.urgency.final, PREP["floor"])
        self.assertTrue(all(t.include is None for t in c.tests))
        self.assertEqual([f.id for f in c.urgency.checklist_flags], [h["id"] for h in PREP["flags"]])
