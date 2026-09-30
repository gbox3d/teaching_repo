---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 12"
footer: "AI Service Deployment"
---

# Week 12
## AI Service Deployment

**3 × 60-minute blocks**<br>
Each block: 20 min explanation/demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Sessions

| Session | 20 min explanation/demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Separating the model server from the app server, schemas, `/health`, error responses | Set up the app server and verify error responses |
| Block 2 | Streaming (SSE) and UX, Gradio UI, CORS | Wire up a streaming chat UI |
| Block 3 | Externalizing config, Dockerfile, containers with Ollama, 3rd integrative assignment | Verify the Dockerfile and reproduction steps |

This week's question: **When you turn a model into a service others can use, what breaks and what slows down — and how do you handle it?**

---

<!-- _class: lead -->

# Block 1 · 20 min Explanation
## Separate the Model Server from the App Server

---

## 0–3 min · How Is a Script Different From a Service?

Through Week 11: it was me, on my PC, one request at a time, checking results with my own eyes.

What changes the moment it becomes a service:

- The caller is **not me** — bad input arrives
- Requests arrive **at the same time**
- Something must respond even when the model is **down or slow**
- You need to know **later** what happened

**Question:** If you put Week 10's `compare.py` straight onto the web, what breaks first?

---

## 3–6 min · The Two-Server Structure

```text
Browser/UI ──HTTP──▶ App server (FastAPI, :8000) ──HTTP──▶ Model server (Ollama, :11434)
  Gradio            validation, error handling, logging          weights, GPU, token generation
```

| Layer | Responsibility | Why it changes |
|---|---|---|
| Model server | loads the model, generates tokens | model swaps, GPU |
| App server | schema, system prompt, status codes, logging | features, policy |
| UI | input, display, cancel | user experience |

Swap the model, and the app server's **HTTP contract** stays the same.

---

## 6–9 min · Request/Response Schemas with pydantic

```python
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)

class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=40)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=2048)
```

- A value outside the allowed range is rejected with **422** before your code even runs
- The same schema becomes the basis for the `/docs` page and Week 13's tests

---

## 9–12 min · `/health` — Alive vs. Ready

```json
{"status": "degraded", "service": "osa-ai-service", "version": "0.1.0",
 "ollama": {"host": "http://localhost:11434", "reachable": false,
            "model": "qwen3:8b", "has_model": false,
            "detail": "... 에 연결할 수 없다. Ollama 가 실행 중인지 ..."}}
```

- If the app server responds at all, that's 200 — it's **alive**
- `status` must be `ok` for the model server to count as **ready**
- Docker's `HEALTHCHECK` and monitoring scripts watch this one endpoint

**Question:** What's the upside and downside of returning 503 instead of 200 when it's not ready?

---

## 12–15 min · Error Responses — A Different Code for Each Cause

| Situation | Exception | Code | What the user does |
|---|---|---:|---|
| Malformed request | pydantic | 422 | fix the input |
| Can't reach model server | `OllamaUnavailable` | 502 | check Ollama and the address |
| Model missing | `OllamaModelMissing` | 503 | `ollama list`, pull |
| Response timed out | `OllamaTimeout` | 504 | retry, lower `max_tokens` |

The 5xx body always has the same shape: `{"request_id", "error", "detail"}`. Only 422 uses FastAPI's default shape `{"detail": [...]}`.
**Don't collapse everything into 500.** Different codes call for different fixes.

---

## 15–17 min · Timeouts, Concurrency, and Logging

- There are **two** timeouts: connect 5s, generation `OLLAMA_TIMEOUT` (60s default)
- Retry only on connection failure — retrying mid-generation burns the GPU twice
- Ollama **queues** requests beyond its concurrency limit (`OLLAMA_NUM_PARALLEL`) — if 3 people ask at once, the last one waits
- Every request logs `request_id`, status, and elapsed time to `outputs/requests.jsonl`

```text
INFO 7c4d0ade POST /chat -> 200 1843ms
WARNING a875afe1 OllamaModelMissing: 모델 'x' 이(가) ... 에 없다
```

**Question:** If a user just says "my answer didn't come back earlier," which single value lets us find that request?

---

## 17–20 min · Handing Off to the Lab

