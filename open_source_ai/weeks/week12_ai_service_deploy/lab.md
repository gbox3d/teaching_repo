# 12주차 실습 — 모델을 서비스로, 서비스를 다른 PC로

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 모델을 내려받지 않는다. 기본 모델(`OLLAMA_MODEL`)은 수업 전에 캐시되어 있다.
- 실패는 Ollama를 끄는 대신 **환경변수를 바꿔** 재현한다(없는 포트, 없는 모델, 짧은 타임아웃). 공유 PC의 Ollama를 종료하지 않는다.
- `.env`는 커밋하지 않는다. 이번 주 예제는 토큰이 필요 없다.

## 1교시 실습 — 앱 서버 세우기와 오류 응답 확인

### 상황

팀원이 "LoRA 실험 결과를 내 PC 밖에서도 써 보고 싶다. HTTP로 열어 달라"고 요청했다. 모델 서버(Ollama) 앞에 앱 서버(FastAPI)를 세우고, 모델 서버가 꺼졌거나 모델이 없거나 느릴 때 앱 서버가 **상태 코드로 원인을 말하는지** 확인하라. 팀원은 캡처가 아니라 상태 코드와 `detail`이 담긴 JSON을 원한다.

이어받는 것: 11주차까지의 개인 저장소와 수업 전에 캐시된 기본 모델(`OLLAMA_MODEL`), 수업 전에 한 번 실행해 둔 `uv sync` 패키지 캐시. 10주차 어댑터가 없어도 이번 주 서비스는 기본 모델로 동작하므로 어댑터 유무는 진행에 영향이 없다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 예제 복사·`uv sync`, 코드를 훑고 실패 4종의 상태 코드 예상 |
| 정상 경로 | 5–12분 | 앱 서버 실행, `/docs`, `smoke_test.py`로 `/health`·`/chat` |
| 실패 경로 | 12–21분 | 없는 포트·없는 모델·짧은 타임아웃·잘못된 요청 재현 |
| 기능 추가 | 21–26분 | `GET /models` 추가 |
| 검증·기록 | 26–30분 | 예상표 완성, `outputs/` 정리 |

### 준비

원본을 두고 개인 실습 폴더에 복사한다. `$src`에는 교재 저장소의 `examples` 폴더 경로를 넣는다. 저장 경로는 학기별 환경 기준표를 따른다(아래는 예시).

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week12_ai_service_deploy\examples"
New-Item -ItemType Directory -Force C:\classwork\week12 | Out-Null
Copy-Item -Recurse "$src\ai_service" C:\classwork\week12\ai_service
Set-Location C:\classwork\week12\ai_service
Copy-Item .env.example .env
uv sync
ollama list
```

`ollama list`에 `.env`의 `OLLAMA_MODEL`과 같은 이름이 있어야 한다. 없으면 강의자에게 사전 캐시 모델 이름을 확인해 `.env`를 고친다.

### 문제 1 · 예상표와 정상 경로

1. 실행 전에 예상표를 적는다.

| 상황 | 예상 코드 | 실제 코드 | `error` 값 | 원인 한 문장 |
|---|---:|---:|---|---|
| `OLLAMA_HOST`를 없는 포트(11435)로 |  |  |  |  |
| `OLLAMA_MODEL`을 `no-such-model`로 |  |  |  |  |
| `OLLAMA_TIMEOUT`을 `0.5`로 |  |  |  |  |
| 요청에 `temperature: 5` |  |  |  |  |

2. 터미널 A에서 앱 서버를 띄운다. 로그 첫 줄에서 모델 서버 주소와 기본 모델을 읽어 적는다.

```powershell
uv run uvicorn app.main:app --port 8000 --reload
```

3. 브라우저에서 `http://localhost:8000/docs`를 열고 `GET /health`를 `Try it out`으로 실행한다. `status`, `reachable`, `has_model`을 기록한다.
4. 터미널 B(같은 폴더)에서 점검 스크립트를 실행하고 `outputs/smoke-*.json`이 생겼는지 확인한다.

```powershell
uv run python smoke_test.py --skip-stream
```

5. `/chat` 응답의 `eval_count`와 `eval_duration_ms`로 초당 토큰 수를 계산해 4주차 `model_report.md`의 값과 비교한다.

