# c037 - Hard-to-control blood pressure or cholesterol

- Referral date (chart cut here): **2002-12-23** - visit: general examination of patient (procedure)
- 56 y, male
- Hook(s) this case tests: none

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** routine
- **Question type:** guideline_exception (see the table in NOTE_GUIDE.md)
- **The note must convey:** LDL still above target on current treatment; the risk calculator says lower risk but the patient has several other conditions - do the usual targets apply?
- **Include this negation:** -
- **Do NOT mention:** -
- **Style:** standard

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| Blood pressure medicines (number and classes) | amLODIPine 2.5 MG Oral Tablet; lisinopril 10 MG Oral Tablet |
| On amlodipine or nifedipine (can cause ankle swelling) | amLODIPine 2.5 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 125 mm[Hg] | 2002-12-23 (today) |
| Diastolic blood pressure | 88 mm[Hg] | 2002-12-23 (today) |
| Recent heart rate | 99 /min | 2002-12-23 (today) |
| Weight trend | 98.9 kg | 2002-12-23 (today) |
| Kidney function (eGFR, creatinine) | 101.34 mL/min/{1.73_m2} | 2002-12-23 (today) |
| Potassium | 4.56 mmol/L | 2002-12-23 (today) |
| Calcium | 10.15 mg/dL | 2002-12-23 (today) |
| Hemoglobin | 13.66 g/dL | 2001-12-17 (12 mo ago) |
| LDL / total cholesterol | 192.06 mg/dL | 2002-12-23 (today) |
| Hemoglobin A1c | 5.9 % | 2002-12-23 (today) |

## Tests first for Hard-to-control blood pressure or cholesterol - already done?

- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2002-12-23 (today; window 90 d)
- Potassium and magnesium: DONE 2002-12-23 (today; window 90 d)
- Calcium: DONE 2002-12-23 (today; window 90 d)
- Glucose: DONE 2002-12-23 (today; window 90 d)
- Hemoglobin A1c: DONE 2002-12-23 (today; window 180 d)
- Lipid panel: DONE 2002-12-23 (today; window 365 d)
- Complete blood count: out of date - last 2001-12-17 (12 mo ago; window 90 d) - stays pre-checked
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

- Anemia (disorder) (since 1968-11-18)
- Refugee (person) (since 1977-11-28)
- Essential hypertension (disorder) (since 1986-09-22)
- Metabolic syndrome X (disorder) (since 1986-09-22)

## Medicines prescribed in the last 365 days

- Acetaminophen 325 MG / HYDROcodone Bitartrate 7.5 MG Oral Tablet (last 2002-05-19)
- Acetaminophen 325 MG Oral Tablet (last 2002-05-19)
- amLODIPine 2.5 MG Oral Tablet (last 2002-12-23)
- lisinopril 10 MG Oral Tablet (last 2002-12-23)

## Last 6 encounters

- 2002-12-23 - General examination of patient (procedure) (AMB)
- 2002-07-05 - Encounter for check up (procedure) (AMB)
- 2002-05-27 - Encounter for check up (procedure) (AMB)
- 2002-05-19 - Emergency room admission (procedure) (EMER)
- 2001-12-17 - General examination of patient (procedure) (AMB)
- 2000-12-25 - Encounter for check up (procedure) (AMB)
