# Abnormal ECG - conduction and QT (2018 ACC/AHA/HRS Bradycardia guideline; 2010 AHA/ACCF TdP statement; US)

## Checked against
- 2018 ACC/AHA/HRS Guideline on the Evaluation and Management of Patients With Bradycardia and Cardiac Conduction Delay (Kusumoto; Circulation 2019;140:e382; JACC 74:e51). No newer version identified. Checked: ACC, "New Guideline Outlines Recommendations for Evaluating, Managing Bradycardia", 2018 - https://www.acc.org/Latest-in-Cardiology/Articles/2018/11/06/12/42/New-in-Clinical-Documents-New-Guideline-Outlines-Recommendations-For-Evaluating-Managing-Bradycardia (news summary; no class/LOE; silent on bundle branch block, Mobitz I, monitoring). Guideline full text and ACC Ten Points not yet checked; recommendation numbers unavailable.
- 2010 AHA/ACCF Scientific Statement, Prevention of Torsade de Pointes in Hospital Settings (Drew; Circulation 2010;121:1047; JACC 55:934). No replacement identified (search not exhaustive). Scope is hospitalised patients, not outpatient triage. Full text not yet checked; points below rest on secondary excerpts of the statement's summary table.
- CredibleMeds (AZCERT) QTdrugs List - https://www.crediblemeds.org/ : the maintained reference list for QT-prolonging drugs (dynamic, updated regularly). Individual drug categories for the examples in the pathway not yet checked.

## Verdicts

| id | Verdict | Notes |
|---|---|---|
| ecg_high_grade_block (urgent) | CONFIRMED (substance) | ACC news summary: for acquired Mobitz II, high-grade or third-degree AV block not due to reversible/physiologic cause, "permanent pacing is recommended regardless of symptoms". Tier/timing not in the guideline - judgment. |
| ecg_high_grade_block_symptomatic (emergent) | NO SOURCE FOUND (tier) | Regex includes "bifascicular", "trifascicular", "2:1 block": bifascicular/trifascicular block is not high-grade AV block; 2:1 block can be Mobitz I or II. Judgment for cardiologist. |
| ecg_very_slow_symptomatic | NO SOURCE FOUND | No numeric "very slow" rate in checked material. Code: fragments "heart rate 3"/"hr 3" also match 300+; "heart rate 4" matches 40s. |
| ecg_active_mi | NO SOURCE FOUND (this guideline) | Belongs to chest-pain/ACS guidance (see chest-pain.md). |
| ecg_new_lbbb (urgent) | NO SOURCE FOUND | Echo: ACC summary "echocardiography is usually the most appropriate initial screening test" for structural heart disease -> CONFIRMED for tests_first echo. New LBBB with chest pain is also an ACS question - cardiologist. |
| ecg_long_qt (QTc >=500) | PARTLY SUPPORTED | 2010 statement summary table: QTc >500 ms, or increase >=60 ms from baseline after starting a TdP-linked drug, signals risk; "no threshold ... at which TdP is certain". Guideline says ">500"; regex catches 500. Hospital drug-monitoring context; the 2-week "urgent" tier is Lantern's. 2018 bradycardia guideline does not cover long QT. |
| decision_facts "QT-prolonging medicines", "Salts that worsen QT" | PARTLY SUPPORTED | 2010 summary: electrolyte disorders (especially hypokalemia, hypomagnesemia) are TdP risk factors; non-QT-prolonging alternative preferred if equally effective. Calcium: not stated in checked material. Drug examples (citalopram, ondansetron...): not yet checked against the QTdrugs List. |
| decision_facts "Sleep apnea" | CONFIRMED | ACC summary: nocturnal bradycardia alone is not a pacing indication; opportunity to screen for sleep apnea. |
| decision_facts "AV-nodal medicines" | PARTLY SUPPORTED | Pacing recommendation applies when cause is not reversible (ACC summary). Specific drug list not stated in checked material. |
| tests_first: electrolytes, calcium, tsh; ambulatory_monitor | NO SOURCE FOUND | Not stated in checked material. |
| low_concern: first-degree AV block | CONFIRMED | ACC summary: for other AV block types (incl. asymptomatic first-degree) pacing considered only with symptoms correlating with the block. |
| low_concern: Mobitz I | PARTLY SUPPORTED | Falls under "all other AV block types"; not named. |
| low_concern: isolated RBBB | NO SOURCE FOUND | |
| subspecialty general / EP | NO SOURCE FOUND | |

## For cardiologist review
- Keep/remove bifascicular, trifascicular, 2:1 in the emergent list; the heart-rate regex.
- Tier for QTc >=500 without symptoms; whether an inpatient statement is the right source for an outpatient rule.