완료 조건:

- [ ] `/docs`가 열리고 `/health`의 `status`가 `ok`다.
- [ ] `smoke-*.json`에 `/chat` 200 응답과 `reply`·`eval_count`가 있다.
- [ ] 초당 토큰 수를 계산해 적었다.

### 문제 2 · 실패 경로 4종과 `GET /models`

환경변수는 `.env`보다 우선하며, `--reload`는 코드 변경만 감지한다. **환경변수를 바꿀 때마다 터미널 A에서 `Ctrl+C` 후 다시 실행**한다.

1. 없는 포트: 터미널 A에서 아래를 실행한 뒤 터미널 B에서 `smoke_test.py --skip-stream`을 실행한다. `/health`의 `status`와 `/chat`의 코드를 예상표에 적는다.

```powershell
$env:OLLAMA_HOST = "http://localhost:11435"
uv run uvicorn app.main:app --port 8000
```

2. 없는 모델: `Remove-Item Env:OLLAMA_HOST` 후 `$env:OLLAMA_MODEL = "no-such-model"`로 재실행한다. `/health`의 `has_model`과 `/chat`의 코드를 적는다.
3. 짧은 타임아웃: `Remove-Item Env:OLLAMA_MODEL` 후 `$env:OLLAMA_TIMEOUT = "0.5"`로 재실행한다. `/health`는 어떤가, `/chat`은 어떤가를 적고 이유를 한 문장으로 쓴다.
4. 잘못된 요청: `Remove-Item Env:OLLAMA_TIMEOUT` 후 정상 재실행하고 `/docs`의 `POST /chat`에서 `temperature`를 `5`로, 그다음 `messages`를 `[]`로 보내 코드와 본문을 적는다.
5. `app/main.py`에 `GET /models`를 추가한다. `client.list_models()`가 돌려주는 이름 목록을 `{"models": [...]}`로 응답한다. 모델 서버가 꺼졌을 때(1번 상황) 이 엔드포인트가 502를 돌려주는지 확인한다 — 예외 핸들러가 이미 있으므로 `try`를 쓰지 않아도 된다.

완료 조건:

- [ ] 예상표의 네 행에 실제 코드(502·503·504·422)와 `error` 값이 채워졌고, 502·503·504는 각각 `smoke-*.json`으로, 422는 `/docs` 응답과 `outputs/requests.jsonl`의 한 줄로 남았다.
- [ ] `GET /models`가 `/docs`에 나타나고 정상일 때 이름 목록을, 모델 서버가 꺼졌을 때 502를 돌려준다.
- [ ] 환경변수를 모두 원복했다(`Get-ChildItem Env:OLLAMA_*`가 비어 있다).

### 단계별 힌트

<details>
<summary>힌트 1 — <code>ModuleNotFoundError: No module named 'app'</code></summary>

현재 폴더가 `pyproject.toml`과 `app/`이 함께 보이는 곳인지 `Get-Location`으로 확인한다. `uv run uvicorn app.main:app`은 프로젝트 루트에서 실행해야 한다.
</details>

<details>
<summary>힌트 2 — 환경변수를 바꿨는데 결과가 그대로다</summary>

앱 서버는 시작할 때 환경변수를 읽는다. `--reload`는 파일 변경만 감지하므로 `Ctrl+C` 후 다시 실행한다. 셸 변수가 `.env`보다 우선하니 이전 실험의 변수가 남아 있지 않은지 `Get-ChildItem Env:OLLAMA_*`로 확인한다.
</details>

<details>
<summary>힌트 3 — 504가 아니라 200이 나온다</summary>

모델이 이미 GPU에 올라가 있고 답이 짧으면 0.5초 안에 끝날 수 있다. `smoke_test.py --max-tokens 400`으로 답을 길게 만들거나 `OLLAMA_TIMEOUT`을 `0.1`로 줄인다. `/health`는 `/api/tags`만 부르므로 여전히 `ok`일 수 있다 — 그 차이가 관찰 대상이다.
</details>

### 검증

