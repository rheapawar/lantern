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
import functools
import os
import re
from datetime import date

import yaml

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
MONTHS = (r"(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|(?<=in )may|june?|july?|aug(ust)?|sep(t(ember)?)?"
          r"|oct(ober)?|nov(ember)?|dec(ember)?)\.?")
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


def _history_cue(text, start, end):
    if re.search(HISTORY_CUES, _clause_before(text, start, HIST_WINDOW)):
        return True
    return PAST_DATE_AFTER.search(text[end:end + 40]) is not None


# A mention dated more than this many days back is history, not the current problem.
PAST_DAYS = 90


def historical(text, start, end):
    """Past history: a history cue just before, a date just after, or its phrase is dated > PAST_DAYS ago
    ("syncope at a funeral in 2016", "ST depression ... last fall", "as a teen")."""
    if _history_cue(text, start, end):
        return True
    t = _timing_days(_segment(text, start, end))
    return t is not None and t > PAST_DAYS


# ...or if the same sentence goes on to say it went away. Only looks AFTER the mention and stops at "but",
# so "pain had settled, but ECG shows new ST elevation" still counts.
RESOLVED_AFTER = re.compile(
    r"\b(resolved|resolving|normali[sz]ed|no longer|not recurred|no recurrence|nothing since|none since"
    r"|no (?:\w+ ){0,2}since|(?:repeat|follow-up|later)\b[^.;]{0,30}\b(?:normal|unremarkable|resolved))\b")
SENTENCE_END = re.compile(r"[;!?\n]|(?<!\d)\.(?!\d)|\bbut\b|\bhowever\b")


def resolved(text, end):
    stop = SENTENCE_END.search(text, end)
    return RESOLVED_AFTER.search(text, end, stop.start() if stop else len(text)) is not None


def _phrase_regex(phrase):
    return re.compile(r"(?<![a-z0-9])" + re.escape(phrase.lower()) + r"(?![a-z0-9])")


# ...or (only in the tiers the pathway's `explained_cue` names, never red flags) if the same clause pins it on
# another cause: "knee swollen from an arthritis flare", "SOB unchanged for years from asthma".
# The gap may not cross a comma or "and", so "leg swelling and SOB from asthma" still counts the swelling.
EXPLAINED_AFTER = re.compile(
    r"(?:(?!\band\b)[^,;.\n]){0,40}?\b(?:from|due to|caused by|secondary to|because of|attributed to|related to)\b"
    r"(?P<cause>[^,;.\n]{0,40})")
# a hedged cause is not an explanation: "likely from asthma", "? from reflux", "asthma vs heart"
HEDGE = re.compile(r"\?|\b(?:likely|probably|possibly|possible|maybe|may|might|presumed|thought|suspect\w*"
                   r"|unclear|unknown|uncertain|vs|versus|or|query|r/o|rule out)\b")


def explained(text, start, end, own_cause_terms):
    m = EXPLAINED_AFTER.match(text, end)
    if not m:
        return False
    window = text[max(0, start - 30):m.end()]
    if HEDGE.search(window):
        return False
    cause = m.group("cause")
    return not any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", cause) for w in own_cause_terms)


def text_hits(pattern, text, explain=None):
    """Spans where `pattern` matches as a current, non-negated statement.
    `explain` = own-cause terms when the explained-by-another-cause cue applies (urgent/soon tiers only)."""
    out = []
    for m in pattern.finditer(text):
        if negated(text, m.start()) or historical(text, m.start(), m.end()) or resolved(text, m.end()):
            continue
        if explain is not None and explained(text, m.start(), m.end(), explain):
            continue
        out.append(m.group(0))
    return out


# --- Numbers in the note ----------------------------------------------------------------------------
# Reads measurements the way people write them, not as fixed strings. Names come from
# config/note_metrics.yaml; the grammar below is general.

METRICS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "note_metrics.yaml")

# a value: 140, 1,750, 0.52, 130s, "high 30s"
NUM = r"(?:(?P<q>low|mid|high)[- ]?)?(?P<n>\d{1,3}(?:,\d{3})+(?!\d)|\d+(?:\.\d+)?)(?P<s>s(?![a-z]))?"
# a BP pair: 190/110, 190 over 110, 190s/110s
PAIR = re.compile(r"(?<![\d/.])(?P<a>\d{2,3})(?P<as>s)?\s*(?:/|\bover\b)\s*(?P<b>\d{2,3})(?P<bs>s)?(?![\d/])")
# a number followed by one of these is a count, duration, dose or date part, not a measurement
NOT_A_READING = re.compile(r"\s*(?:years?|yrs?|y/?o|months?|mos?|weeks?|wks?|days?|hours?|hrs?|h|minutes?|mins?"
                           r"|mg|mcg|g|kg|lbs?|pounds|%|mm|cm|ml|l|times|x|pillows?|blocks?|flights?|episodes?"
                           r"|am|pm|st|nd|rd|th)\b|\s*/\s*\d")
