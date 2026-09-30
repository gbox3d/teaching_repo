---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 13"
footer: "Testing, CI, Security, and Code Review"
---

# Week 13
## Testing, CI, Security, and Code Review

**3 × 60-minute blocks**<br>
Each block: 20 min explanation/demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Sessions

| Session | 20 min explanation/demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | pytest structure, isolating model calls, unit vs. integration, ruff | Build service tests with a fake client |
| Block 2 | GitHub Actions structure, setup-uv/caching, status checks, reading failure logs | Turn GitHub Actions green, then red |
| Block 3 | Supply-chain security, preventing secret leaks, model-file safety, review checklist | Dependency audit, secret scanning, cross-review |

This week's question: **How do we automatically check code that calls a model, and how do we safely accept someone else's changes?**

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## Check It Even With the Model Turned Off

---

## 0–3 min · Automating "It Works on My PC"

In Week 12 we reproduced 502/503/504 **by hand** — changing environment variables, restarting the server, checking with our own eyes.

- Repeat that procedure for every reviewer and every PR, and eventually nobody does it
- Tests = that same checking procedure, **written down as code**. One line, `uv run pytest`, repeats it
- What gets checked: our own code's conversion, validation, and error mapping
- What doesn't get checked: the quality of the model's answers (that's Week 11's evaluation)

**Question:** The model's answer is different every time — so what can you actually `assert`?

---

## 3–6 min · pytest Structure — Discovery, assert, Output

```python
# tests/test_schemas.py   ← files named test_*.py, functions named test_*, found automatically
from app.schemas import ChatRequest

def test_valid_request_uses_defaults():
    request = ChatRequest(prompt="question")
    assert request.temperature == 0.2   # on failure, both sides are shown together
```

```text
uv run pytest -q
...........F.......                                            [100%]
FAILED tests/test_service.py::test_chat_converts_fake_response - assert 1500000.0 == 1500.0
```

The failure summary's `assert left == right` is your first clue. Read **the difference between the two values** before you read the whole stack trace.

---

## 6–9 min · Fixtures and parametrize

```python
@pytest.fixture
def service(fake_client):                # injected into any parameter with this name
    return ChatService(client=fake_client, model="fake-model:test", host="http://fake")

@pytest.mark.parametrize("body", [
    {"prompt": ""}, {"prompt": "hi", "temperature": 5.0}, {"prompt": "hi", "max_tokens": 0},
])
def test_out_of_range_request_is_rejected(body):
    with pytest.raises(ValidationError):
        ChatRequest(**body)
```

- Fixture: setup code lives in one place. Put it in `tests/conftest.py` and every test file shares it
- parametrize: run the same check against several inputs. On failure, it shows **which input** failed

---

## 9–12 min · Isolating Model Calls — Dependency Injection

```text
Production: main.py get_service() ─▶ ChatService(client=HttpOllamaClient) ─▶ Ollama :11434
Test:       conftest.py            ─▶ ChatService(client=FakeOllamaClient) ─▶ a fixed dict
```

- The service depends only on a **shape (Protocol)** — `chat()`, `list_models()` — not a concrete class
- The fake lets you set `reply`/`fail_with` to produce success or failure at will, and `calls` lets you see what was passed in
- The HTTP layer uses `app.dependency_overrides[get_service]` + `TestClient` — checks 422/503 without starting uvicorn
- Week 12's `get_client` is exactly this seam

**Question:** If the fake's response shape doesn't match the real Ollama, what does a passing test actually guarantee?

---

## 12–15 min · Unit vs. Integration, Marking Slow Tests

| Kind | Target | Requires | Speed | When |
|---|---|---|---|---|
| Unit | schema, service | nothing | ms | every save, every push |
| HTTP layer | routing, status codes | TestClient | ms | every push |
| Integration | real Ollama | server, model, GPU | seconds–minutes | manually, before release |

```toml
[tool.pytest.ini_options]
addopts = "-m 'not integration'"        # excluded from the default run
markers = ["integration: slow tests that need a real Ollama server"]
```

Add `pytestmark = pytest.mark.integration` at the top of the file, and it only actually runs when `RUN_INTEGRATION=1`.

---

## 15–17 min · ruff — Lint and Format

```powershell
uv run ruff check .             # list of issues. --fix only applies safe, automatic fixes
uv run ruff format --check .    # check only, don't fix (for CI)
uv run ruff format .            # actually fix it
```

- lint: unused imports (F401), undefined names (F821), import order (I), common bugs (B), long lines (E501)
- format: line breaks, quotes, whitespace — **hand style arguments over to the tool**
- Rules live under `[tool.ruff]` in `pyproject.toml`. The whole team shares the same rules

**Question:** If "two spaces here" comments disappear, what does the reviewer spend their time on instead?

