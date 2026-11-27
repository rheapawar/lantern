# c008 - Chest pain

- Referral date (chart cut here): **2026-05-28** - visit: follow-up encounter (procedure)
- 55 y, male
- Hook(s) this case tests: kidney_disease

## Writing plan (from cases/plan.csv - see cases/NOTE_GUIDE.md)

- **Tier the note should show:** routine
- **Question type:** concerns_despite_normal_tests (see the table in NOTE_GUIDE.md)
- **The note must convey:** Chest discomfort after meals with some heartburn; ECG in clinic was normal, but the patient is still worried it is the heart.
- **Include this negation:** -
- **Do NOT mention:** kidney disease / CKD / eGFR (Lantern must find it in the chart)
- **Style:** econsult_4_fields

## Chart facts Lantern will look for

| Fact | Found |
|---|---|
| High blood pressure | Essential hypertension (disorder) |
| Diabetes | Disorder of kidney due to diabetes mellitus (disorder) |
| Chronic kidney disease | Chronic kidney disease stage 1 (disorder) |
| Blood pressure medicines (number and classes) | amLODIPine 2.5 MG Oral Tablet; losartan potassium 25 MG Oral Tablet |
| On amlodipine or nifedipine (can cause ankle swelling) | amLODIPine 2.5 MG Oral Tablet |

## Latest vitals and labs

| Item | Value | Date |
|---|---|---|
| Systolic blood pressure | 128 mm[Hg] | 2026-04-22 (36 d ago) |
| Diastolic blood pressure | 95 mm[Hg] | 2026-04-22 (36 d ago) |
| Recent heart rate | 65 /min | 2026-04-22 (36 d ago) |
| Weight trend | 84.5 kg | 2026-04-22 (36 d ago) |
| Kidney function (eGFR, creatinine) | 61.18 mL/min/{1.73_m2} | 2026-04-22 (36 d ago) |
| Potassium | 4.91 mmol/L | 2026-04-22 (36 d ago) |
| Calcium | 8.83 mg/dL | 2026-04-22 (36 d ago) |
| Hemoglobin | 15.29 g/dL | 2026-04-22 (36 d ago) |
| LDL / total cholesterol | 204.65 mg/dL | 2025-04-16 (13 mo ago) |

## Tests first for Chest pain - already done?

- 12-lead ECG: never done
- Lipid panel: out of date - last 2025-04-16 (13 mo ago; window 365 d) - stays pre-checked
- Hemoglobin A1c: never done
- Kidney panel (creatinine, eGFR, BUN, sodium): DONE 2026-04-22 (36 d ago; window 90 d)
- Stress test (type chosen by cardiology): never done
- Coronary CT angiography (CCTA): not recorded in Synthea - never shows as done

## Flags you could write into the note

- EMERGENT: Chest pain at rest or ongoing (possible heart attack - ER by ambulance, don't wait for office tests)
- EMERGENT: Chest pain with sweating, fainting or breathlessness
- EMERGENT: Recent chest pain with new ischemic ECG changes
- EMERGENT: Sudden tearing pain to the back, or sudden breathlessness / coughing blood (aortic dissection or blood clot in lung)
- URGENT: New or worsening chest pain with exertion

## Active problems (disorders; social 'findings' omitted)

- Essential hypertension (disorder) (since 2015-02-18)
- Chronic kidney disease stage 1 (disorder) (since 2021-03-24)
- Disorder of kidney due to diabetes mellitus (disorder) (since 2021-03-24)
- Medication review due (situation) (since 2024-05-15)
- Chronic sinusitis (disorder) (since 2024-06-01)
- History of appendectomy (situation) (since 2024-08-06)
- Loss of teeth (disorder) (since 2026-05-13)

## Medicines prescribed in the last 365 days

- Acetaminophen 325 MG / Oxycodone Hydrochloride 10 MG Oral Tablet [Percocet] (last 2026-04-22)
- Acetaminophen 325 MG Oral Tablet [Tylenol] (last 2026-04-22)
- amLODIPine 2.5 MG Oral Tablet (last 2026-04-22)
- losartan potassium 25 MG Oral Tablet (last 2026-04-22)
- sodium fluoride 0.0272 MG/MG Oral Gel (last 2026-05-07)

## Last 6 encounters

- 2026-05-28 - Follow-up encounter (procedure) (AMB)
- 2026-05-13 - Encounter for problem (procedure) (AMB)
- 2026-05-06 - Encounter for check up (procedure) (AMB)
- 2026-04-22 - General examination of patient (procedure) (AMB)
- 2025-04-30 - Encounter for check up (procedure) (AMB)
- 2025-04-16 - General examination of patient (procedure) (AMB)