# gap between a name and its value: short, no other number, no sentence break
GAP = r"[^\d.;\n]{0,30}?"
# when a reading was taken -> age in days
WORD_NUM = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "few": 3, "couple of": 2}
UNIT_DAYS = {"day": 1, "week": 7, "wk": 7, "month": 30, "mo": 30, "year": 365, "yr": 365,
             "fall": 180, "autumn": 180, "spring": 180, "summer": 180, "winter": 180}
AGO = re.compile(r"\b(\d+|a|an|one|two|three|four|five|six|few|couple of)\s+(day|week|wk|month|mo|year|yr)s?\s+ago\b")
LAST = re.compile(r"\blast\s+(week|wk|month|mo|year|yr|visit|time|fall|autumn|spring|summer|winter)\b")
YESTERDAY = re.compile(r"\b(yesterday|last night)\b")
IN_YEAR = re.compile(r"\bin\s+(19|20)\d\d\b")
EARLIER = re.compile(r"\b(previously|earlier|prior|previous)\b")
SEGMENT_BREAK = re.compile(r"[,;\n]|(?<!\d)\.(?!\d)|\b(but|now|then|however|vs|versus)\b")
OLD = 10 ** 6   # history with no stated time: older than anything dated


def _metric_cfg():
    if not hasattr(_metric_cfg, "cfg"):
        with open(METRICS_PATH) as fh:
            _metric_cfg.cfg = yaml.safe_load(fh)
    return _metric_cfg.cfg


def _value(m, a="n", q="q", s="s"):
    v = float(m.group(a).replace(",", ""))
    if m.groupdict().get(s) and v == int(v) and int(v) % 10 == 0:      # a decade: 130s -> 135, high 30s -> 38
        v += {"low": 2, "mid": 5, "high": 8}.get(m.groupdict().get(q) or "", 5)
    return v


def _segment(text, start, end):
    """The phrase around a reading: from the last break before it to the next break after it."""
    before = list(SEGMENT_BREAK.finditer(text, max(0, start - 40), start))
    after = SEGMENT_BREAK.search(text, end, min(len(text), end + 40))
    return text[before[-1].end() if before else max(0, start - 40): after.start() if after else min(len(text), end + 40)]


SINCE = re.compile(r"\bsince\s+(?:last\s+\w+|in\s+\w+|\w+)")          # "since last month" = still going on
LIFE_STAGE = re.compile(r"\bas an? (?:child|kid|teen|teenager|adolescent|young adult)\b"
                        r"|\bin (?:his|her|their) (?:teens|twenties|childhood)\b|\bchildhood\b")
MONTH_NAMED = re.compile(r"\b(?:in|on|during|from)\s+" + MONTHS + r"(?![a-z])")


def _timing_days(seg):
    """How long ago a phrase says something happened, in days; None if it gives no timing."""
    seg = SINCE.sub(" ", seg)
    m = AGO.search(seg)
    if m:
        n = int(m.group(1)) if m.group(1).isdigit() else WORD_NUM[m.group(1)]
        return n * UNIT_DAYS[m.group(2)]
    m = LAST.search(seg)
    if m:
        return UNIT_DAYS.get(m.group(1), 30)
    if YESTERDAY.search(seg):
        return 1
    if IN_YEAR.search(seg) or LIFE_STAGE.search(seg):
        return 365 if IN_YEAR.search(seg) else OLD
    if MONTH_NAMED.search(seg):
        return 120          # a named month with no year: treated as months back (unknown exactly)
    if EARLIER.search(seg):
        return OLD
    return None


def _age_days(text, start, end):
    """Days since a measurement, from timing words in its phrase. 0 = now / unstated; OLD = history, no date."""
    if _history_cue(text, start, end):
        return OLD
    t = _timing_days(_segment(text, start, end))
    return 0 if t is None else t


def _name_regex(cfg):
    alts = [re.escape(n) for n in cfg.get("names", [])] + ([cfg["names_regex"]] if cfg.get("names_regex") else [])
    return r"(?<![a-z0-9])(?:" + "|".join(alts) + r")(?![a-z0-9])" if alts else None