- 정상: `/health`가 `ok`, `/chat`이 200이며 `X-Request-ID` 헤더와 본문의 `request_id`가 같다.
- 경계 또는 실패: 없는 포트 502, 없는 모델 503, 짧은 타임아웃 504, 범위 밖 값 422가 각각 재현되고 `detail`에 다음 행동이 적혀 있다.
- 설명: 502와 504를 하나의 500으로 합치면 안 되는 이유를 **사용자가 할 조치** 관점에서 한 문장으로 적는다.

### 확장 문제

1. `/health`가 `degraded`일 때 200 대신 503을 돌려주도록 바꾸고, 점검 도구(Docker `HEALTHCHECK`) 관점에서 장단점을 두 문장으로 적는다.
2. `OllamaUnavailable`에 한해 1회 재시도하도록 클라이언트를 고치고, 왜 `OllamaTimeout`에는 재시도를 붙이면 안 되는지 적는다.
3. `outputs/requests.jsonl`에서 `/chat`의 평균 `elapsed_ms`를 구하는 PowerShell 한 줄(`Get-Content | ConvertFrom-Json`)을 만든다.

## 2교시 실습 — 스트리밍 채팅 UI 연결

### 상황

팀원이 "답이 나올 때까지 10초 넘게 화면이 멈춰 보여서 사용자가 새로고침을 누른다"고 보고했다. 전체 시간을 줄일 수는 없다. 대신 첫 글자를 빨리 보여 주고, 중간에 멈출 수 있게 하고, 끊겼을 때 무엇을 해야 하는지 화면이 말하게 하라.

이어받는 것: 1교시의 `C:\classwork\week12\ai_service` 폴더. 환경변수를 모두 원복하고(`Remove-Item Env:OLLAMA_*`) 터미널 A에서 앱 서버를 정상 실행해 둔다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 두 모드의 첫 글자까지 시간·전체 시간 예상 |
| SSE 원문 | 4–10분 | `smoke_test.py --show-events`로 이벤트 관찰, `first_chunk_ms`와 `total_ms` |
| UI 두 모드 | 10–18분 | `--no-stream`과 기본 모드로 같은 질문, 시간 기록 |
| 상태·오류 | 18–25분 | Stop, 앱 서버 중단, 모델 서버 실패의 UI 문구 |
| 검증·기록 | 25–30분 | `ui-turns.jsonl` 정리, 비교표 완성 |

### 준비

```powershell
Set-Location C:\classwork\week12\ai_service
Get-ChildItem Env:OLLAMA_*        # 비어 있어야 한다
uv run uvicorn app.main:app --port 8000 --reload   # 터미널 A
```

### 문제 1 · 첫 글자까지의 시간

1. 예상을 적는다: 같은 질문에 대해 비스트리밍 전체 시간, 스트리밍 첫 글자까지 시간, 스트리밍 전체 시간(초 단위).
2. 터미널 B에서 SSE 원문과 시간을 본다. 출력의 `data:` 줄 5개와 `[stream] first=…ms total=…ms`, 그리고 `[chat] …ms`를 적는다.

```powershell
uv run python smoke_test.py --show-events --max-tokens 300
```

3. 비스트리밍 UI를 띄우고 `http://localhost:7860`에서 긴 질문("uv, Git, Ollama를 각각 세 문장으로 설명해 줘")을 보낸다. 답이 나타나기까지 화면에 무엇이 보이는지, 몇 초 걸리는지 적는다.

```powershell
uv run python ui/gradio_app.py --no-stream
```

4. `Ctrl+C`로 끄고 스트리밍 모드로 다시 띄워 같은 질문을 보낸다. 글자가 늘어나는 모습과 `Stop` 버튼이 있는지 적는다.

```powershell
uv run python ui/gradio_app.py
```

5. `outputs/ui-turns.jsonl`의 두 줄에서 `first_ms`·`total_ms`를 읽어 비교표를 만든다.

| 모드 | 첫 글자까지(ms) | 전체(ms) | 화면에 보인 것 |
|---|---:|---:|---|
| once |  |  |  |
| stream |  |  |  |

완료 조건:

- [ ] SSE 이벤트의 모양(`delta`, `done`)을 원문으로 확인했다.
- [ ] 두 모드의 `first_ms`·`total_ms`가 `ui-turns.jsonl`에 남았고 비교표를 채웠다.
- [ ] "전체 시간이 같은데 왜 스트리밍이 낫게 느껴지는가"를 한 문장으로 적었다.

