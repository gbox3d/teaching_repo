---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 14"
footer: "Release and Community Feedback"
---

# Week 14
## Release and Community Feedback

**3 × 60-minute blocks**<br>
Each block: 20 min explanation/demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Sessions

| Session | 20 min explanation | 30 min lab |
|---|---|---|
| Block 1 | The release document set | Fill out the release document set |
| Block 2 | Versions and releases | Create a release and cross-reproduce it |
| Block 3 | Community feedback and demo prep | Respond to feedback and rehearse the demo |

This week's question: **What makes up a release that a stranger can run in 10 minutes from the README alone, and want to leave feedback on?**

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## The Release Document Set

---

## 0–3 min · A Release Is a Promise, Not Just Code

- What carries over: Week 13's green light (pytest, ruff, CI), Week 9's LICENSE/CONTRIBUTING/CoC, `SOURCES.md`
- A release is the promise that "these files, at this point in time, are safe for others to use"
- A stranger reads **the documents first**, not the code
- This week's deliverables: document set → `v0.1.0` → cross-reproduction → responding to feedback

**Question:** What's the first thing a stranger looks for in our README?

---

## 3–6 min · The 8 Sections of a README

```text
What        one line: what tool, for whom
Why         the user and situation, and what existing solutions fall short on
Install     clone → checkout the tag → uv sync --frozen → .env
Run         2–3 commands that work by copy-paste
Example     one input → one output (with the source visible)
Limits      what doesn't work, VRAM/model/data conditions
License     the most restrictive condition across code + model + data
Provenance  SOURCES.md · CHANGELOG · CITATION
```

**Paste the install/run sections into a fresh window, run them once, and only then commit.**

---

## 6–9 min · Rechecking LICENSE — Which Way Compatibility Runs

```text
Code MIT ──┬── Dependency Apache-2.0        → compatible
           ├── Model   Apache-2.0 (Qwen)    → compatible
           ├── Data    CC-BY-NC-4.0         → the NC condition propagates to the adapter/output
           └── Dependency GPL-3.0           → the whole distribution is under GPL terms
```

- The most restrictive condition applies to the whole project
- Write the conclusion **as a sentence** in the README's "Limits" and "License" sections
- The evidence is the SPDX ID and URL in `SOURCES.md`

**Question:** If the training data is CC-BY-NC, can you release the adapter under MIT?

---

## 9–12 min · CONTRIBUTING and the Model Card

| Document | What happens without it | Minimum contents |
|---|---|---|
| CONTRIBUTING.md | no feedback comes in, or it comes in every different shape | Issue template, branch/PR rules, who responds first |
| MODEL_CARD.md | whoever gets the adapter doesn't know its use or limits | base model/revision, data/license, training setup, evaluation table, limits |
| CODE_OF_CONDUCT.md | no standard exists when a conflict arises | the adopted text and a contact channel |

- Uploading it as `README.md` on a Hub model repo turns the frontmatter (`license`, `base_model`) into metadata
- A team not releasing the adapter finalizes only `SOURCES.md` instead of a Model Card

---

## 12–15 min · CHANGELOG and CITATION.cff

```markdown
## [Unreleased]
### Added
- A document-search answer generator that shows its sources
### Fixed
- Return a clear connection message when Ollama isn't running (#12)
```

- Keep a Changelog: newest first, under Added/Changed/Fixed, **written from the user's point of view**
- Don't copy commit titles. Rewrite each one as "what changed for the user"
- CITATION.cff needs 4 required fields: `cff-version`, `message`, `title`, `authors`. `version` is optional but should match `pyproject.toml` when present

**Question:** Does "refactor config loader" belong in the CHANGELOG?

---

## 15–17 min · AI-Tool Usage Log and Automated Checks

```powershell
uv run python release_check.py --repo C:\classwork\team-a-repo --tag v0.1.0
```

- AI-tool usage log, 3 columns: file/scope, what the AI produced, what a human verified or fixed
- `release_check.py` checks README's 8 sections, LICENSE, CONTRIBUTING, CHANGELOG, CITATION, SOURCES, whether `.env` is tracked, and whether the version matches the tag → `outputs/release-check-*.json`
- Exit code 1 = there's a FAIL. It's read-only and never edits a file
- **The tool only checks "is it there." Whether it's "right" is a human's call**

---

## 17–20 min · Handing Off to the Lab

