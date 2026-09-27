---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 2"
footer: "Git/GitHub Collaboration and Licensing"
---

# Week 2
## Git/GitHub Collaboration and Licensing

**3 × 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Block | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Branches, remotes, resolving conflicts | Connect a remote and resolve one conflict |
| Block 2 | The GitHub collaboration flow and review | Propose a change to a partner's repo and get reviewed |
| Block 3 | Reading and choosing a license | Determine a license and add a LICENSE file |

This week's question: how do you **safely propose** your changes to someone else's repository, and how do you decide **under what terms** you can use and share their code?

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Branches, Remotes, Resolving Conflicts

---

## 0–3 min · Carrying Over: History That Lives Only on Your PC

```text
Week 1: git init → "Add environment report"   (exists only on my one PC)
Week 2: push that history to GitHub, and merge diverged work
```

- Right now your repository lives only on your PC. If the disk fails, it's gone
- No one else can see it or propose changes to it
- Today a fourth place appears: **the remote**

**Question:** `git log` shows the commit, but GitHub doesn't yet. Which command is missing?

---

## 3–6 min · Reviewing the Three Areas

```text
working tree ── git add ──▶ staging area ── git commit ──▶ repository (HEAD)
   editing                    next commit candidate            confirmed history
```

- `git status`: summarizes the differences between the three areas
- `git diff`: working tree ↔ stage · `git diff --staged`: stage ↔ HEAD
- One commit = one intent. You should be able to tell what changed from the message alone

**Key point:** a commit finishes locally. Only a separate command changes the remote.

---

## 6–9 min · Remotes: clone, push, pull, fetch

```text
local main ── push ──▶ origin/main (GitHub)
local main ◀─ pull ─── origin/main      (= fetch + merge)
          ◀─ fetch ── updates only the origin/main reference; working files stay the same
```

```bash
git remote add origin (your repo's HTTPS URL)
git push -u origin main
git branch -vv
```

- `clone`: copies a whole remote to create a new local repo
- `-u`: remembers the tracking relationship, so `git push` alone sends to the same place afterward

**Question:** Nothing changed after a `fetch`. Did it fail?

---

## 9–13 min · Branch and Merge

```text
main:            A ── B ─────────── M   (merge commit, two parents)
                       \           /
feature/readme:         C ── D ───┘
```

```bash
git switch -c feature/readme   # create and switch
git switch main
git merge feature/readme
```

- A branch is a **label** pointing at a commit. It costs almost nothing to create
- Fast-forward: if `main` only fell behind, the label just moves forward
- Merge commit: if both sides moved on, a commit with two parents is created

---

## 13–16 min · A Conflict Is a Request for a Decision

```text
<<<<<<< HEAD
This repository holds lab records for the Open Source AI Applications course.
=======
This repository is the starting point for a local AI assistant project.
>>>>>>> feature/readme
```

- Condition: two branches changed **the same line of the same file** differently
- Git doesn't know which side is right. A person writes the resulting sentence
- Steps: `git status` → open the file → remove the markers, write the result → `git add` → `git commit`
- To undo: `git merge --abort`

**Key point:** a conflict isn't an error — it's **a request for a decision**.

---

## 16–18 min · Commit Message Conventions

```text
Add run instructions to README

New members could not find how to start the tool.
Related to #3
```

- Subject: start with an imperative verb, around 50 characters, no period
- One blank line between subject and body
- Body: **why**, not what. Reference the related issue number
- Bad examples: `update`, `fix`, `final2`

**Question:** Reading only `git log --oneline`, can you tell what each commit changed for the user?

---

## 18–20 min · Lab Handoff

