"""The card: what the pipeline saves per case and what the screens and database read. (Contract v0.2)

This file is the agreement between the engine and everything downstream (API, DB, React).
It holds NO decision logic: build_card() only copies and merges what the plain-code steps and the
verified model answer already produced. Change it deliberately, and update the screens in the same commit.

Who fills what (so the screens can show provenance):
  code      - retriever (chart facts, test status), red-flag checklist (floor, flags), card hints, routing
  model     - only after the verifier passed: urgency suggestion + reason, summary, cited facts,
              include/relevant + why for tests and options, fit, missing_info
  specialist- SpecialistInput, filled on the card screen; never by the engine

When status is not 'verified', every model field is None/empty and the card still works from the
code parts alone: urgency = the floor, tests pre-checked from the pathway, options unticked.
"""
from __future__ import annotations

from datetime import date as Date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

CONTRACT_VERSION = "0.2"

Tier = Literal["emergent", "urgent", "soon", "routine"]
TIER_ORDER = ("emergent", "urgent", "soon", "routine")          # same as pathway tier_order
Status = Literal["verified", "needs_manual_review", "error"]
# verified            - model answer passed every plain-code check
# needs_manual_review - the model answered twice and failed the checks both times
# error               - infrastructure failure (rate limit, timeout); rerun it, don't score it


class _M(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --- chart context (code) -----------------------------------------------------------------------

class ChartItem(_M):
    value: object = None
    unit: Optional[str] = None
    date: Optional[Date] = None
    days_ago: Optional[int] = None
    ref: str = Field(description="FHIR id, or the note ref for facts taken from the referral")
    display: Optional[str] = None
    from_note: bool = False


class ChartFact(_M):
    id: str = Field(description="pathway fact id")
    text: str
    found: bool
    items: list[ChartItem] = Field(default_factory=list)


class CitedFact(_M):
    """A fact the model chose to put in front of the specialist (verifier checked ref and quote)."""
    fact: str
    ref: str
    statement: str
    quote: Optional[str] = Field(None, description="exact note words, required when ref is the note")


# --- urgency ----------------------------------------------------------------------------------

class FlagHit(_M):
    id: str
    tier: Tier
    text: str
    why: list[str] = Field(default_factory=list, description="what matched, from the checklist")


class Urgency(_M):
    final: Tier = Field(description="max(floor, model) - never below the floor")
    floor: Tier = Field(description="set by the plain-code red-flag checklist")
    model: Optional[Tier] = Field(None, description="the model's suggestion; None unless verified")
    set_by: Literal["floor", "model"] = Field(description="'model' only when the model raised it above the floor")
    reason: str = Field(description="model's urgency_reason, or a code-written line from the flags")
    checklist_flags: list[FlagHit] = Field(default_factory=list, description="always from code, never the model")
    model_flags: list[str] = Field(default_factory=list)
    advise_er: bool = Field(description="final == emergent; the card shows 'advise ER now'")


# --- tests, options, fit (code row + model columns) ---------------------------------------------

class LastResult(_M):
    date: Optional[Date] = None
    ago: Optional[str] = None
    days_ago: Optional[int] = None
    value: object = None
    unit: Optional[str] = None
    display: Optional[str] = None
    ref: Optional[str] = None


class TestRow(_M):
    id: str
    name: str
    status: Literal["done", "out_of_date", "not_done", "not_recorded_in_source"]
    last: Optional[LastResult] = None
    valid_days: Optional[int] = None
    redo_if: list = Field(default_factory=list)
    prechecked: bool = Field(description="from the pathway (code)")
    include: Optional[bool] = Field(None, description="model's suggestion; None unless verified")
    why: Optional[str] = None
    depends_on: list[str] = Field(default_factory=list)


class DecisionGroup(_M):
    group: str = Field(description="heading shown beside the option, e.g. 'Heart-attack risk and symptoms'")
    facts: list[str] = Field(description="pathway fact ids; the screen shows their chart values next to the option")


class OptionRow(_M):
    """Never pre-ticked: the specialist decides. `relevant` only sorts and highlights."""
    id: str
    text: str
    kind: Optional[str] = Field(None, description="pathway option kind, e.g. advice, med_review")
    decision_facts: list[DecisionGroup] = Field(default_factory=list, description="from the pathway (code)")
    relevant: Optional[bool] = None
    why: Optional[str] = None
    depends_on: list[str] = Field(default_factory=list)


class Hint(_M):
    id: str
    text: str
    why: list[str] = Field(default_factory=list)


class Route(_M):
    id: str
    suggest_fit: Optional[str] = Field(None, description="None = a note for the specialist, not a fit change")
    note: str
    why: list[str] = Field(default_factory=list)


class Fit(_M):
    suggested: Optional[str] = Field(None, description="model's pick; None unless verified")
    reason: Optional[str] = None
    choices: dict[str, str] = Field(description="fit id -> text, from the pathway")
    routing: list[Route] = Field(default_factory=list, description="chart-based suggestions (code)")


# --- specialist + provenance ---------------------------------------------------------------------

class SpecialistInput(_M):
    selected_tests: list[str] = Field(default_factory=list)
    selected_options: list[str] = Field(default_factory=list)
    interim_plan_text: str = ""
    chosen_fit: Optional[str] = None
    urgency_confirmed: Optional[Tier] = None


class Provenance(_M):
    run_id: str
    created_at: datetime
    pathway_version: str
    model: Optional[str] = None
    model_version: Optional[str] = None
    request_hash: Optional[str] = None
    attempts: int = 0
    tokens: Optional[dict] = None


class Card(_M):
    contract_version: str = CONTRACT_VERSION
    case_id: str
    specialty: str
    status: Status
    reason_id: str
    reason_label: str
    referral_date: Date
    age: Optional[int] = None
    sex: Optional[str] = None
    note_ref: str
    note: str
    summary: Optional[str] = Field(None, description="one line for the queue; None unless verified")

    urgency: Urgency
    chart: list[ChartFact]
    cited_facts: list[CitedFact] = Field(default_factory=list)
    tests: list[TestRow]
    options: list[OptionRow]
    hints: list[Hint] = Field(default_factory=list)
    fit: Fit
    missing_info: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list, description="verifier warnings")
    problems: list[str] = Field(default_factory=list, description="verifier errors from the last attempt")

    specialist: SpecialistInput = Field(default_factory=SpecialistInput)
    provenance: Provenance


