# 13주차 예제 — 테스트·CI·보안 점검이 붙은 최소 AI 서비스

12주차 앱 서버와 같은 구조(스키마·서비스·HTTP 계층)를 테스트하기 좋게 줄여 다시 쓴 uv 프로젝트다. 12주차 코드를 그대로 복사한 것이 아니다 — 요청 본문이 `messages` 목록이 아니라 `prompt`·`system`이고, 클라이언트가 동기이며, 예외→상태 코드가 12주차의 502·503·504가 아니라 503·404·502다. 1교시는 가짜 클라이언트를 주입한 pytest와 ruff, 2교시는 GitHub Actions, 3교시는 의존성 감사·비밀 검색·교차 리뷰에 쓴다. 학생 팀 저장소에는 `.github/workflows/ci.yml`, `audit_report.py`, `security_check.ps1`, `REVIEW_CHECKLIST.md`를 그대로 옮겨 붙이면 되고, `tests/`는 팀 코드의 스키마 필드·예외 이름·상태 코드에 맞춰 고쳐 쓴다.

```text
운영:   app/main.py get_service() ─▶ ChatService(client=HttpOllamaClient) ─HTTP─▶ Ollama(:11434)
테스트: tests/conftest.py         ─▶ ChatService(client=FakeOllamaClient) ─▶ 미리 정한 dict

CI:     push·PR ─▶ .github/workflows/ci.yml ─▶ setup-uv ─▶ uv sync ─▶ ruff check ─▶ ruff format --check ─▶ pytest
보안:   audit_report.py (uv export ─▶ pip-audit) ─▶ outputs/audit-*.md
        security_check.ps1 (토큰 패턴·.env 추적·pickle 모델 파일·trust_remote_code) ─▶ outputs/security-*.md
```

## 파일 구성

| 경로 | 역할 |
|---|---|
| `ci_lab/pyproject.toml` | uv 프로젝트. 실행 의존성(fastapi, uvicorn, httpx, python-dotenv) + `dev` 그룹(pytest, ruff, pip-audit). `[tool.pytest.ini_options]`(integration 마커 제외), `[tool.ruff]`(규칙·줄 길이) |
| `ci_lab/.env.example` | 설정 항목과 기본값. 복사해 `.env`로 쓴다 |
| `ci_lab/.gitignore` | `.venv`·`.env`·`outputs`·캐시를 Git 밖에 둔다 |
| `ci_lab/app/schemas.py` | `ChatRequest`(공백 prompt 거절 validator 포함)·`ChatResponse`·`HealthResponse` |
| `ci_lab/app/ollama_client.py` | `OllamaClient` 프로토콜, `HttpOllamaClient`(`/api/chat`·`/api/tags`, `think: false`), 예외 `OllamaUnavailableError`·`ModelNotFoundError`·`OllamaError` |
| `ci_lab/app/service.py` | `ChatService` — 클라이언트를 생성자에서 주입받는다. `health()`는 예외를 `ok=False`로, `chat()`은 예외를 그대로 올린다 |
| `ci_lab/app/main.py` | FastAPI 앱. `get_service`가 주입 지점(12주차 `get_client`와 같은 자리), 예외 → 503·404·502 |
| `ci_lab/tests/conftest.py` | `FakeOllamaClient`(`reply`·`models`·`fail_with`·`calls`), fixture `fake_client`·`service`·`make_service`·`api_for` |
| `ci_lab/tests/test_schemas.py` | 스키마 검증 5개 함수(parametrize 포함 8건) |
| `ci_lab/tests/test_service.py` | 응답 변환·옵션 전달·health 정상/모델 없음/서버 없음·chat 예외 6건 |
| `ci_lab/tests/test_api.py` | TestClient로 200·422·503·502 매핑 5건 |
| `ci_lab/tests/test_integration.py` | 실제 Ollama가 필요한 2건. `integration` 마커, `RUN_INTEGRATION=1`일 때만 실행 |
| `ci_lab/.github/workflows/ci.yml` | `test` 잡(setup-uv → sync → ruff → pytest) + `audit` 잡(uv export → pip-audit, `continue-on-error`) |
| `ci_lab/audit_report.py` | `uv export` → `pip-audit -f json` → `outputs/audit-*.md`·`.json` 요약. `--sample`·`--from-json`은 네트워크 없이 동작 |
| `ci_lab/security_check.ps1` | Git이 아는 파일에서 토큰 패턴·`.env` 추적·pickle 계열 모델 파일·`trust_remote_code=True`를 찾아 `outputs/security-*.md`에 기록. 문제가 있으면 종료 코드 1 |
| `ci_lab/REVIEW_CHECKLIST.md` | 교차 코드리뷰 항목(CI·코드·보안·출처)과 코멘트 양식(근거→문제→제안), 리뷰 기록 표 |
| `ci_lab/README.md` | 프로젝트 안 짧은 안내 |

