"""Scorecard: compare a run's saved cards with the hand-written labels. No API calls - re-score any run free.

    .venv/bin/python eval.py runs/<run_id>          # writes scorecards/<run_id>.md and .json
    .venv/bin/python eval.py runs/<run_id> --print  # also print it

The FIRST line is always emergent misses. This is the only code that reads label.json (the answer key).

How cases count:
  verified             scored on everything
  needs_manual_review  scored: urgency = the floor, and a miss on every content metric (no model answer)
  error / missing      NOT scored - the API failed; rerun with the same --run-id. Listed separately.
Recall-type metrics are pooled over all scored cases (sum of hits / sum of expected).
A held-out (--final) run is scored into $LANTERN_HELDOUT/scorecards/, never into the repo.
"""
import argparse
import glob
import json
import os
import sys

import yaml

from lantern.cases import CASES, ROOT, heldout_dir

TIERS = ("emergent", "urgent", "soon", "routine")
SCORED = ("verified", "needs_manual_review")


def _load(path):
    with open(path) as fh:
        return json.load(fh)


def load_run(run_dir):
    """(manifest, {case_id: record}) for every saved case file in the run."""
    manifest = _load(os.path.join(run_dir, "manifest.json"))
    recs = {}
    for p in sorted(glob.glob(os.path.join(run_dir, "*.json"))):
        if os.path.basename(p) != "manifest.json":
            r = _load(p)
            recs[r["case_id"]] = r
    return manifest, recs


def load_labels(case_ids, final):
    base = heldout_dir() if final else CASES
    out = {}
    for cid in case_ids:
        d = os.path.join(CASES, cid) if os.path.isdir(os.path.join(CASES, cid)) else os.path.join(base, cid)
        p = os.path.join(d, "label.json")
        if os.path.exists(p):
            out[cid] = _load(p)
    return out


# --- per-case facts the metrics need -----------------------------------------------------------------

def surfaced_facts(card):
    """Fact ids the card puts in front of the specialist: cited facts + test/option depends_on."""
    s = {f["fact"] for f in card.get("cited_facts", [])}
    for row in card.get("tests", []) + card.get("options", []):
        s |= set(row.get("depends_on") or [])
    return s


def citations_ok(card):
    """Independent re-check of the saved card: every cited ref is a chart item of that fact, or the note."""
    refs_by_fact = {f["id"]: {i["ref"] for i in f["items"]} for f in card.get("chart", [])}
    for c in card.get("cited_facts", []):
        if c["ref"] != card["note_ref"] and c["ref"] not in refs_by_fact.get(c["fact"], set()):
            return False
        if c["ref"] == card["note_ref"] and not (c.get("quote") and " ".join(c["quote"].lower().split())
                                                 in " ".join(card["note"].lower().split())):
            return False
    return True


def case_result(card, label, hooks_map):
    u = card["urgency"]
    want, got, floor = label["urgency"], u["final"], u["floor"]
    included = {t["id"] for t in card["tests"] if t.get("include")}
    relevant = {o["id"] for o in card["options"] if o.get("relevant")}
    surfaced = surfaced_facts(card)
    hooks = (label.get("answer_key_only") or {}).get("hooks") or []
    unmapped = [h for h in hooks if h not in hooks_map]
    if unmapped:
        raise KeyError(f"{card['case_id']}: hooks {unmapped} have no fact mapping in config/eval.yaml")
    fit_ok = card["fit"].get("suggested") is not None and (
        card["fit"]["suggested"] == label["fit"] or card["fit"]["suggested"] in (label.get("acceptable_fits") or []))
    return {
        "case_id": card["case_id"], "reason": card["reason_id"], "status": card["status"],
        "want": want, "got": got, "floor": floor, "set_by": u["set_by"],
        "under": TIERS.index(got) > TIERS.index(want), "over": TIERS.index(got) < TIERS.index(want),
        "citations_ok": citations_ok(card),
        "chart_dependent": bool(label.get("chart_dependent")),
        "hooks_caught": {h: bool(set(hooks_map[h]) & surfaced) for h in hooks},
        "tests_want": sorted(label.get("tests_first") or []), "tests_got": sorted(included),
        "facts_want": sorted(label.get("decision_facts") or []), "facts_got": sorted(surfaced),
        "options_want": sorted(label.get("acceptable_options") or []), "options_got": sorted(relevant),
        "fit_want": label["fit"], "fit_got": card["fit"].get("suggested"), "fit_ok": fit_ok,
        "request_hash": card["provenance"].get("request_hash"), "tokens": card["provenance"].get("tokens") or {},
        "warnings": card.get("warnings", []), "problems": card.get("problems", []),
    }


