---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 3"
footer: "Reproducible Python Open Source Projects"
---

# Week 3
## Reproducible Python Open Source Projects

**3 × 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Block | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Reproducibility failures, virtual environments, the uv command flow, `pyproject.toml`/`uv.lock` | Create a uv project and reproduce it in a clean folder |
| Block 2 | src layout, entry points, argparse/logging, README run steps | Finish the oss-tool CLI |
| Block 3 | Separating config from code, `.env`, config layers, secrets already committed | A config loader and separating secrets |

This week's question: **what do you include and what do you leave out, so the same result shows up on a different PC?**

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Code That Only Works on My PC Isn't Open Source

---

## 0–3 min · What "It Works on My PC" Really Means

```text
A: last year's Python and packages, versions not recorded
B: Python and packages prepared today, no shared lock
Same code → A works, B gets ImportError or a different result
```

- No one knows which packages, which versions, or where they were installed
- If two projects share one Python, fixing one can break the other
- The repo only has the code — the environment lives **only in my head**

**Question:** In Week 2, when you cloned your partner's repo, did it actually run? What was missing?

---

## 3–6 min · Virtual Environments: A Separate Room per Project

```text
C:\classwork\
 ├─ osa-practice\.venv\    ← this project's own Python + packages
 └─ other-proj\.venv\      ← a different version, no interference either way
```

- A virtual environment is a project's own **isolated package folder**
- It must be safe to delete and recreate → so it's never committed
- Isolation alone isn't enough: you also need **a record of what was installed** for it to be reproducible

---

## 6–9 min · Four Jobs uv Handles at Once

| Task | uv commands and files |
|---|---|
| Prepare Python | `uv python install`, `uv python pin` → `.python-version` |
| Prepare environment and run | `uv run` → creates and uses `.venv` |
| Declare dependencies | `uv add` → updates `pyproject.toml` |
| Lock and install | `uv lock` → `uv.lock`; `uv sync` → environment |

Run from the folder containing `pyproject.toml`: **`uv run` prepares the environment, then runs.**
No activation needed. Check: `uv run python -c "import sys; print(sys.executable)"`

---

## 9–12 min · The Flow of Five Commands

```powershell
uv init --no-package     # build the package layout ourselves in Block 2
uv add httpx             # update declaration + lock + environment
uv lock                  # update lock only (add may have already done it)
uv sync --locked         # verify the shared lock, install its packages
uv run --locked python -c "import httpx; print(httpx.__version__)"
```

- Plain `uv run`: automatically updates the lock and environment when needed
- `--locked`: fails if the lock is missing or needs an update → clone/CI checks
- `--frozen`: uses the existing lock without checking project consistency

---

## 12–15 min · How pyproject.toml and uv.lock Relate

```toml
# pyproject.toml — the human-written "intent"
dependencies = ["httpx"]
```

```text
# uv.lock — the tool-generated "result". Never edit by hand
httpx <exact version> ← anyio, certifi, h11, httpcore, idna, ...
each package's exact version + file hash (the count varies by resolution)
```

- `pyproject.toml`: just the name is enough ("we need httpx")
- `uv.lock`: pins the **exact versions of the whole tree**, resolved today
- Commit both. Without the lock, the next person resolves **a different today**

---

## 15–17 min · What to Commit and What to Leave Out

| Commit it | Don't commit it |
|---|---|
| `pyproject.toml` | `.venv/` (a few MB to a few GB per project) |
| `uv.lock` | `__pycache__/`, `*.pyc` |
| `.python-version`, `.env.example` | `.env`, `.env.local` (private settings) |
| `src/`, `README.md`, `.gitignore` | `outputs/`, caches, model weights |

**Keep `uv.lock` tracked.** Read `git diff --cached` before publishing.
See the [uv guide](../../uv_guide.md) for ignore rules and a clean-clone check.

---

## 17–20 min · Lab Handoff

