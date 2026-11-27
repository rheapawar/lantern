# Heart failure symptoms - fact-check (NICE NG106 + QS9, UK; 2022 AHA/ACC/HFSA, US)

## Checked against
- NICE NG106, Chronic heart failure in adults: diagnosis and management (UK), recommendations 1.1-1.12 and Terms used, last updated 3 Sep 2025 - FULL TEXT. Catalog label "(2018)" should read "updated 3 Sep 2025".
- NICE QS9, Chronic heart failure in adults - quality standard: not yet checked (its cited NG106 rec numbers should be compared; NG106 itself has 1.2.3 = >2000, 1.2.4 = 400-2000).
- 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure (US; Circulation 2022;145:e895-e1032; PMID 35363499; DOI 10.1161/CIR.0000000000001063) - FULL TEXT (sections 1-14, Tables 1-33, Appendix 3).
- 2025 AHA/ACC High Blood Pressure guideline (Circulation 2025;152:e114-e218) - FULL TEXT (Tables 13, 17; 5.1; 5.3.4.1; scope 1.4 excludes BP management in HF).
- FDA Drug Safety Communication on NSAIDs, 9 Jul 2015, as reproduced by the American Society of Anesthesiologists - https://asahq.org/advocacy-and-asapac/fda-and-washington-alerts/fda-alerts/2015/07/nsaids-fda-strengthens-warning-of-increased-chance-of-heart-attack-or-stroke
- Takeda, "Takeda Revises ACTOS (pioglitazone HCl) Prescribing Label", 6 Jun 2007 - https://takeda.com/en-us/newsroom/news-releases/2007/takeda-revises-actos-pioglitazone-hcl-prescribing-label
- ACC, "Iron Deficiency and Treatment for Cardiovascular Disease: Key Points", 2022 (summary of an EHJ review, not the guideline) - https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2022/11/30/17/14/iron-deficiency-and-cvd
- AHA scientific statement "Drugs That May Cause or Exacerbate Heart Failure" (Page et al., Circulation 2016;134:e32; DOI 10.1161/CIR.0000000000000426): not checked directly; its key rows are reproduced in HF 2022 Table 13.
- Still current: no 2026 AHA/ACC HF guideline identified; ESC 2026 HF guideline and ESC 2023 focused update not yet checked.

## Verdicts

