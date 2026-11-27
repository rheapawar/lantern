# c035 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2026-04-03** - visit: encounter for check up (procedure)
- 48 y, female
- Hook(s) this case tests: none

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** urgent
- **Question type:** specific_workup_or_management (see the table in NOTE_GUIDE.md)
- **The note must convey:** BP 186/124 in clinic and similar at home, with no headache, chest pain or vision change.
- **Include this negation:** no headache, no chest pain, no vision change
- **Do NOT mention:** -
- **Style:** rambling

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| Blood pressure medicines (number and classes) | Hydrochlorothiazide 25 MG Oral Tablet; lisinopril 10 MG Oral Tablet |
| On a diuretic (water pill) | Hydrochlorothiazide 25 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 124 mm[Hg] | 2026-03-20 (14 d ago) |
| Diastolic blood pressure | 100 mm[Hg] | 2026-03-20 (14 d ago) |
| Recent heart rate | 95 /min | 2026-03-20 (14 d ago) |
| Weight trend | 77.5 kg | 2026-03-20 (14 d ago) |
| Kidney function (eGFR, creatinine) | 69.96 mL/min/{1.73_m2} | 2026-03-20 (14 d ago) |
| Hemoglobin | 12.39 g/dL | 2026-03-20 (14 d ago) |
| LDL / total cholesterol | 144.22 mg/dL | 2024-03-08 (2 y ago) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2026-03-20 (14 d ago; window 90 d)
- Potassium and magnesium: never done
- Calcium: never done
- Glucose: never done
- Hemoglobin A1c: never done
- Lipid panel: out of date - last 2024-03-08 (2 y ago; window 365 d) - stays pre-checked
- Complete blood count: DONE 2026-03-20 (14 d ago; window 90 d)
- Thyroid (TSH): never done
- Urinalysis: never done
- Urine albumin/creatinine ratio: never done (only if: {"any": [{"fact_present": "hypertension"}, {"fact_present": "diabetes"}, {"fact_present": "ckd"}]})
- 12-lead ECG: never done
- Home or ambulatory BP monitoring to confirm readings: not recorded in Synthea - never shows as done
- Aldosterone/renin ratio (screen for primary aldosteronism): not recorded in Synthea - never shows as done (only if: {"any": [{"fact_count": {"fact": "bp_meds", "op": ">=", "value": 3}}, {"chart_obs": {"fact": "potassium", "op": "<", "value": 3.5, "within_days": 180}}, {"fact_present": "sleep_apnea"}]})

## Flags you could write into the note

- EMERGENT: BP over 180/120 with signs of organ damage: chest pain, confusion, vision change, severe headache, weakness, breathlessness (hypertensive emergency - ER)
- URGENT: BP over 180/120 without signs of organ damage (severe hypertension - not an ER visit; outpatient medicine adjustment)

## Active problems (disorders; social 'findings' omitted)

- Loss of teeth (disorder) (since 2002-12-27)
- Essential hypertension (disorder) (since 2008-12-12)
- Past pregnancy history of miscarriage (situation) (since 2021-03-09)
- Medication review due (situation) (since 2023-03-03)

## Medicines prescribed in the last 365 days

- 1 ML medroxyprogesterone acetate 150 MG/ML Injection (last 2025-10-22)
- Acetaminophen 325 MG / Oxycodone Hydrochloride 10 MG Oral Tablet [Percocet] (last 2026-03-20)
- Acetaminophen 325 MG Oral Tablet [Tylenol] (last 2026-03-20)
- Hydrochlorothiazide 25 MG Oral Tablet (last 2026-03-20)
- lisinopril 10 MG Oral Tablet (last 2026-03-20)
- sodium fluoride 0.0272 MG/MG Oral Gel (last 2026-04-03)

## Last 6 encounters

- 2026-04-03 - Encounter for check up (procedure) (AMB)
- 2026-03-20 - General examination of patient (procedure) (AMB)
- 2025-10-22 - Consultation for treatment (procedure) (AMB)
- 2025-03-14 - General examination of patient (procedure) (AMB)
- 2024-10-10 - Encounter for symptom (procedure) (AMB)
- 2024-03-22 - Encounter for check up (procedure) (AMB)
