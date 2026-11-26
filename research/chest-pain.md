# Chest pain - fact-check (2021 AHA/ACC multisociety Chest Pain guideline, US)

Guideline: 2021 AHA/ACC/ASE/CHEST/SAEM/SCCT/SCMR Guideline for the Evaluation and Diagnosis of Chest Pain, Circulation 2021;144:e368 (JACC 78:e187). Title in `sources.aha_chest_pain_2021` is CORRECT. No newer version found.

## Checked against
- ACC, "2021 AHA/ACC Chest Pain Guideline Perspectives" (Ten Points to Remember), 2021 - https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2021/10/27/14/06/2021-guideline-for-chest-pain-gl_chestpain . A summary: it gives no recommendation numbers, ECG timing target, contrast/kidney or lab-panel advice, so those items below are NO SOURCE FOUND, not "wrong".
- Not yet checked: guideline full text.

## Verdicts (key = pathway id)

| id | Verdict | Notes |
|---|---|---|
| cp_rest_or_ongoing (emergent) | PARTLY SUPPORTED | Summary Pt 3: patients with acute chest pain should "call 9-1-1" for EMS transport to nearest ED. Guideline does not define an "emergent tier" or the words "at rest"; the tier mapping is Lantern's. |
| cp_with_alarm_symptoms (emergent) | PARTLY SUPPORTED | Pt 2: accompanying symptoms (nausea, palpitations, SOB) common in ACS. No specific "sweating/fainting" rule found in the checked summary. Cardiologist to confirm. |
| cp_ecg_ischemia (emergent) | NO SOURCE FOUND (for the tier) | Pt 4: ECG key to assess ACS; troponin (hs preferred, Pt 5). Whether an ST change in a referral note is emergent when pain has resolved is already in `review_notes`; judgment call. |
| cp_dissection_pe (emergent) | PARTLY SUPPORTED | Pt 8 names aortic syndrome and pulmonary embolism as nonischemic causes to consider. No tier guidance. |
| cp_new_or_worsening_exertional (urgent) | NO SOURCE FOUND (for 2-week tier) | Guideline defines acute chest pain as "new onset or change from previous in pattern, intensity, or duration" (Pt 1) - i.e. new/worsening pain is, by definition, ACUTE chest pain which the guideline evaluates in the ED/expedited pathway. Mapping it to "urgent specialist within ~2 weeks" is a judgment call for cardiologist review. Code note: the regex requires "chest pain"+"new/worsening" but does NOT require an exertion word, despite the text saying "with exertion". |
| tests_first: ecg | CONFIRMED | Pt 4: ECG important in both acute and stable chest pain. |
| tests_first: lipids, a1c, kidney_panel | NO SOURCE FOUND | Not stated in the checked summary. Plausible as risk-factor/contrast-safety labs but unverified. Needs the full text. |
| tests_first: stress_or_ccta (not pre-checked) | CONFIRMED | Pt 10: intermediate-high risk no known CAD -> CCTA or stress imaging; known obstructive CAD on GDMT -> stress imaging; low probability -> CAC may be first-line or testing deferred. Type depends on risk => leaving it unchecked / "chosen by cardiology" is consistent. |
| decision_facts "Heart risk factors" why-text | CONFIRMED | Pt 6/10: structured risk assessment / pretest probability model using age, sex, symptoms decides whether testing can be deferred. (Guideline wording is probability/"risk", not exactly "low/intermediate/high" for outpatients - Pt 8 uses low/intermediate/high for ED pathways.) |
| decision_facts "Known coronary disease" | CONFIRMED | Pt 10 splits recommendations by known obstructive CAD, known nonobstructive CAD, no known CAD. |
| decision_facts "Accompanying symptoms, especially women" | CONFIRMED | Pt 2: women more often have accompanying nausea, palpitations, SOB. |
| review_notes "uses cardiac/possibly cardiac/noncardiac, not typical/atypical" | CONFIRMED | Pt 1: "Chest pain should be described as cardiac, possibly cardiac, or noncardiac rather than as typical or atypical." |
| decision_facts "Kidney function (contrast)" | NO SOURCE FOUND | Contrast-nephropathy caution for CCTA/angiography is not stated in the checked summary. (Also CLAUDE.md hook "kidney disease -> contrast-dye tests".) Common clinical teaching; no source in the checked material. |
| decision_facts "Previous ECG, stress test..." | PARTLY SUPPORTED | Pt 10 branches on prior CAD/GDMT; "recent normal testing may change what is needed" not found in text. |
| er_precautions option | CONFIRMED | Pt 3: teach patients to call 9-1-1. |
| review_bp_lipid_meds option | NO SOURCE FOUND | Not stated in the checked text. See hypertension.md / cholesterol notes. |
| not_seen: low-risk patient, further testing may not be needed | CONFIRMED | Pt 8 and 10: low risk -> additional testing may not be needed / can be deferred. |
| not_seen: MSK / reflux | NO SOURCE FOUND | Pt 8 lists nonischemic causes but MSK/GI wording is not in the checked summary. |

## ESC comparison
2024 ESC Chronic Coronary Syndromes guideline - not checked; no claim made.

## For cardiologist review
- Where "new or worsening" chest pain belongs (urgent referral vs same-day evaluation).
- Whether an "ECG ischemia" flag should be emergent only when pain is current.
- Whether lipids/A1c/kidney panel belong pre-checked for chest pain referrals.