---

## 17–20 min · Handing Off to the Lab

[Block 1 lab — Build service tests with a fake client](lab.md#1교시-실습--가짜-클라이언트로-서비스-테스트-만들기) · [Block 1 files](examples/period1/README.md)

Done when:

1. You added 3 tests (reject a blank prompt, system-prompt ordering, model-missing → 404) and `uv run pytest` passes
2. `ruff check` and `ruff format --check` both pass, and you have a record of fixing a deliberately introduced issue with `--fix`
3. `pytest -m integration` shows `skipped` or actually runs, depending on `RUN_INTEGRATION`

30 min lab, then a 10 min break.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## The Checks Run Outside My PC

---

## 0–3 min · What CI Does

```text
push / PR ─▶ GitHub rents a clean virtual machine ─▶ checkout ─▶ uv sync ─▶ ruff ─▶ pytest ─▶ green / red
```

- **The same procedure, every time**, in a place where "works on my PC" doesn't apply
- The result shows up on the PR as a status check — reviewers see a green light instead of a log
- This combines Week 3's reproducibility (`uv sync`) with Block 1's tests

**Question:** Does a green CI light mean "there are no bugs"?

---

## 3–6 min · Workflow Structure — on, jobs, steps

```text
.github/workflows/ci.yml       ← must be at exactly this path from the repo root to be recognized
├─ on:           when (push, pull_request, workflow_dispatch)
├─ permissions:  token permissions (contents: read is the minimum)
└─ jobs:
   └─ test:      runs-on: ubuntu-latest
      └─ steps:  uses (someone else's action) / run (a shell command), in order
```

- Jobs run in parallel on separate machines; steps run in order on one machine
- If a step fails, that job stops right there → **the name of the failed step** is your first clue

---

## 6–9 min · Reading ci.yml

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v7
        with: { enable-cache: true }
      - run: uv python install          # reads requires-python
      - run: uv sync                    # use --frozen if you committed the lock file
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pytest -q
```

These are **the same commands** you'd type locally. Only the machine is different.

---

## 9–12 min · setup-uv, Caching, and Lock Verification

- `astral-sh/setup-uv`: installs uv, and with `enable-cache: true`, reuses downloaded packages on the next run
- Compare the `uv sync` time between the first run and the second
- `uv sync --frozen` installs from the lock file **without checking it** — it still passes even if the lock is stale. `uv sync --locked` (or `uv lock --check`) is what **fails** a PR that forgot to update the lock
- The runner is Linux — `C:\` paths and `.ps1` scripts don't run in CI
- Pin action major versions (`@v5`, `@v7`) using the environment baseline document

**Question:** Can a cache hold onto an old, vulnerable version? What actually determines the installed version?

---

## 12–15 min · PR Status Checks and Branch Protection

| Indicator | Meaning | Reviewer action |
|---|---|---|
| Yellow circle | running | wait |
| Green check | all required jobs passed | start the code review |
| Red X | at least one failed | attach the log link in a comment and request changes |

- Settings → Branches → `main` protection rule: **required status checks** + PR required
- A red light locks the merge button. Even admins get no exception
- Write this rule as one line in Week 9's `CONTRIBUTING.md`

---

## 15–17 min · How to Read a Failure Log

```text
1. Actions tab → the failed run → click the red job
2. In the step list, find the one marked X → what command did that step run?
3. Copy the log's first error line (FAILED …, error:, E501 …)
4. Reproduce locally with the same command → fix it → push → green again
```

- Look at the **first error**, not the last one. Later errors are usually consequences of the first
- Passes locally but fails only in CI: OS differences (paths, case sensitivity), no cache yet, missing environment variables

**Question:** `pytest` passes locally but CI raises `ModuleNotFoundError`. What do you suspect first?

---

## 17–20 min · Handing Off to the Lab

[Block 2 lab — Turn GitHub Actions green, then red](lab.md#2교시-실습--github-actions로-초록불과-빨간불-만들기) · [Block 2 files](examples/period2/README.md)

Done when:

1. You pushed to a new repository, the first Actions run went green, and the status check appears on a PR
2. You caused a red light with a deliberately broken commit and recorded **the failed step's name and the first error line**
3. You made it green again with a fix commit and merged the PR

30 min lab, then a 10 min break.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## Safely Accepting Someone Else's Code

---

## 0–3 min · Supply Chain — the ~300 Lines I Wrote, the Tens of Thousands I Pulled In

```text
ci_lab (~300 lines of my own code)
 ├─ fastapi ─ starlette ─ anyio ─ …
 ├─ pydantic ─ pydantic-core ─ typing-extensions
 ├─ httpx ─ httpcore ─ h11 ─ certifi
 └─ pytest, ruff, pip-audit ─ …           → count them with `uv export` and it's over 40
```

- My code can be safe and the service still gets compromised through a hole in one dependency
- **A model file is a dependency too** — a weights file can have code embedded inside it

**Question:** Have you ever counted how many packages a single `uv sync` pulls in?

---

## 3–6 min · pip-audit — Checking Against Known Vulnerabilities

```powershell
uv export --format requirements-txt --no-hashes -o outputs/requirements-audit.txt
uv run pip-audit -r outputs/requirements-audit.txt --no-deps
uv run python audit_report.py            # both of the above + a summary in outputs/audit-*.md
```

Reading the result: package · installed version · vulnerability ID (PYSEC/GHSA/CVE) · **fixed version**

- A fixed version exists → raise the lower bound → `uv lock` → test → PR
- No fixed version → decide whether we actually use that feature, and record it
- Querying the vulnerability database needs network access. CI's `audit` job runs with `continue-on-error`

---

## 6–9 min · Lock Verification and Typosquatting

| Risk | Example | Defense |
|---|---|---|
| A package name one letter off | `requests` vs. `reqeusts` | check the PyPI page, repo link, and download count before installing |
| Installing without a lock file | today's and tomorrow's versions differ | commit `uv.lock` + `uv sync --frozen` |
| A tampered distribution file | same version, different contents | uv checks the sha256 against the lock |
| A "just bumped the version" PR | dependency diff not reviewed | read the `uv.lock` diff + require a green CI |

Read the package name **one more time** before `uv add`. A typo'd package can run code the moment it's installed.

---

## 9–12 min · Preventing Secret Leaks — Three Layers

```text
Layer 1, my PC:    .gitignore(.env) + security_check.ps1 (before commit)   ← can be automated with a pre-commit hook
Layer 2, GitHub:   secret scanning + push protection (blocks the push itself if a pattern matches)
Layer 3, after:    if it's in history, deleting it doesn't end it → rotate the token (revoke and reissue)
```

- `security_check.ps1`: token patterns, tracked `.env`, pickle model files, `trust_remote_code` — it **never prints the content** of a matched line
- Same principle as Week 3's `git log -p` check: once a secret is pushed, treat it as leaked

**Question:** Push protection blocked it. Is that token still safe?

---

## 12–15 min · Model-File Safety — pickle vs. safetensors

| Format | Loading method | Risk |
|---|---|---|
| `.pkl`, `.pt`, `.bin` (pickle) | deserializes Python objects = can execute code | arbitrary code just from opening the file |
| `.safetensors` | tensor data only, no code | low. the Hub default (e.g. `Qwen/Qwen2.5-0.5B-Instruct`) |
| `.gguf` (Ollama) | weights + metadata | low |

- `trust_remote_code=True` **runs the Python code in the model repo** → pin the repo and revision, read the code, and record it
- Don't accept adapters or checkpoints of unknown origin. Record revisions and hashes in `SOURCES.md`

---

## 15–17 min · Cross Code Review — What to Look At, How to Say It

Order: description/Issue → green CI → tests present? → error paths → secrets/dependencies → provenance/docs (`REVIEW_CHECKLIST.md`)

```text
[Evidence] app/service.py line 42: total_duration is divided by 1_000.
[Problem] Ollama reports nanoseconds, so the result isn't ms. It disagrees with test_service's 1500.0.
[Suggestion] Divide by 1_000_000 instead, and name the variable with its unit (duration_ms).
```

- One comment = **evidence (file:line) → problem → suggestion**. Style preferences are `nit`
- The verdict is one of two: approve / request changes (+ what would earn an approval)

**Question:** What's the difference between "this code is bad" and the comment above?

---

## 17–20 min · Handing Off to the Lab

[Block 3 lab — Dependency audit, secret scanning, cross-review](lab.md#3교시-실습--의존성-감사와-비밀-검색-교차-리뷰) · [Block 3 files](examples/period3/README.md)

Done when:

1. `outputs/audit-*.md` states the number of packages checked, the number of vulnerabilities, and the next action
2. `security_check.ps1` found 0 issues in a clean repo, caught every planted `.env`, fake token, and `.pt` file, and you removed what you planted
3. You left 2+ checklist-based comments and a verdict on another team's PR, and recorded the URL

30 min lab, then a 10 min break.

---

## This Week's Wrap-Up

```text
Tests:   inject a fake client → check conversion/validation/error-mapping without a model → separate slow ones with a marker
CI:      push/PR → clean machine → uv sync → ruff → pytest → must be green to merge
Security: pip-audit (dependencies) + security_check (secrets, model files) + checklist review (humans)
```

Let the machine catch what a machine can catch (ruff, pytest, CI, pip-audit); humans spend their time on **judgment backed by evidence**.

Next week (`week14_release_feedback`): release the green-lit repository as `v0.1.0`.
