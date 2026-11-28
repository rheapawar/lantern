"""Run the engine over cases: retriever -> red-flag floor -> one LLM call -> verifier (+1 retry) -> card.

    .venv/bin/python -m lantern.pipeline                         # all training cases, new run id
    .venv/bin/python -m lantern.pipeline --cases c001 c004       # some cases
    .venv/bin/python -m lantern.pipeline --run-id <id>           # resume: reruns 'error' cases and unfinished ones
    .venv/bin/python -m lantern.pipeline --final                 # held-out cases; written OUTSIDE the repo

Each case is saved as runs/<run_id>/<case>.json: the Card (lantern/card.py, validated before saving), the
full outcome (every attempt, raw answer, check result) and the request. runs/<run_id>/manifest.json pins the
code: git commit, uncommitted-diff hash, prompt/pathway/config hashes, model. A resume that would mix code
versions is refused. Status 'error' (the API failed) is kept apart from 'needs_manual_review' (the model
failed the checks twice) and is retried on resume.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from lantern.card import CONTRACT_VERSION, build_card
from lantern.cases import ROOT, final_ids, heldout_dir, load_case, training_ids
from lantern.chart import load_map
from lantern.llm import load_config, make_provider, new_run_id, parse, prepare, request_hash
from lantern.verifier import ERROR, call_and_verify

DONE = ("verified", "needs_manual_review")      # resume skips these; 'error' and missing cases run again
PINNED = ("git_commit", "diff_hash", "prompt_hash", "pathway_version", "pathway_hash", "config_hash",
          "fhir_map_hash", "model", "contract_version")


class RunRefused(RuntimeError):
    pass


# --- what code produced a run ------------------------------------------------------------------------

def _sha(text):
    return hashlib.sha256(text.encode() if isinstance(text, str) else text).hexdigest()[:12]


def _file_hash(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return _sha(fh.read())


def git_state():
    """{'git_commit', 'dirty', 'diff_hash'}: uncommitted edits to tracked files make the tree dirty."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout
    diff = git("diff", "HEAD")
    return {"git_commit": git("rev-parse", "HEAD").strip(), "dirty": bool(diff.strip()),
            "diff_hash": _sha(diff) if diff.strip() else None}


def code_state(cfg, pathway, state_fn=git_state):
    return {**state_fn(), "prompt_hash": _file_hash(cfg["prompt"]), "pathway_version": pathway["version"],
            "pathway_hash": _file_hash(os.path.join("pathways", f"{pathway['specialty']}.json")),
            "config_hash": _sha(json.dumps(cfg, sort_keys=True)), "fhir_map_hash": _file_hash("config/fhir_map.yaml"),
            "model": cfg["model"], "contract_version": CONTRACT_VERSION}


# --- shared rate pacing --------------------------------------------------------------------------------

class PacedProvider:
    """One timer shared by every worker: calls start at least `min_seconds` apart in total, so two workers
    can't double the rate. (Retries inside the provider after a 429 use their own backoff.)"""

    def __init__(self, inner, min_seconds):
        self.inner, self.min_seconds = inner, min_seconds or 0
        self._lock, self._next = threading.Lock(), 0.0
        self.starts = []

    def call(self, request, feedback=None):
        with self._lock:
            wait = self._next - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            now = time.monotonic()
            self._next = now + self.min_seconds
            self.starts.append(now)
        return self.inner.call(request, feedback=feedback)


# --- runs -------------------------------------------------------------------------------------------

def run_root(final):
    """Held-out runs never land inside the repo."""
    return os.path.join(heldout_dir(), "runs") if final else os.path.join(ROOT, "runs")


def _write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False, default=str)
    os.replace(tmp, path)


def _read_json(path):
    with open(path) as fh:
        return json.load(fh)


def open_run(run_dir, state, allow_dirty, final, cfg):
    """Create the manifest, or check a resume against it. Returns the manifest."""
    if state["dirty"] and not allow_dirty:
        raise RunRefused("uncommitted changes to tracked files - commit them, or pass --allow-dirty "
                         "(the manifest records the diff hash either way)")
    mpath = os.path.join(run_dir, "manifest.json")
    if os.path.exists(mpath):
        m = _read_json(mpath)
        diff = [k for k in PINNED if m.get(k) != state.get(k)]
        if diff:
            raise RunRefused(f"this run was made with different code ({', '.join(diff)} changed); "
                             "resuming would mix versions - start a new --run-id")
        return m
    os.makedirs(run_dir, exist_ok=True)
    m = {**state, "run_id": os.path.basename(run_dir), "final": final, "config": cfg,
         "created_at": dt.datetime.now().isoformat(timespec="seconds"), "cases": {}}
    _write_json(mpath, m)
    return m


