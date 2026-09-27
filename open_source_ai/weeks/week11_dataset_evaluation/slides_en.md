---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 11"
footer: "Dataset Curation and Model Evaluation"
---

# Week 11
## Dataset Curation and Model Evaluation

**3 × 60-minute blocks**<br>
Each block: 20 min explanation/demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Sessions

| Session | 20 min explanation/demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Data pipeline and data cards | Clean, mask, and split raw data |
| Block 2 | Baselines and metrics — how do we prove it got better? | Baseline vs. LoRA quantitative comparison |
| Block 3 | Qualitative evaluation and failure analysis | Manual scoring and a failure analysis report |

This week's question: **Is my data trustworthy and safe, and what proves the model actually improved?**

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## Data Pipeline and Data Cards

---

## 0–3 min · A Model Resembles Its Data

```text
Collect ──▶ Clean ──▶ Deduplicate ──▶ PII check ──▶ Split ──▶ Data card
raw.jsonl    blanks/normalize   exact/near      mask/remove    train/val/test
48 records
```

- Week 10's adapter learned about 50 records from `sample_sft.jsonl` **exactly as they were**
- If the data has a phone number in it, the model memorizes the phone number
- If the same question appears in both training and evaluation, the score gets inflated

**Question:** Given 48 records from a teammate, what should you suspect first?

---

## 3–6 min · Cleaning: What to Remove

| Check | Rule | In the example |
|---|---|---|
| Required fields | id/instruction/output not empty | q040 has empty output |
| Normalization | NFKC, collapse repeated spaces | `uv sync ` vs `uv sync` |
| Exact duplicates | key from lowercased/space/punctuation-stripped instruction | q009 = q003, q021 = q014 |
| Near duplicates | instruction+output char 2-gram Jaccard ≥ 0.8 | q033 ≈ q027 (0.94) |

- The threshold is **set by looking at the data** — at 0.95, q033 would survive
- Log every removal with its reason in `clean_report.json`

---

## 6–9 min · Splitting and Leakage

```text
44 records ─ train_test_split(seed 42) ─▶  train 20  │  val 4  │  test 20
                                            training    tuning    sealed
```

- `train` updates weights, `val` picks hyperparameters, `test` is seen **only once**
- Leakage: if the same question appears in two splits, the test score is memorization, not skill — `leak_check` finds it by the normalized key
- Record the seed, or you can't reproduce the same split

**Question:** What goes wrong if you deduplicate **after** splitting instead of before?

---

## 9–12 min · Personal Info, Copyright, and Bias

| Type | Pattern the regex looks for | Example value (fake) |
|---|---|---|
| PHONE | Korean mobile numbers `010`/`011`/`016`–`019` (separators optional) | q012 output |
| EMAIL | `name@domain.tld` | q025 instruction |
| RRN | `######-#######`, 7th digit 1–4 | q038 output |

- A regex has **no context**: it can flag an illustrative example number (q038, a false positive) and miss a number in an unusual shape (a false negative)
- A human re-reads the detection list and records the judgment **in the data card**
- Copyright: don't train on documents with no known source or license · Bias: count the distribution of the `source` column

---

## 12–15 min · The Data Card: Letting Others Judge

| Section | What to write | Source file |
|---|---|---|
| Overview & provenance | intended/prohibited uses, counts and licenses per source | `raw.jsonl` |
| Composition & cleaning | counts per stage, dedup rule and threshold, removed ids | `clean_report.json` |
| Personal info | detections by type, actions taken, false-positive calls | `pii_report.json` |
| Split | seed, counts, leakage, overlap with external data | `split_report.json` |
| Bias & limits | topic distribution, effects of fixed formatting | direct observation |

**Every number is copied straight from a report JSON file.** Week 14's Model Card "Training Data" section points back to this card.

---

## 15–17 min · Demo: Running the Three Scripts Together

```powershell
uv run python clean.py                      # 48 → 44, 4 removed with reasons
uv run python pii_check.py --action report  # PHONE 1 · EMAIL 1 · RRN 1
uv run python pii_check.py                  # masked to [PHONE] → masked.jsonl
uv run python split.py                      # train 20 / val 4 / test 20, leakage 0
```

```text
  - q009: 정확 중복(instruction) ← q003
  - q033: 근사 중복(instruction+output) ← q027 (유사도 0.94)
  - q040: 필수 필드 비어 있음: output
```

**Question:** If you switch to `--seed 7`, which items land in `test`? Can you know in advance?

---

## 17–20 min · Handing Off to the Lab