모델 ID·주소·양자화·용량은 학기별 환경 기준표에서 확정하며, 코드의 기본값(`OLLAMA_HOST=http://localhost:11434`, `OLLAMA_MODEL=qwen3:8b`, CPU 대체 `qwen3:0.6b`)은 교재 검증용 기본값이다. `uv.lock`은 이 폴더에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

### 환경변수

| 변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | 실제 클라이언트가 찾아갈 모델 서버. 단위 테스트는 쓰지 않는다 |
| `OLLAMA_MODEL` | `qwen3:8b` | 기본 생성 모델. CPU 대체 `qwen3:0.6b` |
| `OLLAMA_TIMEOUT` | `60` | 실제 클라이언트의 응답 대기 시간(초) |
| `RUN_INTEGRATION` | (비어 있음) | `1`이면 `tests/test_integration.py`가 실제 서버를 호출한다 |

## 실행 방법

원본을 훼손하지 않도록 `ci_lab/`을 개인 실습 폴더에 복사한 뒤 그 안에서 실행한다. `$src`에는 교재 저장소의 이 `examples` 폴더 경로를 넣는다. 저장 경로는 학기별 환경 기준표를 따른다(아래는 예시).

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week13_test_ci_security\examples"
New-Item -ItemType Directory -Force C:\classwork\week13 | Out-Null
Copy-Item -Recurse "$src\ci_lab" C:\classwork\week13\ci_lab
Set-Location C:\classwork\week13\ci_lab
Copy-Item .env.example .env
uv sync                                   # dev 그룹까지 설치
```

테스트와 lint(모델 서버 불필요):

```powershell
uv run pytest -q                          # 19 passed, 2 deselected 가 기대값
uv run pytest -q --durations=3            # 느린 테스트 3개 표시
uv run ruff check .                       # lint. --fix 로 안전한 것만 자동 수정
uv run ruff format --check .              # 서식 검사만 (CI 와 같은 명령)
uv run ruff format .                      # 서식 적용
```

통합 테스트(실제 Ollama 필요):

```powershell
$env:RUN_INTEGRATION = "1"
uv run pytest -m integration -q --durations=3
Remove-Item Env:RUN_INTEGRATION
```

의존성 감사와 비밀 검색:

```powershell
uv run python audit_report.py             # uv export → pip-audit → outputs/audit-*.md (네트워크 필요)
uv run python audit_report.py --sample    # 네트워크 없이 보고서 형식만
.\security_check.ps1                      # outputs/security-*.md, 문제 있으면 종료 코드 1
.\security_check.ps1 -Path C:\classwork\team-a   # 다른 저장소 점검
```

GitHub Actions는 복사본을 **저장소 루트**로 만들어 push해야 돈다(`.github/workflows/ci.yml`이 루트 기준 경로이기 때문). 팀 저장소의 하위 폴더에 넣을 때는 `ci.yml`에 `defaults: run: working-directory: <폴더>`를 추가한다.

## 관찰 지점

1. `uv run pytest -q` 출력의 `19 passed, 2 deselected` — 2건은 `integration` 마커로 걸러진 것이다. `-m integration`으로 돌리면 `RUN_INTEGRATION`이 없을 때 `2 skipped`가 된다.
2. `tests/conftest.py`의 `FakeOllamaClient.calls` — 서비스가 클라이언트에 무엇을 넘겼는지(모델·messages 순서·options) 테스트가 들여다보는 통로다.
3. `test_service.py`의 `1500.0` — 나노초→밀리초 변환. `service.py`의 `1_000_000`을 `1_000`으로 바꾸면 이 테스트만 정확히 실패한다(2교시 빨간불 재료).
4. `test_api.py`의 422 본문 `detail[0]["loc"]` — 어느 필드가 잘못됐는지 pydantic이 알려 준다.
5. `ruff check` 출력의 규칙 코드(F401, I001, E501, B…)와 `--fix`가 고치는 것·고치지 않는 것.
6. `ci.yml`의 `test` 잡 step 이름과 로컬 명령이 **같다**는 점. CI 실패는 로컬에서 같은 명령으로 재현한다.
7. `outputs/audit-*.md`의 `고친 버전` 열 — 있으면 하한 올리기·`uv lock`, 없으면 판단·기록.
8. `outputs/security-*.md` — 찾은 줄의 내용은 적지 않고 파일·줄 번호만 적는다. 왜 그런지 생각해 본다.

## GPU 없을 때 · 네트워크 없을 때

- **GPU 없음**: 이번 주 단위·HTTP 계층 테스트는 모델을 쓰지 않으므로 차이가 없다. 통합 테스트만 `OLLAMA_MODEL=qwen3:0.6b`, `OLLAMA_TIMEOUT=180`으로 바꾼다.
- **Ollama 없음**: 1교시 전체와 3교시가 그대로 된다. 통합 테스트는 `RUN_INTEGRATION`을 비워 두면 `skipped`로 끝난다 — 그 자체가 "느린 테스트 표시"의 관찰 대상이다.
- **네트워크 없음**: `uv sync`는 패키지 캐시가 필요하므로 수업 전에 한 번 실행해 둔다. 2교시 GitHub Actions는 네트워크가 필수이므로 강의자 PC 시연 + 사전 캡처된 실행 로그로 대체하고, 학생은 `ci.yml`을 읽고 각 step에 대응하는 로컬 명령을 실행해 같은 결과를 기록한다. 3교시 `pip-audit`은 `audit_report.py --sample`로 보고서 읽기만 연습한다. `security_check.ps1`은 네트워크가 필요 없다.
- **GitHub 계정·저장소 문제**: 2교시는 짝의 저장소에 협업자로 들어가 같은 PR을 함께 만든다. 3교시 교차 리뷰는 짝의 PR로 진행한다.

## 복사 후 변형

- 팀 프로젝트에 가져갈 때: `app/`은 팀 코드로 바꾸고 `tests/conftest.py`의 `FakeOllamaClient`는 팀 클라이언트의 메서드 모양에 맞춘다. 주입 지점(`get_service` 또는 12주차 `get_client`)은 반드시 유지한다.
- `ci.yml`은 팀 저장소 루트의 `.github/workflows/`로 옮기고, `uv.lock`을 커밋했다면 `uv sync`를 `uv sync --locked`로 바꾼다(`--frozen`은 lock을 검사하지 않으므로 어긋나도 통과한다).
- 실패 재현은 예제 원본이 아니라 복사본에서 한다. `service.py`의 단위 변환, `schemas.py`의 범위 값을 바꿔 어느 테스트가 잡아내는지 본다.
- `outputs/`는 Git에 넣지 않는다. 제출 증거로 쓸 `audit-*.md`·`security-*.md`는 별도 폴더(예: `evidence/week13/`)로 복사해 커밋한다. 복사 전에 사용자 홈 경로 같은 개인 식별 정보가 없는지 확인한다.