def queue_sort_key(card: Card, days_waiting: int = 0):
    """Emergent first, then urgent, soon, routine; longest-waiting first within a tier."""
    return (TIER_ORDER.index(card.urgency.final), -days_waiting)


# --- builder: copies only, no decisions -----------------------------------------------------------

def _first_value(chart, fid):
    f = chart.get(fid)
    return f["items"][0]["value"] if f and f["found"] and f["items"] else None


def build_card(case, prep, outcome, pathway, provenance) -> Card:
    """case: lantern.cases.load_case(); prep: lantern.llm.prepare(); outcome: verifier.call_and_verify()
    (or {'status': 'error', ...}); provenance: dict for Provenance."""
    reason = case["meta"]["reason"]
    r = pathway["reasons"][reason]
    ctx = prep["context"]
    ok = outcome.get("status") == "verified"
    ans = outcome.get("answer") if ok else None
    ans = ans or {}

    floor = prep["floor"]
    final = outcome.get("urgency") if ok else floor
    model_u = ans.get("urgency")
    raised = ok and model_u in TIER_ORDER and TIER_ORDER.index(model_u) < TIER_ORDER.index(floor)
    if ok and ans.get("urgency_reason"):
        why = ans["urgency_reason"]
    elif prep["flags"]:
        why = "Red-flag checklist: " + "; ".join(h["text"] for h in prep["flags"])
    else:
        why = "No red flags matched; model answer not available." if not ok else "No red flags matched."

    tests_ans = {t["test"]: t for t in ans.get("tests", [])}
    tests = []
    for t in ctx["tests"]:
        a = tests_ans.get(t["id"], {})
        tests.append(TestRow(id=t["id"], name=t["name"], status=t["status"], last=t["last"],
                             valid_days=t["valid_days"], redo_if=t["redo_if"], prechecked=t["prechecked"],
                             include=a.get("include"), why=a.get("why"), depends_on=a.get("depends_on", [])))

    opt_ans = {o["option"]: o for o in ans.get("options", [])}
    options = []
    for oid in r["interim_options"]:
        o, a = pathway["options"][oid], opt_ans.get(oid, {})
        options.append(OptionRow(id=oid, text=o["text"], kind=o.get("kind"), decision_facts=o.get("decision_facts", []),
                                 relevant=a.get("relevant"), why=a.get("why"), depends_on=a.get("depends_on", [])))

    attempts = outcome.get("attempts", [])
    last_check = next((a.get("check") for a in reversed(attempts) if a.get("check")), None) or {}
    return Card(
        case_id=case["id"], specialty=pathway["specialty"], status=outcome.get("status", "error"),
        reason_id=reason, reason_label=r["label"], referral_date=case["meta"]["referral_date"],
        age=_first_value(ctx["facts"], "age"), sex=_first_value(ctx["facts"], "sex"),
        note_ref=ctx["note_ref"], note=case["note"], summary=ans.get("summary"),
        urgency=Urgency(final=final, floor=floor, model=model_u if ok else None,
                        set_by="model" if raised else "floor", reason=why,
                        checklist_flags=[FlagHit(**{k: h.get(k) for k in ("id", "tier", "text")},
                                                 why=h.get("why") or []) for h in prep["flags"]],
                        model_flags=ans.get("urgency_flags", []), advise_er=(final == "emergent")),
        chart=list(ctx["facts"].values()), cited_facts=ans.get("facts", []), tests=tests, options=options,
        hints=prep.get("hints", []),
        fit=Fit(suggested=ans.get("fit"), reason=ans.get("fit_reason"),
                choices={f: pathway["fits"][f] for f in r["fit_choices"]}, routing=prep.get("routes", [])),
        missing_info=ans.get("missing_info", []), warnings=outcome.get("warnings", []) if ok else [],
        problems=[] if ok else last_check.get("errors", []),
        provenance=Provenance(**{**provenance, "attempts": len(attempts)}),
    )
