# c036 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2026-02-13** - visit: general examination of patient (procedure)
- 42 y, male
- Hook(s) this case tests: none

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** emergent
- **Question type:** new_symptom_assessment (see the table in NOTE_GUIDE.md)
- **The note must convey:** BP 210/125 today with new confusion and blurred vision; PCP asks for an urgent cardiology appointment.
- **Include this negation:** -
- **Do NOT mention:** -
- **Style:** econsult_4_fields

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| High cholesterol | Hyperlipidemia (disorder) |
| Blood pressure medicines (number and classes) | Hydrochlorothiazide 25 MG Oral Tablet; amLODIPine 2.5 MG Oral Tablet; lisinopril 10 MG Oral Tablet |
| Statin or ezetimibe | Simvastatin 10 MG Oral Tablet |
| On amlodipine or nifedipine (can cause ankle swelling) | amLODIPine 2.5 MG Oral Tablet |
| On a diuretic (water pill) | Hydrochlorothiazide 25 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 122 mm[Hg] | 2026-02-13 (today) |
| Diastolic blood pressure | 84 mm[Hg] | 2026-02-13 (today) |
| Recent heart rate | 69 /min | 2026-02-13 (today) |
| Weight trend | 91.8 kg | 2026-02-13 (today) |
| Kidney function (eGFR, creatinine) | 143.72 mL/min/{1.73_m2} | 2026-02-13 (today) |
| Potassium | 5.14 mmol/L | 2025-11-22 (2 mo ago) |
| Calcium | 8.6 mg/dL | 2025-11-22 (2 mo ago) |
| Hemoglobin | 13.31 g/dL | 2024-02-02 (2 y ago) |
| LDL / total cholesterol | 96.28 mg/dL | 2025-11-22 (2 mo ago) |
| Serum albumin | 4.97 g/dL | 2025-11-22 (2 mo ago) |
| Liver tests (ALT, AST) | 22.14 U/L | 2025-11-22 (2 mo ago) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2026-02-13 (today; window 90 d)
- Potassium and magnesium: DONE 2025-11-22 (2 mo ago; window 90 d)
- Calcium: DONE 2025-11-22 (2 mo ago; window 90 d)
- Glucose: DONE 2025-11-22 (2 mo ago; window 90 d)
- Hemoglobin A1c: never done
- Lipid panel: DONE 2025-11-22 (2 mo ago; window 365 d)
- Complete blood count: out of date - last 2024-02-02 (2 y ago; window 90 d) - stays pre-checked
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

- Essential hypertension (disorder) (since 2024-02-02)
- Hyperlipidemia (disorder) (since 2024-11-01)
- Medication review due (situation) (since 2026-02-13)

## Medicines prescribed in the last 365 days

- Hydrochlorothiazide 25 MG Oral Tablet (last 2026-02-13)
- Simvastatin 10 MG Oral Tablet (last 2025-11-22)
- amLODIPine 2.5 MG Oral Tablet (last 2026-02-13)
- lisinopril 10 MG Oral Tablet (last 2026-02-13)

## Last 6 encounters

- 2026-02-13 - General examination of patient (procedure) (AMB)
- 2025-11-22 - Follow-up encounter (procedure) (AMB)
- 2025-02-21 - Encounter for check up (procedure) (AMB)
- 2025-02-07 - General examination of patient (procedure) (AMB)
- 2024-11-22 - Follow-up encounter (procedure) (AMB)
- 2024-11-08 - Encounter for check up (procedure) (AMB)
