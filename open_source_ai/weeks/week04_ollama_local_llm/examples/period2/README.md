# 2교시 — Python에서 대화하기

Ollama 프로그램이 모델을 돌리고, `ollama` 라이브러리가 Python에서 질문을 보낸다. 요청 만들기·오류 처리는 라이브러리가 해 주므로 우리는 `ollama.chat()` 한 줄을 쓴다.

```powershell
uv sync
uv run ex01
```

`ex01`은 답 한 번을 출력하고 끝난다. `ex02`~`ex05`는 `나>`에서 질문을 받고 답한 뒤 다시 입력을 기다린다. 빈 줄은 건너뛰고 `/bye`를 입력하면 끝난다.

```text
나> 리스트가 무엇이야?
AI> ...
나> 리스트와 튜플의 차이를 한 문장으로 알려 줘.
AI> ...
나> /bye
```

`ex02`~`ex04`는 이번 질문만 보내는 입력 반복 예제다. `ex02`는 질문 하나에 역할별로 답하고, `ex04`는 설정별로 두 번씩 답한다. **입력을 반복하는 것과 앞 대화를 기억하는 것은 다르다.** 앞의 질문과 답까지 보내는 방법은 `ex05`에서 배운다.

| 예제 | 배우는 것 | 해 보기 |
|---|---|---|
| `uv run ex01` | `ollama.chat()`으로 질문하고 `response.message.content`로 답 읽기 | 질문 문장을 바꿔 다시 실행 |
| `uv run ex02` | `system`(역할·규칙)과 `user`(이번 질문)의 차이 | `SYSTEMS`에 자기 역할 하나 추가하고 `나>`에서 같은 질문의 역할별 답 비교 |
| `uv run ex03` | `stream=True`로 답을 조각으로 받기 | 질문을 두 번 입력해 출력 방식을 보고 ex01과 비교 |
| `uv run ex04` | `options={"temperature": ...}`로 답의 다양성 조절 | `고양이 이름을 하나만 지어 줘. 이름만 답해.` 입력 후 0일 때 두 답, 1일 때 두 답 비교 |
| `uv run ex05` | 앞의 질문과 답을 `messages`에 쌓아 함께 보내는 것이 "기억" | 아래 순서로 대화하고, 기억을 끈 채 다시 해 보기 |

## 처음부터 만들어 보기 — `uv init`

이 폴더를 쓰기 전에 같은 구조를 직접 만들어 본다. `--python 3.12`가 사용할 Python 버전을 정하고, `--package`가 아래의 배포 표준 구조를 만든다.

```powershell
uv init --package --python 3.12 --vcs none my-ollama
Set-Location my-ollama
uv add ollama
uv run my-ollama        # Hello from my-ollama!
```

생긴 `.python-version`·`pyproject.toml`·`src/my_ollama/__init__.py`를 이 폴더의 파일과 비교한다. `src/my_ollama/__init__.py`의 `main()` 안에 `ex01`의 코드를 옮겨 넣으면 내 프로젝트에서도 같은 질문을 할 수 있다.

## 예제 구조 — 배포 표준

이 폴더는 PyPI에 올라가는 오픈소스 Python 패키지와 같은 구조다.

```text
period2/
  pyproject.toml          프로젝트 이름·의존성·명령 등록
  src/ex01/__init__.py    예제 하나 = 패키지 하나, 안에 def main()
  src/ex02/__init__.py
  ...
```

`pyproject.toml`에서 세 부분을 읽는다.

| 부분 | 뜻 |
|---|---|
| `[project.scripts]`의 `ex01 = "ex01:main"` | `uv run ex01` 명령을 만들고, 실행하면 `ex01` 패키지의 `main()`을 부른다 |
| `[build-system]`의 `uv_build` | 이 프로젝트를 패키지로 빌드·설치하는 도구. 없으면 명령이 만들어지지 않는다 |
| `[tool.uv.build-backend]`의 `module-name` | `src/` 아래 패키지 이름 목록. 프로젝트 이름(`osa-week04-period2`)과 다르므로 적는다 |

`uv sync`가 이 프로젝트를 `.venv`에 설치하면서 `.venv\Scripts\ex01.exe`(macOS·Linux는 `.venv/bin/ex01`)를 만든다. 그 안에서 하는 일은 `from ex01 import main; main()`이다. 그래서 `main`이 없으면 명령이 실패하고, `[project.scripts]`를 고치면 프로젝트를 다시 설치해야 새 명령이 생긴다. `uv sync`가 그 일을 하고, `uv run`도 실행 전에 바뀐 것을 확인해 자동으로 다시 설치한다. `ruff`·`black`처럼 설치해서 쓰는 오픈소스 명령도 같은 방식으로 만들어진다.

## ex05 대화 기억

모델은 앞의 대화를 스스로 기억하지 않는다. `나>`에 차례로 입력한다.

```text
수업용 이름은 student01이고 좋아하는 색은 파랑이야.
내가 좋아하는 색은 무엇이야?
/bye
```

"보내는 메시지" 개수가 2개 → 4개로 느는 것을 본다. 그다음 `request = messages` 줄을 `request = [messages[0], messages[-1]]`(규칙과 이번 질문만)로 바꿔 같은 대화를 다시 한다. 대화는 계속 `messages`에 쌓이지만 모델에게는 두 개만 간다. 색을 기억하는지 비교한다.

## 안 될 때

- `Failed to connect to Ollama`: Ollama 앱을 켜고 `ollama list`가 되는지 확인한다.
- `model ... not found`: `src/exNN/__init__.py` 위의 `MODEL`을 `ollama list`에 보이는 이름과 똑같이 맞춘다.
- `No module named 'ollama'`: 이 폴더에서 `uv sync`를 했는지, `python 파일` 대신 `uv run ex01`처럼 명령으로 실행했는지 확인한다.
- `Failed to spawn: ex01`: 명령이 아직 없다. `pyproject.toml`의 `[project.scripts]`·`[build-system]`을 확인하고 `uv sync`를 다시 한다.
