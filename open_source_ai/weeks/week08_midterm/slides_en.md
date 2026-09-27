---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 8"
footer: "Midterm Assessment and Project 2"
---

# Week 8
## Midterm Assessment and Project 2

**Three 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Session | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | How the hands-on exam is structured, and how to read a mock question | Mock exam A: recovering a project and answering discriminating questions |
| Block 2 | Diagnostic points and the rubric for local-AI hands-on tasks | Mock exam B: adding a client feature and interpreting the results |
| Block 3 | Running the exam, and final checks on Project 2 | Individual hands-on exam and fallback procedures |

This week's question: **can you reproduce and explain weeks 1–7 on your own?**

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## How the Hands-On Exam Is Structured, and How to Read a Mock Question

---

## 0–3 min · This Week Is Reproduction, Not New Features

```text
Weeks 1–7 labs ──▶ Can you rebuild them alone?          → hands-on exam
Weeks 5–7 combined ──▶ Did you package it for others to reproduce? → Project 2
```

- Exam: Blocks 1–2 are public, matched-format mock exams -> Block 3 is the individual exam (a closed packet).
- Project: license/source analysis + RAG mini-project + reproduction steps.
- This material contains no actual exam questions or answers.

**Question:** Of everything you've built over 7 weeks, what could you rebuild right now, starting from an empty folder?

---

## 3–6 min · Six Assessment Areas

| Area | What it checks |
|---|---|
| Git & collaboration | Branches, commits, conflict/PR judgment, secret separation |
| License & sourcing | Permissive/copyleft, model & data conditions, SPDX, `SOURCES.md` |
| uv reproducibility | Restoring `pyproject`, sync/run, `.gitignore` / `.env.example` |
| Ollama execution & API | Request JSON, `stream`/`think`/`options`, metadata, failure handling |
| HF pipeline & model cards | Reading label/score/device/warnings, intended use and limits |
| Verification & explanation | Reproducing success/failure paths, `outputs/`, evidence-backed reasoning |

See [exam_structure.md](exam_structure.md) for the detailed table.

---

## 6–9 min · Rules: Allowed Material, AI Tools, Submission

- Allowed material: public course materials, your own repository, official docs — scope is finalized by the exam notice.
- AI tools: allowed scope and how to disclose their use follow the school's official documents.
- Submission: the designated files + your final commit id + a short note (what and why).
- Instructions are the same for everyone; there are no individual hints that amount to answers.
- Student code and scores are never published to a public repository.

**Key point:** the grader looks at **reproducible files and commits**, not screenshots.

---

## 9–12 min · The Order for Reading a Question

```text
Requirement       "Fix it so uv sync works"
    ↓
Completion check  "uv run python report.py produces outputs/report.json"
    ↓
Verify order      "1) uv sync  2) uv run  3) open the file  4) git ls-files"
```

- Turn the completion check into a checklist before you touch any code.
- Fixing the verification commands in advance lets you *show* "it's done" to someone else.

**Question:** What do you lose by fixing something not covered by the completion check first?

---

## 12–15 min · Mock A Preview: A Broken Project

```powershell
uv sync
# TOML parse error at line 8 ... missing comma between array elements
```

- Defect 1: a `pyproject.toml` syntax error — visible on the very first run.
- Defect 2: a misspelled table name — sync pretends to succeed, but `import` fails.
- Defect 3: a bad `requires-python` value — only appears after defect 2 is fixed.
- Defect 4: no `.gitignore` and `.env` committed — no command error, but it's sitting in history.

Errors appear **one at a time**. Fix one, rerun, read the next.

---

## 15–17 min · A One-Line Rationale Is the Score on Discriminating Questions

| Weak answer | Strong answer |
|---|---|
| "You can use it" | "You can use it — MIT only requires keeping the copyright notice on redistribution" |
| "You can't" | "Importing GPL-3.0 code and shipping it means the combined work must also follow GPL terms" |
| "You pull" | "`git fetch`, then `git merge origin/main` — resolve conflicts in the working tree" |

