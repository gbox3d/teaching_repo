# 10주차 · Python 함수와 Ollama 도구 호출

9주차에는 모델의 답을 앱 화면에 표시했다. 이번 주에는 Python 함수로 시뮬레이터의 LED를 제어한 뒤, 모델이 고른 함수와 인수를 검사해 같은 함수를 실행한다. 마지막에는 같은 입력을 반복해 호출 선택과 실제 상태를 따로 확인한다.

## 목표와 교시별 결과

| 교시 | 설명·시연 20분 | 실습 30분 | 실행 |
|---|---|---|---|
| 1 | 제어 함수 분리, 연결 유지, 상태 읽기 | 수동 명령으로 LED·온습도 확인 | `uv run ex01` |
| 2 | Ollama의 호출 제안과 Python 검증 | 자연어 입력 뒤 호출·실제 상태 대조 | `uv run ex02` |
| 3 | 같은 입력의 반복 검사와 실패 분류 | 고정 평가셋 실행과 틀린 문항 재현 | `uv run ex03` |

각 교시는 설명·시연 20분, 실습 30분, 휴식 10분이다. `ex03`은 테스트 실행기다. 직접 대화할 때는 `ex02`를 사용한다. 모델은 세부 제어를 직접 실행하지 않고 호출할 함수와 인수를 제안한다.

## 준비와 프로젝트 구조

Python 3.12, uv, Ollama와 `qwen3.5:2b`를 수업 전에 준비한다. [실습지](lab.md)의 프로젝트 생성 연습을 마친 뒤 `teaching_repo` 전체를 clone한 경로에서 실습한다. `examples`만 복사하면 상대 경로로 참조하는 공용 라이브러리가 빠진다.

한 주차의 `examples/`가 uv 프로젝트 하나다. 각 예제는 `src/`의 패키지이며 `main()`에서 시작한다. `[project.scripts]`는 `ex01`~`ex03` 명령과 함수를 연결하고, `[build-system]`의 `uv_build`는 패키지를 설치한다. scripts를 바꾸면 `uv sync`를 다시 실행한다. `period1`~`period3`에는 실행 순서를 안내하는 README만 둔다.

주차 `shared`는 저장소의 `tools/bleuno-control`에 있는 `bleuno_control`을 import한다. 이 의존성은 `[tool.uv.sources]`의 상대 path로 연결한다. TCP 통신 코드를 각 예제에 복사하지 않고, 모델·도구 설명처럼 비교할 값은 해당 소스의 상수에서 바꾼다.

## 시뮬레이터와 제어 범위

저장소 루트의 별도 터미널에서 실행한다.

```powershell
uv run --python 3.12 tools/bleuno-sim/sim.py --bind 127.0.0.1
```

창 없는 검증에는 같은 명령 끝에 `--no-window`를 붙인다. 명령은 TCP 8266, 실제 상태 조회는 HTTP 8080의 `GET /state`를 사용한다. 브라우저에서 `http://127.0.0.1:8080/state`를 열어 새로 고침할 수 있다.

| Python 함수 | 허용 입력 | 확인할 결과 |
|---|---|---|
| `turn_on(index)` | LED 번호 정수 0~3 | 해당 LED 밝기 255 |
| `turn_off(index)` | LED 번호 정수 0~3 | 해당 LED 밝기 0 |
| `set_brightness(index, value)` | 번호 0~3, 밝기 정수 0~255 | 해당 LED의 요청한 밝기 |
| `read_environment()` | 인수 없음 | 현재 온도·습도 |

번호와 밝기에 `True`·`False`를 허용하지 않는다. 모델에는 위 네 함수만 제공하며 센서 값을 바꾸는 `POST /set`을 제공하지 않는다. 온습도는 시뮬레이터의 모의 값이다.

연결 직후에는 `hello` 이벤트가 먼저 오며, 이후에도 이벤트 행이 명령 응답 사이에 들어올 수 있다. 라이브러리는 이벤트를 건너뛰고 명령 응답을 읽는다. TCP 연결을 유지한 상태에서 결과를 확인한다. 새 연결과 연결 종료는 LED를 초기화하므로, 종료 뒤의 상태를 명령 실패의 증거로 쓰지 않는다.

모델에 선언한 함수 이름은 호출 규약이다. 실제 실행은 공용 `Board.execute()`가 이름·인수를 검증한 뒤 TCP 명령으로 바꾼다. `tools.json`의 같은 명세를 두 모델이 사용한다.

## 자료와 완료 기준

[한국어 슬라이드](slides.md) · [English slides](slides_en.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제](examples/README.md)

- [ ] 수동 입력과 모델 입력이 같은 제어 함수를 사용하는 이유를 설명했다.
- [ ] 모델의 함수 이름·인수와 Python 검증 결과를 구분했다.
- [ ] 연결을 유지하며 `GET /state`의 LED 값과 온습도를 대조했다.
- [ ] 범위 밖 번호·밝기와 불리언을 거부하는 이유를 설명했다.
- [ ] 같은 평가셋의 성공·실패와 실제 측정 시간을 기록했다.
- [ ] 틀린 입력을 `ex02`에서 재현하고 원인과 다음 확인 방법을 적었다.

실측 전에는 정확도·속도를 예상 숫자로 채우지 않는다. 다음 주에는 같은 제어 함수와 평가 입력으로 [Needle3](../week11_dataset_evaluation/README.md)를 비교한다.

## 참고 자료

[Ollama 도구 호출](https://docs.ollama.com/capabilities/tool-calling) · [시뮬레이터](../../../tools/bleuno-sim/README.md)
