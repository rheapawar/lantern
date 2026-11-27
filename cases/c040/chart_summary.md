# c040 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2026-11-13** - visit: encounter for symptom (procedure)
- 81 y, female - **HELD OUT** (score only at the end; don't tune on it)
- Hook(s) this case tests: none

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** urgent
- **Question type:** specific_workup_or_management (see the table in NOTE_GUIDE.md)
- **The note must convey:** BP 188/122 on two readings, no symptoms; PCP has adjusted medicines and wants a specialist soon.
- **Include this negation:** denies chest pain or confusion
- **Do NOT mention:** -
- **Style:** econsult_4_fields

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High cholesterol | Hyperlipidemia (disorder) |
| Statin or ezetimibe | Simvastatin 10 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 147 mm[Hg] | 2026-08-04 (3 mo ago) |
| Diastolic blood pressure | 73 mm[Hg] | 2026-08-04 (3 mo ago) |
| Recent heart rate | 69 /min | 2026-08-04 (3 mo ago) |
| Weight trend | 77 kg | 2026-08-04 (3 mo ago) |
| Kidney function (eGFR, creatinine) | 76.43 mL/min | 2026-08-11 (3 mo ago) |
| Potassium | 3.82 mmol/L | 2026-08-11 (3 mo ago) |
| Calcium | 8.78 mg/dL | 2026-08-11 (3 mo ago) |
| Hemoglobin | 16.71 g/dL | 2022-07-12 (4 y ago) |
| LDL / total cholesterol | 135.82 mg/dL | 2026-08-11 (3 mo ago) |
| Hemoglobin A1c | 6.32 % | 2026-08-04 (3 mo ago) |
| Serum albumin | 3.58 g/dL | 2026-08-11 (3 mo ago) |
| Liver tests (ALT, AST) | 11.35 U/L | 2026-08-11 (3 mo ago) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): out of date - last 2026-08-11 (3 mo ago; window 90 d) - stays pre-checked
- Potassium and magnesium: out of date - last 2026-08-11 (3 mo ago; window 90 d) - stays pre-checked
- Calcium: out of date - last 2026-08-11 (3 mo ago; window 90 d) - stays pre-checked
- Glucose: out of date - last 2026-08-11 (3 mo ago; window 90 d) - stays pre-checked
- Hemoglobin A1c: DONE 2026-08-04 (3 mo ago; window 180 d)
- Lipid panel: DONE 2026-08-11 (3 mo ago; window 365 d)
- Complete blood count: out of date - last 2022-07-12 (4 y ago; window 90 d) - stays pre-checked
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

- Past pregnancy history of miscarriage (situation) (since 1965-09-24)
- Recurrent urinary tract infection (disorder) (since 1971-06-11)
- Anemia (disorder) (since 1981-06-02)
- Hyperlipidemia (disorder) (since 2002-03-19)
- Medication review due (situation) (since 2024-07-23)
- Osteoporosis (disorder) (since 2025-03-05)
- Acute viral pharyngitis (disorder) (since 2026-11-13)

## Medicines prescribed in the last 365 days

- Alendronic acid 10 MG Oral Tablet (last 2026-08-04)
- Simvastatin 10 MG Oral Tablet (last 2026-08-11)

## Last 6 encounters

- 2026-11-13 - Encounter for symptom (procedure) (AMB)
- 2026-08-18 - Encounter for check up (procedure) (AMB)
- 2026-08-11 - Follow-up encounter (procedure) (AMB)
- 2026-08-04 - General examination of patient (procedure) (AMB)
- 2025-07-30 - Follow-up encounter (procedure) (AMB)
- 2025-07-29 - General examination of patient (procedure) (AMB)
