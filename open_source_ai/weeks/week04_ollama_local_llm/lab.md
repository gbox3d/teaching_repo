# 4주차 실습 — 로컬 모델을 실측하고, 호출하고, 역할을 입힌다

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 실습 시간에 `ollama pull`을 실행하지 않는다. 모델은 수업 전에 캐시되어 있고, 이름은 환경 기준표가 정한다. 이 문서의 `qwen3:4b`·`qwen3:0.6b`는 교재 검증용 기본값이다.
- 실제 토큰·비밀번호를 `.env`나 산출물에 쓰지 않는다. `.env`는 커밋하지 않는다.

## 1교시 실습 — 모델 두 개를 실행하고 측정하기

### 상황

팀 저장소 README에 "이 도우미는 어떤 모델을 쓰며 실습실 PC에서 얼마나 빠른가"를 적어야 한다. 팀원이 원하는 것은 캡처가 아니라 파라미터 수·양자화·메모리·tokens/s와, 같은 질문에 대한 답 품질 차이가 적힌 `model_report.md`다. 기본 모델과 소형 모델을 같은 절차로 측정해 채워라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 두 모델의 파일 크기·메모리·tokens/s를 예상표에 적기 |
| 기본 모델 실측 | 5–13분 | `ollama show` → `ollama run` + `/set verbose` + 질문 3개 → `ollama ps` |
| 소형 모델 실측 | 13–20분 | 같은 절차를 소형 모델로 반복 |
| 답 비교·계산 | 20–25분 | 질문 3개의 답 차이, 파라미터 수 × 바이트 계산과 실측 대조 |
| 검증·기록 | 25–30분 | `model_report.md` 1~4절 완성, `ollama_probe.ps1` 출력 저장 |

### 준비

원본을 두고 개인 실습 폴더에 복사한다. `$src`에는 교재 저장소의 `examples` 폴더 경로를 넣는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
New-Item -ItemType Directory -Force C:\classwork\week04 | Out-Null
Copy-Item "$src\model_report_template.md" C:\classwork\week04\model_report.md
Copy-Item "$src\ollama_probe.ps1" C:\classwork\week04\
Set-Location C:\classwork\week04
ollama list
```

`ollama list`에 기본 모델과 소형 모델 두 줄이 보여야 시작한다. 보이지 않으면 힌트 1로 간다.

### 문제 1 · 기본 모델 실측

1. 실행 전에 예상표를 적는다. 기본 모델의 파일 크기, `ollama ps`에 보일 메모리 크기, tokens/s, 소형 모델은 각각 몇 배가 될지.
2. `ollama show qwen3:4b`를 실행해 `parameters`, `quantization`, `context length` 값을 `model_report.md` 1절에 옮겨 적는다. `ollama list`의 SIZE도 적는다.
3. `ollama run qwen3:4b`로 들어가 `/set verbose`를 입력한 뒤, 보고서 2절의 질문 3개를 **그대로** 차례로 묻는다. 각 답 뒤에 나오는 `eval rate`(tokens/s)와 첫 답의 `load duration`을 적는다. `/bye`로 나온다.
4. 나오자마자 `ollama ps`를 실행해 SIZE와 PROCESSOR를 적는다. 5분이 지나면 모델이 메모리에서 내려가므로 비어 있을 수 있다.
5. `.\ollama_probe.ps1 -Model qwen3:4b`로 `list/show/ps` 출력을 `outputs/`에 저장한다.

완료 조건:

- [ ] 보고서 1절의 모델 A 열이 모두 채워졌다(예상표와 다른 칸에 표시).
- [ ] 질문 3개의 답이 각각 어떤 형식(문장·표·코드)으로 왔는지 한 줄씩 적었다.
- [ ] `outputs/probe-qwen3-4b-*.txt`가 생겼다.

### 문제 2 · 소형 모델과 비교

1. `qwen3:0.6b`로 문제 1의 2~5단계를 반복한다. 질문은 바꾸지 않는다.
2. 보고서 2절에 질문별 답 차이를 한 문장씩 적는다. 길이·형식·정확성 중 무엇이 달랐는지 명시한다.
3. 보고서 3절을 채운다. 파라미터 수 × 파라미터당 바이트(Q4 계열은 약 0.6)로 예상 가중치 크기를 계산해 파일 크기와 대조하고, `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다른 이유를 적는다.
4. 보고서 4절에 팀 도우미 기본 모델을 고르고 이유 두 가지를 적는다.

