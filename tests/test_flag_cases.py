"""Phrase bank: every 'fire' sentence must trigger its flag, every 'quiet' sentence must not.

tests/flag_cases.yaml comes from a clean writer that never saw the matching rules
(tools/make_writer_packet.py -> tools/import_writer_output.py). This is the set to tune against.

Rules for changing the matcher or pathway:
  - fix the GRAMMAR (clauses, negation, numbers) before adding phrases;
  - a new phrase needs a new fire AND quiet sentence here, written in general terms, never copied from a note.
"""
import json
import os
import unittest

import yaml

from lantern.matcher import urgency_floor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(ROOT, "tests", "flag_cases.yaml")
PATHWAY = json.load(open(os.path.join(ROOT, "pathways", "cardiology.json")))


def fired(text):
    return {h["id"] for h in urgency_floor(PATHWAY, text, None)[1]}


@unittest.skipUnless(os.path.exists(BANK), "no tests/flag_cases.yaml yet - run the clean-writer packet")
class PhraseBank(unittest.TestCase):
    def test_bank(self):
        with open(BANK) as fh:
            bank = yaml.safe_load(fh) or {}
        misses, false_alarms, n = [], [], 0
        for fid, d in sorted(bank.items()):
            for s in d.get("fire", []):
                n += 1
                if fid not in fired(s):
                    misses.append(f"{fid}: {s}")
            for s in d.get("quiet", []):
                n += 1
                if fid in fired(s):
                    false_alarms.append(f"{fid}: {s}")
        print(f"\n  phrase bank: {n} sentences, {len(misses)} misses, {len(false_alarms)} false alarms", end=" ")
        msg = "\nMISSED (should fire):\n  " + "\n  ".join(misses) + \
              "\nFALSE ALARM (should stay quiet):\n  " + "\n  ".join(false_alarms)
        self.assertEqual([], misses + false_alarms, msg)


if __name__ == "__main__":
    unittest.main()