### 문제 2 · 취소와 오류 상태

1. 스트리밍 UI에서 긴 질문을 보내고 답이 흐르는 도중 `Stop`을 누른다. 화면에 남은 텍스트, 다음 질문이 가능한지, 터미널 A의 로그에 남은 줄을 적는다.
2. 터미널 A의 앱 서버를 `Ctrl+C`로 끈 뒤 UI에서 질문한다. UI가 보여 주는 문구를 그대로 적고 앱 서버를 다시 켠다.
3. 터미널 A를 `$env:OLLAMA_HOST = "http://localhost:11435"`로 재실행하고 UI에서 질문한다. 문구의 코드·`detail`·힌트를 적는다. 끝나면 `Remove-Item Env:OLLAMA_HOST` 후 정상 재실행한다.
4. `ui/gradio_app.py`의 `ERROR_HINTS`에서 502·504 문구를 **팀 프로젝트의 사용자**가 읽을 문장으로 고친다(무엇이 잘못됐는지 + 사용자가 지금 할 수 있는 일 한 가지). 실제 연락처·이름을 넣지 않는다.

완료 조건:

- [ ] Stop·앱 서버 중단·모델 서버 실패 세 상황의 문구를 기록했다.
- [ ] `ui-turns.jsonl`에 `error: true`인 턴이 2건 이상 있다.
- [ ] 고친 `ERROR_HINTS` 문구가 "원인 + 다음 행동" 구조다.

### 단계별 힌트

<details>
<summary>힌트 1 — 7860 포트를 이미 쓰고 있다</summary>

이전 UI 프로세스가 남아 있다. 그 터미널에서 `Ctrl+C`로 끄거나 `uv run python ui/gradio_app.py --port 7861`로 다른 포트를 쓴다.
</details>

<details>
<summary>힌트 2 — 스트리밍 모드인데 글자가 한꺼번에 나온다</summary>

UI 상단 설명줄의 `모드 stream`을 확인한다. 그다음 `smoke_test.py --show-events`의 `events` 수가 2 이상이면 앱 서버는 이미 청크를 내보내는 것이므로 문제는 UI 쪽이다. 답이 아주 짧으면 청크가 한두 개뿐이니 `max_tokens`가 큰 긴 질문을 쓴다.
</details>

<details>
<summary>힌트 3 — UI에 "[연결 실패]"가 뜬다</summary>

앱 서버가 꺼져 있거나 `API_BASE_URL`·`--api`가 다른 포트를 가리킨다. 터미널 B에서 `uv run python smoke_test.py --skip-stream`으로 앱 서버부터 확인한다.
</details>

### 검증

- 정상: 스트리밍의 `first_ms`가 비스트리밍의 `total_ms`보다 뚜렷이 작고, 두 모드의 `total_ms`는 비슷하다.
- 경계 또는 실패: Stop 뒤에도 지금까지의 텍스트가 남고 다음 질문이 가능하다. 앱 서버 중단은 `[연결 실패]`, 모델 서버 실패는 `[오류 502]`로 구분되어 보인다.
- 설명: 스트리밍이 전체 시간을 줄이지 않는데도 사용자 경험이 나아지는 이유를 한 문장으로 적는다.

### 확장 문제

1. 정적 HTML 한 장을 만들어 `fetch`로 `/chat`을 부르고 `uv run python -m http.server 5500`으로 연다. 브라우저 콘솔의 CORS 오류를 기록한 뒤 `CORS_ORIGINS`에 `http://localhost:5500`을 추가해 해결한다.
2. Stop을 눌렀을 때 취소가 모델 서버까지 전달되는지 `ollama ps`와 터미널 A 로그로 확인하고, 전달되지 않는다면 어디서 끊기는지 가설을 적는다.
3. `ui-turns.jsonl`에서 모드별 `first_ms` 평균을 구한다.

## 3교시 실습 — Dockerfile과 재현 절차 검증

### 상황

