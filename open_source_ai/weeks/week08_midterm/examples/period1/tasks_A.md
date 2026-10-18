# 모의 실기 A — uv 사용법과 프로젝트 관리법

공개 동형 모의 문제다. 실제 실기 패킷의 문항·값·정답이 아니다. 제한 시간은 30분이며, 답안은 실습 폴더의 `answers_A.md`에 맨 아래 양식으로 쓴다. 허용 자료·AI 도구 범위는 실제 시험에서는 시험 공지를 따른다.

A-1은 직접 고치는 실기이고, A-2~A-4는 1·3주차에 배운 uv 사용법과 프로젝트 관리법을 묻는 개념 문항이다. 개념 문항은 **판단 + 근거** 두세 줄로 답하고, 명령은 실제로 입력하는 형태로 쓴다. 확신이 없으면 "확인할 문서나 명령"을 적는다. 빈칸보다 낫다.

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

## A-2 · uv 명령과 두 파일

### A-2-1 · `uv add`가 바꾸는 것

`uv init --no-package --python 3.12`로 만든 프로젝트에서 `uv add httpx`를 실행했다.

- (a) 이 명령으로 새로 생기거나 바뀌는 파일·폴더 세 가지를 쓰고, 각각 무엇을 담는지 한 줄씩 쓴다.
- (b) 그 셋 중 commit하지 않는 것은 무엇인가? 그것이 `git status`에 보이지 않는 이유를 그 폴더 안의 어떤 파일로 확인할 수 있는가?

### A-2-2 · 의도와 결과

`pyproject.toml`에는 `dependencies = ["httpx"]` 한 줄만 있고, `uv.lock`에는 `httpx`와 그 하위 패키지들의 정확한 버전과 해시가 들어 있다.

- (a) 수업에서 두 파일을 각각 "사람이 쓰는 ○○", "도구가 만든 ○○"라고 불렀다. ○○를 채우고 뜻을 쓴다.
- (b) `uv.lock`을 `.gitignore`에 넣으면 안 되는 이유를 "다른 오늘"이라는 말을 넣어 한 문장으로 쓴다.
- (c) `uv.lock`을 손으로 고치면 안 되는 이유는?

### A-2-3 · `--locked`가 실패하는 때

깨끗한 폴더에 clone한 복제본에서 `uv.lock`을 지우고 `uv sync --locked`를 실행했다.

- (a) 어떻게 되는가? 종료 코드는 0인가?
- (b) 같은 폴더에서 플래그 없이 `uv sync`를 실행하면 무엇이 달라지는가?
- (c) `--locked`와 `--frozen`의 차이를 한 줄로 쓴다. README의 재현 절차에 `--locked`를 쓰는 이유도 쓴다.

### A-2-4 · `uv run`이 먼저 하는 일

팀원이 `python main.py`로 실행했더니 `ModuleNotFoundError: No module named 'ollama'`가 났다. 같은 폴더에서 `uv run python main.py`로는 된다.

- (a) `uv run`이 프로그램을 실행하기 전에 하는 일 두 가지를 쓴다.
- (b) `uv run ex01`처럼 파일 이름이 아니라 **명령 이름**으로 실행할 수 있는 조건은 무엇인가? `pyproject.toml`의 어느 블록이 필요한가?
- (c) `uv run ex01`을 했는데 `Failed to spawn: ex01`이 나왔다. 먼저 확인할 것 두 가지를 쓴다.

## A-3 · 프로젝트 구조와 엔트리포인트

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

### A-3-1 · 이름과 함수를 잇는 한 줄

- (a) `oss-tool = "oss_tool.cli:main"`에서 `oss-tool`, `oss_tool`, `cli`, `main`은 각각 무엇인가? 명령 이름에는 하이픈, 패키지 이름에는 밑줄을 쓰는 이유도 쓴다.
- (b) `uv sync` 뒤 `.venv\Scripts\` 아래에 무엇이 생기는가? 그것을 만든 `pyproject.toml`의 줄은 어느 줄인가?
- (c) `main()`이 `0`이 아닌 값을 돌려주면 어떻게 되는가?

### A-3-2 · 오타는 언제 드러나는가

`oss_tool.cli:main`을 `oss_tool.cli:mian`으로 잘못 적고 `uv run oss-tool greet`를 실행했다.

- (a) `uv sync` 단계에서 실패하는가, 실행 단계에서 실패하는가? 그렇게 판단한 이유를 쓴다.
- (b) 마지막 오류 줄에는 어떤 종류의 오류가 보일까? 되돌린 뒤 무엇으로 확인하는가?

### A-3-3 · 왜 `src/` 아래에 두는가

```text
osa-practice/
 ├─ pyproject.toml
 ├─ src/
 │   └─ oss_tool/
 │       ├─ __init__.py
 │       ├─ cli.py
 │       ├─ sysinfo.py
 │       └─ config.py
 └─ outputs/
