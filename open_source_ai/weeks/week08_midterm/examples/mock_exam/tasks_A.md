# 모의 실기 A — uv 사용법과 프로젝트 관리법

공개 동형 모의 문제다. 실제 실기 패킷의 문항·값·정답이 아니다. 제한 시간은 30분이며, 답안은 실습 폴더의 `answers_A.md`에 맨 아래 양식으로 쓴다. 허용 자료·AI 도구 범위는 실제 시험에서는 시험 공지를 따른다.

A-1·A-2는 직접 하는 실기이고, A-3·A-4는 3·4주차에 배운 것을 짧게 설명하는 개념 문항이다. 명령과 터미널 출력은 그대로 붙이고, 개념 문항은 한두 문장으로 답한다. 확신이 없으면 "확인할 명령이나 문서"를 적는다. 빈칸보다 낫다.

## A-1 · 깨진 uv 프로젝트 복구

### 요구사항

`make_broken_repo.ps1`이 만든 `week08-mock-a` 저장소를 다음 상태로 만든다.

1. `uv sync`가 오류 없이 끝나고 의존성이 설치된다.
2. `uv run python report.py`가 `outputs/report.json`을 만든다.
3. `.env`는 Git 추적에서 빠지고, `.gitignore`와 값이 비어 있는 `.env.example`이 추적된다.
4. 위 변경이 한 commit으로 정리되어 있고 `git status`가 clean이다.

`report.py`는 고치지 않는다. 그 파일에는 오류가 없다.

### 완료 조건

- [ ] `uv sync` 출력의 `Resolved N packages`에서 N이 2 이상이고 설치 줄이 보인다.
- [ ] `uv run python report.py`의 종료 코드가 0(연결됨) 또는 2(연결 실패)다.
- [ ] `outputs/report.json`에 `host`, `model`, `ollama_reachable`, `model_available`, `hf_token_present` 키가 있다.
- [ ] `git ls-files`에 `.env`가 없고 `.gitignore`, `.env.example`이 있다.
- [ ] `git status`가 clean이다.

### 검증 순서

```powershell
uv sync
uv run python report.py
$LASTEXITCODE
Get-Content outputs\report.json
git ls-files
git status
git log --oneline
```

### 답안에 적을 것

고친 항목마다 한 줄: `증상(첫 오류 메시지의 핵심) → 원인 → 고친 내용`. 그리고 "`.env`를 `git rm --cached`로 뺀 뒤에도 남아 있는 문제"를 한 줄로 적는다.

## A-2 · 표준 양식 프로젝트 만들기와 `uv run hello`

4주차 2교시 문제 0에서 한 것을 처음부터 다시 한다. 명령과 터미널 출력은 그대로 답안에 붙인다.

### 요구사항

1. `C:\classwork\week08` 아래에서 `uv init --package --python 3.12 --vcs none week8-hello`로 프로젝트를 만든다.
2. `src/week8_hello/__init__.py`의 `main()`이 `Hello, uv!`를 출력하게 고친다.
3. `pyproject.toml`의 `[project.scripts]`에 `hello` 명령을 추가해 `uv run hello`가 그 문장을 출력하게 한다.
4. `.gitignore` 파일을 만들어 `__pycache__/` 한 줄을 적고, `git init` → `git status` → `git add .` → `git status` → `git commit -m "Add hello project"` → `git log --oneline`을 차례로 실행한다.

### 완료 조건

- [ ] `uv run hello`가 `Hello, uv!`를 출력한다.
- [ ] `pyproject.toml`에 `[project.scripts]`의 `hello` 줄과 `[build-system]`이 있고, `.python-version`이 `3.12`다.
- [ ] `git log --oneline`에 commit이 1개 있고, `git status`가 clean이며 `.venv/`는 어디에도 보이지 않는다.

### 검증 순서

```powershell
uv run hello
Get-Content pyproject.toml
Get-Content .python-version
git status
git log --oneline
```

### 답안에 적을 것

- `pyproject.toml` 전체, `__init__.py` 전체, `uv run hello`의 출력.
- (a) `uv run hello`를 입력하면 어느 줄 덕분에 `main()`이 실행되는지 한 문장("패키지:함수" 형식을 언급).
- (b) 프로젝트 폴더에 생긴 `.venv`와 `uv.lock`은 각각 무엇이고, 둘 중 Git에 올리지 않는 것은 어느 쪽인가. `.venv/`는 `.gitignore`에 적지 않았는데도 `git status`에 보이지 않는 이유.
- (c) `git add .` 전과 후의 `git status` 출력, `git log --oneline` 출력.
- (d) `git add`가 하는 일(staging area가 무엇인지)과 `git commit`이 하는 일을 각각 한 문장으로. commit까지 했는데 GitHub에 보이지 않을 때 빠진 명령.

