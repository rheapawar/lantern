# Clinical vocabulary for pathways/cardiology.json flags

Scope: how each flag's finding is commonly written in notes (terms, abbreviations, lay phrasings, ECG/lab wording) and look-alikes that should not count. Derived from the flag meanings in pathways/cardiology.json v0.3-draft and from the sources below only. Number grammar (BP, rate, QTc, NT-proBNP, weight) is handled in code; for numeric flags only the labels, units and wordings are listed.

Source quality: MedlinePlus, AHA and CDC pages are patient-facing and give lay wording. LITFL gives ECG wording. Wikipedia pages are terminology references only (not guidelines) and are marked "Wikipedia". Abbreviation groups with no opened source are marked "(no source found - common usage, needs clinician check)". All terms are a vocabulary for review, not clinical rules; membership decisions are for cardiologist review.

## Sources opened

| Key | Title, organisation, year, URL |
|---|---|
| ML-faint | MedlinePlus Medical Encyclopedia, "Fainting", NLM, current. https://medlineplus.gov/ency/article/003092.htm |
| ML-palp | "Palpitations", MedlinePlus, NLM. https://medlineplus.gov/ency/article/003081.htm |
| ML-cp | "Chest pain", MedlinePlus, NLM. https://medlineplus.gov/ency/article/003079.htm |
| ML-angina | "Stable angina", MedlinePlus, NLM. https://medlineplus.gov/ency/article/000198.htm |
| ML-mi | "Heart attack", MedlinePlus, NLM. https://medlineplus.gov/ency/article/000195.htm |
| ML-dissect | "Aortic dissection", MedlinePlus, NLM. https://medlineplus.gov/ency/article/000181.htm |
| ML-pe | "Pulmonary embolus", MedlinePlus, NLM. https://medlineplus.gov/ency/article/000132.htm |
| ML-hemopt | "Coughing up blood", MedlinePlus, NLM. https://medlineplus.gov/ency/article/003073.htm |
| ML-hf | "Heart failure", MedlinePlus, NLM. https://medlineplus.gov/ency/article/000168.htm |
| ML-sob | "Shortness of breath", MedlinePlus, NLM. https://medlineplus.gov/ency/article/003075.htm |
| ML-af | "Atrial fibrillation/flutter", MedlinePlus, NLM. https://medlineplus.gov/ency/article/000184.htm |
| AHA-mi | "Warning signs of a heart attack", American Heart Association. https://www.heart.org/en/health-topics/heart-attack/warning-signs-of-a-heart-attack |
| AHA-af | "What is atrial fibrillation (AFib or AF)?", AHA. https://www.heart.org/en/health-topics/atrial-fibrillation/what-is-atrial-fibrillation-afib-or-af |
| AHA-hf | "Warning signs of heart failure", AHA. https://www.heart.org/en/health-topics/heart-failure/warning-signs-of-heart-failure |
| AHA-bp | "Understanding blood pressure readings", AHA. https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings |
| CDC-stroke | "Signs and symptoms of stroke", CDC. https://www.cdc.gov/stroke/signs-symptoms/index.html |
| LITFL-QT | "QT interval", Life in the Fast Lane ECG Library. https://litfl.com/qt-interval-ecg-library/ |
| LITFL-LBBB | "Left bundle branch block (LBBB)", Life in the Fast Lane ECG Library. https://litfl.com/left-bundle-branch-block-lbbb-ecg-library/ |
| W-syncope | Wikipedia, "Syncope (medicine)". https://en.wikipedia.org/wiki/Syncope_(medicine) |
| W-avb | Wikipedia, "Atrioventricular block". https://en.wikipedia.org/wiki/Atrioventricular_block |
| W-hb | Wikipedia, "Heart block". https://en.wikipedia.org/wiki/Heart_block |
| W-brady | Wikipedia, "Bradycardia". https://en.wikipedia.org/wiki/Bradycardia |
| W-wpw | Wikipedia, "Wolff-Parkinson-White syndrome". https://en.wikipedia.org/wiki/Wolff%E2%80%93Parkinson%E2%80%93White_syndrome |
| W-ecg | Wikipedia, "Electrocardiography". https://en.wikipedia.org/wiki/Electrocardiography |
| W-lqts | Wikipedia, "Long QT syndrome". https://en.wikipedia.org/wiki/Long_QT_syndrome |
| W-lbbb | Wikipedia, "Left bundle branch block". https://en.wikipedia.org/wiki/Left_bundle_branch_block |
| W-bnp | Wikipedia, "Brain natriuretic peptide". https://en.wikipedia.org/wiki/Brain_natriuretic_peptide |
| W-hte | Wikipedia, "Hypertensive emergency". https://en.wikipedia.org/wiki/Hypertensive_emergency |
| W-af | Wikipedia, "Atrial fibrillation" (first 100,000 characters read). https://en.wikipedia.org/wiki/Atrial_fibrillation |
| W-hypotn | Wikipedia, "Hypotension". https://en.wikipedia.org/wiki/Hypotension |
| W-orthopnea | Wikipedia, "Orthopnea". https://en.wikipedia.org/wiki/Orthopnea |
| W-oximetry | Wikipedia, "Pulse oximetry". https://en.wikipedia.org/wiki/Pulse_oximetry |
| W-edema | Wikipedia, "Edema". https://en.wikipedia.org/wiki/Edema |
| W-sinustachy | Wikipedia, "Sinus tachycardia". https://en.wikipedia.org/wiki/Sinus_tachycardia |
| W-sob | Wikipedia, "Shortness of breath". https://en.wikipedia.org/wiki/Shortness_of_breath |
| W-mi | Wikipedia, "Myocardial infarction". https://en.wikipedia.org/wiki/Myocardial_infarction |
| W-dissect | Wikipedia, "Aortic dissection". https://en.wikipedia.org/wiki/Aortic_dissection |
| LITFL-isch | Burns E, Cadogan M. "Myocardial Ischaemia", Life in the Fast Lane ECG Library, 1 Aug 2020 (full page text). litfl.com |
| LITFL-preex | Burns E, Buttner R. "Pre-excitation syndromes", LITFL ECG Library, 1 Mar 2021 (full page text). litfl.com |
| LITFL-avb1 | Larkin J, Buttner R. "First Degree Heart Block", LITFL ECG Library, 7 Nov 2020 (full page text). litfl.com |
| LITFL-mob1 | Burns E, Buttner R. "AV Block: 2nd degree, Mobitz I (Wenckebach Phenomenon)", LITFL ECG Library, 1 Aug 2020 (full page text). litfl.com |
| LITFL-fixed | Burns E, Cadogan M. "AV block: 2nd degree, 'fixed ratio' blocks", LITFL ECG Library, 1 Aug 2020 (full page text). litfl.com |
| LITFL-hgavb | Burns E. "AV block: 2nd degree, 'high-grade' AV block", LITFL ECG Library, 1 Aug 2020 (full page text). litfl.com |
| LITFL-chb | Larkin J, Buttner R. "AV block: 3rd degree (complete heart block)", LITFL ECG Library, 1 Aug 2018 (full page text). litfl.com |
| LITFL-svt | Burns E, Buttner R. "Supraventricular Tachycardia (SVT)", LITFL ECG Library, 1 Aug 2020 (full page text). litfl.com |
| LITFL-rw | Corry Á, Cadogan M. "Romano-Ward syndrome", LITFL Eponymictionary, 3 Apr 2022 (full page text). litfl.com |
| SP-syncope | Grossman SA, Badireddy M. "Syncope", StatPearls (NCBI Bookshelf NBK442006), updated 22 Jun 2025 (full page text). |
| SP-brady | Hafeez Y, Gibney S, Grossman SA. "Sinus Bradycardia", StatPearls (NBK493201), updated 14 Sep 2026 (full page text). |
| SP-avb1 | Varghese A, Makaryus AN. "First-Degree Heart Block", StatPearls (NBK448164), updated 17 Sep 2026 (full page text). |
| SP-avb2 | Mangi MA, Jones WM, Mansour MK, Napier L. "Second-Degree Atrioventricular Block", StatPearls (NBK482359), updated 14 Aug 2023 (full page text). |
| SP-avb3 | "Third-Degree Atrioventricular Block", StatPearls (body text read; the copy that was read did not include the author, date or Bookshelf ID lines, so those still need to be filled in). |
| SP-acs | Jain A, Singh A, Shah K, Grossman SA. "Acute Coronary Syndrome", StatPearls (NBK459157), updated 5 Jul 2026 (full page text). |
| ML-bnp | MedlinePlus Medical Tests, "Natriuretic Peptide Tests (BNP, NT-proBNP)", NLM, last updated 4 Dec 2023 (full page text). https://medlineplus.gov/lab-tests/natriuretic-peptide-tests-bnp-nt-probnp/ (URL inferred from the page title; confirm before citing) |

