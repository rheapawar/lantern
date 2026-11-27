# What PCPs ask cardiology in eConsults (source for note style and label question_type)

## Source
- Chan E, Johnson CB, Liddy C, Keely E, et al. "Paging the eCardiologist: insights into referral behaviour of primary care physicians from qualitative analysis of a cardiology eConsult service." Digital Health 2018. Champlain BASE (Ottawa). Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6120168 (also DOAJ: https://doaj.org/article/5d953777fcf844ae9671438a03d55e3e). FULL TEXT (figures 1-2 are images; only captions read).

## Sample
114 cardiology eConsults, July 2014 - January 2015; 14 excluded (no specific question), leaving 100 from 61 PCPs (92% family physicians). Patients 53% male, mean age 59.2.

## Question themes (counts out of 100)
| Theme | Count | Lantern `question_type` |
|---|---|---|
| Interpretation of diagnostic testing | 46 | test_interpretation |
| Specific investigation / management questions | 18 | specific_workup_or_management |
| Exceptions to clinical guidelines | 13 | guideline_exception |
| Non-cardiac treatment in a cardiac patient | 13 | noncardiac_drug_in_cardiac_patient |
| Screening for positive family history | 6 (text elsewhere says four cases) | family_history_screening |
| Clinical concerns despite normal testing | 4 | concerns_despite_normal_tests |
| (not in the paper) new or worsening symptoms needing assessment | - | new_symptom_assessment (Lantern addition) |

Two cross-cutting subthemes (no counts given): multiple comorbidities; mild abnormalities on cardiac tests.

## Findings relevant to Lantern
- Multimorbidity drives questions: PCPs ask how to apply several guidelines at once, and how to read risk scores when comorbidities are not accounted for.
- Mild test abnormalities unrelated to the clinical problem commonly trigger eConsults; PCPs often want reassurance.
- The paper quotes 24 PCP questions (7 / 3 / 4 / 5 / 3 / 2 across the themes). Most open with age plus one key fact, then a specific question. That pattern is visible in the excerpts; the paper does not analyse question structure.
- Not reported: how many eConsults avoided a face-to-face referral, overall or by theme. The paper cannot be used to check Lantern's "eConsult is enough" suggestions by question type.

## How it is used
- `cases/plan.csv` gives each case a `question_type`; `cases/NOTE_GUIDE.md` shows the themes with paraphrased examples.
- `cases/label.schema.json` field `question_type` records what each note actually asks.
- Coverage gap in the current 40 cases: no `family_history_screening`, one `noncardiac_drug_in_cardiac_patient` (c031). Neither matches one of the five referral reasons well; both are likely eConsult-only questions.