다른 팀이 "너희 서비스를 우리 PC에서 돌려 보고 싶다"고 했다. 그 PC에 Docker가 있을 수도, 없을 수도 있다. 설정이 코드 밖으로 나와 있는지 확인하고, Docker 경로와 uv 경로 두 가지 실행 절차를 README에 적은 뒤, 짝이 README만 보고 `/health`가 `ok`가 될 때까지 따라 하게 하라. 마지막으로 3차 종합과제 점검표를 채운다.

이어받는 것: 1교시 폴더. 개인 실습 폴더가 Git 저장소가 아니면 `git init` 후 첫 commit을 만든다(`.env`가 목록에 없어야 한다). 터미널 A의 앱 서버는 끈다(8000 포트를 비운다).

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | Dockerfile을 읽고 "코드 한 줄 수정 후 재빌드 시 어느 레이어가 다시 도는가" 예상 |
| 설정 외부화 점검 | 4–9분 | `reproduce_check.ps1`, `git status`, `.env` 미추적 확인 |
| 포장·실행 | 9–20분 | 경로 A: `docker build`·`run` / 경로 B: 깨끗한 폴더에서 `uv sync`·실행 |
| 재현 절차 교차 검증 | 20–26분 | README 실행 절 작성, 짝이 따라 실행 |
| 검증·기록·과제 점검 | 26–30분 | 3차 과제 점검표 |

### 준비

```powershell
Set-Location C:\classwork\week12\ai_service
docker --version        # 있으면 경로 A, 없거나 오류면 경로 B
git status --short
```

### 문제 1 · 설정 외부화와 이미지 경계

1. 점검 스크립트를 실행하고 세 절(필수 파일, `.env` 추적 여부, 실행 경로)의 결과를 적는다.

```powershell
.\reproduce_check.ps1
```

2. `git add -A` 후 `git status --short`에 `.env`와 `outputs/`가 **없어야** 한다. 있으면 `.gitignore`를 확인하고 `git restore --staged`로 내린다.
3. `Dockerfile`을 읽고 `COPY pyproject.toml uv.lock* ./`가 `COPY . .`보다 앞에 있는 이유를 두 문장으로 적는다.
4. 경로 A(Docker 있음): 빌드하고, `app/main.py`에 주석 한 줄을 추가한 뒤 다시 빌드해 `CACHED`가 어느 단계까지 표시되는지 적는다. 그다음 실행하고 호스트에서 점검한다.

```powershell
docker build -t osa-ai-service:dev .
docker run --rm -p 8001:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 -e OLLAMA_MODEL=qwen3:8b osa-ai-service:dev
uv run python smoke_test.py --api http://localhost:8001 --skip-stream     # 다른 터미널
```

   `/health`가 `degraded`이고 `detail`이 연결 실패면 호스트의 Ollama가 `127.0.0.1`에만 묶여 있는 것이다. 실습실 정책상 Ollama 설정을 바꿀 수 없으면 그 사실과 `detail`을 기록하고 경로 B로 넘어간다.
5. 경로 B(Docker 없음): 깨끗한 폴더에 `.venv`·`.env`·`outputs`를 뺀 파일만 복사(또는 `git clone`)하고 처음부터 실행한다.

```powershell
git clone C:\classwork\week12\ai_service C:\classwork\week12\clean
Set-Location C:\classwork\week12\clean
Copy-Item .env.example .env
uv sync
uv run uvicorn app.main:app --port 8001
uv run python smoke_test.py --api http://localhost:8001 --skip-stream     # 다른 터미널
```

완료 조건:

- [ ] `reproduce_check.ps1`의 세 절이 모두 `ok`이고 `git status`에 `.env`·`outputs/`가 없다.
- [ ] 경로 A 또는 B로 깨끗한 환경에서 `/health`가 `ok`(또는 `degraded`의 원인 문장)다.
- [ ] 레이어 순서의 이유(경로 A는 `CACHED` 위치까지)를 적었다.

### 문제 2 · README 실행 절과 3차 과제 점검

