# c003 - Chest pain

- Referral date (chart cut here): **2023-10-29** - visit: encounter for check up (procedure)
- 53 y, female - **HELD OUT** (score only at the end; don't tune on it)
- Hook(s) this case tests: kidney_disease

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** emergent
- **Question type:** new_symptom_assessment (see the table in NOTE_GUIDE.md)
- **The note must convey:** Chest pressure that started at rest this morning and is still there, with sweating; PCP is asking for 'a quick cardiology look' (under-calls it).
- **Include this negation:** -
- **Do NOT mention:** kidney disease / CKD / eGFR (Lantern must find it in the chart)
- **Style:** rambling

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| Diabetes | Diabetes mellitus type 2 (disorder); Disorder of kidney due to diabetes mellitus (disorder); Neuropathy due to type 2 diabetes mellitus (disorder) |
| Chronic kidney disease | Chronic kidney disease stage 1 (disorder) |
| Blood pressure medicines (number and classes) | Hydrochlorothiazide 25 MG Oral Tablet; amLODIPine 2.5 MG Oral Tablet; lisinopril 10 MG Oral Tablet |
| On amlodipine or nifedipine (can cause ankle swelling) | amLODIPine 2.5 MG Oral Tablet |
| On a diuretic (water pill) | Hydrochlorothiazide 25 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 99 mm[Hg] | 2023-10-15 (14 d ago) |
| Diastolic blood pressure | 63 mm[Hg] | 2023-10-15 (14 d ago) |
| Recent heart rate | 85 /min | 2023-10-15 (14 d ago) |
| Weight trend | 64.7 kg | 2023-10-15 (14 d ago) |
| Kidney function (eGFR, creatinine) | 81.61 mL/min/{1.73_m2} | 2023-10-15 (14 d ago) |
| Potassium | 4.71 mmol/L | 2023-10-15 (14 d ago) |
| Calcium | 9.59 mg/dL | 2023-10-15 (14 d ago) |
| Hemoglobin | 16.87 g/dL | 2021-06-20 (2 y ago) |
| LDL / total cholesterol | 134.61 mg/dL | 2023-10-15 (14 d ago) |
| Hemoglobin A1c | 3.95 % | 2023-10-15 (14 d ago) |
| Urine albumin/creatinine ratio | 14.35 mg/g | 2023-10-15 (14 d ago) |

## Tests first for Chest pain - already done?

- 12-lead ECG: never done
- Lipid panel: DONE 2023-10-15 (14 d ago; window 365 d)
- Hemoglobin A1c: DONE 2023-10-15 (14 d ago; window 180 d)
- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2023-10-15 (14 d ago; window 90 d)
- Stress test (type chosen by cardiology): never done
- Coronary CT angiography (CCTA): not recorded in Synthea - never shows as done

## Flags you could write into the note

- EMERGENT: Chest pain at rest or ongoing (possible heart attack - ER by ambulance, don't wait for office tests)
- EMERGENT: Chest pain with sweating, fainting or breathlessness
- EMERGENT: Recent chest pain with new ischemic ECG changes
- EMERGENT: Sudden tearing pain to the back, or sudden breathlessness / coughing blood (aortic dissection or blood clot in lung)
- URGENT: New or worsening chest pain with exertion

## Active problems (disorders; social 'findings' omitted)

- Anemia (disorder) (since 1989-07-09)
- History of tubal ligation (situation) (since 1995-08-16)
- Diabetes mellitus type 2 (disorder) (since 2016-05-29)
- Essential hypertension (disorder) (since 2018-06-03)
- Hypertriglyceridemia (disorder) (since 2018-06-03)
- Metabolic syndrome X (disorder) (since 2018-06-03)
- Neuropathy due to type 2 diabetes mellitus (disorder) (since 2021-06-20)
- Chronic kidney disease stage 1 (disorder) (since 2023-05-21)
- Disorder of kidney due to diabetes mellitus (disorder) (since 2023-05-21)

## Medicines prescribed in the last 365 days

- Hydrochlorothiazide 25 MG Oral Tablet (last 2023-10-15)
- amLODIPine 2.5 MG Oral Tablet (last 2023-10-15)
- insulin isophane, human 70 UNT/ML / insulin, regular, human 30 UNT/ML Injectable Suspension [Humulin] (last 2023-10-15)
- lisinopril 10 MG Oral Tablet (last 2023-10-15)
- sodium fluoride 0.0272 MG/MG Oral Gel (last 2023-10-29)
- tropicamide 5 MG/ML Ophthalmic Solution (last 2022-12-22)

## Last 6 encounters

- 2023-10-29 - Encounter for check up (procedure) (AMB)
- 2023-10-15 - Encounter for check up (procedure) (AMB)
- 2023-08-27 - Encounter for check up (procedure) (AMB)
- 2023-08-13 - Urgent care clinic (environment) (AMB)
- 2023-07-16 - Encounter for check up (procedure) (AMB)
- 2023-07-02 - General examination of patient (procedure) (AMB)
