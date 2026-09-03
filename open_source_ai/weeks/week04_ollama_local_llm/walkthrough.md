# 4주차 따라하기 — 모델 실측, REST API 호출, 커스텀 모델

이 문서는 4주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 각 교시의 20분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- Ollama가 설치되어 있고 서버가 켜져 있다(`ollama list`가 오류 없이 출력된다).
- 기본 모델과 소형 모델이 수업 전에 캐시되어 있다. 이 문서의 `qwen3:8b`·`qwen3:0.6b`는 교재 검증용 기본값이며 실제 이름은 환경 기준표가 정한다. 실습 중 `ollama pull`을 하지 않는다.
- uv, Git, VS Code, PowerShell을 사용한다. `uv sync`는 수업 전에 한 번 실행해 둔다.
- [`examples/`](examples/README.md) 폴더를 개인 실습 폴더(`C:\classwork\week04`)에 **복사**해서 사용한다. 수업 자료 원본은 수정하지 않는다.
- 터미널 명령은 복사한 폴더 안에서 실행한다. 현재 경로를 먼저 확인하는 습관을 들인다.

---

## 1교시 — 모델 두 개를 실행하고 측정하기

### 단계 1. 서버와 캐시 확인

**할 일**

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
New-Item -ItemType Directory -Force C:\classwork\week04 | Out-Null
Copy-Item "$src\model_report_template.md" C:\classwork\week04\model_report.md
Copy-Item "$src\ollama_probe.ps1" C:\classwork\week04\
Set-Location C:\classwork\week04
ollama list
```

**예상 결과** — `NAME`, `ID`, `SIZE`, `MODIFIED` 열이 있는 표에 `qwen3:8b`와 `qwen3:0.6b`가 보인다. SIZE는 파일 크기다(8b는 5 GB 안팎, 0.6b는 1 GB 미만).

**확인** — [ ] 두 모델의 SIZE를 `model_report.md` 1절 "파일 크기" 칸에 옮겨 적었다.

### 단계 2. `ollama show`로 모델 정보 읽기

**할 일** — `ollama show qwen3:8b`를 실행하고 `parameters`, `quantization`, `context length` 줄을 찾는다.

**예상 결과** — `Model` 항목 아래에 architecture, parameters(예: `8.2B`), context length, embedding length, quantization(예: `Q4_K_M`)이 보인다. `Capabilities`에 `completion`·`tools`와 함께 `thinking`이 보인다. 기본 모델은 하이브리드라 생각 모드를 켜고 끌 수 있다(2교시).

**확인** — [ ] 파라미터 수 × 0.6바이트로 계산한 값이 단계 1의 파일 크기와 대략 맞는지 적었다.

### 단계 3. `ollama run` + `/set verbose`로 속도 측정

**할 일**

1. `ollama run qwen3:8b`를 실행한다. 프롬프트 `>>>`가 나오면 `/set verbose`를 입력한다.
2. `model_report.md` 2절의 질문 3개를 그대로 차례로 입력한다.
3. 각 답 뒤에 붙는 `eval rate`와 첫 답의 `load duration`을 적는다.
4. `/bye`로 나온다.

**예상 결과** — 첫 답은 로드 때문에 몇 초 늦게 시작하고, 이후 답은 바로 시작한다. 답 뒤에 `total duration`, `load duration`, `prompt eval count`, `eval count`, `eval rate` 줄이 붙는다. Qwen3 계열은 답 앞에 생각 텍스트가 보일 수 있다.

**확인** — [ ] eval rate 세 값의 평균을 1절에 적었다. 생각 텍스트가 보였다면 그 사실도 적었다.

### 단계 4. `ollama ps`로 메모리 실측

**할 일** — `/bye`로 나온 직후 `ollama ps`를 실행하고, 이어서 `.\ollama_probe.ps1 -Model qwen3:8b`를 실행한다.

**예상 결과** — `ollama ps`에 `qwen3:8b`가 한 줄 보이고 SIZE는 단계 1의 파일 크기보다 크며, PROCESSOR는 GPU PC에서 `100% GPU`다. `outputs/probe-qwen3-8b-<날짜시각>.txt`가 생기고 안에 list/show/ps 출력이 모두 들어 있다.

**확인** — [ ] 파일 크기와 메모리 크기의 차이를 "컨텍스트(KV 캐시)와 실행 버퍼"로 설명했다. 5분이 지나 `ps`가 비어 있었다면 다시 올린 뒤 측정했다.

### 단계 5. 소형 모델로 반복

**할 일** — `qwen3:0.6b`로 단계 2~4를 반복한다. 질문은 바꾸지 않는다.

**예상 결과** — 파일·메모리 크기가 훨씬 작고 tokens/s는 몇 배 빠르다. 답은 짧거나 형식(표·JSON)을 덜 지키거나 틀릴 수 있다. GPU가 없는 PC에서는 PROCESSOR에 `CPU`가 포함된다.

**확인** — [ ] 두 모델의 tokens/s 비율을 3절에 적고, 질문별 답 차이를 2절에 한 문장씩 적었다.

### 단계 6. 보고서 마무리

**할 일** — `model_report.md` 3절(계산과 실측)과 4절(결론)을 채운다.

**예상 결과** — 계산값과 실측값이 같은 자릿수 안에서 맞고, 팀 도우미 기본 모델과 그 이유 두 가지, GPU 없는 팀원의 대체 모델이 적혀 있다.

**확인** — [ ] [`lab.md`](lab.md) 1교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분.

---

## 2교시 — REST API로 대화하고 실패를 다루기

### 단계 1. `/api/tags`로 서버 확인과 프로젝트 준비

**할 일**

```powershell
Invoke-RestMethod http://localhost:11434/api/tags | Select-Object -ExpandProperty models | Format-Table name, size
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"   # 새 창이면 다시 지정
Copy-Item -Recurse "$src\ollama_client" C:\classwork\week04\ollama_client
Set-Location C:\classwork\week04\ollama_client
Copy-Item .env.example .env
uv sync
uv run python config.py
```

**예상 결과** — 첫 줄에 캐시된 모델 이름과 바이트 단위 크기가 표로 나온다. `uv sync`가 `.venv`를 만들고, `config.py`가 `host = http://localhost:11434`, `model = qwen3:8b`를 출력한다.

