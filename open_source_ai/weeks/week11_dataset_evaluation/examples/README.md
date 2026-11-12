# 11주차 실행 예제

전체 `teaching_repo`를 clone한 뒤 이 `examples/`에서 세 교시를 이어간다. `examples`만 복사하지 않는다. `period1`~`period3`은 안내 README이며 실행 위치는 여기다.

| 교시 | 안내 | 소스 | 실행 |
|---|---|---|---|
| 1 | [Needle 도구 호출](period1/README.md) | [ex01_needle](src/ex01_needle/__init__.py) | `uv run ex01` |
| 2 | [Ollama·Needle 고정 평가](period2/README.md) | [ex02_compare](src/ex02_compare/__init__.py) | `uv run ex02` |
| 3 | [Needle 도구 설명 변경](period3/README.md) | [ex03_descriptions](src/ex03_descriptions/__init__.py) | `uv run ex03` |

`ex01`과 `ex03`은 Needle 자연어 명령을 반복해서 받는다. `ex02`는 두 모델을 같은 평가셋에서 비교하는 실행기다. `ex03`의 `DESCRIPTIONS`에서 설명만 바꿔 비교한다.

## 설치와 실행

```powershell
uv sync
uv run ex01
```

Python 3.12를 사용한다. 각 패키지의 `main()`을 `[project.scripts]`가 명령으로 연결한다. `[build-system]`의 `uv_build`가 `src/` 패키지를 설치하며 scripts 수정 뒤에는 `uv sync`를 다시 실행한다. 프로젝트 생성 연습은 [실습지](../lab.md)의 수업 전 준비에 있다.

시뮬레이터는 저장소 루트의 별도 터미널에서 켜 둔다.

```powershell
uv run --python 3.12 tools/bleuno-sim/sim.py --bind 127.0.0.1
```

창 없는 검증에는 `--no-window`를 추가한다. 대화 예제는 빈 줄을 건너뛰고 `/bye`로 종료한다. 입력 반복과 대화 이력 유지는 구분한다.

## 공용 코드와 평가 자료

주차 [shared](src/shared/__init__.py)는 공용 [bleuno_control](../../../../tools/bleuno-control/src/bleuno_control/__init__.py)을 import한다. `Board`는 연결·제어·상태 읽기, `chat`은 반복 입력, `load_cases`는 고정 평가셋 로드를 담당한다. 모델 호출은 `models.ollama_predict`·`models.needle_predictor`, 평가는 `evaluation.evaluate`에서 읽는다. 각 예제끼리 직접 import하지 않는다.

`[tool.uv.sources]`의 상대 경로 `../../../../tools/bleuno-control`은 이 프로젝트에서 공용 라이브러리를 찾는 기준이다. 문서 링크의 상대 경로와 설정 파일의 경로를 혼동하지 않는다.

공용 [control_cases.json](../../../../tools/bleuno-control/src/bleuno_control/data/control_cases.json)은 한글 8·영어 8, 호출 10·무호출 6의 16문항이다. 예열 1회는 집계에서 제외한다. 문항마다 LED를 `[0, 64, 128, 255]`로 복원하며 모델 추론 시간과 준비 시간을 분리한다. 지표 정의는 [실습지](../lab.md#고정-평가셋과-측정-기준)를 따른다.

## 실행 결과 확인

TCP 8266 연결을 유지한 채 HTTP 8080의 `GET /state`를 읽는다. `hello`·이벤트 행은 명령 응답에서 제외한다. 연결·해제 때 LED가 초기화되므로 종료 전 상태를 기록한다.

함수는 `turn_on(index)`, `turn_off(index)`, `set_brightness(index, value)`, `read_environment()` 네 개다. 번호 0~3·밝기 0~255의 정수만 허용하고 불리언은 거부한다. 센서 값을 바꾸는 `POST /set`은 모델 도구가 아니다.
