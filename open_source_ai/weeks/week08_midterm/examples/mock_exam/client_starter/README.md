# client_starter — 모의 실기 B 시작 코드

최소 Ollama `/api/chat` 클라이언트다. 이 폴더를 개인 실습 폴더에 복사한 뒤 `chat.py`의 `TODO(B-1)`을 채운다. 문제는 [`../tasks_B.md`](../tasks_B.md), 시간 배분은 [`lab.md`](../../../lab.md)에 있다.

## 실행

```powershell
Copy-Item .env.example .env
uv sync
uv run python check_env.py
uv run python chat.py --prompt "uv sync 가 하는 일을 한 문장으로 설명하라."
```

| 파일 | 역할 |
|---|---|
| `config.py` | 인자 > 환경변수(`.env`) > 기본값 순서로 설정을 정한다 |
| `chat.py` | 비스트리밍 `/api/chat` 호출, `outputs/chat-*.json` 기록. `TODO(B-1)` 세 곳 |
| `check_env.py` | `/api/tags`로 연결·모델 확인, `outputs/env-check.json` 기록. 3교시 시작 전 점검에도 쓴다 |

- `OLLAMA_MODEL` 기본값 `qwen3:4b`, GPU 없는 PC는 `.env`에서 `qwen3:0.6b`. 확정 값은 학기별 환경 기준표.
- `uv.lock`은 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