def run_case(case, pathway, fmap, cfg, provider, run_id, state):
    prep = prepare(pathway, fmap, case, cfg)
    rh = request_hash(prep["request"])
    t0 = time.time()
    outcome = call_and_verify(provider, prep, pathway, case["meta"]["reason"], parse)
    tokens = {}
    for a in outcome["attempts"]:
        for k, v in (a.get("usage") or {}).items():
            tokens[k] = tokens.get(k, 0) + (v or 0)
    versions = [a.get("model_version") for a in outcome["attempts"] if a.get("model_version")]
    card = build_card(case, prep, outcome, pathway, {
        "run_id": run_id, "created_at": dt.datetime.now(), "pathway_version": state["pathway_version"],
        "model": cfg["model"], "model_version": versions[-1] if versions else None, "request_hash": rh,
        "tokens": tokens or None})
    return {"case_id": case["id"], "status": card.status, "request_hash": rh, "seconds": round(time.time() - t0, 1),
            "card": card.model_dump(mode="json"),
            "outcome": {k: outcome[k] for k in ("status", "urgency", "warnings", "attempts")},
            "request": prep["request"]}


def run(case_ids, run_id=None, workers=1, final=False, allow_dirty=False, provider=None, loader=load_case,
        state_fn=git_state, log=print, root=None, min_seconds=None):
    """Run (or resume) cases. Returns {case_id: status}.
    provider / loader / state_fn / root / min_seconds are overridable for tests (root is ignored with --final:
    held-out runs always go to $LANTERN_HELDOUT/runs)."""
    cfg = load_config()
    pathway = _read_json(os.path.join(ROOT, "pathways", "cardiology.json"))
    fmap = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
    state = code_state(cfg, pathway, state_fn)
    run_id = run_id or new_run_id(cfg)
    run_dir = os.path.join(run_root(final) if final or root is None else root, run_id)
    manifest = open_run(run_dir, state, allow_dirty, final, cfg)
    if manifest.get("final") != final:
        raise RunRefused("can't resume a training run as --final or the other way round")

    todo = []
    for cid in case_ids:
        p = os.path.join(run_dir, f"{cid}.json")
        if os.path.exists(p) and _read_json(p).get("status") in DONE:
            continue
        todo.append(cid)
    log(f"run {run_id}: {len(case_ids) - len(todo)} done, {len(todo)} to run -> {run_dir}")
    paced = PacedProvider(provider or make_provider(cfg),
                          cfg.get("min_seconds_between_calls", 0) if min_seconds is None else min_seconds)
    lock = threading.Lock()

    quota_hit = threading.Event()

    def one(cid):
        if quota_hit.is_set():                 # out of quota: leave the rest unattempted for a later resume
            return cid, None
        rec = run_case(loader(cid, final=final), pathway, fmap, cfg, paced, run_id, state)
        last_err = (rec["outcome"]["attempts"] or [{}])[-1].get("error") or ""
        if last_err.startswith("QuotaExhausted"):
            quota_hit.set()
            log(f"  {cid}: quota exhausted - stopping the run ({last_err[:160]})")
        _write_json(os.path.join(run_dir, f"{cid}.json"), rec)
        with lock:
            manifest["cases"][cid] = {"status": rec["status"], "request_hash": rec["request_hash"]}
            _write_json(os.path.join(run_dir, "manifest.json"), manifest)
        c = rec["card"]
        log(f"  {cid}: {rec['status']:19} urgency {c['urgency']['final']:8} (floor {c['urgency']['floor']}) "
            f"{rec['seconds']}s")
        return cid, rec["status"]

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        results = dict(ex.map(one, todo))
    manifest["finished_at"] = dt.datetime.now().isoformat(timespec="seconds")
    _write_json(os.path.join(run_dir, "manifest.json"), manifest)
    statuses = {cid: manifest["cases"].get(cid, {}).get("status") for cid in case_ids}
    n_err = sum(1 for s in statuses.values() if s == ERROR)
    n_skip = sum(1 for s in statuses.values() if s is None)
    log(f"done: {sum(1 for s in statuses.values() if s == 'verified')} verified, "
        f"{sum(1 for s in statuses.values() if s == 'needs_manual_review')} need review, {n_err} API errors"
        + (f", {n_skip} not attempted (quota)" if n_skip else "")
        + (f" - rerun with --run-id {run_id} to retry them" if n_err or n_skip else ""))
    return statuses


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", nargs="*", help="case ids (default: all training cases, or all held-out with --final)")
    ap.add_argument("--run-id", help="resume this run (must match the current code)")
    ap.add_argument("--workers", type=int, default=1, help="parallel cases (calls stay paced by min_seconds_between_calls)")
    ap.add_argument("--final", action="store_true", help="held-out run; written to $LANTERN_HELDOUT/runs/")
    ap.add_argument("--allow-dirty", action="store_true", help="run with uncommitted changes (not for scoring)")
    a = ap.parse_args()
    ids = a.cases or (final_ids() if a.final else training_ids())
    try:
        run(ids, a.run_id, a.workers, a.final, a.allow_dirty)
    except RunRefused as e:
        raise SystemExit(f"refused: {e}")


if __name__ == "__main__":
    main()
