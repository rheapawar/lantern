# Palpitations / AFib - fact-check (2023 ACC/AHA/ACCP/HRS AF guideline, US)

Guideline: 2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation (Circulation 2023; JACC 2024;83:109-279; PMID 38033089). Catalog title in `sources.acc_afib_2023` is correct. Current (errata exist; a 2026 AHA/ACC AF "quality measures" document is not a guideline).

## Checked against
- ACC, "2023 Guideline for Diagnosis and Management of Atrial Fibrillation: Key Perspectives" (Ten Points), 2023 - https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2023/11/27/19/46/2023-acc-guideline-for-af-gl-af
- ACC Cardiology Magazine, "Focus on EP: A Practical Primer for the 2023 AFib Guideline", 2024 - https://www.acc.org/latest-in-cardiology/articles/2024/04/01/00/42/focus-on-ep-a-practical-primer-for-the-2023-afib-guideline
- ACC, "New ACC/AHA Guideline Focuses on Diagnosis, Management of AFib", 2023 - https://www.acc.org/Latest-in-Cardiology/Articles/2023/11/29/18/58/New-ACC-AHA-Guideline-Focuses-on-Diagnosis-Management-of-AFib-gl-af
- Rienstra et al., ten novel aspects of the 2024 ESC/EACTS AF guidelines, Europace 2024 - https://pmc.ncbi.nlm.nih.gov/articles/PMC11666470
- Guideline full text (initial-evaluation, unstable AF, WPW, rate-control sections): not yet checked; recommendation numbers unavailable.

## Verdicts

| id | Verdict | Notes |
|---|---|---|
| decision_facts "Stroke-risk factors" why-text: "~2%+ yearly (roughly score 2+ men, 3+ women)" | CONTRADICTED (outdated numbers) | Ten Points: recommendations are by estimated annual thromboembolic risk using a validated score (CHA2DS2-VASc, ATRIA, GARFIELD-AF); risk of 2% or more -> stroke-prevention therapy; below 2% = intermediate. ACC primer: anticoagulation is "more reasonable" for men with score 1 and women with score 2 (Class 2a in 2023, upgraded from 2b in 2019), described as intermediate annual risk 1-2%. The 2/3 cut-offs are the 2019 update. Suggested wording: drop numeric score thresholds. |
| anticoag facts: CHA2DS2-VASc components | NO SOURCE FOUND (component list) | Checked summaries endorse CHA2DS2-VASc but do not enumerate components. ESC 2024 uses CHA2DS2-VA (sex dropped): DOAC advised at >=2, consider at 1. US/EU difference flagged. |
| "Bleeding-risk factors" why-text | CONFIRMED | Ten Points: "Bleeding risk scores should not be used in isolation to determine eligibility for oral anticoagulation"; use them to identify/modify risk factors. |
| bleeding facts: antiplatelet | CONFIRMED | Ten Points / ACC primer: aspirin alone or with clopidogrel not recommended as alternative to OAC without another indication; antiplatelet continues when coronary/peripheral disease requires it; OAC alone preferred over OAC + antiplatelet in chronic coronary disease. |
| bleeding facts: NSAID, alcohol | NO SOURCE FOUND | Not stated in checked summaries. |
| "Already on blood thinner? (INR)" | PARTLY SUPPORTED | DOACs preferred over warfarin except mitral stenosis or mechanical valve (Ten Points). INR matters only for warfarin; consider adding `valve_disease` to anticoag_decision facts (judgment). |
| risk_factor_modification / "AFib drivers" | CONFIRMED | Ten Points: weight loss (BMI >27), activity toward 210 min/week, minimize/eliminate alcohol, optimal BP control, screen for sleep-disordered breathing, tobacco cessation. ACC news piece: stronger focus on weight loss, activity, smoking cessation, alcohol moderation, comorbidity management. |
| option cut_caffeine_alcohol | PARTLY SUPPORTED | Alcohol confirmed (above). Caffeine in AF: not stated in checked AF material. (Caffeine is listed as a BP-interfering substance, 2025 BP guideline Table 11.) |
| Thyroid "overactive thyroid causes AFib; treat first" | NO SOURCE FOUND | Not stated in checked AF material. |
| tests_first: ecg, tsh, electrolytes, kidney, liver, cbc | NO SOURCE FOUND | Initial-evaluation section of the guideline not yet checked. |
| tests_first: echo | PARTLY SUPPORTED | ESC 2024 (Europace review): echocardiogram for all AF patients where it might guide treatment. US text not yet checked. |
| tests_first: ambulatory_monitor | NO SOURCE FOUND | ACC primer: only a Class 2a recommendation for consumer devices to monitor recurrence in known AF. |
| red flags palp_syncope, palp_chest_pain, palp_fast_low_bp, palp_stroke_symptoms, palp_preexcitation | NO SOURCE FOUND | Unstable AF / cardioversion and pre-excitation sections not yet checked. Code note: confirm "tia" is matched with word boundaries. |
| urgent: palp_new_af_rvr, palp_heart_failure_signs | NO SOURCE FOUND | No tier/time-frame or numeric heart-rate threshold found. |
| rate-control facts (HF, BP, COPD); "beta-blocker caution mainly asthma" | NO SOURCE FOUND | Rate-control section not yet checked. |
| subspecialty electrophysiology | NO SOURCE FOUND | Routing is Lantern/clinician judgment. |

## For cardiologist review
- Reword the CHA2DS2-VASc "why" text.
- Whether Lantern computes the score or lists parts; if computing, CHA2DS2-VASc (US) vs CHA2DS2-VA (ESC).
- Whether new AFib with fast rate is urgent vs emergent; any heart-rate cut-off.