[Block 1 Lab — Connect a Remote and Resolve One Conflict](lab.md#1교시-실습--원격-연결과-충돌-1회-해결)

Completion criteria:

1. In `git branch -vv`, `main` tracks `origin/main` and is at the same commit
2. You reproduced a same-line conflict once and created a merge commit with a marker-free result sentence
3. `git log --graph --oneline --all` shows the two branches and where they meet

30-minute lab, then a 10-minute break. Block 2 after the break.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## The GitHub Collaboration Flow and Review

---

## 0–3 min · Carrying Over: From My Repo to Someone Else's

- Block 1: merged branches inside **my own** repository
- Block 2: propose changes to someone else's repo, **where I have no write access**
- Tools: Fork, Issue, Pull Request, Review — all GitHub features, none of them part of Git itself
- Today's lab is in pairs. You each propose changes to the other's repo and review each other

**Question:** What happens if you `git push` to a repo you don't have push access to?

---

## 3–7 min · The 6-Step Collaboration Flow

```text
Fork ──▶ Issue ──▶ Branch ──▶ Pull Request ──▶ Review ──▶ Merge
my copy   propose/agree  work line   change request      review/fix    applied
```

| Step | Where | Who |
|---|---|---|
| Fork, branch, push | My account, my PC | The proposer |
| Issue, PR | The original repo | The proposer |
| Review, merge | The original repo | The maintainer (repo owner) |

**Key point:** the proposer never touches the original directly. The maintainer clicks Merge.

---

## 7–10 min · Issue: The Proposal Comes Before the Code

- An issue is where you ask "is this change okay" **before** writing code
- A good issue: current situation → proposal → expected effect → alternatives
- Once the maintainer says "sounds good," you create the branch
- Getting rejected costs you nothing, because you haven't written code yet
- `Closes #12` in a PR body automatically closes the issue on merge

**Question:** If you send a large PR with no issue and it gets rejected, what have you lost?

---

## 10–13 min · Small PRs and a PR Description Template

| Field | Content |
|---|---|
| Related issue | `Closes #12` |
| What changed | What you changed (files, behavior) |
| Why | Why it's needed |
| How to verify | Commands the reviewer can run as-is |
| Checklist | One intent, no secrets, verified it runs, sources recorded |

- One PR = one intent. Sized so a reviewer can **read it in 10 minutes**
- **Draft PR**: not yet ready to merge. Open one when you want early feedback on direction

---

## 13–16 min · Review Etiquette: About the Code, Not the Person

- Target the code and the reasoning: "This line doesn't check the current folder" (good) vs. "Why did you do it this way?" (bad)
- Be specific about the request: what to change, why, and how
- Leave it open as a question: "Does this command work the same on Windows?"
- Note something good too, in one line
- The proposer doesn't defend — they **respond with a fix commit**
- Pick one of Approve, Comment, or Request changes, with reasoning

**Key point:** review is a **conversation about fixing things together**, not a verdict.

---

## 16–18 min · What Templates Do

```text
.github/
├─ PULL_REQUEST_TEMPLATE.md     # auto-inserted into the body when a PR is opened
└─ ISSUE_TEMPLATE/
   └─ proposal.md               # shown as an option when creating an issue
CONTRIBUTING.md                  # contribution process and rules
```

- Must live on the original repo's **default branch** to take effect
- A template means fewer questions the reviewer has to ask
- Start by copying `examples/pr_template/` as-is

**Question:** If the template only exists in your fork, does it apply to the PR sent to the original repo?

---

## 18–20 min · Lab Handoff

[Block 2 Lab — Propose a Change to a Partner's Repo and Get Reviewed](lab.md#2교시-실습--짝-저장소에-제안하고-리뷰-받기)

Completion criteria:

1. You opened 1 issue and 1 PR filled from the template on your partner's repo (URL)
2. You left at least 1 line-level review comment and a change request on your partner's PR (URL)
3. A fix commit was pushed and the PR was merged

30-minute lab, then a 10-minute break. Block 3 after the break.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Reading and Choosing a License

---

## 0–3 min · Copyright Comes First, a License Is Permission

```text
Copyright exists the moment code is written (no registration needed)
        ▼
Default: all rights reserved → copying, modifying, redistributing not allowed
        ▼
LICENSE file = permission the copyright holder grants, with conditions attached
```

- Even if it's public on GitHub, **no LICENSE means no permission**
- Even the partner's code merged in Block 2 has no stated terms without a license

**Question:** A repo with 10,000 stars has no LICENSE. Can you put it in your project?

---

## 3–6 min · Permissive: MIT, Apache-2.0, BSD

| License | SPDX ID | What you must do |
|---|---|---|
| MIT | `MIT` | Keep the copyright and permission notice |
| BSD 3-Clause | `BSD-3-Clause` | Keep the notice, don't use the name for promotion |
| Apache 2.0 | `Apache-2.0` | Notice, keep NOTICE, mark changes, patent grant |

- In common: commercial use allowed, private modification allowed, redistribution only needs the notice
- "Permissive" = doesn't force a license on the result
- This course's default choice for your personal repo: **MIT or Apache-2.0**

**Question:** Can you put an MIT library into a paid app and sell it without releasing your source?

---

## 6–9 min · Copyleft: GPL, LGPL, AGPL

| License | SPDX ID | When source disclosure becomes required |
|---|---|---|
| GPL 3.0 | `GPL-3.0-only` | When you **distribute** the combined program, in full |
| LGPL 3.0 | `LGPL-3.0-only` | Only the library's modifications (dynamically linked apps stay free) |
| AGPL 3.0 | `AGPL-3.0-only` | Even offering a modified version as a **network service** without distributing it |

- "The same freedom passed on to the next person" — the result carries the same license
- No obligation if you only use it internally without distributing it (AGPL is the exception)

**Key point:** distinguish whether the triggering event is distribution or offering a service.

---

## 9–12 min · Patent Clauses and Compatibility Direction

```text
permissive ──▶ copyleft    : possible (MIT code into a GPL project)
copyleft   ──▶ permissive  : not possible (the result becomes GPL)
Apache-2.0 ──▶ GPL-3.0     : possible
Apache-2.0 ──▶ GPL-2.0     : not possible
```

- Apache-2.0: includes an explicit **patent grant** from contributors; that grant ends if you sue over patents on that software
- MIT, BSD: no mention of patents → why companies often pick Apache-2.0
- Compatibility = whether you can satisfy both sets of terms **at the same time** when combining and distributing

**Question:** Can a program combining MIT code and GPL-3.0 code be distributed under MIT?

---

## 12–15 min · Model Licenses: Open Weight ≠ Open Source

| Model family | License | Character |
|---|---|---|
| Qwen (most sizes) | Apache-2.0 | OSI-approved, few conditions |
| Llama | Llama Community License | Use policy, attribution, separate permission for large-scale users |
| Gemma | Gemma Terms of Use | Includes a prohibited-use policy |
| RAIL family (OpenRAIL-M) | Use restriction clauses | Restricted use = outside the OSI definition |

- The OSI Open Source AI Definition: use/study/modify/share without use restrictions + data info, code, weights
- "You can download the weights" and "you can do anything with them" are different statements
- Even within the same family, terms can differ by size → **check the model card every time**

---

## 15–18 min · Data Licenses and "No License"

| Label | SPDX ID | Training/redistribution terms |
|---|---|---|
| CC0 | `CC0-1.0` | No conditions (recording the source is still good practice) |
| CC BY | `CC-BY-4.0` | Attribution |
| CC BY-SA | `CC-BY-SA-4.0` | Attribution + derivatives under the same terms |
| CC BY-NC | `CC-BY-NC-4.0` | Non-commercial only |
| None · "research only" | — | Not usable, or ask the copyright holder |

- Training data's terms **carry through into the model and the service**
- List code, model, and data all in one table → `license_matrix.md`
- For licenses not in the SPDX list (Llama, Gemma terms), write `LicenseRef-name`

**Key point:** no license means no use. If you can't decide, don't use it.

---

## 18–20 min · Lab Handoff

[Block 3 Lab — Determine a License and Add a LICENSE File](lab.md#3교시-실습--라이선스-판별과-license-추가)

Completion criteria:

1. `license_cards_answers.md` has a judgment (allowed/conditional/not allowed) and reasoning for all 10 questions
2. A `LICENSE` (MIT or Apache-2.0) and one sentence explaining the choice were committed and pushed to your personal repo
3. `license_matrix.md` lists 5+ entries across code/model/data with SPDX ID and source URL

30-minute lab, then a 10-minute break. Next week is `week03_reproducible_python`.

---

## This Week's Summary

```text
Block 1: local commit → push → branch → merge → a conflict is a request for a decision
Block 2: Fork → Issue → Branch → PR → Review → Merge
Block 3: copyright → license (permission) → permissive / copyleft → into models and data too
```

One rule ties it together: **propose where you have no access, and don't use code without permission.**

Next week, `week03_reproducible_python`: turn this repository into a reproducible uv-based Python project.