[Block 1 lab — Clean, mask, and split raw data](lab.md#1교시-실습--원시-데이터를-정제마스킹분할하기)

Done when:

1. You can state the ids and reasons for the 4 removals in `clean_report.json`, plus one sentence on the difference between threshold 0.95 vs. 0.8
2. You've made a false-positive/false-negative call and action for each of the 3 hits in `pii_report.json`, and read the leakage count (0) and overlap count in `split_report.json`
3. You've filled `DATA_CARD.md`'s 7 sections with values from the reports

30 min lab, then a 10 min break, then Block 2.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## Baselines and Metrics — How Do We Prove It Got Better?

---

## 0–3 min · "It Got Better" Needs a Baseline

```text
run-001.md : format compliance 5/5 after applying the adapter   ← what baseline? which items?
this week  : base 0/20 → lora 17/20 (test, greedy, seed 42, same system prompt)
```

- Baseline: the **zero-shot** score of the untrained model
- Hold constant across the comparison: same test split, same system prompt, greedy decoding, same seed, same `max_new_tokens`
- Change even one of these and you're no longer comparing "better," you're comparing "different"

**Question:** What was wrong with the 5/5 score from Week 10's 5-item `eval_prompts.json`?

---

## 3–6 min · Classification Metrics: Start From the Confusion Matrix

```text
              Predicted 1   Predicted 0
Actual 1          TP            FN
Actual 0          FP            TN

accuracy = (TP+TN)/total   precision = TP/(TP+FP)   recall = TP/(TP+FN)
F1 = 2·P·R/(P+R)
```

- Use this for **yes/no** judgments, like "did it follow the format?"
- With a 14:6 imbalance, predicting all 1s still gives accuracy 0.7 — recall 1.0, precision 0.7, and zero 0s ever found
- `metrics.py --demo`: accuracy 0.8, precision 0.857, recall 0.857

---

## 6–10 min · Generation Metrics: What Each One Misses

| Metric | Computation | What it misses |
|---|---|---|
| Exact match | identical string after normalization | 0 even if only the wording differs |
| Keyword coverage | fraction of expected keywords present | a nonsense answer that just stuffs in keywords |
| Similarity | character 2-gram Jaccard | can score high even with the opposite meaning |
| Format compliance | 3 lines (Key:/Why:/Next:), 400 chars | **passes even if the content is wrong** |
| Korean ratio / repetition | character statistics | short English commands |

- Metrics are **symptom detectors**. The verdict is a human's job (Block 3)
- For open-ended generation with more than one right answer, exact match is close to 0 — don't be surprised

---

## 10–13 min · Letting an LLM Grade

- LLM-as-judge: another model scores the output using a judging prompt — fast and cheap
- Known biases: favors **longer answers, confident answers, and models from its own family**; also order effects
- To use it responsibly: have a human score 20 sample items first and record the **agreement rate**, and put the rubric directly in the judge prompt
- This course's default: automatic metrics (symptoms) + human scoring (verdict). LLM judging is an extension, not the baseline

**Question:** The judge model gave 2 points, saying "the format is perfect." What should you check?

---

## 13–15 min · Benchmark Contamination: A Model That Saw the Exam Early

```text
Week 10 sample_sft.jsonl : "When should I use torch.no_grad?"   ← used for LoRA training
Week 11 test.jsonl q023  : "When should I use torch.no_grad?"   ← the same question
```

- Sometimes a high public benchmark score just means "the training data contained the exam"
- `split.py --against training_file.jsonl` measures similarity between test items and training questions and reports overlapping ids
- Recomputing the score with overlapping items excluded via `evaluate.py --exclude` gets you closer to a generalization score
- `test` is sealed right after the split — pick hyperparameters using **val** only

---

## 15–17 min · Demo: Running the Scorer Without a Model

```powershell
uv run python evaluate.py --predictions data/sample_predictions/base.json data/sample_predictions/lora.json
```

```text
| run  | n  | keyword rate | format rate | avg similarity | repeats |
| base | 20 | 0.400        | 0.000       | 0.116           | 1       |
| lora | 20 | 0.825        | 0.850       | 0.513           | 1       |
```

- The samples are **fabricated outputs for the textbook's own verification** — real models generate with `--adapter`
- `items` inside `eval-*.json` keeps every item's output and metrics

**Question:** lora's q043 passes the format check but scores 0 on keywords. Which metric should you trust?

---

## 17–20 min · Handing Off to the Lab

[Block 2 lab — Baseline vs. LoRA quantitative comparison](lab.md#2교시-실습--기준선-vs-lora-정량-비교)

Done when:

1. You have the prediction-mode table and the id/reason for one item that "passed format but got the content wrong"
2. You have model-mode `eval-*.json` (baseline + adapter, or baseline alone) and a comparison table
3. You have the score gap between "all items" and "overlap items excluded via `--against`"

30 min lab, then a 10 min break, then Block 3.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## Qualitative Evaluation and Failure Analysis

---

## 0–3 min · What the Numbers Don't Say

```text
q043 "Can I make the CHANGELOG by copying the commit log?"
lora: Key: Yes, you can copy the commit log directly.
      Why: Commit messages are essentially the change history.
      Next: Auto-generate CHANGELOG.md with `git log --changelog`.
Automatic metrics: format OK · keywords 0/2 · similarity 0.19
```

- The format is perfect and it even learned the tone. But it's describing a **command that doesn't exist**
- A 0.85 format-compliance rate is evidence that "it learned the tone," not that "it's telling the truth"

**Question:** If this answer shipped to a real service, what would the user end up doing?

---

## 3–6 min · A Classification Table for Error Types

| Code | Type | Signal | Sample id |
|---|---|---|---|
| H | Hallucination | nonexistent command, wrong facts, 0 keywords | q043 |
| F | Format violation | missing header, wrong line count, over 400 chars | q031, q027 |
| R | Refusal / evasion | "I can't answer that" | q024 |
| P | Repetition | the same sentence reappears | q038 |
| L | Language mixing | Korean ratio drops, foreign-language sentences | q035 |
| S | Safety / PII | `[PHONE]` token reproduced, harmful content | needs review |

- One output can carry several codes — record all of them
- The **count per type** determines the order in which you fix things

---

## 6–9 min · A 3-Point Rubric and Scoring Consistency

| Score | Meaning | Order of judgment |
|---:|---|---|
| 0 | Unacceptable | wrong info, off-topic, refusal, repetition, or empty — any one of these |
| 1 | Partial | content is correct but format is violated, incomplete, or padded |
| 2 | Acceptable | correct content, correct format, no wrong information |

- Judge **starting from 0**: if the information is wrong, a perfect format still scores 0
- Before scoring, agree with your partner in one sentence each on what counts as "wrong information" and "incomplete"
- Score the same 5 items independently and record the **agreement rate** — at 3/5 or below, fix the criteria and redo it

**Question:** What changes if you score while looking at the automatic-metrics column?

---

## 9–12 min · Checking for Harmful Output and PII Leakage

```text
Training data (after masking): "Next: if that still doesn't work, contact the TA at [PHONE]."

Check 1  Does the output reproduce [PHONE]/[EMAIL]/[RRN] tokens as-is?   → it learned the masking artifact
Check 2  Does it invent a number-shaped answer to "give me the TA's number"?   → hallucination + safety (H, S)
Check 3  If it trained on unmasked data, does a real number show up?          → discard and retrain immediately
```

- Run the regex check **on the output too** (reuse the patterns from `pii_check.py`)
- Keep 2–3 leading questions separate from `test` and ask the same ones every run
- Log any issue found under the data card's "Limitations" section and the failure analysis's "Safety check" section

---

## 12–15 min · The Improvement Loop: From Failure Analysis to run-002

```text
Evaluate (run-001) ──▶ Failure analysis: counts per type + 3 cases (symptom, hypothesis, evidence, fix)
     ▲                                          │
     └── Re-evaluate (same test) ◀── Retrain (run-002) ◀── change exactly one thing
```

- The hypothesis is one of four: **data** (missing/contradictory/inconsistent format) / **training setup** (epochs, lr) / **decoding** (length, repetition) / **prompt**
- Find the evidence: if the baseline is also wrong, the data has no knowledge of it; if the baseline is right but LoRA is wrong, training broke it
- Write your success criteria **as numbers**, in advance: "cases 1–3 score 2, format rate 0.85→0.95, 0 repeats"

---

## 15–17 min · Preparing for the 3rd Integrative Assignment

- (a) **2 or more** experiment logs: `experiments/run-001.md` (Week 10) + `run-002.md`, `DATA_CARD.md`, `eval-*.json`, `FAILURE_ANALYSIS.md`
- (b) AI service beta: built in Week 12 with `/health`, `/chat`, and a UI
- (c) Evidence of individual contribution: this week's data card, scoring sheet, and failure analysis also go in as **per-person commits**
- This week's "Next experiment" in `FAILURE_ANALYSIS.md` becomes run-002's "Purpose" directly

**Question:** If run-002 turns out worse than run-001, should you delete it from the record?

---

## 17–20 min · Handing Off to the Lab

[Block 3 lab — Manual scoring and a failure analysis report](lab.md#3교시-실습--수동-채점과-실패-분석-보고)

Done when:

1. `scoring-*.md` has scores, error types, and notes for 20 items, plus your 5-item agreement rate with a partner
2. `FAILURE_ANALYSIS.md` has 3 cases of different types (symptom, hypothesis, evidence, fix, how to verify)
3. You have your safety-check results and a "change exactly one thing" next experiment with a numeric success criterion

30 min lab, then a 10 min break. Leads into this week's wrap-up.

---

## This Week's Wrap-Up

```text
Data:       clean → deduplicate → PII check → split (sealed) → data card
Evaluation: baseline + matched conditions + automatic metrics (symptoms) + human scoring (verdict) + failure analysis → run-002
```

- "The data is trustworthy" is backed by **report JSON files and the data card**
- "It got better" is backed by **numbers from the baseline on the same test split**, plus a scoring sheet noting what the numbers missed
- Next week (`week12_ai_service_deploy`): wrap this model in a FastAPI/Gradio service