완료 조건:

- [ ] 모델 B 열이 채워지고 두 모델의 tokens/s 비율을 계산했다.
- [ ] 답 차이 3문장에 "길이·형식·정확성" 중 하나 이상이 근거로 들어 있다.
- [ ] 계산값과 실측값의 차이를 한 문장으로 설명했다.

### 단계별 힌트

<details>
<summary>힌트 1 — `ollama list`가 오류를 내거나 모델이 보이지 않는다</summary>

서버가 켜져 있지 않으면 CLI도 동작하지 않는다. 트레이의 Ollama 아이콘을 확인하거나 새 PowerShell 창에서 `ollama serve`를 실행한 채로 둔다. 모델이 목록에 없으면 강의자에게 사전 캐시 상태를 확인한다. 실습 시간에 `ollama pull`을 실행하지 않는다.
</details>

<details>
<summary>힌트 2 — `/set verbose`를 쳤는데 속도가 안 보인다</summary>

`/set verbose`는 `ollama run` 안의 프롬프트(`>>>`)에서 입력하는 명령이다. 입력 뒤 다음 질문의 답이 끝나면 `total duration`, `eval count`, `eval rate` 줄이 나온다. 슬래시가 빠지면 모델에게 보내는 문장이 된다.
</details>

<details>
<summary>힌트 3 — `ollama ps`가 비어 있다</summary>

모델은 마지막 요청 뒤 기본 5분이 지나면 메모리에서 내려간다. `ollama run`으로 질문 하나를 다시 던지고 `/bye`한 직후에 `ollama ps`를 실행한다. Qwen3 계열의 답 앞에 생각 텍스트가 섞이면 그것도 기록한다. 2교시의 API 호출에서는 `think:false`로 끈다.
</details>

### 검증

- 정상: 두 모델 모두 질문 3개에 답했고, tokens/s·SIZE·PROCESSOR가 기록되어 있다. GPU PC에서는 PROCESSOR가 `100% GPU`, GPU가 없는 PC에서는 `CPU`가 포함된 값이다.
- 경계 또는 실패: `ollama ps`가 비어 있는 상태(언로드)를 한 번 보고, 다시 올린 뒤 채웠다. 파일 크기(`list`)와 메모리 크기(`ps`)가 다르다는 것을 확인했다.
- 설명: "양자화 표기(예: `Q4_K_M`)가 파라미터당 바이트에 어떤 뜻이고, 그래서 파일 크기가 계산과 대략 맞는다"를 한 문장으로 적었다.

### 확장 문제

1. `ollama run` 안에서 `/set parameter num_ctx 16384`를 입력하고 질문 하나를 던진 뒤 `ollama ps`의 SIZE가 기본값일 때와 얼마나 달라지는지 기록한다.
2. 같은 질문을 연속으로 두 번 물어 첫 답과 두 번째 답의 `load duration`·`prompt eval count` 차이를 설명한다.
3. 캐시에 세 번째 모델이 있으면 보고서에 열을 추가하고 같은 질문 3개로 측정한다.

## 2교시 실습 — REST API로 대화하고 실패를 다루기

### 상황

