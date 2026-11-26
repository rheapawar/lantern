# Lantern research index - guideline fact-check of pathways/cardiology.json

Date: 2026-11-26. Verdicts: CONFIRMED / CONTRADICTED / PARTLY SUPPORTED / NO SOURCE FOUND. NO SOURCE FOUND = the checked material does not settle it (not "wrong").

Files: chest-pain.md, afib.md, heart-failure.md, hypertension-cholesterol.md, conduction-qt.md, selection-rules.md.

## What each guideline was checked against

| Guideline | Checked against | Sections still to check |
|---|---|---|
| NICE NG106 Chronic heart failure in adults (UK, last updated 3 Sep 2025) | Full text: recommendations 1.1-1.12 and Terms used | - |
| 2025 AHA/ACC High Blood Pressure guideline (US; Circulation 2025;152:e114-e218; DOI 10.1161/CIR.0000000000001356) | Full text | - |
| 2021 AHA/ACC Chest Pain guideline (US; Circulation 2021;144:e368; DOI 10.1161/CIR.0000000000001029) | ACC "Ten Points to Remember" summary | Stable chest pain initial testing (ECG, labs, chest X-ray); CAC/CCTA/stress selection and known / no-known CAD algorithms; contrast and kidney statements; cardiac / possibly cardiac / noncardiac definition |
| 2023 ACC/AHA/ACCP/HRS Atrial Fibrillation guideline (US) | ACC "Key Perspectives" summary; 2024 ESC AF review (Rienstra et al., Europace 2024) | Stroke-risk recommendations and thresholds; bleeding risk; initial evaluation (ECG, echo, TSH, labs, monitoring); risk-factor modification; unstable AF and pre-excitation |
| 2022 AHA/ACC/HFSA Heart Failure guideline (US; Circulation 2022;145:e895; PMID 35363499; DOI 10.1161/CIR.0000000000001063) | PubMed abstract; ACC "Key Perspectives" summary | Sodium (7.3.1); medicines that worsen HF; iron deficiency and anemia; natriuretic-peptide diagnosis; initial evaluation of suspected HF. Full text is free on PMC. |
| NICE QS9 Chronic heart failure (UK) | Not yet checked | Statement 2 (specialist assessment) and the NG106 recommendations it cites |
| 2018 ACC/AHA/HRS Bradycardia and Cardiac Conduction Delay guideline (US; Circulation 2019;140:e382) | ACC news summary | Evaluation and reversible causes (drugs, thyroid, electrolytes, sleep apnea); acquired AV block recommendations (first-degree, Mobitz I/II, high-grade, 2:1) with COR/LOE; bundle/fascicular block with syncope; echo for conduction disease |
| 2010 AHA/ACCF Prevention of Torsade de Pointes in Hospital Settings (US; Circulation 2010;121:1047) | Secondary summaries only | TdP risk-factor table; ECG-signs table (QTc >500 ms, +60 ms); measuring QT; correcting K/Mg/Ca; stopping offending drugs; scope (inpatient) |
| 2026 ACC/AHA Dyslipidemia guideline (US; JACC DOI 10.1016/j.jacc.2025.11.016) | ACC journal-scan summary | LDL-C >=190; baseline lipid testing; LDL-C goals table; statin intolerance; Lp(a); risk estimator |
| ESC 2024 hypertension, 2023 HF focused update, 2026 HF, 2024 chronic coronary syndromes | Not checked | - |

2025 BP guideline refs verified against the full text: 3.1.2 + Table 6; 3.1.4; 3.2.2; 3.2.3 + Tables 10-11; 3.2.3.1 rec 1 and rec 5; 5.1 rec 4; 5.2.5; 5.2.7; 5.3.4.1; 5.6 + Fig 8; 6.2 + Fig 9; Tables 13 and 17; scope 1.4 (excludes BP management in chronic coronary disease, HF, AF, valve disease, aortic disease, PAD).

## Superseded / catalog problems
| Source key | Finding |
|---|---|
| aha_bp_2017_2025 | 2017 retired and replaced by 2025 (Circulation 2025;152:e114-e218; DOI 10.1161/CIR.0000000000001356). Cite only 2025. |
| aha_chol_2018 | SUPERSEDED by the 2026 ACC/AHA Dyslipidemia guideline (13 Mar 2026). |
| nice_ng106 "(2018)" | Updated 3 Sep 2025 (verified). |
| nice_qs9 | Not yet checked; check which NG106 rec numbers it cites. |
| aha_qt_2010 | No replacement found (not exhaustive); inpatient statement, weak fit. |
| acc_brady_2018, aha_chest_pain_2021, acc_afib_2023, aha_hf_2022 | Titles correct, still current. |

