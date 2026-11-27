# c033 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2026-11-08** - visit: follow-up encounter (procedure)
- 77 y, female
- Hook(s) this case tests: kidney_disease

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** routine
- **Question type:** specific_workup_or_management (see the table in NOTE_GUIDE.md)
- **The note must convey:** BP above goal (about 150/95) despite current medicines; asks what to add.
- **Include this negation:** -
- **Do NOT mention:** kidney disease / CKD / eGFR (Lantern must find it in the chart)
- **Style:** standard

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| Diabetes | Disorder of kidney due to diabetes mellitus (disorder) |
| High cholesterol | Hyperlipidemia (disorder) |
| Prior heart attack, coronary disease, stent or bypass | History of coronary artery bypass grafting (situation); Ischemic heart disease (disorder) |
| Chronic kidney disease | Chronic kidney disease stage 1 (disorder) |
| Blood pressure medicines (number and classes) | lisinopril 10 MG Oral Tablet |
| Statin or ezetimibe | Simvastatin 10 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 119 mm[Hg] | 2026-11-07 (1 d ago) |
| Diastolic blood pressure | 81 mm[Hg] | 2026-11-07 (1 d ago) |
| Recent heart rate | 72 /min | 2026-11-07 (1 d ago) |
| Weight trend | 84.2 kg | 2026-11-07 (1 d ago) |
| Kidney function (eGFR, creatinine) | 88.95 mL/min | 2026-11-08 (today) |
| Potassium | 4.59 mmol/L | 2026-11-08 (today) |
| Calcium | 9.17 mg/dL | 2026-11-08 (today) |
| Hemoglobin | 14.54 g/dL | 2026-10-10 (29 d ago) |
| LDL / total cholesterol | 88.73 mg/dL | 2026-11-08 (today) |
| Serum albumin | 4.28 g/dL | 2026-11-08 (today) |
| Liver tests (ALT, AST) | 19.37 U/L | 2026-11-08 (today) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2026-11-08 (today; window 90 d)
- Potassium and magnesium: DONE 2026-11-08 (today; window 90 d)
- Calcium: DONE 2026-11-08 (today; window 90 d)
- Glucose: DONE 2026-11-08 (today; window 90 d)
- Hemoglobin A1c: never done
- Lipid panel: DONE 2026-11-08 (today; window 365 d)
- Complete blood count: DONE 2026-10-10 (29 d ago; window 90 d)
- Thyroid (TSH): never done
- Urinalysis: DONE 2026-11-07 (1 d ago; window 365 d)
- Urine albumin/creatinine ratio: never done (only if: {"any": [{"fact_present": "hypertension"}, {"fact_present": "diabetes"}, {"fact_present": "ckd"}]})
- 12-lead ECG: never done
- Home or ambulatory BP monitoring to confirm readings: not recorded in Synthea - never shows as done
- Aldosterone/renin ratio (screen for primary aldosteronism): not recorded in Synthea - never shows as done (only if: {"any": [{"fact_count": {"fact": "bp_meds", "op": ">=", "value": 3}}, {"chart_obs": {"fact": "potassium", "op": "<", "value": 3.5, "within_days": 180}}, {"fact_present": "sleep_apnea"}]})

## Flags you could write into the note

- EMERGENT: BP over 180/120 with signs of organ damage: chest pain, confusion, vision change, severe headache, weakness, breathlessness (hypertensive emergency - ER)
- URGENT: BP over 180/120 without signs of organ damage (severe hypertension - not an ER visit; outpatient medicine adjustment)

## Active problems (disorders; social 'findings' omitted)

- Past pregnancy history of miscarriage (situation) (since 1982-07-20)
- Osteoarthritis of knee (disorder) (since 1997-05-25)
- Loss of teeth (disorder) (since 1997-07-26)
- Hyperlipidemia (disorder) (since 1999-06-05)
- Essential hypertension (disorder) (since 2004-07-03)
- Ischemic heart disease (disorder) (since 2012-08-18)
- History of coronary artery bypass grafting (situation) (since 2012-09-06)
- Chronic kidney disease stage 1 (disorder) (since 2026-10-10)
- Disorder of kidney due to diabetes mellitus (disorder) (since 2026-10-10)
- Medication review due (situation) (since 2026-11-07)

## Medicines prescribed in the last 365 days

- Simvastatin 10 MG Oral Tablet (last 2026-11-08)
- lisinopril 10 MG Oral Tablet (last 2026-11-07)

## Last 6 encounters

- 2026-11-08 - Follow-up encounter (procedure) (AMB)
- 2026-11-07 - General examination of patient (procedure) (AMB)
- 2026-10-10 - Encounter for check up (procedure) (AMB)
- 2025-11-08 - Follow-up encounter (procedure) (AMB)
- 2025-11-01 - General examination of patient (procedure) (AMB)
- 2024-11-09 - Encounter for check up (procedure) (AMB)
