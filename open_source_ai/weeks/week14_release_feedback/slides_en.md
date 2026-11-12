---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 14"
footer: "Wonkwang University Chatbot and Public Evaluation"
---

# Week 14
## Wonkwang University Chatbot and Public Evaluation

3 × 60-minute blocks

Each block: 20 min explanation/demo + 30 min lab + 10 min break

---

## This Week

| Block | 20 min explanation | 30 min lab |
|---|---|---|
| 1 | Task rules, input and response | Run the baseline chatbot |
| 2 | 20 public items and scoring | Baseline evaluation and failure review |
| 3 | One change and evidence | Reevaluate and draft the report |

Keep using the single Week 14 project. Performance and report grades stay separate.

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## Final task and chatbot run

---

## 0–3 min · Two separate grade components

Build a chatbot that introduces Wonkwang University and evaluate it with the shared tool.

| Grade component | Evidence |
|---|---|
| Presentation score | AI performance on hidden questions in Week 15 |
| Report score | A separately assessed development report |

Apply the existing presentation and report weights separately.
Speaking skill and presentation duration earn no points. School points and deadlines will be announced.

---

## 3–7 min · Five summaries of official sources

| Document ID | Official summary topic |
|---|---|
| `wku-location` | Location, address, contact details |
| `wku-values` | Motto, educational aims, founding spirit |
| `wku-symbols` | School color, bird, tree, flower |
| `wku-history` | Early history |
| `wku-services` | Website service links |

[Shared documents and sources](examples/src/shared/data/README.md): v1, checked 2026-11-12.
These five summaries define the evaluation scope. Do not guess beyond them.

---

## 7–11 min · One input and three return fields

`student_bot.answer(question)` takes a question string and returns a dictionary.
Example for a question asking for both the city and school bird:

```python
{"answers": ["익산시", "봉황"],
 "sources": ["wku-location", "wku-symbols"], "abstain": False}
```

Return short facts in `answers` and document IDs, not URLs, in `sources`.
`abstain` is a Boolean: `false` in JSON. The string `"false"` is invalid.
Each evaluation call is independent. [Evaluation specification](evaluation_spec.md)

---

## 11–15 min · Repeated questions in the terminal

Run these commands inside Week 14's `examples/` directory.

```sh
uv sync
uv run ex01
```

Enter a question, read the response, then enter another question.
Empty input is skipped. Use `/bye` or Ctrl+C to exit.
Repeated input does not imply conversation memory. Evaluation handles one question at a time.

---

## 15–18 min · One Python 3.12 project

Inspect the initial project command and the structure it creates.

```sh
uv init --package --python 3.12 --vcs none wku-bot
```

Class work continues in the single supplied `examples/` project.
Locate `.python-version`, `pyproject.toml`, `src/`, and `uv.lock`.
`main()` starts a command. `uv_build` builds the package for installation.
Run `uv sync` again after changing `[project.scripts]`.

---

## 18–20 min · Block 1 lab handoff

Use `ex01` in the [run guide](examples/README.md).

1. Find a question and its supporting document ID in the summaries.
2. Enter two questions in sequence. Read the facts, sources, and abstention flag.
3. Check empty input and normal exit, then record what happened.

Work for 30 minutes, then take a 10-minute break. Next, evaluate the same function.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## Public evaluation and baseline score

---

## 0–3 min · Twenty public practice questions

| Type | Count | What it checks |
|---|---:|---|
| `fact` | 12 | Requested facts and sources |
| `composite` | 4 | Missing or extra facts in a combined question |
| `unknown` | 4 | Abstention when the documents cannot answer |

The public dataset and evaluation tool are provided together for practice.
Week 15 uses hidden questions with the same tool and conditions.
Hidden questions and answers are not included in the course materials.

---

## 3–7 min · Fact set F1

Let G be the expected fact set and P the returned fact set.

```text
Fact F1 = 2 × matching facts / (size of P + size of G)
Expected {A, B}, returned {A}       : 2 × 1 / (1 + 2) = 2/3
Expected {A, B}, returned {A, B, C} : 2 × 2 / (3 + 2) = 4/5
```