1. 팀 저장소(없으면 개인 실습 폴더) README에 「실행」 절을 쓴다. 순서: 전제 2줄(Ollama 실행 중, 모델 pull 완료) → 경로 A 명령 → 경로 B 명령 → 확인 명령(`smoke_test.py`) → 실패 시 볼 것(`/health`의 `detail`, `outputs/requests.jsonl`).
2. 짝과 저장소를 바꾼다. 짝은 README **만** 보고 5분 안에 `/health`가 `ok`가 되는지 시도하고, 막힌 줄과 이유를 한 줄씩 적어 준다. 받은 내용을 README에 반영한다.
3. [3차 종합과제 안내서](assignment_brief.md)의 「제출 전 검사」를 `assignment3_checklist.md`로 옮겨 항목마다 O/X와 근거(파일 경로·commit·Issue 번호)를 적는다. X 항목에는 담당자와 처리할 Issue 번호를 적는다.

완료 조건:

- [ ] README 실행 절이 두 경로와 확인 명령, 실패 시 볼 것을 포함한다.
- [ ] 짝 검증 기록(막힌 줄·이유·반영 여부)이 있다.
- [ ] `assignment3_checklist.md`에 모든 항목의 O/X와 근거가 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — <code>docker build</code>가 데몬 연결 오류로 실패한다</summary>

Docker Desktop이 실행 중이 아니다. 실습실 정책상 켤 수 없으면 경로 B로 진행하고 README에는 두 경로를 모두 적는다. 경로 A는 강의자 PC 시연으로 대체한다.
</details>

<details>
<summary>힌트 2 — 컨테이너의 <code>/health</code>가 <code>reachable: false</code>다</summary>

컨테이너 안의 `localhost`는 컨테이너 자신이다. `-e OLLAMA_HOST=http://host.docker.internal:11434`를 넣었는지 확인한다. 그래도 실패하면 호스트의 Ollama가 외부 인터페이스에서 듣지 않는 것이며, Ollama 서버 쪽 `OLLAMA_HOST=0.0.0.0` 설정과 재시작이 필요하다(Ollama FAQ).
</details>

<details>
<summary>힌트 3 — 8000 또는 8001 포트를 이미 쓰고 있다</summary>

1·2교시의 uvicorn이나 컨테이너가 아직 떠 있다. 해당 터미널에서 `Ctrl+C`, 컨테이너는 `docker ps` 후 `docker stop <id>`로 정리한다.
</details>

### 검증

- 정상: 깨끗한 폴더 또는 컨테이너에서 `/health`가 `ok`이고 `smoke_test.py`가 종료 코드 0으로 끝난다.
- 경계 또는 실패: `.env` 없이 실행하면 코드 기본값으로 뜬다(설정 계층의 맨 아래). 잘못된 `OLLAMA_HOST`를 주면 `degraded`와 `detail`이 원인을 말한다.
- 설명: 컨테이너 안에서 `localhost:11434`가 호스트의 Ollama가 아닌 이유를 한 문장으로 적는다.

### 확장 문제

1. `docker image ls`로 이미지 크기를 적고, `gradio`를 선택 의존성으로 분리해 이미지를 줄이는 방법을 `pyproject.toml` 수준에서 설계한다(실제 적용은 선택).
2. `docker ps`의 `STATUS` 열에 `(healthy)`가 나타나는 시점을 관찰하고, `HEALTHCHECK`에 `--start-interval=15s`를 추가해 다시 빌드·실행한 뒤 시점이 어떻게 달라지는지 본다. `--start-period`만 바꾸면 왜 시점이 그대로인지도 적는다.
3. 기준 PC에서 `uv lock`을 만들었다고 가정하고 Dockerfile의 `uv sync`에 `--frozen`을 붙였을 때 무엇이 달라지는지 두 문장으로 적는다.

## 제출 체크

- `outputs/smoke-*.json`: 정상 1건 + 502·503·504 각 1건(파일명과 상황을 표로)
- `outputs/requests.jsonl`: 1교시 요청 기록. 422 두 건(`temperature: 5`, `messages: []`)이 여기에 남는다
- `GET /models` 추가 commit id
- `outputs/ui-turns.jsonl`: 두 모드 비교 턴 + 오류 턴 2건 이상, 비교표
- 취소·앱 서버 중단·모델 서버 실패 세 상황의 UI 문구 기록과 고친 `ERROR_HINTS`
- `Dockerfile`, `.dockerignore`, `.env.example`, `reproduce_check.ps1` 결과
- README 「실행」 절(두 경로) + 짝 검증 기록
- `assignment3_checklist.md`: 3차 과제 점검표
- 선택: 확장 문제 결과
