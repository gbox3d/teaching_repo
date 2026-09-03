# 12주차 따라하기 — 앱 서버, 스트리밍 UI, 포장과 재현

이 문서는 12주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 각 교시의 20분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- Git, uv, Ollama가 설치되어 있고 기본 모델이 캐시되어 있다. (`uv --version`, `ollama list`로 확인)
- [`examples/ai_service/`](examples/ai_service/) 폴더를 개인 실습 폴더에 **복사**해서 사용한다. 수업 자료 원본은 수정하지 않는다.
- 수업 전에 복사본에서 `uv sync`를 한 번 실행해 패키지 캐시를 채워 두었다. 1교시 단계 1의 `uv sync`는 캐시에서 몇 초 안에 끝나야 하며, 수 분이 걸리면 캐시가 없는 것이므로 강의자에게 알린다.
- 터미널은 두 개를 쓴다. 터미널 A는 서버(앱 서버 또는 UI), 터미널 B는 점검 명령용이다. 둘 다 복사한 폴더 안에서 실행한다.
- Docker Desktop은 3교시 경로 A에만 필요하다. 없으면 경로 B(uv)로 진행한다.

---

## 1교시 — 앱 서버 세우기와 오류 응답 확인

### 단계 1. 예제 복사와 의존성 설치

**할 일** — `$src`에는 교재 저장소의 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week12_ai_service_deploy\examples"
New-Item -ItemType Directory -Force C:\classwork\week12 | Out-Null
Copy-Item -Recurse "$src\ai_service" C:\classwork\week12\ai_service
Set-Location C:\classwork\week12\ai_service
Copy-Item .env.example .env
uv sync
ollama list
```

**예상 결과** — `.venv/`가 생기고 `uv sync`가 오류 없이 끝난다. `ollama list`에 `.env`의 `OLLAMA_MODEL`과 같은 이름(교재 기본값 `qwen3:8b`)이 보인다.

**확인** — [ ] `.env`를 열어 `OLLAMA_HOST`·`OLLAMA_MODEL`·`OLLAMA_TIMEOUT` 세 값을 읽었다. 모델 이름이 다르면 `.env`를 고쳤다.

### 단계 2. 앱 서버 실행과 `/docs`

**할 일**

1. 터미널 A에서 실행한다.

```powershell
uv run uvicorn app.main:app --port 8000 --reload
```

2. 브라우저에서 `http://localhost:8000/docs`를 연다.

**예상 결과** — 터미널 A에 `모델 서버 http://localhost:11434, 기본 모델 qwen3:8b`와 `Uvicorn running on http://127.0.0.1:8000`이 보이고 명령이 끝나지 않은 채 대기한다. `/docs`에 `GET /health`, `POST /chat`, `POST /chat/stream` 세 항목이 있다.

**확인** — [ ] `/docs`에서 `POST /chat`을 펼쳐 요청 예시(`messages`, `temperature`, `max_tokens`)와 응답 코드 목록(200·422·502·503·504)을 봤다.

### 단계 3. 정상 경로 — `/health`와 `/chat`

**할 일** — 터미널 B에서 실행한다.

```powershell
uv run python smoke_test.py --skip-stream
```

**예상 결과** — `[health] 200 status=ok`, `[chat] 200 …ms '…'`가 출력되고 `기록: outputs\smoke-….json`이 보인다. 터미널 A에는 `GET /health -> 200`, `POST /chat -> 200 …ms` 로그가 남는다. JSON 안의 `chat.eval_count`와 `chat.eval_duration_ms`가 숫자다.

**확인** — [ ] `eval_count ÷ (eval_duration_ms ÷ 1000)`으로 초당 토큰 수를 계산했다. [ ] `outputs/requests.jsonl`이 생겼고 한 줄에 `request_id`·`path`·`status`·`elapsed_ms`가 있다.

### 단계 4. 실패 경로 — 없는 포트(502)

**할 일**

1. 예측을 적는다: "모델 서버 주소가 틀리면 `/health`와 `/chat`은 각각 무엇을 돌려줄까?"
2. 터미널 A에서 `Ctrl+C` 후 환경변수를 바꿔 다시 띄운다.

```powershell
$env:OLLAMA_HOST = "http://localhost:11435"
uv run uvicorn app.main:app --port 8000
```

3. 터미널 B에서 `uv run python smoke_test.py --skip-stream`을 다시 실행한다.

**예상 결과** — `/health`는 200이지만 `status=degraded`이고 `ollama.reachable`이 `false`, `detail`에 "연결할 수 없다"가 있다. `/chat`은 **502**이며 본문은 `{"request_id", "error": "OllamaUnavailable", "detail": …}`다. 터미널 A에 `WARNING … OllamaUnavailable` 한 줄이 남는다.

