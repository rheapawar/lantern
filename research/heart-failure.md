# Heart failure symptoms - fact-check (NICE NG106 + QS9, UK; 2022 AHA/ACC/HFSA, US)

## Checked against
- NICE NG106, Chronic heart failure in adults: diagnosis and management (UK), recommendations 1.1-1.12 and Terms used, last updated 3 Sep 2025 - FULL TEXT. Catalog label "(2018)" should read "updated 3 Sep 2025".
- NICE QS9, Chronic heart failure in adults - quality standard: not yet checked (its cited NG106 rec numbers should be compared; NG106 itself has 1.2.3 = >2000, 1.2.4 = 400-2000).
- 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure (US; Circulation 145:e895; PMID 35363499; DOI 10.1161/CIR.0000000000001063): abstract and ACC Key Perspectives only - https://www.acc.org/Latest-in-Cardiology/ten-points-to-remember/2022/03/29/19/53/2022-AHA-ACC-HFSA-Heart-Failure-Guideline-gl-hf . Also HelixTalk summary (Rosalind Franklin Univ.) https://www.rosalindfranklin.edu/academics/college-of-pharmacy/helixtalk/helixtalk-147-key-recommendations-from-the-2022-aha-acc-hfsa-heart-failure-guidelines/ . Sections 7.3.1 (sodium), drugs to avoid, and initial workup: full text not yet checked (free on PMC).
- 2025 AHA/ACC High Blood Pressure guideline (Circulation 2025;152:e114-e218) - FULL TEXT (Tables 13, 17; 5.1; 5.3.4.1; scope 1.4 excludes BP management in HF).
- FDA Drug Safety Communication on NSAIDs, 9 Jul 2015, as reproduced by the American Society of Anesthesiologists - https://asahq.org/advocacy-and-asapac/fda-and-washington-alerts/fda-alerts/2015/07/nsaids-fda-strengthens-warning-of-increased-chance-of-heart-attack-or-stroke
- Takeda, "Takeda Revises ACTOS (pioglitazone HCl) Prescribing Label", 6 Jun 2007 - https://takeda.com/en-us/newsroom/news-releases/2007/takeda-revises-actos-pioglitazone-hcl-prescribing-label
- ACC, "Iron Deficiency and Treatment for Cardiovascular Disease: Key Points", 2022 (summary of an EHJ review, not the guideline) - https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2022/11/30/17/14/iron-deficiency-and-cvd
- AHA scientific statement "Drugs That May Cause or Exacerbate Heart Failure" (Page et al., Circulation 2016;134:e32; DOI 10.1161/CIR.0000000000000426): not yet checked directly.
- Still current: no 2026 AHA/ACC HF guideline identified; ESC 2026 HF guideline and ESC 2023 focused update not yet checked.

## Verdicts

