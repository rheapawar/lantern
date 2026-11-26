# select_charts.py RULES, CLAUDE.md hooks, and scorecard targets

"Full text" = NICE NG106 and the 2025 AHA/ACC BP guideline (see README). NO SOURCE FOUND = no guideline or reference source found in the checked material.

## select_charts.py RULES

| Rule | Verdict | Notes |
|---|---|---|
| TSH_NORMAL (0.4, 4.5) | PARTLY SUPPORTED | American Thyroid Association, "Determination of optimal TSH ranges for reflex Free T4 testing", Clinical Thyroidology for the Public, Feb 2018 - https://www.thyroid.org/patient-thyroid-information/ct-for-patients/february-2018/vol-11-issue-2-p-3-4/ : laboratories vary, most reporting a lower limit of about 0.4-0.5 and an upper limit of about 4-5.5 mU/L; 0.4-4 mU/L used in that study. 0.4-4.5 falls within typical lab ranges; the reporting lab's own range is preferable. |
| POTASSIUM_LOW 3.5 | NO SOURCE FOUND | MedlinePlus potassium blood test page defines hypokalemia but gives no numeric range - https://medlineplus.gov/lab-tests/potassium-blood-test/ . 2025 BP guideline 3.2.3.1: hypokalemia is a PA screening trigger (full text), no cut-off. |
| EGFR_LOW 60 (CKD) | CONFIRMED (with caveat) | KDIGO 2024 CKD guideline (Kidney Int 2024;105(4S):S117-S314), via 2 Minute Medicine summary https://www.2minutemedicine.com/guidelines/kdigo-ckd-staging/ : CKD = abnormal kidney structure or function >3 months; eGFR <60 mL/min/1.73 m2, or markers of damage such as UACR >=30 mg/g. A single eGFR <60 is not CKD (needs persistence). NICE NG106 1.6.2 uses eGFR <30 for renal liaison (full text). KDIGO primary text not yet checked. |
| MED_ACTIVE_DAYS 365 | NO SOURCE FOUND | Engineering heuristic. |
| Fit: chest pain age >=45 + risk factor | NO SOURCE FOUND | 2021 chest pain guideline uses pretest probability from age, sex, symptoms (Ten Points Pt 10); no age cutoff of 45 found. Project memory prefers facts as context, not hard cutoffs. |
| Fit: HF age >=60 + HTN/CAD/valve/diabetes | NO SOURCE FOUND | Same. |
| Fit: HTN on 2+ BP meds / hyperlipidemia on statin | PARTLY SUPPORTED | Resistant HTN = 3 meds incl. diuretic or >=4 (5.6, full text); 2+ is looser. |
| Condition match "hypertension" | code observation | Also matches "pulmonary hypertension", "ocular hypertension". |
| NSAID list ibuprofen, naproxen only | PARTLY SUPPORTED | 2025 BP Table 11 lists many more BP-raising substances. |

## CLAUDE.md hooks

| Hook | Verdict | Notes |
|---|---|---|
| Amlodipine causes ankle swelling | CONFIRMED (full text) | 2025 BP Table 13 (dose-related lower extremity edema, more common in women); Table 17. |
| Kidney disease matters for contrast tests | PARTLY SUPPORTED | ACC 2025 contrast-media article: contrast kidney-injury risk uncertain at eGFR <30, "relative contraindication"; 2021 chest pain guideline's own wording not yet checked (see chest-pain.md). |
| Abnormal TSH -> check thyroid first (palpitations) | NO SOURCE FOUND (AF); PARTLY SUPPORTED (BP, HF) | TSH in BP Table 6 (3.1.2) and NG106 1.2.12 (full text). |
| Known AFib, no blood thinner -> stroke-risk decision | CONFIRMED | 2023 AF Ten Points (anticoagulation by annual stroke risk). |
| Low potassium + abnormal ECG | PARTLY SUPPORTED | Hypokalemia is a TdP risk factor (2010 statement summary). |
| NSAIDs and hard-to-control BP | CONFIRMED (full text) | 2025 BP Table 11. |
| Prior MI/CAD -> chest pain urgency up | PARTLY SUPPORTED | Testing pathway changes when CAD known (Pt 10); no tier rule. Prior MI and old ECG changes: NO SOURCE FOUND. |

## CLAUDE.md pathway table
Same verdicts as per-topic files. ">=180/120" should be ">180/120" (6.2); "Cut caffeine" has no AF-guideline source (alcohol does), though caffeine is a BP-interfering substance (Table 11); HF "fast weight gain" no source; "new/worsening exertional chest pain = urgent" is judgment. `tiers.urgent` "matches NICE 2-week" only for NT-proBNP >2000.

## Scorecard targets
NO SOURCE FOUND for an external benchmark for referral-triage under/over-triage rates or recall metrics (search not exhaustive). Treat as product targets.
