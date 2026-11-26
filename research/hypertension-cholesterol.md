# Hard-to-control BP / cholesterol - fact-check

## Source status
- 2025 AHA/ACC/AANP/AAPA/ABC/ACCP/ACPM/AGS/AMA/ASPC/NMA/PCNA/SGIM Guideline for the Prevention, Detection, Evaluation and Management of High Blood Pressure in Adults (Jones et al.), Circulation 2025;152:e114-e218; JACC DOI 10.1016/j.jacc.2025.05.007 (Circulation DOI 10.1161/CIR.0000000000001356). US.
- Verified against full text: all section/table refs below were checked against the full guideline on 2026-11-26.
- It retires and replaces the 2017 guideline, so `sources.aha_bp_2017_2025` ("2017; updated 2025") is misleading - cite only 2025.
- Scope (sec 1.4): the guideline EXCLUDES BP management in chronic coronary disease, HF, AF, valve disease, aortic disease and PAD. So it is a source for the hard-to-control BP reason only, not for BP advice inside the chest pain / AF / HF reasons.
- Secondary summaries also read: ACC journal scan https://www.acc.org/latest-in-cardiology/journal-scans/2025/08/14/15/36/new-acc-aha-guideline-addresses-prevention-detection-evaluation-and-management-of-hbp ; https://www.2minutemedicine.com/guidelines/high-blood-pressure/ ; https://www.nephjc.com/news/accaha2025-klno3 ; https://medicaldialogues.in/cardiology-ctvs/guidelines/new-blood-pressure-guidelines-10-practice-changing-updates-to-know-154111 .
- Cholesterol: 2018 AHA/ACC guideline SUPERSEDED by the 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Dyslipidemia (13 Mar 2026, JACC DOI 10.1016/j.jacc.2025.11.016). Checked against the ACC summary only: https://www.acc.org/latest-in-cardiology/journal-scans/2026/03/13/15/20/acc-aha-release-new-clinical-guideline-for-managing-dyslipidemia

## BP verdicts