Both missing and extra facts matter. Order and duplicates add no points.
Matching normalizes NFKC, case, whitespace, and final periods, then applies allowed `aliases`.
An arbitrary paraphrase is not automatically a match.

---

## 7–11 min · Source credit and item score

`fact` and `composite` use the same formula.

```text
Item score = 80 × fact set F1 + 20 × source set F1
If fact F1 is 0, source credit is also 0
```

Source F1 compares expected and returned document ID sets.
One of two facts, with all correct sources, earns about 73.33 points.

**80/20 belongs inside this performance metric.** It does not combine performance and report grades.

---

## 11–15 min · Abstention and zero-score cases

Full-credit response for an `unknown` question:

```python
{"answers": [], "sources": [], "abstain": True}
```

All three conditions are required for 100 points. Otherwise, the item earns 0.
Format errors, execution errors, and over 30 seconds earn 0. Warm-up is excluded.
The overall score averages every item, including zeros.
Student PC performance earns no points. Response time is reported only.

---

## 15–18 min · Running the public evaluation

Run inside the same `examples/` directory.

```sh
uv run ex02
# Alias for the same public evaluation
uv run evaluate
```

Both `ex01` and the evaluator call `student_bot.answer`.
Record the initial overall mean, results by type, and failed items.
Compare one output row with the formula in the [evaluation specification](evaluation_spec.md).

---

## 18–20 min · Block 2 lab handoff

1. Run all 20 public questions and record the baseline score.
2. Check fact F1 and source F1 for one fact or composite item.
3. Inspect an unknown response and classify an observed failure. If none, try a new question.

Missing fact / extra fact / wrong source / wrong abstention / format or timeout

Work for 30 minutes, then take a 10-minute break. Leave the answer key and evaluator unchanged.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## One change and report evidence

---

## 0–3 min · Improving the shared answer function

```text
ex01  Terminal chatbot ─┐
ex02  Public evaluator ─┼─ student_bot.answer(question)
ex03  Improvement run  ─┘
```

`ex03` checks the same function with repeated terminal input.
Change one element: `TOP_K` or the prompt in `src/student_bot/__init__.py`.
Improve how questions use documents rather than memorizing answers by public item ID.

---

## 3–7 min · One change at a time

| Observed failure | A possible change |
|---|---|
| One requested fact is missing | Collect each fact requested by the question |
| Unrelated documents appear as sources | Return only documents supporting the answer |
| The bot invents information outside the documents | Abstain when evidence is absent |

Choose one failure. Record the code location and expected effect first.
Keep model and evaluation settings fixed. A new UI or framework is optional.

---

## 7–11 min · Trying the change and evaluating again

```sh
uv run ex03
uv run ex02
```

In `ex03`, enter the target question followed by a different question.
Check empty input, exit, and the three return fields.
Then rerun the complete set of 20 public questions.
Compare the mean, changes by type, and newly failing items with the baseline.

---

## 11–15 min · Comparison conditions and failure records

Keep documents, questions, evaluator, model, and generation settings fixed.
Record the changed answer logic and the settings that stayed unchanged.

| Record | What to include |
|---|---|
| Before/after values | Measured overall mean, results by type, response time |
| Failure | Question, actual return value, error and supporting evidence |
| Choice | Why the change was kept and why an alternative was rejected |

Record unchanged or lower scores too. Do not invent measurements.

---

## 15–18 min · Evidence for the development report

Fill the [report template](report_template.md) with evidence from the lab.

- Baseline and changes: the file and behavior you modified
- Before/after values, failures, and choices: linked to actual output
- Reproduction, sources, and AI use: commands, documents, assistance and checks

The public score is practice evidence. Hidden evaluation determines the presentation score next week.
The development report receives a separate report grade.

---

## 18–20 min · Block 3 lab handoff

1. Change one part of the answer function and check it with `ex03`.
2. Rerun the same 20 questions with `ex02` and keep both results.
3. Record the reason, remaining limits, reproduction steps, and AI use in the report.

Work for 30 minutes, then take a 10-minute break.
Week 15 uses the same tool for hidden final evaluation and completes the report.