# --- scoring -----------------------------------------------------------------------------------------

def _recall(rows, want, got):
    hit = sum(len(set(r[want]) & set(r[got])) for r in rows)
    total = sum(len(r[want]) for r in rows)
    return hit, total


def _rate(n, d):
    return None if d == 0 else n / d


def score(manifest, recs, labels, cfg, runs_root=None):
    """The scorecard as a dict (rendered by render()). runs_root: folder holding this run and its siblings."""
    hooks_map = cfg["hooks"]
    rows, not_scored, unlabelled = [], [], []
    for cid, rec in sorted(recs.items()):
        if rec["status"] not in SCORED:
            not_scored.append({"case_id": cid, "status": rec["status"]})
        elif cid not in labels:
            unlabelled.append(cid)
        else:
            rows.append(case_result(rec["card"], labels[cid], hooks_map))
    missing = sorted(set(manifest.get("cases", {})) - set(recs))
    n = len(rows)

    emergent = [r for r in rows if r["want"] == "emergent"]
    urgent = [r for r in rows if r["want"] == "urgent"]
    dep = [r for r in rows if r["chart_dependent"]]
    raised = [r for r in rows if r["set_by"] == "model"]
    t_hit, t_tot = _recall(rows, "tests_want", "tests_got")
    t_prec_hit, t_prec_tot = _recall(rows, "tests_got", "tests_want")
    f_hit, f_tot = _recall(rows, "facts_want", "facts_got")
    o_hit, o_tot = _recall(rows, "options_want", "options_got")
    m = {
        "emergent_missed": [r["case_id"] for r in emergent if r["got"] != "emergent"],
        "emergent_cases": len(emergent),
        "urgent_under_called": [r["case_id"] for r in urgent if r["under"]],
        "urgent_cases": len(urgent),
        "any_under_called": [r["case_id"] for r in rows if r["under"]],
        "over_called": [r["case_id"] for r in rows if r["over"]],
        "over_called_rate": _rate(sum(r["over"] for r in rows), n),
        "citations_valid_rate": _rate(sum(r["citations_ok"] for r in rows if r["status"] == "verified"),
                                      sum(1 for r in rows if r["status"] == "verified")),
        "needs_manual_review": [r["case_id"] for r in rows if r["status"] == "needs_manual_review"],
        "chart_dependent_caught": [r["case_id"] for r in dep if r["hooks_caught"] and all(r["hooks_caught"].values())],
        "chart_dependent_cases": len(dep),
        "chart_dependent_caught_rate": _rate(sum(1 for r in dep if r["hooks_caught"] and all(r["hooks_caught"].values())),
                                             len(dep)),
        "tests_first_recall": _rate(t_hit, t_tot), "tests_first_precision": _rate(t_prec_hit, t_prec_tot),
        "decision_facts_recall": _rate(f_hit, f_tot),
        "options_recall": _rate(o_hit, o_tot),
        "fit_correct_rate": _rate(sum(r["fit_ok"] for r in rows), n),
        "raised_above_floor": [{"case_id": r["case_id"], "floor": r["floor"], "final": r["got"], "label": r["want"],
                                "verdict": "right" if r["got"] == r["want"] else ("over" if r["over"] else "still under")}
                               for r in raised],
    }
    m["emergent_missed_n"] = len(m["emergent_missed"])
    m["urgent_under_called_n"] = len(m["urgent_under_called"])

    by_reason = {}
    for r in rows:
        b = by_reason.setdefault(r["reason"], [])
        b.append(r)
    reasons = {}
    for rid, rs in sorted(by_reason.items()):
        th, tt = _recall(rs, "tests_want", "tests_got")
        oh, ot = _recall(rs, "options_want", "options_got")
        fh, ft = _recall(rs, "facts_want", "facts_got")
        reasons[rid] = {"cases": len(rs), "urgency_exact": sum(r["got"] == r["want"] for r in rs),
                        "under": sum(r["under"] for r in rs), "over": sum(r["over"] for r in rs),
                        "tests_recall": _rate(th, tt), "facts_recall": _rate(fh, ft),
                        "options_recall": _rate(oh, ot), "fit_correct": sum(r["fit_ok"] for r in rs)}

    tokens = {}
    for r in rows:
        for k, v in r["tokens"].items():
            tokens[k] = tokens.get(k, 0) + (v or 0)
    label_status = {}
    for cid in [r["case_id"] for r in rows]:
        lab = labels[cid]
        key = "unreviewed draft" if (lab.get("status") == "draft" or "draft" in str(lab.get("labeler", ""))) \
            else "reviewed"
        label_status[key] = label_status.get(key, 0) + 1

    targets = {}
    for k, t in cfg["targets"].items():
        v = m.get(k + "_n", m.get(k)) if k in ("emergent_missed", "urgent_under_called") else m.get(k)
        if v is None:
            targets[k] = None
        else:
            targets[k] = (v <= t["max"]) if "max" in t else (v >= t["min"])

    return {"run_id": manifest["run_id"], "final": manifest.get("final", False), "manifest": {
                k: manifest.get(k) for k in ("git_commit", "dirty", "diff_hash", "model", "prompt_hash",
                                             "pathway_version", "pathway_hash", "contract_version", "created_at",
                                             "finished_at")},
            "scored": n, "not_scored": not_scored, "missing": missing, "unlabelled": unlabelled,
            "metrics": m, "targets": targets, "by_reason": reasons, "cases": rows, "tokens": tokens,
            "label_status": label_status, "determinism": determinism(manifest, recs, runs_root)}


