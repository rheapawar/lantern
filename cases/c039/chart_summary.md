# c039 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2026-03-04** - visit: encounter for check up (procedure)
- 60 y, female
- Hook(s) this case tests: none

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** routine
- **Question type:** test_interpretation (see the table in NOTE_GUIDE.md)
- **The note must convey:** BP high in clinic but normal at home; asks if this is white-coat hypertension.
- **Include this negation:** -
- **Do NOT mention:** -
- **Style:** rambling

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High cholesterol | Hyperlipidemia (disorder) |
| Statin or ezetimibe | Simvastatin 10 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 121 mm[Hg] | 2026-02-18 (14 d ago) |
| Diastolic blood pressure | 90 mm[Hg] | 2026-02-18 (14 d ago) |
| Recent heart rate | 90 /min | 2026-02-18 (14 d ago) |
| Weight trend | 92 kg | 2026-02-18 (14 d ago) |
| Kidney function (eGFR, creatinine) | 66.97 mL/min | 2026-02-25 (7 d ago) |
| Potassium | 4.9 mmol/L | 2026-02-25 (7 d ago) |
| Calcium | 10.02 mg/dL | 2026-02-25 (7 d ago) |
| Hemoglobin | 14.46 g/dL | 2022-01-26 (4 y ago) |
| LDL / total cholesterol | 114.29 mg/dL | 2026-02-25 (7 d ago) |
| Serum albumin | 3.72 g/dL | 2026-02-25 (7 d ago) |
| Liver tests (ALT, AST) | 12.51 U/L | 2026-02-25 (7 d ago) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2026-02-25 (7 d ago; window 90 d)
- Potassium and magnesium: DONE 2026-02-25 (7 d ago; window 90 d)
- Calcium: DONE 2026-02-25 (7 d ago; window 90 d)
- Glucose: DONE 2026-02-25 (7 d ago; window 90 d)
- Hemoglobin A1c: never done
- Lipid panel: DONE 2026-02-25 (7 d ago; window 365 d)
- Complete blood count: out of date - last 2022-01-26 (4 y ago; window 90 d) - stays pre-checked
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

- Past pregnancy history of miscarriage (situation) (since 1986-10-04)
- Malignant neoplasm of breast (disorder) (since 2009-06-17)
- Hyperlipidemia (disorder) (since 2009-12-02)
- Polyp of colon (disorder) (since 2025-11-17)

## Medicines prescribed in the last 365 days

- Simvastatin 10 MG Oral Tablet (last 2026-02-25)
- tramadol hydrochloride 50 MG Oral Tablet (last 2026-02-18)

## Last 6 encounters

- 2026-03-04 - Encounter for check up (procedure) (AMB)
- 2026-02-25 - Follow-up encounter (procedure) (AMB)
- 2026-02-18 - General examination of patient (procedure) (AMB)
- 2025-12-24 - Screening surveillance (regime/therapy) (AMB)
- 2025-12-24 - Postoperative follow-up visit (procedure) (AMB)
- 2025-12-24 - Follow-up visit (procedure) (AMB)
