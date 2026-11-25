# 10주차 실행 예제

전체 `teaching_repo` checkout에서는 이 `examples/`가 실행 위치다. 저장소 없이 시작하려면 [실습 ZIP 설치 안내](../distribution/README.md)를 따라 압축을 푼 `week10-simulator-lab/`을 사용한다. 두 경로의 설치·실행 명령은 같다. `period1`~`period3`은 checkout에서 읽는 안내 README다.

| 교시 | 안내 | 소스 | 실행 |
|---|---|---|---|
| 1 | [Python 수동 명령](period1/README.md) | [ex01_manual](src/ex01_manual/__init__.py) | `uv run ex01` |
| 2 | [Ollama 도구 호출](period2/README.md) | [ex02_tools](src/ex02_tools/__init__.py) | `uv run ex02` |
| 3 | [같은 모델의 고정 평가](period3/README.md) | [ex03_check](src/ex03_check/__init__.py) | `uv run ex03` |

`ex01`은 `on 0`·`off 0`·`pwm 1 128`·`sensor`를 입력하는 수동 명령 대화, `ex02`는 Ollama 자연어 대화, `ex03`은 평가 실행기다. 평가 중 틀린 입력을 직접 다시 넣을 때는 `ex02`로 돌아간다.

## 설치와 실행

```powershell
uv sync --locked
```

Python 3.12를 사용한다. ZIP과 checkout 모두 `pyproject.toml`의 `wleno==0.1.0`을 PyPI에서 설치한다. 첫 설치에는 인터넷 연결이 필요하다. 패키지 하나에 시뮬레이터와 제어 API가 들어 있다. 각 예제의 `main()`을 `[project.scripts]`가 명령으로 연결한다. `[build-system]`의 `uv_build`가 `src/` 패키지를 설치하며 scripts 수정 뒤에는 `uv sync --locked`를 다시 실행한다. 프로젝트 생성 연습은 [실습지](../lab.md)의 수업 전 준비에 있다.

터미널 A를 같은 프로젝트 폴더에서 열어 시뮬레이터를 켜 둔다.

```powershell
uv run wleno --bind 127.0.0.1
```

터미널 B도 같은 폴더에서 열어 `uv run ex01`을 실행한다. 창 없는 검증에는 터미널 A의 명령에 `--no-window`를 추가한다. 대화 예제는 빈 줄을 건너뛰고 `/bye`로 종료한다. ex01은 Ollama 없이 실행하며, ex02·ex03은 Ollama와 `qwen3.5:2b`가 필요하다. 입력 반복과 대화 이력 유지는 구분한다.

## 공용 코드와 평가 자료

각 예제는 `wleno.control`에서 필요한 공용 API를 직접 import한다. `Board`는 연결·제어·상태 읽기, `chat`은 반복 입력, `load_cases`는 고정 평가셋 로드를 담당한다. 주차 [shared](src/shared/__init__.py)에는 모델 이름과 `predict()`만 둔다. 모델 호출은 `wleno.control.models.ollama_predict`, 평가는 `wleno.control.evaluation.evaluate`에서 읽는다. 각 예제끼리 직접 import하지 않는다. 제어 코드의 원본은 [공용 제어 라이브러리](../../../../tools/bleuno-control/src/bleuno_control/__init__.py)에 있다.

새 프로젝트에 패키지만 설치할 때는 `uv add wleno`를 사용한다. 프로젝트 생성부터 실행까지는 [패키지 설치 안내](../distribution/README.md#새-프로젝트에서-패키지만-설치)를 따른다.

공용 [control_cases.json](../../../../tools/bleuno-control/src/bleuno_control/data/control_cases.json)은 한글 8·영어 8, 호출 10·무호출 6의 16문항이다. 예열 1회는 집계에서 제외한다. 문항마다 LED를 `[0, 64, 128, 255]`로 복원하며 모델 추론 시간과 준비 시간을 분리한다. 지표 정의는 [실습지](../lab.md#고정-평가셋과-측정-기준)를 따른다.

ex02는 사용자가 입력한 문장을 모델에 보낸다. ex03은 파일의 `query`만 모델에 보내고 `calls`는 채점할 정답으로 보관한다. 예를 들어 `query`가 `0번 LED를 켜 주세요`이면 기대 호출은 `[{"name": "turn_on", "arguments": {"index": 0}}]`이다. 정답 호출을 모델 입력에 포함하지 않는다.

## 실행 결과 확인

TCP 8266 연결을 유지한 채 HTTP 8080의 `GET /state`를 읽는다. `hello`·이벤트 행은 명령 응답에서 제외한다. 연결·해제는 LED 상태를 유지한다. 제어 전후 상태를 기록한다.

함수는 `turn_on(index)`, `turn_off(index)`, `set_brightness(index, value)`, `read_environment()` 네 개다. 번호 0~3·밝기 0~255의 정수만 허용하고 불리언은 거부한다. 센서 값을 바꾸는 `POST /set`은 모델 도구가 아니다.
