# Writing the referral notes

You'll write **40 short referral notes**, the message a primary care doctor (PCP) sends when referring a patient to cardiology. Lantern reads each note plus the patient's chart and has to work out how urgent the case is, which tests to order first, and which clinic the patient belongs in. The notes are its test, so they need to read like real PCP notes. Some should be messy, and a few should under-call how sick the patient is.

All patients are synthetic (Synthea). There is no real patient data anywhere.

---

## For each case

1. Open `cases/<id>/chart_summary.md`. The top section, **Writing plan**, tells you what this note must do. The rest is everything the PCP could see on the referral date.
2. Write the note and save it as **`cases/<id>/referral.txt`** (plain text).
3. Move to the next case. Rhea re-runs `python3 build_cases.py` to load the notes.

Only open `chart_summary.md`. Don't open `bundle.json`, and don't open or fill in `label.json`; that's the answer key. In the summary, you can skip the "Tests first - already done?" section; it's for the labeller.

---

## Format

- **Plain text.** About 40–150 words; the `econsult_4_fields` style can run to ~200.
- **Written by the PCP on the referral date** in the summary. Write in the present tense, as if you saw the patient today.
- **No names.** Write "pt", "she", "58M", "72 yo woman". The Synthea names aren't needed.
- **End with the referral question**, e.g. "Please evaluate for ischemia", "Need for anticoagulation?", "Next step for BP?"
- **Numbers:** use the values in the summary, or the ones the plan gives you. Don't invent a lab that contradicts the chart.

## The four styles (the plan picks one)

| Style | Looks like |
|---|---|
| `standard` | 3–5 full sentences, a normal clinical note |
| `terse` | Fragments and abbreviations: "68F, CP on exertion x3 wks, worse. HTN, DM2. ECG NSR. ?ischemia, pls eval." |
| `rambling` | Long, chatty and a bit disorganised, with the key symptom buried in the middle |
| `econsult_4_fields` | Four labelled lines: **Patient:** / **Background:** / **Question:** / **Done so far:** |

## What real PCP questions look like

A study of 100 real cardiology eConsults from the Champlain BASE service (Chan, Johnson, Liddy, Keely et al., *Digital Health* 2018) sorted PCP questions into six types. The plan gives each case a **question type**. Write the note so it's clearly asking that kind of question.

