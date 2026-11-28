"""Tests for lantern/matcher.py: the plain-code red-flag checklist and chart rules.

Held-out cases are never evaluated or printed here (overfitting guard, CLAUDE.md).
"""
import csv
import json
import os
import sys
import unittest
import warnings

from lantern.chart import load_map
from lantern.matcher import Chart, card_hints, evaluate, routing, tests_for, urgency_floor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _json(path):
    with open(path) as fh:
        return json.load(fh)


PATHWAY = _json(os.path.join(ROOT, "pathways", "cardiology.json"))
FMAP = load_map(os.path.join(ROOT, "config", "fhir_map.yaml"))
REF_DATE = "2026-06-01"


def floor(note, chart=None):
    return urgency_floor(PATHWAY, note, chart)[0]


def fired(note, chart=None):
    return {h["id"] for h in urgency_floor(PATHWAY, note, chart)[1]}


def synthetic_chart():
    """A tiny bundle: active hypertension, resolved pneumonia, 3 BP meds, an inpatient one-off,
    low potassium 30 days ago, TSH 9 last year."""
    def entry(i, r):
        r["id"] = str(i)
        return {"fullUrl": f"urn:uuid:{i}", "resource": r}

    def med(name, when, status="active", enc=None):
        r = {"resourceType": "MedicationRequest", "status": status, "authoredOn": when,
             "medicationCodeableConcept": {"text": name}}
        if enc:
            r["encounter"] = {"reference": enc}
        return r

    def obs(code, value, when):
        return {"resourceType": "Observation", "effectiveDateTime": when,
                "code": {"coding": [{"code": code}]}, "valueQuantity": {"value": value, "unit": "x"}}

    rs = [
        {"resourceType": "Patient", "birthDate": "1960-01-01", "gender": "female"},
        {"resourceType": "Condition", "onsetDateTime": "2015-01-01", "code": {"text": "Essential hypertension (disorder)"}},
        {"resourceType": "Condition", "onsetDateTime": "2020-01-01", "abatementDateTime": "2020-02-01",
         "code": {"text": "Pneumonia (disorder)"}},
        {"resourceType": "Encounter", "class": {"code": "IMP"}, "period": {"start": "2026-01-10", "end": "2026-01-12"}},
        med("lisinopril 10 MG Oral Tablet", "2026-03-01"),
        med("amlodipine 5 MG Oral Tablet", "2026-03-01"),
        med("hydrochlorothiazide 25 MG Oral Tablet", "2026-03-01"),
        med("ibuprofen 400 MG Oral Tablet", "2026-01-10", status="completed", enc="urn:uuid:3"),
        obs("2823-3", 3.2, "2026-05-02"),
        obs("3016-3", 9.0, "2025-07-01"),
    ]
    bundle = {"resourceType": "Bundle", "entry": [entry(i, r) for i, r in enumerate(rs)]}
    return Chart(bundle, FMAP, REF_DATE)


class TextRules(unittest.TestCase):
    def test_negation(self):
        self.assertEqual(floor("Denies chest pain at rest. Mild ankle swelling."), "routine")
        self.assertNotIn("hf_syncope", fired("Denies fainting or chest pain."))
        self.assertEqual(floor("No headache, no chest pain, no vision change."), "routine")

    def test_negation_does_not_cross_into_a_new_statement(self):
        self.assertIn("palp_new_af_rvr",
                      fired("He has never had this before and I suspect new atrial fibrillation, pulse fast at 130."))

    def test_history_is_not_current(self):
        self.assertNotIn("ecg_active_mi", fired("80M, history of STEMI, now stable."))
        self.assertNotIn("ecg_active_mi", fired("80M, STEMI Jan '25, remote CABG."))
        self.assertIn("ecg_active_mi", fired("ECG today shows STEMI."))

    def test_present_tense_words_are_not_history(self):
        self.assertEqual(floor("70 year old man. For the past two weeks he gets chest pain walking up stairs, new for him."),
                         "urgent")

    def test_whole_words_only(self):
        self.assertNotIn("palp_stroke_symptoms", fired("Alzheimer's dementia, LDL 124."))
        self.assertIn("palp_stroke_symptoms", fired("Palpitations, then a TIA last week."))

    def test_chest_symptom_wording(self):
        self.assertEqual(floor("Tightness in her chest when she climbs stairs, coming on more often."), "urgent")
        self.assertEqual(floor("Pressure in the middle of her chest since she woke up, hasn't gone away."), "emergent")

    def test_red_flags_from_every_reason(self):
        """A palpitations referral that mentions chest pain at rest is still emergent."""
        self.assertEqual(floor("Palpitations for a week; today chest pain at rest."), "emergent")

    def test_reason_specific_flags_need_their_main_symptom(self):
        self.assertEqual(floor("Ankle swelling for months, otherwise well."), "routine")
        self.assertEqual(floor("Palpitations for 3 weeks, now new ankle swelling."), "urgent")

    def test_numbers(self):
        self.assertEqual(floor("BP 186/124 today, no symptoms."), "urgent")
        self.assertEqual(floor("BP 210/125 and confused since this morning."), "emergent")
        self.assertIn("ecg_long_qt", fired("ECG: QTc came back around 510 ms."))
        self.assertNotIn("ecg_long_qt", fired("QTc 440 ms."))
        self.assertIn("ecg_high_grade_block", fired("ECG shows Mobitz type II block."))
        self.assertEqual(floor("NT-proBNP last week was 900 pg/mL."), "soon")
        self.assertEqual(floor("NT-proBNP 2,500."), "urgent")


