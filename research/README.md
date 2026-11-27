# Lantern research index - guideline fact-check of pathways/cardiology.json v0.3-draft

Verdicts: CONFIRMED / CONTRADICTED / PARTLY SUPPORTED / NO SOURCE FOUND. NO SOURCE FOUND = no source in the checked material settles the item (not "wrong"). "Full text" = checked against the complete guideline text. Section/table numbers are given only where checked against full text; otherwise "Pt n" refers to the numbered points of the ACC Ten Points summary.

BP refs (2025 AHA/ACC BP guideline, Circulation 2025;152:e114-e218) were re-verified against the full text on 2026-11-26 and all matched: 1.4; 3.1.2 + Table 6; 3.1.4; 3.2.2; 3.2.3 + Tables 10-11; 3.2.3.1 rec 1 and rec 5; 5.1 rec 4; 5.2.5; 5.2.7; 5.3.4.1; 5.6 + Fig 8; 6.2 + Fig 9; Tables 13, 17.

## Index of files
- chest-pain.md - chest pain flags, tests, options (2021 AHA/ACC)
- afib.md - palpitations / AFib (2023 ACC/AHA/ACCP/HRS)
- heart-failure.md - HF symptoms (NICE NG106, 2022 AHA/ACC/HFSA)
- hypertension-cholesterol.md - BP (2025 AHA/ACC) and cholesterol (2026 supersedes 2018)
- conduction-qt.md - abnormal ECG: conduction (2018) and QT (2010)
- selection-rules.md - select_charts.py thresholds, CLAUDE.md hooks, scorecard targets
- recency-windows.md - how long a prior test result stays "already done", per test, with what makes an older result stale
- econsult-questions.md - what PCPs ask cardiology in eConsults (Chan, Liddy, Keely et al. 2018): question types used for note style and the label `question_type`

## What each guideline was checked against
| Guideline / source | Region, year | Checked against | Not yet checked |
|---|---|---|---|
| NICE NG106 Chronic heart failure in adults | UK, updated 3 Sep 2025 | Full text: recommendations 1.1-1.12, Terms used (incl. 1.7.4 monitoring) | - |
| NICE QS9 Chronic heart failure quality standard | UK | - | Entire document |
| 2025 AHA/ACC High Blood Pressure guideline | US, 2025 | Full text; ACC Ten Points; ACC journal scan; 2 Minute Medicine; NephJC; Medical Dialogues | - |
| 2021 AHA/ACC Chest Pain guideline | US, 2021 | ACC Ten Points; AAFP 2023 summary; ACC imaging takeaways 2022; ACC contrast-media article 2025 | Full text: recommendation numbers, outpatient labs, CKD/contrast wording |
| 2023 ACC/AHA/ACCP/HRS AF guideline | US, 2023 | ACC Ten Points; ACC Cardiology Magazine primer 2024; ACC news summary; Europace review of 2024 ESC AF | Full text: initial evaluation, unstable AF, WPW, rate control, monitoring |
| 2022 AHA/ACC/HFSA HF guideline | US, 2022 | Full text (sections 1-14, Tables 1-33) | - |
| 2018 ACC/AHA/HRS Bradycardia guideline | US, 2018 | ACC news summary | Full text and ACC Ten Points |
| 2010 AHA/ACCF Torsade de Pointes statement | US, 2010 | Secondary excerpts of the summary table | Full text |
| 2018 AHA/ACC Cholesterol guideline (superseded) | US, 2018 | AAFP 2019 summary (lipid repeat intervals) | Full text |
| 2026 ACC/AHA Dyslipidemia guideline | US, 2026 | ACC journal scan | Full text |
| 2020 ACC/AHA Valvular Heart Disease guideline | US, 2020 | ACC Key Perspectives Part 1 | Surveillance-interval tables |
| ADA Standards of Care 2025, section 6 | US, 2025 | Recommendation 6.2 (PMC copy) | 2026 edition |
| 2016 AHA statement Drugs That May Cause or Exacerbate HF | US, 2016 | - | Entire document |
| KDIGO 2024 CKD guideline | International, 2024 | 2 Minute Medicine summary | Primary text; Figure 13 monitoring grid |
| FDA NSAID Drug Safety Communication | US, 9 Jul 2015 | ASA reproduction of the notice | fda.gov original |
| Pioglitazone (Actos) labeling | US | Takeda 2007 label-revision announcement | Current prescribing information |
| ATA TSH reference-range summary | US, 2018 | ATA Clinical Thyroidology for the Public | - |
| CredibleMeds QTdrugs List | US | Home page | Individual drug categories |
| ESC 2024 HTN, 2024 CCS, 2021/2023/2026 HF | EU | - | All (only the 2024 ESC AF review checked) |

