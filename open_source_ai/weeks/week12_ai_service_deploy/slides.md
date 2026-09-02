---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 12주차"
footer: "AI 서비스화와 배포"
---

# 12주차
## AI 서비스화와 배포

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 모델 서버와 앱 서버 분리, 스키마, `/health`, 오류 응답 | 앱 서버 세우기와 오류 응답 확인 |
| 2교시 | 스트리밍(SSE)과 사용자 경험, Gradio UI, CORS | 스트리밍 채팅 UI 연결 |
| 3교시 | 설정 외부화, Dockerfile, 컨테이너와 Ollama, 3차 종합과제 | Dockerfile과 재현 절차 검증 |

이번 주 질문: **모델을 다른 사람이 쓸 수 있는 서비스로 만들 때 무엇이 끊기고 느려지며, 그것을 어떻게 다루는가?**

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 모델 서버와 앱 서버를 분리한다

---

## 0–3분 · 스크립트와 서비스는 무엇이 다른가

11주차까지: 내가, 내 PC에서, 한 번에 하나씩, 결과를 눈으로 확인했다.

서비스가 되는 순간 달라지는 것:

- 부르는 사람이 **내가 아니다** — 잘못된 입력이 들어온다
- 여러 요청이 **동시에** 온다
- 모델이 꺼져 있거나 **느릴 때도** 무언가 답해야 한다
- 무슨 일이 있었는지 **나중에** 알아야 한다

**질문:** 10주차 `compare.py`를 그대로 웹에 올리면 첫 번째로 무엇이 깨질까?

---

## 3–6분 · 두 서버 구조

```text
브라우저·UI ──HTTP──▶ 앱 서버(FastAPI, :8000) ──HTTP──▶ 모델 서버(Ollama, :11434)
  Gradio             검증·오류 처리·기록                   가중치·GPU·토큰 생성
```

| 층 | 책임 | 바뀌는 이유 |
|---|---|---|
| 모델 서버 | 모델 적재, 토큰 생성 | 모델 교체, GPU |
| 앱 서버 | 스키마, system 프롬프트, 상태 코드, 기록 | 기능·정책 |
| UI | 입력·표시·취소 | 사용자 경험 |

모델을 바꿔도 앱 서버의 **HTTP 계약**은 그대로다.

---

## 6–9분 · 요청·응답 스키마 — pydantic

```python
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)

class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=40)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=2048)
```

- 범위 밖 값은 내 코드가 돌기 전에 **422**로 거절된다
- 같은 스키마가 `/docs` 문서와 13주차 테스트의 기준이 된다

---

## 9–12분 · `/health` — 살아 있는가, 준비되었는가

```json
{"status": "degraded", "service": "osa-ai-service", "version": "0.1.0",
 "ollama": {"host": "http://localhost:11434", "reachable": false,
            "model": "qwen3:4b", "has_model": false,
            "detail": "... 에 연결할 수 없다. Ollama 가 실행 중인지 ..."}}
```

- 앱 서버가 응답하면 200 — **살아 있다**
- `status`가 `ok`여야 모델 서버까지 **준비되었다**
- Docker `HEALTHCHECK`와 점검 스크립트가 이 주소 하나를 본다

**질문:** 준비가 안 됐을 때 200 대신 503을 돌려주면 무엇이 좋고 무엇이 나쁜가?

---

## 12–15분 · 오류 응답 — 원인마다 다른 코드

| 상황 | 예외 | 코드 | 사용자가 할 일 |
|---|---|---:|---|
| 요청 형식 오류 | pydantic | 422 | 입력을 고친다 |
| 모델 서버 연결 실패 | `OllamaUnavailable` | 502 | Ollama·주소 확인 |
| 모델 없음 | `OllamaModelMissing` | 503 | `ollama list`, pull |
| 응답 시간 초과 | `OllamaTimeout` | 504 | 재시도, `max_tokens` 축소 |

