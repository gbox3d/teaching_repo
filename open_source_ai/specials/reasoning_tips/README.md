# 팁엔트릭엔 추론

완성된 응답을 받는 호출에서 시작해 추론 원문과 응답 상태를 확인하고, 생성 중인 추론을 중단·복구하는 방법을 비교한다. Python·LangChain·Ollama로 만든 독립 CLI 복습 자료다. 각 예제의 `main()`에서 입력 반복문, 모델 호출, 출력을 먼저 읽는다.

[한국어 팁 카드](slides.md) · [영어 팁 카드](slides_en.md)

## 실행

Python 3.12와 [uv](../../uv_guide.md)를 준비한다. Ollama를 실행하고 `ollama list`에서 `qwen3.5:2b`를 확인한다. 목록에 없으면 `ollama pull qwen3.5:2b`로 내려받는다. 저장소 루트에서 실행한다.

```powershell
cd open_source_ai/specials/reasoning_tips/examples
uv sync --locked
uv run ex01
```

`나>`에 다음 질문을 입력한다.

> 딸기 3개에서 두 사람이 1개씩 먹으면 몇 개 남나요?

`/bye`로 종료하고 `uv run ex02`, `uv run ex03`을 차례로 실행한다. ex02에서 같은 질문을 다시 보내고, 새 응답의 추론 원문과 본문을 읽는다. 터미널 출력을 바로 보려면 `uv run ex03`부터 실행해도 된다. ex03의 추론은 `추론>` 뒤에 수신한 조각대로 나타나고, 본문이 도착하면 `AI>` 뒤에 답이 한 글자씩 나타난다.

| 명령 | 읽을 코드 | 호출과 이력 |
|---|---|---|
| `uv run ex01` | [ex01_baseline](examples/src/ex01_baseline/__init__.py) | `invoke`로 완성 응답 한 개 수신. 이번 질문만 보낸다 |
| `uv run ex02` | [ex02_observe](examples/src/ex02_observe/__init__.py) | `invoke` 응답의 추론 원문·길이·종료 사유 확인. 이번 질문만 보낸다 |
| `uv run ex03` | [ex03_recover](examples/src/ex03_recover/__init__.py) | 추론 조각 표시·점검·복구. 앞 대화를 함께 보낸다 |

세 예제 모두 입력을 반복하고 `/bye`로 종료한다. `/clear`는 ex03에서 이력을 지운다. ex01·ex02는 질문 이력이 없다는 안내를 출력한다.

`pyproject.toml`의 `[build-system]`은 패키지 설치 도구를, `[project.scripts]`는 명령과 각 `main()`의 연결을 지정한다. 명령 이름이나 진입점을 바꿨다면 `uv sync --locked`를 다시 실행한다. [shared](examples/src/shared/__init__.py)는 모델 생성과 터미널 출력에 쓰는 함수·설정을 제공한다.

## ex01 · main에서 입력하고 완성 응답 받기

`src/ex01_baseline/__init__.py`의 `main()`을 읽는다. 아래는 입력·호출·출력 흐름을 발췌한 코드다. 예제 파일에는 빈 입력, `/clear`, 입력 종료 처리도 있다.

```python
from shared import CHAT_PROMPT, EMPTY_ANSWER, create_model

def main():
    model = create_model()
    while True:
        question = input("나> ").strip()
        if question == "/bye":
            break
        reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
        print("AI>", reply.text if reply.text.strip() else EMPTY_ANSWER)
```

`create_model()`은 공통 설정으로 모델을 만든다. `invoke()`는 생성이 끝난 응답 한 개를 돌려준다. `reply.text`는 본문 문자열이다. 입력할 때마다 현재 질문 한 개만 보내며 중간 조각이나 이전 질문을 다루지 않는다.

기본값 `REASONING=True`로 모델 추론은 켜져 있지만 ex01은 추론 필드를 읽지 않는다. 생성 예산을 추론에 쓰고 본문 없이 끝나면 빈 답변 안내가 나온다. 이것은 `REASONING=False`로 추론을 끄는 것과 다르다.

## ex02 · 완성 응답에서 상태 읽기

`src/ex02_observe/__init__.py`는 같은 입력 반복문에 다음 관찰을 더한다.

```python
reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
thought = reply.additional_kwargs.get("reasoning_content") or ""
done_reason = reply.response_metadata.get("done_reason") or "미제공"
if thought:
    print("추론>", thought)
```

완성 응답을 받은 뒤 추론이 있으면 `추론>` 원문을 먼저 출력한다. 이어서 추론 길이 `len(thought)`, 본문 길이 `len(reply.text)`, `done_reason`을 출력하고, 마지막에 `AI>` 본문 또는 빈 답변 안내를 표시한다. 길이는 공백을 포함한 글자 수다. 한 번의 요청이 끝난 뒤 표시하며 실시간 출력은 아니다. 추론이 비어 있으면 원문 출력을 건너뛴다.