```

- (a) 코드를 `src/` 아래에 두면 어떤 종류의 버그가 사라지는가?
- (b) `uv init --package --python 3.12 --vcs none my-ollama`를 실행하면 같은 구조가 자동으로 생긴다. 생기는 파일 중 `.python-version`과 `src/my_ollama/__init__.py`는 각각 무엇을 위한 것인가? `uv run my-ollama`가 `Hello from my-ollama!`를 출력하기까지 이름이 함수로 연결되는 경로를 쓴다.
- (c) `outputs/`를 commit하지 않는 이유와, 그래도 보관할 결과(예: 환경 보고서)는 어떻게 하는지 1주차 방법으로 쓴다.

### A-3-4 · stdout·stderr와 README

`uv run oss-tool sysinfo --json | Out-String | ConvertFrom-Json`이 동작하려면 결과 JSON은 어디로, "저장 경로" 안내 로그는 어디로 나와야 하는가? 코드에서 각각 무엇으로 출력하는가(`print`/`logging`)? 마지막으로 README 「실행」 절의 세 줄을 `--locked`를 포함해 직접 쓴다.

## A-4 · 설정과 비밀 분리

### A-4-1 · `.env`와 `.env.example`

- (a) 둘 중 commit하는 것은 무엇인가? 각 파일에는 무엇이 들어 있어야 하는가?
- (b) 새 PC에서 프로젝트를 clone한 뒤 설정을 준비하는 명령 한 줄을 쓴다.
- (c) 비밀이 아닌 값(`OLLAMA_MODEL`)도 `.env`로 다루는 이유는?

### A-4-2 · 설정 계층

`.env`에 `OLLAMA_MODEL=qwen3:0.6b`, 셸에 `$env:OLLAMA_MODEL = "qwen3:1.7b"`, 명령에 `--model qwen3:14b`를 동시에 주고 `uv run oss-tool config`를 실행했다.

- (a) `OLLAMA_MODEL`의 값과 출처는 무엇으로 표시되는가? 네 단계 우선순위를 낮은 쪽부터 쓴다.
- (b) `--model`을 빼고 실행하면? 셸 변수까지 지우면?
- (c) `load_dotenv()` 대신 `dotenv_values(".env")`를 쓴 이유는?

### A-4-3 · 토큰은 화면에도 나오면 안 된다

`.env`에 `HF_TOKEN=hf_fake_token_for_class_only`가 있다. `uv run oss-tool config`의 화면 출력, `--json` 출력, `outputs/` 파일에 이 값이 그대로 나오면 안 되는 이유와, 코드가 어떤 규칙으로 값을 가리는지(키 이름의 어떤 단어를 보는지) 쓴다.

### A-4-4 · ignore 규칙 읽기

`.gitignore`에 다음이 있다.

```text
.env
.env.*
!.env.example
```

- (a) 세 줄이 각각 하는 일을 쓴다. `!`의 뜻은?
- (b) `git check-ignore -v .env` 출력이 알려 주는 것은?
- (c) `git ls-files -- .env .env.example`에는 무엇만 보여야 하는가? `git log --all --oneline -- .env`와 `git log --all --oneline -S "hf_fake_token"`이 둘 다 비어 있으면 무엇을 뜻하는가?

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

## A-2 uv 명령과 두 파일

### A-2-1
(a) 셋과 역할:
(b) commit하지 않는 것 / 확인 방법:

### A-2-2
(a):
(b):
(c):

### A-2-3
(a):
(b):
(c):

### A-2-4
(a):
(b):
(c):

## A-3 프로젝트 구조와 엔트리포인트

### A-3-1
(a):
(b):
(c):

### A-3-2
(a) 시점 / 이유:
(b):

### A-3-3
(a):
(b):
(c):

### A-3-4
결과 / 로그 / print·logging:
README 실행 절 세 줄:
1.
2.
3.

## A-4 설정과 비밀 분리

### A-4-1
(a):
(b):
(c):

### A-4-2
(a) 값 / 출처 / 우선순위:
(b):
(c):

### A-4-3

### A-4-4
(a):
(b):
(c):

## 못 끝낸 항목 (증상·관찰·시도)
```