| id | Verdict | Ref / notes |
|---|---|---|
| hf_ntprobnp_over_2000 (urgent) | CONFIRMED | NICE NG106 1.2.3: >2,000 ng/L -> specialist + echo within 2 weeks. UK; no US equivalent time-frame found. "2 weeks = urgent" is Lantern's mapping. |
| hf_ntprobnp_400_2000 (soon hint) | CONFIRMED | NG106 1.2.4: within 6 weeks. ng/L = pg/mL. |
| "below 400 makes HF less likely (untreated)" | CONFIRMED | NG106 1.2.5, 1.2.6. |
| review_note prior-MI fast track | CONFIRMED not kept | Absent from current NG106 (was in CG108). |
| "NT-proBNP pushed UP by age >70, AFib, eGFR<60, lung disease, diabetes" | CONTRADICTED vs NICE / PARTLY SUPPORTED (US) | NG106 1.2.7 lists pulmonary, renal, liver, systemic pathologies, sepsis, COPD, diabetes, cirrhosis; not age or AF; no eGFR cut-off. HF 2022 Table 6 lists advancing age, AF, anemia, renal failure, pulmonary disease, sepsis, critical illness (no numeric cut-offs). Pathway follows NICE; US list added as a note. |
| "NT-proBNP pushed DOWN by obesity (BMI>35), drugs" | PARTLY SUPPORTED | 1.2.7: obesity, African/African-Caribbean family background, diuretics, ACEi/ARNI/ARB, beta-blockers, MRAs. "BMI >35" not in NICE; ARNI and ancestry missing. |
| tests_first ecg, cxr, renal, tsh, liver, lipids, a1c, cbc, urinalysis | CONFIRMED | NG106 1.2.12 (non-ECG items "consider"; peak flow/spirometry not in pathway). |
| tests_first nt_probnp, echo | CONFIRMED | 1.2.2-1.2.4. |
| tests_first electrolytes, calcium | CONFIRMED | HF 2022 4.1.1 rec 2 (COR 1, C-EO): serum electrolytes in initial labs; synopsis specifies sodium, potassium, calcium and magnesium. Not in NG106 1.2.12 ("renal function" may cover). |
| tests_first iron_studies | CONFIRMED | HF 2022 4.1.1 rec 2 (COR 1, C-EO): iron studies (serum iron, ferritin, transferrin saturation) in initial labs; NG106 1.4.5 (HFrEF). HF 2022 10.1: iron deficiency = ferritin <100 ug/L, or 100-300 ug/L with TSAT <20%; IV iron reasonable in HFrEF with iron deficiency (2a, B-R); oral iron not adequate (IRONOUT HF). |
| red flags hf_breathless_rest, hf_chest_pain, hf_syncope; hf_rapid_weight_gain | NO SOURCE FOUND | Not in NG106. HF 2022 has no outpatient red-flag list: shock criteria (9.5, Table 22: SBP <90 for >30 min plus hypoperfusion), advanced-HF indicators (8.1, Table 18) and precipitants of decompensation (Table 21: ACS, uncontrolled hypertension, AF, infection, NSAIDs, verapamil) are hospital or advanced-stage context. |
| option limit_salt | CONTRADICTED (NICE) / PARTLY SUPPORTED (US) | NG106 1.9.10: do NOT routinely advise salt/fluid restriction; 1.9.11 avoid potassium salt substitutes. HF 2022 7.1.2 rec 1 (COR 2a, C-LD): "avoiding excessive sodium intake is reasonable to reduce congestive symptoms"; no numeric target (AHA <2,300 mg/d is general health advice with no HF trials); restriction can reduce diet quality. 8.2 (2b, C-LD): benefit of fluid restriction in advanced HF with hyponatremia uncertain. Salt substitutes not addressed. CONFLICT: 2025 BP 5.1 rec 4 (COR 2a, LOE A) says potassium-based salt substitutes can be useful except in CKD or with drugs reducing potassium excretion; BP guideline scope 1.4 excludes HF. Project rule: NICE wording kept; flagged for clinician. |
| option daily_weights | PARTLY SUPPORTED | HF 2022: weight monitoring in discharge instructions and the transitional care plan (9.6 text 2, Table 25); daily standing weights for inpatients (9.3 text 2); self-care education to monitor for worsening signs and symptoms (7.1.1). No outpatient daily-weight recommendation and no weight-gain threshold. |
| option diuretic_by_specialist | NO SOURCE FOUND | Design choice. HF 2022 4.1 rec 1 (COR 1, B-NR): congestion assessed at each encounter to guide diuretic adjustment; 7.2: diuretics for fluid retention (COR 1) - neither says who adjusts. |
| option review_hf_worsening_meds | CONFIRMED (HFrEF) | HF 2022 7.3.7: NSAIDs worsen HF, avoid or withdraw (rec 7, 3: Harm, B-NR); thiazolidinediones increase worsening HF (rec 5, 3: Harm, A); non-dihydropyridine CCBs (diltiazem, verapamil) not recommended (rec 3, 3: Harm, A); saxagliptin/alogliptin avoid (rec 6, 3: Harm, B-R); Table 13 adds COX-2 inhibitors, flecainide, disopyramide, sotalol, dronedarone, doxazosin, nifedipine. 6.1 rec 7: thiazolidinediones not with LVEF <50%. Also NG106 1.4.12; FDA 2015 (NSAIDs); Takeda 2007 (pioglitazone). Amlodipine: 7.3.7 rec 1 - no benefit for HF but may be used for hypertension, so not an HF-worsening drug; listed for swelling (next row). |
| hook "amlodipine causes ankle swelling" | CONFIRMED | 2025 BP Table 13: dihydropyridine CCB "associated with dose-related lower extremity edema, more common in women"; Table 17: combining with a RAS inhibitor reduces CCB-induced leg swelling. |
| "Other causes of swelling: kidney, liver, low albumin" | NO SOURCE FOUND | |
| not_seen kidney disease (nephrology) | PARTLY SUPPORTED | NG106 1.6.2: eGFR <30 -> liaise with renal physician (HF management, not routing). |
| subspecialty heart_failure | PARTLY SUPPORTED | NG106 specialist assessment pathway. HF 2022 8.1 rec 1 (COR 1, C-LD): timely referral to HF specialty care for ADVANCED HF; Table 18 lists indicators. No outpatient referral time-frames. |
| tiers.urgent "2 weeks matches NICE" | PARTLY SUPPORTED | NICE 2-week rule applies only to NT-proBNP >2000. |
| Diagnosis when EF >40% needs raised filling pressure (e.g. natriuretic peptide) | CONFIRMED | HF 2022 2.2-2.3, Table 4; Figure 4 natriuretic peptide thresholds NT-proBNP >125 pg/mL, BNP >=35 pg/mL. |

## For cardiologist review
- Salt advice wording (UK vs US vs BP-guideline potassium-substitute conflict).
- Surfacing ancestry; age/AF as "may raise" from other literature.
- NT-proBNP 90-day window.
