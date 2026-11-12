---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 15"
footer: "Hidden Final Evaluation and Development Report"
---

# Week 15
## Hidden Final Evaluation and Development Report

3 × 60-minute blocks

Each block: 20 min explanation/demo + 30 min lab + 10 min break

---

## This Week

| Block | 20 min explanation | 30 min lab |
|---|---|---|
| 1 | Submission and public results | Public check and settings review |
| 2 | Hidden evaluation procedure | Evaluation and implementation notes |
| 3 | Report evidence and criteria | Complete the report and submission check |

Keep using the single Week 14 project. Performance and report grades stay separate.

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## Preparing the final evaluation

---

## 0–3 min · Presentation and report grades

| Grade component | Evidence this week |
|---|---|
| Presentation score | Submitted chatbot's AI performance on hidden questions |
| Report score | Implementation, changes, and verification in the development report |

Apply the existing presentation and report weights separately.
Speaking skill and presentation duration earn no points.
School points, deadlines, and submission routes follow the official announcement.

---

## 3–7 min · Same tool, hidden questions

Apply Week 14's [evaluation specification](../week14_release_feedback/evaluation_spec.md) unchanged.

- API: `student_bot.answer(question)`
- Return fields: `answers`, `sources`, `abstain`
- Fixed documents, model, generation settings, evaluator, and normalization
- Final questions and answers stay private

`uv run evaluate` is an alias for public practice evaluation.
Running it as a student does not complete the hidden final evaluation.

---

## 7–11 min · Submission and execution settings

The evaluator must run the same files that the report describes.

| Check | Evidence to retain |
|---|---|
| Code | Submission identifier and edits to `student_bot.answer` |
| Project | Python 3.12, `pyproject.toml`, `uv.lock` |
| Evaluation settings | Fixed document, evaluator, model, and generation versions |
| Execution | Returned fields and errors for a given input |

Keep the submitted code unchanged during final evaluation. Record environment issues for the instructor.

---

## 11–15 min · Reproducing the existing project

Review the original structure. Do not reinitialize the existing directory.

```sh
uv init --package --python 3.12 --vcs none wku-bot
```

Continue using the same project in Week 14's `examples/` directory.
Check `.python-version`, `src/`, `pyproject.toml`, and `uv.lock`.
Scripts map commands to `main()`. `uv_build` installs the package.
Use `uv sync --frozen` for reproduction, or `uv sync` after script changes.

---

## 15–18 min · Public check before final evaluation

Run inside the same project.

```sh
uv sync --frozen
uv run ex03
uv run ex02
```

Check repeated questions, empty input, exit, and return format.
Compare the public results with Week 14 and record the submission identifier.
Student PC speed is not a grade component. Report response time and the environment.

---

## 18–20 min · Block 1 lab handoff

Continue with the [Week 14 run guide](../week14_release_feedback/examples/README.md).

1. Check the code and environment files you will submit.
2. Rerun public evaluation and associate the results with that submission.
3. Record the command, message, and stage of any execution error.

Work for 30 minutes, then take a 10-minute break. Final evaluation uses this submission.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## Hidden performance evaluation

---

## 0–3 min · Running the hidden evaluation

The evaluator applies the same tool to the fixed submission.

1. Check the code and fixed environment.
2. Pass hidden questions one at a time to `student_bot.answer`.
3. Score format, facts, sources, and abstention using the same rules.
4. Retain item scores, the overall mean, and execution status.

Do not copy hidden questions or answers into student code or public materials.
Students may explain the procedure. Speaking skill and duration earn no points.

---

## 3–7 min · Fixed final evaluation conditions

| Fixed element | Rule |
|---|---|
| Input and evidence | Same dataset version and five document summaries |
| Execution | Same evaluator, model, generation settings, and environment |
| Matching | Same aliases, NFKC, whitespace rules, and timeout |
| Aggregation | Arithmetic mean of every item, including zeros |

The evaluator applies the same conditions to every submission.
Student PC performance earns no points. Response time is recorded only.

---

## 7–11 min · Checking the item score rules