@functools.lru_cache(maxsize=512)
def note_readings(text):
    """{metric: [(position, value, age_days), ...]} for every measurement written in the note."""
    cfg = _metric_cfg()
    out, taken = {}, []
    sys_id, dia_id = cfg["bp_pair"]
    lo_s, hi_s = cfg["metrics"][sys_id]["range"]
    lo_d, hi_d = cfg["metrics"][dia_id]["range"]
    for m in PAIR.finditer(text):
        a, b = _value(m, "a", "q", "as"), _value(m, "b", "q", "bs")
        if lo_s <= a <= hi_s and lo_d <= b <= hi_d and a > b:
            age = _age_days(text, m.start(), m.end())
            out.setdefault(sys_id, []).append((m.start(), a, age))
            out.setdefault(dia_id, []).append((m.start(), b, age))
            taken.append((m.start(), m.end()))
    names = {mid: _name_regex(c) for mid, c in cfg["metrics"].items()}
    any_name = re.compile("|".join(f"(?:{r})" for r in names.values() if r))
    for mid, c in cfg["metrics"].items():
        lo, hi = c["range"]
        found = []
        if names[mid]:
            after_name = re.compile("(?P<gap>" + GAP + ")" + NUM)
            other = c.get("not_followed_by")
            other = re.compile(r"\s*(?:" + "|".join(map(re.escape, other)) + r")\b") if other else None
            for nm in re.finditer(names[mid], text):          # each name separately, so "qt ... qtc 505" reads qtc
                if other and other.match(text, nm.end()):
                    continue                                   # e.g. "pulse ox": a different measurement
                m = after_name.match(text, nm.end())
                if m and not any_name.search(m.group("gap")):  # else the number belongs to a later name
                    found.append(m)
        for u in c.get("units_after", []):
            found += list(re.finditer(r"(?<![\d.,])" + NUM + r"\s*" + re.escape(u) + r"\b", text))
        for m in found:
            ns, ne = m.start("n"), m.end()
            if any(s <= ns < e for s, e in taken) or NOT_A_READING.match(text, ne):
                continue
            if re.search(NEGATION_CUES, text[max(0, m.start() - 12):m.start()]):
                continue
            v = _value(m)
            unit = re.match(r"\s*([a-z]+)", text[ne:])
            if unit and unit.group(1) in c.get("scale", {}):
                v *= c["scale"][unit.group(1)]
            if lo <= v <= hi:
                out.setdefault(mid, []).append((m.start(), v, _age_days(text, m.start(), ne)))
                taken.append((ns, ne))
    return out


def latest_reading(text, metric, within_days=None):
    """The newest reading of `metric` in the note (smallest age; ties -> written last), or None."""
    rs = [r for r in note_readings(text).get(metric, []) if r[2] < OLD]
    if within_days is not None:
        rs = [r for r in rs if r[2] <= within_days]
    if not rs:
        return None
    return min(rs, key=lambda r: (r[2], -r[0]))[1]


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


def _compare(v, c):
    if c["op"] == "between":
        return c["range"][0] <= v <= c["range"][1]
    if c["op"] == "outside":
        return v < c["range"][0] or v > c["range"][1]
    return OPS[c["op"]](v, c["value"])


def evaluate(cond, note, chart, why=None, explain=None):
    """True/False. `why` (a list) collects the evidence that made it true.
    `explain`: own-cause terms if the explained-by-another-cause cue applies to this flag's tier."""
    why = why if why is not None else []
    if "all" in cond:
        sub = []
        ok = all(evaluate(c, note, chart, sub, explain) for c in cond["all"])
        if ok:
            why += sub
        return ok
    if "any" in cond:
        for c in cond["any"]:
            sub = []
            if evaluate(c, note, chart, sub, explain):
                why += sub
                return True
        return False
    if "not" in cond:
        return not evaluate(cond["not"], note, chart, [], explain)
    text = note.lower()
    if "text_any" in cond:
        for ph in cond["text_any"]:
            hits = text_hits(_phrase_regex(ph), text, explain)
            if hits:
                why.append(f"note: '{hits[0]}'")
                return True
        return False
    if "text_regex" in cond:
        hits = text_hits(re.compile(cond["text_regex"]), text, explain)
        if hits:
            why.append(f"note: '{hits[0]}'")
        return bool(hits)
    if "text_obs" in cond:
        c = cond["text_obs"]
        v = latest_reading(text, c["fact"], c.get("within_days"))
        ok = v is not None and _compare(v, c)
        if ok:
            why.append(f"note: {c['fact']} = {v:g}")
        return ok
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
        ok = _compare(v, c)
        if ok:
            why.append(f"chart: {c['fact']} = {v}")
        return ok
    raise ValueError(f"unknown condition {list(cond)}")


def urgency_floor(pathway, note, chart):
    """Run EVERY reason's red/urgent/soon flags (a palpitations referral can still say chest pain at rest).
    Returns (floor_tier, [ {id, reason, tier, text, why} ... ]) - floor is 'routine' if nothing fires."""
    order = pathway["tier_order"]
    cue = pathway.get("explained_cue") or {}
    hits = []
    for rid, r in pathway["reasons"].items():
        for key, tier in TIER_FLAG_LISTS:
            # red flags (the top tier) never take the cue, whatever the pathway file says
            explain = cue["own_cause_terms"] if tier in cue.get("tiers", []) and tier != order[0] else None
            for f in r.get(key, []):
                why = []
                if evaluate(f["match"], note, chart, why, explain):
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