팀 저장소에 "도우미 CLI가 서버가 꺼져 있으면 스택 트레이스만 뿜는다"는 Issue가 올라왔다. 예제 클라이언트를 돌려 응답 메타를 읽고, 실패 두 가지(연결 실패·모델 없음)를 재현해 메시지와 종료 코드를 확인하고, `--seed`를 추가한 뒤 temperature 옵션이 답에 미치는 영향을 기록하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 첫 호출과 둘째 호출의 시간 차이, 실패 두 가지의 메시지·종료 코드 예상 |
| chat.py·메타 읽기 | 5–12분 | 실행 → JSON에서 `eval_count`·`eval_duration` 찾아 tokens/s 손계산 |
| stream.py·실패 경로 | 12–19분 | 스트리밍 관찰 → 포트 오류·모델 이름 오류 재현 |
| seed 추가·temperature 비교 | 19–25분 | `--seed` 옵션 구현 → temperature 0과 1을 각 2회 |
| 검증·기록 | 25–30분 | 실패 메시지 2건, 비교 문단, `outputs/` 확인 |

### 준비

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
Copy-Item -Recurse "$src\ollama_client" C:\classwork\week04\ollama_client
Set-Location C:\classwork\week04\ollama_client
Copy-Item .env.example .env
uv sync
uv run python config.py
```

`config.py` 출력의 `host`와 `model`이 `.env` 값과 같으면 시작한다. 하루가 바뀌어 서버에 모델이 올라와 있지 않아도 된다. 첫 호출이 느린 것은 로드 시간이다.

### 문제 1 · chat.py와 stream.py, 메타 읽기

1. 예상을 적는다. 같은 프롬프트를 두 번 보내면 `load_seconds`와 `total_seconds`는 어떻게 달라질까. `--num-predict 32`를 주면 `done_reason`은 무엇일까.
2. `uv run python chat.py --prompt "uv가 무엇인지 두 문장으로 설명해 줘." --tag first`를 실행한다. 화면의 `tokens/s`를 적는다.
3. `outputs/chat-<날짜시각>-first.json`을 열어 `response` 안의 `eval_count`와 `eval_duration`을 찾고 `eval_count ÷ (eval_duration ÷ 1e9)`를 계산기로 계산해 화면 값과 비교한다.
4. 같은 명령을 `--tag second`로 한 번 더 실행하고 두 JSON의 `metrics.load_seconds`를 비교한다.
5. `uv run python stream.py --prompt "MIT 라이선스와 GPL의 차이를 표로 정리해 줘."`를 실행한다. 조각이 찍히는 모습, `chunks`, `first_piece`를 적는다.
6. `uv run python chat.py --prompt "오픈소스의 정의를 설명해 줘." --num-predict 32 --tag short`를 실행하고 `done_reason`을 확인한다.

완료 조건:

- [ ] 손으로 계산한 tokens/s와 화면 값이 소수점 둘째 자리까지 일치한다(반올림 차이 허용).
- [ ] 두 번째 호출의 `load_seconds`가 첫 호출보다 작은 이유를 한 문장으로 적었다.
- [ ] `stream.py`의 메타가 마지막 줄(`done:true`)에만 있음을 JSON의 `final_chunk`에서 확인했다.

### 문제 2 · 실패 두 가지와 temperature 비교

1. 연결 실패: `uv run python chat.py --host http://localhost:11435 --prompt "안녕"`을 실행하고 곧바로 `$LASTEXITCODE`를 확인한다. 서버를 끄지 않고 포트만 틀리게 하는 방법이다. 메시지를 그대로 적는다.
2. 모델 없음: `uv run python chat.py --model no-such-model --prompt "안녕"`을 실행하고 `$LASTEXITCODE`와 메시지를 적는다. `stream.py`로도 한 번 반복한다.
3. `chat.py`에 `--seed` 옵션을 추가한다. `argparse`에 정수 인자를 하나 더 두고, 값이 주어졌을 때만 `options`에 `seed`를 넣는다. `--show-request`로 요청 JSON에 `seed`가 들어갔는지 확인한다.
4. 같은 프롬프트(`MIT 라이선스와 GPL의 차이를 표로 정리해 줘.`)로 네 번 실행한다: `--temperature 0 --seed 7 --tag t0a`, `--temperature 0 --seed 7 --tag t0b`, `--temperature 1 --seed 7 --tag t1a`, `--temperature 1 --seed 7 --tag t1b`.
5. 네 답을 비교해 한 문단을 쓴다. temperature 0의 두 답이 같은가, temperature 1의 두 답은 같은가, 같은 seed인데 다르다면 무엇이 개입했다고 보는가.

