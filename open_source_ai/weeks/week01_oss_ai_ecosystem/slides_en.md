---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 1"
footer: "Orientation and the Open Source AI Ecosystem"
---

# Week 1
## Orientation and the Open Source AI Ecosystem

**3 × 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Block | 20 min explanation | 30 min lab |
|---|---|---|
| Block 1 | Running the course and reproducible evidence | Build a lab-environment checklist |
| Block 2 | Open source and open weights are not the same | Explore public AI projects |
| Block 3 | What it means to run a model on my PC | First uv run, first commit |

**Question:** Who publishes open source AI projects, why, under what rules — and is my PC ready to run them?

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Running the Course and Reproducible Evidence

---

## 0–3 min · What's Left at the End of a Semester

- One AI application repository that someone else can clone and **run with the same result**
- Its license, source list, experiment log, tests, and release tags
- What we build today: 1 checklist, 1 exploration table, 1 first commit

**Question:** Can "it worked on my PC" count as evidence?

---

## 3–5 min · A Course That Runs in Three 60-Minute Blocks

```text
[Block 1] 20 min explanation & demo → 30 min hands-on lab → 10 min break
[Block 2] 20 min explanation & demo → 30 min hands-on lab → 10 min break
[Block 3] 20 min explanation & demo → 30 min hands-on lab → 10 min break
```

- Depending on your section, two blocks and one block may fall on different days
- The block order never changes. Each block builds on the result of the one before it
- The 30-minute lab schedule lives only in `lab.md`. The 20-minute explanation sets up what to expect

---

## 5–8 min · 4 Chapters, 4 Capstone Checks

| Chapter | Weeks | Capstone check |
|---|---|---|
| Ch.1 Open source collaboration and local AI basics | 1–4 | Project 1: collaborative repo + Ollama client |
| Ch.2 Using and analyzing public AI models | 5–8 | Project 2: license analysis + RAG, occasional hands-on checks |
| Ch.3 Model adaptation and service implementation | 9–12 | Project 3: LoRA experiment log + service beta |
| Ch.4 Open source quality and release | 13–15 | Project 4: release package, final exam, final presentation |

Weeks without a project have no submission. Instead, **each week's lab results accumulate in your personal repository.** The exact weights and deadlines follow the school's course documents.

---

## 8–10 min · The Repository You Grow All Semester

```text
Weeks 1–3    Personal repo + uv project skeleton + LICENSE
Week 4       Ollama API client CLI                              ← Project 1
Weeks 5–7    HF model/data analysis, embeddings, sourced RAG     ← Project 2
Week 9       Team project proposal
Weeks 10–12  LoRA experiments, data & evaluation, service beta   ← Project 3
Weeks 13–15  Testing/CI/security, release v0.1.0, presentation   ← Project 4
```

The topic is up to you. The textbook examples are **minimal code that shows the structure.**

**Question:** What problem will your repository start out solving?

---

## 10–12 min · Why Reproducible Evidence Is the Grading Standard

| Evidence | Can someone else verify it? |
|---|---|
| A screenshot | You can't tell when or with what command it was produced |
| A sentence with the command and output | Can be checked again with the same command |
| A repo commit id + the steps to run it | Can be re-run on a different PC |

**A short sentence explaining the cause and the evidence is worth more than a screenshot.**<br>
Start holding yourself to this standard from your very first commit today.

---

## 12–14 min · Safety Rules

- Don't put your real name, student ID, phone number, passwords, or tokens in lab files or your repository
- Use course values for display names: `student01`, team names like `team-a`
- Don't change `git config --global` on a shared PC
- Don't download models during lab time. Models are cached before class
- Don't edit the original course materials. Copy them into your own folder first

**Question:** If your terminal output shows your home folder path, is it okay to submit as-is?

---

## 14–16 min · No uv? Install It Yourself

Install on your personal laptop **without admin rights**. uv only writes files inside your user folder.

```powershell
# Method 1 · Official install script (default)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Method 2 · winget (if script execution is blocked)
winget install --id=astral-sh.uv -e
```

- Install location: `%USERPROFILE%\.local\bin\uv.exe`. It never touches system folders
- **Don't install Python first.** uv fetches whatever Python it needs on its own
- macOS/Linux laptop: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Question:** Can you just type `uv --version` in the same window right after installing?

---

## 16–18 min · Installed, But the Command Isn't Found

```text
What the install script did: put uv.exe in %USERPROFILE%\.local\bin
                              and added that folder to the user PATH
What an already-open window knows: the PATH from the moment it opened — the old value
```

1. **Close the PowerShell window and open a new one.** Always try this first
2. Still failing in a new window? Check whether the file actually exists

```powershell
Test-Path "$env:USERPROFILE\.local\bin\uv.exe"    # True means the install itself succeeded
$env:Path -split ';' | Select-String '\.local'    # Nothing shown means PATH wasn't registered
& "$env:USERPROFILE\.local\bin\uv.exe" --version  # The full path always works
```

