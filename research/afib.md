# Palpitations / AFib - fact-check (2023 ACC/AHA/ACCP/HRS AF guideline, US)

Guideline: 2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation (Circulation 2023). Title in `sources.acc_afib_2023` is CORRECT. Not superseded (errata exist; a 2026 AHA/ACC "quality measures" document appeared but is not a guideline).

## Checked against
- ACC, "2023 Guideline for Diagnosis and Management of Atrial Fibrillation: Key Perspectives" (Ten Points), 2023 - https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2023/11/27/19/46/2023-acc-guideline-for-af-gl-af
- Rienstra et al., "Ten novel aspects of the 2024 ESC AF guidelines", Europace 2024 - https://pmc.ncbi.nlm.nih.gov/articles/PMC11666470
- Not yet checked: guideline full text. Initial workup (TSH, echo, ECG), red flags and pre-excitation items are therefore NO SOURCE FOUND for the US guideline.

## Verdicts

| id | Verdict | Notes |
|---|---|---|
| decision_facts "Stroke-risk factors" why-text: "yearly stroke risk ~2%+ (roughly score 2+ in men, 3+ in women)" | CONTRADICTED (outdated numbers) | 2023 Ten Points: anticoagulation recommendations are driven by estimated annual thromboembolic risk with a validated score (CHA2DS2-VASc, ATRIA, GARFIELD-AF); "risk of 2% or more" -> stroke-prevention therapy; <2% = "intermediate". The 2 (men)/3 (women) cut-offs are the 2019 update; in 2023 men 1 / women 2 were upgraded to Class 2a (from 2b) - that class detail comes from a secondary summary, not the checked ACC page, so treat as likely but verify. Suggested wording: drop the numeric score thresholds, say "about 2%/yr or more; lower-risk scores are shared decision" - cardiologist to word. |
| anticoag facts: CHA2DS2-VASc components (age, sex, HF, HTN, diabetes, stroke/TIA/clot, vascular disease) | NO SOURCE FOUND (in checked text) | Component list is the standard score but the Ten Points page doesn't enumerate it. ESC 2024 (Europace review) uses CHA2DS2-VA (sex dropped): DOAC advised at >=2, "consider" at 1. US 2023 still lists CHA2DS2-VASc as one endorsed option. Flag US/EU difference. |
| "Bleeding-risk factors" why-text: fix modifiable ones rather than withhold | CONFIRMED | Ten Points: "Bleeding risk scores should not be used in isolation to determine eligibility for oral anticoagulation." Use them to identify and modify risk factors. |
| bleeding facts: antiplatelet/NSAID | PARTLY SUPPORTED | Ten Points: aspirin alone or +clopidogrel is not recommended as an alternative to OAC (without another indication); OAC alone preferred over OAC+antiplatelet in chronic coronary disease. NSAID/alcohol as bleeding factors: not in the checked text. |
| "Already on blood thinner? (INR)" | PARTLY SUPPORTED | Ten Points: DOACs preferred over warfarin except mitral stenosis or mechanical valve. INR only relevant for warfarin; consider adding `valve_disease` to anticoag_decision facts (judgment: mitral stenosis/mechanical valve decide DOAC vs warfarin). |
| "AFib drivers" / option risk_factor_modification | CONFIRMED | Ten Points: weight loss (BMI >27 kg/m2), exercise toward 210 min/week, minimize/eliminate alcohol, optimal BP control, screen for sleep-disordered breathing, tobacco cessation. |
| option cut_caffeine_alcohol | PARTLY SUPPORTED | Alcohol: CONFIRMED (above). Caffeine: NO SOURCE FOUND in the checked material. |
| Thyroid group "overactive thyroid causes AFib and should be treated first" | NO SOURCE FOUND | Not stated in the checked summary. Also affects CLAUDE.md hook "abnormal TSH -> check thyroid first". |
| tests_first: ecg, tsh, electrolytes, kidney, liver, cbc | NO SOURCE FOUND | Not stated in the checked summary. |
| tests_first: echo | PARTLY SUPPORTED | ESC 2024 (Europace review): echocardiogram recommended for all AF patients where it might guide treatment. US full text not checked. |
| tests_first: ambulatory_monitor | NO SOURCE FOUND | Ten Points not covering; ESC review covers screening only. |
| red flags palp_syncope, palp_chest_pain, palp_fast_low_bp, palp_stroke_symptoms, palp_preexcitation (emergent) | NO SOURCE FOUND | The checked summary does not cover unstable AF/cardioversion or WPW. Clinically these are standard "send to ER" items but no source in the checked material. Code note: "tia" substring in palp_stroke_symptoms will match words such as "tia" inside other words only if tokenised loosely - check matcher uses word boundaries. |
| urgent: palp_new_af_rvr, palp_heart_failure_signs | NO SOURCE FOUND | No guideline tier/time frame found. Heart-rate cutoffs: the regex has none besides "rate 1"; there is no numeric threshold in sources. Judgment for cardiology. |
| rate-control facts (HF, BP, COPD) "beta-blocker caution mainly asthma" | NO SOURCE FOUND | Already flagged in the pathway for clinician. |
| subspecialty: electrophysiology | NO SOURCE FOUND | Routing is Lantern/clinician judgment. |

## For cardiologist review
- Reword the CHA2DS2-VASc "why" text (above).
- Whether Lantern computes the score or lists parts (already in review_notes). If it computes, decide CHA2DS2-VASc (US) vs CHA2DS2-VA (ESC).
- Is "new AFib with fast rate" urgent vs emergent; is there a heart-rate cut-off.
