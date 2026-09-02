# ai_service — FastAPI 앱 서버 + Ollama 모델 서버 + Gradio UI

12주차 예제 uv 프로젝트다. 자세한 실행 방법과 관찰 지점은 상위 [`../README.md`](../README.md)에 있다.

## 빠른 실행

```powershell
Copy-Item .env.example .env
uv sync
uv run uvicorn app.main:app --port 8000 --reload
```

다른 터미널에서:

```powershell
uv run python smoke_test.py            # /health, /chat, /chat/stream 점검 → outputs/smoke-*.json
uv run python ui/gradio_app.py         # http://localhost:7860 채팅 UI
```

## 구성

| 경로 | 역할 |
|---|---|
| `app/main.py` | `/health`, `/chat`, `/chat/stream`, 오류 응답(502·503·504), 요청 기록 |
| `app/ollama_client.py` | Ollama `/api/tags`·`/api/chat` 호출, 실패를 예외 3종으로 구분 |
| `app/schemas.py` | pydantic 요청·응답 스키마 |
| `ui/gradio_app.py` | `/chat/stream`(또는 `/chat`)에 붙는 채팅 UI |
| `smoke_test.py` | 세 엔드포인트를 호출해 상태 코드·시간을 JSON 으로 기록 |
| `Dockerfile`, `.dockerignore` | 앱 서버만 담는 이미지 |
| `reproduce_check.ps1` | 필수 파일·`.env` 추적 여부·실행 경로 점검 |

- 모델 ID·주소는 환경변수(`.env.example` 참고)로 읽는다. 기본값은 교재 검증용이며 실제 값은 환경 기준표에서 확정한다.
- `uv.lock` 은 환경 기준표 확정 후 기준 PC에서 `uv lock` 으로 생성해 커밋한다.