Answer format: **judgment + reasoning + (if any) source**. Never more than three lines.

**Question:** How do you turn "I'm not sure" into a sentence that still earns points?

---

## 17–20 min · Handoff to Lab

[Block 1 lab — Mock Exam A: Recovering a Project and Discriminating Questions](lab.md#1교시-실습--모의-실기-a-프로젝트-복구와-판별-문항)

Completion criteria:

1. `uv run python report.py` produces `outputs/report.json`.
2. `git ls-files` shows no `.env`, and `.gitignore` / `.env.example` are committed.
3. `answers_A.md` has judgment and reasoning for 3 license questions and 1 Git question.

Timer: 30 min. 30 min lab, then a 10 min break; Block 2 follows.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Diagnostic Points and the Rubric for Local-AI Hands-On Tasks

---

## 0–3 min · What Local-AI Questions Check

- Can you **read and write** the request JSON — `model`/`messages`/`stream`/`think`/`options`?
- Do you turn failures into human-readable messages — a connection failure differs from a missing model?
- Do you log response metadata so "it's slow" becomes a number?
- Do you read the model name and address from environment variables with defaults, instead of hardcoding them?

**Question:** When the server is down versus when the model is missing, what exception does the program hit in each case?

---

## 3–6 min · Diagnosis 1: Connection Failure vs. Missing Model

| Symptom | Exception / response | Check first |
|---|---|---|
| Fails immediately, no response | `httpx.ConnectError` | Is `ollama serve` running? `OLLAMA_HOST`? |
| Hangs, then fails | `httpx.TimeoutException` | Is it still loading the first time? The `timeout` value? |
| Fails immediately, "not found" in the body | HTTP 404 | `ollama list`, model name and tag |
| 200 but the answer looks off | A normal response | `think`, `temperature`, the prompt |

The same "it doesn't work" has different causes when the **exception type** differs.

---

## 6–9 min · Diagnosis 2: Parsing a Stream and What Options Do

```json
{"model": "qwen3:8b",
 "messages": [{"role": "user", "content": "..."}],
 "stream": false,
 "think": false,
 "options": {"temperature": 0.2, "num_predict": 256}}
```

- With `stream: true`, the response is **NDJSON, line by line** — `json.loads` each line.
- `think: false` splits Qwen3's thinking output out of the answer.
- `options` overrides the Modelfile defaults on a per-request basis.

---

## 9–12 min · How to Read Response Metadata

```python
eval_count = data["eval_count"]        # number of generated tokens
eval_ns = data["eval_duration"]        # nanoseconds
tokens_per_sec = eval_count / (eval_ns / 1e9)
```

- `total_duration`: loading + prompt processing + generation, all together.
- `prompt_eval_count`: number of input tokens — grows as the context gets longer.
- "Fast" or "slow" without a logged number isn't grading evidence.

**Question:** Why is `total_duration` large only on the first call for the same model?

---

## 12–15 min · How to Read the Rubric

| Area | Points |
|---|---:|
| Reproduction & execution | 15 |
| Git & collaboration | 15 |
| License & sourcing | 15 |
| Local AI API | 25 |
| HF usage | 15 |
| Verification & explanation | 15 |

Out of 100, weighted. Three levels — full, partial, not met — see [exam_rubric.md](exam_rubric.md).

---

## 15–17 min · Common Reasons for Losing Points

- No `outputs/`, or run results were never saved to a file.
- Exceptions are caught but the message doesn't say why ("an error occurred").
- Model name or address hardcoded in the code.
- `.env`, `.venv`, or `outputs/` included in a commit.
- Only the success path is demonstrated, with no evidence of the failure path.
- It runs, but you can't explain which code you changed or why.

**Key point:** rather than doing one less feature, carry **one path through to the end** with evidence.

---

## 17–20 min · Handoff to Lab

[Block 2 lab — Mock Exam B: Adding a Client Feature and Interpreting Results](lab.md#2교시-실습--모의-실기-b-클라이언트-기능-추가와-결과-해석)

Completion criteria:

1. The `--system` option works, and you wrote one sentence with evidence of how the answer changed.
2. `outputs/chat-*.json` logs `eval_count`, `eval_duration`, and `tokens_per_sec`.
3. `answers_B.md` has judgment and reasoning for 3 pipeline-interpretation questions.

Timer: 30 min. 30 min lab, then a 10 min break; Block 3 follows.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Running the Exam and Final Checks on Project 2

---

## 0–3 min · Five Environment Checks Before You Start

```powershell
uv run python check_env.py     # Ollama connection + default model present
git status                     # working tree clean
ollama list                    # pre-cached models
Get-Location                   # the designated save path
```

- Upload a test file to the submission path and re-download it to check.
- Check results are saved as `outputs/env-check.json` — evidence if something goes wrong.

---

## 3–6 min · Packet Structure and What to Submit

```text
Packet:    requirements doc + starter + fixture + the file name to submit
Submitted: the designated files + your final commit id + a short note (what and why)
```

- Turn each requirement's completion check into a checklist before you start.
- Uncommitted changes are not part of the submission — do a final `git status` check.
- **Reopen** the submitted file and confirm it matches what you intended.

**Question:** Why submit the commit id along with the files?

---

## 6–9 min · If Something Goes Wrong

| Situation | Fallback |
|---|---|
| GPU not detected | Continue with a CPU-friendly model (`qwen3:0.6b`), record the fact in your answer |
| Ollama server not running | Restart once; if it still fails, notify the proctor with the time |
| No network | `uv sync --offline`, use only pre-cached models |
| Submission system outage | Use the backup submission channel, record the outage time |

An outage is **recorded separately** from a student error. Report it, don't hide it.

---

## 9–12 min · Required Deliverables for Project 2

1. License/source analysis report: an expanded `model_cards.md` / `SOURCES.md` / `license_matrix.md`.
2. RAG mini-project: 10+ of your own documents, source display, handling of out-of-context questions.
3. Evaluation: 10 questions in `evalset.json`, hit rate, source-match rate, 2 failure analyses.
4. Reproduction steps: README, `uv.lock`, `.env.example`.
5. Evidence of individual contribution: commits, Issues, PRs, Reviews.

[assignment_brief.md](assignment_brief.md) · [assignment_rubric.md](assignment_rubric.md)

---

## 12–15 min · Final Checks Start From a Clean Folder

```powershell
git clone <repo-url> check-clean
Set-Location check-clean
uv sync --frozen
uv run python chunk.py ; uv run python embed.py   # the outputs/ index isn't in the clone
uv run python eval.py --evalset evalset.json
```

- Run the commands **exactly as written** in the README.
- If even one step needs an action not in the README, the README is incomplete.
- Use `examples/assignment_check.ps1` to scan for missing files and traces of secrets first.

**Question:** What's the most common reason something "only works on my PC"?

---

## 15–17 min · Checking for Secrets and Personal Data Right Before Submission

```powershell
git ls-files | Select-String "\.env$"
git log --all -p -S "hf_" | Select-String "hf_"
```

- If `.env` was ever committed to history, a delete commit alone isn't enough — rotate the token.
- Check that your RAG documents and eval set contain no real names or contact info.
- Check whether personal data leaked into the response JSON under `outputs/`.

---

## 17–20 min · Handoff to Lab

[Block 3 lab — Individual Hands-On Exam and Fallback Procedures](lab.md#3교시-실습--개인-실기평가와-대체-운영)

Completion criteria:

1. You started with `outputs/env-check.json` present and `git status` clean.
2. You recorded your submitted files and commit id, then reopened the submission to confirm.
3. If running a fallback session, you reproduced Project 2 from a clean folder and recorded the check results.

Exam timing follows the institution's schedule. 30 min lab, then a 10 min break.

---

## This Week's Summary

```text
Exam:    requirement -> completion check -> verification order -> evidence (files + commit id)
Project: from a clean folder, README as written -> same result -> no secrets
```

- Read errors one at a time.
- Attach one line of reasoning to every judgment.
- Next week (`week09_project_governance`) is the team project proposal.
