# 5주차 실습 — 로컬 모델과 프롬프트 연결

## 준비

Python 버전과 패키지 구조를 먼저 확인한다.

```powershell
uv init --package --python 3.12 --vcs none week05-skeleton
```

교재의 `examples` 전체를 개인 실습 폴더에 복사하고 그 루트에서 명령을 실행한다. 세 교시는 같은 프로젝트를 이어 쓴다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week05_langchain_basics\examples"
$dst = "C:\classwork\week05"
New-Item -ItemType Directory -Force "C:\classwork" | Out-Null
Copy-Item -Recurse $src $dst
Set-Location $dst
uv sync
ollama list
```

`main()`, `[project.scripts]`, `[build-system]`이 각각 시작 함수·명령 연결·설치 방법이라는 점을 확인한다. scripts를 수정하면 `uv sync`를 다시 실행한다. 패키지는 수업 전에 설치하고 모델은 4주차의 `qwen3.5:2b`를 재사용한다.

## 1교시 실습 — Ollama 연결

| 시간 | 활동 |
|---|---|
| 0–5분 | 프로젝트와 Ollama 준비 확인 |
| 5–15분 | ex01에서 두 질문 입력 |
| 15–25분 | 4주차 호출과 코드 비교 |
| 25–30분 | 빈 입력·종료, 기록 |

1. `uv run ex01`을 실행하고 `리스트가 무엇이야?`, `튜플이 무엇이야?`를 입력한다.
2. 모델에 들어간 system·human 메시지와 응답의 `content`를 찾는다.
3. 4주차 `ollama.chat()`과 이번 `model.invoke()`가 같은 로컬 서버를 사용하는지 [shared](examples/src/shared/__init__.py)의 주소·모델 이름으로 확인한다.
4. 빈 줄을 입력한 뒤 다음 질문을 받는지 확인하고 `/bye`로 종료한다.

완료 조건: 모델 호출 방식과 실제 모델을 구분해 설명하고, 두 번의 입력과 종료를 확인한다.

## 2교시 실습 — 프롬프트 연결

| 시간 | 활동 |
|---|---|
| 0–5분 | 프롬프트와 변수 읽기 |
| 5–15분 | 기본 역할로 질문 두 개 |
| 15–25분 | 역할 한 값 변경 후 비교 |
| 25–30분 | 연결 단계와 결과 기록 |

1. `uv run ex02`에서 `리스트가 무엇이야?`를 입력하고 답을 기록한다. 다른 질문도 입력한 뒤 종료한다.
2. [ex02](examples/src/ex02_prompt/__init__.py)의 `ROLE`을 `비유로 설명하는 Python 선생님`으로 바꿔 같은 질문을 다시 한다.
3. 프롬프트의 `{role}`·`{question}`과 `chain.invoke({...})`의 키를 짝지어 설명한다. `|`는 앞 단계의 출력을 다음 단계에 전달하는 LangChain 연결이다.
4. 프롬프트 → 모델 → 문자열 출력 순서와 역할 변경 전후의 차이를 `week05_note.md`에 적는다. 모델이 규칙을 어긴 경우 실제 답을 기록한다.

완료 조건: 변수 하나를 바꿔 결과를 비교하고 연결의 세 단계를 설명한다. 질문을 반복해도 이 예제는 이전 질문을 보내지 않는다.

## 3교시 실습 — 대화 기억과 스트리밍

| 시간 | 활동 |
|---|---|
| 0–5분 | history와 stream 읽기 |
| 5–15분 | 이름·색을 알려 준 뒤 이어서 질문 |
| 15–25분 | 이력을 보내지 않은 실행과 비교 |
| 25–30분 | 출력 방식과 기억의 원인 기록 |

1. `uv run ex03`을 실행하고 다음을 입력한다.

   ```text
   수업용 이름은 student01이고 좋아하는 색은 파랑이야.
   내가 좋아하는 색은 무엇이야?
   /bye
   ```

2. 답이 조각으로 출력되는지 확인한다. `answer += part`가 전체 답을 모으고 `history.extend(...)`가 질문과 완성 답을 보존하는 이유를 설명한다.
3. 코드의 `"history": history`를 `"history": []`로 바꿔 같은 순서를 다시 실행한다. 답이 우연히 맞아도 이력을 기억한 증거로 보지 않는다.
4. 새로 실행하면 `history = []`에서 시작한다. 디스크 저장과 자동 장기 기억은 이 예제에 없다는 점을 적는다.
5. 종료 후 원래 코드로 복원하고 `week05_note.md`에 두 실행의 차이를 기록한다.

완료 조건: 대화를 이어서 묻고, 이력 전달 여부와 답의 차이를 설명한다.

선택 확장: `MessagesPlaceholder("history")` 앞의 system 문장을 바꿔 말투를 비교한다. 다음 주에는 `context`에 검색 문서를 넣는다.