| Question type (plan value) | Share of the 100 | What the PCP is asking (paraphrased from the paper's examples) |
|---|---|---|
| `test_interpretation` | 46 | "Is this result significant?" A new bundle branch block in someone with a past stent; a mildly enlarged aorta on CT; a slow heart rate on a Holter after episodes of light-headedness |
| `specific_workup_or_management` | 18 | One concrete step: which test before hip surgery in an 84-year-old; keep the ACE inhibitor when BP runs low; is a statin still needed after leg cramps |
| `guideline_exception` | 13 | The patient doesn't fit the usual rule: an older patient with diabetes, kidney disease and cirrhosis and new AFib (anticoagulate?); a risk calculator that says "no statin" but ignores another risk factor |
| `noncardiac_drug_in_cardiac_patient` | 13 | Is this non-heart drug safe for this heart: an antidepressant with a long QT; a stimulant with WPW |
| `concerns_despite_normal_tests` | ~4 | Symptoms keep happening although the tests were normal; asking for reassurance or the next step |
| `family_history_screening` | ~6 | A relative has an inherited heart condition; the patient is well (none in this test set yet) |
| `new_symptom_assessment` | not in the paper | Lantern's own addition: new or worsening symptoms that need a specialist to assess them |

The paper reports 4 and 6 for the last two types in one place and different numbers elsewhere; all six add up to 100.

**Patterns visible in the real questions:**
- They usually open with **age plus the one key fact**, e.g. "This 71-year-old with a previous stent has…", then give two or three supporting details and end with **one specific question**.
- Many patients have **several other conditions**, and the PCP is unsure which guideline applies. Some notes should read like that busy, multi-problem patient.
- **Mildly abnormal tests** found by chance prompt a lot of questions, often with a request for reassurance.

Paraphrase this style; don't copy the paper's sentences.

## What the note must contain

1. **"The note must convey"** from the plan, in your own words. Don't paste the plan sentence, and don't copy the flag wording from the summary. Real PCPs paraphrase.
2. **The negation**, if the plan lists one, worked in naturally ("denies chest pain at rest"). This checks that Lantern doesn't flag a symptom the patient doesn't have.
3. **One or two chart facts a PCP would naturally mention**, such as "known HTN on lisinopril". Not the whole problem list.

## What the note must NOT contain

- **Anything under "Do NOT mention".** That's the chart fact the case is testing (kidney disease, prior heart attack, a thyroid problem, amlodipine, an NSAID). Lantern has to find it in the chart on its own, so leave it out completely, including hints like "renal issues".
- **The future.** Write nothing the PCP couldn't know on that date: no later diagnoses and no results that come back afterwards.
- **The tier.** Never write "urgent", "routine" or "emergent" as a label. Show it through the symptoms.

## What each tier looks like in a note

| Tier | The note should show |
|---|---|
| **emergent** | ER-level symptoms: chest pain at rest or ongoing, fainting, breathless at rest or can't lie flat, very high BP with confusion or vision change, complete heart block with fainting. **Write it as the PCP under-calling it**: asking for an appointment rather than sending the patient to the ER. That's the case Lantern must catch. |
| **urgent** | Should be seen within ~2 weeks: new or worsening exertional chest pain, new AFib with a fast rate, fast weight gain with worsening swelling, new LBBB, Mobitz II, long QT, BP over 180/120 without symptoms. |
| **soon** | Within ~4–6 weeks. For now this is only the heart failure cases with an NT-proBNP of 400–2,000 written in the note. |
| **routine** | Stable, long-standing or reassuring; the patient is otherwise well. Many routine cases include a negation. |

## Three example notes

These patients are made up and match none of the 40 cases. Don't reuse the wording.

**Routine, `test_interpretation`, terse:**
> 66M, pre-op ECG for knee replacement shows RBBB, no prior ECG to compare. No CP, no SOB, no syncope. Walks 3 km daily. HTN on ramipril. Is this significant / does it change surgery? Thx.

**Urgent, `new_symptom_assessment`, standard:**
> This 59-year-old woman with type 2 diabetes and high cholesterol describes chest tightness when climbing stairs or walking uphill, starting about three weeks ago and now coming on with less effort. It settles within a few minutes of rest. She denies pain at rest. Clinic ECG today shows sinus rhythm without acute changes. Could you please assess for angina and advise on testing?

**Emergent, written as the PCP under-calling it, `econsult_4_fields`:**
> **Patient:** 74F, known HTN and hyperlipidemia.
> **Background:** Since this morning she has had pressure across her chest while sitting, still present at the visit, and she looked sweaty and pale. She says it's "probably indigestion".
> **Question:** Could cardiology see her in the next few weeks to rule out a heart cause?
> **Done so far:** ECG ordered, gave antacid.

## Before you save

- [ ] Shows the planned tier through symptoms, without naming the tier
- [ ] Includes the negation, if one is listed
- [ ] Doesn't mention the "Do NOT mention" item, even indirectly
- [ ] Matches the chart: age, sex, known conditions and medicines
- [ ] Asks the planned question type, opening with age and the key fact
- [ ] Uses the planned style and ends with a question
- [ ] Contains no names and nothing from after the referral date

---

## For the labeller (Rhea or a clinician): filling in `label.json`

Do this **after** the note exists, right away while the case is fresh. Use **ids from `pathways/cardiology.json`**, not free text.

| Field | What to put |
|---|---|
| `urgency` | `emergent` / `urgent` / `soon` / `routine`: the right answer, which may differ from `planned_tier` if the note came out differently |
| `urgency_flags` | Flag ids that justify it (from any reason), e.g. `cp_rest_or_ongoing` |
| `urgency_rationale` | One line |
| `question_type` | What the note actually asks, using the types in the table above. It may differ from `planned_question_type` if the note came out differently |
| `tests_first` | Test ids to order before the visit. `helper.tests_first_status` shows what's already done |
| `acceptable_options` | Interim option ids a specialist could reasonably pick |
| `decision_facts` | Fact ids the specialist must see for this case |
| `fit` / `acceptable_fits` | Best clinic id, plus others that are also fine |
| `chart_hook_expectation` | If `chart_dependent` is true, what Lantern should do because of the hook ("flag eGFR <30 before coronary CT") |
| `status` / `labeler` | Set `status` to `done` and add your name; use `reviewed` and add `reviewed_by` once a clinician checks it |

Leave `answer_key_only` and `helper` as generated. Then run `python3 -m unittest discover -s tests`. It fails on any id that isn't in the pathway file.

**Held-out cases** (marked in the summary) get notes and labels like every other case. Just don't look at Lantern's output on them until the final scorecard.