| Item or status | Score |
|---|---|
| `fact`, `composite` | 80 × fact F1 + 20 × source F1 |
| Fact F1 is 0 | Source credit is also 0 |
| `unknown` | 100 only for `true` abstention and two empty lists |
| Format/execution error or over 30 seconds | 0 for that item |

Set F1 measures overlap with expected sets, after aliases and normalization.
80/20 weights the item metric. It does not combine performance and report grades.

---

## 11–15 min · Errors and evaluation results

- Invalid format or timeout: retain the item with its zero score.
- Fact, source, or abstention error: retain the evaluator's result.
- Installation or environment failure: report the stage and message.

Do not change scores arbitrarily by confusing environment failures with wrong answers.
If a rerun is needed, the instructor applies the same procedure and records why.
Students do not edit submissions after seeing hidden answers.

---

## 15–18 min · Reviewing the performance result

Results link the submission identifier and settings to item outcomes and the overall mean.

Label public practice and hidden final scores separately.
A strong public score does not replace the hidden final score.
Report response time with its environment. There is no speed bonus.

Include only results released by the evaluator in the report.
Keep hidden questions and answers out of public repositories and report examples.

---

## 18–20 min · Block 2 lab handoff

1. Participate in the instructor's hidden evaluation with the fixed submission.
2. Record its actual state: complete, in progress, or environment failure.
3. Check that any released result belongs to your submission.

While waiting, organize public experiment records and the report.
Do not invent a score for an unfinished evaluation.
Work for 30 minutes, then take a 10-minute break.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## Development report

---

## 0–3 min · Report structure

Compare the [report template](../week14_release_feedback/report_template.md) with the [rubric](assignment_rubric.md).

| Report criterion | Points | Evidence |
|---|---:|---|
| Purpose and design | 25 | Question/data scope and choices |
| Implementation understanding | 25 | Processing flow and code you checked |
| Improvement experiments | 30 | Baseline, changes, same-condition results |
| Limits, reproduction, sources | 20 | Limits, commands, sources and AI use |

This is the report's own /100 rubric. Existing school report points still apply.
It is separate from performance. Length and speaking skill are not criteria.

---

## 3–7 min · Connecting changes to measurements

| Change | Before | After | Evidence |
|---|---|---|---|
| Logic you changed | Measured value | Measured value | Output from the same public evaluation |

Name the baseline, edited file/function, and reason first.
Check affected items and results by type as well as the overall mean.
State whether questions, documents, model, and generation settings were fixed.
Mark unmeasured cells as “not measured” and explain why.

---

## 7–11 min · Failures and choices

Place one public question, the actual return value, and expected evidence side by side.

Name the missing fact or incorrect document ID instead of just saying “low accuracy.”
Separate confirmed causes from guesses and describe the next check.

Explain why a change was kept, reverted, or not attempted.
Record real attempts and checks even when scores do not improve.
Use public failure examples. Do not copy hidden answers into the report.

---

## 11–15 min · Reproduction, sources, and AI use

- Reproduction: submission, Python 3.12, dependencies, commands, actual results
- Sources: supplied document IDs and official URLs, plus other references
- AI use: tool, assisted files/scope, and your edits and checks

Include files an AI tool created or edited directly.
Distinguish assistance from the work you can explain and verify.
If no AI tool was used, say so. Exclude secret keys and personal information.

---

## 15–18 min · Checking the two submissions

| Submission | What to check |
|---|---|
| Chatbot and performance evaluation | Link to final results and any unfinished state |
| Development report | Baseline, edits, values, failures, reasons, reproduction, sources, AI use |

Report and presentation grades use their respective evidence separately.
Apply the existing presentation and report weights separately.
Check the official announcement for points, deadlines, and submission routes.

---

## 18–20 min · Block 3 lab handoff

1. Complete the report with actual changes, results, failures, and reasons.
2. Check commands, sources, AI assistance, and your own verification.
3. Confirm that code, results, and report describe the same submission.

Keep unmeasured values and pending evaluation states explicit.
Submit according to the school's official announcement. Finish with a 10-minute break after the 30-minute lab.