**확인** — [ ] `uv run python config.py --model qwen3:0.6b`로 인자가 환경변수를 이기는 것을 보았다.

### 단계 2. `chat.py` 첫 호출과 메타 손계산

**할 일**

```powershell
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag first
```

`outputs/chat-<날짜시각>-first.json`을 열어 `response.eval_count`와 `response.eval_duration`을 찾는다.

**예상 결과** — 답 두 문장, 구분선, `model=… eval_tokens=… tokens/s=… load=…s total=…s done_reason=stop`, `saved: outputs\chat-…-first.json`이 차례로 나온다. JSON의 `request`에는 `"stream": false`, `"think": false`, `"options"`가 있다.

**확인** — [ ] `eval_count ÷ (eval_duration ÷ 1e9)`를 계산기로 계산한 값이 화면의 `tokens/s`와 같다.

### 단계 3. 두 번째 호출과 스트리밍

**할 일**

```powershell
uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag second
uv run python stream.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."
uv run python chat.py --prompt "오픈소스의 정의를 설명해 줘." --num-predict 32 --tag short
```

**예상 결과** — 두 번째 호출의 `load`가 0에 가깝다. `stream.py`는 글자가 조각으로 찍히고 끝에 `chunks=…  first_piece=…s  wall=…s`가 나온다. `--num-predict 32`는 답이 중간에 끊기고 `done_reason=length`다.

**확인** — [ ] `outputs/stream-*.json`의 `final_chunk`에만 `eval_count`가 있고 `answer`는 조각을 이어 붙인 전체 문장이다.

### 단계 4. 실패 두 가지 재현

**할 일**

```powershell
uv run python chat.py --host http://localhost:11435 --prompt "안녕"
$LASTEXITCODE
uv run python chat.py --model no-such-model --prompt "안녕"
$LASTEXITCODE
uv run python stream.py --model no-such-model --prompt "안녕"
```

**예상 결과** — 첫 번째는 `[연결 실패] http://localhost:11435 에 접속할 수 없다. …` 한 문장과 종료 코드 `2`. 두 번째는 `[모델 없음] 'no-such-model' … ollama list 로 …`와 종료 코드 `3`. 스택 트레이스는 나오지 않는다. `stream.py`도 같은 문장을 낸다.