완료 조건:

- [ ] 연결 실패는 종료 코드 2, 모델 없음은 3이고, 두 메시지 모두 다음에 할 일(`OLLAMA_HOST` 확인, `ollama list`)을 담고 있다.
- [ ] `--show-request` 출력에 `"seed"`가 보인다.
- [ ] 비교 문단에 temperature와 seed의 역할이 각각 한 문장으로 들어 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — `uv sync`가 실패한다</summary>

네트워크가 막혀 있으면 의존성을 받을 수 없다. 수업 전 캐시가 준비된 PC라면 `uv sync --offline`을 시도하고, 안 되면 강의자에게 uv 캐시 경로를 확인한다. `pip install`은 쓰지 않는다.
</details>

<details>
<summary>힌트 2 — 연결 실패가 아니라 시간 초과 메시지가 나온다</summary>

포트가 열려 있지만 응답하지 않는 상태다. `--host`에 적은 포트가 다른 프로그램의 포트는 아닌지 확인하고, 재현 목적이면 `11435`처럼 비어 있는 포트를 쓴다. 정상 호출이 시간 초과라면 `.env`의 `OLLAMA_TIMEOUT`을 늘리고 `ollama ps`로 모델이 올라오는지 본다.
</details>

<details>
<summary>힌트 3 — `--seed`를 넣었는데 요청 JSON에 안 보인다</summary>

`build_payload()`가 만드는 `options` 딕셔너리에 실제로 넣었는지 확인한다. `args.seed`가 `None`일 때는 넣지 않도록 조건을 둔다. `--show-request`는 서버에 보내기 직전의 JSON을 그대로 출력하므로 여기서 보이지 않으면 서버에도 가지 않은 것이다.
</details>

### 검증

- 정상: `outputs/`에 `chat-*-first.json`, `chat-*-second.json`, `stream-*.json`, `chat-*-t0a.json` 등이 있고, 각 JSON의 `request`에 `"stream"`, `"think": false`, `"options"`가 들어 있다.
- 경계 또는 실패: 연결 실패·모델 없음 모두 스택 트레이스 없이 한 문장으로 끝났고 종료 코드가 0이 아니다. `--num-predict 32`에서 `done_reason`이 `length`였다.
- 설명: "`/api/chat`의 `messages`에 이력을 쌓는 책임이 서버가 아니라 클라이언트에 있는 이유"를 한 문장으로 적었다.

### 확장 문제

1. `chat.py`를 복사해 `/api/generate`를 쓰는 `generate.py`를 만들고, 같은 프롬프트에 대한 응답 JSON에서 필드 이름이 어떻게 다른지(`response` vs `message.content`) 기록한다.
2. `--messages-file` 옵션을 추가해 JSON 파일의 대화 이력을 `messages`에 그대로 넣어 보내고, 이전 답을 참조하는 후속 질문이 되는지 확인한다.
3. `num_ctx`를 512로 줄이고 긴 프롬프트를 보내 답이 어떻게 달라지는지 관찰한다.

## 3교시 실습 — 수업 도우미 모델 만들기와 과제 점검

### 상황