## Superseded / catalog problems
| Source key | Finding |
|---|---|
| aha_bp_2017_2025 | 2017 guideline retired and replaced by 2025. Cite only 2025 (Circulation 2025;152:e114-e218; DOI 10.1161/CIR.0000000000001356). |
| aha_chol_2018 | SUPERSEDED by the 2026 ACC/AHA Dyslipidemia guideline (13 Mar 2026). |
| nice_ng106 "(2018)" | Updated 3 Sep 2025. |
| nice_qs9 | Compare cited NG106 rec numbers to NG106 (1.2.3 = >2000; 1.2.4 = 400-2000). |
| aha_qt_2010 | No replacement identified; inpatient statement, weak fit for outpatient triage. |
| acc_brady_2018, aha_chest_pain_2021, acc_afib_2023, aha_hf_2022 | Titles correct, still current. |

## Summary table (key = pathway item id; ref where known)
| id | Verdict | Ref |
|---|---|---|
| cp_rest_or_ongoing | PARTLY SUPPORTED | Chest pain 2021 Pt 3 |
| cp_with_alarm_symptoms | PARTLY SUPPORTED | Pt 2; AAFP 2023 |
| cp_ecg_ischemia | NO SOURCE FOUND (tier) | Pt 4-5 |
| cp_dissection_pe | PARTLY SUPPORTED | Pt 8 |
| cp_new_or_worsening_exertional | NO SOURCE FOUND (tier); regex lacks exertion | Pt 1 |
| chest_pain tests: ecg | CONFIRMED (incl. within 10 min) | Pt 4; AAFP 2023 |
| chest_pain tests: lipids/a1c/kidney | NO SOURCE FOUND | |
| chest_pain tests: stress_or_ccta | CONFIRMED | Pt 10; ACC imaging 2022 |
| chest_pain decision facts (risk, known CAD, women, prior tests) | CONFIRMED | Pt 1,2,6,10; ACC imaging 2022 |
| chest_pain kidney/contrast | PARTLY SUPPORTED | ACC contrast article 2025 |
| er_precautions | CONFIRMED | Pt 3 |
| review_bp_lipid_meds (chest pain) | NO SOURCE FOUND | |
| palp red flags (syncope, chest pain, unstable, stroke, WPW) | NO SOURCE FOUND | |
| palp_new_af_rvr, palp_heart_failure_signs | NO SOURCE FOUND | |
| AF CHA2DS2-VASc "2+ men / 3+ women" | CONTRADICTED (2019 numbers; 2023 annual-risk based; Class 2a for men 1 / women 2) | 2023 AF; ACC primer |
| AF CHA2DS2-VASc component list | NO SOURCE FOUND (ESC uses CHA2DS2-VA) | |
| AF bleeding-risk why-text; antiplatelet | CONFIRMED | 2023 AF Ten Points |
| risk_factor_modification | CONFIRMED | 2023 AF Ten Points |
| cut_caffeine_alcohol | PARTLY (alcohol yes; caffeine no AF source) | 2023 AF; BP Table 11 |
| AF thyroid "treat first" | NO SOURCE FOUND | |
| AF tests (ecg/tsh/lytes/kidney/liver/cbc/monitor) | NO SOURCE FOUND; echo PARTLY (ESC 2024) | |
| hf_ntprobnp_over_2000 | CONFIRMED (full text) | NG106 1.2.3 (UK) |
| hf_ntprobnp_400_2000 | CONFIRMED (full text) | NG106 1.2.4 |
| NT-proBNP <400 text | CONFIRMED (full text) | NG106 1.2.5-1.2.6 |
| NT-proBNP "raised by age>70, AFib, eGFR<60" | CONTRADICTED vs NICE | NG106 1.2.7 |
| NT-proBNP "lowered by obesity BMI>35, drugs" | PARTLY SUPPORTED | NG106 1.2.7 |
| HF tests (ecg, cxr, renal, tsh, liver, lipids, a1c, cbc, urinalysis) | CONFIRMED (full text) | NG106 1.2.12 |
| HF electrolytes | NO SOURCE FOUND | |
| HF iron_studies | PARTLY SUPPORTED (HFrEF; ferritin/TSAT definition) | NG106 1.4.5; ACC iron 2022 |
| hf_breathless_rest, hf_chest_pain, hf_syncope, hf_rapid_weight_gain | NO SOURCE FOUND | |
| limit_salt | CONTRADICTED by NICE (1.9.10); US PARTLY SUPPORTED; conflict BP 5.1 rec 4 vs NICE 1.9.11 | NG106; 2022 HF summary; 2025 BP |
| daily_weights, diuretic_by_specialist | NO SOURCE FOUND | |
| review_hf_worsening_meds | PARTLY SUPPORTED: diltiazem/verapamil, pioglitazone, NSAIDs CONFIRMED; amlodipine is edema, not HF worsening | NG106 1.4.12; BP Table 13; Takeda 2007; FDA DSC 2015 |
| amlodipine ankle swelling (hook + fact) | CONFIRMED (full text) | BP Table 13; Table 17 |
| prior-MI fast-track review note | CONFIRMED not in NG106 | |
| HF not_seen: kidney disease | PARTLY SUPPORTED | NG106 1.6.2 |
| bp_emergency | PARTLY; threshold should be > not >= | BP 6.2 + Fig 9 |
| bp_severe_no_symptoms | PARTLY (outpatient, 4-week follow-up) | BP 6.2 + Fig 9 |
| bp_low_potassium (urgent) | CONTRADICTED as urgency | BP 3.2.3.1 rec 1 |
| BP goal <130/80; resistant definition | CONFIRMED | BP 5.2.7; 5.6 + Fig 8 |
| BP initial labs | CONFIRMED | BP 3.1.2 + Table 6 |
| out_of_office_bp, home_bp_log | CONFIRMED | BP 3.1.4; 3.2.2 |
| adherence_check | CONFIRMED | BP 5.2.5 |
| aldosterone_renin | CONFIRMED | BP 3.2.3.1 rec 1 |
| review_interfering_meds | CONFIRMED | BP 3.2.3 + Table 11 |
| PA -> endocrinology/HTN specialist | CONFIRMED | BP 3.2.3.1 rec 5 |
| nephrology / subspecialty routing | PARTLY SUPPORTED | BP 5.6 + Fig 8 |
| LDL "190+" | NO SOURCE FOUND | |
| LDL goals/add-on | CONFIRMED vs 2026 summary (2018 superseded) | 2026 Dyslipidemia |
| ecg_high_grade_block | CONFIRMED (pacing regardless of symptoms); tier judgment | 2018 brady |
| ecg_high_grade_block_symptomatic | NO SOURCE (tier); bifascicular/2:1 questionable | |
| ecg_very_slow_symptomatic | NO SOURCE; regex issue | |
| ecg_new_lbbb | NO SOURCE FOUND; echo CONFIRMED | 2018 brady |
| ecg_long_qt (QTc 500) | PARTLY SUPPORTED (inpatient context) | 2010 TdP |
| low_concern first-degree AVB / Mobitz I / RBBB | CONFIRMED / PARTLY / NO SOURCE | 2018 brady |
| sleep apnea fact | CONFIRMED | 2018 brady |
| TSH_NORMAL | PARTLY SUPPORTED (lab-dependent) | ATA 2018 |
| POTASSIUM_LOW 3.5 | NO SOURCE FOUND | |
| EGFR_LOW 60 | CONFIRMED (persistence >3 months) | KDIGO 2024 summary |
| other select_charts rules | NO SOURCE FOUND | selection-rules.md |
| CLAUDE.md hooks | see selection-rules.md | |
| Scorecard targets | NO SOURCE FOUND (external benchmark) | |
| Recency windows (valid_days per test) | stress_or_ccta CONFIRMED; lipids, a1c, tsh, urinalysis, UACR, kidney panel, K, calcium, glucose, CBC PARTLY SUPPORTED; ECG, NT-proBNP, liver, iron, echo, monitor, aldosterone/renin, chest X-ray, out-of-office BP NO SOURCE FOUND for the number | recency-windows.md; NG106 1.7.4; BP 3.1.2; ADA 6.2; ACC imaging 2022 |

## Needs a cardiologist
Tier mapping for new/worsening chest pain, ECG-ischemia flag, fast AF, severe HTN without symptoms (guideline: 4-week outpatient), QTc >=500 asymptomatic; heart-block regex membership; salt advice and potassium salt-substitute conflict (UK vs US); CHA2DS2-VASc vs CHA2DS2-VA; Lp(a)/2026 lipid updates; ancestry for NT-proBNP; whether recency windows should be fixed numbers or tied to symptom/medication change.
