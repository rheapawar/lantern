#!/usr/bin/env python3
"""Build a folder for a CLEAN writer: a Claude Code session that has never seen Lantern's matching rules.

    python3 tools/make_writer_packet.py                 # writes ../lantern-writer/
    python3 tools/make_writer_packet.py --out /some/dir

The clean writer produces (1) the phrase bank that tests the red-flag rules and (2) referral notes for
the fresh held-out cases. It must not be able to read pathways/, lantern/, tests/ or any existing note,
so this script copies ONLY what it needs into a folder OUTSIDE the repo. Open that folder in a new
VS Code window and start a new Claude Code chat there.

Packet contents:
  WRITER_PROMPT.md   what to do (paste "Follow WRITER_PROMPT.md" into the new chat)
  NOTE_GUIDE.md      how to write a note (labeller section removed)
  flags.md           every flag: id, tier, plain-English meaning. NO match rules.
  research/          guideline notes (how clinicians describe these symptoms; no phrase lists)
  charts/hNNN.md     chart summaries for the fresh held-out cases (from cases/heldout/)
  out/               where the writer saves its work (read back by tools/import_writer_output.py)
"""
import argparse
import glob
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIER_KEYS = [("red_flags", "emergent"), ("urgent_flags", "urgent"), ("soon_flags", "soon")]


def flags_md(pathway):
    L = ["# Flags", "",
         "Each flag is a reason a referral should be seen sooner than normal. The id is what you use in",
         "phrase_bank.yaml. The text says what the flag MEANS - it is not the wording to copy.", "",
         "## Tiers", ""]
    for t in pathway["tier_order"]:
        L.append(f"- **{t}**: {pathway['tiers'][t]}")
    for rid, r in pathway["reasons"].items():
        L += ["", f"## {r['label']}  (`{rid}`)", "", "| id | tier | meaning |", "|---|---|---|"]
        for key, tier in TIER_KEYS:
            for f in r.get(key, []):
                L.append(f"| `{f['id']}` | {tier} | {f['text']} |")
    return "\n".join(L) + "\n"


def strip_guide(text):
    """Drop the labeller section (it points at pathway ids and label.json)."""
    return re.split(r"\n## For the labeller", text)[0].rstrip() + "\n"


def strip_chart(text):
    """Drop any writing plan - the clean writer makes its own plan."""
    return re.sub(r"## Writing plan.*?(?=\n## )", "", text, flags=re.S)