**확인** — [ ] 앱 서버는 살아 있는데(200) 준비는 안 된(degraded) 상태를 구분해 말할 수 있다. [ ] `Remove-Item Env:OLLAMA_HOST`로 원복했다.

### 단계 5. 실패 경로 — 없는 모델(503), 짧은 타임아웃(504), 잘못된 요청(422)

**할 일** — 각 항목마다 터미널 A를 `Ctrl+C` → 환경변수 설정 → 재실행하고, 터미널 B에서 `smoke_test.py --skip-stream`을 돌린다.

1. `$env:OLLAMA_MODEL = "no-such-model"` → 실행 → 기록 → `Remove-Item Env:OLLAMA_MODEL`
2. `$env:OLLAMA_TIMEOUT = "0.5"` → 실행 → 기록 → `Remove-Item Env:OLLAMA_TIMEOUT`
3. 정상 재실행 후 `/docs`의 `POST /chat`에서 `temperature`를 `5`로 보낸다.

**예상 결과** — 1은 `/health`가 `has_model: false`·`degraded`, `/chat`이 **503** `OllamaModelMissing`. 2는 `/health`가 `ok`(목록 조회는 빠르다)인데 `/chat`이 **504** `OllamaTimeout`. 3은 **422**이며 본문의 `detail`에 `temperature`와 `less than or equal to 2`가 들어 있다.

**확인** — [ ] 502·503·504 세 상황의 `smoke-*.json`이 `outputs/`에 있고, 422는 `outputs/requests.jsonl`에 한 줄로 남았다(`smoke_test.py`는 늘 올바른 본문을 보내므로 422를 만들지 않는다). [ ] `Get-ChildItem Env:OLLAMA_*`가 비어 있다.

### 단계 6. `GET /models` 추가

**할 일**

1. `app/main.py`의 `health` 함수 아래에 `GET /models` 라우트를 추가한다. `client.list_models()` 결과를 `{"models": [...]}`로 돌려준다. 시그니처는 `health`와 같은 방식으로 `client: OllamaClient = Depends(get_client)`를 받는다.
2. `--reload`가 켜져 있으면 저장 즉시 재시작된다. `/docs`를 새로고침해 `GET /models`를 실행한다.
3. 단계 4처럼 없는 포트로 재실행해 `/models`를 다시 부른다.

**예상 결과** — 정상일 때 `ollama list`와 같은 이름 목록이 나온다. 없는 포트일 때는 `try` 없이도 **502**와 `OllamaUnavailable` 본문이 나온다 — `@app.exception_handler(OllamaError)`가 모든 라우트에 적용되기 때문이다.

**확인** — [ ] 변경을 commit했다(`Add GET /models endpoint`). [ ] 환경변수를 원복하고 앱 서버를 정상 상태로 켜 두었다(2교시에서 이어 쓴다).

---

## 2교시 — 스트리밍 채팅 UI 연결

이어받는 것: 1교시 폴더, 정상 실행 중인 앱 서버(터미널 A). 환경변수는 비어 있어야 한다.

### 단계 1. SSE 원문 관찰

**할 일** — 터미널 B에서 실행한다.

```powershell
uv run python smoke_test.py --show-events --max-tokens 300
```

**예상 결과** — `[chat] 200 …ms` 다음에 `data: {"delta": "…"}` 형태의 줄이 5개 출력되고, `[stream] 200 first=…ms total=…ms events=…`가 보인다. `first`는 `[chat]`의 시간보다 훨씬 작고 `total`은 비슷하다. JSON의 `stream.reply_chars`가 0보다 크다.

**확인** — [ ] 이벤트 한 건이 `data:` 한 줄과 빈 줄로 이루어진 것을 원문에서 봤다. [ ] 마지막 이벤트가 `{"done": true, "eval_count": …}`임을 JSON에서 확인했다.

### 단계 2. 비스트리밍 UI

**할 일**

1. 터미널 B에서 UI를 띄운다(앱 서버는 터미널 A에 그대로).

```powershell
uv run python ui/gradio_app.py --no-stream
```

2. `http://localhost:7860`을 열고 긴 질문 "uv, Git, Ollama를 각각 세 문장으로 설명해 줘"를 보낸다.

**예상 결과** — 상단 설명줄에 `모드 once`가 보인다. 보낸 뒤 몇 초 동안 답 영역이 비어 있다가 전체 답이 한 번에 나타난다. `outputs/ui-turns.jsonl`에 `"mode": "once"` 줄이 생기고 `first_ms`와 `total_ms`가 거의 같다.

