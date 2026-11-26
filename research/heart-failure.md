# Heart failure symptoms - fact-check (NICE NG106 + QS9, UK; 2022 AHA/ACC/HFSA, US)

## Source status
- NICE NG106 (UK, last updated 3 Sep 2025): verified against full text (recommendations 1.1-1.12 and Terms used). Catalog label "(2018)" should say updated 3 Sep 2025.
- NICE QS9 (UK): not yet checked. NG106 itself has 1.2.3 = >2,000 and 1.2.4 = 400-2,000.
- 2022 AHA/ACC/HFSA HF guideline (US; Circulation 145:e895; PMID 35363499; DOI 10.1161/CIR.0000000000001063): checked against the PubMed abstract and the ACC Key Perspectives page (https://www.acc.org/Latest-in-Cardiology/ten-points-to-remember/2022/03/29/19/53/2022-AHA-ACC-HFSA-Heart-Failure-Guideline-gl-hf). From those: HF classified by LVEF; when EF >40% the diagnosis needs evidence of raised filling pressures (e.g. natriuretic peptide); comorbidities to manage include anemia, iron deficiency, hypertension, sleep disorders, diabetes, AF, CAD. Not yet checked: sodium (7.3.1), drugs to avoid, initial workup.
- 2025 BP guideline refs below are verified against the full text (Circulation 2025;152:e114-e218); its scope (1.4) excludes BP management in HF.
- Still current: no 2026 AHA/ACC HF guideline found (next guideline reportedly late 2027, per secondary sources). An ESC 2026 HF guideline exists (not checked).

## Verdicts

| id | Verdict | Ref / notes |
|---|---|---|
| hf_ntprobnp_over_2000 (urgent) | CONFIRMED - verified against full text | NG106 1.2.3: >2,000 ng/L -> specialist + echo within 2 weeks. UK guidance; no US equivalent timeframe in the checked material. 2 weeks = "urgent" is Lantern's mapping. |
| hf_ntprobnp_400_2000 (soon hint) | CONFIRMED - verified | NG106 1.2.4: within 6 weeks. |
| "below 400 makes HF less likely" | CONFIRMED - verified | 1.2.5, 1.2.6. |
| review_note prior-MI fast track | CONFIRMED not kept - verified | Absent from current NG106; delete note. |
| "NT-proBNP pushed UP by age >70, AFib, eGFR<60..." | CONTRADICTED vs NICE - verified | 1.2.7 lists pulmonary, renal, liver, systemic pathologies, sepsis, COPD, diabetes, cirrhosis; NOT age >70 or AF; no eGFR cut-off. |
| "NT-proBNP pushed DOWN by obesity (BMI>35), drugs" | PARTLY SUPPORTED - verified | 1.2.7: obesity, African/African-Caribbean background, diuretics, ACEi/ARNI/ARB, beta-blockers, MRAs. "BMI >35" not in NICE; ARNI and ancestry missing. |
| tests_first ecg, cxr, renal, tsh, liver, lipids, a1c, cbc, urinalysis | CONFIRMED - verified | 1.2.12 (non-ECG items "consider"; spirometry/peak flow not in pathway). |
| tests_first nt_probnp, echo | CONFIRMED - verified | 1.2.2-1.2.4. |
| tests_first electrolytes | NO SOURCE FOUND | |
| tests_first iron_studies | PARTLY SUPPORTED | NG106 1.4.5 (HFrEF management; verified). US 2022: comorbidities include iron deficiency/anemia (ACC page); the "guideline recommends iron studies" claim is not verified (class 2a IV iron is from a secondary summary only). |
| red flags hf_breathless_rest, hf_chest_pain, hf_syncope; hf_rapid_weight_gain | NO SOURCE FOUND | |
| option limit_salt | CONTRADICTED (by NICE, verified) / US unverified | NG106 1.9.10: do NOT routinely advise salt/fluid restriction. 1.9.11: avoid potassium salt substitutes. US 2022 sodium rec (7.3.1; secondary summaries give COR 2a, LOE C-LD "avoid excessive sodium") is NOT verified from full text. Separate CONFLICT: 2025 BP 5.1 rec 4 (COR 2a, LOE A; verified) says potassium-based salt substitutes can be useful except in CKD or with drugs reducing potassium excretion; NICE 1.9.11 says avoid in HF. Different populations; BP guideline scope (1.4) excludes HF. Project rule: keep NICE wording for the HF option; flagged for clinician. |
| option daily_weights | NO SOURCE FOUND | Not found in NG106 text checked; search 1.9 self-management for "weigh". |
| option diuretic_by_specialist | NO SOURCE FOUND | Design choice. |
| option review_hf_worsening_meds | PARTLY SUPPORTED | Diltiazem/verapamil: CONFIRMED - NG106 1.4.12 (avoid in HFrEF; also short-acting dihydropyridines) and 2025 BP Table 13 / 5.3.4.1 "Do not use in patients with HFrEF" (verified against full text). NSAIDs and pioglitazone: NO SOURCE FOUND. Amlodipine: not on NICE's avoid list (long-acting DHP); it belongs under "cause swelling", not "worsen HF". |
| hook / fact "amlodipine causes ankle swelling" | CONFIRMED (verified against full text) | 2025 BP Table 13: dihydropyridine CCB "associated with dose-related lower extremity edema, more common in women than men"; Table 17: DHP CCB + RAS inhibitor reduces CCB-induced leg swelling. Confirms the CLAUDE.md hook. |
| "Other causes of swelling: kidney, liver, low albumin" | NO SOURCE FOUND | |
| not_seen kidney disease (nephrology) | PARTLY SUPPORTED - verified | NG106 1.6.2: eGFR <30 -> liaise with renal physician (HF management, not routing). |
| subspecialty heart_failure | PARTLY SUPPORTED | NG106 specialist assessment (verified); 2022 US: timely referral for ADVANCED HF (ACC page). |
| tiers.urgent "2 weeks matches NICE" | PARTLY SUPPORTED | Only for NT-proBNP >2000. |
| HF diagnosis when EF >40% needs raised filling pressure (e.g. natriuretic peptide) | CONFIRMED (ACC Key Perspectives / abstract, not guideline full text) | 2022 AHA/ACC/HFSA. |

## For cardiologist review
- Salt advice wording (UK vs US vs BP-guideline conflict).
- Surfacing ancestry; age/AF as "may raise" from other literature.
- NT-proBNP 90-day window.
