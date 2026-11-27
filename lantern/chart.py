"""Read a Synthea FHIR R4 bundle: cut it at the referral date and look things up via config/fhir_map.yaml.

The referral-date cutoff is the most important rule in Lantern: nothing dated after the referral
may reach the engine. cut_at() removes later resources, strips later dates from kept ones, and
check_no_future_dates() fails loudly if any later date survives.
"""
import copy
import json
import re
from datetime import date

import yaml

DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})")

# Where each resource type keeps the date that decides if it existed by the referral date.
DATE_FIELDS = {
    "Encounter": [("period", "start")],
    "Condition": [("onsetDateTime",), ("recordedDate",)],
    "Observation": [("effectiveDateTime",), ("issued",)],
    "DiagnosticReport": [("effectiveDateTime",), ("issued",)],
    "Procedure": [("performedPeriod", "start"), ("performedDateTime",)],
    "MedicationRequest": [("authoredOn",)],
    "MedicationAdministration": [("effectiveDateTime",), ("effectivePeriod", "start")],
    "Immunization": [("occurrenceDateTime",)],
    "CarePlan": [("period", "start")],
    "CareTeam": [("period", "start")],
    "Claim": [("billablePeriod", "start"), ("created",)],
    "ExplanationOfBenefit": [("billablePeriod", "start"), ("created",)],
    "ImagingStudy": [("started",)],
    "AllergyIntolerance": [("recordedDate",)],
    "DocumentReference": [("date",)],
    "Media": [("createdDateTime",)],
    "SupplyDelivery": [("occurrenceDateTime",)],
    "Device": [("manufactureDate",)],
}
_BY_URL = {}
INPATIENT_CLASSES = {"IMP", "EMER", "ACUTE", "NONAC", "OBSENC", "SS"}
KEEP_UNDATED = {"Patient", "Organization", "Practitioner", "PractitionerRole", "Location", "Medication"}
# Provenance lists every resource (incl. future ones); Claim/EOB are billing, can be created after the
# visit and point at later procedures. None of them is clinical information Lantern needs.
DROP_ALWAYS = {"Provenance", "Claim", "ExplanationOfBenefit"}


def _get(res, path):
    for k in path:
        if not isinstance(res, dict) or k not in res:
            return None
        res = res[k]
    return res


def res_date(res):
    for path in DATE_FIELDS.get(res["resourceType"], []):
        v = _get(res, path)
        if v:
            return v[:10]
    return None


def load_bundle(path):
    with open(path) as fh:
        return json.load(fh)


def cut_at(bundle, cutoff):
    """Return (new_bundle, report). cutoff is 'YYYY-MM-DD'; records ON that date are kept."""
    out = copy.deepcopy(bundle)
    global _BY_URL
    _BY_URL = {e.get("fullUrl"): e["resource"] for e in bundle["entry"]}
    kept, report = [], {"dropped_future": 0, "dropped_undated": {}, "stripped": []}
    for e in out["entry"]:
        r = e["resource"]
        t = r["resourceType"]
        if t in DROP_ALWAYS:
            continue
        if t in KEEP_UNDATED:
            _strip_future(r, cutoff, report)
            kept.append(e)
            continue
        d = res_date(r)
        if d is None:
            report["dropped_undated"][t] = report["dropped_undated"].get(t, 0) + 1
            continue
        if d > cutoff:
            report["dropped_future"] += 1
            continue
        _strip_future(r, cutoff, report)
        kept.append(e)
    out["entry"] = kept
    kept_urls = {e.get("fullUrl") for e in kept}
    report["dangling_refs"] = sorted({ref for e in kept for ref in _refs(e["resource"])
                                      if ref.startswith("urn:uuid:") and ref not in kept_urls})
    return out, report