**확인** — [ ] 기다리는 동안 화면에 무엇이 보였는지 한 문장으로 적었다.

### 단계 3. 스트리밍 UI와 Stop

**할 일**

1. 터미널 B에서 `Ctrl+C` 후 스트리밍 모드로 띄운다.

```powershell
uv run python ui/gradio_app.py
```

2. 같은 질문을 보낸다. 3. 한 번 더 보내고 답이 흐르는 도중 `Stop`을 누른다.

**예상 결과** — `모드 stream`. 첫 글자가 1초 안팎에 나타나고 글자가 계속 늘어나며 입력창 자리에 `Stop`이 보인다. Stop을 누르면 지금까지의 텍스트가 남고 다음 질문을 보낼 수 있다. `ui-turns.jsonl`의 `"mode": "stream"` 줄에서 `first_ms`가 `total_ms`보다 뚜렷이 작다.

**확인** — [ ] 두 모드의 `first_ms`·`total_ms`를 비교표에 옮겼다. [ ] Stop 뒤 터미널 A의 로그에 어떤 줄이 남는지 적었다.

### 단계 4. 오류 상태 — 앱 서버 중단과 모델 서버 실패

**할 일**

1. 터미널 A의 앱 서버를 `Ctrl+C`로 끈다. UI에서 질문한다.
2. 터미널 A를 `$env:OLLAMA_HOST = "http://localhost:11435"`로 재실행한다. UI에서 질문한다.
3. `Remove-Item Env:OLLAMA_HOST` 후 정상 재실행한다.

**예상 결과** — 1은 `[연결 실패] 앱 서버 http://localhost:8000 에 연결할 수 없다 …`. 2는 `[오류 502] … 연결할 수 없다 …` 다음 줄에 "모델 서버(Ollama)에 연결하지 못했다 …" 힌트. 두 문구가 서로 다른 원인을 가리킨다. `ui-turns.jsonl`에 `"error": true` 줄이 2개 생긴다.

**확인** — [ ] 두 문구를 그대로 기록했다. [ ] `ERROR_HINTS`의 502·504 문구를 팀 사용자용으로 고쳤다(실제 연락처·이름 없음).

### 단계 5. 기록 정리

**할 일** — `outputs/ui-turns.jsonl`을 열어 `once`·`stream`·오류 턴을 표로 옮기고 "전체 시간이 같은데 스트리밍이 낫게 느껴지는 이유"를 한 문장으로 적는다.

**예상 결과** — 표에 최소 4행(once 1, stream 1, error 2)이 있다.

**확인** — [ ] `lab.md` 2교시 완료 조건 3개를 모두 체크했다.

---

## 3교시 — Dockerfile과 재현 절차 검증

이어받는 것: 1교시 폴더. 앱 서버와 UI를 모두 끈다(8000·7860 포트를 비운다). 폴더가 Git 저장소가 아니면 `git init` 후 첫 commit을 만든다.

### 단계 1. 설정 외부화 점검

**할 일**

```powershell
.\reproduce_check.ps1
git add -A
git status --short
```

**예상 결과** — 스크립트가 필수 파일 9개를 `ok`로 표시하고 `.env 는 추적되지 않는다`, 실행 경로(docker 또는 uv)를 안내한다. `git status --short`에 `.env`와 `outputs/`가 **없다**.

**확인** — [ ] `.env`가 목록에 나타났다면 `.gitignore`를 확인하고 `git restore --staged .env`로 내렸다.

### 단계 2. Dockerfile 읽기

**할 일** — `Dockerfile`을 열고 각 줄이 무엇을 만드는지 순서대로 말한다. 예측을 적는다: "`app/main.py`에 주석 한 줄을 추가하고 다시 빌드하면 어느 단계부터 다시 실행될까?"

**예상 결과** — `COPY pyproject.toml uv.lock* ./` → `RUN uv sync` → `COPY . .` 순서다. 코드만 바뀌면 `uv sync` 레이어까지는 캐시를 쓰고 `COPY . .`부터 다시 만든다. `.dockerignore` 때문에 `.env`·`.venv`·`outputs`는 이미지에 들어가지 않는다.

**확인** — [ ] 레이어 순서의 이유를 두 문장으로 적었다.

### 단계 3. 경로 A — 빌드와 실행 (Docker가 있을 때)

**할 일**

```powershell
docker build -t osa-ai-service:dev .
docker run --rm -p 8001:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 -e OLLAMA_MODEL=qwen3:8b osa-ai-service:dev
```