[Block 1 lab — Fill out the release document set](lab.md#1교시-실습--릴리스-문서-세트-보완)

Done when:

1. `release_check.py` reports no FAILs (any remaining WARN has a written reason)
2. Every row of `SOURCES.md` has a license, SPDX ID, and URL, and the README "Limits" section states the most restrictive condition
3. `CHANGELOG`'s `[Unreleased]` has 3+ user-facing entries, and you have one commit for these fixes

30 min lab, then a 10 min break, then Block 2.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## Versions and Releases

---

## 0–3 min · A Release Freezes a Point in Time

- What carries over: a FAIL-free, pushed repo from Block 1, a cleaned-up `[Unreleased]`
- A tag is a name attached to one commit. A release is a tag + notes + (optional attachments)
- Never change a commit you've released. If you fix it, that's a **new version**
- Today's output: `v0.1.0` → a partner team reproduces it → an Issue

**Question:** What's the difference between `main`'s latest commit and the commit the `v0.1.0` tag points to?

---

## 3–6 min · Semantic Versioning

```text
v0.1.0
 │ │ └── PATCH  docs/bug fixes, behavior-compatible
 │ └──── MINOR  new features, backward-compatible
 └────── MAJOR  breaking changes (0.x is still an unstable stage)
```

- First public release is `0.1.0`. Fix a cross-reproduction defect and it's `0.1.1`; add a feature and it's `0.2.0`
- Decide the version in exactly one place: `pyproject.toml`'s version = the tag = `CITATION.cff`'s version
- An adapter experiment name (`adapters/run-002`) is not a release version

**Question:** You only fixed a README typo. Which of the three digits goes up?

---

## 6–9 min · Tags and GitHub Releases

```powershell
uv run python tag_notes.py --repo C:\classwork\team-a-repo --version 0.1.0 --promote
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
git show v0.1.0 --stat | Select-Object -First 8
```

- Use `-a` annotated tags: they carry a tagger, date, and message. Don't use lightweight tags
- `tag_notes.py` promotes `[Unreleased]` to `[0.1.0] - date` and writes `outputs/release-notes-v0.1.0.md`
- GitHub → Releases → Draft a new release → select the tag → paste in the notes → Publish
- Release notes = changelog entries + a 3-line run command + limits + a feedback channel

---

## 9–12 min · Verifying Reproduction — Become the Stranger

```powershell
.\reproduce_by_stranger.ps1 -Source https://github.com/team-b/local-ai-helper -Tag v0.1.0
```

- Rules: a new folder, README only, don't ask a teammate, a 10-minute timer
- clone → checkout the tag → `uv sync --frozen` → `.env` → run → the example → tests
- Wherever you get stuck is a README defect. Try for only 30 seconds, record it, don't fix it yourself
- **"It works on my PC" is not evidence**

**Question:** `uv sync --frozen` failed with "no uv.lock." Whose problem is that?

---

## 12–15 min · Fixing Things After a Release

| Situation | Don't | Do |
|---|---|---|
| README typo | delete the tag and remake it | fix it, then `v0.1.1` |
| A defect that breaks the run | edit the released commit and force-push | a fix commit → CHANGELOG → `v0.1.1` |
| A new feature request | squeeze it into a patch version | pile it into `[Unreleased]` for `v0.2.0` |

- Someone has already pulled that release. **A pushed tag never moves**
- Patch releases follow the same procedure: promote CHANGELOG → tag → Release notes

---

## 15–17 min · Distributing Model/Adapter Artifacts

- Don't commit weights to the code repository (size and history bloat)
- Release asset: attach a small adapter (`adapter_model.safetensors` + `adapter_config.json`), with its SHA256 in the README
- Hugging Face Hub: a model repo + Model Card frontmatter (`license`, `base_model`), uploaded via the `huggingface_hub` Python API (an extension task)
- Check first: does the base model's and data's license **allow redistribution**?
- Large weights and GGUF conversion are out of scope this term

**Question:** If you attach only the adapter, what does the recipient still need to prepare?

---

## 17–20 min · Handing Off to the Lab

[Block 2 lab — Create a release and cross-reproduce it](lab.md#2교시-실습--릴리스-생성과-교차-재현)

Done when:

1. The annotated `v0.1.0` tag is pushed and the GitHub Release has release notes
2. `repro-log-*.md` records a partner team's release reproduced in a new folder, with per-step timing and results
3. You filed an Issue with environment, command, output, and README location for every point you got stuck (or, if you never got stuck, reported the total time)

30 min lab, then a 10 min break, then Block 3.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## Community Feedback and Demo Prep

---

## 0–3 min · Feedback Is the Release's First Result

- What carries over: Block 2's release URL, Issues our team received, Issues we filed
- The moment the first Issue arrives, a project stops being "code only I use"
- Today: triage → try to reproduce → respond → record the decision → 3-minute demo rehearsal
- What matters more than response speed is **predictability of the response** (label, decision, which version it lands in)

**Question:** What does an Issue left open with no response say to a stranger?

---

## 3–6 min · 5 Triage Labels

| Label | Meaning | Criteria |
|---|---|---|
| `bug` | followed the docs, got different behavior | has a repro command/output, and we can reproduce it too |
| `docs` | code is right, README is wrong or missing something | fixing the docs alone resolves it |
| `enhancement` | a new feature or improvement idea | current behavior is working as intended |
| `question` | a usage question | the answer might turn into a docs fix |
| `needs-repro` | not enough info to reproduce | missing environment, command, or output |

Don't label from the title alone. If there's not enough information, don't decide — just apply `needs-repro`.

---

## 6–9 min · Response Etiquette and Managing Expectations

```text
[Reproduced and accepted]  reproduced with the same command → one-line cause → which version fixes it
[Couldn't reproduce]       our environment's result → request the info needed to find the difference (needs-repro)
[Deferred / out of scope]  reason → a workaround → logged as a candidate in DECISIONS.md
```

- Talk about the behavior, not the person. Don't promise a deadline
- Don't close it out with "works on my PC"
- Three things to ask for in an unreproducible report: version output, the full command run, and the full output at the point of failure

**Question:** A reporter pasted output that includes their home path and real name. What do you do first?

---

## 9–12 min · Recording the Adoption Decision

```markdown
| Issue | Summary | Label | Decision | Reason | Landed in |
|---|---|---|---|---|---|
| #3 | uv sync --frozen fails | bug | accepted | uv.lock wasn't committed, reproduced | v0.1.1 |
| #4 | support running without a GPU | enhancement | deferred | out of scope; pointed to small-model guidance instead | TBD |
```

- Record accepted, deferred, and rejected all in `DECISIONS.md` — even a rejection needs a reason
- If accepted but not fixable this term, write "accepted · timing TBD" and why
- This table is the **evidence of feedback incorporated** for the 4th integrative assignment

---

## 12–15 min · Structuring a 3-Minute Demo

| Segment | Time | What to say | Screen |
|---|---:|---|---|
| Problem | 0:00–0:30 | who, what situation, why existing solutions fall short | README front page |
| Demo | 0:30–2:00 | run command → one input → one output → where the source is shown | terminal or UI |
| Limits | 2:00–2:30 | 2 things that don't work, conditions (VRAM/model/data license) | README "Limits" |
| Next | 2:30–3:00 | one piece of feedback received, the `v0.1.1` plan, how to contribute | Issue list |

- Start the server and load the model beforehand, and get the first response in. The first request is slow
- **One input, one output.** Cut screen switches, not explanation.

---

## 15–17 min · Anticipating Questions, Preparing for Failure

- 5 expected questions: why this model / data provenance / how long reproduction takes / what doesn't work / how to contribute
- The evidence behind your answers lives in the repo: `SOURCES.md`, `experiments/run-*.md`, `docs/repro/`, `FAILURE_ANALYSIS.md`, `CONTRIBUTING.md`
- Answering order: restate the question → facts (file/number) → reasoning → limits and next steps
- Failure fallbacks: no response from Ollama → pre-captured output JSON; the service won't start → CLI; no network → a local file
- Have a teammate time the rehearsal. Over 3:30, trim the demo segment

**Question:** Can you open the file behind your answer within 10 seconds?

---

## 17–20 min · Handing Off to the Lab

[Block 3 lab — Respond to feedback and rehearse the demo](lab.md#3교시-실습--피드백-응답과-시연-리허설)

Done when:

1. 2+ received Issues have a label, a reproduction attempt result, and a response comment
2. `DECISIONS.md` records accept/defer/reject with reasons and target versions
3. `docs/demo_outline.md` has per-segment timing for 2 demo rehearsals, and the second run is under 3:30

30 min lab, then a 10 min break. Next week is the final presentation.

---

## This Week's Wrap-Up

```text
Docs:     README's 8 sections · LICENSE compatibility · CONTRIBUTING · CHANGELOG · CITATION · SOURCES · (Model Card)
Version:  [Unreleased] → v0.1.0 annotated tag → Release notes → a fix becomes v0.1.1
Repro:    new folder · README only · 10 minutes · a blocker becomes an Issue
Feedback: label → attempt to reproduce → respond → DECISIONS.md → 3-minute demo rehearsal
```

**It only becomes a release once a stranger can run it in 10 minutes and leave an Issue.**
