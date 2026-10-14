# 4주차 실습 — 오픈소스 모델을 내 PC에서 가져다 쓴다

## 공통 규칙

- 모델은 `qwen3.5:2b` 하나로 한다. 수업 전에 `ollama pull qwen3.5:2b`(약 2.7 GB)로 받아 두고, 실습 중에는 내려받지 않는다.
- 현재 교시의 [예제 폴더](examples/README.md)를 `C:\classwork\week04` 아래에 복사해 그 안에서 실행한다.
- 실행하기 전에 무엇이 나올지 한 줄로 예상하고, 실행한 뒤 실제 결과와 비교한다.
- 관찰은 상위 폴더의 `week04_report.md` 한 파일에 적는다. 처음 한 번만 [보고서 양식](examples/week04_report_template.md)을 복사한다.
- 실명 대신 `student01` 같은 수업용 이름을 쓴다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week04_ollama_local_llm\examples"
$dst = "C:\classwork\week04"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\week04_report.md")) { Copy-Item "$src\week04_report_template.md" "$dst\week04_report.md" }
```

## 1교시 실습 — 터미널에서 모델 실행하고 숫자 읽기

### 상황

방금 받은 오픈소스 모델이 내 PC에서 얼마나 큰지, 얼마나 빠른지, GPU에서 도는지 숫자로 확인한다. 코드는 쓰지 않는다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 예상 | 0–3분 | 파라미터 수, 메모리 크기, tokens/s를 예상해 보고서에 적기 |
| 모델 정보 | 3–10분 | `ollama list`, `ollama show qwen3.5:2b` |
| 대화와 속도 | 10–20분 | `ollama run qwen3.5:2b --think=false`, `/set verbose`, 질문 2개 |
| 메모리 | 20–25분 | `/bye` 직후 `ollama ps` |
| 기록 | 25–30분 | 보고서 1절 채우기 |

### 문제

1. `ollama show qwen3.5:2b`에서 parameters, quantization, context length, Capabilities를 찾아 적는다.
2. `ollama run qwen3.5:2b --think=false`로 들어가 `/set verbose`를 입력하고 다음 두 질문을 한다.
   - `파이썬이 무엇인지 두 문장으로 설명해 줘.`
   - `uv가 무엇인지 두 문장으로 설명해 줘.`
3. 답 아래의 `eval rate`(tokens/s)를 적는다. 두 답의 내용이 맞는지도 한 줄씩 적는다.
4. `/bye`로 나온 직후 `ollama ps`를 실행해 `SIZE`와 `PROCESSOR`를 적는다.

완료 조건:

- [ ] 보고서 1절 표(파라미터 수, 양자화, Capabilities, eval rate, SIZE, PROCESSOR)가 채워졌다.
- [ ] `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다른 이유를 한 문장으로 적었다.

<details>
<summary>힌트</summary>

