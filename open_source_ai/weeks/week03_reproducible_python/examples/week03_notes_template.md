# 3주차 기록 — 재현 가능한 Python 프로젝트

- 이름: student01
- 저장소: (URL)
- 이 파일은 개인 저장소의 `notes/week03.md`로 복사해 채운다. 사용자 홈 경로·토큰·개인정보를 적지 않는다.

## 1교시 · uv 프로젝트와 재현

### 예상표

| 관찰 대상 | 예상 | 실제 |
|---|---|---|
| `uv init` 뒤 새로 생기는 파일 |  |  |
| `uv add httpx` 뒤 새로 생기는 파일·폴더 |  |  |
| `uv add httpx` 뒤 `git status`에 `.venv/`가 보이는가 |  |  |
| clone한 복제본에 있는 것과 없는 것 |  |  |
| 복제본에서 `uv.lock`을 지우고 `uv sync --frozen`하면 |  |  |

### 실패 경로

- `uv.lock` 없이 `uv sync --frozen` — 오류 첫 줄:
- 종료 코드(`$LASTEXITCODE`):
- 플래그 없는 `uv sync` 뒤 `git diff --stat` 결과:

### 재현 로그

- 파일: `notes/week03_reproduce.md`
- 네 단계 결과(OK/FAIL):

### 설명 문장

- `pyproject.toml`만 커밋하면 재현이 아닌 이유:
- `.venv/`가 `git status`에 보이지 않는 이유:

## 2교시 · oss-tool CLI

### 예상표

| 관찰 대상 | 예상 | 실제 |
|---|---|---|
| `[project.scripts]`의 함수 이름이 틀리면 실패하는 시점(sync·실행) |  |  |
| `uv sync` 뒤 `.venv\Scripts`에 생기는 파일 |  |  |
| `uv run oss-tool greet`와 `uv run python src\oss_tool\cli.py greet`의 차이 |  |  |
| `.venv\Scripts\oss-tool.exe`를 만든 `pyproject.toml`의 줄 |  |  |

### 실패 경로

- 엔트리포인트 오타(`mian`) — 오류 마지막 줄:
- 실패한 시점(sync 때·실행 때):

### 실행 출력

- `uv run oss-tool greet --name student01`:
- `uv run oss-tool sysinfo --json | Out-String | ConvertFrom-Json | Select-Object os, python`:
- `outputs/`에 생긴 파일 이름:

### 설명 문장

- `python sysinfo.py`와 `oss-tool sysinfo`의 차이:

## 3교시 · 설정 로더와 비밀정보

### 예상표

| 관찰 대상 | 예상 | 실제 |
|---|---|---|
| `.env`·셸 변수·`--model`을 동시에 주면 이기는 것 |  |  |
| `HF_TOKEN` 값의 화면 표시 |  |  |
| `.gitignore`에 `.env`가 없을 때 `git add .` 뒤 `.env`의 상태 |  |  |

### 출처 관찰

| 방법 | 명령 | `OLLAMA_MODEL` 값 | 출처 |
|---|---|---|---|
| 아무것도 없음 | `uv run oss-tool config` |  |  |
| `.env` | `uv run oss-tool config` |  |  |
| 셸 환경변수 | `$env:OLLAMA_MODEL = "qwen3:1.7b"` 뒤 `uv run oss-tool config` |  |  |
| 명령 인자 | `uv run oss-tool config --model qwen3:14b` |  |  |

### 실수 복구 기록

- `git add .` 뒤 `git status`의 `.env` 줄:
- `git restore --staged .env` 뒤 `git status`의 `.env` 줄:
- `.gitignore`에 `.env` 추가 뒤 `git status`·`git check-ignore -v .env`:

### 이력 검사

- `git log --all --oneline -- .env` 결과:
- `git log --all --oneline -S "hf_fake_token"` 결과:
- 결론 문장:

### 설명 문장

- `.gitignore`가 막지 못하는 경우:

## 확장 문제(선택)

- 수행한 확장 문제 번호와 결과:
