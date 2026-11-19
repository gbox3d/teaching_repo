# 12주차 1교시 데이터 점검과 Needle 대화

[실습지](../../lab.md) · [예제 전체 안내](../README.md) · [따라하기](../../walkthrough.md)

## 실행 위치와 소스

전체 저장소를 clone한 뒤 `open_source_ai/weeks/week12_control_lora/examples`에서 실행한다. 이 `period1/`은 안내 폴더이며 별도 프로젝트가 아니다. Python 3.12, 수업 전 준비한 의존성·엔진·기본 모델을 사용한다.

같은 `examples/` 위치의 다른 터미널에서 WlEno를 먼저 시작한다. WlEno는 Python 표준 라이브러리만 사용하며 uv 환경을 만들지 않는다.

```powershell
python ../../../../tools/wleno/main.py
```

TCP `127.0.0.1:8266`과 HTTP `http://127.0.0.1:8080`이 준비되면 AI 예제 터미널에서 다음 명령을 실행한다. 연결 확인은 [WlEno REST Client 안내](../../../../../tools/wleno/examples/README.md)의 `01_connection/requests.http`를 따른다. `GET /state`의 `leds`와 센서값을 대화 출력과 대조한다.

```powershell
uv sync
uv run ex01
```

`[project.scripts]`의 `ex01_data:main`과 [src/ex01_data/__init__.py](../src/ex01_data/__init__.py)를 읽는다. 학습 원본은 [src/shared/data/train_examples.jsonl](../src/shared/data/train_examples.jsonl)의 48행이다. 원본에는 `query`·`answers`·`reasoning`을 두며 공용 도구 스키마는 학습 입력을 만들 때 합친다.

## 실습 순서

30분의 세부 시간은 [실습지](../../lab.md)가 정본이다.

| 순서 | 읽거나 실행할 것 | 확인할 근거 |
|---|---|---|
| 데이터 점검 | 명령·도구 정의·정답 호출 | 함수·인자·범위와 명령 속 근거 |
| 수정 | 학습용 데이터, 미학습 비교 문항 분리 | 수정 전후와 수정 이유 |
| 대화 | `uv run ex01` | 입력·호출 제안·다음 입력 |
| 문맥·종료 | 독립 명령, 앞 LED를 가리킨 명령 | 이력 초기화, 빈 입력 건너뛰기, `/bye` 종료 |

함수는 `turn_on(index)`, `turn_off(index)`, `set_brightness(index, value)`, `read_environment()`다. `index`는 정수 0~3, `value`는 정수 0~255다. 도구와 무관한 명령은 빈 호출로 다룬다. 인자 값을 추측해 채우지 않는다.

입력 반복은 문맥 유지를 보장하지 않는다. 제공 예제는 모델을 재사용하되 질문마다 이력을 초기화한다. “그 LED”만으로 이전 대상을 기억한다고 가정하지 않고 번호를 다시 적는다. 실제 실행은 허용 목록·인자 검사 뒤 진행하고 `GET /state`를 확인한다. 센서값은 함수 반환에서 읽는다. TCP 연결은 대화 동안 유지하며 해제해도 LED 상태는 유지된다.

잘못된 호출은 오류를 표시하고 다음 입력을 받는다. WlEno 연결이 끊기면 대화를 종료하므로 시뮬레이터가 실행 중인지 확인한 뒤 `uv run ex01`을 다시 실행한다. WlEno를 계속 실행한 상태에서 AI 예제만 재시작하면 기존 LED·센서 상태로 이어진다.

## 다음 교시에 넘길 내용

수정한 학습 데이터, 수정 이유, 기본 모델의 실제 호출 관찰과 질문을 보존한다. 3교시 비교 문항은 학습에 넣지 않는다. 2교시에도 같은 `examples/`에서 `uv run ex02`를 실행한다. 명령·모델이 준비되지 않았다면 막힌 단계와 오류를 남기고 대화 완료로 표시하지 않는다.