<details>
<summary>힌트</summary>

- `uv init --package`가 만든 `pyproject.toml`에는 이미 `[project.scripts]`에 `week8-hello = "week8_hello:main"` 한 줄이 있다. 그 아래에 `hello = "week8_hello:main"`을 한 줄 더 적으면 된다. 형식은 `명령이름 = "패키지:함수"`다.
- `main()`은 `src/week8_hello/__init__.py`에 있다. `print(...)` 안의 문장만 바꾼다.
- `uv run hello`가 `Failed to spawn: hello`라고 하면 `[project.scripts]`에 `hello` 줄이 있는지 보고 `uv sync`를 한 번 실행한다. 그러면 `.venv\Scripts\hello.exe`가 생긴다.
- `git status`의 `Untracked files`는 아직 Git이 모르는 파일, `Changes to be committed`는 `git add`로 올라간 다음 commit 후보다. `.venv` 안에는 uv가 만든 `.gitignore`가 있어서 보이지 않는다.
- `git commit`이 이름과 메일을 묻으면 `git config user.name student01`, `git config user.email student01@example.com`(수업용 값)을 설정하고 다시 commit한다.
</details>

## A-3 · 프로젝트 구조 읽기

3주차 `oss-tool`의 `pyproject.toml` 일부다.

```toml
[project.scripts]
oss-tool = "oss_tool.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oss_tool"]
```

- (a) `oss-tool = "oss_tool.cli:main"`에서 `oss-tool`, `oss_tool`, `cli`, `main`은 각각 무엇인가?
- (b) 코드를 `src/` 아래에 두는 이유를 한 문장으로 쓴다.
- (c) `uv sync`가 끝나면 `.venv\Scripts\` 아래에 무엇이 생기고, 그래서 어떤 명령을 칠 수 있게 되는가?
- (d) README 「실행」 절에 적을 세 줄을 `uv sync --locked`부터 쓴다.

<details>
<summary>힌트</summary>

3주차 2교시 슬라이드 「엔트리포인트: 이름과 함수를 잇는 한 줄」과 「src 레이아웃」을 다시 본다. 형식은 `명령이름 = "패키지.모듈:함수"`이고, 명령 이름은 하이픈, 패키지 이름은 밑줄이다. README 세 줄은 3주차 2교시 문제 2의 5번 그대로다.
</details>

## A-4 · 설정 파일과 비밀값

- (a) `.env`와 `.env.example` 중 commit하는 것은 무엇인가? 각 파일에는 무엇이 들어 있어야 하는가?
- (b) 새 PC에서 clone한 뒤 설정을 준비하는 명령 한 줄을 쓴다.
- (c) `.env`에 `OLLAMA_MODEL=qwen3:0.6b`가 있고 명령에 `--model qwen3:14b`를 주었다. `uv run oss-tool config`는 어느 값을 보여 주는가? 이유를 한 줄로 쓴다(설정 계층).
- (d) `.gitignore`에 `.env`, `.env.*`, `!.env.example` 세 줄이 있다. 각 줄이 하는 일을 쓴다.

<details>
<summary>힌트</summary>

3주차 3교시: `.env.example`은 키 이름과 예시값만 적어 commit하고, `.env`는 내 PC의 실제 값이라 commit하지 않는다. 설정 계층은 기본값 < `.env` < 셸 환경변수 < 명령 인자다. `!`는 "이 파일은 예외"라는 뜻이다.
</details>

## `answers_A.md` 양식

```markdown
# 모의 실기 A 답안 — student01

## A-1 복구 기록

| 순서 | 증상(첫 오류의 핵심) | 원인 | 고친 내용 |
|---:|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |

`.env`를 추적에서 뺀 뒤에도 남는 문제:

마지막 commit id:

## A-2 표준 양식 프로젝트

pyproject.toml:
```toml
```

__init__.py:
```python
```

uv run hello 출력:

(a) main()이 실행되는 이유:
(b) .venv / uv.lock / 올리지 않는 것 / .venv가 안 보이는 이유:
(c) git add 전 status / 후 status / log:
(d) add / commit / 빠진 명령:

## A-3 프로젝트 구조

(a):
(b):
(c):
(d) README 실행 절 세 줄:
1.
2.
3.

## A-4 설정 파일과 비밀값

(a):
(b):
(c):
(d):

## 못 끝낸 항목 (증상·관찰·시도)
```
