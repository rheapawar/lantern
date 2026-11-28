"""A small hand-made case (synthetic, committed) so safety tests run on a fresh clone without Synthea data.

70-year-old woman, chest pain referral: hypertension, lisinopril, BP panel 134/82, LDL 129.73,
eGFR 13.4, A1c 7.28, a resolved pneumonia; the note describes worsening exertional chest tightness
(red-flag floor: urgent).
"""
REFERRAL_DATE = "2025-01-07"

NOTE = ("70 year old woman with hypertension on lisinopril and type 2 diabetes (last A1c 7.3%). "
        "Over the past 3 to 4 weeks she gets tightness in her chest when she walks uphill, and it is coming "
        "on more often. Her brother had a heart attack at 52. Could you see her to evaluate for angina?")


def _obs(code, value, unit, when):
    return {"resourceType": "Observation", "status": "final", "effectiveDateTime": when,
            "code": {"coding": [{"system": "http://loinc.org", "code": code}]},
            "valueQuantity": {"value": value, "unit": unit}}


def bundle():
    rs = [
        {"resourceType": "Patient", "id": "pt", "birthDate": "1954-06-02", "gender": "female"},
        {"resourceType": "Condition", "id": "htn", "onsetDateTime": "2015-03-01",
         "code": {"text": "Essential hypertension (disorder)"}},
        {"resourceType": "Condition", "id": "dm", "onsetDateTime": "2018-05-01",
         "code": {"text": "Diabetes mellitus type 2 (disorder)"}},
        {"resourceType": "Condition", "id": "pna", "onsetDateTime": "2020-01-01", "abatementDateTime": "2020-02-01",
         "code": {"text": "Pneumonia (disorder)"}},
        {"resourceType": "MedicationRequest", "id": "lis", "status": "active", "authoredOn": "2024-10-01",
         "medicationCodeableConcept": {"text": "lisinopril 10 MG Oral Tablet"}},
        {"resourceType": "Observation", "id": "bp", "status": "final", "effectiveDateTime": "2024-04-20",
         "code": {"coding": [{"code": "85354-9"}]},
         "component": [{"code": {"coding": [{"code": "8480-6"}]}, "valueQuantity": {"value": 134, "unit": "mm[Hg]"}},
                       {"code": {"coding": [{"code": "8462-4"}]}, "valueQuantity": {"value": 82, "unit": "mm[Hg]"}}]},
        {**_obs("18262-6", 129.73, "mg/dL", "2024-04-20"), "id": "ldl"},
        {**_obs("33914-3", 13.4, "mL/min/{1.73_m2}", "2024-04-20"), "id": "egfr"},
        {**_obs("4548-4", 7.28, "%", "2024-04-20"), "id": "a1c"},
        {"resourceType": "ServiceRequest", "id": "ref", "authoredOn": REFERRAL_DATE},
    ]
    return {"resourceType": "Bundle", "entry": [{"fullUrl": f"urn:uuid:{r['id']}", "resource": r} for r in rs]}


def case():
    return {"id": "fixture", "note": NOTE, "bundle": bundle(),
            "meta": {"case_id": "fixture", "specialty": "cardiology", "reason": "chest_pain",
                     "referral_date": REFERRAL_DATE}}