| id | Verdict | Ref / notes |
|---|---|---|
| Goal BP "<130/80" | CONFIRMED (verified against full text) | 5.2.7: goal <130/80; judge on average of >=2 readings at >=2 visits. |
| bp_emergency (emergent) | PARTLY SUPPORTED + minor CONTRADICTION (verified against full text) | 6.2 + Fig 9: hypertensive emergency = >180 and/or >120 with acute target-organ damage -> ICU. Pathway regex/obs use >=180 / >=120; guideline is strictly ">". CLAUDE.md table also says ">=". Symptom list is a text proxy for acute TOD - cardiologist to confirm. |
| bp_severe_no_symptoms (urgent) | PARTLY SUPPORTED (verified against full text) | 6.2 + Fig 9: severe hypertension >180/120 WITHOUT acute TOD -> outpatient, no ED referral, follow-up within 4 weeks. Whether this is "urgent ~2 weeks" is Lantern's tier choice - cardiologist judgment. |
| bp_low_potassium (urgent) | CONTRADICTED as an urgency criterion (verified against full text) | 3.2.3.1 rec 1: PA screening COR 1 for resistant HTN regardless of K; hypokalemia (spontaneous or diuretic-induced) is one screening trigger, not an urgency criterion. Suggest remove from urgent_flags. Code: match checks only K <3.5 in 180 days, not high BP. K<3.5 itself is a lab convention. |
| Resistant-HTN definition (why-text) | CONFIRMED (verified against full text) | 5.6 + Fig 8: above goal on 3 meds incl. a diuretic, or needing >=4. |
| Exclude white-coat effect | CONFIRMED (verified against full text) | 3.2.2 (COR 2a): confirm apparent resistant HTN with out-of-office monitoring. Pathway already has out_of_office_bp. |
| tests_first labs | CONFIRMED (verified against full text) | 3.1.2 + Table 6: CBC, Na/K/Ca, creatinine+eGFR, lipids, glucose or HbA1c, TSH, urinalysis, UACR, ECG. Pathway lists both glucose and a1c; guideline "or" (minor). |
| tests_first: out_of_office_bp | CONFIRMED (verified against full text) | 3.1.4 (COR 1, LOE A): ABPM and/or HBPM, for diagnosis and for titration. |
| option home_bp_log | CONFIRMED (verified against full text) | 3.1.4 as above (home BP monitoring for diagnosis and titration). |
| option adherence_check | CONFIRMED (verified against full text) | 5.2.5 (adherence). |
| tests_first: aldosterone_renin (not pre-checked) | CONFIRMED (verified against full text) | 3.2.3.1 rec 1: COR 1 for resistant HTN regardless of K; also hypokalemia, OSA, adrenal incidentaloma, family history early-onset HTN, stroke <40 (COR 1); COR 2b for stage 2 HTN per earlier summaries. Judgment: pre-check when resistant criteria met? |
| Secondary-cause clues (K, OSA, CKD, young age) | PARTLY SUPPORTED (verified against full text) | 3.2.3 + Table 10 lists secondary causes; PA triggers above. "Kidney disease" and "young age" are not PA triggers per se; family history early-onset HTN, stroke <40 and adrenal incidentaloma are missing from the pathway fact list. |
| option review_interfering_meds | CONFIRMED (verified against full text) | 3.2.3 + Table 11: alcohol, caffeine, decongestants, NSAIDs, stimulants, SNRI/TCA/MAOI, atypical antipsychotics, cyclosporine/tacrolimus, oral contraceptives, systemic corticosteroids, licorice, etc. Pathway text omits caffeine, antidepressants, immunosuppressants, licorice (judgment). |
| not_seen PA -> endocrinology | CONFIRMED (verified against full text) | 3.2.3.1 rec 5: positive screen -> hypertension specialist or endocrinologist. |
| not_seen kidney -> nephrology; subspecialty routing | PARTLY SUPPORTED (verified against full text) | 5.6 + Fig 8: refer for suspected secondary cause or BP uncontrolled >6 months. No kidney-specific rule found in these refs. "Often eConsult" is a product assumption. |
| review_notes "severe hypertension replaced hypertensive urgency; outpatient" | CONFIRMED (verified against full text) | 6.2 + Fig 9. |
| amlodipine/dihydropyridine CCB causes ankle swelling | CONFIRMED (verified against full text) | Table 13: "Associated with dose-related lower extremity edema, which is more common in women than men." Table 17: dihydropyridine CCB + RAS inhibitor reduces CCB-induced leg swelling. Confirms the CLAUDE.md hook. (Replaces NO SOURCE FOUND.) |
| diltiazem/verapamil in HFrEF | CONFIRMED (verified against full text) | Table 13; 5.3.4.1: "Do not use in patients with HFrEF". Same as NICE NG106 1.4.12. |
| Potassium-based salt substitutes (CONFLICT with NICE) | CONFLICT - flag for clinician | 5.1 rec 4 (COR 2a, LOE A): potassium-based salt substitutes can be useful to lower BP except in CKD or with drugs reducing potassium excretion (verified against full text). NICE NG106 1.9.11: avoid potassium salt substitutes in HF. Different populations (hypertension vs HF), and 1.4 scope excludes HF from the BP guideline. Project rule: NICE wording kept for HF option. |

### ESC comparison (BP)
2024 ESC hypertension guideline: not checked. No claim.

## Cholesterol verdicts

| id | Verdict | Notes |
|---|---|---|
| sources.aha_chol_2018 | SUPERSEDED | Replaced by 2026 ACC/AHA Dyslipidemia guideline. Update catalog and the "Cholesterol source" review note. |
| "LDL 190+ suggests inherited high cholesterol" | NO SOURCE FOUND | The checked 2026 summary does not address LDL >=190. |
| "on-statin LDL above goal may need added therapy" / LDL goals | CONFIRMED (2026 ACC summary, not full text) | Goals <100 / <70 / <55 mg/dL by risk; add ezetimibe, bempedoic acid or PCSK9 mAb when statin + lifestyle insufficient. 2018 had no numeric goals. |
| New in 2026 (not in pathway) | for review | One-time Lp(a); PREVENT-ASCVD equations (30-79); optional apoB; selective CAC. |
| lipids/a1c in BP referral | CONFIRMED (verified against full text) | Table 6. |

## For cardiologist review
- Strict ">" vs ">=" at 180/120; whether bp_low_potassium should leave "urgent".
- Tier for severe hypertension without TOD (guideline: outpatient, 4-week follow-up).
- Potassium salt-substitute conflict (above).
- Updating cholesterol content to the 2026 guideline.
