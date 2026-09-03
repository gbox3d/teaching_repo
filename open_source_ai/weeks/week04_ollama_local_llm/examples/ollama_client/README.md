# ollama_client — 4주차 예제 uv 프로젝트

Ollama `/api/chat`을 비스트리밍(`chat.py`)과 스트리밍(`stream.py`)으로 호출하는 최소 클라이언트다. 설명과 관찰 지점은 상위 [`../README.md`](../README.md)에 있다.

## 실행

```powershell
Copy-Item .env.example .env      # 값은 그대로 두어도 된다
uv sync                          # 의존성 설치(수업 전 한 번)
uv run python config.py          # 설정 우선순위 확인
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘."
uv run python stream.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."
ollama create osa-helper -f Modelfile
uv run python chat.py --model osa-helper --prompt "uv가 무엇인지 두 문장으로 설명해 줘."
```

결과는 `outputs/chat-*.json`, `outputs/stream-*.json`에 쌓인다(`.gitignore` 대상).

## 파일

| 파일 | 역할 |
|---|---|
| `config.py` | 기본값 < `.env`·환경변수 < 인자 순서의 설정 로더 |
| `ollama_api.py` | 오류 문장, 메타 계산(tokens/s), JSON 저장 도우미 |
| `chat.py` | `/api/chat` 비스트리밍. `stream:false`, `think:false`, `options` 명시 |
| `stream.py` | `/api/chat` 스트리밍. NDJSON 조각 출력, 마지막 줄 메타 기록 |
| `Modelfile` | 수업 도우미 커스텀 모델 정의 |
| `.env.example` | 환경변수 예시. `.env`로 복사해서 쓴다 |

## 기본값

`OLLAMA_HOST`(`http://localhost:11434`)·`OLLAMA_MODEL`(`qwen3:8b` — Q4_K_M, 내려받는 크기 약 5.2 GB. CPU 대체 `qwen3:0.6b`)은 교재 검증용 기본값이다. 모델 ID·양자화·용량은 학기별 환경 기준표에서 확정한다. `uv.lock`은 환경 기준표 확정 후 기준 PC에서 `uv lock`을 생성해 커밋한다.
