# 3교시 — 이미지 인식, 툴 콜링, 내 도우미 모델

```powershell
uv sync
ollama show qwen3.5:2b
```

`Capabilities`에 `vision`(그림 읽기)과 `tools`(함수 부르기)가 보이면 이 교시 실습을 모두 이 모델로 할 수 있다.

두 Python 예제 모두 `나>`에 질문을 입력하고 답을 받은 뒤 이어서 질문한다. 빈 입력은 건너뛰고 `/bye`로 종료한다. `ex05`에서 배운 것처럼 질문과 답을 함께 보내 대화 문맥을 유지한다.

## 1. 이미지 인식 — `uv run ex06`

```powershell
uv run ex06
```

첫 질문 메시지에 `"images": [IMAGE]`를 넣어 글과 그림을 함께 보낸다. 다음 질문에도 그 메시지가 포함된 대화 이력을 보낸다. 예제 그림 `src/ex06/error_screen.png`는 `No module named 'ollama'` 오류가 난 터미널 화면이다. 코드가 쓰는 파일은 코드와 함께 `src/` 패키지 안에 두고 `Path(__file__).parent`로 찾는다. 다음처럼 질문하며 모델이 화면의 글자를 읽어 옮기는지 본다.

```text
나> 이 화면의 마지막 오류 줄을 그대로 옮겨 적고, 무슨 뜻인지 한국어 한 문장으로 설명해 줘.
나> 그 오류를 해결하려면 무엇부터 확인해야 해? 한 문장으로 답해 줘.
나> /bye
```

**해 보기:** `/bye`로 종료한 뒤 `src/ex06/__init__.py`의 `IMAGE`를 자기 화면 캡처나 사진으로 바꿔 다시 실행하고, `나>`에 그림에 맞는 질문을 입력한다. 예: 수업 시간표 캡처 → "수요일 수업만 표로 정리해 줘". 글자를 옮기는 일과 내용을 판단하는 일 중 어느 쪽이 더 정확한지 기록한다.

## 2. 툴 콜링 — `uv run ex07`

```powershell
uv run ex07
```

```text
나> 지금 몇 시야? 그리고 1234 곱하기 5678은 얼마야?
나> 그 계산 결과에 2를 곱해 줘.
나> /bye
```

언어 모델은 지금 시각과 오늘 날씨를 모르고 큰 수 계산도 자주 틀린다. 툴 콜링은 이런 일을 **우리 Python 함수에 맡기는** 방법이다.

| 파일 | 하는 일 |
|---|---|
| `src/ex07/tools.py` | 모델에게 맡길 함수 `get_current_time`·`multiply`·`get_weather`와 이름표 `TOOLS` |
| `src/ex07/__init__.py` | 대화 반복과 툴 콜링 세 단계(`main`) |

`get_weather`는 API 키 없이 쓰는 공개 날씨 API [Open-Meteo](https://open-meteo.com)를 `httpx`로 부른다. 인터넷이 필요하다. `전주 날씨 어때?`처럼 물으면 모델이 `get_weather({'city': '전주'})`를 요청한다.

1. `tools=list(TOOLS.values())`로 함수 목록을 보낸다. 라이브러리가 함수 이름·인자 타입·docstring을 읽어 모델에게 설명해 준다.
2. 모델은 답 대신 `tool_calls`(어떤 함수를 어떤 값으로 불러 달라)를 돌려준다. 화면의 `[함수 실행]` 줄이 그것이다.
3. 함수는 **우리 프로그램이** 실행하고 결과를 `role: "tool"` 메시지로 돌려준다. 모델이 그 결과를 보고 최종 답을 만든다.

함수 호출 없이 바로 답한 경우에는 그 답을 출력한다. 호출 요청·함수 결과·최종 답도 이력에 남겨 다음 질문에 함께 보낸다.

함수 결과(`02:07`)와 모델의 최종 답을 비교해 본다. 모델이 결과를 옮기면서 틀릴 수도 있다(예: 02:07을 "오후 2시"로 말함).

**해 보기:** `src/ex07/tools.py`에 함수를 하나 더 만든다. 예: `def celsius_to_fahrenheit(celsius: float) -> float:`(섭씨 → 화씨)를 만들어 `TOOLS`에 넣고 "섭씨 36.5도는 화씨로 몇 도야?"라고 물어 모델이 새 함수를 부르는지 확인한다. 함수 이름·타입·docstring이 모델이 읽는 설명서다. 날씨 결과에 없는 내용(내일 예보 등)을 모델이 덧붙이는지도 본다. 함수 결과에 있는 것만 믿는다.

## 3. 내 도우미 모델 — `Modelfile`

`Modelfile`은 원래 모델(`FROM`)에 시스템 프롬프트(`SYSTEM`)와 옵션(`PARAMETER`)을 붙여 새 이름으로 등록하는 설정 파일이다. 모델을 다시 학습시키지 않는다.

```powershell
ollama create student01-helper -f Modelfile
ollama list
ollama run student01-helper --think=false
```

같은 질문을 `ollama run qwen3.5:2b --think=false`에도 해 보고 답을 비교한다. Python에서 쓰려면 예제의 `MODEL`을 `"student01-helper"`로 바꾸면 된다.

작은 모델은 틀린 답을 자신 있게 하기도 한다(예: Python 도구 uv를 자외선 접착제로 설명). 시스템 프롬프트는 말투와 형식을 바꿀 뿐 모르는 지식을 채워 주지 않는다. 모르는 지식을 채우는 방법(문서 검색, RAG)은 7주차에 다룬다.

**해 보기:** `SYSTEM` 문장을 한 줄 바꾸고 `ollama create`를 다시 실행한 뒤 같은 질문으로 비교한다.
