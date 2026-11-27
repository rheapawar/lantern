# c038 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2025-12-20** - visit: follow-up encounter (procedure)
- 76 y, male
- Hook(s) this case tests: none

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** routine
- **Question type:** guideline_exception (see the table in NOTE_GUIDE.md)
- **The note must convey:** Cholesterol above goal; patient reluctant to take statins and has several other conditions; PCP unsure the standard guideline fits.
- **Include this negation:** -
- **Do NOT mention:** -
- **Style:** terse

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High cholesterol | Hyperlipidemia (disorder) |
| Prior heart attack, coronary disease, stent or bypass | History of coronary artery bypass grafting (situation); Ischemic heart disease (disorder) |
| Statin or ezetimibe | Simvastatin 10 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 137 mm[Hg] | 2025-11-29 (21 d ago) |
| Diastolic blood pressure | 72 mm[Hg] | 2025-11-29 (21 d ago) |
| Recent heart rate | 64 /min | 2025-11-29 (21 d ago) |
| Weight trend | 87.4 kg | 2025-11-29 (21 d ago) |
| Kidney function (eGFR, creatinine) | 67.79 mL/min | 2025-11-29 (21 d ago) |
| Potassium | 3.99 mmol/L | 2025-11-29 (21 d ago) |
| Calcium | 9.71 mg/dL | 2025-11-29 (21 d ago) |
| Hemoglobin | 15.48 g/dL | 2021-11-06 (4 y ago) |
| LDL / total cholesterol | 124.42 mg/dL | 2025-11-29 (21 d ago) |
| Hemoglobin A1c | 6.01 % | 2025-11-29 (21 d ago) |
| Serum albumin | 4.49 g/dL | 2025-11-29 (21 d ago) |
| Liver tests (ALT, AST) | 18.31 U/L | 2025-11-29 (21 d ago) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2025-11-29 (21 d ago; window 90 d)
- Potassium and magnesium: DONE 2025-11-29 (21 d ago; window 90 d)
- Calcium: DONE 2025-11-29 (21 d ago; window 90 d)
- Glucose: DONE 2025-11-29 (21 d ago; window 90 d)
- Hemoglobin A1c: DONE 2025-11-29 (21 d ago; window 180 d)
- Lipid panel: DONE 2025-11-29 (21 d ago; window 365 d)
- Complete blood count: out of date - last 2021-11-06 (4 y ago; window 90 d) - stays pre-checked
- Thyroid (TSH): never done
- Urinalysis: out of date - last 2017-12-23 (7 y ago; window 365 d) - stays pre-checked
- Urine albumin/creatinine ratio: never done (only if: {"any": [{"fact_present": "hypertension"}, {"fact_present": "diabetes"}, {"fact_present": "ckd"}]})
- 12-lead ECG: never done
- Home or ambulatory BP monitoring to confirm readings: not recorded in Synthea - never shows as done
- Aldosterone/renin ratio (screen for primary aldosteronism): not recorded in Synthea - never shows as done (only if: {"any": [{"fact_count": {"fact": "bp_meds", "op": ">=", "value": 3}}, {"chart_obs": {"fact": "potassium", "op": "<", "value": 3.5, "within_days": 180}}, {"fact_present": "sleep_apnea"}]})

## Flags you could write into the note

- EMERGENT: BP over 180/120 with signs of organ damage: chest pain, confusion, vision change, severe headache, weakness, breathlessness (hypertensive emergency - ER)
- URGENT: BP over 180/120 without signs of organ damage (severe hypertension - not an ER visit; outpatient medicine adjustment)

## Active problems (disorders; social 'findings' omitted)

- Anemia (disorder) (since 1993-07-17)
- Ischemic heart disease (disorder) (since 2006-08-12)
- History of coronary artery bypass grafting (situation) (since 2006-08-26)
- Alzheimer's disease (disorder) (since 2021-11-06)
- Hyperlipidemia (disorder) (since 2025-11-29)
- Medication review due (situation) (since 2025-11-29)

## Medicines prescribed in the last 365 days

- Simvastatin 10 MG Oral Tablet (last 2025-12-20)

## Last 6 encounters

- 2025-12-20 - Follow-up encounter (procedure) (AMB)
- 2025-12-13 - Encounter for check up (procedure) (AMB)
- 2025-11-29 - General examination of patient (procedure) (AMB)
- 2025-10-25 - Follow-up consultation (procedure) (AMB)
- 2024-11-23 - General examination of patient (procedure) (AMB)
- 2024-07-06 - Admission to hospice (procedure) (HH)
