---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 9"
footer: "Project Proposals and Open Source Governance"
---

# Week 9
## Project Proposals and Open Source Governance

**Three 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Session | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Open source governance — roles, rules, health metrics | Governance document analysis table |
| Block 2 | Defining the problem and justifying technical choices | Team proposal draft |
| Block 3 | Milestones, roles, and the proposal pitch | Team repository and issue breakdown |

Through Week 8 you worked alone. Starting this week, you grow **one team repository** all the way to the Week 15 release.

**Question:** In a repository with not a single line of code yet, what should be decided first?

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Open Source Governance — Roles, Rules, Health Metrics

---

## 0–3 min · What Gets Decided Before Code

```text
Governance = who (role) decides and changes what (scope of decision) and how (process)
```

- Working alone, "I decide" was enough.
- With three people, you need merge rights, a review order, and a tiebreaker for conflicts.
- If the rule isn't in a document, the rule belongs to whoever speaks loudest.

**Rules should be committed to the repository, just like code.**

**Question:** If two teammates each insist on a different model, who decides, and how?

---

## 3–6 min · Four Roles

```text
User ──▶ Contributor ──▶ Committer ──▶ Maintainer
 (runs it)   (Issues, PRs)  (merge rights)  (direction, releases, rules)
```

| Role | What they do | Authority |
|---|---|---|
| User | Runs it, reports bugs | None |
| Contributor | Issues, PRs, review comments | Only within their fork |
| Committer | Approves reviews, merges | Write access to branches |
| Maintainer | Roadmap, releases, rule changes | Repository settings |

On our team, all three of you are committers, and **the maintainer role rotates** (whoever handles the release).

---

## 6–9 min · Decision-Making Models

| Model | Who decides | Example | Strength / weakness |
|---|---|---|---|
| BDFL | One founder | Small early-stage projects | Fast · bus factor of 1 |
| Committee | Elected/appointed maintainers | Large community projects | Stable · slow |
| Foundation | A technical committee under a legal entity | Projects shared across companies | Neutral · heavy process |

- Look past the model's name to **where the decision gets recorded**: an Issue thread, an RFC doc, meeting minutes.
- For a team project, "no consensus -> post reasoning in an Issue, then majority vote; a tie is broken by whoever owns this milestone" is enough.

---

## 9–12 min · The Set of Rule Documents

| File | Question it answers |
|---|---|
| `CODE_OF_CONDUCT.md` | How do we treat each other — adopting the Contributor Covenant |
| `CONTRIBUTING.md` | How do you contribute — branches, PRs, review, response time |
| `.github/ISSUE_TEMPLATE/*.md` | What has to be written for a report to count |
| `.github/PULL_REQUEST_TEMPLATE.md` | How to describe a change |
| `LICENSE` | Under what terms can it be used and shared |

GitHub shows these files together on one screen at **Insights → Community Standards**.

**Question:** What's the difference between a CoC that's copy-pasted in full and one that just declares "we adopt X"?

---

## 12–15 min · Project Health Metrics

| Metric | Where to read it | What it tells you |
|---|---|---|
| First-response time | First comment time on the last 3 Issues | Is the maintainer active? |
| Open/closed Issue ratio | Open and Closed counts on the Issues tab | How fast issues get handled |
| Release cadence | Dates on the Releases tab | Predictable shipping |
| Bus factor | Top-contributor share on Insights → Contributors | How many people leaving would stop the project |

- A single number doesn't say "good" or "bad" by itself. **Compare two projects by the same yardstick.**
- Roughly estimate bus factor as "commit share of the top 3 contributors."

**Question:** What does it mean when first response is fast but the release cadence is long?

---

## 15–17 min · Demo — Two Repositories, the Same Table

1. `huggingface/transformers` -> Insights -> Community Standards -> check each item.
2. The `.github/` folder -> number of issue template types -> the last 5 release dates.
3. Do the same for `ollama/ollama`.
4. Fill in the numeric items with a script.

```powershell
uv run python repo_health.py --repo huggingface/transformers --repo ollama/ollama
```

The output `outputs/health-*.json` records whether community files exist, release cadence, and top-3 commit share.
**Evidence read in the browser comes first; the script only supports it.**

---

## 17–20 min · Handoff to Lab

