---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 15"
footer: "Final Assessment and Project Presentation"
---

# Week 15
## Final Assessment and Project Presentation

**3 × 60-minute blocks**<br>
Each block: 20 min explanation/demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Sessions

| Session | 20 min explanation | 30 min lab |
|---|---|---|
| Block 1 | Presentation rules and what a grader looks for | Final presentation round |
| Block 2 | Reproducibility verification steps and final assessment items | Cross-reproduction verification |
| Block 3 | Retrospective and life after open source | Retrospective and final submission check |

This week's question: **Is our project an open-source release that someone else can reproduce, verify, and contribute to?**

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## Presentation Rules and What a Grader Looks For

---

## 0–3 min · A Presentation Is Evidence, Not a Claim

- What carries over: Week 14's `v0.1.0` release, cross-reproduction Issues, the demo rehearsal
- This week's three pieces of evidence: presentation record → verification record → retrospective/submission check
- A presentation isn't a place to show off polish
- **It's a place to actually run a reproducible claim, live, in 3 minutes**

**Question:** Instead of saying "it works," what can you show that makes a grader believe you?

---

## 3–6 min · Presentation Rules

| Item | Rule |
|---|---|
| Time | 3-minute demo + 2-minute Q&A per team, keep to the timer |
| Reference build | the commit the release tag points to, start with `git describe --tags` |
| Code | no edits during your presentation or another team's |
| Failure | fall back to a plan B (pre-captured `outputs/` or a recording), and record the cause |
| Screen | no tokens, `.env`, personal paths, or real names visible |

**A demo run outside the tag isn't evidence for the release.**

---

## 6–10 min · Four Things a Grader Looks For

| What's checked | Pass signal | Fail signal |
|---|---|---|
| Problem | who and what situation, in one sentence, within 30 seconds | opens with a list of technology names |
| Demo | one feature actually runs, with source and model visible | just flipping through screenshots |
| Limits | one number and one failure case, given equal weight | "everything works" |
| Reproduction | 3 lines of README steps, an open Issue | no mention of reproduction |

**Question:** Of these four, which is weakest for our team right now?

---

## 10–13 min · Structuring a 3-Minute Demo

| Time | Screen | Evidence |
|---:|---|---|
| 0:00–0:30 | README front page, `git describe --tags` | repo URL, tag |
| 0:30–1:45 | one core feature run live + one error handled | run output, `outputs/` |
| 1:45–2:20 | one evaluation number, one failure case | `eval-*.json`, `FAILURE_ANALYSIS.md` |
| 2:20–3:00 | 3 lines of reproduction steps, open Issues | README, Issues |

Start the server, load the model, and open the repo **before** presenting. The live-run segment should be the longest.

---

## 13–16 min · Question Cards and How to Answer

Sample cards (`examples/question_cards.md`):

- On a brand-new PC, reading only the README, where does it first get stuck?
- The model is open-weight — can we still call this "open source AI"?
- If Ollama is off, what does `/chat` return? Show us right now.

Answering order: **restate the question → current facts (file/number) → why we chose it → limits and next steps**

**Question:** For a question you don't know the answer to, what's the worst possible answer, and what's the best?

---

## 16–18 min · Order, Equipment, and Failure

- Decide presentation order and who's recording notes first
- On the presenting PC: `git status` clean, `git describe --tags`, `ollama list`
- Enlarge the terminal font; keep demo commands in one file, in order
- Failure fallback: restart Ollama once → then pre-captured `outputs/` → then play a recording
- The audience logs one row per team in `presentation_log.md`, **no scores recorded there**

---

## 18–20 min · Handing Off to the Lab