Opened but unhelpful for abbreviations: Wikipedia "List of medical abbreviations" (https://en.wikipedia.org/wiki/List_of_medical_abbreviations) does not list SOB, LOC, SBP, CP, AF, LBBB etc.; it lists HR only as "hour" and CP only within CPK/CPR.

## Shared groups (referenced by several flags)

### Chest pain wording
Terms: chest pain, chest pressure, tightness, heaviness, squeezing, crushing, fullness, discomfort, ache, burning, dull, sharp, stabbing, tearing, ripping; pain spreading to arm, shoulder, jaw, neck, back or between the shoulder blades; "feels like gas or indigestion" (ML-cp, ML-angina, AHA-mi).
Clinical terms: angina, angina pectoris, rest angina, "chest pain - angina" (ML-angina); heart attack, myocardial infarction, MI, acute MI, STEMI, NSTEMI (ML-mi); ACS, AMI (W-mi).
Abbreviations: CP (chest pain), MI, AMI, ACS, STEMI, NSTEMI, CAD. Only MI, STEMI, NSTEMI, CAD appear in ML-mi / ML-angina; CP and ACS as chest pain/acute coronary syndrome - (no source found - common usage, needs clinician check).
Accompanying symptoms: nausea, dizziness, sweating, cold sweats, racing heartbeat, shortness of breath, unusual fatigue, lightheadedness (ML-cp, AHA-mi). Women may more often report shortness of breath, nausea, vomiting, upset stomach, shoulder/back/arm pain, unusual tiredness (AHA-mi).
Not chest pain of cardiac type: costochondritis, strained chest muscle, GERD/heartburn, esophageal spasm, gallstones, pleurisy, pneumonia, panic attack, shingles (ML-cp).
SP-acs (full text): substernal chest pressure or heaviness, "band-like sensation", "discomfort rather than pain", radiating to jaw, neck, either shoulder or left arm, lasting 10 minutes or longer; with dyspnea, diaphoresis, nausea or lightheadedness. Anginal equivalent: unexplained new-onset exertional dyspnea. Atypical presentations (isolated dyspnea, epigastric pain, fatigue without chest pain) are more common in women, older adults and people with diabetes or kidney disease. Terms: ACS, STEMI, NSTEMI, NSTE-ACS, unstable angina. Less typical of ischemia, though these do not rule it out (SP-acs): pleuritic pain, pain reproduced by pressing on the chest, episodes lasting seconds. Look-alikes (SP-acs): pericarditis (sharp pleuritic pain, better sitting forward, diffuse ST elevation), myocarditis (after a viral illness), aortic dissection (tearing pain to the back, pulse differences), Takotsubo, PE, pneumothorax, pneumonia, GERD / esophageal spasm / peptic ulcer / pancreatitis, costochondritis / chest wall pain, panic or anxiety.

### Fainting wording
Terms: syncope, fainting, fainted, passed out, "lightheadedness - fainting" (ML-faint); blacking out, swooning, transient loss of consciousness (W-syncope). Lay: "blacked out", "collapsed", "went out", "lost consciousness" - "collapsed" and "went out" (no source found - common usage, needs clinician check).
Abbreviations: LOC, TLOC, "syncopal episode" - (no source found - common usage, needs clinician check; W-syncope uses "loss of consciousness" spelled out).
Not syncope: presyncope (consciousness not completely lost; W-syncope notes it is managed similarly but it is a separate term); lightheadedness/dizziness alone; seizure (differentiated from syncope, W-syncope); hypoglycemia, hyperventilation (ML-faint lists as causes, not heart-related).
Situational/reflex syncope (blood draw, cough, urination, defecation, prolonged standing, fear, pain; vasovagal) (ML-faint; W-syncope). These are noncardiac mechanisms; whether they count toward a rhythm red flag is for cardiologist review.
SP-syncope (full text): syncope = transient loss of consciousness and postural tone with spontaneous recovery; described as "fainting", "blacking out", "falling out", "having a spell", "losing consciousness"; "syncopal episode", "fainting spell". Near syncope / presyncope = "a feeling that one is going to pass out but does not"; the source notes that clinicians use these terms differently. Warning signs pointing to a heart cause: syncope while lying down or with no warning symptoms beforehand; syncope with chest pain, dyspnea or palpitations; abnormal ECG; known heart disease or left ventricular dysfunction (SP-syncope, Boston Syncope Criteria). Not syncope (SP-syncope): an episode lasting more than a few minutes; seizure (aura, tonic-clonic activity, prolonged unconsciousness, incontinence, tongue biting, confusion afterwards); hypoglycemia; panic attack. Usually benign: vasovagal / neurocardiogenic syncope ("the common faint"), orthostatic hypotension, situational syncope (coughing, urinating, defecating, after meals, swallowing), carotid sinus syncope.

### Shortness of breath wording
Terms: shortness of breath, breathlessness, difficulty breathing, dyspnea/dyspnoea, "not getting enough air", air hunger (ML-sob, W-sob); winded, "can't catch my breath" - "winded" appears in AHA-hf as "getting winded" during tasks; "can't catch my breath" (no source found - common usage, needs clinician check).
At rest or minimal effort: "while at rest", "after only slight activity", "with simple talking", "wakes you up at night or requires you to sleep propped up" (ML-sob); orthopnea (lying flat), paroxysmal nocturnal dyspnea (PND) (W-sob, W-orthopnea, AHA-hf: "wake up at night gasping and need extra pillows").
Abbreviations: SOB, DOE (dyspnea on exertion), PND, SOBOE - W-sob uses SOB and PND, describes DOE without defining it; SOBOE (no source found - common usage, needs clinician check).
Ambiguous: SOB (can also be read as "short of breath" vs. "side of bed"/"son of a b" in informal notes - (no source found - common usage, needs clinician check)); DOE also used for "dyspnea on exertion" only. Exertional breathlessness is not "at rest" (ML-sob).

## Chest pain flags (reason: chest_pain)

## cp_rest_or_ongoing (chest pain at rest or ongoing)
Terms: chest pain/pressure/tightness/heaviness at rest, rest angina ("angina while sitting"), ongoing, constant, persistent, "not going away", "not relieved by rest or nitroglycerin", "worsening or returning after initially improving", "more intense, comes on with lighter activity, lasts longer than usual" (ML-angina, ML-cp). Timing phrases such as "since this morning", "woke him from sleep", "right now", "currently" (no source found - common usage, needs clinician check).
Abbreviations: CP, NTG (nitroglycerin), SL NTG, ACS, MI (see shared group; NTG - no source found - common usage, needs clinician check).
Not this flag: pain that came and went and is fully resolved ("resolved", "no longer present") - ML-cp/ML-angina describe angina lasting 1-15 minutes easing with rest, which is stable angina rather than ongoing pain; reproducible chest-wall pain (costochondritis, strain), reflux/heartburn, panic attack, shingles (ML-cp); "chest pain" in the past history list ("history of chest pain", "no chest pain") - negation and history wording (no source found - common usage, needs clinician check).
Ambiguous: "chest tightness" can be respiratory (asthma/COPD) as well as cardiac; "pressure" can be BP pressure.

## cp_with_alarm_symptoms (chest pain with sweating, fainting or breathlessness)
Terms: see Chest pain and Fainting and Shortness of breath groups. Sweating: diaphoresis, diaphoretic, sweaty, cold sweats, "broke out in a sweat" (AHA-mi: cold sweats; ML-cp: sweating; diaphoresis/diaphoretic - (no source found - common usage, needs clinician check)).
Abbreviations: SOB, DOE, CP, "CP with diaphoresis" (see shared groups).
Not this flag: sweating from fever, exercise, menopause (hot flashes/night sweats) without chest pain - (no source found - common usage, needs clinician check); presyncope/lightheadedness listed separately; breathlessness of known lung disease at baseline.
Ambiguous: SOB; LOC.

## cp_ecg_ischemia (recent chest pain with new ischemic ECG changes)
ECG wording: ST elevation, ST-elevation MI, STEMI, ST depression, T-wave inversion, hyperacute T waves, new Q waves, reciprocal changes, "ischemic changes", "ischaemia" (UK spelling), "nonspecific ST-T changes" (W-ecg: ST elevation by at least 1 mm in early STEMI; ST depression or T-wave inversion in ischemia/NSTEMI; pathologic Q waves hours after MI and generally persist). Units: mm (1 mm); leads named by territory (V1-V6, I, aVL, II, III, aVF) (LITFL-QT uses mm/ms conventions).
Abbreviations: STE, STD, TWI, STEMI, NSTEMI, ACS, LAD (no source found - common usage, needs clinician check, except STEMI/NSTEMI per W-ecg).
Not this flag: old/chronic changes ("old inferior MI", "Q waves unchanged", "unchanged from prior"), benign early repolarization (LITFL-QT names BER as a mimic of hyperacute T waves), pericarditis, Brugada pattern, "J-point elevation" normal variant (W-ecg lists pericarditis, Brugada, J-point elevation as other causes of ST elevation), LVH or digoxin ST depression (W-ecg), "nonspecific ST-T changes" (borderline; cardiologist to decide), LBBB repolarization changes (LITFL-LBBB: expected discordant ST/T changes).
Ambiguous: "ST" alone could mean sinus tachycardia in some notes (no source found - common usage, needs clinician check); "new" vs "old" depends on prior ECG availability.
LITFL-isch (full text): non-ST-elevation ACS (NSTEACS) = NSTEMI + unstable angina pectoris (UAP). ECG wording: ST segment depression (horizontal or downsloping, >= 0.5 mm at the J-point in >= 2 contiguous leads; >= 1 mm more specific), T wave flattening or inversion (TWI >= 1 mm in >= 2 contiguous leads with dominant R waves), "dynamic" ST/T changes (different from the old ECG or changing over time), hyperacute (peaked) T waves, pseudonormalisation of previously inverted T waves, U-wave inversion, Wellens syndrome / Wellens pattern (biphasic or deeply inverted T waves in V2-4; patients may be pain free when the ECG is taken yet remain at very high risk). Not this flag (LITFL-isch): upsloping ST depression, ST depression < 0.5 mm, TWI < 1 mm, T wave flattening alone (non-specific); TWI in III, aVR or V1 alone (normal variant); LVH and digoxin effect (mimics). Rate-related ST depression during SVT that resolves in sinus rhythm (LITFL-svt). Relevant to the review question on pain-free ST changes: a Wellens pattern matters even after pain has settled (LITFL-isch).

## cp_dissection_pe (sudden tearing back pain, sudden breathlessness / coughing blood)
Terms (dissection): tearing, ripping, stabbing, sharp, abrupt/sudden onset, pain between the shoulder blades (interscapular), radiating to the back, "worst pain of my life" - last phrase (no source found - common usage, needs clinician check); migrating pain as dissection extends (ML-dissect, W-dissect: "tearing, stabbing, or sharp"; interscapular pain; 96% sudden onset). Names: aortic dissection, dissecting aneurysm, thoracic aortic aneurysm - dissection, AD, TAAD/TBAD, Stanford A/B (ML-dissect, W-dissect).
Terms (PE): pulmonary embolism, pulmonary embolus, lung blood clot, venous thromboembolism, VTE, DVT, PE, "sudden shortness of breath", sharp/stabbing pleuritic chest pain worse with deep breath, swollen leg after travel or bed rest (ML-pe, ML-cp).
Terms (blood): coughing up blood, hemoptysis, spitting up blood, bloody sputum, blood-streaked mucus (ML-hemopt).
Not this flag: bleeding from nose, mouth, throat or GI tract (hematemesis) - ML-hemopt states coughing up blood is not the same as bleeding from mouth, throat or GI tract; "tearing" used for other pain (e.g., muscle strain, reflux "ripping" cough); gradual exertional breathlessness (not sudden); pleuritic pain from pneumonia or pleurisy (ML-cp lists as non-PE cause).
Ambiguous: PE = pulmonary embolism vs physical exam ("PE") (W list of abbreviations lists "PE" nowhere as pulmonary embolism, but ML-pe uses PE; physical exam sense - no source found - common usage, needs clinician check); "tearing" in lay speech is often figurative.

## cp_new_or_worsening_exertional (new/worsening chest pain with exertion)
Terms: exertional chest pain/angina, "pain with exertion", with walking/stairs/hill/exercise/carrying, "comes on with lighter activity", "lasts longer than usual", "more often", "crescendo", "eases with rest or nitroglycerin", "typical angina", "stable angina" (chronic, predictable), "unstable angina" (new, worse, or at rest) (ML-angina). Triggers listed: physical exertion, emotional stress, cold weather, large meals (ML-angina). "Chest pain on exertion", "CP on exertion", "DOE" (DOE refers to breathlessness; see shared group).
Abbreviations: CCS class (Canadian Cardiovascular Society angina class) and "exertional CP" - (no source found - common usage, needs clinician check).
Not this flag: chronic stable pattern unchanged for years ("unchanged", "stable") - ML-angina describes stable angina as predictable; pain brought on by position, breathing or palpation; breathlessness without pain; "exertion" in non-cardiac sense (e.g., muscle exertion causing strain) (no source found - common usage, needs clinician check).
Ambiguous: "worse" and "started" can describe other symptoms in the same sentence; "activity" may refer to non-physical activity.

## Palpitations / AFib flags (reason: palpitations_afib)

### Palpitation wording (shared)
Terms: palpitations, heartbeat sensations, irregular heartbeat, heart pounding or racing, fluttering, skipped or stopped beats, "unpleasant awareness of heartbeat", felt in chest, throat or neck (ML-palp); "fluttering, skipped beats, pounding, racing" (AHA-af); "rapid, racing, pounding or thumping, fluttering, irregular, or too slow" pulse (ML-af). "Thumping", "flip-flopping", "missed beat" - "thumping" in ML-af; others (no source found - common usage, needs clinician check).
Abbreviations: palps, HR, PVC, PAC, ectopy, SVT, AF/AFib/A-fib/AFL (ML-af lists AFib, A-fib, AF, AFL; PVC/PAC defined in W-ecg).
Non-rhythm look-alikes (ML-palp): anxiety, panic, caffeine, stimulants, decongestants, diet pills, nicotine, exercise, fever, excessive alcohol. Sinus tachycardia is a regular physiologic rate rise (W-sinustachy).
LITFL-svt (full text): SVT, supraventricular tachycardia, paroxysmal SVT (pSVT), AVNRT, AVRT, narrow complex tachycardia, regular tachycardia ~140-280 bpm; patients "complain of the sudden onset of rapid, regular palpitations"; associated presyncope or syncope, chest pain, dyspnoea, anxiety. Atrial flutter, atrial tachycardia, multifocal atrial tachycardia and AF are listed as SVT subtypes. Not an emergency in itself: "generally well tolerated".

## palp_syncope (palpitations with fainting)
Terms: palpitations plus syncope, fainted, passed out, blacked out, lost consciousness (see Fainting group; palpitations in ML-af listed with fainting). Arrhythmia is the most common cause of cardiac syncope (W-syncope).
Abbreviations: LOC, TLOC, syncopal episode (see Fainting group).
Not this flag: presyncope / near-faint / lightheadedness without loss of consciousness (separate; W-syncope); vasovagal or situational syncope at blood draw, cough, urination, defecation, prolonged standing (ML-faint, W-syncope); orthostatic drop on standing (W-syncope); seizure; hypoglycemia; remote history ("fainted years ago", "no syncope"). Whether fainting that is unrelated in time to the palpitations counts is a clinician question.
Ambiguous: LOC (loss vs level of consciousness - no opened source; Wikipedia page for "Level of consciousness" returned 404); "spell", "episode".

## palp_chest_pain (palpitations with chest pain)
Terms: palpitation wording above plus chest pain wording above; "racing heart with chest pressure/tightness" (ML-af lists chest pain or pressure among AFib symptoms; AHA-mi lists racing or irregular heartbeat as heart-attack sign).
Abbreviations: see shared groups.
Not this flag: palpitations and chest pain in separate unrelated episodes; chest wall pain, reflux (ML-cp); panic attack (ML-cp, ML-palp list panic/anxiety as causes of each).
Ambiguous: "tightness" may be anxiety-related.

## palp_fast_low_bp (very fast heart rate with low BP or near-fainting)
Rate wording (labels, not numbers): heart rate, HR, pulse, rate, ventricular rate, bpm, beats per minute, "rate of 150", "HR 150s", "150 bpm" (W-af uses bpm; W-bradycardia uses BPM). Terms: tachycardia, rapid ventricular response, RVR, "fast AF", "AF with RVR", wide-complex tachycardia, SVT, VT (W-af: RVR = AF with fast ventricular rate; uncontrolled AF causes shortness of breath, dizziness, lightheadedness, swelling, and "low blood pressure is the most concerning sign").
BP wording: low blood pressure, hypotension, hypotensive, "BP 80/50", SBP, systolic, mmHg, MAP (mean arterial pressure) (W-hypotn: systolic below 90 or diastolic below 60 mmHg commonly called hypotension; MAP below 65). Lay: lightheaded, dizzy, giddy, weak, near-fainting, faint, confusion, blurred vision (W-hypotn lists lightheaded/dizzy as most common, plus "near fainting" and fainting).
Abbreviations: HR, BP, SBP, DBP, MAP, RVR, SVT, VT (RVR and the BP set per W-af and W-hypotn; SBP/DBP not defined in W-hte).
Not this flag: sinus tachycardia from exercise, fever, anxiety, dehydration, anemia, hyperthyroidism, stimulants (W-sinustachy); fast rate with normal BP and no symptoms (separate urgent flag palp_new_af_rvr); orthostatic hypotension on standing (W-hypotn); "racing heart" that is only a sensation with normal documented rate; "very fast" describing speech or other events.
Ambiguous: "rate 150" may be a drug dose or respiratory rate; "pulse" may mean pulse oximeter reading; "pulse ox" is oxygen saturation, not heart rate (W-oximetry: SpO2 in %, though most monitors also show pulse rate); "brady" and "tachy" shorthand (no source found - common usage, needs clinician check); "low" alone (low potassium, low BP).

## palp_stroke_symptoms (face droop, arm weakness, speech trouble)
Terms: face drooping, facial droop, one side of the face droops, arm weakness or drift, sudden numbness or weakness of face/arm/leg especially one side, slurred speech, trouble speaking or understanding speech, sudden confusion, sudden trouble seeing, sudden trouble walking/dizziness/loss of balance, sudden severe headache; BE-FAST (Balance, Eyes, Face, Arms, Speech, Time); stroke, TIA, "mini-stroke" with symptoms clearing within minutes (CDC-stroke). Also CVA (cerebrovascular accident) - (no source found - common usage, needs clinician check).
Abbreviations: TIA, CVA, FAST/BE-FAST (TIA, FAST per CDC-stroke).
Not this flag: prior remote stroke/TIA listed in history ("history of TIA", "no focal deficits"), which is a CHA2DS2-VASc input and not an acute symptom; dizziness alone without other signs; Bell's palsy (peripheral facial weakness) and migraine aura as look-alikes - (no source found - common usage, needs clinician check); the substring "tia" inside other words (e.g., "initial", "patient", "essential") - a text-matching hazard, not a clinical term.
Ambiguous: "TIA" can match inside longer words; "weakness" generic fatigue vs focal weakness.

## palp_preexcitation (AFib with pre-excitation / WPW on ECG)
Terms: Wolff-Parkinson-White, WPW, WPW pattern, WPW syndrome, "ventricular pre-excitation", pre-excitation, delta wave, accessory pathway, bundle of Kent, short PR interval (<120 ms), wide QRS (>120 ms) with slurred upstroke, AVRT (atrioventricular reentrant tachycardia), "irregular wide-complex tachycardia" in AF with pre-excitation (W-wpw). Spellings: Wolff-Parkinson-White with en dash or hyphen, "Wolf" misspelling - (no source found - common usage, needs clinician check).
Abbreviations: WPW, AVRT, AF, PR, QRS, ms.
Not this flag: Lown-Ganong-Levine (listed in W-wpw only as another pre-excitation syndrome, not described); ordinary AF with normal narrow QRS; "delta" used in unrelated contexts (delta troponin, delta gap, "delta variant") - (no source found - common usage, needs clinician check); "WPW pattern" without AF (pattern vs. syndrome distinction not formally defined in W-wpw).
Ambiguous: "WPW" alone (pattern, no arrhythmia) vs. with AF; "pre-excitation" vs "preexcitation" spelling.
LITFL-preex (full text): Wolff-Parkinson-White (WPW) syndrome = congenital accessory pathway (AP) plus tachyarrhythmias; "often used interchangeably with pre-excitation syndrome". ECG wording: PR interval < 120 ms, delta wave ("slurring slow rise of initial portion of the QRS", "slurred upstroke"), QRS > 110 ms, discordant ST-T changes, pseudo-infarction pattern / pseudo-Q waves; AP also called bypass tract, Bundle of Kent, atrioventricular bypass tract; "type A" (left-sided) and "type B" (right-sided) WPW pattern. Tachyarrhythmias: AF or flutter conducted via the AP, and AVRT. Not this flag: concealed pathway (no pre-excitation on the sinus-rhythm ECG), Lown-Ganong-Levine (short PR, normal QRS, existence disputed), Mahaim-type pre-excitation. Ambiguous: "type A / type B" is also used for Wellens T-wave patterns (LITFL-isch).

## palp_new_af_rvr (AF with fast rate)
Terms: atrial fibrillation, AF, AFib, A-fib, A fib, afib, "auricular fibrillation", irregularly irregular (ML-af lists AFib, A-fib, Afib, AF, AFL, auricular fibrillation; "irregularly irregular" is not used by W-af but describes irregular R-R intervals with absent P waves). Fast rate: fast, rapid, RVR, rapid ventricular response, "fast AF", "AF with RVR", rate often above 100, AF/flutter rates up to 250-350 atrial (ML-af). Pattern names: paroxysmal, persistent, long-standing persistent, permanent, first detected, subclinical AF (W-af). Rate-control wording: "rate controlled", "uncontrolled rate", "rate control target under 110" (W-af).
Heart-rate labels: HR, pulse, ventricular rate, bpm, beats per minute, "rate 130s".
Abbreviations: AF, AFib, A-fib, AFL (atrial flutter), RVR, PAF (paroxysmal AF), CAF, NSR, SVT (PAF/CAF - no source found - common usage, needs clinician check).
Not this flag: atrial flutter (organized, regular, saw-tooth; separate diagnosis, ML-af, W-af); SVT; sinus tachycardia (W-sinustachy); PACs/PVCs; "history of AF" in sinus rhythm now ("s/p ablation", "in sinus"); AF with controlled rate ("rate controlled", "HR 70s") for the fast-rate component; "new" vs known AF is determined from the chart, not by wording alone.
Ambiguous: "fast" can describe pulse or breathing; "racing" is lay and may be sinus tachycardia; RVR sometimes written "rapid ventricular response" vs "rapid ventricular rate"; AF vs AFL abbreviation confusion (ML-af uses AFL for flutter).

## palp_heart_failure_signs (palpitations with new swelling or breathlessness)
Terms: palpitation wording plus swelling: swelling, swollen, edema/oedema, puffiness in feet, ankles, legs, hands, belly, "pitting edema", pedal edema, peripheral edema, fluid retention (W-edema, AHA-hf); breathlessness: see shared group. AHA-hf lists a racing or pounding heartbeat among heart failure signs.
Abbreviations: LE edema, BLE edema, SOB, DOE, PND (LE/BLE - no source found - common usage, needs clinician check).
Not this flag: swelling from lymphedema, lipedema, myxedema, venous insufficiency, DVT, pregnancy, menstruation, immobility, medications such as amlodipine (W-edema lists causes; amlodipine per the pathway's own fact list and the 2025 BP guideline Table 13); breathlessness from lung disease (W-sob); chronic unchanged baseline swelling (flag text says "new").
Ambiguous: "swelling" in joints or insect bites; "new" requires time context.

## Heart failure flags (reason: heart_failure_symptoms)

## hf_breathless_rest (breathless at rest or can't lie flat)
Terms: shortness of breath at rest, breathless talking, "after only slight activity or while at rest", "with simple talking", dyspnea at rest, orthopnea, "can't lie flat", sleeping upright or in a chair/recliner, "propped up on pillows", "two-pillow orthopnea", paroxysmal nocturnal dyspnea (PND), "wakes up at night gasping" (ML-sob, ML-hf: shortness of breath after lying down or being asleep, AHA-hf: wake gasping and need extra pillows, called orthopnea; W-orthopnea: sleep propped up or in a chair). Pillow count wording "two-pillow orthopnea" is not addressed in W-orthopnea - (no source found - common usage, needs clinician check).
Abbreviations: SOB, SOBAR (SOB at rest), PND, DOE, "3PO" (three-pillow orthopnea) - SOBAR, 2PO/3PO (no source found - common usage, needs clinician check); SOB, PND per W-sob.
Not this flag: exertional breathlessness only (ML-sob: climbing stairs may be normal); platypnea (worse upright), trepopnea, bendopnea (W-orthopnea lists as related but distinct); orthopnea from asthma, chronic bronchitis, sleep apnea, panic disorder, liver disease (W-orthopnea lists non-HF causes); breathlessness from lung disease (COPD) at known baseline; "lying flat" for back pain.
Ambiguous: SOB; "winded" (exertional); "rest" also appears in "rest of the day".

## hf_chest_pain (chest pain with HF symptoms)
Terms: chest pain wording above (ML-hf lists chest pain or pressure, more likely with exercise, among HF symptoms) together with swelling, shortness of breath, weight gain or orthopnea. Weight gain wording below.
Not this flag: see Chest pain look-alikes. A flag whose only chest-pain term is a history entry ("no chest pain") is not a hit; negation handling is a code question.
Ambiguous: see shared groups.

## hf_syncope (fainting)
Terms and look-alikes: see Fainting group. ML-hf lists "cough, fatigue, weakness, or faintness" among heart failure symptoms; "faintness" is closer to presyncope than syncope (ML-hf).
Not this flag: presyncope/faintness/lightheadedness (separate flag wording needed - clinician to decide); orthostatic hypotension from diuretics (W-syncope: medications, dehydration); vasovagal/situational.
Ambiguous: LOC.

## hf_ntprobnp_over_2000 and hf_ntprobnp_400_2000 (NT-proBNP value)
Label wording: NT-proBNP, NTproBNP, NT-pro-BNP, "pro-BNP", proBNP, "N-terminal pro-B-type natriuretic peptide", BNP, "B-type natriuretic peptide", "brain natriuretic peptide" (older name), BNP-32 (W-bnp). Units: pg/mL and ng/L (W-bnp: ng/L equivalent to pg/mL; pmol/L not mentioned there). Comparison wording ("over", "above", ">", "elevated to", "was 2,500", "2.5k") is handled in code.
Abbreviations: BNP, NT-proBNP, pro-BNP, NP (natriuretic peptide).
Not this flag: BNP versus NT-proBNP are different assays with different cut-offs (the NICE 400/2,000 ng/L bands apply to NT-proBNP; W-bnp gives BNP-based cut-offs around 100-500 pg/mL); ANP (atrial natriuretic peptide) is a separate hormone (W-bnp); a value from the pathway's own fact "NT-proBNP" dated outside the window; values raised by kidney disease or lowered in obesity (W-bnp: confounders).
Ambiguous: "BNP" in a note may mean BNP or NT-proBNP; "pro-BNP" hyphenation; "BNP" also appears in "BNP 2000" without units.
ML-bnp (full text): two different tests. BNP = brain natriuretic peptide = B-type natriuretic peptide. NT-proBNP = N-terminal pro b-type natriuretic peptide, also written "NT-pro B-type natriuretic peptide" and "N terminal proBNP". Because the two tests are different, a BNP value must NOT be read as an NT-proBNP value. ML-bnp gives no cut-offs for either test; the pathway's 400 and 2000 thresholds apply to NT-proBNP only. ML-bnp also says levels are judged against normal values for age and sex. Higher than true heart-failure level for other reasons: kidney failure, valve or heart-muscle disease, pulmonary embolism, pulmonary hypertension. Lower than the true level: obesity. HF symptoms listed: shortness of breath, swelling (abdomen, feet, legs, neck veins), fatigue or weakness, cough, unable to sleep lying flat, urinating often at night, loss of appetite and nausea.

## hf_rapid_weight_gain (fast weight gain or worsening swelling)
Terms: rapid weight gain, "gained X lbs/pounds/kg in a day/week", "weight up", "up 5 pounds", fluid retention, worsening swelling, "swelling getting worse", puffiness of feet, ankles, legs, hands or belly (AHA-hf: sudden gain over a day or a week, often from fluid retention; sudden loss can also be concerning; W-edema: also called oedema, fluid retention, swelling). Units: lb, lbs, pounds, kg, kilograms; periods: day, week, overnight.
Abbreviations: wt, lbs, kg, LE edema, BLE (lower-extremity), "+2 pitting edema" (grading of edema absent to +++ per W-edema); wt, BLE (no source found - common usage, needs clinician check).
Not this flag: intentional or gradual weight gain (diet, steroid, pregnancy), weight loss, chronic unchanged swelling, swelling from lymphedema, venous insufficiency, medicines, kidney or liver disease (W-edema); unit confusion between lb and kg.
Ambiguous: "gained" (muscle, appetite, a lead); "up" in "weight up".

## Abnormal ECG flags (reason: abnormal_ecg)

### Conduction wording (shared)
Names: first-degree AV block (PR interval greater than 200 ms), second-degree type 1 / Mobitz I / Wenckebach (progressive PR lengthening then dropped beat), second-degree type 2 / Mobitz II (fixed PR, random dropped beats; "Hay block"), high-grade or advanced block, 2:1 block, third-degree AV block / complete heart block / CHB (no relationship between P waves and QRS) (W-avb, W-hb). "Heart block", HB, AVB, AV nodal block (W-hb). Bundle branch block: LBBB, RBBB, bifascicular, fascicular block / hemiblock, LAFB, LPFB (W-hb, W-lbbb).
Look-alikes of block: pseudo-AV block from concealed junctional extrasystoles (W-avb); blocked PACs; AV dissociation without complete block, e.g. AIVR, VT, isorhythmic dissociation (LITFL-chb); first-degree block and Mobitz I can be normal variants in athletes or children (W-avb).

## ecg_active_mi (signs of an ongoing heart attack)
Terms: STEMI, ST elevation, ST-elevation myocardial infarction, acute MI, AMI, "ongoing chest pain", "acute coronary syndrome", ACS, hyperacute T waves; alternative names for heart attack: myocardial infarction, MI, acute MI, STEMI, NSTEMI (ML-mi). ECG: ST elevation of at least 1 mm in early STEMI (W-ecg).
Abbreviations: STEMI, NSTEMI, MI, AMI, ACS.
Not this flag: old MI (Q waves, "age-indeterminate", "unchanged"); NSTEMI (no ST elevation, separate management - cardiologist to decide whether it belongs to the flag); pericarditis, early repolarization, Brugada, LVH, LV aneurysm, paced rhythm (W-ecg lists non-MI causes of ST elevation); LBBB-related ST changes (LITFL-LBBB); "rule out MI" / "r/o MI" (a question, not a finding) - (no source found - common usage, needs clinician check).
Ambiguous: "ongoing" attaches to many symptoms; "MI" also "mitral insufficiency" in older echo reports (no source found - common usage, needs clinician check).
LITFL-isch (full text): hyperacute (peaked) T waves suggest hyperacute STEMI; ST depression confined to one territory is more likely reciprocal change from a STEMI elsewhere; widespread ST depression with ST elevation in aVR > 1 mm suggests left main (LMCA) occlusion. Named STEMI patterns: anterior, lateral, inferior, posterior, right ventricular infarction, LMCA occlusion.

## ecg_high_grade_block_symptomatic and ecg_high_grade_block (complete / high-grade block)
Terms: complete heart block, CHB, third-degree AV block, 3rd degree, high-grade AV block, advanced AV block, Mobitz II / type 2 second-degree, 2:1 AV block (see shared conduction wording; W-avb, W-hb). Symptoms for the symptomatic flag: dizzy, lightheaded, fainted, syncope, passed out, near-faint, shortness of breath, fatigue; lay symptoms in heart block: occasional missed beats, light-headedness, fainting, palpitations (W-hb).
Abbreviations: AVB, CHB, 2:1, Mobitz, HB, PPM (permanent pacemaker; no source found - common usage, needs clinician check).
Not this flag: first-degree AV block (PR >200 ms, no dropped beats); Mobitz I/Wenckebach (progressive PR, often benign; W-avb); bundle branch blocks and fascicular blocks (infra-Hisian conduction delay, W-hb) including bifascicular/trifascicular block (pathway's own source_note already questions their inclusion); 2:1 conduction can be Mobitz I or II and the QRS width only hints which (LITFL-fixed); whether 2:1 belongs in the emergent list is still a cardiologist question; sinus pauses and SA exit block (W-brady); paced rhythm.
Ambiguous: "Type II second-degree" vs Mobitz II; "2:1" may be a ratio unrelated to block (e.g., 2:1 flutter, 2:1 dosing).
LITFL (full text) - block wording and severity:
- First-degree AV block (LITFL-avb1): PR > 200 ms ("marked" > 300 ms); isolated finding is benign, no specific treatment. Not this flag.
- Mobitz I / Wenckebach / "Mobitz type I" (LITFL-mob1): progressive PR prolongation then a non-conducted P wave, grouped beating; usually benign, low risk of progression, asymptomatic patients need no treatment. Not this flag.
- Fixed-ratio blocks 2:1, 3:1, 4:1 (LITFL-fixed): can result from either Mobitz I or Mobitz II; narrow QRS favours Mobitz I, broad QRS favours Mobitz II, but the distinction "is not infallible". This is the source for the open question on whether "2:1" belongs in the emergent list.
- High-grade AV block (LITFL-hgavb): second-degree block with P:QRS 3:1 or higher, extremely slow ventricular rate; may result from Mobitz I or II.
- Complete heart block / CHB / third-degree ("3rd degree") AV block (LITFL-chb): complete AV dissociation with independent atrial and ventricular rates, junctional or ventricular escape rhythm; "high risk of ventricular standstill and sudden cardiac death"; "require urgent admission for cardiac monitoring, backup temporary pacing and usually insertion of a permanent pacemaker". Mobitz II is also called Hay block (LITFL-mob1 page links).
- Not this flag (LITFL-chb): AV dissociation from other causes (e.g. AIVR, VT) is not complete heart block; isorhythmic AV dissociation can look like 2:1 block.
StatPearls (full text):
- First-degree block / "AV conduction delay" (SP-avb1): PR > 0.20 s with 1:1 conduction; marked if PR > 0.30 s; almost always without symptoms; progression is uncommon. Not this flag.
- Second-degree block (SP-avb2): Mobitz type I / Wenckebach ("dropped beat", grouped beating, often a normal variant); Mobitz type II (constant PR, often wide QRS / bundle branch block, "often progresses to third-degree"). "If more than one P wave is not conducted this is no longer a Mobitz type II and is considered a high degree AV block." Symptoms of Mobitz II: fatigue, dyspnea, chest pain, presyncope or syncope.
- 2:1 block (SP-avb2): "difficult to differentiate between type I and type II"; recommended to "assume the worst-case scenario", call it a "non-typeable second-degree AV block", and manage it like type II. LITFL-fixed says that 2:1 block can be either type. Taken together: if the plain-code check counts 2:1 as high-grade, it follows SP-avb2's worst-case advice; a cardiologist still needs to confirm.
- Conflict on Mobitz I: SP-avb2 says in one place that "All patients with Mobitz 1 block should be admitted and monitored" and in another that Mobitz I without symptoms "requires no treatment"; LITFL-mob1 says it is usually benign. A cardiologist should decide; this is not a reason to raise the urgency tier.
- Third-degree block / complete heart block (SP-avb3): complete AV dissociation; junctional, fascicular or ventricular escape rhythm; rate "typically less than 45 to 50 beats/min"; "Rarely are patients asymptomatic"; cannon A waves. SP-avb3 says: "patients with Mobitz II block, high-degree AV block, and third-degree AV block require urgent admission". Not this flag (SP-avb3): AV dissociation from an idioventricular rhythm (ventricular rate faster than atrial rate). Second-degree and high-grade blocks can look like complete heart block.

## ecg_very_slow_symptomatic and ecg_very_slow (very slow heart rate)
Terms: bradycardia, sinus bradycardia, slow heart rate, "heart rate in the 30s", HR 38, pause, sinus pause, sinus arrest, "pauses", bradyarrhythmia (W-brady). Adult definition below 60 bpm (some use 50); sleeping rates below 50 can be normal in young healthy adults and athletes; sinus pauses and SA exit block (W-brady). Symptoms: fatigue, shortness of breath, dizziness, confusion, fainting (W-brady); near-faint / presyncope (W-syncope); low blood pressure (W-hypotn); chest pain, breathlessness at rest.
Labels and units: HR, heart rate, pulse, rate, bpm, BPM, "beats per minute".
Abbreviations: brady, HR, bpm, SB (sinus bradycardia), SSS (sick sinus syndrome) (W-brady names sick sinus syndrome; brady/SB (no source found - common usage, needs clinician check)).
Not this flag: physiologic bradycardia in athletes, sleep, vagal tone; rates measured only asleep or overnight ("nocturnal", "sleep study", "Holter overnight") - handled by the card hint; beta-blocker or other drug effect at a stable asymptomatic slow rate is a "reversible cause" question for a clinician (W-brady causes: beta blockers, calcium channel blockers, antiarrhythmics, digoxin, clonidine, lithium; hypothyroidism, electrolytes, sleep apnea-type vagal causes); sinus arrhythmia (W-brady: common and usually benign).
Ambiguous: "brady" (bradycardia vs "bradykinesia"); "pause" (breath-holding, "pause in therapy", "pause in speech"); "pulse ox" is oxygen saturation not heart rate (W-oximetry); "HR" can mean hour(s) (the Wikipedia abbreviation list lists "hr" only as hour); "slow" can describe gait or speech; "low" can mean BP.
LITFL-fixed / LITFL-chb (full text): slow rates in block are written as "ventricular rate ~38 bpm", "ventricular rate only 15 bpm", "atrial rate ~85 bpm" - the ventricular rate is the one that matters, the atrial rate is not the heart rate.
SP-brady (full text): sinus bradycardia; the 2025 AHA ACLS update defines clinically meaningful bradycardia as a rate below 50 bpm, compared with the traditional threshold of below 60. Related terms: sinus node dysfunction, sick sinus syndrome, tachycardia-bradycardia syndrome ("tachy-brady"), sinus pause (> 3 s), sinus arrest, sinoatrial exit block, ectopic atrial bradycardia, junctional escape rhythm, ventricular escape rhythm, chronotropic incompetence, "bradycardic". Symptoms: fatigue, exercise intolerance, lightheadedness, dizziness, syncope or presyncope, worsening angina, worsening heart failure, cognitive changes. Signs of instability: hypotension, altered mental status, dyspnea. Common causes from medicines: beta-blockers, calcium channel blockers, digoxin, ivabradine, clonidine, antiarrhythmics. Not this flag (SP-brady): asymptomatic slow rate in healthy athletes or young adults (high vagal tone); slow rate during sleep, including in adults over 65. Gap: the shorthand "brady" (as in "sinus brady") does not appear as a separate word in SP-brady or W-brady; it is still unsourced.

## ecg_new_lbbb (new left bundle branch block)
Terms: left bundle branch block, LBBB, "left BBB", "left bundle block", "complete LBBB", "incomplete LBBB" (QRS under 120 ms; separate entity, LITFL-LBBB); "new", "new onset", "presumed new", "not seen on prior ECG", "new since [date]" (LITFL-LBBB: new LBBB with chest pain was once a STEMI-equivalent; current practice looks at excessive discordance or concordant ST changes). ECG wording: QRS 120 ms or longer, broad notched R in I/aVL/V5-6, QS or rS in V1, no lateral Q waves, discordant ST-T (LITFL-LBBB, W-lbbb). "Wide QRS" (W-ecg: QRS over 120 ms suggests LBBB or RBBB).
Abbreviations: LBBB, RBBB, LAFB, LPFB, BBB, IVCD (IVCD - no source found - common usage, needs clinician check; others per W-lbbb, W-ecg).
Not this flag: RBBB (separate entity); LAFB/LPFB (partial left blocks, W-lbbb); incomplete LBBB; LV-paced rhythm (similar morphology with pacing spikes, LITFL-LBBB); LVH mimicking LBBB (LITFL-LBBB); "known/chronic/old/unchanged LBBB" (flag requires "new"); the word "new" far from the LBBB mention.
Ambiguous: "BBB" with no side; "new" appearing in unrelated text.

## ecg_long_qt (long QT; QTc 500 or more)
Terms: long QT, prolonged QT, QT prolongation, long QT syndrome, LQTS, "acquired long QT", "drug-induced QT prolongation", torsades de pointes, TdP, "QT-prolonging drugs", corrected QT, QTc (LITFL-QT, W-lqts). Measurement wording: QT, QTc, "QTc (Bazett)", QTcB, "QTc (Fridericia)", QTcF, Framingham, Hodges; units ms (milliseconds) with RR in seconds; "QTc 512", "QTc of 510 ms" (LITFL-QT lists Bazett, Fridericia, Framingham, Hodges; QTcB/QTcF abbreviations (no source found - common usage, needs clinician check)). Reference wording: prolonged above 440 ms (men) or 460 ms (women), above 500 ms increased torsades risk (LITFL-QT); HRS: above 500 ms without other QT-prolonging factors or above 480 ms with syncope (W-lqts).
Abbreviations: QT, QTc, QTcB, QTcF, LQTS, TdP, SQTS (short QT syndrome).
Not this flag: short QT / short QTc (below 350 ms, SQTS; LITFL-QT); digoxin effect (relative shortening, LITFL-QT); T-U fusion or prominent U waves from hypokalemia producing apparent QT prolongation, hypocalcemia (prolongs ST segment, LITFL-QT); wide QRS (LBBB, RBBB, paced) inflating QT without true repolarization prolongation - not covered in an opened source, clinician to confirm; QT "WNL"/"normal"; "no long QT", "family history of long QT" (history, not a finding); Brugada or ARVC (W-lqts differentials).
Ambiguous: "QT" with no c (uncorrected); "QTc" values from machine read vs manual; "QTc 500" lower bound for the flag is a threshold issue handled in code; "LQTS" family history.
LITFL-rw (full text): congenital long QT syndrome (LQTS); Romano-Ward syndrome (autosomal dominant, no deafness; also "Ward-Romano syndrome", "congenital long QT syndrome without deafness"); Jervell and Lange-Nielsen syndrome (with congenital deafness); torsades de pointes; syncope triggered by exertion or emotion. QT written in seconds in older reports ("QT = 0.60"), which supports reading QTc in seconds as well as ms.

## ecg_slow_during_sleep (card hint: slow rate during sleep)
Terms: nocturnal bradycardia, slow heart rate overnight, asleep, sleeping, during sleep, at night, nighttime, overnight Holter, sleep study, "in his/her sleep" (W-brady: resting rates under 50 can be normal during sleep in young healthy adults and athletes). Sleep apnea, OSA (obstructive sleep apnea; hint refers to apnea screening per the pathway source note).
Not this hint: slow rate while awake, bradycardia with symptoms (dizziness, syncope), "sleep" used for another idea ("sleep well", "poor sleep").
Ambiguous: "OSA" and "night" (night sweats, night shift).
SP-brady (full text): "If bradycardia occurs during sleep, an evaluation for sleep apnea should be pursued. Nocturnal bradycardia in isolation is not an indication for permanent pacing". This supports keeping the slow-during-sleep finding as a card hint that does not change the tier.

## Hard-to-control BP / cholesterol flags (reason: hard_to_control_bp_chol)

### Blood pressure wording (shared)
Labels and forms: blood pressure, BP, systolic (SBP, "top number"), diastolic (DBP, "bottom number"), written "systolic/diastolic" e.g. "190/124", unit mm Hg / mmHg (AHA-bp); MAP (W-hte, W-hypotn). Terms: severe hypertension, hypertensive crisis, hypertensive urgency (older term for severe elevation without acute organ damage), hypertensive emergency, malignant hypertension (older), "BP over 180/120", "BP greater than 180/120", "BP above 180 systolic", "SBP in the 190s" (AHA-bp: higher than 180 and/or higher than 120; W-hte: urgency vs emergency, older term malignant hypertension). Measurement settings: office, clinic, home, ambulatory, "repeat BP", "BP recheck after 5 minutes" (AHA-bp advises waiting a minute and retaking the reading first).
Abbreviations: BP, SBP, DBP, HTN, HTN urgency, HTN emergency, HMOD (hypertension-mediated organ damage), MAP (HMOD, MAP per W-hte; SBP/DBP not defined in opened sources).

## bp_emergency (BP over 180/120 with signs of organ damage)
Terms (organ-damage symptoms): chest pain, shortness of breath, back pain, numbness, weakness, change in vision, difficulty speaking (AHA-bp); severe headache, confusion or altered mental status, agitation, vertigo, fainting, abnormal sensations, stroke, pulmonary edema, heart failure, blood or protein in urine, reduced urine output, retinal hemorrhage, papilledema, nausea/vomiting, nosebleeds that are hard to stop (W-hte). Lay: blurry vision, double vision, "worst headache", slurred speech (slurred per CDC-stroke; others (no source found - common usage, needs clinician check)).
Abbreviations: HTN emergency, HMOD, AMS (altered mental status; no source found - common usage, needs clinician check).
Not this flag: severe BP elevation without symptoms (the separate urgent flag; AHA-bp: contact your professional and retake in one minute); a single office reading likely transient or white-coat (W-hte lists white-coat only as related); symptoms attributed to another cause; older "hypertensive urgency" wording applies to elevation without organ damage (W-hte); BP in pregnancy has lower thresholds (W-hte: systolic above 160 or diastolic above 110).
Ambiguous: "weakness" (generalized fatigue vs focal); "headache" (chronic); "180/120" appearing as a target or threshold in counseling text rather than a measured reading; "over" can mean "BP over HR" or "over 180".

## bp_severe_no_symptoms (BP over 180/120 without organ damage)
Terms: see Blood pressure wording; "severe hypertension", "hypertensive urgency" (older term), "asymptomatic severe hypertension", "markedly elevated BP", "BP 190/110", "BP 178/122" (W-hte, AHA-bp).
Not this flag: normal or controlled readings quoted as a goal ("goal under 130/80"); readings in the past outside the window; ambulatory/home averages that are lower; hypertensive emergency (if any organ-damage symptom is present the emergency flag applies); a patient-reported home reading without a device (clinician decision); "BP 180" as a pulse or weight.
Ambiguous: "SBP", "DBP" shorthand; "180/120" could be a date-like or fraction pattern; "over" wording.

## bp_low_potassium (card hint: high BP with low potassium)
Terms: hypokalemia, hypokalaemia, low potassium, "K 3.2", "K+ low", serum potassium, "potassium of 3.1 mmol/L" (units mmol/L or mEq/L, equivalent for potassium) - "K", "K+" shorthand; "hypokalemia" spelled out (UK hypokalaemia per W-lqts lists "hypokalaemia"). Aldosterone/renin: primary aldosteronism, hyperaldosteronism, Conn syndrome, aldosterone-renin ratio, ARR, PAC (plasma aldosterone concentration), PRA (plasma renin activity) - Conn syndrome and ARR/PAC/PRA (no source found - common usage, needs clinician check).
Abbreviations: K, K+, HTN, ARR, PA (primary aldosteronism).
Not this hint: potassium normal or high; low potassium from diuretics (a cause, still low potassium) - the pathway guideline note treats both spontaneous and diuretic-induced hypokalemia as reasons to screen; "K" in other contexts (ketamine, Kalium); history of hypokalemia now resolved; PA = also "pulmonary artery", "physician assistant" (ambiguous).
Ambiguous: "K"; "PA".

## Cross-flag ambiguity summary
- SOB: shortness of breath; used with at-rest wording for hf_breathless_rest and with exertion wording elsewhere.
- LOC: loss of consciousness (syncope flags) vs level of consciousness; no opened source settled the abbreviation.
- Brady / tachy: shorthand for bradycardia / tachycardia (no opened source); "pulse ox" = oxygen saturation (W-oximetry).
- HR: heart rate vs "hour(s)" (abbreviation list) vs hazard ratio.
- PE: pulmonary embolism vs physical exam; CP: chest pain vs cerebral palsy / "CPK/CPR" in the abbreviation list.
- TIA matches inside ordinary words; WPW and "delta wave" have unrelated uses.
- PND: paroxysmal nocturnal dyspnea.
- RVR: rapid ventricular response (W-af).
- BNP vs NT-proBNP differ in assay and cut-offs; ANP is different.
- "New" and "ongoing" require context (prior ECG, timing).

## Gaps (sources not opened)
- LITFL AV block, WPW, MI/STEMI ECG pages returned HTTP 403; NCBI StatPearls pages (syncope, AV block, bradycardia, ACS) returned a CAPTCHA; MedlinePlus BNP test pages returned 404; AHA heart block page returned 404; Wikipedia "Level of consciousness (medicine)" returned 404.
- No opened source for medical abbreviation lists (SOB, LOC, SBP, CP, BLE, NTG, etc.); those entries are marked common usage.
- NICE CKS pages and guideline texts were not used for this vocabulary file.
