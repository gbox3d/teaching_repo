# 10주차 시뮬레이터 실습 · 0.1.0

Python 수동 명령으로 LED를 제어한 뒤 Ollama의 함수 호출 제안과 실제 상태를 비교하는 예제다. 시뮬레이터와 제어 라이브러리는 `wleno` 0.1.0 패키지 하나로 설치한다.

## 다운로드와 설치

1. [릴리스의 실습 ZIP](https://github.com/gbox3d/teaching_repo/releases/download/wleno-v0.1.0/week10-simulator-lab-0.1.0.zip)을 내려받아 압축을 푼다.
2. `week10-simulator-lab` 폴더를 연다. `pyproject.toml`, `uv.lock`, `src/`, `wheels/`가 보이는 위치다.
3. Python 3.12와 uv를 준비하고 이 폴더의 터미널에서 실행한다.

```powershell
uv sync --locked
```

ZIP의 `wheels/wleno-0.1.0-py3-none-any.whl`을 사용한다. `wheels/`와 프로젝트 파일은 함께 보관한다. 첫 설치 때 Python 3.12가 없거나 빌드 도구 `uv_build`가 캐시에 없으면 uv가 인터넷에서 내려받는다. [uv 설치 안내](https://github.com/gbox3d/teaching_repo/blob/main/open_source_ai/uv_guide.md)

## 터미널 A · 시뮬레이터

`week10-simulator-lab`에서 실행하고 켜 둔다.

```powershell
uv run wleno --bind 127.0.0.1
```

LED·온습도를 표시하는 창이 열린다. Tkinter 창을 사용할 수 없거나 창 없이 실행하려면 다음 명령을 대신 사용한다.

```powershell
uv run wleno --bind 127.0.0.1 --no-window
```

같은 PC에서 TCP `127.0.0.1:8266`으로 제어하고 HTTP `127.0.0.1:8080`으로 상태를 읽는다. 기본 포트가 사용 중이면 먼저 같은 시뮬레이터를 중복 실행했는지 확인한다. 종료는 창 닫기 또는 `Ctrl+C`다.

## 터미널 B · 세 예제

두 번째 터미널도 같은 `week10-simulator-lab` 폴더에서 연다.

```powershell
uv run ex01
```

`on 0`, `pwm 1 128`, `off 0`, `sensor`를 한 줄씩 입력한다. 프로그램의 응답·LED 상태 출력과 시뮬레이터 창을 비교한다. `ex01`에는 Ollama가 필요 없다. 빈 줄은 건너뛰며 `/bye`로 종료한다. 프로그램을 종료해도 시뮬레이터의 LED 상태는 유지된다.

`ex02`·`ex03`에는 실행 중인 Ollama와 `qwen3.5:2b`가 필요하다. `ollama list`로 확인하고, 모델이 없으면 실습 전에 `ollama pull qwen3.5:2b`로 준비한다.

| 명령 | 하는 일 | 입력·종료 |
|---|---|---|
| `uv run ex01` | 수동 명령으로 제어 | `on 0`, `pwm 1 128`, `sensor` 등. `/bye` 종료 |
| `uv run ex02` | 자연어에서 함수 호출을 제안하고 검증 후 실행 | `Turn on LED 0.` 또는 `0번 LED를 켜 줘.`. `/bye` 종료 |
| `uv run ex03` | 고정 16문항의 호출과 실제 상태 평가 | 별도 입력 없이 평가 후 종료 |

ex01을 끝낸 뒤 `uv run ex02`, 이어서 `uv run ex03`을 실행한다. ex02는 사용자가 입력한 문장을 모델에 보낸다. ex03은 정해진 문항의 `query`만 모델에 보내고, `calls`는 채점할 정답으로 보관한다. 틀린 문항을 직접 다시 입력하려면 ex02를 사용한다. 모델의 완료 문장만으로 성공을 판단하지 않고 호출한 함수·인수·실제 상태를 비교한다.

## 읽고 수정할 코드

모든 경로는 압축을 푼 폴더 기준이다.

| 경로 | 역할 |
|---|---|
| `src/ex01_manual/__init__.py` | 수동 입력과 함수 호출 연결 |
| `src/ex02_tools/__init__.py` | 자연어 대화 |
| `src/ex03_check/__init__.py` | 고정 평가 실행 |
| `src/shared/__init__.py` | 모델 이름과 `predict()` |
| `pyproject.toml` | `ex01`~`ex03`의 `main()` 연결과 동봉 wheel 지정 |

제어 API는 `from wleno.control import Board`로 가져온다. 다음은 호출 형식이다. 터미널 A의 시뮬레이터가 실행 중이어야 한다.

```python
from wleno.control import Board

with Board() as board:
    board.execute([{"name": "turn_on", "arguments": {"index": 0}}])
    print(board.state()["leds"])
```

`turn_on`은 모델에 알려 준 도구 이름이며 `Board.turn_on()` 메서드가 아니다. `Board.execute()`가 호출 목록을 검사하고 실행한다. LED 번호는 0~3, 밝기는 0~255의 정수만 허용한다.

## 새 프로젝트에서 패키지만 설치

이 ZIP은 이미 wheel을 지정하므로 위의 `uv sync --locked`만 실행하면 된다. 새 프로젝트를 따로 만들고 PyPI에서 패키지를 설치할 때는 다음과 같이 실행한다.

```powershell
uv init --package --python 3.12 --vcs none my-wleno-lab
cd my-wleno-lab
uv add wleno
```

이 버전의 wheel을 직접 설치하려면 같은 프로젝트에서 다음 명령을 대신 사용한다.

```powershell
uv add https://github.com/gbox3d/teaching_repo/releases/download/wleno-v0.1.0/wleno-0.1.0-py3-none-any.whl
```

설치한 프로젝트에서 `uv run wleno --bind 127.0.0.1`로 실행할 수 있다. `uv add wleno`는 PyPI에 등록된 패키지를 찾고, URL 설치는 지정한 0.1.0 wheel을 가져온다. PyPI에서 찾지 못하면 wheel 설치 경로를 사용한다. `ex01`~`ex03`은 실습 ZIP에 포함된 명령이므로 패키지만 설치한 새 프로젝트에는 생기지 않는다.

## 교재와 도움말

[10주차 교재](https://github.com/gbox3d/teaching_repo/blob/wleno-v0.1.0/open_source_ai/weeks/week10_simulator_control/README.md) · [실습지](https://github.com/gbox3d/teaching_repo/blob/wleno-v0.1.0/open_source_ai/weeks/week10_simulator_control/lab.md) · [시뮬레이터 안내](https://github.com/gbox3d/teaching_repo/blob/wleno-v0.1.0/tools/wleno/README.md)

연결 오류가 나면 터미널 A의 실행 상태를 먼저 확인한다. 설치 오류가 나면 `pyproject.toml`이 있는 폴더인지, `wheels/`가 함께 있는지 확인한다. 모델 호출 오류는 Ollama 실행 상태와 `ollama list`를 확인한다. 시뮬레이터 옵션은 `uv run wleno --help`로 읽는다.