def hr_chart(bpm, when=REF_DATE):
    """A chart with one heart-rate reading."""
    rs = [{"resourceType": "Patient", "birthDate": "1960-01-01", "gender": "male"},
          {"resourceType": "Observation", "effectiveDateTime": when, "code": {"coding": [{"code": "8867-4"}]},
           "valueQuantity": {"value": bpm, "unit": "/min"}}]
    bundle = {"resourceType": "Bundle", "entry": [{"fullUrl": f"urn:uuid:{i}", "resource": dict(r, id=str(i))}
                                                  for i, r in enumerate(rs)]}
    return Chart(bundle, FMAP, REF_DATE)


class HeartRateRules(unittest.TestCase):
    """Fast AFib (> 110) and very slow rate (< 40) with fainting: numbers in the note or the chart."""

    def test_fast_af_from_note_numbers(self):
        for note in ["New AFib, HR 140 at the visit.", "Atrial fibrillation with rates in the 130s.",
                     "Afib, heart rate of 118.", "New afib, 150 bpm on the monitor."]:
            self.assertIn("palp_new_af_rvr", fired(note), note)
        for note in ["AFib, HR 72 and well controlled.", "Afib, heart rate 110 at rest.", "Afib, HR 1."]:
            self.assertNotIn("palp_new_af_rvr", fired(note), note)

    def test_fast_af_from_chart(self):
        self.assertIn("palp_new_af_rvr", fired("New atrial fibrillation on ECG.", hr_chart(128)))
        self.assertNotIn("palp_new_af_rvr", fired("New atrial fibrillation on ECG.", hr_chart(84)))
        self.assertNotIn("palp_new_af_rvr", fired("New atrial fibrillation on ECG.", hr_chart(128, "2026-04-01")))

    def test_slow_with_fainting(self):
        for note in ["HR 38 and fainted at home.", "Passed out twice, pulse down to 35.", "Syncope, 32 bpm on ECG."]:
            self.assertIn("ecg_very_slow_symptomatic", fired(note), note)
        for note in ["HR 38, no fainting.", "Fainted once, HR 64.", "On rate control for 30 years, fainted once."]:
            self.assertNotIn("ecg_very_slow_symptomatic", fired(note), note)
        self.assertIn("ecg_very_slow_symptomatic", fired("Fainted at home yesterday.", hr_chart(36)))

    def test_slow_with_other_serious_signs_is_emergent(self):
        for note in ["HR 36 and confused this morning.", "Bradycardia to 35 with chest pain.",
                     "Pulse 34, nearly fainted in the shower.", "Heart rate 38 with low blood pressure."]:
            self.assertEqual(floor(note), "emergent", note)

    def test_slow_without_serious_signs_is_urgent(self):
        self.assertEqual(floor("HR 38 on routine ECG, feels fine."), "urgent")
        self.assertEqual(floor("Sinus bradycardia with pauses, more tired and dizzy lately."), "urgent")
        self.assertEqual(floor("Routine physical.", hr_chart(37)), "urgent")
        for note in ["Sinus bradycardia, rate 52, asymptomatic.", "HR 64, feels fine."]:
            self.assertEqual(floor(note), "routine", note)

    def test_sleep_readings_need_more_context(self):
        self.assertEqual(floor("Watch showed HR 38 overnight while asleep, feels fine."), "routine")
        self.assertEqual(floor("Holter: rate down to 36 during sleep. Dizzy during the day."), "urgent")
        self.assertEqual(floor("HR 37 at night, passed out on waking."), "emergent")
        self.assertEqual(floor("HR 38 overnight.", hr_chart(36)), "urgent")  # awake clinic reading still counts
        hints = {h["id"] for h in card_hints(PATHWAY, "abnormal_ecg", "Watch showed HR 38 overnight while asleep.", None)}
        self.assertIn("ecg_slow_during_sleep", hints)
        self.assertEqual([], card_hints(PATHWAY, "abnormal_ecg", "HR 38 on routine ECG.", None))


class ChartRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart = synthetic_chart()

    def ev(self, cond):
        return evaluate(cond, "", self.chart)

    def test_fact_present(self):
        self.assertTrue(self.ev({"fact_present": "hypertension"}))
        self.assertFalse(self.ev({"fact_present": "diabetes"}))
        self.assertFalse(self.ev({"fact_present": "nsaid"}), "inpatient one-off is not a current medicine")

    def test_fact_count(self):
        self.assertTrue(self.ev({"fact_count": {"fact": "bp_meds", "op": ">=", "value": 3}}))
        self.assertFalse(self.ev({"fact_count": {"fact": "bp_meds", "op": ">=", "value": 4}}))

    def test_chart_obs(self):
        self.assertTrue(self.ev({"chart_obs": {"fact": "potassium", "op": "<", "value": 3.5, "within_days": 180}}))
        self.assertFalse(self.ev({"chart_obs": {"fact": "potassium", "op": "<", "value": 3.5, "within_days": 7}}))
        self.assertTrue(self.ev({"chart_obs": {"fact": "tsh", "op": "outside", "range": [0.4, 4.5], "within_days": 365}}))
        self.assertFalse(self.ev({"chart_obs": {"fact": "nt_probnp", "op": "between", "range": [400, 2000]}}),
                         "missing data never fires")

    def test_not(self):
        self.assertTrue(self.ev({"not": {"fact_present": "heart_failure"}}))

    def test_only_if_routing_and_hints(self):
        tests = tests_for(PATHWAY, "hard_to_control_bp_chol", "", self.chart)
        self.assertIn("urine_albumin", tests)
        self.assertIn("aldosterone_renin", tests)
        rules = {r["id"] for r in routing(PATHWAY, "hard_to_control_bp_chol", "", self.chart)}
        self.assertIn("bp_secondary_cause", rules)
        self.assertNotIn("bp_nsaid_only", rules)
        self.assertIn("bp_low_potassium", {h["id"] for h in card_hints(PATHWAY, "hard_to_control_bp_chol", "", self.chart)})
        self.assertIn("palp_abnormal_tsh", {r["id"] for r in routing(PATHWAY, "palpitations_afib", "", self.chart)})


class TrainingNotes(unittest.TestCase):
    """Non-held-out notes: the plain-code floor must never be BELOW the tier the note was written to show.
    Uses the label's urgency once a label is filled in, else the plan's tier."""

    def test_no_under_calls(self):
        with open(os.path.join(ROOT, "cases", "plan.csv")) as fh:
            plan = list(csv.DictReader(fh))
        order = PATHWAY["tier_order"]
        under, over, checked, missing = [], [], 0, []
        for row in plan:
            cid = row["case_id"]
            if row["heldout"] == "True":
                continue
            d = os.path.join(ROOT, "cases", cid)
            if not (os.path.exists(os.path.join(d, "referral.txt")) and os.path.exists(os.path.join(d, "bundle.json"))):
                missing.append(cid)
                continue
            label = _json(os.path.join(d, "label.json"))
            want = label["urgency"] or row["planned_tier"]
            with open(os.path.join(d, "referral.txt")) as fh:
                note = fh.read()
            chart = Chart(_json(os.path.join(d, "bundle.json")), FMAP, _json(os.path.join(d, "meta.json"))["referral_date"])
            got = floor(note, chart)
            checked += 1
            if order.index(got) > order.index(want):
                under.append(f"{cid}: want {want}, floor {got}")
            elif order.index(got) < order.index(want):
                over.append(f"{cid}: want {want}, floor {got}")
        print(f"\n  training notes checked: {checked}, over-called: {len(over)} {over}", end=" ")
        if checked == 0:
            self.skipTest("no cases/*/bundle.json (gitignored) - run build_cases.py; NOTHING WAS CHECKED")
        self.assertEqual([], under)
        # bundle.json is gitignored (rebuilt from Synthea), so a fresh clone or CI has none and would pass
        # having checked nothing. Say so loudly instead of passing silently.
        fix = "regenerate Synthea output, then run: python3 build_cases.py"
        if checked == 0:
            msg = f"No training notes were checked: cases/*/bundle.json missing for all {len(missing)} cases; {fix}"
            print(f"\n\n  Warning: {msg}\n", file=sys.stderr)
            self.skipTest(msg)
        if missing:
            warnings.warn(f"{len(missing)} training notes NOT checked (no referral.txt/bundle.json): "
                          f"{', '.join(missing)}; {fix}")


if __name__ == "__main__":
    unittest.main()