**Question:** Why doesn't "the installer said it succeeded" count as evidence?

---

## 18–20 min · Lab Handoff

[Block 1 Lab — Build a Lab-Environment Checklist](lab.md#1교시-실습--실습환경-점검표-만들기)

Completion criteria:

1. The checklist records the status of all five: `git`, `code`, `uv`, `ollama`, `nvidia-smi`
2. If **uv** was missing, you installed it yourself and confirmed the version string in a new window
3. The GPU name and VRAM (or "no GPU" and a fallback path) are recorded
4. Every failed item has one sentence describing the fix, and no passwords or tokens appear anywhere

The only thing you install today is **uv**. For Ollama, just note "not installed → install before Week 4."

30-minute lab, then a 10-minute break. Block 2 after the break.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Open Source and Open Weights Are Not the Same

---

## 0–3 min · Is Everything on GitHub Open Source?

- Copyright exists the moment a work is created. Being visible doesn't mean you can use it
- A license is **written permission** to use, modify, and share
- A repository with no license file should be treated as "read-only"

**Question:** If a repo with 50,000 stars has no `LICENSE`, can you use it in your project?

---

## 3–7 min · The OSI Open Source Definition — 10 Criteria, Grouped

| Group | Criteria |
|---|---|
| Redistribution | Doesn't block free or paid distribution (no royalties) (1) |
| Source code | Source must be available; derived works can be made and distributed under the same terms (2·3·4) |
| No discrimination | No discrimination against people, groups, or fields of endeavor (5·6) |
| License nature | Applies automatically on distribution, and isn't tied to a specific product, other software, or technology (7·8·9·10) |

"No commercial use", "research only" — either one means **it's not open source**.

---

## 7–10 min · Free, Open Source, Source-Available, Open Weight

| Term | Meaning | Example |
|---|---|---|
| Free software | The four freedoms: run, study, redistribute, modify (FSF) | GPL family |
| Open source | A license that meets the OSI's 10 criteria | MIT, Apache-2.0 |
| Source-available | Code is visible but use/commercial use is restricted | Some commercial products' core |
| Open weight | Weights are released; data, training code, and terms of use vary | Many public LLMs |

**Open weight ≠ open source.** The fact that you can download a weights file tells you nothing about the terms.

---

## 10–13 min · The OSI Open Source AI Definition (OSAID)

To guarantee an AI system the four freedoms (use, study, modify, share), you must also release it in **a form that allows modification**.

| What must be released | Content |
|---|---|
| Data information | Training data information detailed enough for a skilled person to build an equivalent system |
| Code | The complete source code used for data processing, training, and inference (OSI-approved license) |
| Parameters | Weights and settings (under OSI-approved terms) |

**Question:** A model that releases only its weights under Apache-2.0 — which of these three does it satisfy?

---

## 13–15 min · Who's in the Ecosystem

```text
Foundations (Linux Foundation, PyTorch Foundation, Apache SF) ── neutral ownership and governance
Companies (release models/frameworks)                          ── resources, platforms, people
Maintainers ── set direction, merge PRs, cut releases
Contributors ── issues, PRs, docs, translation, testing
Users        ── bug reports, use cases, feedback
```

One person can hold several roles. In this course, you move **from user to contributor**.

---

## 15–17 min · Why Companies Release Models

- Claim the ecosystem standard: get tools built on top of your model or framework
- External review and contributions: let the community find bugs, vulnerabilities, and improvements
- Hiring and reputation: earn trust from researchers and developers
- Sell the platform: release the model, sell hardware, cloud, and support
- Respond to regulation: answer demands for transparency

Also notice **what isn't released** (training data, training code, the largest models).

**Question:** Why release the weights but not the training data?

---

## 17–20 min · Lab Handoff

[Block 2 Lab — Explore Public AI Projects](lab.md#2교시-실습--공개-ai-프로젝트-탐색표)

Completion criteria:

1. The table lists 3 repos' license (SPDX ID), latest commit, open issue count, contributing guide, and release cadence
2. Each repo has one sentence on "which part of OSAID does this satisfy"
3. Every value is next to the URL of the screen you checked it on

30-minute lab, then a 10-minute break. Block 3 after the break.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## What It Means to Run a Model on My PC

---

## 0–2 min · Why Local AI Matters

- **Cost**: you spend electricity and time, not per-call fees. Run experiments as many times as you want
- **Privacy**: data never leaves the PC
- **Offline**: unaffected by network issues, API outages, or pricing changes
- **Reproducibility**: fix the same weights and settings, and the experiment repeats identically on a different PC

**Question:** If a cloud API's model quietly gets updated, what happens to last week's experiment results?

---

## 2–4 min · Cloud API vs. Local Execution

| Item | Cloud API | Local execution |
|---|---|---|
| Cost | Charged per token | GPU, electricity, time |
| Data location | Provider's servers | My PC |
| Model choice/pinning | The provider decides | I pin the ID, quantization, revision |
| Performance ceiling | Latest large models | Whatever VRAM allows |
| Reproducibility | Low | High (if you record it) |

Neither one is always the right answer. **This course defaults to local and compares from there.**

---

## 4–7 min · Parameter Count × Bytes = Memory

```text
7B model × 2 bytes (FP16)    ≈ 14 GB  → doesn't fit a 12 GB GPU
7B model × 0.5 bytes (4-bit) ≈ 3.5 GB → fits (+ headroom for context)
```

- B = 1 billion parameters. How many bytes you store per parameter determines the size
- While running, you also need **context (KV cache) and working memory**, beyond the weights
- Weight file size ≈ minimum VRAM; add 20–30% headroom on top

**Question:** How many GB is a 4B model at FP16?

---

## 7–9 min · Quantization — Trim Precision to Cut Size

| Format | Bytes per parameter | 7B baseline |
|---|---:|---:|
| FP32 | 4 | 28 GB |
| FP16 · BF16 | 2 | 14 GB |
| INT8 · Q8 | 1 | 7 GB |
| Q4 family | about 0.5–0.6 | 3.5–4.2 GB |

Lower precision means smaller and faster, but quality drops a bit. Where "good enough" ends is something you'll **measure yourself in Week 4**.

---

## 9–11 min · What Fits in 12 GB (Rough Numbers)

| Model size | Format | Weights | 12 GB GPU |
|---|---|---:|---|
| 0.5B–0.6B | FP16 | 1–1.2 GB | Plenty of room. Runs on CPU too |
| 4B | Q4 | about 2.5 GB | Fits, but not our default |
| 8B | Q4 | 5.2 GB | Our default lab size |
| 14B | Q4 | about 9 GB | Tight. Need to reduce context |
| 32B | Q4 | about 20 GB | Doesn't fit |

The `qwen3:4b` tag is a reasoning-only build that can't turn off its thinking process, so our default is `qwen3:8b`.

**Question:** With a 14B Q4 model, if you feed in a whole long document, what runs out first?

---

## 11–13 min · This Course's Default Model and Environment Variables

| Env var | Default | Purpose |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server |
| `OLLAMA_MODEL` | `qwen3:8b` | Default generation model (CPU fallback `qwen3:0.6b`) |
| `HF_TEXT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | Small Transformers generation model |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` | Sentence embeddings |

- Model names aren't hardcoded. Read them from **an environment variable + a default**
- The exact ID, quantization, and size are fixed in the per-semester environment reference table
- Today's `sysinfo.py` only reads these values into the report. Calling them starts in Week 4

---

## 13–15 min · What uv Replaces

| Used to be its own step | Old tool | uv |
|---|---|---|
| Install a Python version | python.org installer | `uv python install` |
| Isolate the project | `python -m venv .venv` | Created automatically |
| Install packages | `pip install` | `uv add` |
| Pin exact versions | `pip freeze > requirements.txt` | `uv.lock` (automatic) |

- **One executable** handles the Python version, virtual environment, packages, and lock file together
- No global `pip install`. Your laptop's Python stays clean

**Question:** What happens if two courses on the same laptop need Python 3.11 and 3.12 at the same time?

---

## 15–18 min · What One `uv run` Line Does

```text
uv run python sysinfo.py
  ① Walk up from the current folder looking for pyproject.toml
  ② If no Python satisfies requires-python = ">=3.12", download one
  ③ Create .venv if it doesn't exist
  ④ Sync dependencies (python-dotenv) into .venv → generates uv.lock
  ⑤ Run sysinfo.py with that .venv's python
```

- No `activate` to type. The right project environment is picked automatically, every time
- That's why **the same one line builds the same environment on a different PC.** This is reproducibility
- Today's evidence to check: `python.in_project_venv` in `sysinfo.json`

**Question:** If you run `python sysinfo.py` without uv, which Python gets used?

---

## 18–20 min · Lab Handoff

[Block 3 Lab — First uv Run, First Commit](lab.md#3교시-실습--첫-uv-실행과-첫-commit)

Completion criteria:

1. `uv run python sysinfo.py` created `outputs/sysinfo.json` with a GPU entry (or a reason for "no GPU")
2. Changing `OLLAMA_MODEL` in `.env` changes the report's value with no code edits
3. Your personal repo has an `Add environment report` commit, and `.venv`, `outputs/`, `.env` are untracked

30-minute lab, then a 10-minute break.

---

## This Week's Summary

```text
Course:     3 × 60-minute blocks × 15 weeks → build reproducible evidence in your own repo
Terms:      open source (OSI 10 criteria) ≠ source-available ≠ open weight
            OSAID = data information + code + parameters
Local:      parameter count × bytes = memory; 8B Q4 is the default for 12 GB
            manage model names/addresses with environment variables
Tooling:    one uv handles the Python version + venv + packages + lock file
            install into the user folder; always verify in a new window
```

Next week: connect this personal repo to a GitHub remote and exchange PRs with a partner.
