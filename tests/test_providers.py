"""Provider adapters with fake clients (no network): OpenAI request shape, strict schema, quota fail-fast."""
import json
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_verifier import PREP, valid_answer  # noqa: E402

import openai  # noqa: E402
import httpx2 as httpx  # noqa: E402  (openai 3.x is built on httpx2)

from lantern.llm import OpenAIProvider, QuotaExhausted, strict_schema  # noqa: E402

CFG = {"model": "test-model", "max_output_tokens": 1000, "max_retries": 2, "reasoning_effort": "medium"}


def _resp():
    usage = SimpleNamespace(input_tokens=100, output_tokens=40,
                            output_tokens_details=SimpleNamespace(reasoning_tokens=15))
    return SimpleNamespace(output_text=json.dumps(valid_answer()), model="test-model-2026", usage=usage,
                           status="completed", incomplete_details=None)


def _rate_limit(code):
    r = httpx.Response(429, request=httpx.Request("POST", "https://x"))
    return openai.RateLimitError(f"Error code: 429 - {{'error': {{'code': '{code}'}}}}", response=r, body=None)


class FakeResponses:
    def __init__(self, *outcomes):
        self.outcomes, self.kwargs = list(outcomes), []

    def create(self, **kw):
        self.kwargs.append(kw)
        o = self.outcomes.pop(0)
        if isinstance(o, Exception):
            raise o
        return o


def provider(*outcomes):
    fr = FakeResponses(*outcomes)
    return OpenAIProvider(CFG, client=SimpleNamespace(responses=fr)), fr


class OpenAI(unittest.TestCase):
    def test_request_shape(self):
        p, fr = provider(_resp())
        out = p.call(PREP["request"], feedback="Your previous answer: ...")
        kw = fr.kwargs[0]
        self.assertEqual(kw["instructions"], PREP["request"]["system"])
        self.assertEqual([m["content"] for m in kw["input"]], [PREP["request"]["user"], "Your previous answer: ..."])
        self.assertFalse(kw["store"])
        self.assertEqual(kw["text"]["format"]["type"], "json_schema")
        self.assertTrue(kw["text"]["format"]["strict"])
        self.assertEqual(kw["reasoning"], {"effort": "medium"})
        self.assertEqual(out["usage"], {"input": 100, "output": 25, "thinking": 15})
        self.assertEqual(out["model_version"], "test-model-2026")

    def test_strict_schema_closes_every_object(self):
        s = strict_schema(PREP["request"]["schema"])
        def objects(x):
            if isinstance(x, dict):
                if x.get("type") == "object":
                    yield x
                for v in x.values():
                    yield from objects(v)
            elif isinstance(x, list):
                for v in x:
                    yield from objects(v)
        objs = list(objects(s))
        self.assertGreaterEqual(len(objs), 4)
        for o in objs:
            self.assertIs(o["additionalProperties"], False)
            self.assertEqual(set(o["required"]), set(o["properties"]))
        self.assertNotIn("additionalProperties", PREP["request"]["schema"])     # the saved request is unchanged

    def test_rate_limit_is_retried(self):
        import lantern.llm as llm
        orig, llm.time.sleep = llm.time.sleep, lambda s: None
        try:
            p, fr = provider(_rate_limit("rate_limit_exceeded"), _resp())
            self.assertIn("text", p.call(PREP["request"]))
            self.assertEqual(len(fr.kwargs), 2)
        finally:
            llm.time.sleep = orig

    def test_out_of_credit_fails_fast(self):
        p, fr = provider(_rate_limit("insufficient_quota"), _resp())
        with self.assertRaises(QuotaExhausted):
            p.call(PREP["request"])
        self.assertEqual(len(fr.kwargs), 1)                                    # no retries
