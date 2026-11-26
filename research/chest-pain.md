# Chest pain - fact-check (2021 AHA/ACC multisociety Chest Pain guideline, US)

Guideline: 2021 AHA/ACC/ASE/CHEST/SAEM/SCCT/SCMR Guideline for the Evaluation and Diagnosis of Chest Pain, Circulation 2021;144:e368 (JACC 78:e187). Catalog title in `sources.aha_chest_pain_2021` is correct. No newer version identified.

## Checked against
- ACC, "2021 AHA/ACC Chest Pain Guideline Perspectives" (Ten Points to Remember), 2021 - https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2021/10/27/14/06/2021-guideline-for-chest-pain-gl_chestpain
- AAFP, "Chest Pain Evaluation: Updated Guidelines From the AHA/ACC", American Family Physician 2023 - https://www.aafp.org/afp/2023/0200/practice-guidelines-chest-pain-evaluation
- ACC, "Key Imaging Takeaways From the 2021 Chest Pain Guidelines", 2022 - https://www.acc.org/latest-in-cardiology/articles/2022/03/14/11/34/key-imaging-takeaways-from-the-2021-chest-pain-guidelines
- ACC, "Contrast Media in Advanced Cardiovascular Imaging: Clinical Questions and Shifting Paradigms", 2025 - https://www.acc.org/Latest-in-Cardiology/Articles/2025/07/28/17/07/Contrast-Media-in-Advanced-Cardiovascular-Imaging (not a guideline; cites the 2021 guideline)
- Guideline full text (recommendation numbers, outpatient lab section): not yet checked. Recommendation numbers below are therefore "Pt n" of the ACC Ten Points.

## Verdicts (key = pathway id)

| id | Verdict | Notes |
|---|---|---|
| cp_rest_or_ongoing (emergent) | PARTLY SUPPORTED | Ten Points Pt 3: patients with acute chest pain should "call 9-1-1" for EMS transport to the nearest ED. The guideline does not define an "emergent tier" or the phrase "at rest"; tier mapping is Lantern's. |
| cp_with_alarm_symptoms (emergent) | PARTLY SUPPORTED | Pt 2: accompanying symptoms (nausea, palpitations, shortness of breath) are common in ACS. AAFP 2023: women, people with diabetes and older patients more often present with nausea, fatigue or shortness of breath. No specific "sweating/fainting" rule found. Cardiologist to confirm. |
| cp_ecg_ischemia (emergent) | NO SOURCE FOUND (for the tier) | Pt 4: ECG key to assess ACS; Pt 5: serial high-sensitivity troponin preferred. AAFP 2023: repeat ECG if first normal but suspicion high. Whether ST changes in a referral note are emergent when pain has resolved is a judgment call (also in `review_notes`). |
| cp_dissection_pe (emergent) | PARTLY SUPPORTED | Pt 8 lists aortic syndrome and pulmonary embolism among nonischemic causes. No tier guidance. |
| cp_new_or_worsening_exertional (urgent) | NO SOURCE FOUND (for 2-week tier) | Pt 1 defines acute chest pain as "new onset or change from previous in pattern, intensity, or duration" - so new/worsening pain is acute chest pain in this guideline's terms. Mapping it to "urgent specialist within ~2 weeks" is a judgment call. Code note: the regex requires "chest pain" + "new/worsening" but not an exertion term. |
| tests_first: ecg | CONFIRMED | Pt 4 (ECG in acute and stable chest pain). AAFP 2023: 12-lead ECG "recommended within 10 minutes of arrival in clinic and emergency settings". |
| tests_first: lipids, a1c, kidney_panel | NO SOURCE FOUND | The checked summaries do not list outpatient laboratory tests for chest pain (AAFP states it does not address outpatient labs). Guideline full text not yet checked. |
| tests_first: stress_or_ccta (not pre-checked) | CONFIRMED | Pt 10 and ACC imaging takeaways: low-risk stable pain without known CAD -> CAC or exercise ECG reasonable first line; intermediate/high risk -> CCTA or stress imaging; known obstructive CAD -> stress imaging; prior CABG -> CCTA or stress imaging. AAFP: CCTA preferred in intermediate/high risk under 65; stress testing favoured at 65+ or when more obstructive disease suspected. Choice depends on risk, so leaving it unchecked ("chosen by cardiology") is consistent. |
| decision_facts "Heart risk factors" | CONFIRMED | Pt 6/10: structured risk assessment / pretest-probability using age, sex, symptoms decides whether testing can be deferred. |
| decision_facts "Known coronary disease" | CONFIRMED | Pt 10 branches on known obstructive CAD, nonobstructive CAD, no known CAD; ACC imaging takeaways repeat this. |
| decision_facts "Accompanying symptoms, especially women" | CONFIRMED | Pt 2; AAFP 2023 and ACC imaging summary: guideline recommends a history emphasising accompanying symptoms more common in women, and warns risk tools can underestimate risk in women. |
| decision_facts "Previous ECG, stress test, coronary CT or angiogram" | CONFIRMED | ACC imaging takeaways / AAFP: normal CCTA has about a 2-year "warranty", normal stress test about 1 year; inconclusive CCTA -> stress imaging reasonable; equivocal stress test -> anatomic testing indicated. |
| decision_facts "Kidney function (contrast)" | PARTLY SUPPORTED | ACC 2025 contrast-media article: risk of IV iodinated contrast kidney injury is "low" in stable patients but "uncertain" with eGFR <30; estimated incidence 0% at eGFR >=45, 0-2% at 30-44, 0-17% at <30; uncertainty "makes IV contrast use in these populations a relative contraindication". The 2021 chest pain guideline's own wording on CKD and CCTA has not been checked; the AAFP and imaging summaries do not discuss it. |
| review_notes "uses cardiac/possibly cardiac/noncardiac" | CONFIRMED | Pt 1: "Chest pain should be described as cardiac, possibly cardiac, or noncardiac rather than as typical or atypical." |
| option er_precautions | CONFIRMED | Pt 3. |
| option review_bp_lipid_meds | NO SOURCE FOUND | Not stated in the checked chest-pain material. |
| not_seen: low-risk patient, no further testing | CONFIRMED | Pt 8/10; AAFP: for stable pain, low-risk patients "need no further testing". |
| not_seen: MSK / reflux | NO SOURCE FOUND | Pt 8 lists nonischemic causes; MSK/GI wording not found. |

## ESC comparison
2024 ESC Chronic Coronary Syndromes guideline: not yet checked.

## For cardiologist review
- Where "new or worsening" chest pain belongs (urgent referral vs same-day evaluation).
- Whether an "ECG ischemia" flag should be emergent only when pain is current.
- Whether lipids/A1c/kidney panel belong pre-checked for chest pain referrals.
