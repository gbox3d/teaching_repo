# 5주차 실행 예제

한 uv 프로젝트에서 세 명령을 실행한다. 명령은 복사한 `examples` 루트에서 실행하고, `period1`~`period3` README는 현재 교시의 소스를 안내한다.

| 교시 | 안내 | 소스 | 실행 |
|---|---|---|---|
| 1 | [Ollama 연결](period1/README.md) | [ex01_chat](src/ex01_chat/__init__.py) | `uv run ex01` |
| 2 | [프롬프트 연결](period2/README.md) | [ex02_prompt](src/ex02_prompt/__init__.py) | `uv run ex02` |
| 3 | [기억·스트리밍](period3/README.md) | [ex03_memory_stream](src/ex03_memory_stream/__init__.py) | `uv run ex03` |

모델 설정과 생성 함수는 [shared](src/shared/__init__.py)에 모으고 `from shared import create_model`로 가져온다. 각 예제의 `main()`을 scripts가 명령으로 연결하며 `uv_build`가 패키지를 설치한다. scripts 수정 뒤에는 `uv sync`를 다시 실행한다.

## 수업 전 준비

```powershell
ollama list
uv sync
```

`qwen3.5:2b`가 없다면 수업 전에 다운로드한다. 수업 중에는 4주차 모델을 재사용한다. 모델을 바꾸면 해당 모델에서 생각 출력 비활성화가 지원되는지 확인한다. 예제는 `reasoning=False`로 생각 출력을 끈다.

## 입력

```text
나> 파이썬 리스트를 한 문장으로 설명해 줘.
AI> ...
나> 파이썬 튜플을 한 문장으로 설명해 줘.
AI> ...
나> /bye
```

빈 입력은 요청하지 않는다. `ex01`·`ex02`는 독립 질문을 반복하고 `ex03`만 이전 대화까지 보낸다. 연결 실패는 Ollama 실행 상태와 `OLLAMA_HOST`를, 모델 오류는 `ollama list`와 `OLLAMA_MODEL`을 확인한다.
