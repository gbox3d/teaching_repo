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
| Block 1 | How the hands-on exam is structured, and how to read a mock question | Mock exam A: recovering a project and uv/project concept questions |
| Block 2 | Diagnostic points and the rubric for Git and Ollama hands-on tasks | Mock exam B: Git situation judgment and Ollama tool calling |
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

## 3–6 min · Five Assessment Areas

| Area | What it checks |
|---|---|
| uv usage & reproducibility | Restoring `pyproject`, what `uv add` changes, `pyproject.toml` vs `uv.lock`, `sync --locked`, `uv run` |
| Project management | src layout, `[project.scripts]`, stdout vs stderr, `.env` / `.env.example`, config layering |
| Git concepts & usage | Four areas, reading `git status`, add/commit/push, branch/conflict/PR judgment, secret separation |
| Ollama usage & application | `list`/`show`/`run`/`ps`, message roles, `options`/`think`, telling failures apart, tool calling |
| Verification & explanation | Reproducing success/failure paths, run logs, evidence-backed reasoning |

Mock exams A and B cover weeks 1–4. Whether licenses, HF, or RAG are included is set by each term's exam notice. See [exam_structure.md](exam_structure.md) for the detailed table.

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
| "You don't need to commit the lock" | "Commit `uv.lock` too — without it the next person resolves a different today" |
| "You pull" | "`git fetch`, then `git merge origin/main` — resolve conflicts in the working tree" |
| "The model remembers" | "You pile earlier questions and answers into `messages` and send them again — the model stores nothing between requests" |

Answer format: **judgment + reasoning + (if any) source**. Never more than three lines.

**Question:** How do you turn "I'm not sure" into a sentence that still earns points?

---

## 17–20 min · Handoff to Lab

[Block 1 lab — Mock Exam A: Recovering a Project and uv/Project Concept Questions](lab.md#1교시-실습--모의-실기-a-프로젝트-복구와-uv프로젝트-개념-문항) · [Period files](examples/period1/README.md)

Completion criteria:

1. `uv run python report.py` produces `outputs/report.json`.
2. `git ls-files` shows no `.env`, and `.gitignore` / `.env.example` are committed.
3. `uv run hello` prints in `week8-hello` with a first commit, and `answers_A.md` answers A-3 and A-4.

Timer: 30 min. 30 min lab, then a 10 min break; Block 2 follows.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Diagnostic Points and the Rubric for Git and Ollama Hands-On Tasks

---

## 0–3 min · What Git and Ollama Questions Check

- Can you read the three groups in `git status` as **areas** and pick the next command?
- Can you publish to GitHub with `remote add` and `push -u`, and explain why plain `git push` works afterwards?
- Can you explain how the Ollama server, the terminal command, and the Python library relate, and the three message roles?
- In tool calling, do you know **who executes** the function?

**Question:** Which area does each of `Changes to be committed`, `Changes not staged for commit`, and `Untracked files` belong to?

---

## 3–6 min · Diagnosis 1: Read `git status` as Areas

| Output | Area | Next command |
|---|---|---|
| `Changes to be committed: modified: a.py` | staging area | `git commit` |
| `Changes not staged for commit: modified: b.md` | working tree | `git add b.md` |
| `Untracked files: c.txt` | untracked (working tree) | `git add c.txt` or `.gitignore` |
| `Your branch is ahead of 'origin/main' by 1 commit` | repository is ahead | `git push` |

`.gitignore` only blocks files that are **not yet tracked**. An `.env` that is already added comes off the stage with `git restore --staged .env`.

---

## 6–9 min · Diagnosis 2: Three "It Doesn't Work"s Have Different Causes

| Message | Cause | Check first |
|---|---|---|
| `Failed to connect to Ollama` | The server (app) is off | Does `ollama list` work? |
| `model 'qwen3.5:2b' not found` | Name/tag typo, not downloaded | NAME column of `ollama list` |
| `No module named 'ollama'` | Run outside the project environment | Did you run `uv run ex01`? `uv sync` |
| The answer looks off | A normal response | `think`, `temperature`, system |

The terminal command and the Python library are both **guests** asking the same server. If the server is off, neither works.

---

## 9–12 min · Re-reading the Five Lines of Tool Calling

```text
① my program → model     question + list of functions (get_current_time, multiply)
② model → my program     "please call multiply(a=1234, b=5678)"   ← tool_calls
③ my program             runs the function itself → 7006652
④ my program → model     passes the result with role "tool"
⑤ model → person         "1234 × 5678 = 7,006,652"
```

- The model only **asks**. The execution is always my program.
- If the function result and the `AI>` answer differ, **the function result is correct**.
- The library reads the name, types, and docstring as the manual for the model → an empty `Args:` leaves the model unable to pick arguments.

**Question:** What changes if you drop `tools=` and ask "what is 1234 times 5678?"

---

## 12–15 min · How to Read the Rubric

| Area | Points |
|---|---:|
| uv usage & reproducibility | 20 |
| Project management | 15 |
| Git concepts & usage | 20 |
| Ollama usage & application | 30 |
| Verification & explanation | 15 |

Out of 100, weighted. Three levels — full, partial, not met — see [exam_rubric.md](exam_rubric.md).

---

## 15–17 min · Common Reasons for Losing Points

- The command is right, but there is no explanation of which area it changes.
- Forgetting `git add` before committing, so the change was never recorded, yet writing "I pushed it".
- Writing only "it worked" with no `[함수 실행]` line — the run log is the evidence.
- `.env`, `.venv`, or `outputs/` included in a commit.
- Lumping connection failure, missing model, and missing module into one cause.
- It runs, but you can't explain which code you changed or why.

**Key point:** rather than doing one less feature, carry **one path through to the end** with evidence.

---

## 17–20 min · Handoff to Lab

[Block 2 lab — Mock Exam B: Git Situation Judgment and Ollama Tool Calling](lab.md#2교시-실습--모의-실기-b-git-상황-판단과-ollama-툴-콜링) · [Period files](examples/period2/README.md)

Completion criteria:

1. B-1 gives the area of each of the three files and labels the area each command changes, and the B-2 GitHub repository shows 2 commits.
2. The B-3 table gives different causes and checks for the three "it doesn't work" messages.
3. `answers_B.md` has the `[함수 실행]` line where the new function was called, plus the three-step explanation.

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

[Block 3 lab — Individual Hands-On Exam and Fallback Procedures](lab.md#3교시-실습--개인-실기평가와-대체-운영) · [Period files](examples/period3/README.md)

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
