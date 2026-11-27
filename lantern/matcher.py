"""Plain-code rule engine: evaluates pathway conditions against the referral note and the cut chart.

This is the red-flag checklist from CLAUDE.md. It runs before the LLM and sets an urgency floor
that the LLM can only raise. Nothing here calls a model.

Condition grammar (see pathways/schema.json):
  all / any / not                      combine conditions
  text_any:  [phrases]                 any phrase in the note, as whole words, not negated, not history
  text_regex: "pattern"                regex on the lower-cased note, same negation/history rules
  fact_present: fact_id                fact found in the chart (condition active, outpatient med, procedure)
  fact_count: {fact, op, value}        number of distinct matching medicines / conditions
  chart_obs: {fact, op, value|range, within_days}   latest observation on or before the referral date
"""
import re
from datetime import date

from lantern.chart import (_display, active_conditions, condition_matches, current_meds, med_matches,
                           observations, procedures, resources)

TIER_FLAG_LISTS = [("red_flags", "emergent"), ("urgent_flags", "urgent"), ("soon_flags", "soon")]

# A match is ignored if one of these appears earlier in the same clause, within NEG_WINDOW characters.
NEGATION_CUES = r"\b(no|not|denies|denied|denying|without|negative for|never|free of|absence of|nor)\b"
NEG_WINDOW = 60
# ...or if it is described as past history.
HISTORY_CUES = r"\b(history of|hx of|hx|h/o|s/p|status post|prior|previous|remote)\b"
# Not "past"/"old": "for the past two weeks" and "a 70 year old" describe the present.
HIST_WINDOW = 25
# ...or if a past date follows it closely ("STEMI Jan '25", "MI in 2019").
MONTHS = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
PAST_DATE_AFTER = re.compile(r"^[^.;:\n]{0,12}?\b(" + MONTHS + r"\b|in (19|20)\d\d|'\d\d|(19|20)\d\d)")
CLAUSE_BREAK = re.compile(r"[.;:\n!?]|\bbut\b|\bhowever\b|\bthen\b|\bnow\b|\bwhich\b"
                          r"|\band (i|he|she|they|we|it|his|her|their|my)\b")


def _clause_before(text, start, window):
    """Text from the start of the clause (or `window` chars back) up to `start`."""
    seg = text[max(0, start - window):start]
    breaks = list(CLAUSE_BREAK.finditer(seg))
    return seg[breaks[-1].end():] if breaks else seg


def negated(text, start):
    return re.search(NEGATION_CUES, _clause_before(text, start, NEG_WINDOW)) is not None


def historical(text, start, end):
    if re.search(HISTORY_CUES, _clause_before(text, start, HIST_WINDOW)):
        return True
    return PAST_DATE_AFTER.search(text[end:end + 40]) is not None


def _phrase_regex(phrase):
    return re.compile(r"(?<![a-z0-9])" + re.escape(phrase.lower()) + r"(?![a-z0-9])")


def text_hits(pattern, text):
    """Spans where `pattern` matches as a current, non-negated statement."""
    out = []
    for m in pattern.finditer(text):
        if not negated(text, m.start()) and not historical(text, m.start(), m.end()):
            out.append(m.group(0))
    return out


class Chart:
    """Facts from a cut bundle, looked up through config/fhir_map.yaml."""

    def __init__(self, bundle, fmap, referral_date):
        self.bundle, self.fmap, self.cutoff = bundle, fmap, referral_date
        self.conds = active_conditions(bundle, referral_date)
        self.meds = current_meds(bundle, referral_date, outpatient_only=True)
        self.patient = next((r for r in resources(bundle, "Patient")), {})

    def matches(self, fact):
        m = self.fmap["facts"].get(fact, {})
        hits = []
        hits += condition_matches(self.conds, m.get("conditions", []))
        hits += med_matches(self.meds, m.get("meds", []))
        if m.get("procedure_sct") and procedures(self.bundle, m["procedure_sct"]):
            hits.append("procedure")
        if m.get("loinc") and not (m.get("conditions") or m.get("meds")):
            hits += [str(v) for _, v, *_ in observations(self.bundle, m["loinc"])][-1:]
        return hits

    def count(self, fact):
        """Distinct medicine fragments (e.g. number of BP drug classes/agents) or conditions."""
        m = self.fmap["facts"].get(fact, {})
        names = " | ".join(n.lower() for n, _ in self.meds)
        meds = {f for f in m.get("meds", []) if f in names}
        conds = set(condition_matches(self.conds, m.get("conditions", [])))
        return len(meds) + len(conds)

    def latest(self, fact, within_days=None):
        obs = observations(self.bundle, self.fmap["facts"].get(fact, {}).get("loinc", []))
        obs = [o for o in obs if o[0] and o[1] is not None]
        if not obs:
            return None
        d, v, *_ = obs[-1]
        if within_days is not None and (date.fromisoformat(self.cutoff) - date.fromisoformat(d)).days > within_days:
            return None
        return v


