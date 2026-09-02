# 12주차 예제 — FastAPI 앱 서버 + Ollama 모델 서버 + Gradio UI

모델 서버(Ollama)와 앱 서버(FastAPI)를 분리한 최소 서비스 구조다. 1교시는 앱 서버와 오류 응답, 2교시는 스트리밍과 UI, 3교시는 Dockerfile과 재현 절차에 쓴다. 학생 팀 프로젝트의 서비스 베타는 이 구조를 복사해 기능만 바꾸면 된다.

```text
UI(ui/gradio_app.py, :7860) ──HTTP──▶ 앱 서버(app/main.py, :8000) ──HTTP──▶ 모델 서버(Ollama, :11434)
smoke_test.py ────────────────────────┘        └ app/ollama_client.py
```

## 파일 구성

| 경로 | 역할 |
|---|---|
| `ai_service/pyproject.toml` | uv 프로젝트(fastapi, uvicorn, httpx, python-dotenv, gradio) |
| `ai_service/.env.example` | 설정 항목과 기본값. 복사해 `.env`로 쓴다 |
| `ai_service/.gitignore`, `.dockerignore` | `.env`·`.venv`·`outputs`를 Git과 이미지 밖에 둔다 |
| `ai_service/app/schemas.py` | pydantic 요청·응답 스키마(`ChatRequest`, `ChatResponse`, `HealthResponse`, `ErrorResponse`) |
| `ai_service/app/ollama_client.py` | Ollama `/api/tags`·`/api/chat` 호출. 실패를 `OllamaUnavailable`·`OllamaTimeout`·`OllamaModelMissing`으로 구분. 단독 점검 CLI 포함 |
| `ai_service/app/main.py` | `/health`, `/chat`, `/chat/stream`(SSE), 예외→502·503·504, `request_id`·소요 시간 기록, CORS |
| `ai_service/ui/gradio_app.py` | `/chat/stream`(기본) 또는 `/chat`(`--no-stream`)에 붙는 채팅 UI. 오류 코드별 안내 문구 |
| `ai_service/smoke_test.py` | 세 엔드포인트를 호출해 상태 코드·시간을 `outputs/smoke-*.json`으로 기록 |
| `ai_service/Dockerfile` | uv 공식 이미지, 의존성 레이어 → 코드 레이어, `HEALTHCHECK` |
| `ai_service/reproduce_check.ps1` | 필수 파일·`.env` 추적 여부·실행 경로(docker/uv) 점검 |
| `ai_service/README.md` | 프로젝트 안 짧은 안내 |

모델 ID·주소·양자화·용량은 학기별 환경 기준표에서 확정하며, 코드의 기본값(`OLLAMA_HOST=http://localhost:11434`, `OLLAMA_MODEL=qwen3:4b`)은 교재 검증용 기본값이다. `uv.lock`은 이 폴더에 두지 않는다. 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.

## 실행 방법

원본을 훼손하지 않도록 `ai_service/`를 개인 실습 폴더에 복사한 뒤 그 안에서 실행한다. `$src`에는 교재 저장소의 이 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week12_ai_service_deploy\examples"
New-Item -ItemType Directory -Force C:\classwork\week12 | Out-Null
Copy-Item -Recurse "$src\ai_service" C:\classwork\week12\ai_service
Set-Location C:\classwork\week12\ai_service
Copy-Item .env.example .env
uv sync
```

터미널 A — 앱 서버:

```powershell
uv run uvicorn app.main:app --port 8000 --reload
```

터미널 B — 점검과 UI:

```powershell
uv run python smoke_test.py                  # /health → /chat → /chat/stream, outputs/smoke-*.json
uv run python smoke_test.py --skip-stream    # 스트리밍 제외
uv run python smoke_test.py --show-events    # SSE 원문 앞 5줄 출력
uv run python ui/gradio_app.py               # http://localhost:7860, 스트리밍 모드
uv run python ui/gradio_app.py --no-stream   # 비스트리밍 모드
uv run python -m app.ollama_client           # 앱 서버 없이 Ollama 클라이언트만 점검
```

컨테이너(Docker가 있을 때):

```powershell
docker build -t osa-ai-service:dev .
docker run --rm -p 8001:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 -e OLLAMA_MODEL=qwen3:4b osa-ai-service:dev
uv run python smoke_test.py --api http://localhost:8001 --skip-stream
```

### 환경변수

| 변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | 앱 서버가 찾아갈 모델 서버 주소. 컨테이너 안에서는 `http://host.docker.internal:11434` |
| `OLLAMA_MODEL` | `qwen3:4b` | 기본 생성 모델. CPU 대체 `qwen3:0.6b` |
| `OLLAMA_TIMEOUT` | `60` | 생성 응답 대기 시간(초). `0.5`로 줄이면 504 재현 |
| `APP_HOST`, `APP_PORT` | `127.0.0.1`, `8000` | `python -m app.main`으로 띄울 때의 주소 |
| `SYSTEM_PROMPT` | 수업 도우미 문장 | 클라이언트가 system을 보내지 않았을 때 붙이는 기본 프롬프트 |
| `CORS_ORIGINS` | `http://localhost:7860,http://127.0.0.1:7860` | 브라우저 직접 호출을 허용할 출처 |
| `LOG_DIR` | `outputs` | `requests.jsonl`, `smoke-*.json`, `ui-turns.jsonl` 위치 |
| `API_BASE_URL` | `http://localhost:8000` | UI·점검 스크립트가 바라보는 앱 서버 |