팀장이 "모든 팀원의 CLI가 같은 말투와 형식으로 답하게 해 달라"고 했다. 시스템 프롬프트를 클라이언트가 매번 보내는 대신 모델 이름 안에 넣어 두고, 기준 모델·커스텀 모델·SYSTEM 한 줄 변경 후의 답을 같은 질문 3개로 비교표에 남긴 뒤, 1차 종합과제 저장소를 체크리스트로 점검하라.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | create 뒤 `ollama list` SIZE, 답 길이 변화 예상 |
| Modelfile 수정·create | 4–11분 | FROM 확인, SYSTEM에 팀명 한 줄 추가, `ollama create`, `show` |
| 전후 비교 | 11–19분 | 질문 3개를 기준 모델과 커스텀 모델로 `chat.py` 실행, 표 채우기 |
| SYSTEM 한 줄 변경·재비교 | 19–24분 | 한 줄만 바꿔 재생성, 같은 질문 재실행, `--system` 충돌 관찰 |
| 증거 정리 | 24–30분 | 1차 과제 체크리스트 점검, 빈 항목과 계획 기록, `outputs/` JSON 6개 이상 확인 |

### 준비

```powershell
Set-Location C:\classwork\week04\ollama_client
Get-Content Modelfile
ollama show qwen3:4b --modelfile | Select-Object -First 30
```

두 번째 명령으로 기준 모델의 Modelfile(특히 `TEMPLATE`)이 어떻게 생겼는지 훑어본다. 우리 Modelfile에는 `TEMPLATE`을 쓰지 않는다.

### 문제 1 · 커스텀 모델 생성과 전후 비교

1. 예상을 적는다. `ollama create` 뒤 `ollama list`의 SIZE는 기준 모델과 같을까 다를까. 커스텀 모델의 답은 기준 모델보다 길까 짧을까.
2. `Modelfile`의 `FROM`이 캐시된 기본 모델 이름과 같은지 확인한다. GPU가 없으면 소형 모델 이름으로 바꾼다.
3. `SYSTEM` 블록 첫 줄을 `너는 'team-a'의 오픈소스 AI 응용 실습 도우미다.`처럼 팀명이 들어가게 고친다(팀명은 수업용 값).
4. `ollama create student01-helper -f Modelfile`을 실행하고 `ollama list`, `ollama show student01-helper`로 확인한다. 교재 예시 이름은 `osa-helper`이지만 공용 PC에서 다른 사람과 겹치지 않도록 자기 표시 이름을 앞에 붙인다. 이름은 소문자·숫자·`-`만 쓴다.
5. 보고서 2절의 질문 3개를 기준 모델과 커스텀 모델로 각각 실행한다. 예: `uv run python chat.py --prompt "<Q1>" --tag base-1`, `uv run python chat.py --model student01-helper --prompt "<Q1>" --tag helper-1`.
6. `model_report.md` 5절의 "기준 모델"·"커스텀 v1" 열에 답의 길이·언어·형식·정확성을 적는다.

완료 조건:

- [ ] `ollama list`에 `student01-helper`가 보이고 `ollama show`에 System 항목이 있다.
- [ ] 질문 3개 × 모델 2개 = JSON 6개가 `outputs/`에 있다.
- [ ] 예상(SIZE·길이)과 실제가 다른 칸에 표시했다.

### 문제 2 · SYSTEM 한 줄 변경과 과제 점검

1. `Modelfile`의 `SYSTEM`에서 **한 줄만** 바꾼다. 예: `답은 5문장 이내로 짧게 한다.`를 `답은 한 문장으로만 한다.`로. 바꾼 줄을 보고서 5절 제목 칸에 적는다.
2. 같은 이름으로 다시 `ollama create student01-helper -f Modelfile`을 실행한다(덮어쓴다). `ollama show student01-helper`로 바뀐 System을 확인한다.
3. 질문 3개를 다시 실행해(`--tag helper-2`) "커스텀 v2" 열을 채운다.
4. 커스텀 모델에 요청 쪽 시스템 메시지를 함께 보낸다: `uv run python chat.py --model student01-helper --system "영어로만 답한다." --prompt "<Q1>" --tag conflict`. Modelfile의 SYSTEM과 요청의 `--system` 중 어느 쪽이 답에 나타났는지 보고서 5절 마지막 줄에 적는다.
5. [1차 종합과제 안내](assignment_brief.md)의 "제출 전 검사" 목록을 열어 자기 저장소 기준으로 하나씩 표시하고, 비어 있는 항목과 다음 수업 전까지 채울 계획을 `assignment_check.md`에 적는다.

