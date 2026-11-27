# c034 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2026-09-24** - visit: follow-up encounter (procedure)
- 49 y, male - **HELD OUT** (score only at the end; don't tune on it)
- Hook(s) this case tests: regular_nsaid

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** routine
- **Question type:** specific_workup_or_management (see the table in NOTE_GUIDE.md)
- **The note must convey:** BP creeping up over 6 months (about 155/95) without an obvious cause.
- **Include this negation:** -
- **Do NOT mention:** ibuprofen, naproxen or any NSAID (Lantern must find it in the chart)
- **Style:** terse

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| Diabetes | Diabetes mellitus type 2 (disorder) |
| Blood pressure medicines (number and classes) | Hydrochlorothiazide 25 MG Oral Tablet; lisinopril 10 MG Oral Tablet |
| Regular NSAID (ibuprofen, naproxen) | Ibuprofen 400 MG Oral Tablet [Ibu] |
| On a diuretic (water pill) | Hydrochlorothiazide 25 MG Oral Tablet |
| Medicines that can worsen heart failure | Ibuprofen 400 MG Oral Tablet [Ibu] |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 127 mm[Hg] | 2026-09-24 (today) |
| Diastolic blood pressure | 82 mm[Hg] | 2026-09-24 (today) |
| Recent heart rate | 94 /min | 2026-04-27 (5 mo ago) |
| Weight trend | 96.7 kg | 2026-04-27 (5 mo ago) |
| Kidney function (eGFR, creatinine) | 107.58 mL/min/{1.73_m2} | 2026-04-27 (5 mo ago) |
| Potassium | 4.48 mmol/L | 2026-04-27 (5 mo ago) |
| Calcium | 10.06 mg/dL | 2026-04-27 (5 mo ago) |
| Hemoglobin | 17.26 g/dL | 2022-04-04 (4 y ago) |
| LDL / total cholesterol | 144.02 mg/dL | 2026-04-27 (5 mo ago) |
| Hemoglobin A1c | 7.17 % | 2026-04-27 (5 mo ago) |
| Urine albumin/creatinine ratio | 16.6 mg/g | 2026-04-27 (5 mo ago) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): out of date - last 2026-04-27 (5 mo ago; window 90 d) - stays pre-checked
- Potassium and magnesium: out of date - last 2026-04-27 (5 mo ago; window 90 d) - stays pre-checked
- Calcium: out of date - last 2026-04-27 (5 mo ago; window 90 d) - stays pre-checked
- Glucose: out of date - last 2026-04-27 (5 mo ago; window 90 d) - stays pre-checked
- Hemoglobin A1c: DONE 2026-04-27 (5 mo ago; window 180 d)
- Lipid panel: DONE 2026-04-27 (5 mo ago; window 365 d)
- Complete blood count: out of date - last 2022-04-04 (4 y ago; window 90 d) - stays pre-checked
- Thyroid (TSH): never done
- Urinalysis: never done
- Urine albumin/creatinine ratio: DONE 2026-04-27 (5 mo ago; window 365 d) (only if: {"any": [{"fact_present": "hypertension"}, {"fact_present": "diabetes"}, {"fact_present": "ckd"}]})
- 12-lead ECG: never done
- Home or ambulatory BP monitoring to confirm readings: not recorded in Synthea - never shows as done
- Aldosterone/renin ratio (screen for primary aldosteronism): not recorded in Synthea - never shows as done (only if: {"any": [{"fact_count": {"fact": "bp_meds", "op": ">=", "value": 3}}, {"chart_obs": {"fact": "potassium", "op": "<", "value": 3.5, "within_days": 180}}, {"fact_present": "sleep_apnea"}]})

## Flags you could write into the note

- EMERGENT: BP over 180/120 with signs of organ damage: chest pain, confusion, vision change, severe headache, weakness, breathlessness (hypertensive emergency - ER)
- URGENT: BP over 180/120 without signs of organ damage (severe hypertension - not an ER visit; outpatient medicine adjustment)

## Active problems (disorders; social 'findings' omitted)

- Anemia (disorder) (since 2008-03-10)
- Diabetes mellitus type 2 (disorder) (since 2025-04-21)
- Essential hypertension (disorder) (since 2026-04-27)
- Hypertriglyceridemia (disorder) (since 2026-04-27)
- Metabolic syndrome X (disorder) (since 2026-04-27)

## Medicines prescribed in the last 365 days

- Hydrochlorothiazide 25 MG Oral Tablet (last 2026-04-27)
- Ibuprofen 400 MG Oral Tablet [Ibu] (last 2026-04-27)
- lisinopril 10 MG Oral Tablet (last 2026-04-27)
- tropicamide 5 MG/ML Ophthalmic Solution (last 2026-05-04)

## Last 6 encounters

- 2026-09-24 - Follow-up encounter (procedure) (AMB)
- 2026-07-26 - Follow-up encounter (procedure) (AMB)
- 2026-05-27 - Follow-up encounter (procedure) (AMB)
- 2026-05-04 - Ophthalmic examination and evaluation (procedure) (AMB)
- 2026-04-27 - General examination of patient (procedure) (AMB)
- 2026-01-02 - Encounter for symptom (procedure) (AMB)
