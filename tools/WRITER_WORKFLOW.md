# Clean-writer workflow (keeps the tests honest)

The session that tunes the rules must never write, or see, the sentences that test them.

Folders, side by side:
    ~/projects/lantern/          the repo - the tuning chat works here
    ~/projects/lantern-writer/   the clean writer's folder (no rules, no notes)
    ~/projects/lantern-heldout/  held-out notes + the hidden 20% of the phrase bank. NOT in the repo.

Held-out material stays outside the repo because a deny rule only blocks Claude Code's file tools;
a `grep -r` or `cat` run through the shell would still read it. Outside the repo, routine searches
never touch it. Back it up somewhere private (a separate private repo, or cloud storage) - not here.

1. `python3 tools/pick_new_heldout.py` - picks h001-h010 from unused charts -> `../lantern-heldout/heldout_v2.csv`
2. `python3 build_cases.py --shortlist ../lantern-heldout/heldout_v2.csv --cases-dir ../lantern-heldout` (needs `output/fhir/`)
3. `python3 tools/make_writer_packet.py` - builds `../lantern-writer/`
4. Open `../lantern-writer/` in a NEW VS Code window, new Claude Code chat: "Follow WRITER_PROMPT.md"
5. `python3 tools/import_writer_output.py`, then step 2 again so the bundles carry the notes
6. `python3 -m unittest discover -s tests` - `test_flag_cases.py` shows misses and false alarms. Tune here.
7. Checkpoints only: `python3 tools/score_hidden_bank.py "label"` and the held-out scorecard.
   These print numbers only. Never ask Claude Code to open, print or explain anything in ../lantern-heldout.

When a test fails: describe the failure in general terms, fix the grammar first, add a new general
fire + quiet sentence for any new phrase. Never paste a note into the chat when asking for a rule fix.