**확인** — [ ] 두 메시지에 "다음에 할 일"(`OLLAMA_HOST` 확인, `ollama list`)이 들어 있음을 확인하고 `failures.md`에 원문을 적었다.

### 단계 5. `--seed` 추가와 temperature 비교

**할 일**

1. `chat.py`의 `build_parser()`에 정수 인자 `--seed`를 추가하고, `build_payload()`에서 값이 있을 때만 `options["seed"]`를 넣는다.
2. `uv run python chat.py --prompt "안녕" --seed 7 --show-request`로 요청 JSON에 `"seed": 7`이 보이는지 확인한다.
3. 같은 프롬프트로 네 번 실행한다.

```powershell
$q = "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."
uv run python chat.py --prompt $q --temperature 0 --seed 7 --tag t0a
uv run python chat.py --prompt $q --temperature 0 --seed 7 --tag t0b
uv run python chat.py --prompt $q --temperature 1 --seed 7 --tag t1a
uv run python chat.py --prompt $q --temperature 1 --seed 7 --tag t1b
```

**예상 결과** — temperature 0의 두 답은 거의 또는 완전히 같다. temperature 1의 두 답은 seed가 같으므로 같거나 매우 비슷하되, GPU 연산 순서 때문에 조금 다를 수 있다. temperature 1 쪽이 0 쪽보다 표현이 다양하다.

**확인** — [ ] `temperature_compare.md`에 temperature와 seed의 역할을 각각 한 문장으로 적었다. [`lab.md`](lab.md) 2교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분.

---

## 3교시 — 수업 도우미 모델 만들기와 과제 점검

### 단계 1. 기준 모델의 Modelfile 훑어보기

**할 일**

```powershell
Set-Location C:\classwork\week04\ollama_client
ollama show qwen3:8b --modelfile | Select-Object -First 30
Get-Content Modelfile
```

**예상 결과** — 기준 모델의 Modelfile에는 `FROM`(blob 경로), 긴 `TEMPLATE`, `PARAMETER`, `LICENSE`가 있다. 우리 Modelfile에는 `FROM qwen3:8b`, `SYSTEM """…"""`, `PARAMETER` 두 줄만 있고 `TEMPLATE`은 없다.

**확인** — [ ] `TEMPLATE`을 직접 쓰지 않아도 `FROM`에서 물려받는다는 것을 확인했다.

### 단계 2. SYSTEM 수정과 `ollama create`

**할 일**

1. `Modelfile`의 `FROM`이 `ollama list`에 있는 이름과 같은지 확인한다(GPU가 없으면 소형 모델 이름으로).
2. `SYSTEM` 첫 줄에 팀명을 넣는다: `너는 'team-a'의 오픈소스 AI 응용 실습 도우미다.`
3. 실행한다. 교재 예시 이름은 `osa-helper`이지만 공용 PC에서 겹치지 않도록 자기 표시 이름을 붙인다.

```powershell
ollama create student01-helper -f Modelfile
ollama list
ollama show student01-helper
```

**예상 결과** — `create`가 몇 초 안에 `success`로 끝난다. `ollama list`에 `student01-helper:latest`가 생기고 SIZE는 기준 모델과 같아 보인다(가중치 blob 공유). `ollama show student01-helper`에 `System` 항목과 `Parameters`(temperature, num_ctx)가 보인다.

**확인** — [ ] `create`가 다운로드를 시작하지 않았다(시작했다면 `Ctrl+C` 후 `FROM` 이름을 고친다).

### 단계 3. 기준 모델과 커스텀 모델 전후 비교

**할 일** — 질문 3개를 두 모델로 실행한다. Q1만 예로 든다.

```powershell
$q1 = "uv가 무엇인지 두 문장으로 설명해 줘."
uv run python chat.py --prompt $q1 --tag base-1
uv run python chat.py --model student01-helper --prompt $q1 --tag helper-1
```