우선순위는 코드 기본값 → `.env` → 셸 환경변수 → 명령 인자 순으로 뒤가 앞을 덮는다. `--reload`는 파일 변경만 감지하므로 환경변수를 바꾸면 서버를 다시 띄운다.

## 관찰 지점

1. 터미널 A 첫 로그: 모델 서버 주소와 기본 모델 — 설정이 어디서 왔는지(`.env`인지 셸 변수인지) 말할 수 있어야 한다.
2. `/health`의 `status`·`reachable`·`has_model`: 앱 서버가 **살아 있는 것**(200)과 모델 서버가 **준비된 것**(`ok`)의 차이.
3. `/chat` 실패 코드: 없는 포트 → 502 `OllamaUnavailable`, 없는 모델 → 503 `OllamaModelMissing`, 짧은 타임아웃 → 504 `OllamaTimeout`, 범위 밖 값 → 422. 본문은 항상 `{"request_id", "error", "detail"}`.
4. `smoke_test.py --show-events`: SSE 이벤트 원문(`data: {"delta": …}`, 마지막 `{"done": true, …}`)과 `first_chunk_ms` 대 `total_ms`.
5. UI 두 모드의 `outputs/ui-turns.jsonl`: `first_ms`·`total_ms`·`error`.
6. `/chat/stream`은 첫 청크를 받은 뒤에야 200을 확정한다. 그 전 실패는 502·503·504, 그 뒤 실패는 `{"error": …}` 이벤트다.
7. `outputs/requests.jsonl`: 모든 요청의 `request_id`·상태·소요 시간. 응답 헤더 `X-Request-ID`와 같은 값이다.
8. Docker 두 번째 빌드에서 `CACHED`가 붙는 단계, `docker ps`의 `(healthy)`.

## GPU 없을 때 · 네트워크 없을 때

- **GPU 없음**: `.env`의 `OLLAMA_MODEL=qwen3:0.6b`, `OLLAMA_TIMEOUT=180`으로 바꾼다. 구조·상태 코드·스트리밍 관찰은 그대로 되고 시간만 길어진다. 첫 글자까지의 시간 차이는 CPU에서 오히려 더 크게 보인다.
- **네트워크 없음**: 모든 통신이 `localhost` 안에서 끝난다. 단, `uv sync`는 패키지 캐시가 필요하므로 수업 전에 한 번 실행해 둔다. Docker 경로는 베이스 이미지를 미리 내려받지 않았다면 건너뛰고 uv 경로(3교시 경로 B)로 진행한다. Gradio는 시작 시 외부 확인을 시도할 수 있으나 실패해도 동작한다.
- **Ollama가 없는 PC**: 앱 서버는 뜨고 `/health`가 `degraded`, `/chat`이 502가 된다. 이 상태 자체가 1교시 실패 경로 실습 자료가 된다. 정상 경로는 강의자 PC 시연으로 대체한다.
- **Docker 없음**: 3교시는 `reproduce_check.ps1`이 안내하는 uv 경로로 진행하고 Dockerfile은 읽기·레이어 순서 설명까지만 한다.

## 복사 후 변형

- 실패 재현은 Ollama를 끄는 대신 `$env:OLLAMA_HOST`·`$env:OLLAMA_MODEL`·`$env:OLLAMA_TIMEOUT`을 바꿔서 한다. 끝나면 `Remove-Item Env:OLLAMA_*`로 원복한다.
- 팀 프로젝트에 가져갈 때는 `app/schemas.py`의 필드와 `SYSTEM_PROMPT`, `ui/gradio_app.py`의 `ERROR_HINTS`부터 바꾼다. `get_client` 의존성 주입 지점은 13주차 테스트에서 가짜 클라이언트로 바꿔 끼우므로 유지한다.
- `outputs/`는 Git에 넣지 않는다. 제출 증거로 쓸 JSON은 별도 폴더(예: `evidence/week12/`)로 복사해 커밋한다.
