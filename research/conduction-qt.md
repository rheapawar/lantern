# Abnormal ECG - conduction and QT (2018 ACC/AHA/HRS Bradycardia guideline; 2010 AHA/ACCF TdP statement; US)

## Source status
- 2018 ACC/AHA/HRS Guideline on the Evaluation and Management of Patients With Bradycardia and Cardiac Conduction Delay (Kusumoto; Circulation 2019;140:e382; JACC 74:e51). Catalog title lacks "Evaluation and Management of Patients With" (cosmetic). No newer version found. Checked against a news summary only: ACC, "New Guideline Outlines Recommendations for Evaluating, Managing Bradycardia", 2018 - https://www.acc.org/Latest-in-Cardiology/Articles/2018/11/06/12/42/New-in-Clinical-Documents-New-Guideline-Outlines-Recommendations-For-Evaluating-Managing-Bradycardia (no class/LOE, no BBB, no Mobitz I, no monitoring). Guideline full text not yet checked.
- 2010 AHA/ACCF Scientific Statement, Prevention of Torsade de Pointes in Hospital Settings (Drew; Circulation 2010;121:1047). Title in catalog is correct. Checked against secondary summaries only (lower confidence); full text not yet checked. No newer replacement found (search not exhaustive). Scope is HOSPITALIZED patients - not outpatient referral triage.

## Verdicts

| id | Verdict | Notes |
|---|---|---|
| ecg_high_grade_block (urgent) / text "pacemaker usually indicated" | CONFIRMED (substance) | ACC summary: for acquired Mobitz II, high-grade or third-degree AV block not due to reversible/physiologic cause, "permanent pacing is recommended regardless of symptoms". Tier (urgent vs emergent, timing) is not in the guideline - judgment. |
| ecg_high_grade_block_symptomatic (emergent) | NO SOURCE FOUND (tier) | Symptomatic high-grade block -> emergent is clinically common but not cited. Regex includes "bifascicular", "trifascicular" and "2:1 block": bifascicular/trifascicular block is not high-grade AV block, and 2:1 block can be Mobitz I or II - judgment call; consider removing from the emergent match. |
| ecg_very_slow_symptomatic | NO SOURCE FOUND | No numeric "very slow" rate in the checked text. Code note: regex fragments "heart rate 3" / "hr 3" also match 300+ (tachycardia) and "heart rate 4" matches 40s (not very slow). |
| ecg_active_mi | NO SOURCE FOUND (this guideline) | Belongs to chest-pain/ACS guidelines (see chest-pain.md). |
| ecg_new_lbbb (urgent) | NO SOURCE FOUND | Not stated in the checked text. Echo for conduction disease/LV function: ACC summary "echocardiography is usually the most appropriate initial screening test" for structural heart disease -> CONFIRMED for tests_first echo. Note: new LBBB with chest pain is also an ACS question (chest-pain flags only list ST/T changes) - ask cardiologist. |
| ecg_long_qt "QTc 500 or more is high risk" | PARTLY SUPPORTED | 2010 statement (secondary summary only): QTc >500 ms or an increase >=60 ms from baseline after starting a TdP-linked drug flag risk; "no threshold ... at which TdP is certain". Guideline says ">500", the regex catches 500 too (trivial). The statement concerns drug monitoring in hospital, not asymptomatic outpatient ECG referrals; the 2-week "urgent" tier is Lantern's call. The pathway already notes the 2018 bradycardia guideline does not cover long QT - correct. |
| decision_facts "QT-prolonging medicines", "Salts that worsen QT" | PARTLY SUPPORTED | Excerpt: risk factors for drug-induced TdP include hypokalemia and hypomagnesemia; non-QT-prolonging alternative preferred if equally effective. Calcium: NO SOURCE FOUND. Specific drug examples (citalopram, ondansetron...): not verified. |
| decision_facts "Sleep apnea" | CONFIRMED | ACC summary: nocturnal bradycardia alone is not a pacing indication; opportunity to screen for sleep apnea. |
| decision_facts "AV-nodal medicines (reversible cause)" | PARTLY SUPPORTED | ACC summary: pacing recommendation applies when cause is not reversible; drug review is implied. Specific list (beta blockers, diltiazem, verapamil, digoxin, amiodarone) not in the checked text. |
| tests_first: electrolytes, calcium, tsh | NO SOURCE FOUND | Not stated in the checked text. |
| tests_first: ambulatory_monitor | NO SOURCE FOUND | Plausible; not stated in the checked summary. |
| low_concern: first-degree AV block alone | CONFIRMED | ACC summary: for other AV block types (incl. asymptomatic first-degree) pacing considered only with symptoms correlating with block. |
| low_concern: Mobitz I without symptoms | PARTLY SUPPORTED | Falls under "all other AV block types" in the same sentence; Mobitz I not named in summary. |
| low_concern: isolated RBBB | NO SOURCE FOUND | |
| subspecialty general / EP | NO SOURCE FOUND | Routing: "high-grade AV block -> EP" is conventional but not from the checked text. |

## For cardiologist review
- Remove/keep bifascicular, trifascicular, 2:1 in the emergent block list; the heart-rate regex.
- Tier for QTc >=500 without symptoms; whether to cite the 2010 inpatient statement for an outpatient rule (consider whether the 2017/2022 arrhythmia guidelines are better sources - not checked).