def _strip_future(r, cutoff, report):
    t = r["resourceType"]
    if t == "Patient" and (r.get("deceasedDateTime") or "")[:10] > cutoff:
        r.pop("deceasedDateTime"); report["stripped"].append("Patient.deceasedDateTime")
    if t == "Condition" and (r.get("abatementDateTime") or "")[:10] > cutoff:
        r.pop("abatementDateTime"); r["clinicalStatus"] = {"coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]}
        report["stripped"].append("Condition.abatementDateTime")
    if t == "MedicationRequest" and r.get("status") in ("stopped", "completed"):
        # Synthea sets 'stopped'/'completed' when the drug ended, which may be after the referral -> 'unknown'.
        # Exception: a one-off given during a hospital/ER stay that ended by the cutoff stays 'completed'
        # (known on the referral date). by_url is attached by cut_at.
        enc = _BY_URL.get((r.get("encounter") or {}).get("reference", ""), {})
        end = ((enc.get("period") or {}).get("end") or "")[:10]
        inpatient = (enc.get("class") or {}).get("code") in INPATIENT_CLASSES
        if not (r["status"] == "completed" and inpatient and end and end <= cutoff):
            r["status"] = "unknown"
    if t == "Device":
        r.pop("expirationDate", None)
    _strip_nested_ends(r, cutoff, report, t)


def _strip_nested_ends(x, cutoff, report, where):
    """Remove any 'end' or 'abatementDateTime' later than the cutoff, at any depth (periods that were still open)."""
    if isinstance(x, dict):
        for k in list(x):
            v = x[k]
            if k in ("end", "abatementDateTime") and isinstance(v, str) and v[:10] > cutoff:
                x.pop(k); report["stripped"].append(f"{where}.{k}")
            else:
                _strip_nested_ends(v, cutoff, report, f"{where}.{k}")
    elif isinstance(x, list):
        for v in x:
            _strip_nested_ends(v, cutoff, report, where)


def _refs(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "reference" and isinstance(v, str):
                yield v
            else:
                yield from _refs(v)
    elif isinstance(x, list):
        for y in x:
            yield from _refs(y)


def check_no_future_dates(bundle, cutoff):
    """Every YYYY-MM-DD string anywhere in the bundle must be <= cutoff. Returns offending paths."""
    bad = []

    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
        elif isinstance(x, str):
            for d in DATE_RE.findall(x):
                if d > cutoff:
                    bad.append((path, d))
    for e in bundle["entry"]:
        walk(e["resource"], e["resource"]["resourceType"])
    return bad


def add_service_request(bundle, case_id, specialty, cutoff, visit_id, note, reason_label):
    patient = next(e for e in bundle["entry"] if e["resource"]["resourceType"] == "Patient")
    enc = next((e for e in bundle["entry"] if e["resource"]["resourceType"] == "Encounter"
                and e["resource"]["id"] == visit_id), None)
    sr = {
        "resourceType": "ServiceRequest",
        "id": f"referral-{case_id}",
        "status": "active",
        "intent": "order",
        "category": [{"coding": [{"system": "http://snomed.info/sct", "code": "3457005",
                                  "display": "Patient referral"}]}],
        "code": {"text": f"Referral to {specialty}"},
        "reasonCode": [{"text": reason_label}],
        "subject": {"reference": patient["fullUrl"]},
        "authoredOn": cutoff,
        "note": [{"text": note}],
    }
    if enc:
        sr["encounter"] = {"reference": enc["fullUrl"]}
    bundle["entry"].append({"fullUrl": f"urn:uuid:referral-{case_id}", "resource": sr,
                            "request": {"method": "POST", "url": "ServiceRequest"}})
    return sr


# ---------------------------------------------------------------- lookups via fhir_map

def load_map(path="config/fhir_map.yaml"):
    with open(path) as fh:
        return yaml.safe_load(fh)


def _codes(cc):
    return {c.get("code") for c in (cc or {}).get("coding", [])}


def _display(cc):
    cc = cc or {}
    return (cc.get("text") or next((c.get("display") for c in cc.get("coding", []) if c.get("display")), "")) or ""


def resources(bundle, rtype):
    return [e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == rtype]


def observations(bundle, loincs):
    """[(date, value, unit, display)] for matching codes, including panel components (e.g. BP)."""
    out = []
    for r in resources(bundle, "Observation"):
        d = res_date(r)
        if _codes(r.get("code")) & set(loincs) and "valueQuantity" in r:
            q = r["valueQuantity"]; out.append((d, q.get("value"), q.get("unit"), _display(r["code"])))
        for c in r.get("component", []):
            if _codes(c.get("code")) & set(loincs) and "valueQuantity" in c:
                q = c["valueQuantity"]; out.append((d, q.get("value"), q.get("unit"), _display(c["code"])))
    return sorted(out, key=lambda x: x[0] or "")


def procedures(bundle, codes):
    return sorted(res_date(r) for r in resources(bundle, "Procedure") if _codes(r.get("code")) & set(codes))


def active_conditions(bundle, cutoff):
    """Display names of conditions active on the cutoff date. '(finding)' entries are skipped for matching."""
    out = []
    for r in resources(bundle, "Condition"):
        ab = (r.get("abatementDateTime") or "")[:10]
        if ab and ab <= cutoff:
            continue
        out.append((res_date(r), _display(r.get("code"))))
    return sorted(set(out))


def current_meds(bundle, cutoff, days=365, outpatient_only=True):
    """Medicines prescribed within `days` before the cutoff. By default, one-off drugs given during a
    hospital or ER stay (status 'completed' on an inpatient encounter) are skipped; discharge
    prescriptions from that stay are kept."""
    c = date.fromisoformat(cutoff)
    out = {}
    by_url = {e.get("fullUrl"): e["resource"] for e in bundle["entry"]}
    for r in resources(bundle, "MedicationRequest"):
        d = res_date(r)
        if outpatient_only:
            enc = by_url.get((r.get("encounter") or {}).get("reference", ""), {})
            if (enc.get("class") or {}).get("code") in INPATIENT_CLASSES and r.get("status") == "completed":
                continue
        if d and (c - date.fromisoformat(d)).days <= days:
            name = med_name(r, by_url)
            out[name] = max(out.get(name, ""), d)
    return sorted(out.items())


def med_name(r, by_url):
    """Drug name from medicationCodeableConcept, or from the Medication resource it references."""
    if r.get("medicationCodeableConcept"):
        return _display(r["medicationCodeableConcept"])
    ref = (r.get("medicationReference") or {}).get("reference", "")
    med = by_url.get(ref) or next((m for m in by_url.values() if m.get("resourceType") == "Medication"
                                   and ref.endswith("/" + m.get("id", "?"))), None)
    return _display((med or {}).get("code")) or "(unnamed medicine)"


def condition_matches(conds, frags):
    return [n for _, n in conds if "(finding)" not in n.lower() and any(f in n.lower() for f in frags)]


def med_matches(meds, frags):
    return [n for n, _ in meds if any(f in n.lower() for f in frags)]


def days_between(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days
