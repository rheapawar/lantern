# Hard-to-control BP / cholesterol - fact-check

## Checked against
- 2025 AHA/ACC/AANP/AAPA/ABC/ACCP/ACPM/AGS/AMA/ASPC/NMA/PCNA/SGIM Guideline for the Prevention, Detection, Evaluation and Management of High Blood Pressure in Adults (Jones et al.), Circulation 2025;152:e114-e218; JACC DOI 10.1016/j.jacc.2025.05.007; Circulation DOI 10.1161/CIR.0000000000001356. US. FULL TEXT. Refs verified (re-verified 2026-11-26, all matched): 1.4 scope; 3.1.2 + Table 6; 3.1.4; 3.2.2; 3.2.3 + Tables 10-11; 3.2.3.1 rec 1 and rec 5; 5.1 rec 4; 5.2.5; 5.2.7; 5.3.4.1; 5.6 + Fig 8; 6.2 + Fig 9; Tables 13 and 17.
- ACC Ten Points for the 2025 BP guideline.
- Secondary summaries: ACC journal scan https://www.acc.org/latest-in-cardiology/journal-scans/2025/08/14/15/36/new-acc-aha-guideline-addresses-prevention-detection-evaluation-and-management-of-hbp ; 2 Minute Medicine https://www.2minutemedicine.com/guidelines/high-blood-pressure/ ; NephJC https://www.nephjc.com/news/accaha2025-klno3 ; Medical Dialogues https://medicaldialogues.in/cardiology-ctvs/guidelines/new-blood-pressure-guidelines-10-practice-changing-updates-to-know-154111
- The 2025 guideline retires and replaces the 2017 guideline; `sources.aha_bp_2017_2025` ("2017; updated 2025") should cite only 2025. Scope (1.4) excludes BP management in chronic coronary disease, HF, AF, valve disease, aortic disease and PAD.
- Cholesterol: 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Dyslipidemia (13 Mar 2026; JACC DOI 10.1016/j.jacc.2025.11.016) retires and replaces the 2018 AHA/ACC Blood Cholesterol guideline. ACC summary only: https://www.acc.org/latest-in-cardiology/journal-scans/2026/03/13/15/20/acc-aha-release-new-clinical-guideline-for-managing-dyslipidemia ; guideline full text not yet checked.

## BP verdicts