[Block 1 lab — Governance Document Analysis Table](lab.md#1교시-실습--거버넌스-문서-분석표) · [Period files](examples/period1/README.md)

Completion criteria:

1. `governance_survey.md` lists, with source URLs, both projects' CoC, CONTRIBUTING, issue templates, release cadence, and maintainer count.
2. You recorded a first-response-time sample (3 Issues) and the top-3 commit share.
3. "Three rules our team will adopt" has a source and a plan for applying each one.

30 min lab, then a 10 min break. Block 2 follows the break.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Defining the Problem and Justifying Technical Choices

---

## 0–3 min · A Problem, Not an Idea

```text
[User] runs into [problem] in [situation].
Right now they solve it with [current solution], but it has [limitation].
```

- "We'll build a class-helper chatbot" is an idea. It isn't a problem.
- "A student who hits a uv error during lab searches the web, but the answer misses our class context (uv, Ollama, Windows)" is a problem.

**If the problem statement wobbles, your model and data choices wobble too.**

---

## 3–6 min · One User, One Situation

| Item | Example |
|---|---|
| User | A student taking this course |
| Situation | Must fix an error within a 30-minute lab |
| Current solution | Web search, asking a neighbor |
| Limitation | Answers don't match the class setup; not enough people to ask |
| Success signal | Enter the error message, get a first step back with a citation to a class document |

- "All developers" is not a user. Pick **one person whose face you can picture**.
- The success signal must be something you can actually measure in the Week 12 beta.

**Question:** How is your team's user solving this problem right now?

---

## 6–9 min · Must / Should / Could

| Grade | Meaning | Example |
|---|---|---|
| Must | No beta without it (3 items) | Error message in -> sourced answer, `/health`, a run-it README |
| Should | Clearly good to have | Chat history, auto-updating class docs |
| Could | If time allows | Web UI theme, voice input |

- Must is **exactly the 3 things that absolutely must be in the Week 12 beta (Project 3)**.
- Should-or-higher becomes an Issue, but scheduled after milestone M3.
- Over-scoping is the most common failure. 5 Musts is already too many.

---

## 9–12 min · Four Criteria for Choosing a Model

| Criterion | How to check | What to record |
|---|---|---|
| License | The model card's SPDX ID or terms name | Commercial use and redistribution conditions |
| VRAM | params × bits ÷ 8 + KV cache | Does it fit in 12 GB? |
| Reproducibility | Ollama tag, pinned HF revision | The exact ID |
| Korean quality | Compare the same 5 prompts | Reuse Week 4's `model_report.md` |

```powershell
uv run python vram_estimate.py --candidate "qwen3:8b,8.2B,4" --candidate "qwen3:0.6b,0.6B,4"
```

**Write the estimate and the measured value side by side.** An estimate alone isn't evidence.

---

## 12–15 min · Criteria for Choosing Data

| Criterion | Question |
|---|---|
| Availability | Self-written, public dataset, or user-generated — which is it? |
| License | Is redistribution allowed, like CC-BY/CC0, or is it research-only? |
| Privacy | Could emails, phone numbers, or name patterns show up? |
| Volume | LoRA can start with as few as 40–60 self-written examples |
| Eval split | Set aside 10–20 questions from the start that are never used for training |

- Week 5's `SOURCES.md` and Week 7's `evalset.json` already stand as evidence for your data candidates.
- "We'll get data later" is not a plan — it's a **risk**.

**Question:** Who writes your team's first 50 examples, and when?

---

## 15–17 min · Risks and Mitigations

| Risk | Signal | Mitigation |
|---|---|---|
| No data | Zero training examples by Week 10 | Each of 3 teammates writes 20 |
| VRAM shortage | OOM at load time | A smaller model, quantization, smaller `num_ctx` |
| Over-scoping | 5+ Musts | Cut to 3 Musts, demote the rest to Should |
| Team member drops out / goes silent | Commits landing on one person's branch only | Keep Issues small, cross-assign reviewers |

Don't write a risk as "none." **The team that writes "none" is the one most stuck by Week 12.**

---

## 17–20 min · Handoff to Lab

[Block 2 lab — Team Proposal Draft](lab.md#2교시-실습--팀-제안서-초안) · [Period files](examples/period2/README.md)

Completion criteria:

1. `proposal.md` has one problem sentence, one user (situation, current solution, limitation, success signal), and 3 Musts.
2. Two model candidates have license and VRAM estimate/measurement evidence; data candidates have how to get them, license, and a privacy check.
3. Two risks each have a signal and a mitigation.

30 min lab, then a 10 min break. Block 3 follows the break.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Milestones, Roles, and the Proposal Pitch

---

## 0–3 min · Counting Backward From Week 15

| Week | Fixed | This week's decision |
|---|---|---|
| 15 | Final release package & pitch (Project 4) | What to demo |
| 14 | `v0.1.0` tag & cross-reproduction | Who owns the release |
| 13 | Testing, CI, security review | Which modules to test |
| 12 | Service beta (Project 3) | The 3 Musts |
| 10–11 | First LoRA experiment, data, evaluation | Model and data candidates |

**A schedule is built by subtracting from the end, not adding from the start.**

**Question:** Can you name, right now, one thing that absolutely must be in the Week 12 beta?

---

## 3–6 min · Three Milestones

```text
M1 · Week 11 · First experiment log   experiments/run-001.md, DATA_CARD.md, 10-question eval set
M2 · Week 12 · Service beta           /health, /chat, one UI, a run-it README   ← Project 3
M3 · Week 15 · v0.1.0 release         green CI, tag, CHANGELOG, presentation   ← Project 4
```

- Define a milestone by "what has to exist for it to close." A milestone with only a date never closes.
- Put Should/Could items in `Backlog`, after M3.

**Question:** If M1 doesn't close by Week 11, what happens to M2?

---

## 6–9 min · Principles for Breaking Down Issues

| Principle | Weak example | Strong example |
|---|---|---|
| Small (≤ 3 days) | Implement LoRA training | Train run-001 with `train_lora.py` and log the loss |
| Verifiable | Prepare data | `data/sft.jsonl` with 50 examples, passing `pii_check.py` |
| One owner | The whole team | `student02` |
| Belongs to a milestone | None | M1 |

- Write the Issue title so it reads as a **completed state**.
- An Issue with no "completion criteria" line can't be closed.

```powershell
uv run python issue_plan_check.py --plan issue_plan.json
```

---

## 9–12 min · PR Rules and Reviewers

| Rule | Our team default |
|---|---|
| Branch name | `feat/<issue-number>-<short-description>` |
| PR size | ≤ 300 changed lines, 1 PR per Issue |
| Reviewer | Required: one teammate who isn't the author |
| Self-merge | Forbidden (merge only after review approval) |
| Expected response time | 48 hours after requesting review |

- Write these in `CONTRIBUTING.md`, reflecting the 3 rules you chose in Block 1.
- In Week 13 you'll **enforce these rules in the repository settings** via branch protection.

---

## 12–15 min · Evidence of Individual Contribution

```text
Team repo -> Insights -> Contributors: who, when, how much
Issues (assignee:@me) · Pull requests (author:@me) · Reviews (reviewed-by:@me)
```

- Even on a team project, **grading looks at each individual's commits, Issues, PRs, and Reviews**.
- If everything is pushed under one account, the rest of the team's evidence disappears.
- On shared PCs, each person logs in with their own account and logs out when done.

**Question:** Code written together in pair programming — whose contribution does it register as?

---

## 15–17 min · Structure of the 3-Minute Proposal Pitch

| Time | Content | Rubric item |
|---|---|---|
| 0:00–0:30 | User and problem, in one sentence | Clarity of problem and user |
| 0:30–1:15 | 3 Musts, model/data candidates and their licenses | Scope and technical justification, legality |
| 1:15–2:15 | Architecture diagram, 3 milestones, roles | Realism of milestones and roles |
| 2:15–3:00 | 2 risks and mitigations, Q&A | Timing and Q&A |

- Criteria: [proposal_rubric.md](proposal_rubric.md). The presentation slot follows the school schedule.
- Rehearse **with a timer running**. Record what you ran over on and what you left out.

---

## 17–20 min · Handoff to Lab

[Block 3 lab — Team Repository and Issue Breakdown](lab.md#3교시-실습--팀-저장소와-이슈-분해) · [Period files](examples/period3/README.md)

Completion criteria:

1. The team repository has LICENSE, CODE_OF_CONDUCT.md, CONTRIBUTING.md, and issue/PR templates, and `uv run team-project doctor` runs successfully.
2. 3 milestones and 8–10 Issues are registered, each with completion criteria, an owner, and a milestone.
3. `docs/rehearsal.md` has your 3-minute rehearsal record (time taken, what was missing, 2 expected questions).

30 min lab, then a 10 min break.

---

## This Week's Summary

```text
Governance: roles -> decision process -> rule documents -> health metrics
Proposal:   one problem sentence -> one user -> 3 Musts -> model/data justification -> risks
Execution:  count back from Week 15 -> 3 milestones -> 8-10 Issues -> PR rules -> individual evidence
```

Next week, `week10_peft_lora`: you actually LoRA-train one of the model candidates from your proposal.
That experiment log is **the evidence that closes M1's first Issue**.