def determinism(manifest, recs, runs_root=None):
    """Other runs with the same code (commit + diff + prompt + pathway): any case whose request differs?"""
    runs_root = runs_root or os.path.join(ROOT, "runs")
    keys = ("git_commit", "diff_hash", "prompt_hash", "pathway_hash", "config_hash", "fhir_map_hash")
    out = []
    for mp in glob.glob(os.path.join(runs_root, "*", "manifest.json")):
        other = _load(mp)
        if other.get("run_id") == manifest["run_id"] or any(other.get(k) != manifest.get(k) for k in keys):
            continue
        for cid, info in other.get("cases", {}).items():
            mine = recs.get(cid)
            if mine and info.get("request_hash") and mine["request_hash"] != info["request_hash"]:
                out.append({"case_id": cid, "other_run": other["run_id"]})
    return out


# --- rendering ---------------------------------------------------------------------------------------

def _pct(v):
    return "n/a" if v is None else f"{v:.0%}"


def _mark(ok):
    return "n/a" if ok is None else ("PASS" if ok else "FAIL")


def render(s):
    m, t = s["metrics"], s["targets"]
    L = [f"**Emergent cases missed: {m['emergent_missed_n']} of {m['emergent_cases']}** "
         f"(target 0) {_mark(t['emergent_missed'])}" + (f" - {', '.join(m['emergent_missed'])}" if m["emergent_missed"] else ""),
         "", f"# Scorecard - {s['run_id']}", ""]
    mf = s["manifest"]
    L += [f"Model `{mf['model']}` | commit `{(mf['git_commit'] or '')[:7]}`" + (" (DIRTY tree)" if mf["dirty"] else "")
          + f" | prompt `{mf['prompt_hash']}` | pathway {mf['pathway_version']} `{mf['pathway_hash']}` "
          f"| card contract {mf['contract_version']} | {mf['created_at']} -> {mf.get('finished_at') or 'unfinished'}", ""]
    ls = s["label_status"]
    if ls.get("unreviewed draft"):
        L += [f"> **Labels:** {ls['unreviewed draft']} of {s['scored']} scored labels are unreviewed drafts "
              "written by Claude. Their `tests_first` and `decision_facts` were generated from the pathway file, so "
              "those two lines partly grade the pathway against itself. Treat this scorecard as a draft until a "
              "clinician has reviewed the labels.", ""]
    L += [f"Scored: **{s['scored']}** cases" + (f" | **not scored (API errors - rerun):** "
          f"{', '.join(x['case_id'] for x in s['not_scored'])}" if s["not_scored"] else "")
          + (f" | missing: {', '.join(s['missing'])}" if s["missing"] else "")
          + (f" | no label: {', '.join(s['unlabelled'])}" if s["unlabelled"] else ""), ""]

    L += ["| Metric | Result | Target | |", "|---|---|---|---|",
          f"| Emergent cases missed | {m['emergent_missed_n']} of {m['emergent_cases']} | 0 | {_mark(t['emergent_missed'])} |",
          f"| Urgency under-called (urgent cases) | {m['urgent_under_called_n']} of {m['urgent_cases']} | 0 | "
          f"{_mark(t['urgent_under_called'])} |",
          f"| Urgency over-called | {len(m['over_called'])} of {s['scored']} ({_pct(m['over_called_rate'])}) | <20% | "
          f"{_mark(t['over_called_rate'])} |",
          f"| Citations valid (verified cards, re-checked) | {_pct(m['citations_valid_rate'])} | 100% | "
          f"{_mark(t['citations_valid_rate'])} |",
          f"| Chart-dependent cases caught | {len(m['chart_dependent_caught'])} of {m['chart_dependent_cases']} | 80% | "
          f"{_mark(t['chart_dependent_caught_rate'])} |",
          f"| Tests-first recall (precision) | {_pct(m['tests_first_recall'])} ({_pct(m['tests_first_precision'])}) | 70% | "
          f"{_mark(t['tests_first_recall'])} |",
          f"| Decision facts surfaced | {_pct(m['decision_facts_recall'])} | 80% | {_mark(t['decision_facts_recall'])} |",
          f"| Options recall | {_pct(m['options_recall'])} | 80% | {_mark(t['options_recall'])} |",
          f"| Fit correct | {_pct(m['fit_correct_rate'])} | 70% | {_mark(t['fit_correct_rate'])} |",
          f"| Needs manual review | {len(m['needs_manual_review'])} | - | |", ""]
    if m["any_under_called"]:
        L += [f"Under-called (any tier): {', '.join(m['any_under_called'])}", ""]
    if m["over_called"]:
        L += [f"Over-called: {', '.join(m['over_called'])}", ""]

    L += ["## What the model added above the red-flag floor", ""]
    if m["raised_above_floor"]:
        L += ["| Case | Floor | Final | Label | Verdict |", "|---|---|---|---|---|"]
        L += [f"| {x['case_id']} | {x['floor']} | {x['final']} | {x['label']} | {x['verdict']} |" for x in m["raised_above_floor"]]
    else:
        L += ["The model never raised urgency above the floor in this run."]
    L += [""]

    L += ["## By referral reason", "", "| Reason | Cases | Urgency exact | Under | Over | Tests | Facts | Options | Fit |",
          "|---|---|---|---|---|---|---|---|---|"]
    for rid, b in s["by_reason"].items():
        L.append(f"| {rid} | {b['cases']} | {b['urgency_exact']} | {b['under']} | {b['over']} | {_pct(b['tests_recall'])} "
                 f"| {_pct(b['facts_recall'])} | {_pct(b['options_recall'])} | {b['fit_correct']}/{b['cases']} |")
    L += ["", "## Per case (misses only)", "",
          "| Case | Status | Urgency (floor) / label | Tests missed | Facts missed | Options missed | Fit | Hooks |",
          "|---|---|---|---|---|---|---|---|"]
    for r in s["cases"]:
        tm = sorted(set(r["tests_want"]) - set(r["tests_got"]))
        fm = sorted(set(r["facts_want"]) - set(r["facts_got"]))
        om = sorted(set(r["options_want"]) - set(r["options_got"]))
        hk = ", ".join(f"{h}{'' if ok else ' MISSED'}" for h, ok in r["hooks_caught"].items())
        u = f"{r['got']} ({r['floor']}) / {r['want']}" + (" UNDER" if r["under"] else " over" if r["over"] else "")
        fit = "ok" if r["fit_ok"] else f"{r['fit_got']} vs {r['fit_want']}"
        if tm or fm or om or not r["fit_ok"] or r["under"] or r["over"] or "MISSED" in hk or r["status"] != "verified":
            L.append(f"| {r['case_id']} | {r['status']} | {u} | {', '.join(tm)} | {', '.join(fm)} | {', '.join(om)} "
                     f"| {fit} | {hk} |")
    L += [""]
    if s["determinism"]:
        L += ["## Determinism warning", "", "Same code as another run, but these requests differ (something in "
              "request building is not deterministic - fix before comparing scorecards):", ""]
        L += [f"- {d['case_id']} vs run {d['other_run']}" for d in s["determinism"]] + [""]
    tk = s["tokens"]
    L += [f"Tokens (scored cases): input {tk.get('input', 0):,}, output {tk.get('output', 0):,}, "
          f"thinking {tk.get('thinking', 0):,}."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()
    with open(os.path.join(ROOT, "config", "eval.yaml")) as fh:
        cfg = yaml.safe_load(fh)
    manifest, recs = load_run(a.run_dir)
    final = manifest.get("final", False)
    labels = load_labels(list(recs), final)
    s = score(manifest, recs, labels, cfg, os.path.dirname(os.path.abspath(a.run_dir)))
    out_dir = os.path.join(heldout_dir(), "scorecards") if final else os.path.join(ROOT, "scorecards")
    os.makedirs(out_dir, exist_ok=True)
    md = render(s)
    base = os.path.join(out_dir, manifest["run_id"])
    with open(base + ".md", "w") as fh:
        fh.write(md)
    with open(base + ".json", "w") as fh:
        json.dump(s, fh, indent=1, default=str)
    print(md.splitlines()[0])
    print(f"-> {base}.md")
    if a.print:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