[Block 1 Lab — Create a uv Project and Reproduce It in a Clean Folder](lab.md#1교시-실습--uv-프로젝트를-만들고-깨끗한-폴더에서-재현하기)

[period1: examples for this lab](examples/period1/README.md)

Completion criteria:

1. `pyproject.toml` and `uv.lock` are committed, and `.venv/` doesn't show up in `git status`
2. There's a log showing: clone into a clean folder → `uv sync --locked` → `import httpx` succeeded
3. You wrote one sentence explaining why `--locked` fails when `uv.lock` is deleted

30-minute lab, then a 10-minute break. Block 2 after the break.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Turning One Script into an Installable Tool

---

## 0–3 min · Why We Need Structure

```text
Now:   uv run python sysinfo.py           # only runs if you know where the file is
Goal:  uv run oss-tool sysinfo --json     # runs by name in the project environment
```

- Once you're past three files, `from sysinfo import ...` breaks depending on the current folder
- Other people start by asking "which file am I supposed to run?"
- One named command shrinks the README's run steps to **three lines**

**Question:** What breaks if you run `python sysinfo.py` from a folder outside the repo?

---

## 3–6 min · src Layout, Packages, and Modules

```text
osa-practice/
 ├─ pyproject.toml
 ├─ src/
 │   └─ oss_tool/          ← package (folder + __init__.py)
 │       ├─ __init__.py
 │       ├─ cli.py          ← module
 │       ├─ sysinfo.py
 │       └─ config.py
 └─ outputs/               ← run results, not committed
```

- Putting it under `src/` means only the **installed package** is importable → bugs from depending on the current folder disappear
- Package name is `oss_tool` (underscore), command name is `oss-tool` (hyphen)

---

## 6–9 min · Entry Point: One Line Connecting Name and Function

```toml
[project.scripts]
oss-tool = "oss_tool.cli:main"      # command name = "package.module:function"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oss_tool"]
```

- `uv sync` installs the project into `.venv` in **editable mode** → creates `.venv\Scripts\oss-tool.exe`
- `main()`'s return value becomes the exit code (0 = success)

---

## 9–12 min · Designing argparse Subcommands

```python
parser = argparse.ArgumentParser(prog="oss-tool")
sub = parser.add_subparsers(dest="command", required=True)

greet = sub.add_parser("greet", help="print a greeting")
greet.add_argument("--name", default="student01")
greet.set_defaults(func=cmd_greet)

args = parser.parse_args()
return args.func(args)            # dispatch to a function per subcommand
```

- Like `git commit` or `uv add`: **one verb = one subcommand**
- `--help` is free. One `help=` line is the documentation

**Question:** What's the difference between putting `--name`'s default in code versus in a config file?

---

## 12–15 min · logging, Not print

```python
import logging, sys
log = logging.getLogger("oss_tool")
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="%(levelname)s %(name)s: %(message)s")

log.info("saved: %s", path)      # progress → stderr
print(json.dumps(result))        # result → stdout
```

- Results go to **stdout**, progress/warnings go to **stderr** → `| ConvertFrom-Json` doesn't break
- `--verbose` turns on `DEBUG`: change how much information appears without touching the code

---

## 15–17 min · Three Lines of README Run Steps

```markdown
## Run
From the project root (containing pyproject.toml):
1. `uv sync --locked`
2. `uv run --locked oss-tool greet --name student01`
3. `uv run --locked oss-tool sysinfo --json`
```

- Reproduction steps for a project shared with its lock (results in `outputs/`)
- Leave the option list to `--help`; the README only states the flow

---

## 17–20 min · Lab Handoff

[Block 2 Lab — Finish the oss-tool CLI](lab.md#2교시-실습--oss-tool-cli-완성하기)

[period2: examples for this lab](examples/period2/README.md)

Completion criteria:

1. `uv run oss-tool greet --name student01` prints a greeting
2. `uv run oss-tool sysinfo --json` prints valid JSON and leaves a file under `outputs/`
3. The README has the three run steps, and it's committed

30-minute lab, then a 10-minute break. Block 3 after the break.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Config Stays Outside the Repo, Code Stays Inside

---

## 0–3 min · The Cost of Config Baked into Code

```python
HOST = "http://10.0.0.5:11434"       # classroom server address
TOKEN = "hf_(actual token)"          # my token
```

- Change PCs, edit the code → the edited code gets committed → everyone gets my address
- If a token ends up in the repo, **publishing it leaks it instantly**
- Separate code from config, and the same code runs unchanged in the classroom, at home, or in CI

**Question:** If the classroom PC and your home PC have different Ollama addresses, how many lines of code need to change?

---

## 3–6 min · .env and .env.example

```text
.env.example   ← committed. just key names, sample values, and descriptions
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
HF_TOKEN=

.env           ← not committed. the actual values on my PC
```

- `.env.example` is **documentation**: "here's the list of settings this project reads"
- On a new PC: `Copy-Item .env.example .env`, then just fill in the values
- Even non-secret values (`OLLAMA_MODEL`) go through the same channel

---

## 6–9 min · python-dotenv and os.environ

```python
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()                        # .env → os.environ (won't override existing vars)
os.environ.get("OLLAMA_HOST")        # shows a mix of shell vars and .env values

file_values = dotenv_values(".env")  # reads only .env as a dict → source is traceable
```

- If the shell sets `$env:OLLAMA_MODEL = "qwen3:1.7b"`, it takes priority over `.env`
- The example `config.py` uses `dotenv_values` to record **where each value came from**

---

## 9–12 min · Config Layers: Default < .env < Environment Variable < Argument

```text
Default    DEFAULTS["OLLAMA_MODEL"] = "qwen3:8b"    in code, for textbook verification
  ↓ overridden by
.env       OLLAMA_MODEL=qwen3:0.6b                 this PC's standing setting
  ↓ overridden by
Env var    $env:OLLAMA_MODEL = "..."                only in this shell window
  ↓ overridden by
Argument   --model qwen3:14b                       only for this one run
```

**The narrower the scope, the higher the priority.** `oss-tool config` shows the value along with its source.

---

## 12–15 min · A Secret Already Committed Lingers Even After You Delete It

```text
commit 3  delete .env                ← the file is gone now, but
commit 2  edit README
commit 1  add .env (with a token)    ← anyone can read it with git log -p
```

- `.gitignore` only blocks files **not yet tracked**. It can't stop a file already added
- A pushed secret isn't "deleted" → the only fix is to **revoke the token and issue a new one (rotate it)**
- Rewriting history is a last resort, and it affects every collaborator

**Question:** You added `.env` to `.gitignore`, but `.env` still shows up in `git status`. Why?

---

## 15–17 min · A Mistake-Recovery Flow

```powershell
git add -f .env                    # fake lab values only! simulate bypassing ignore
git status                         # notice "new file: .env"
git restore --staged .env          # unstage only; keep the local file
git check-ignore -v .env           # the existing ignore applies again
git ls-files -- .env .env.example  # only .env.example should appear
git log --all --oneline -- .env    # also inspect history
```

Avoid `-f` in normal publishing. After ignoring `.env.*`, add the exception `!.env.example`.

---

## 17–20 min · Lab Handoff

[Block 3 Lab — A Config Loader and Separating Secrets](lab.md#3교시-실습--설정-로더와-비밀정보-분리)

[period3: examples for this lab](examples/period3/README.md)

Completion criteria:

1. `uv run oss-tool config` prints `OLLAMA_HOST`/`OLLAMA_MODEL`'s values and their sources
2. `.env.example` is committed and `.env` is blocked by `.gitignore`
3. You checked with `git log` and wrote a sentence confirming no secret is in history

30-minute lab, then a 10-minute break.

---

## This Week's Summary

```text
Reproducibility: commit pyproject.toml (intent) + uv.lock (result), exclude .venv → uv sync --locked
Structure:       src/oss_tool + [project.scripts] → uv run oss-tool <subcommand>
Config:          default < .env < environment variable < argument; commit only .env.example
```

Next week (`week04_ollama_local_llm`) uses the `OLLAMA_HOST`/`OLLAMA_MODEL` this `config.py` reads to **actually call a local model**.