[Block 1 lab — Set up the app server and verify error responses](lab.md#1교시-실습--앱-서버-세우기와-오류-응답-확인) · [Block 1 files](examples/period1/README.md)

Done when:

1. `/docs` opens, and `smoke_test.py`'s checks on `/health` and `/chat` both return 200
2. You reproduced 502, 503, and 504 **once each**, saved to `outputs/smoke-*.json`, and 422 shows up in `outputs/requests.jsonl`
3. You added `GET /models` and it returns a list of model names

30 min lab, then a 10 min break.

---

<!-- _class: lead -->

# Block 2 · 20 min Explanation
## Streaming and User Experience

---

## 0–3 min · Why Streaming?

```text
Non-streaming  |■■■■■■■■■■■■■■■■■■■■■■■■|  everything at once, after 12s
Streaming      |■|■|■|■|■|■|■|■|■|■|■|■|  first char at 0.4s … done at 12s
```

- Total time is the same. **Time to first character** is not
- Users judge "is it stuck?" by when the first character appears
- Being able to **cancel** mid-stream saves GPU time

**Question:** What kind of response is actually worse off with streaming? (Anything you need in full before it's usable, like JSON.)

---

## 3–7 min · The Path a Chunk Travels

```text
Ollama ──NDJSON, one line at a time──▶ App server ──SSE events──▶ UI
{"message":{"content":"uv"},"done":false}      data: {"delta": "uv"}
{"message":{"content":" lock"},"done":false}   data: {"delta": " lock"}
{"done":true,"eval_count":12,...}              data: {"done": true, ...}
```

- Ollama's `stream: true` sends line-delimited JSON (the same shape as Week 4's `stream.py`)
- The app server converts each line into an SSE event as soon as it arrives
- SSE = `text/event-stream`; one event is one `data:` line followed by a blank line

---

## 7–10 min · FastAPI's StreamingResponse

```python
stream = client.chat_stream(messages)
first = await anext(stream)        # a failure here means 502, 503, or 504

async def event_source():
    chunk = first
    while True:
        yield sse({"delta": chunk["message"]["content"]})
        if chunk.get("done"):
            return
        chunk = await anext(stream)

return StreamingResponse(event_source(), media_type="text/event-stream")
```

**The 200 is only committed after the first chunk arrives.** Once the body starts flowing, the status code can no longer change.

**Question:** If the model server dies on the tenth chunk, what should the client receive?

---

## 10–13 min · A Minimal Gradio ChatInterface

```python
def respond(message, history):
    text = ""
    with httpx.Client(base_url=api) as http, http.stream("POST", "/chat/stream", json=body) as resp:
        for line in resp.iter_lines():
            if line.startswith("data: "):
                event = json.loads(line[6:])
                if "delta" in event:
                    text += event["delta"]
                    yield text          # keep emitting the accumulated string

gr.ChatInterface(fn=respond).launch()   # history is a list of role/content dicts
```

With `yield`, Gradio automatically adds **partial rendering and a Stop button**. The UI doesn't know about the model — only about the HTTP contract.

---

## 13–15 min · States the UI Must Show

| State | What the user sees | Our code |
|---|---|---|
| Waiting | a loading indicator before the first char | Gradio default |
| Streaming | text growing + Stop | `yield` |
| Cancelled | text so far stays visible | generator closes |
| Error | code + detail + what to do next | `ERROR_HINTS` |
| Connection failed | "Can't reach the app server" | `httpx.ConnectError` |

**Question:** Is it OK to show the server's raw `detail` in an error message? What should you hide?

---

## 15–17 min · Static HTML + fetch, and CORS

```js
const resp = await fetch("http://localhost:8000/chat/stream", {
  method: "POST", headers: {"Content-Type": "application/json"},
  body: JSON.stringify({messages: [{role: "user", content: q}]})});
const reader = resp.body.getReader();   // read chunks directly
```

- This works even without Gradio — the browser calls the app server **directly**
- Then the page's origin and the API's origin differ → the browser blocks it → **CORS**
- The app server allows only the origins listed in `CORS_ORIGINS`. `*` is a temporary classroom-only value

---

## 17–20 min · Handing Off to the Lab

[Block 2 lab — Wire up a streaming chat UI](lab.md#2교시-실습--스트리밍-채팅-ui-연결) · [Block 2 files](examples/period2/README.md)

Done when:

1. You compared **time to first character** and **total time** for the same question in both modes
2. You recorded the UI wording for three situations: stopping a long answer, the app server going down, and the model server failing
3. `outputs/ui-turns.jsonl` has both normal turns and error turns

30 min lab, then a 10 min break.

---

<!-- _class: lead -->

# Block 3 · 20 min Explanation
## Package It to Run the Same Way on Another PC

---

## 0–3 min · Separate Code, Config, and Secrets

| Kind | Example | Where it lives |
|---|---|---|
| Code | `app/main.py` | Git |
| Config | `OLLAMA_MODEL`, `APP_PORT` | `.env.example` (Git) + `.env` (local) |
| Secrets | tokens | `.env` only, never Git |

- Override order: code defaults → `.env` → shell environment variables → command-line args
- Containers get `-e KEY=VALUE` instead of `.env` — so the code should **only read environment variables**

**Question:** If you already committed `.env` and then add it to `.gitignore`, is that fixed? (Week 3)

---

## 3–7 min · Dockerfile — Layers and Caching

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim
WORKDIR /app
COPY pyproject.toml uv.lock* ./              # 1) dependencies first
RUN uv sync --no-dev --no-install-project    #    → a cacheable layer
COPY . .                                     # 2) code comes later
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Each instruction = one layer. If the earlier layers match, Docker reuses the **cache**
- Change only the code, and `uv sync` doesn't rerun — order determines build time
- `.dockerignore` keeps `.env`, `.venv`, and `outputs` out of the image

---

## 7–10 min · From a Container to the Host's Ollama

```text
[Host] Ollama :11434  ◀── host.docker.internal:11434 ── [Container] App server :8000
```

```powershell
docker run --rm -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 osa-ai-service:dev
```

- `localhost` inside a container means **the container itself**
- Same name, different meaning: the app server's `OLLAMA_HOST` is the *address to reach*; Ollama's own `OLLAMA_HOST` is the *address to listen on* (it must be opened to `0.0.0.0` for the container to reach it)
- Keep the GPU and the model outside the container — the image holds only the app server, so it stays small

**Question:** If you set `OLLAMA_HOST=http://localhost:11434` inside the container, what does `/health` return?

---

## 10–13 min · README Reproduction Steps — Two Paths

```text
Path A (Docker)                       Path B (uv)
docker build -t osa-ai-service:dev .  Copy-Item .env.example .env
docker run ... -e OLLAMA_HOST=...     uv sync
                                       uv run uvicorn app.main:app --port 8000
Verify (same for both): uv run python smoke_test.py --skip-stream
```

- A first-time reader should finish by **copy-pasting alone**
- Put prerequisites (Ollama running, model pulled) **before** the steps
- Put what to check on failure (`/health`'s `detail`) **after** the steps

---

## 13–15 min · 3rd Integrative Assignment — Required Deliverables

Cumulative from weeks 9–12. In the team repository:

- **(a) 2 or more experiment logs** — `experiments/run-*.md`, data card, evaluation results, failure analysis
- **(b) AI service beta** — `/health`, `/chat`, one UI, error handling, `.env.example`, run instructions
- **(c) Evidence of individual contribution** — even as a team, per-person commits, Issues, PRs, Reviews

[Assignment brief](assignment_brief.md) · [Rubric](assignment_rubric.md)

---

## 15–17 min · 3rd Assignment — What's Assessed

| Item | Points |
|---|---:|
| Reproducibility of experiment logs | 20 |
| Validity of data and evaluation | 15 |
| Service functionality and error handling | 25 |
| Reproduction steps | 15 |
| Evidence of collaboration | 15 |
| Security and licensing | 10 |

100 points, relative weighting. **The actual percentage and deadline follow the university's official syllabus.**

**Question:** Between 10 screenshots and one `smoke-*.json` file, which is stronger evidence for a grader?

---

## 17–20 min · Handing Off to the Lab

[Block 3 lab — Verify the Dockerfile and reproduction steps](lab.md#3교시-실습--dockerfile과-재현-절차-검증) · [Block 3 files](examples/period3/README.md)

Done when:

1. `reproduce_check.ps1` confirms `.env` is not in Git and `.env.example` exists
2. `/health` returns `ok` in a **clean environment**, via either the Docker path or the uv path
3. A partner followed your team's README reproduction steps and recorded the result

30 min lab, then a 10 min break.

---

## This Week's Wrap-Up

```text
UI ──▶ App server (schema, status codes, logging) ──▶ Model server (Ollama)
        └ /health · /chat · /chat/stream                └ outside the container
Packaging: environment variables + .env.example + Dockerfile + two README paths
```

When it breaks, **speak in codes** (502/503/504); when it's slow, **show something first** (streaming); when you move it, **change only the config** (environment variables).

Next week (`week13_test_ci_security`): add pytest, CI, and security checks to this app server.