**예상 결과** — 커스텀 모델의 답이 5문장 이내로 짧고, 명령이 나오면 PowerShell 코드 블록 하나로 온다. 기준 모델은 길이·형식이 자유롭다. JSON 6개(`base-1..3`, `helper-1..3`)가 `outputs/`에 쌓인다.

**확인** — [ ] `model_report.md` 5절의 "기준 모델"·"커스텀 v1" 열을 길이·언어·형식·정확성 기준으로 채웠다.

### 단계 4. SYSTEM 한 줄 변경과 재비교

**할 일**

1. `SYSTEM`에서 한 줄만 바꾼다(예: `5문장 이내` → `한 문장으로만`). 바꾼 줄을 5절 제목 칸에 적는다.
2. 같은 이름으로 다시 `ollama create student01-helper -f Modelfile`을 실행한다.
3. 질문 3개를 `--tag helper-2`로 다시 실행해 "커스텀 v2" 열을 채운다.
4. 충돌 관찰: `uv run python chat.py --model student01-helper --system "영어로만 답한다." --prompt $q1 --tag conflict`

**예상 결과** — `ollama show student01-helper`의 System이 바뀐 줄로 갱신되어 있다. v2의 답 길이가 바뀐 줄대로 달라진다(달라지지 않으면 그 사실이 관찰이다). 충돌 실행에서는 요청의 `--system`과 Modelfile SYSTEM 중 한쪽의 지시가 답에 드러난다.

**확인** — [ ] 어느 쪽이 답에 나타났는지 5절 마지막 줄에 한 문장으로 적었다.

### 단계 5. 1차 종합과제 점검

**할 일** — [`assignment_brief.md`](assignment_brief.md)의 "제출 전 검사" 목록을 열어 자기 저장소 기준으로 하나씩 표시하고, 비어 있는 항목과 다음 수업 전까지 채울 계획을 `assignment_check.md`에 적는다.

**예상 결과** — 2주차 LICENSE·PR·리뷰, 3주차 `pyproject.toml`·`uv.lock`·`.env.example`은 이미 있고, 이번 주의 `chat`·`stream` 서브커맨드 통합, `model_report.md`, `Modelfile`, `evidence/`가 남은 항목으로 드러난다.

**확인** — [ ] [`lab.md`](lab.md) 3교시 완료 조건을 모두 표시했다. 실습 30분 뒤 휴식 10분. 이번 주 종료.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| `ollama list`가 오류를 낸다 | 1교시 단계 1 (서버 트레이 아이콘 확인, 새 창에서 `ollama serve`) |
| 모델이 목록에 없다 | 1교시 단계 1 (사전 캐시 확인. 실습 중 `pull` 금지, 강의자에게 문의) |
| `/set verbose`를 쳤는데 속도가 안 나온다 | 1교시 단계 3 (`>>>` 프롬프트에서 슬래시 포함해 입력) |
| `ollama ps`가 비어 있다 | 1교시 단계 4 (모델이 내려감. `run`으로 다시 올린 뒤 5분 안에 실행) |
| `ollama_probe.ps1`이 "스크립트를 실행할 수 없으므로"로 멈춘다 | 1교시 단계 4 (`powershell -ExecutionPolicy Bypass -File .\ollama_probe.ps1 -Model qwen3:8b`로 이번 실행만 우회) |
| `uv sync`가 실패한다 | 2교시 단계 1 (네트워크·uv 캐시 확인. `pip install` 금지) |
| 연결 실패 대신 시간 초과가 난다 | 2교시 단계 4 (재현용 포트는 비어 있는 것으로. 정상 호출이면 `OLLAMA_TIMEOUT` 증가) |
| `--seed`가 요청 JSON에 안 보인다 | 2교시 단계 5 (`build_payload()`의 `options`에 넣었는지, `--show-request`로 확인) |
| `ollama create`가 다운로드를 시작한다 | 3교시 단계 2 (`Ctrl+C` 후 `FROM`을 `ollama list`의 이름으로) |
| 커스텀 모델 답에 생각 텍스트가 섞인다 | 3교시 단계 3 (`chat.py`로 호출하면 `think:false`. `ollama run`은 섞일 수 있음) |
| v1과 v2 답이 거의 같다 | 3교시 단계 4 (`--temperature 0`으로 재실행. 그래도 같으면 "효과 없음"이 결론) |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