본문은 항상 같은 모양 `{"request_id", "error", "detail"}`.
**500 하나로 뭉개지 않는다.** 코드가 다르면 조치가 다르다.

---

## 15–17분 · 타임아웃·동시 요청·기록

- 타임아웃은 **두 개**: 연결 5초, 생성 `OLLAMA_TIMEOUT`(기본 60초)
- 재시도는 연결 실패에만 — 생성 중 재시도는 GPU를 두 번 태운다
- Ollama는 동시 처리 수(`OLLAMA_NUM_PARALLEL`)를 넘는 요청을 **줄 세운다** — 3명이 동시에 물으면 마지막은 기다린다
- 모든 요청에 `request_id`·상태·소요 시간 → `outputs/requests.jsonl`

```text
INFO 7c4d0ade POST /chat -> 200 1843ms
WARNING a875afe1 OllamaModelMissing: 모델 'x' 이(가) ... 에 없다
```

**질문:** 사용자가 "아까 답이 안 왔다"고만 말하면, 우리는 어떤 값 하나로 그 요청을 찾아낼 수 있는가?

---

## 17–20분 · 실습 인계

[1교시 실습 — 앱 서버 세우기와 오류 응답 확인](lab.md#1교시-실습--앱-서버-세우기와-오류-응답-확인)

완료 조건:

1. `/docs`가 열리고 `smoke_test.py`의 `/health`·`/chat`이 200이다
2. 502·503·504·422를 **각각 한 번씩** 재현해 `outputs/smoke-*.json`에 남겼다
3. `GET /models`를 추가해 모델 이름 목록이 나온다

실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 스트리밍과 사용자 경험

---

## 0–3분 · 왜 스트리밍인가

```text
비스트리밍  |■■■■■■■■■■■■■■■■■■■■■■■■|  12초 뒤 전체가 한 번에
스트리밍    |■|■|■|■|■|■|■|■|■|■|■|■|  0.4초 뒤 첫 글자 … 12초 뒤 완성
```

- 전체 시간은 같다. **첫 글자까지의 시간**이 다르다
- 사용자는 "멈췄나?"를 첫 글자로 판단한다
- 중간에 **취소**할 수 있어야 GPU 시간을 아낀다

**질문:** 스트리밍이 오히려 불리한 응답은 무엇일까? (JSON처럼 다 받아야 쓸 수 있는 것)

---

## 3–7분 · 청크가 지나가는 길

```text
Ollama ──NDJSON 한 줄씩──▶ 앱 서버 ──SSE 이벤트──▶ UI
{"message":{"content":"uv"},"done":false}      data: {"delta": "uv"}
{"message":{"content":" lock"},"done":false}   data: {"delta": " lock"}
{"done":true,"eval_count":12,...}              data: {"done": true, ...}
```

- Ollama `stream: true` → 줄 단위 JSON(4주차 `stream.py`에서 본 것)
- 앱 서버는 줄을 받는 즉시 SSE 이벤트로 바꿔 흘려보낸다
- SSE = `text/event-stream`, 이벤트 하나는 `data:` 한 줄 + 빈 줄

---

## 7–10분 · FastAPI StreamingResponse

```python
stream = client.chat_stream(messages)
first = await anext(stream)        # 여기서 실패하면 502·503·504

async def event_source():
    chunk = first
    while True:
        yield sse({"delta": chunk["message"]["content"]})
        if chunk.get("done"):
            return
        chunk = await anext(stream)

return StreamingResponse(event_source(), media_type="text/event-stream")
```

**첫 청크를 받은 뒤에야 200을 확정한다.** 본문이 흐르기 시작하면 상태 코드를 바꿀 수 없다.

**질문:** 열 번째 청크에서 모델 서버가 죽으면 클라이언트는 무엇을 받아야 하는가?

---

## 10–13분 · Gradio ChatInterface 최소 코드

```python
def respond(message, history):
    text = ""
    with httpx.Client(base_url=api) as http, http.stream("POST", "/chat/stream", json=body) as resp:
        for line in resp.iter_lines():
            if line.startswith("data: "):
                event = json.loads(line[6:])
                if "delta" in event:
                    text += event["delta"]
                    yield text          # 누적 문자열을 계속 내보낸다

gr.ChatInterface(fn=respond, type="messages").launch()
```

`yield`가 있으면 Gradio가 **부분 표시와 Stop 버튼**을 알아서 붙인다. UI는 모델을 모르고 HTTP 계약만 안다.

---

## 13–15분 · UI가 보여 줘야 할 상태

| 상태 | 사용자가 보는 것 | 우리 코드 |
|---|---|---|
| 대기 | 첫 글자 전 로딩 표시 | Gradio 기본 |
| 진행 | 글자가 늘어남 + Stop | `yield` |
| 취소 | 지금까지 텍스트 유지 | 생성기 닫힘 |
| 오류 | 코드 + detail + 다음 행동 | `ERROR_HINTS` |
| 연결 실패 | "앱 서버에 연결할 수 없다" | `httpx.ConnectError` |

**질문:** 오류 문구에 서버의 `detail`을 그대로 보여 줘도 되는가? 무엇을 가려야 하는가?

---

## 15–17분 · 정적 HTML + fetch, 그리고 CORS

```js
const resp = await fetch("http://localhost:8000/chat/stream", {
  method: "POST", headers: {"Content-Type": "application/json"},
  body: JSON.stringify({messages: [{role: "user", content: q}]})});
const reader = resp.body.getReader();   // 청크를 직접 읽는다
```

- Gradio 없이도 된다. 브라우저가 앱 서버에 **직접** 요청한다
- 그러면 페이지의 출처(origin)와 API의 출처가 다르다 → 브라우저가 막는다 → **CORS**
- 앱 서버가 `CORS_ORIGINS`에 적은 출처만 허용한다. `*`는 수업용 임시값이다

---

## 17–20분 · 실습 인계

[2교시 실습 — 스트리밍 채팅 UI 연결](lab.md#2교시-실습--스트리밍-채팅-ui-연결)

완료 조건:

1. 같은 질문으로 **첫 글자까지 시간**과 **전체 시간**을 두 모드에서 비교했다
2. 긴 답 중 Stop, 앱 서버 중단, 모델 서버 실패 — 세 상황의 UI 문구를 기록했다
3. `outputs/ui-turns.jsonl`에 정상 턴과 오류 턴이 모두 있다

실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 다른 PC에서 그대로 실행되게 포장한다

---

## 0–3분 · 코드·설정·비밀을 분리한다

| 종류 | 예 | 어디에 두는가 |
|---|---|---|
| 코드 | `app/main.py` | Git |
| 설정 | `OLLAMA_MODEL`, `APP_PORT` | `.env.example`(Git) + `.env`(로컬) |
| 비밀 | 토큰 | `.env`에만, Git 금지 |

- 덮어쓰는 순서: 코드 기본값 → `.env` → 셸 환경변수 → 명령 인자
- 컨테이너에서는 `.env` 대신 `-e KEY=VALUE`로 넣는다 — 그래서 코드는 **환경변수만** 읽어야 한다

**질문:** `.env`를 이미 커밋한 뒤 `.gitignore`에 넣으면 해결되는가? (3주차)

---

## 3–7분 · Dockerfile — 레이어와 캐시

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock* ./              # 1) 의존성만 먼저
RUN uv sync --no-dev --no-install-project    #    → 캐시되는 레이어
COPY . .                                     # 2) 코드는 나중에
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- 명령 한 줄 = 레이어 한 장. 앞 레이어가 같으면 **캐시**를 쓴다
- 코드만 바뀌면 `uv sync`는 다시 돌지 않는다 — 순서가 곧 빌드 시간
- `.dockerignore`가 `.env`·`.venv`·`outputs`를 이미지 밖에 둔다

---

## 7–10분 · 컨테이너에서 호스트의 Ollama로

```text
[호스트] Ollama :11434  ◀── host.docker.internal:11434 ── [컨테이너] 앱 서버 :8000
```

```powershell
docker run --rm -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 osa-ai-service:dev
```

- 컨테이너 안의 `localhost`는 **컨테이너 자신**이다
- 같은 이름, 다른 뜻: 앱 서버의 `OLLAMA_HOST`는 *찾아갈 주소*, Ollama 서버의 `OLLAMA_HOST`는 *들을 주소*(`0.0.0.0`으로 열어야 컨테이너가 들어온다)
- GPU와 모델은 컨테이너 밖에 둔다 — 이미지는 앱 서버만 담아 작게 유지한다

**질문:** 컨테이너 안에서 `OLLAMA_HOST=http://localhost:11434`로 두면 `/health`는 무엇을 돌려줄까?

---

## 10–13분 · README 재현 절차 — 두 경로

```text
경로 A (Docker)                       경로 B (uv)
docker build -t osa-ai-service:dev .  Copy-Item .env.example .env
docker run ... -e OLLAMA_HOST=...     uv sync
                                      uv run uvicorn app.main:app --port 8000
확인(둘 다 같다): uv run python smoke_test.py --skip-stream
```

- 처음 보는 사람이 **복사해서 붙여 넣기만으로** 끝나야 한다
- 전제(Ollama 실행, 모델 pull)를 절차 **앞에** 적는다
- 실패했을 때 볼 것(`/health`의 `detail`)을 절차 **뒤에** 적는다

---

## 13–15분 · 3차 종합과제 — 필수 산출물

9~12주 누적. 팀 저장소에:

- **(a) 실험 기록 2회 이상** — `experiments/run-*.md`, 데이터 카드, 평가 결과, 실패 분석
- **(b) AI 서비스 베타** — `/health`·`/chat`, UI 1종, 오류 처리, `.env.example`, 실행 절차
- **(c) 개인 기여 증거** — 팀이어도 개인별 commit·Issue·PR·Review

[안내서](assignment_brief.md) · [루브릭](assignment_rubric.md)

---

## 15–17분 · 3차 과제 — 무엇을 보는가

| 항목 | 배점 |
|---|---:|
| 실험 기록의 재현성 | 20 |
| 데이터·평가의 타당성 | 15 |
| 서비스 기능·오류 처리 | 25 |
| 재현 절차 | 15 |
| 협업 근거 | 15 |
| 보안·라이선스 | 10 |

100점 상대 배점이다. **실제 비율·마감은 학교 운영 문서가 정한다.**

**질문:** 캡처 10장과 `smoke-*.json` 1개 중 채점자에게 더 강한 증거는 무엇인가?

---

## 17–20분 · 실습 인계

[3교시 실습 — Dockerfile과 재현 절차 검증](lab.md#3교시-실습--dockerfile과-재현-절차-검증)

완료 조건:

1. `.env`가 Git에 없고 `.env.example`이 있음을 `reproduce_check.ps1`로 확인했다
2. Docker 경로 또는 uv 경로 중 하나로 **깨끗한 환경**에서 `/health`가 `ok`다
3. 팀 README 재현 절차를 짝이 따라 해 결과를 기록했다

실습 30분 뒤 휴식 10분.

---

## 이번 주 정리

```text
UI ──▶ 앱 서버(스키마·상태 코드·기록) ──▶ 모델 서버(Ollama)
        └ /health · /chat · /chat/stream          └ 컨테이너 밖
포장: 환경변수 + .env.example + Dockerfile + README 두 경로
```

끊기면 **코드로 말하고**(502·503·504), 느리면 **먼저 보여 주고**(스트리밍), 옮기면 **설정만 바꾼다**(환경변수).

다음 주(`week13_test_ci_security`): 이 앱 서버에 pytest·CI·보안 점검을 붙인다.
