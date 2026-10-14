# 4주차 따라하기 — 터미널, Python 대화, 이미지·툴 콜링·Modelfile

이 문서는 4주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다. 강의자는 20분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다. 문제의 정본은 [실습지](lab.md)다.

- 각 단계는 `할 일 → 예상 결과 → 확인` 순서다. 예상 결과와 다르면 다음 단계로 넘어가지 않는다.
- 모델의 답 문장은 **매번 달라진다.** 예상 결과에는 문장 대신 "무엇이 보여야 하는지"를 적었다.
- 괄호 안의 숫자는 2026-10-15 Mac(Apple GPU, Ollama 0.40.4, `qwen3.5:2b`)에서 잰 값이다. Windows PC의 크기·속도·표기는 다를 수 있으므로 자기 화면의 값을 적는다.

## 시작 전 준비

- `ollama list`에 `qwen3.5:2b`가 보인다. 없으면 [설치 안내](windows_setup.md)를 먼저 한다. 실습 중에는 `pull`하지 않는다.
- PowerShell에서 `uv --version`이 나온다.
- 작업 폴더와 보고서를 만든다. 새 PowerShell 창을 열 때마다 `$src`·`$dst` 두 줄은 다시 입력한다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
$dst = "C:\classwork\week04"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\week04_report.md")) { Copy-Item "$src\week04_report_template.md" "$dst\week04_report.md" }
```

## 1교시 — 터미널에서 모델 실행하고 숫자 읽기

### 시작 전 준비

코드는 없다. 실행 전에 파라미터 수, 메모리 크기, tokens/s를 예상해 보고서 1절 "예상" 칸에 적는다.

### 단계 1. 모델 정보 읽기

**할 일** — `ollama list`, `ollama show qwen3.5:2b`를 실행한다.

**예상 결과** — `list`에 `qwen3.5:2b`와 SIZE가 보인다. `show`의 `Model` 아래에 parameters(2B대, 이 Mac은 `2.2B`), context length, quantization이 있고, `Capabilities`에 `completion`, `vision`, `thinking`, `tools` 네 줄이 있다. quantization 표기는 실행 환경에 따라 다르다.

**확인** — [ ] 파라미터 수·양자화·Capabilities를 보고서 1절 "실제" 칸에 옮겨 적었다.

### 단계 2. 대화하면서 속도 보기

**할 일** — `ollama run qwen3.5:2b --think=false`로 들어가 `>>>`에서 차례로 입력한다.

```text
/set verbose
파이썬이 무엇인지 두 문장으로 설명해 줘.
uv가 무엇인지 두 문장으로 설명해 줘.
```

**예상 결과** — 첫 답은 모델을 올리느라 조금 늦게 시작한다. 각 답 아래에 `total duration`, `load duration`, `eval count`, `eval rate` 줄이 붙는다(이 Mac은 약 97 tokens/s). uv 설명은 틀리는 일이 많다(예: 자외선으로 설명).

**확인** — [ ] 두 답의 `eval rate`를 적었다. 각 답이 맞는지 한 줄씩 적었다.

### 단계 3. 메모리 확인

**할 일** — `/bye`로 나온 직후 `ollama ps`를 실행한다.

**예상 결과** — `qwen3.5:2b` 한 줄이 보이고 SIZE가 `ollama list`의 SIZE보다 크다(이 Mac은 3.1 GB → 5.3 GB). PROCESSOR는 GPU PC에서 `100% GPU`, GPU가 없으면 `CPU`가 들어간다. 목록이 비어 있으면 `ollama run`을 다시 한 뒤 바로 실행한다.

**확인** — [ ] SIZE·PROCESSOR를 적고, 두 SIZE가 다른 이유(가중치 + 대화 내용을 담는 공간)를 한 문장으로 적었다. 실습 30분 뒤 휴식 10분.

## 2교시 — Python에서 대화하기

### 시작 전 준비

```powershell
Copy-Item -Recurse "$src\period2" "$dst\period2"
Set-Location "$dst\period2"
uv sync
```

`uv sync`가 `.venv`를 만들고 `ollama` 라이브러리를 설치한다. 이후 모든 실행은 `uv run python ...`으로 한다.

`ex01`을 제외한 예제는 `나>`에 질문을 입력한다. 답이 끝나면 다음 질문을 입력할 수 있고, 빈 줄은 건너뛰며 `/bye`로 종료한다. `ex02`~`ex04`는 이번 질문만 보내고, `ex05`부터 이전 질문과 답도 함께 보낸다.

### 단계 1. 첫 질문 — `ex01_hello.py`

**할 일** — `uv run python ex01_hello.py`를 실행하고, 질문 문장을 바꿔 한 번 더 실행한다.

**예상 결과** — 한국어 인사 한 문장이 나온다. 오류 메시지나 생각 출력은 없다.

**확인** — [ ] `messages`(보내는 대화 목록)와 `response.message.content`(모델의 답 글자)를 보고서 2절에 한 줄씩 적었다.

### 단계 2. 시스템 프롬프트 — `ex02_system_prompt.py`

**할 일** — `SYSTEMS` 목록 끝에 자기 역할 문장을 하나 추가하고(예: `"너는 영어 회화 도우미다. ..."`) `uv run python ex02_system_prompt.py`를 실행한다. `나>`에 `리스트가 무엇이야?`를 입력한다. 답을 비교한 뒤 `리스트와 튜플의 차이는 무엇이야?`도 입력하고 `/bye`로 종료한다.

**예상 결과** — 입력한 질문마다 `[system] ...` 줄과 답이 세 번 나오고 다시 `나>`가 보인다. 같은 질문인데 길이·말투·코드 유무가 역할마다 다르다. "두 문장으로"를 지키지 않거나 코드 주석이 틀리는 경우도 있다.

**확인** — [ ] 내 시스템 프롬프트와 그 답, 세 답의 차이를 적었다.

### 단계 3. 스트리밍 — `ex03_stream.py`

**할 일** — `uv run python ex03_stream.py`를 실행하고 `파이썬 공부 계획을 세 문장으로 알려 줘.`를 입력한다. 답이 끝나면 `반복문을 한 문장으로 설명해 줘.`도 입력하고 `/bye`로 종료한다.

**예상 결과** — `AI>` 뒤로 글자가 조금씩 흘러나오고 답이 끝나면 다시 `나>`가 보인다. 작은 모델이라 중국어 글자나 깨진 글자가 섞이기도 한다.

**확인** — [ ] ex01(다 만든 뒤 한 번에 출력)과 화면에 나오는 방식의 차이를 적었다.

### 단계 4. temperature — `ex04_temperature.py`

**할 일** — `uv run python ex04_temperature.py`를 실행하고 `고양이 이름을 하나만 지어 줘. 이름만 답해.`를 입력한다. 시간이 되면 같은 질문을 한 번 더 입력한 뒤 `/bye`로 종료한다.

**예상 결과** — 질문 하나마다 설정 표시와 `AI>` 답이 네 번 나온 뒤 다시 `나>`가 보인다. `temperature=0` 두 답은 같거나 비슷한 경우가 많고, `temperature=1.0`에서는 더 다양해질 수 있다. 반드시 서로 다른 답이 나오는 것은 아니므로 실제 결과를 기록한다.

**확인** — [ ] 0과 1의 차이를 한 문장으로 적었다.

### 단계 5. 대화 기억 켜기·끄기 — `ex05_memory.py`

**할 일** — `uv run python ex05_memory.py`를 실행하고 `나>`에 차례로 입력한다. 그다음 `request = messages` 줄을 `request = [messages[0], messages[-1]]`로 바꿔 같은 대화를 다시 한다.

```text
수업용 이름은 student01이고 좋아하는 색은 파랑이야.
내가 좋아하는 색은 무엇이야?
/bye
```

**예상 결과** — 켜기: 두 질문 앞에 `(보내는 메시지 2개)`, `(보내는 메시지 4개)`가 나오고 두 번째 답에 파랑이 나온다. 끄기: 두 질문 모두 `(보내는 메시지 2개)`이고 두 번째 답이 파랑을 맞히지 못한다(우연히 맞힐 수도 있다).

**확인** — [ ] 보고서 2절 표에 켜기(4개)·끄기(2개)의 개수와 답을 적었다. "모델이 기억한다"의 실제 뜻(프로그램이 지난 대화를 매번 함께 보낸다)을 한 문장으로 적었다. 실습 30분 뒤 휴식 10분.

## 3교시 — 이미지 인식, 툴 콜링, 내 도우미 모델

### 시작 전 준비

```powershell
Copy-Item -Recurse "$src\period3" "$dst\period3"
Set-Location "$dst\period3"
uv sync
ollama show qwen3.5:2b
```

`Capabilities`에 `vision`과 `tools`가 있는지 확인한다.

### 단계 1. 이미지 인식 — `ex06_vision.py`

**할 일** — `uv run python ex06_vision.py`를 실행하고 `나>`에 `이 화면의 마지막 오류 줄을 그대로 옮겨 적고, 무슨 뜻인지 한국어 한 문장으로 설명해 줘.`를 입력한다. `그 오류를 해결하려면 무엇부터 확인해야 해? 한 문장으로 답해 줘.`라고 이어서 묻고 `/bye`로 종료한다. 그다음 자기 화면 캡처나 사진을 `period3` 폴더에 복사하고, `IMAGE`를 그 파일 이름으로 바꿔 다시 실행해 그림에 맞는 질문을 입력한다. 관찰을 마치면 `/bye`로 종료한다.

**예상 결과** — 예제 그림에서는 오류 줄 `ModuleNotFoundError: No module named 'ollama'`를 글자 그대로 옮기고 뜻을 한 문장으로 설명한다. "어떻게 고치나"를 물으면 엉뚱한 해결책이 나오기도 한다. 내 그림에서도 글자 옮기기는 대체로 맞고, 개수 세기·위치 비교·판단은 틀리거나 그림에 없는 내용을 지어내기도 한다.

**확인** — [ ] 예제 그림과 내 그림(질문 포함)의 결과, "옮기기와 판단 중 어느 쪽이 정확했는가"를 보고서 3절에 적었다.

### 단계 2. 툴 콜링 — `ex07_tools.py`

**할 일** — `uv run python ex07_tools.py`를 실행하고 `나>`에 `지금 몇 시야? 그리고 1234 곱하기 5678은 얼마야?`를 입력한다. 답을 받은 뒤 `그 계산 결과에 2를 곱해 줘.`라고 이어서 묻고 `/bye`로 종료한다.

**예상 결과** — 최종 답 앞에 두 줄이 먼저 나온다.

```text
[함수 실행] get_current_time({}) -> 2026-10-15 02:07
[함수 실행] multiply({'a': 1234, 'b': 5678}) -> 7006652
```

시각은 실행한 때의 값이다. 최종 답은 이 결과를 옮겨 말하는데, 옮기면서 틀리기도 한다(예: 02:07을 "오후 2시"로 말함). 함수 결과가 정답이다. 다음 질문에서는 앞 계산 결과 `7006652`와 `2`로 `multiply`를 부르는지 확인한다. 답이 끝나면 다시 `나>`가 보인다.

**확인** — [ ] 모델이 부른 함수와 값, 함수를 실제로 실행한 쪽(내 Python 프로그램)을 적었다.

### 단계 3. 함수 하나 추가하기

**할 일** — [실습지](lab.md#3교시-실습--이미지-인식-툴-콜링-내-도우미-모델) 문제 4의 `celsius_to_fahrenheit` 함수를 `multiply` 아래에 붙여 넣고 `TOOLS`에 추가한 뒤 실행한다.

```python
TOOLS = {"get_current_time": get_current_time, "multiply": multiply, "celsius_to_fahrenheit": celsius_to_fahrenheit}
```

`나>`에 `섭씨 36.5도는 화씨로 몇 도야?`를 입력하고 결과를 확인한 뒤 `/bye`로 종료한다.

**예상 결과** — `[함수 실행] celsius_to_fahrenheit({'celsius': 36.5}) -> 97.7`이 나오고 최종 답에 97.7이 들어간다(이 Mac에서 5번 중 5번 호출). 함수를 부르지 않고 바로 답하면 질문을 docstring과 더 가깝게 바꾼다.

**확인** — [ ] 새 함수가 불린 `[함수 실행]` 줄과 툴 콜링 세 단계(함수 목록 보내기 → 모델의 호출 요청 → 내 프로그램이 실행하고 결과 돌려주기)를 보고서에 적었다.

### 단계 4. 내 도우미 모델 — `Modelfile`

**할 일** — `Modelfile`의 `SYSTEM` 문장에 팀명을 넣고(예: `너는 'team-a' 팀의 ...`) 실행한다.

```powershell
ollama create student01-helper -f Modelfile
ollama list
ollama run student01-helper --think=false
```

`>>>`에서 질문 하나(예: `너는 누구야? uv가 무엇인지도 알려 줘.`)를 하고 `/bye`로 나온 뒤, 같은 질문을 `ollama run qwen3.5:2b --think=false`에도 한다.

**예상 결과** — `create`가 다운로드 없이 몇 초 만에 `success`로 끝난다. `ollama list`에 `student01-helper:latest`가 보이고 SIZE는 기준 모델과 같다(가중치를 공유한다). 내 모델은 팀의 실습 도우미라고 소개하며 짧게 답하고, 기준 모델은 Qwen이라고 소개하며 길게 답한다. 두 모델 모두 uv를 틀리게 설명할 수 있다. 시스템 프롬프트는 말투·형식을 바꿀 뿐 지식을 채우지 않는다.

**확인** — [ ] 두 모델의 답 비교를 보고서 3절에 적었다. [lab.md](lab.md) 3교시 완료 조건과 제출 체크를 표시했다. 공용 PC는 제출을 마친 뒤 `ollama rm student01-helper`로 지운다(`qwen3.5:2b`는 남는다).

## 문제가 생겼을 때

| 증상 | 할 일 |
|---|---|
| `ollama` 명령을 찾을 수 없다 | PowerShell·VS Code를 완전히 닫고 다시 연다. [설치 안내 9절](windows_setup.md#9-막혔을-때-확인할-것) |
| `Failed to connect to Ollama` | Ollama 앱을 켜고 `ollama list`가 되는지 본다 |
| `model ... not found` | 파일 위 `MODEL`을 `ollama list`의 이름과 똑같이 맞춘다 |
| `No module named 'ollama'` | 예제 폴더에서 `uv sync`를 했는지, `uv run python`으로 실행했는지 본다 |
| `ollama ps`가 비어 있다 | 모델이 내려갔다. `ollama run`을 다시 한 뒤 바로 실행한다 |
| `ollama create`가 다운로드를 시작한다 | `Ctrl+C` 후 `FROM`을 `ollama list`의 이름(`qwen3.5:2b`)으로 고친다 |

세부 판정 기준과 힌트는 [lab.md](lab.md)에 있다.
