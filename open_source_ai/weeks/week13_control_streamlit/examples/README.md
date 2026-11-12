# 13주차 예제: 한 프로젝트에서 평가·수정 대화·UI 실행

`examples/`에 Python 3.12 uv 프로젝트 하나를 둔다. `period1/`~`period3/`은 교시별 안내이며 실행 폴더가 아니다. 앞 교시의 코드와 모델 경로를 그대로 이어 쓴다.

| 교시 | 명령 | 내용 | 안내 |
|---|---|---|---|
| 1교시 | `uv run ex01` | [ex01_evaluate](src/ex01_evaluate/__init__.py)의 16문항 자동 평가 | [period1](period1/README.md) |
| 2교시 | `uv run ex02` | [ex02_improve](src/ex02_improve/__init__.py)의 독립 요청 대화 | [period2](period2/README.md) |
| 3교시 | `uv run ex03` | [ex03_app](src/ex03_app/__init__.py)에서 [app.py](src/ex03_app/app.py) 시작 | [period3](period3/README.md) |

## 실행 위치와 의존성

실제 수업은 `teaching_repo` 전체 clone을 사용한다. `tools/bleuno-control`의 로컬 의존성 때문에 주차 폴더만 복사하면 실행 환경이 완성되지 않는다.

```sh
# teaching_repo 루트에서
cd open_source_ai/weeks/week13_control_streamlit/examples
uv sync
uv run ex01
```

2·3교시에도 같은 위치에서 각각 `uv run ex02`, `uv run ex03`를 실행한다. Cactus는 수업에서 고정한 `cactus-compute==4.2.0` 계열과 12주차에서 저장한 호환 `.cact`를 사용한다. 엔진·기본 모델·패키지는 수업 전에 준비한다. 재학습이 필요하면 12주차의 `cactus-compute[train]==4.2.0` 환경과 학습 절차로 돌아간다.

## 패키지 구조 읽기

각 예제는 `src/` 아래 패키지 하나이며 `__init__.py`의 `main()`이 진입점이다. `pyproject.toml`의 `[project.scripts]`가 `ex01`·`ex02`·`ex03`를 각 패키지의 `main`에 연결한다. `[build-system]`의 `uv_build`는 그 패키지를 설치 가능한 형태로 빌드한다. `[tool.uv.build-backend] module-name`에는 `ex01_evaluate`, `ex02_improve`, `ex03_app`, `shared`가 들어 있다.

`main()`은 실행 순서의 시작이고 scripts는 짧은 명령과 함수 사이의 연결이다. scripts를 바꾼 뒤에는 `uv sync`로 설치된 진입점을 갱신한다. 값을 바꿀 때는 해당 모듈 위의 대문자 상수를 수정한 뒤 같은 명령을 다시 실행한다. 공용 연결·검증·평가 기능은 [`tools/bleuno-control/src/bleuno_control`](../../../../tools/bleuno-control/src/bleuno_control/__init__.py)에서 가져온다. 로컬 의존성 프로젝트는 `tools/bleuno-control`이다. 예제 패키지끼리 직접 import하지 않는다.

구조 생성 연습은 [실습지의 별도 경로](../lab.md#별도-경로에서-패키지-구조-확인)에서 한 번만 한다. 그 연습용 프로젝트를 배포 예제로 덮어쓰거나 교시마다 새 프로젝트를 만들지 않는다.

## 입출력과 연결 수명

`ex01`은 16문항을 순차 자동 평가하고 `ex02`가 터미널 대화를 제공한다. `ex02`는 빈 입력은 건너뛰고 `/bye`로 종료한다. 현재 predictor는 요청마다 `reset()`하므로 모두 독립 요청이다. 반복 입력은 문맥 유지나 가중치 학습을 뜻하지 않는다. “그 LED”처럼 대상이 빠진 요청은 이전 문맥에서 추측하지 않는다.

TCP 연결은 대화 동안 유지한다. 호출 목록의 함수 이름·인자 이름·정수 타입·범위를 모두 검사한 뒤 실행한다. 같은 비교에서는 초기 LED `[0, 64, 128, 255]`를 매 문항 다시 맞추고 `GET /state`로 확인한다. 센서값은 함수 반환에서 읽는다. 종료할 때 연결을 해제하고 LED 초기화를 확인한다.

Streamlit에서는 모델 준비에 `st.cache_resource`를 사용하고, TCP 연결은 각 세션에 둔다. 공용 predictor는 `Lock` 안에서 `reset()`과 `complete()`를 함께 처리한다. 한 PC의 제어 창은 하나만 사용한다. 화면 재실행만으로 새 연결이나 같은 호출이 생기면 수정이 필요하다. 종료는 명시적인 연결 해제로 확인한다.

## 모델·데이터와 화면 실행

[shared/__init__.py](src/shared/__init__.py)의 `MODELS_DIR`은 12주차 `examples/models/`다. `baseline.cact`·`tuned.cact`는 복사 없이 읽는다. 기본 모델은 B=0인 `baseline_adapter.safetensors`로 변화 없이 내보낸 4bit·20층이며 학습 모델도 4bit·20층이다.
12주차 학습·저장이 중단된 상태라면 평가와 앱 실행을 막는다. 이전 파일이 남아 있어도 학습을 완료한 결과로 사용하지 않는다. 12주차에서 오류 원인을 고친 뒤 `uv run ex02`를 다시 실행한다.

평가 데이터는 공용 [control_cases.json](../../../../tools/bleuno-control/src/bleuno_control/data/control_cases.json) 16문항이다. 한국어 8·영어 8, 호출 10·무호출 6이며 학습 48문장과 정확 문자열 중복은 없다. 의미 독립성까지 보장하지는 않는다. 함수 정확도, 호출 완전일치, 실제 제어 성공, 무호출 문항의 오호출률, median·p95를 읽는다. 정의와 제공 실측은 [주차 안내](../README.md#수업-준비-환경의-단일-실측), 판정은 [실습지](../lab.md)를 따른다.

`ex02_improve`의 `DESCRIPTIONS = {}`로 설명을 바꾸는 실험은 LoRA 전후 비교와 별개다. UI는 공용 기본 설명을 사용한다. `uv run ex03` 뒤 `http://127.0.0.1:8501`을 직접 열고 “시뮬레이터 연결”, “제어 요청”, “요청 실행”, “연결 해제” 순서로 조작한다. 같은 경로의 모델을 다시 학습했다면 서버를 재시작한다.

시뮬레이터의 기본 주소는 TCP `127.0.0.1:8266`, HTTP `http://127.0.0.1:8080`이다. 연결 오류는 시뮬레이터와 [Board](../../../../tools/bleuno-control/src/bleuno_control/__init__.py)의 주소, 모델 파일 오류는 12주차 `models/`를 확인한다. 실행 기록은 자신이 확인한 결과만 쓴다.

## 참고

[주차 안내](../README.md) · [실습지](../lab.md) · [따라하기](../walkthrough.md) · [uv 공통 가이드](../../../uv_guide.md)

공식 API는 [Needle Python Docs](https://cactuscompute.com/blog/needle-python-docs), 학습·내보내기는 [Fine-tuning Needle](https://cactuscompute.com/blog/finetuning-needle)을 참고한다.

## 재학습 후 앱 재시작

12주차에서 같은 `tuned.cact` 경로를 재학습해 덮어썼다면, 화면에서 연결을 해제하고 앱 서버 터미널에서 `Ctrl+C`를 누른 뒤 `uv run ex03`로 다시 시작한다. 브라우저 새로고침만으로 캐시된 가중치는 갱신되지 않는다.