| id | Verdict | Ref / notes |
|---|---|---|
| Goal BP "<130/80" | CONFIRMED (full text) | 5.2.7: goal <130/80; judge on average of >=2 readings at >=2 visits. |
| bp_emergency (emergent) | PARTLY SUPPORTED + minor CONTRADICTION (full text) | 6.2 + Fig 9: hypertensive emergency = >180 and/or >120 with acute target-organ damage -> ICU. Pathway regexes/obs use >=180 / >=120; guideline is strictly ">". CLAUDE.md table also says ">=". Symptom list is a text proxy for acute TOD - cardiologist to confirm. |
| bp_severe_no_symptoms (urgent) | PARTLY SUPPORTED (full text) | 6.2 + Fig 9: severe hypertension >180/120 WITHOUT acute TOD -> outpatient, no ED referral, follow-up within 4 weeks. Whether this is "urgent ~2 weeks" is a Lantern tier choice. |
| bp_low_potassium (urgent) | CONTRADICTED as an urgency criterion (full text) | 3.2.3.1 rec 1: PA screening COR 1 for resistant HTN regardless of K; hypokalemia (spontaneous or diuretic-induced) is one screening trigger, not an urgency criterion. Code: match checks only K <3.5 in 180 days, not high BP. |
| Resistant-HTN definition | CONFIRMED (full text) | 5.6 + Fig 8: above goal on 3 meds incl. a diuretic, or needing >=4. |
| Exclude white-coat effect | CONFIRMED (full text) | 3.2.2 (COR 2a). |
| tests_first labs | CONFIRMED (full text) | 3.1.2 + Table 6: CBC, Na/K/Ca, creatinine+eGFR, lipids, glucose or HbA1c, TSH, urinalysis, UACR, ECG. Pathway lists glucose AND a1c (guideline "or"). |
| tests_first: out_of_office_bp; option home_bp_log | CONFIRMED (full text) | 3.1.4 (COR 1, LOE A): ABPM and/or HBPM for diagnosis and titration. |
| option adherence_check | CONFIRMED (full text) | 5.2.5. |
| tests_first: aldosterone_renin (not pre-checked) | CONFIRMED (full text) | 3.2.3.1 rec 1: COR 1 for resistant HTN regardless of K; also hypokalemia, OSA, adrenal incidentaloma, family history early-onset HTN, stroke <40; COR 2b for stage 2 HTN. Judgment: pre-check when resistant criteria met? |
| Secondary-cause clues (K, OSA, CKD, young age) | PARTLY SUPPORTED (full text) | 3.2.3 + Table 10 secondary causes; PA triggers above. "Kidney disease" and "young age" are not PA triggers as such; family history early-onset HTN, stroke <40, adrenal incidentaloma not in pathway fact list. |
| option review_interfering_meds | CONFIRMED (full text) | 3.2.3 + Table 11: alcohol, caffeine, decongestants, NSAIDs, stimulants, SNRI/TCA/MAOI, atypical antipsychotics, cyclosporine/tacrolimus, oral contraceptives, systemic corticosteroids, licorice. Pathway text omits caffeine, antidepressants, immunosuppressants, licorice. |
| not_seen PA -> endocrinology | CONFIRMED (full text) | 3.2.3.1 rec 5: positive screen -> hypertension specialist or endocrinologist. |
| not_seen kidney -> nephrology; routing | PARTLY SUPPORTED (full text) | 5.6 + Fig 8: refer for suspected secondary cause or BP uncontrolled >6 months. No kidney-specific rule. "Often eConsult" is a product assumption. |
| review_notes "severe hypertension replaced hypertensive urgency; outpatient" | CONFIRMED (full text) | 6.2 + Fig 9. |
| amlodipine/DHP CCB ankle swelling | CONFIRMED (full text) | Table 13: "dose-related lower extremity edema, which is more common in women than men"; Table 17: DHP CCB + RAS inhibitor reduces leg swelling. |
| diltiazem/verapamil in HFrEF | CONFIRMED (full text) | Table 13; 5.3.4.1: "Do not use in patients with HFrEF". |
| Potassium-based salt substitutes (conflict with NICE) | CONFLICT - flag for clinician | 5.1 rec 4 (COR 2a, LOE A): can be useful except in CKD or with drugs reducing potassium excretion. NICE NG106 1.9.11: avoid in HF. Different populations; BP scope (1.4) excludes HF. NICE wording kept for HF option. |

### ESC comparison (BP)
2024 ESC hypertension guideline: not yet checked.

## Cholesterol verdicts

| id | Verdict | Notes |
|---|---|---|
| sources.aha_chol_2018 | SUPERSEDED | Replaced by the 2026 ACC/AHA Dyslipidemia guideline. Update catalog and the "Cholesterol source" review note. |
| "LDL 190+ suggests inherited high cholesterol" | NO SOURCE FOUND | Not stated in the ACC 2026 summary; guideline full text not yet checked. |
| LDL goals / "on-statin LDL above goal may need added therapy" | CONFIRMED (ACC 2026 summary) | Goals <100 mg/dL borderline/intermediate risk, <70 high risk, <55 very-high-risk ASCVD; add ezetimibe, bempedoic acid or PCSK9 mAb when statin + lifestyle insufficient. 2018 had no numeric goals. |
| New in 2026 (not in pathway) | for review | One-time Lp(a) in adulthood; PREVENT-ASCVD equations (ages 30-79); optional apoB; selective CAC. |
| lipids/a1c in BP referral | CONFIRMED (full text) | 2025 BP Table 6. |

## For cardiologist review
- Strict ">" vs ">=" at 180/120; whether bp_low_potassium should leave "urgent".
- Tier for severe hypertension without TOD (guideline: outpatient, 4-week follow-up).
- Potassium salt-substitute conflict.
- Updating cholesterol content to the 2026 guideline.