PROMPT = """# Task for the clean writer

You are writing test material for Lantern, a tool that reads a primary care doctor's referral note
to cardiology and decides how urgent it is. You have NOT seen Lantern's code or matching rules, and
you must keep it that way: work only from the files in this folder. Two jobs.

## Job 1 - phrase bank -> `out/phrase_bank.yaml`

For EVERY flag id in `flags.md`, write short note-style sentences:

- `fire`: 4 sentences where the flag clearly applies.
- `quiet`: 4 near-misses where a careful cardiologist would say the flag does NOT apply.

Format (YAML, flag id -> lists of strings):

```yaml
hf_breathless_rest:
  fire:
    - "can't lie flat, sleeping on 3 pillows"
    - ...
  quiet:
    - "mildly SOB on hills, sleeps flat without trouble"
    - ...
```

Rules for good sentences:
- Write the way real PCPs write: mix full sentences, fragments, abbreviations (SOB, CP, hx, s/p,
  d/t, x2 wks), typos-free but casual. Don't reuse the meaning text from flags.md word for word.
- Vary the wording a lot across the 4. If two sentences differ by one word, replace one.
- `quiet` sentences must be HARD: same topic, different meaning. Use each of these at least once
  across the whole bank: negation ("denies", "no", "ruled out"), past or resolved ("last year,
  resolved", "hx of"), stable or chronic ("unchanged for years"), just below a threshold
  (a number under the cut-off), a different body part or cause ("knee swelling from arthritis"),
  two facts that are both present but unrelated, an earlier reading that was later normal.
- `fire` sentences should include some hard ones too: the key fact buried mid-sentence, unusual
  synonyms, numbers written differently ("HR in the 30s", "3 kg in a week", "BP 190 over 110").
- Every sentence must stand alone (Lantern reads it as a whole note).
- Do not invent thresholds. If a flag needs a number, use what flags.md or research/ says.

## Job 2 - referral notes for `charts/hNNN.md` -> `out/notes/hNNN.txt` and `out/plan.csv`

1. Read NOTE_GUIDE.md (styles, rules, what each tier looks like).
2. For each chart, decide the plan yourself and record it in `out/plan.csv` with the header:
   `case_id,planned_tier,question_type,style,include_negation,do_not_mention,note_must_convey`
   - Across the 10: about 2 emergent (written as the PCP under-calling it), 3 urgent, 1 soon if a
     heart-failure chart fits, the rest routine. Use each style at least twice.
   - question_type is one of: test_interpretation, specific_workup_or_management, guideline_exception,
     noncardiac_drug_in_cardiac_patient, family_history, concerns_despite_normal_tests,
     new_symptom_assessment.
   - do_not_mention: if the chart's "Hook(s) this case tests" line names a hook, that fact must not
     appear in the note (kidney_disease -> kidney/CKD/eGFR; prior_mi_or_cad -> heart attack, coronary
     disease, stents, bypass; abnormal_tsh -> thyroid/TSH; on_amlodipine -> amlodipine or any
     swelling-causing medicine; regular_nsaid -> ibuprofen/naproxen/NSAIDs).
   - The note must agree with the chart: don't state a BP, lab or medicine the chart contradicts.
     If the tier needs a number the chart doesn't have (e.g. today's BP), say it was measured today.
3. Write each note as plain text in `out/notes/hNNN.txt`. End with the referral question. No names,
   nothing after the referral date, never write the tier word.

When done, list anything you weren't sure about in `out/questions.md`.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(ROOT), "lantern-writer"))
    ap.add_argument("--cases-dir", default=os.environ.get("LANTERN_HELDOUT", os.path.join(os.path.dirname(ROOT), "lantern-heldout")))
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    if out.startswith(ROOT + os.sep) or out == ROOT:
        raise SystemExit("put the packet OUTSIDE the repo, or the writer can wander into pathways/")

    with open(os.path.join(ROOT, "pathways", "cardiology.json")) as fh:
        pathway = json.load(fh)
    os.makedirs(os.path.join(out, "out", "notes"), exist_ok=True)
    os.makedirs(os.path.join(out, "charts"), exist_ok=True)
    with open(os.path.join(out, "WRITER_PROMPT.md"), "w") as fh:
        fh.write(PROMPT)
    with open(os.path.join(out, "flags.md"), "w") as fh:
        fh.write(flags_md(pathway))
    with open(os.path.join(ROOT, "cases", "NOTE_GUIDE.md")) as fh:
        guide = strip_guide(fh.read())
    with open(os.path.join(out, "NOTE_GUIDE.md"), "w") as fh:
        fh.write(guide)
    shutil.copytree(os.path.join(ROOT, "research"), os.path.join(out, "research"), dirs_exist_ok=True)

    charts = sorted(glob.glob(os.path.join(a.cases_dir, "h*", "chart_summary.md")))
    for p in charts:
        cid = os.path.basename(os.path.dirname(p))
        with open(p) as fh, open(os.path.join(out, "charts", f"{cid}.md"), "w") as g:
            g.write(strip_chart(fh.read()))

    leaked = [ph for ph in ("text_any", "text_regex", "\"match\"") if ph in open(os.path.join(out, "flags.md")).read()]
    assert not leaked, f"match rules leaked into flags.md: {leaked}"
    print(f"packet: {out}")
    print(f"  flags: {sum(len(r.get(k, [])) for r in pathway['reasons'].values() for k, _ in TIER_KEYS)}, "
          f"charts: {len(charts)}" + ("" if charts else "  <- none yet: run pick_new_heldout.py + build_cases.py --cases-dir ../lantern-heldout first"))
    print("next: open that folder in a NEW VS Code window, new Claude Code chat, say: Follow WRITER_PROMPT.md")


if __name__ == "__main__":
    main()