## Summary table (key = pathway item id; ref where known)
| id | Verdict | Ref |
|---|---|---|
| cp_rest_or_ongoing | PARTLY SUPPORTED | 2021 chest pain, call 9-1-1 (Pt 3) |
| cp_with_alarm_symptoms | PARTLY SUPPORTED | Pt 2 |
| cp_ecg_ischemia | NO SOURCE FOUND (tier) | Pt 4-5 |
| cp_dissection_pe | PARTLY SUPPORTED | Pt 8 |
| cp_new_or_worsening_exertional | NO SOURCE FOUND (tier); regex lacks exertion | Pt 1 |
| chest_pain tests: ecg | CONFIRMED | Pt 4 |
| chest_pain tests: lipids/a1c/kidney | NO SOURCE FOUND | |
| chest_pain tests: stress_or_ccta | CONFIRMED | Pt 10 |
| chest_pain decision facts (risk, known CAD, women symptoms) | CONFIRMED | Pt 1,2,6,10 |
| chest_pain kidney/contrast | NO SOURCE FOUND | |
| er_precautions | CONFIRMED | Pt 3 |
| palp red flags (syncope, chest pain, unstable, stroke, WPW) | NO SOURCE FOUND | |
| palp_new_af_rvr, palp_heart_failure_signs | NO SOURCE FOUND | |
| AF CHA2DS2-VASc "2+ men / 3+ women" | CONTRADICTED (2019 numbers; 2023 annual-risk based) | 2023 AF |
| AF bleeding-risk why-text | CONFIRMED | 2023 AF |
| risk_factor_modification | CONFIRMED | 2023 AF |
| cut_caffeine_alcohol | PARTLY (alcohol yes; caffeine: no AF source, but caffeine is a BP-interfering substance) | 2023 AF; BP Table 11 |
| AF thyroid "treat first" | NO SOURCE FOUND | |
| AF tests | NO SOURCE FOUND; echo PARTLY (ESC 2024) | |
| hf_ntprobnp_over_2000 | CONFIRMED (verified against full text) | NG106 1.2.3 (UK) |
| hf_ntprobnp_400_2000 | CONFIRMED (verified) | NG106 1.2.4 |
| NT-proBNP <400 text | CONFIRMED (verified) | NG106 1.2.5-1.2.6 |
| NT-proBNP "raised by age>70, AFib, eGFR<60" | CONTRADICTED vs NICE (verified) | NG106 1.2.7 |
| NT-proBNP "lowered by obesity BMI>35, drugs" | PARTLY (verified) | NG106 1.2.7 |
| HF tests (ecg, cxr, renal, tsh, liver, lipids, a1c, cbc, urinalysis) | CONFIRMED (verified) | NG106 1.2.12 |
| HF iron_studies | PARTLY (HFrEF management) | NG106 1.4.5; 2022 HF unverified |
| hf_breathless_rest, hf_chest_pain, hf_syncope, hf_rapid_weight_gain | NO SOURCE FOUND | |
| limit_salt | CONTRADICTED by NICE (verified 1.9.10); US sodium rec unverified; CONFLICT: BP 5.1 rec 4 vs NICE 1.9.11 on K salt substitutes (NICE kept, clinician to review) | NG106 1.9.10-1.9.11; BP 5.1 |
| daily_weights, diuretic_by_specialist | NO SOURCE FOUND | |
| review_hf_worsening_meds | PARTLY SUPPORTED: diltiazem/verapamil CONFIRMED (BP Table 13, 5.3.4.1; NG106 1.4.12); NSAIDs, pioglitazone NO SOURCE FOUND | |
| amlodipine ankle swelling (hook + fact) | CONFIRMED (verified against full text) | BP Table 13; Table 17 |
| prior-MI fast-track review note | CONFIRMED not in NG106 (verified) | |
| bp_emergency | PARTLY; threshold should be > not >= (verified) | BP 6.2 + Fig 9 |
| bp_severe_no_symptoms | PARTLY (outpatient, 4-week follow-up; verified) | BP 6.2 + Fig 9 |
| bp_low_potassium (urgent) | CONTRADICTED as urgency (verified) | BP 3.2.3.1 rec 1 |
| BP goal <130/80 | CONFIRMED (verified) | BP 5.2.7 |
| resistant definition | CONFIRMED (verified) | BP 5.6 + Fig 8 |
| BP initial labs | CONFIRMED (verified) | BP 3.1.2 + Table 6 |
| out_of_office_bp, home_bp_log | CONFIRMED (verified) | BP 3.1.4 (COR 1, A); 3.2.2 (white-coat, COR 2a) |
| adherence_check | CONFIRMED (verified) | BP 5.2.5 |
| aldosterone_renin | CONFIRMED (verified) | BP 3.2.3.1 rec 1 |
| review_interfering_meds | CONFIRMED (verified) | BP 3.2.3 + Table 11 |
| PA -> endocrinology/HTN specialist | CONFIRMED (verified) | BP 3.2.3.1 rec 5 |
| nephrology / subspecialty routing | PARTLY (verified) | BP 5.6 + Fig 8 |
| LDL "190+" | NO SOURCE FOUND | |
| LDL goals/add-on | CONFIRMED vs 2026 summary (2018 superseded) | 2026 Dyslipidemia |
| ecg_high_grade_block | CONFIRMED (pacing regardless of symptoms); tier judgment | 2018 brady |
| ecg_high_grade_block_symptomatic | NO SOURCE (tier); bifascicular/2:1 questionable | |
| ecg_very_slow_symptomatic | NO SOURCE; regex bug | |
| ecg_new_lbbb | NO SOURCE FOUND; echo CONFIRMED | 2018 brady |
| ecg_long_qt (QTc 500) | PARTLY (2010 excerpt; inpatient) | 2010 TdP |
| low_concern first-degree AVB / Mobitz I / RBBB | CONFIRMED / PARTLY / NO SOURCE | 2018 brady |
| sleep apnea fact | CONFIRMED | 2018 brady |
| select_charts thresholds | NO SOURCE FOUND | selection-rules.md |
| CLAUDE.md hooks | see selection-rules.md | |
| Scorecard targets | NO SOURCE FOUND (external benchmark) | |

## Needs a cardiologist
Tier mapping for new/worsening chest pain, ECG-ischemia flag, fast AF, severe HTN without symptoms (guideline: 4-week outpatient), QTc>=500 asymptomatic; heart-block regex membership; salt advice and potassium salt-substitute conflict (UK vs US); CHA2DS2-VASc vs CHA2DS2-VA; Lp(a)/2026 lipid updates; ancestry for NT-proBNP.
