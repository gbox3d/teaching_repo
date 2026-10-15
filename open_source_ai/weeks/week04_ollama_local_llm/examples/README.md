# 4주차 예제 — 교시별 폴더

이번 주는 Ollama를 **가져다 쓰는** 주다. 모델 실행은 Ollama 프로그램이, 호출은 공식 Python 라이브러리 [`ollama`](https://github.com/ollama/ollama-python)가 맡는다. 예제 하나는 한 파일에서 핵심 개념 하나를 다룬다.

| 교시 | 폴더 | 하는 일 | 파일 |
|---|---|---|---|
| 1교시 | [period1](period1/README.md) | 터미널에서 모델을 실행하고 숫자 읽기 | 없음 (명령만) |
| 2교시 | [period2](period2/README.md) | Python에서 대화하기 | `ex01` ~ `ex05` |
| 3교시 | [period3](period3/README.md) | 이미지 인식, 툴 콜링, 내 도우미 모델 | `ex06`, `ex07`, `Modelfile` |

## 공통 준비

- [Windows 설치 안내](../windows_setup.md)대로 Ollama를 설치하고 `ollama list`에 `qwen3.5:2b`가 보이는지 확인한다. 모델(약 2.7 GB)은 수업 전에 받아 둔다.
- `qwen3.5:2b`는 글뿐 아니라 그림도 읽고(vision), 함수를 부를 줄 아는(tools) 모델이다. 이번 주 예제는 모두 이 모델 하나로 한다.
- 각 예제 맨 위의 `MODEL = "qwen3.5:2b"`가 사용할 모델이다.
- 예제는 배포 표준 구조다. 예제 하나가 `src/exNN/__init__.py` 패키지 하나이고, `pyproject.toml`의 `[project.scripts]`가 `exNN` 명령을 등록한다. 예제 폴더에서 `uv sync` 한 번, 그다음 `uv run exNN`으로 실행한다. activate는 필요 없다.
- `ex01`은 첫 호출만 확인한다. `ex02`~`ex07`은 `나>`에 직접 질문을 입력하고, 답을 읽은 뒤 다음 질문을 한다. 빈 입력은 건너뛰며 `/bye`로 종료한다.
- `ex02`~`ex04`는 매번 이번 질문만 보낸다. `ex05`에서 대화 이력을 배우고, `ex06`·`ex07`에서 이력을 유지하며 그림·함수 결과에 대해 이어서 묻는다.