[Block 1 lab — Final presentation round](lab.md#1교시-실습--최종-발표-라운드)

Done when:

1. The reference-build (tag) check output appeared on screen
2. The demo included both a live run and a statement of limits
3. `presentation_log.md` records questions received and any you couldn't answer

If there are more than 4 teams, extend the schedule per the university timetable. 30 min lab, then a 10 min break, then Block 2.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## Reproducibility Verification Steps and Final Assessment Items

---

## 0–3 min · Why Someone Else Must Reproduce It

- What carries over: the URLs and tags of the teams to verify, from Block 1's log
- "Works on my PC" is not evidence. **A stranger succeeding with the README alone is evidence**
- The final assessment isn't a written exam — it's a grader verifying the release against a checklist
- Today we apply that same procedure to another team's repository first

**Question:** Is the Issue our team received in Week 14's cross-reproduction closed yet?

---

## 3–7 min · The Grader's 6-Step Checklist

```powershell
git clone <URL> .\review\team-b
git -C .\review\team-b checkout v0.1.0
Set-Location .\review\team-b
uv sync --frozen
uv run python -m app ...      # one feature, per the README's steps
uv run pytest -q
```

Followed by: docs (README, LICENSE, CONTRIBUTING, CHANGELOG, SOURCES) → cross-checking license and provenance → checking for secrets and PII. `reviewer_checklist.md` expands these six steps into rows 0–9.

**Don't change the step order. For any skipped step, write "not applicable" and why.**

---

## 7–10 min · Classifying Failures

| Type | Example | Handling |
|---|---|---|
| Environment issue | model not cached, port conflict, network | retry once, log it as "environment" |
| Release defect | `uv.lock` mismatch, missing README step, failing test, no tag | file it as an Issue |
| Design limitation | model quality/speed | just check that the limit is disclosed |

The first line of the `uv sync --frozen` failure message is your basis for classification.

**Question:** The target team's model isn't on our PC. Which type is that? What would the README need to say for this to pass?

---

## 10–13 min · Demo of the Verification Tools

```powershell
.\cross_review.ps1 -RepoUrl <URL> -Team team-b -Tag v0.1.0
uv run python verify_release.py --repo .\review\team-b --team team-b
```

- `verify_release.py`: required files, `.gitignore`, tag, README sections, secret patterns → `outputs/verify-*.md`
- `cross_review.ps1`: clone → checkout → sync → pytest → verify, all in one log
- Results are PASS / WARN / FAIL. **WARN means the tool deferred the judgment — a human reads it**
- Running the feature per the README steps is not automated

---

## 13–16 min · Final Assessment Items

| Item | Points | What the grader checks |
|---|---:|---|
| Functionality | 30 | the Must-have feature runs via the README steps, both normal and error paths |
| Code quality | 25 | structure, pytest, ruff, CI, review incorporated |
| Reproducibility | 25 | clone → sync → run → test passes with no intervention |
| Completeness | 20 | docs/numbers/limits match reality, tag and CHANGELOG present |

100 points, relative weighting. The actual percentage follows the university's official syllabus. Full criteria: `final_review_rubric.md`.

**Question:** In today's verification, where is the target team most likely to lose points?

---

## 16–18 min · Rules for Writing Up a Review

- Facts only: commands, the first line of output, file names, commit ids
- Write about the repository, not the people
- Don't push to the target repo. Only leave an Issue
- Issue template: title `[Repro] <step> <symptom>`, environment, steps, expected, actual, classification
- **A good repro report is one the target team can follow exactly as written**

---

## 18–20 min · Handing Off to the Lab

[Block 2 lab — Cross-reproduction verification](lab.md#2교시-실습--교차-재현-검증)

Done when:

1. All 10 steps (0–9) have a pass/fail/not-applicable and supporting evidence
2. Every failure is classified as an environment issue, a release defect, or a design limitation
3. You filed one release-defect Issue (or, if none, recorded why)

30 min lab, then a 10 min break, then Block 3.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## Retrospective and Life After Open Source

---

## 0–3 min · A Retrospective Isn't a Grade

- What carries over: Block 2's verification records, Issues our team received
- The point of a retrospective isn't a score — it's **one behavior that changes next project**
- A sentence with no evidence ("we worked hard") isn't a retrospective
- Today's deliverables: one piece of peer feedback, an individual retrospective, finalized submission info

---

## 3–7 min · Three-Column Retrospective Method

| Column | Weak example | Strong example |
|---|---|---|
| What went well | collaboration went well | 11 of 12 PRs merged after at least 1 review (Issues #8–#20) |
| What was hard | we didn't have enough time | LoRA run-002 failed 3 times from a VRAM overflow, caused by batch size 8 |
| What to do differently | start earlier | commit the experiment-log template before the first training run |

**Attach a commit, Issue, or number to every entry.** If you can't, drop it.

**Question:** Which file in our repo can back up a claim in "what went well"?

---

## 7–10 min · Peer Feedback Principles

- No scoring. Separate facts from suggestions
- Be specific: only sentences with a file, command, or number in them
- Be actionable: one suggestion doable within this week
- Write about the repo and the presentation, not about people
- Format: 1 thing that went well, 1 reproduction failure, 1 suggestion, 1 question
- Delivery: post to the target team's Issue or Discussion, and record the URL

---

## 10–13 min · Life After Open Source

| Responsibility | What | When |
|---|---|---|
| Continued contribution | respond to received Issues, patch release (`v0.1.1`) | within the first month after the term |
| Portfolio | README front page, release page, contribution graph | before applying anywhere |
| License maintenance | recheck dependency/model licenses, update `SOURCES.md` | every six months |

**A license is a responsibility you maintain, not a one-time act at release.** Rights already granted to users under a published license can't be taken back.

**Question:** If the license of a model we used changes in a later version, what should our repo do?

---

## 13–16 min · 4th Assignment Submission Check

The eight groups in `examples/submission_checklist.md`:

- Reference build: tag → commit id, the URL opens while logged out
- Run/reproduction: clean-folder clone → `uv sync --frozen` → steps → pytest
- Document set · provenance/licensing (`SOURCES.md`, SPDX)
- Evidence of collaboration: per-member commit/Issue/PR/Review URLs
- Evaluation/limits · AI-tool usage log (adopted, rejected, verified)
- Security: `.env` untracked, no secrets in history, `pip-audit`

Run `verify_release.py --check-ollama` on your own repo and clear FAILs first.

---

## 16–18 min · Three Things to Do After the Term

1. Close one cross-reproduction Issue and ship a **patch release**, `v0.1.1`.
2. Send a **small Issue or PR** to an open-source project outside this course. A docs typo report or a repro-failure report counts as a contribution too.
3. **Recheck the model/data/dependency licenses** six months from now and update `SOURCES.md`.

There's no folder for next week. The repository doesn't close.

**Question:** Which of these three can you actually do this month? Who owns it?

---

## 18–20 min · Handing Off to the Lab

[Block 3 lab — Retrospective and final submission check](lab.md#3교시-실습--회고와-최종-제출-점검)

Done when:

1. All four feedback columns have concrete evidence, and you've sent the URL to the target team
2. Every item in retrospective sections 1–3 has evidence attached
3. `submission.md`'s commit id matches the commit the tag points to

30 min lab, then a 10 min break. This is the term's last block.

---

## This Week's Wrap-Up

```text
Presentation: reference build (tag) → live run → limits → reproduction steps      (3 min + 2 min)
Verification: clone → sync --frozen → run → test → docs/license → secrets
Retrospective: what went well · what was hard · what to do differently  + evidence for each
After:        patch release · outside contribution · license recheck
```

**It only becomes an open-source release once someone else can reproduce, verify, and contribute to it.**