| id | Verdict | Ref / notes |
|---|---|---|
| hf_ntprobnp_over_2000 (urgent) | CONFIRMED | NICE NG106 1.2.3: >2,000 ng/L -> specialist + echo within 2 weeks. UK; no US equivalent time-frame found. "2 weeks = urgent" is Lantern's mapping. |
| hf_ntprobnp_400_2000 (soon hint) | CONFIRMED | NG106 1.2.4: within 6 weeks. ng/L = pg/mL. |
| "below 400 makes HF less likely (untreated)" | CONFIRMED | NG106 1.2.5, 1.2.6. |
| review_note prior-MI fast track | CONFIRMED not kept | Absent from current NG106 (was in CG108). |
| "NT-proBNP pushed UP by age >70, AFib, eGFR<60, lung disease, diabetes" | CONTRADICTED vs NICE | NG106 1.2.7 lists pulmonary, renal, liver, systemic pathologies, sepsis, COPD, diabetes, cirrhosis; not age >70 or AF; no eGFR cut-off. |
| "NT-proBNP pushed DOWN by obesity (BMI>35), drugs" | PARTLY SUPPORTED | 1.2.7: obesity, African/African-Caribbean family background, diuretics, ACEi/ARNI/ARB, beta-blockers, MRAs. "BMI >35" not in NICE; ARNI and ancestry missing. |
| tests_first ecg, cxr, renal, tsh, liver, lipids, a1c, cbc, urinalysis | CONFIRMED | NG106 1.2.12 (non-ECG items "consider"; peak flow/spirometry not in pathway). |
| tests_first nt_probnp, echo | CONFIRMED | 1.2.2-1.2.4. |
| tests_first electrolytes | NO SOURCE FOUND | Not in 1.2.12 ("renal function" may cover). |
| tests_first iron_studies | PARTLY SUPPORTED | NG106 1.4.5: iron studies in HFrEF. 2022 US guideline: recommendations for HF with anemia/iron deficiency (ACC Key Perspectives). Iron deficiency defined as ferritin <100 ng/mL, or 100-299 with TSAT <20% (ACC iron Key Points, 2022). Class/LOE and "initial workup" status in the US guideline not yet checked. |
| red flags hf_breathless_rest, hf_chest_pain, hf_syncope; hf_rapid_weight_gain | NO SOURCE FOUND | Not in NG106 or the checked US summaries. |
| option limit_salt | CONTRADICTED (NICE) / PARTLY SUPPORTED (US) | NG106 1.9.10: do NOT routinely advise salt/fluid restriction; 1.9.11 avoid potassium salt substitutes. US 2022: avoiding excessive sodium is reasonable for congestive symptoms, no numeric maximum, no clear outcome benefit (HelixTalk summary; class/LOE stated as 2a C-LD in other excerpts, section 7.3.1 not yet checked). CONFLICT: 2025 BP 5.1 rec 4 (COR 2a, LOE A) says potassium-based salt substitutes can be useful except in CKD or with drugs reducing potassium excretion; NICE 1.9.11 says avoid in HF; BP guideline scope 1.4 excludes HF. Project rule: NICE wording kept; flagged for clinician. |
| option daily_weights | NO SOURCE FOUND | ACC HF article: "self-care support" for stage C; daily weights not mentioned. NG106 self-management text not yet searched for "weigh". |
| option diuretic_by_specialist | NO SOURCE FOUND | Design choice. |
| option review_hf_worsening_meds | PARTLY SUPPORTED | Diltiazem/verapamil: CONFIRMED (NG106 1.4.12; 2025 BP Table 13 / 5.3.4.1 "Do not use in patients with HFrEF"). Pioglitazone: CONFIRMED (FDA-requested boxed warning, Takeda 2007: "can cause fluid retention that may lead to or worsen heart failure"; current label not yet checked). NSAIDs: CONFIRMED (FDA DSC 2015: "There is an increased risk of heart failure with NSAID use"). Amlodipine: not a "worsens HF" drug in NG106 (only short-acting dihydropyridines); its listing belongs under "cause swelling" - see next row. |
| hook "amlodipine causes ankle swelling" | CONFIRMED | 2025 BP Table 13: dihydropyridine CCB "associated with dose-related lower extremity edema, more common in women"; Table 17: combining with a RAS inhibitor reduces CCB-induced leg swelling. |
| "Other causes of swelling: kidney, liver, low albumin" | NO SOURCE FOUND | |
| not_seen kidney disease (nephrology) | PARTLY SUPPORTED | NG106 1.6.2: eGFR <30 -> liaise with renal physician (HF management, not routing). |
| subspecialty heart_failure | PARTLY SUPPORTED | NG106 specialist assessment pathway; 2022 US: timely referral to HF specialty care for ADVANCED HF (ACC Key Perspectives). |
| tiers.urgent "2 weeks matches NICE" | PARTLY SUPPORTED | NICE 2-week rule applies only to NT-proBNP >2000. |
| Diagnosis when EF >40% needs raised filling pressure (e.g. natriuretic peptide) | CONFIRMED | 2022 AHA/ACC/HFSA via ACC Key Perspectives. |

## For cardiologist review
- Salt advice wording (UK vs US vs BP-guideline potassium-substitute conflict).
- Surfacing ancestry; age/AF as "may raise" from other literature.
- NT-proBNP 90-day window.
