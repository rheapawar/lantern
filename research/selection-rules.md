# select_charts.py RULES, CLAUDE.md hooks, and scorecard targets

NO SOURCE FOUND means "no guideline source found in the checked material", not "wrong". "verified" = checked against full text (NICE NG106; full 2025 AHA/ACC BP guideline, Circulation 2025;152:e114-e218).

## select_charts.py RULES

| Rule | Verdict | Notes |
|---|---|---|
| TSH_NORMAL (0.4, 4.5) | NO SOURCE FOUND | Lab-defined reference range; use the FHIR Observation's own range if present. |
| POTASSIUM_LOW 3.5 | NO SOURCE FOUND | Lab convention. (BP guideline 3.2.3.1: hypokalemia is a PA screening trigger - verified.) |
| EGFR_LOW 60 (CKD) | NO SOURCE FOUND | KDIGO not checked; CKD needs persistence >3 months. NICE NG106 1.6.2 uses eGFR <30 for renal liaison (verified). |
| MED_ACTIVE_DAYS 365 | NO SOURCE FOUND | Engineering heuristic. |
| Fit: chest pain age >=45 + risk factor | NO SOURCE FOUND | 2021 chest pain guideline uses pretest probability from age, sex, symptoms; no 45 cutoff found. Project memory prefers facts as context, not hard cutoffs. |
| Fit: HF age >=60 + HTN/CAD/valve/diabetes | NO SOURCE FOUND | Same. |
| Fit: HTN on 2+ BP meds / hyperlipidemia on statin | PARTLY SUPPORTED | Resistant HTN = 3 meds incl. diuretic or >=4 (5.6, verified); 2+ is looser. |
| Condition match "hypertension" | code observation | Also matches "pulmonary hypertension", "ocular hypertension". |
| NSAID list ibuprofen, naproxen only | PARTLY SUPPORTED | Table 11 (verified) lists many more BP-raising substances incl. caffeine, decongestants, SNRIs/TCAs/MAOIs, corticosteroids, OCPs, licorice. |

## CLAUDE.md hooks

| Hook | Verdict | Notes |
|---|---|---|
| Amlodipine causes ankle swelling | CONFIRMED (verified against full text) | 2025 BP Table 13: dihydropyridine CCB dose-related lower extremity edema, more common in women; Table 17: combining with RAS inhibitor reduces it. (Previously NO SOURCE FOUND.) |
| Kidney disease matters for contrast tests | NO SOURCE FOUND | Not stated in the checked chest-pain summary. |
| Abnormal TSH -> check thyroid first (palpitations) | NO SOURCE FOUND (AF); PARTLY SUPPORTED (BP, HF) | TSH in BP Table 6 (3.1.2) and NG106 1.2.12 (verified). AF guideline wording not yet checked. |
| Known AFib, no blood thinner -> stroke-risk decision | CONFIRMED | 2023 AF Ten Points. |
| Low potassium + abnormal ECG | PARTLY SUPPORTED | TdP risk factor (2010 statement; secondary summary only). |
| NSAIDs and hard-to-control BP | CONFIRMED (verified against full text) | Table 11. |
| Prior MI/CAD -> chest pain urgency up | PARTLY SUPPORTED | Pathway changes when CAD known (Pt 10); no tier rule. |

## CLAUDE.md pathway table
Same verdicts as per-topic files. ">=180/120" should be ">180/120" (6.2, verified); "Cut caffeine" has no AF-guideline source (alcohol does) though caffeine is a BP-interfering substance (Table 11); HF "fast weight gain" no source; "new/worsening exertional chest pain = urgent" is judgment. `tiers.urgent` "matches NICE 2-week" only for NT-proBNP >2000.

## Scorecard targets
NO SOURCE FOUND for an external benchmark for referral-triage under/over-triage rates or recall metrics; not searched exhaustively. Treat as product targets.