- `ollama`를 찾을 수 없다고 나오면 [설치 안내 9절](windows_setup.md#9-막혔을-때-확인할-것)을 본다.
- `ollama ps`가 비어 있으면 모델이 메모리에서 내려간 것이다. `ollama run`을 다시 한 뒤 바로 실행한다.
- `ollama ps`의 SIZE에는 가중치에 더해 대화 내용을 담는 공간(컨텍스트)이 들어간다.

</details>

### 확장

- `ollama run`을 끝내고 5분 뒤 `ollama ps`를 다시 실행한다. 목록이 비면 메모리를 비운 것이다.
- `ollama show qwen3.5:2b --license`로 라이선스 이름을 확인하고 보고서에 적는다.

## 2교시 실습 — Python에서 대화하기

### 상황

1교시에 터미널로 한 대화를 Python 프로그램에서 한다. HTTP 요청이나 오류 처리는 직접 만들지 않는다. 공식 라이브러리 `ollama`의 `ollama.chat()`이 해 준다.

### 준비

```powershell
Copy-Item -Recurse "$src\period2" "$dst\period2"
Set-Location "$dst\period2"
uv sync
```

`ex01` 외에는 `나>`에 직접 질문한다. 답을 받은 뒤 다음 질문을 입력하고 `/bye`로 종료한다. `ex02`~`ex04`는 이번 질문만 보내며, `ex05`부터 앞 대화를 함께 보낸다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 첫 질문 | 0–5분 | `ex01_hello.py` 실행, 질문 바꿔 다시 실행 |
| 시스템 프롬프트 | 5–12분 | `ex02_system_prompt.py`에 자기 역할 하나 추가 |
| 스트리밍·temperature | 12–19분 | `ex03_stream.py`, `ex04_temperature.py` |
| 대화 기억 | 19–27분 | `ex05_memory.py` 켜기·끄기 비교 |
| 기록 | 27–30분 | 보고서 2절 |

### 문제

1. `uv run python ex01_hello.py`를 실행한다. 코드에서 `messages`, `response.message.content`가 각각 무엇인지 보고서에 한 줄씩 적는다.
2. `ex02_system_prompt.py`의 `SYSTEMS` 목록에 자기 역할 하나를 추가한다(예: 영어 회화 도우미, 요리 도우미). 실행하고 `나>`에 `리스트가 무엇이야?`를 입력해 세 답이 어떻게 다른지 적는다. 다른 질문도 입력해 본 뒤 `/bye`로 종료한다.
3. `ex03_stream.py`를 실행하고 `파이썬 공부 계획을 세 문장으로 알려 줘.`를 입력한다. 답을 받은 뒤 다른 질문도 입력해 보고, ex01과 화면에 나오는 방식이 어떻게 다른지 적는다. `/bye`로 종료한다.
4. `ex04_temperature.py`를 실행하고 `고양이 이름을 하나만 지어 줘. 이름만 답해.`를 입력한다. temperature 0의 두 답, 1의 두 답이 각각 같은지 적은 뒤 `/bye`로 종료한다.
5. `ex05_memory.py`를 실행하고 다음을 차례로 입력한다.

   ```text
   수업용 이름은 student01이고 좋아하는 색은 파랑이야.
   내가 좋아하는 색은 무엇이야?
   /bye
   ```

6. `request = messages`를 `request = [messages[0], messages[-1]]`(규칙과 이번 질문만)로 바꿔 같은 대화를 다시 한다. "보내는 메시지" 개수와 답을 비교한다.

완료 조건:

- [ ] 직접 만든 시스템 프롬프트 하나와 그 답이 보고서에 있다.
- [ ] temperature 0과 1의 차이를 한 문장으로 적었다.
- [ ] 기억 켜기·끄기의 "보내는 메시지" 개수와 답을 비교표로 적었다.
- [ ] "모델이 기억한다"는 말이 실제로는 무엇을 뜻하는지 한 문장으로 적었다.

<details>
<summary>힌트</summary>

- `No module named 'ollama'`: `python` 대신 `uv run python`으로 실행했는지, 이 폴더에서 `uv sync`를 했는지 본다.
- `Failed to connect to Ollama`: Ollama 앱이 켜져 있는지 `ollama list`로 확인한다.
- 기억 끄기에서도 모델이 우연히 파랑이라고 답할 수 있다. 답만 보지 말고 보낸 메시지 개수와 함께 판단한다.

</details>

### 확장

- `ex01_hello.py` 끝에 `print(response.eval_count, response.eval_duration)`를 추가한다. `eval_count ÷ (eval_duration ÷ 1e9)`가 1교시의 eval rate와 비슷한지 본다.
- `ex05_memory.py`의 시스템 프롬프트를 "항상 존댓말로 한 문장만 답한다."로 바꾸고 대화해 본다.

## 3교시 실습 — 이미지 인식, 툴 콜링, 내 도우미 모델

### 상황

`qwen3.5:2b`는 그림을 읽는 VLM이고, 필요한 순간 Python 함수를 불러 달라고 요청할 줄 안다. 두 기능을 직접 써 보고, 마지막으로 시스템 프롬프트를 넣은 내 도우미 모델을 만든다.

### 준비

```powershell
Copy-Item -Recurse "$src\period3" "$dst\period3"
Set-Location "$dst\period3"
uv sync
ollama show qwen3.5:2b
```

`Capabilities`에 `vision`과 `tools`가 있는지 확인한다.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 이미지 인식 | 0–10분 | `ex06_vision.py`, 자기 화면 캡처로 바꿔 보기 |
| 툴 콜링 | 10–22분 | `ex07_tools.py` 실행, 함수 하나 추가 |
| Modelfile | 22–28분 | `ollama create`, 기준 모델과 비교 |
| 기록 | 28–30분 | 보고서 3절 |

### 문제

1. `uv run python ex06_vision.py`를 실행한다. `나>`에 `이 화면의 마지막 오류 줄을 그대로 옮겨 적고, 무슨 뜻인지 한국어 한 문장으로 설명해 줘.`를 입력한다. `그 오류를 해결하려면 무엇부터 확인해야 해? 한 문장으로 답해 줘.`라고 이어서 묻는다. 오류 줄과 설명이 맞는지 확인한 뒤 `/bye`로 종료한다.
2. `IMAGE`를 자기 화면 캡처나 사진 파일로 바꾸고 다시 실행한다. `나>`에 그림에 맞는 질문을 입력한다. 글자를 옮기는 일과 내용을 판단하는 일 중 어느 쪽이 더 정확했는지 적고 `/bye`로 종료한다.
3. `uv run python ex07_tools.py`를 실행하고 `지금 몇 시야? 그리고 1234 곱하기 5678은 얼마야?`를 입력한다. `그 계산 결과에 2를 곱해 줘.`라고 이어서 묻는다. `[함수 실행]` 줄에서 모델이 어떤 함수를 어떤 값으로 불렀는지, 함수를 실제로 실행한 것은 누구인지 적고 `/bye`로 종료한다.
4. `ex07_tools.py`에 함수를 하나 추가한다.

   ```python
   def celsius_to_fahrenheit(celsius: float) -> float:
       """섭씨 온도를 화씨 온도로 바꾼다.

       Args:
           celsius: 섭씨 온도
       """
       return celsius * 9 / 5 + 32
   ```

   `TOOLS`에 넣고 다시 실행해 `나>`에 `섭씨 36.5도는 화씨로 몇 도야?`를 입력한다. 모델이 새 함수를 불렀는지 확인한 뒤 `/bye`로 종료한다.
5. `Modelfile`의 `SYSTEM`에 자기 팀명 한 줄을 넣고 다음을 실행한다.

   ```powershell
   ollama create student01-helper -f Modelfile
   ollama run student01-helper --think=false
   ```

   같은 질문을 `ollama run qwen3.5:2b --think=false`에도 해서 답을 비교한다.

완료 조건:

- [ ] 예제 그림과 내 그림 각각의 결과를 보고서에 적었다.
- [ ] 툴 콜링의 세 단계(함수 목록 보내기 → 모델의 호출 요청 → 내 프로그램이 실행하고 결과 돌려주기)를 내 말로 적었다.
- [ ] 직접 추가한 함수를 모델이 부른 `[함수 실행]` 줄이 보고서에 있다.
- [ ] `ollama list`에 내 모델이 보이고, 기준 모델과의 답 비교를 적었다.

<details>
<summary>힌트</summary>

- 그림 경로에 한글·공백이 있어 못 찾으면 파일을 `period3` 폴더로 복사해 이름만 쓴다.
- 모델이 함수를 부르지 않고 바로 답하면 질문을 함수 설명(docstring)과 더 가깝게 바꿔 본다. 작은 모델은 함수를 빠뜨리거나 엉뚱한 함수를 부르기도 한다. 숫자를 받는 함수가 글자를 받는 함수보다 잘 맞는다.
- 함수 결과와 최종 답이 다를 수 있다(예: 02:07을 "오후 2시"라고 말함). 함수 결과가 정답이다.
- `ollama create`는 가중치를 복사하지 않는다. `ollama list`에서 크기가 같아도 디스크를 두 배로 쓰지 않는다.

</details>

### 확장

- `ex07_tools.py`에서 `tools=`를 빼고 실행해 `나>`에 `1234 곱하기 5678은?`을 입력한다. 함수 없이 모델이 직접 계산한 답이 맞는지 비교한다.
- 이미지 두 장을 `"images": [...]`에 함께 넣고 "두 그림의 차이를 알려 줘"라고 물어 본다.
- 글자를 정확히 맞춰야 하는 함수를 만들어 본다. 예: `rooms = {"오픈소스 AI 응용": "공학관 301호"}`에서 과목 이름으로 강의실을 찾는 `get_class_room(course: str)`. 모델이 `"오픈소스 AI 응용 수업"`처럼 다른 글자를 넘기면 사전에서 못 찾는다. 작은 모델이 어디서 틀리는지 관찰하고, 함수 쪽에서 어떻게 받아 주면 될지(예: `in`으로 포함 여부 검사) 적는다.

## 제출 체크

- `week04_report.md`: 1~3절이 채워져 있다.
- `period2/ex02_system_prompt.py`: 내가 추가한 역할이 들어 있다.
- `period3/ex07_tools.py`: 내가 추가한 함수가 들어 있다.
- `period3/Modelfile`: 팀명을 넣은 SYSTEM.
- 이 결과를 [1차 종합과제](assignment_brief.md) 저장소에 옮겨 commit한다. `.venv/`는 커밋하지 않는다.