`done_reason=length`는 생성 한도에서 끝났다는 뜻이다. 이것만으로 반복을 판정하지 않는다. 정상 본문이 왔다면 그 결과도 기록한다.

## ex03 · main에서 복구 함수 호출

`src/ex03_recover/__init__.py`도 입력 반복문을 직접 둔다. 이번 입력을 이력에 더한 뒤 일반 함수를 호출한다.

```python
from shared.recovery import answer_with_recovery

answer = answer_with_recovery(model, messages)
```

이 함수는 추론 원문과 본문을 표시하고 최종 본문 문자열을 반환한다. `main()`은 답이 있으면 이력에 남긴다. 사용자 입력과 완료된 답변만 다음 요청에 보내며 추론 원문과 임시 이어쓰기 메시지는 저장하지 않는다.

자세한 처리는 [src/shared/recovery.py](examples/src/shared/recovery.py)에 있다. ex03만 이 파일 안에서 `model.stream()`을 사용한다. 생성 중 추론 한도나 반복을 감지해 첫 요청을 중단하려면 조각을 받는 방식이 필요하다. 조각의 `part.text`가 한 글자나 한 토큰이라는 보장은 없다.

본문 전에 받은 추론은 `추론>` 뒤에 조각 단위로 즉시 출력한다. 추론 출력에는 별도의 타자 지연을 넣지 않는다. 다음 시도에서 추론이 다시 오면 새 `추론>` 표지로 구분한다. 원문은 두 시도가 공유하는 2,048자 한도 안에서 모으고 표시한다.

다음 동작은 `REASONING=True`일 때 적용한다.

| 상태 | 처리 |
|---|---|
| 본문이 이미 시작됨 | 같은 스트림에서 본문을 계속 표시한다 |
| 본문이 없고 추론 글자 수 한도 도달 | 첫 스트림을 닫고 한 번 이어 쓴다 |
| 본문이 없고 20자 이상인 같은 완성 문장이 세 번 나타남 | 첫 스트림을 닫고 한 번 이어 쓴다 |
| 첫 요청이 본문 없이 종료됨 | 추론이 있으면 같은 이력과 이번 추론으로 한 번 이어 쓴다 |
| 본문과 추론이 모두 없음 | 임시 메시지 없이 원래 이력으로 한 번 재요청한다 |
| 두 번째 요청도 본문이 없음 | 빈 답변 안내를 출력하고 끝낸다 |

완성 문장은 문장부호나 줄바꿈으로 끝난 부분이다. 대소문자와 공백을 정리해 반복을 센다. 미완성 조각은 세지 않는다.

이어 쓸 때는 첫 스트림을 `close()`한 뒤 같은 이력에 이번 턴의 추론과 `content="\n"`을 담은 임시 assistant 메시지를 붙인다. 두 요청 모두 추론을 켜고 글자 수 한도를 공유한다. 세 번째 요청은 없다.