완료 조건:

- [ ] v1과 v2의 답 차이가 바꾼 한 줄로 설명된다(설명되지 않으면 그 사실을 적는다).
- [ ] `--system` 충돌 관찰이 한 문장으로 기록되었다.
- [ ] `assignment_check.md`에 비어 있는 항목과 계획이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — `ollama create`가 다운로드를 시작하거나 manifest 오류를 낸다</summary>

`FROM`에 적은 이름이 캐시에 없다. `Ctrl+C`로 중단하고 `ollama list`에 보이는 이름:태그를 그대로 `FROM`에 적는다. 실습 시간에 다운로드하지 않는다.
</details>

<details>
<summary>힌트 2 — 커스텀 모델의 답에 생각 텍스트가 길게 섞인다</summary>

`chat.py`는 `think:false`를 보내므로 API 호출에서는 섞이지 않아야 한다. `ollama run student01-helper`로 직접 대화하면 섞일 수 있다. 비교표는 `chat.py` 결과로 채운다.
</details>

<details>
<summary>힌트 3 — v1과 v2의 답이 거의 같다</summary>

바꾼 줄이 질문 3개에 영향을 주지 않는 내용일 수 있다. temperature가 0이 아니면 표본 차이도 섞인다. `--temperature 0`으로 다시 실행해 순수하게 SYSTEM 차이만 보고, 그래도 같으면 "이 한 줄은 이 질문들에 효과가 없었다"가 정직한 결론이다.
</details>

### 검증

- 정상: `ollama list`에 커스텀 모델이 있고, 보고서 5절의 세 열(기준·v1·v2)이 질문 3개에 대해 채워져 있다.
- 경계 또는 실패: `FROM`을 존재하지 않는 이름으로 바꿔 `ollama create`가 실패하는 것을 한 번 보고 되돌렸다. 요청의 `--system`과 Modelfile SYSTEM이 충돌하는 경우를 관찰했다.
- 설명: "시스템 프롬프트로 바꿀 수 있는 것과 없는 것"을 이번 비교표의 근거로 한 문장씩 적었다.

### 확장 문제

1. `PARAMETER stop "###"`을 추가하고 답에 `###`이 나오게 유도하는 프롬프트로 생성이 멈추는지 확인한다.
2. Modelfile의 `PARAMETER temperature 0.3`과 요청의 `--temperature 1`이 동시에 있을 때 어느 쪽이 적용되는지 seed를 고정해 확인한다.
3. 커스텀 모델을 `ollama rm student01-helper`로 지우고 `ollama list`에서 기준 모델이 남아 있는지, 다시 `create`하면 즉시 되는지 확인한다.

## 제출 체크

- `model_report.md`: 1~4절(모델 2개 실측·답 비교·계산·결론) + 5절(커스텀 모델 전후 비교표)
- `outputs/probe-*.txt`: 1교시 `list/show/ps` 출력
- `evidence/`: `outputs/`에서 고른 `chat-*-first.json`, `stream-*.json`, `chat-*-t0a.json` 등 2~3개
- `failures.md`: 연결 실패·모델 없음 메시지 원문과 종료 코드
- `temperature_compare.md`: temperature 0과 1, seed에 대한 비교 문단
- `Modelfile`: 팀명이 들어간 SYSTEM, 바꾼 한 줄 표시
- `assignment_check.md`: 1차 과제 체크리스트 점검 결과와 계획
- 선택: 확장 문제 결과