OPS = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
       ">=": lambda a, b: a >= b, "==": lambda a, b: a == b}


def evaluate(cond, note, chart, why=None):
    """True/False. `why` (a list) collects the evidence that made it true."""
    why = why if why is not None else []
    if "all" in cond:
        sub = []
        ok = all(evaluate(c, note, chart, sub) for c in cond["all"])
        if ok:
            why += sub
        return ok
    if "any" in cond:
        for c in cond["any"]:
            sub = []
            if evaluate(c, note, chart, sub):
                why += sub
                return True
        return False
    if "not" in cond:
        return not evaluate(cond["not"], note, chart, [])
    text = note.lower()
    if "text_any" in cond:
        for ph in cond["text_any"]:
            hits = text_hits(_phrase_regex(ph), text)
            if hits:
                why.append(f"note: '{hits[0]}'")
                return True
        return False
    if "text_regex" in cond:
        hits = text_hits(re.compile(cond["text_regex"]), text)
        if hits:
            why.append(f"note: '{hits[0]}'")
        return bool(hits)
    if chart is None:
        return False
    if "fact_present" in cond:
        hits = chart.matches(cond["fact_present"])
        if hits:
            why.append(f"chart: {cond['fact_present']} ({hits[0]})")
        return bool(hits)
    if "fact_count" in cond:
        c = cond["fact_count"]
        n = chart.count(c["fact"])
        ok = OPS[c["op"]](n, c["value"])
        if ok:
            why.append(f"chart: {n} x {c['fact']}")
        return ok
    if "chart_obs" in cond:
        c = cond["chart_obs"]
        v = chart.latest(c["fact"], c.get("within_days"))
        if v is None:
            return False
        if c["op"] == "between":
            ok = c["range"][0] <= v <= c["range"][1]
        elif c["op"] == "outside":
            ok = v < c["range"][0] or v > c["range"][1]
        else:
            ok = OPS[c["op"]](v, c["value"])
        if ok:
            why.append(f"chart: {c['fact']} = {v}")
        return ok
    raise ValueError(f"unknown condition {list(cond)}")


def urgency_floor(pathway, note, chart):
    """Run EVERY reason's red/urgent/soon flags (a palpitations referral can still say chest pain at rest).
    Returns (floor_tier, [ {id, reason, tier, text, why} ... ]) - floor is 'routine' if nothing fires."""
    order = pathway["tier_order"]
    hits = []
    for rid, r in pathway["reasons"].items():
        for key, tier in TIER_FLAG_LISTS:
            for f in r.get(key, []):
                why = []
                if evaluate(f["match"], note, chart, why):
                    hits.append({"id": f["id"], "reason": rid, "tier": tier, "text": f["text"], "why": why})
    floor = min((h["tier"] for h in hits), key=order.index, default="routine")
    return floor, hits


def card_hints(pathway, reason, note, chart):
    out = []
    for f in pathway["reasons"][reason].get("card_hints", []):
        why = []
        if evaluate(f["match"], note, chart, why):
            out.append({"id": f["id"], "text": f["text"], "why": why})
    return out


def tests_for(pathway, reason, note, chart):
    """tests_first for the reason, keeping only those whose only_if holds."""
    out = []
    for t in pathway["reasons"][reason]["tests_first"]:
        if "only_if" not in t or evaluate(t["only_if"], note, chart, []):
            out.append(t["test"])
    return out


def routing(pathway, reason, note, chart):
    out = []
    for rr in pathway["reasons"][reason].get("routing_rules", []):
        why = []
        if evaluate(rr["if"], note, chart, why):
            out.append({"id": rr["id"], "suggest_fit": rr["suggest_fit"], "note": rr["note"], "why": why})
    return out