이 방식은 Qwen3.5/Ollama에 의존한다. Ollama v0.40.14 [렌더러](https://github.com/ollama/ollama/blob/v0.40.14/model/renderers/qwen35.go#L270-L288)는 추론 종료 표시를 만들고, [파서](https://github.com/ollama/ollama/blob/v0.40.14/model/parsers/qwen35.go#L60-L78)는 비어 있지 않은 assistant 본문 뒤의 출력을 본문으로 처리한다. 여기서는 `"\n"`을 사용한다. 다른 모델·버전에서는 동작을 다시 확인한다.

## 한 글자씩 표시하는 터미널 출력

ex03은 본문 조각이 오면 `shared.type_text()`로 곧바로 표시한다. `examples/` 기준 `src/shared/__init__.py`의 `TYPE_DELAY=0.03`은 글자 사이의 지연 시간(초)이다. 실제 터미널에서는 한 글자씩 출력한다. `0`으로 바꾸면 지연을 끈다. 파일 리다이렉션 등 비TTY 출력도 조각을 지연 없이 출력한다.

타자기 효과는 본문에만 적용하는 터미널 연출이다. 모델의 추론 속도나 토큰 생성 간격을 나타내지 않는다. `추론>` 원문은 조각대로 즉시, `AI>` 본문은 설정한 타자 지연으로 표시한다.

## 설정과 두 가지 예산

경로는 `examples/` 기준이다. 상수를 바꾼 뒤 프로그램을 종료하고 다시 실행한다.

| 설정 | 위치 | 의미 |
|---|---|---|
| `REASONING=True` | `src/shared/__init__.py` | 세 예제에서 모델 추론을 켠다 |
| `NUM_PREDICT=128` | 같은 파일 | 요청당 추론과 본문을 합친 토큰 예산 |
| `TYPE_DELAY=0.03` | 같은 파일 | ex03 본문의 터미널 글자 출력 간격(초) |
| `REASONING_CHAR_LIMIT=2048` | `src/shared/recovery.py` | ex03에서 모으고 표시할 추론 글자 수 한도. 두 요청이 공유한다 |

`create_model()`은 같은 `MODEL`·`HOST`·`temperature=0`과 추론·토큰 설정으로 모델을 만든다. 각 `main()`이 같은 `CHAT_PROMPT`를 시스템 메시지에 넣는다. 기본 모델은 `qwen3.5:2b`이며 주소·모델 변경은 환경 변수 `OLLAMA_HOST`·`OLLAMA_MODEL`로 지정한다.

토큰과 글자는 단위가 다르다. 추론 글자 수 한도는 최종 답변 길이를 제한하지 않는다. 토큰 예산이 작으면 본문 전에 끝나는 경우를 관찰하기 쉽지만, 반드시 그렇게 끝나지는 않는다.

선택 대조로 `REASONING=False`를 설정하면 세 예제 모두 한 번만 요청하며 빈 응답이어도 재요청하지 않는다. 추론을 켠 상태의 복구와 구분해 비교한다.

## 같은 한 문장으로 비교

ex01·ex02에서는 이번 질문만 사용한다. ex03은 새 실행 또는 `/clear`로 이력을 비운 뒤 아래 입력을 한 번 보낸다.

> 딸기 3개에서 두 사람이 1개씩 먹으면 몇 개 남나요?

| 예제 | 적을 내용 |
|---|---|
| ex01 | 완성 본문 또는 빈 답변 안내 |
| ex02 | 완성 응답의 추론 원문·추론 및 본문 글자 수·`done_reason`·답 |
| ex03 | 추론 원문, 복구 안내, 본문 출력 모습, 최종 답 또는 안내 |

모델·시스템 지시·입력·토큰 예산을 유지한다. 정상 응답과 재요청 없음도 관찰이다. 답변 문장이 항상 같다고 가정하지 않는다.

완성 CLI에서 기록한 통계·본문 관찰은 다음과 같다. 조건은 위 단일 입력, 새 실행, Ollama 0.40.16, `qwen3.5:2b`(digest 앞 12자 `0689d44085e0`), `temperature=0`, `NUM_PREDICT=128`, `REASONING=True`다.

| 예제 | 확인한 출력 |
|---|---|
| ex01 | 본문 없이 끝나 빈 답변 안내 출력 |
| ex02 | `추론>` 뒤에 원문 397자 표시 후 `추론 397자 · 본문 0자 · 종료 사유: length` 출력 |
| ex03 | `추론>` 뒤에 원문 397자 표시 후 이어 써 `AI> 남은 딸기는 1 개입니다.` 출력 |

ex03은 Windows 터미널의 `stdout.isatty()=True` 실행에서도 확인했다. 이 표는 해당 조건의 1회 관찰이며 다른 실행이나 모델·버전에서는 다른 결과가 나올 수 있다.

ex03이 재요청하면 요청당 토큰 예산을 한 번 더 받는다. 기본값에서 요청마다 최대 128토큰이므로 ex01·ex02와 총 예산이 같지 않다. 동일 비용의 성능 비교로 해석하지 않는다. 출력 지연을 포함한 터미널 대기 시간도 모델 추론 시간과 다르다.

## ex03의 대화 이력 확인

ex03에서 `/clear`한 뒤 아래 문장을 하나씩 보내고 응답을 기다린다.

1. 딸기가 3개 있습니다.
2. 저와 친구가 1개씩 먹었습니다.
3. 몇 개 남았나요?

마지막 질문에는 수량이 없다. 앞의 수량과 먹은 양을 참조하는지 본다. ex01·ex02는 앞 질문을 보내지 않으므로 이 이력 비교의 대상이 아니다.

## 모의 응답으로 동작 확인

`examples/`에서 전체 시험을 실행한다. 가짜 완성 응답과 스트림 조각으로 분기·이력 보존을 확인하며 Ollama나 모델은 필요 없다.

```powershell
uv run python -B -m unittest discover -s tests -v
```

모의 응답으로 세 예제의 동작을 비교·검증하는 시험만 실행할 수도 있다. 실모델 측정과 구분해서 읽는다.

```powershell
uv run python -B -m unittest discover -s tests -p test_reasoning.py -k test_same_reasoning_only_response_compares_all_three_steps -v
```

## 출처

[참고 구현](https://github.com/althoflee/day_20261119_2_1/blob/5efbfcfb85e330f3e4d2bef18fdb13122e30c00f/src/ex02/readme.md)은 커밋 `5efbfcfb85e330f3e4d2bef18fdb13122e30c00f`를 기준으로 읽는다.

[Qwen3.5-2B 모델 카드](https://huggingface.co/Qwen/Qwen3.5-2B#thinking-mode)는 추론 반복 가능성과 스트리밍 중 감지·중단을 설명한다. 이 예제의 글자 수·반복 횟수는 프로그램이 정한 기준이다.
