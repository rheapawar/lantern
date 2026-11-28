# Clean-writer workflow (keeps the tests honest)

The session that tunes the rules must never write the sentences that test them. So a separate
Claude Code chat, in a folder outside the repo, writes the phrase bank and the fresh held-out notes.

1. `python3 tools/pick_new_heldout.py` - picks h001-h010 from unused charts -> `selection/heldout_v2.csv`
2. `python3 build_cases.py --shortlist selection/heldout_v2.csv --cases-dir cases/heldout` - chart summaries (needs `output/fhir/`)
3. `python3 tools/make_writer_packet.py` - builds `../lantern-writer/` (no matching rules, no notes)
4. Open `../lantern-writer/` in a NEW VS Code window, new Claude Code chat: "Follow WRITER_PROMPT.md"
5. Back in the repo: `python3 tools/import_writer_output.py`, then step 2 again so bundles carry the notes
6. `python3 -m unittest discover -s tests` - `test_flag_cases.py` now shows misses and false alarms. Tune here.
7. Checkpoints only: `python3 tools/score_hidden_bank.py "label"` and the held-out scorecard.

`cases/heldout/` is blocked for Claude Code by `.claude/settings.json`. A shell command could still
read it, so don't ask Claude Code to cat, grep or print anything in there.

When a test fails: describe the failure in general terms, fix the grammar first, add a new general
fire + quiet sentence for any new phrase. Never paste a note into the chat when asking for a rule fix.