다른 터미널에서:

```powershell
uv run python smoke_test.py --api http://localhost:8001 --skip-stream
```

**예상 결과** — 첫 빌드는 베이스 이미지와 의존성 설치로 시간이 걸리고, 주석 한 줄을 추가한 두 번째 빌드는 `uv sync` 단계에 `CACHED`가 붙는다. 컨테이너 로그에 `모델 서버 http://host.docker.internal:11434`가 보인다. `/health`가 `ok`면 컨테이너에서 호스트의 Ollama에 닿은 것이다. `degraded`이고 `detail`이 연결 실패면 호스트의 Ollama가 `127.0.0.1`에서만 듣고 있는 것이다 — Ollama 서버 쪽 `OLLAMA_HOST=0.0.0.0` 설정이 필요하며, 실습실에서 바꿀 수 없으면 그 사실을 기록한다.

**확인** — [ ] `CACHED`가 붙은 단계 이름을 적었다. [ ] `docker ps`의 `STATUS` 열에 잠시 뒤 `(healthy)`가 나타나는지 봤다. [ ] 끝나면 `Ctrl+C`로 컨테이너를 내렸다.

### 단계 4. 경로 B — 깨끗한 폴더에서 uv로 (Docker가 없을 때, 또는 추가로)

**할 일**

```powershell
git clone C:\classwork\week12\ai_service C:\classwork\week12\clean
Set-Location C:\classwork\week12\clean
Copy-Item .env.example .env
uv sync
uv run uvicorn app.main:app --port 8001
```

다른 터미널에서 `uv run python smoke_test.py --api http://localhost:8001 --skip-stream`을 실행한다.

**예상 결과** — clone된 폴더에 `.env`·`.venv`·`outputs`가 없다(추적되지 않았으므로). `.env.example`을 복사하고 `uv sync`만 하면 1교시와 같은 결과(`/health` ok, `/chat` 200)가 나온다.

**확인** — [ ] `.env` 없이 실행해도 코드 기본값으로 뜨는지 한 번 확인했다(설정 계층의 맨 아래).

### 단계 5. README 실행 절과 짝 검증, 3차 과제 점검

**할 일**

1. 팀 저장소 README에 「실행」 절을 쓴다: 전제 2줄 → 경로 A → 경로 B → 확인 명령 → 실패 시 볼 것.
2. 짝과 저장소를 바꿔 README만 보고 5분 안에 `/health`가 `ok`가 되는지 시도한다. 막힌 줄과 이유를 받아 README에 반영한다.
3. [`assignment_brief.md`](assignment_brief.md)의 「제출 전 검사」를 `assignment3_checklist.md`로 옮겨 O/X와 근거를 적는다.

**예상 결과** — 짝의 기록에 "막힌 줄"이 0~2개 있고 각각 README에 반영된 commit이 있다. 점검표의 X 항목마다 담당자와 Issue 번호가 있다.

**확인** — [ ] `lab.md` 3교시 완료 조건과 「제출 체크」를 모두 확인했다.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| `uv run uvicorn`이 `No module named 'app'` | 1교시 단계 2 (현재 폴더가 `pyproject.toml`이 있는 곳인지) |
| `/health`가 `degraded`인데 원인을 모르겠다 | 1교시 단계 4 (`detail` 읽기, `Get-ChildItem Env:OLLAMA_*`로 남은 변수 확인) |
| 환경변수를 바꿨는데 결과가 같다 | 1교시 단계 4 (`Ctrl+C` 후 재실행, `--reload`는 파일만 감지) |
| 504 대신 200이 나온다 | 1교시 단계 5 (`--max-tokens 400` 또는 `OLLAMA_TIMEOUT=0.1`) |
| UI가 `[연결 실패]`를 보인다 | 2교시 단계 1 (`smoke_test.py`로 앱 서버부터 확인) |
| 스트리밍인데 글자가 한꺼번에 나온다 | 2교시 단계 1 (`--show-events`의 `events` 수 확인) |
| 7860·8000·8001 포트가 이미 사용 중 | 2교시 단계 2 / 3교시 시작 (이전 프로세스·컨테이너 종료) |
| `docker build`가 데몬 연결 오류 | 3교시 단계 4 (경로 B로 진행) |
| 컨테이너의 `/health`가 `reachable: false` | 3교시 단계 3 (`host.docker.internal`, Ollama 바인딩 주소) |
| clone한 폴더에서 `uv sync` 후 실행이 다르다 | 3교시 단계 4 (`.env.example` 복사 여부, 기본값 확인) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
