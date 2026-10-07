# Python으로 Ollama 사용하기 — 질문, 프롬프트, 대화 기억

먼저 [Windows 설치 안내](windows_setup.md)를 따라 `ollama list`에 `qwen3:0.6b`가 보이고 직접 채팅할 수 있는지 확인한다. 이 문서의 명령은 **Windows PowerShell** 기준이다. Ollama 앱을 켜 둔 상태에서 진행한다.

## 1. Python 라이브러리로 첫 답 받기

Ollama 프로그램이 모델을 실행하고, Python 패키지 `ollama`는 그 프로그램에 질문을 보낸다. Python 패키지만 설치하면 모델까지 설치되는 것은 아니다. [공식 Python 라이브러리 안내](https://github.com/ollama/ollama-python)

VS Code에서 교재 폴더를 연다. **터미널 → 새 터미널**을 선택하고 PowerShell인지 확인한다. 아래 첫 줄의 경로는 자신의 교재 위치로 바꾼다.

```powershell
Set-Location "C:\classwork\teaching_repo\open_source_ai\weeks\week04_ollama_local_llm\examples\period2"
uv --version
uv sync
$env:OLLAMA_MODEL = "qwen3:0.6b"
uv run python hello.py
```

`uv sync`는 이 폴더의 `pyproject.toml`을 읽고 `.venv`에 Python 패키지를 설치한다. Python 3.12 이상을 사용하는 예제이며, 해당 버전이 없으면 uv 설정에 따라 Python을 다운로드할 수 있다. `activate`는 필요 없다. 처음 생성한 `uv.lock`은 개인 실습 저장소에 커밋한다. 검증된 lock을 배포받은 경우에는 `uv sync --locked`로 확인한다.

`$env:OLLAMA_MODEL`은 현재 PowerShell에서 실행하는 Python이 사용할 모델을 정한다. 3주차 설정 로더를 재사용하며, 기존 기본값은 `qwen3:8b`이므로 **이 줄을 생략하지 않는다.** 터미널을 새로 열면 다시 지정한다. 계속 사용하려면 `.env.example`을 `.env`로 복사한 뒤 `OLLAMA_MODEL=qwen3:0.6b`로 수정한다.

`hello.py`를 열고 다음 부분을 읽는다.

```python
response = client.chat(
    model=settings.model,
    messages=[{"role": "user", "content": "안녕. 한국어로 한 문장만 인사해 줘."}],
    think=False,
)
print(response.message.content)
```

`model`은 답을 생성할 모델, `messages`는 모델에 보여 줄 대화다. `role`은 누가 말하는지, `content`는 말의 내용이다. 반환된 `response.message.content`가 모델의 답이다. `think=False`는 이번 Qwen3 모델에서 생각 출력 없이 답을 받기 위한 설정이다.

**해 보기:** 질문을 “파이썬으로 할 수 있는 일을 두 가지 알려 줘.”로 바꾸고 다시 실행한다. 화면의 문장이 달라지는지 확인한다. 처음부터 응답 시간·토큰 수를 계산할 필요는 없다.

## 2. 시스템 프롬프트와 사용자 프롬프트 만들기

| 역할 | 의미 | 예 |
|---|---|---|
| `system` | 도우미의 역할과 답변 규칙 | “너는 초보자용 Python 선생님이다. 쉬운 예 하나로 설명한다.” |
| `user` | 사용자가 지금 묻는 질문 | “리스트가 무엇이야?” |
| `assistant` | 모델이 한 답 | “리스트는 여러 값을 순서대로 담는 …” |

시스템 프롬프트에는 **누구인지, 어떻게 답할지**를 적고, 사용자 프롬프트에는 **이번에 부탁할 일**을 적는다. 시스템 프롬프트가 있어도 모델이 규칙을 반드시 지키는 것은 아니다. 실행 결과로 확인한다.

같은 질문으로 답변 규칙만 바꿔 본다.

```powershell
uv run python prompt_chat.py --model qwen3:0.6b --system "너는 초보자용 Python 선생님이다. 한국어로 비유 하나를 들어 두 문장으로 설명한다." --prompt "리스트가 무엇이야?" --output outputs/teacher.json
uv run python prompt_chat.py --model qwen3:0.6b --system "너는 Python 참고서다. 한국어로 짧은 정의와 코드 예 하나를 보여 준다." --prompt "리스트가 무엇이야?" --output outputs/reference.json
```

첫 명령은 `outputs/teacher.json`, 두 번째는 `outputs/reference.json`에 보낸 메시지와 답을 저장한다. VS Code에서 두 파일을 열어 `messages`의 `system`과 `user`, 그리고 `answer`를 비교한다.

**해 보기:** 자신만의 역할 하나를 정한다. 예: 영어 회화 도우미, 요리 도우미, 면접 연습 도우미. 시스템 프롬프트에 역할·말투·답변 길이를 넣고, 그 역할에 맞는 사용자 질문 두 개를 작성한다. 관찰한 답변 차이를 세 문장으로 기록한다.

이 프로그램은 매번 새 메시지 두 개만 보낸다. 첫 실행에서 이름을 알려 줘도 다음 실행에는 그 이름이 전달되지 않는다.

## 3. 이전 대화를 기억하게 만들기

여기서 기억은 **이전 질문과 답을 다음 질문과 함께 다시 보내는 것**이다. 프로그램이 다음 목록을 보관한다.

```text
system: 한국어로 짧게 답한다.
user: 수업용 이름은 student01이고 좋아하는 색은 파랑이야.
assistant: 알겠어요.
user: 내가 좋아하는 색은 무엇이야?
```

모델은 마지막 질문만 보는 것이 아니라 앞서 받은 대화도 함께 읽는다. 모델의 가중치를 학습시켜 바꾸는 작업은 아니다. [Ollama 대화 메시지 API](https://docs.ollama.com/api/chat)

이제 `period3` 폴더로 이동한다.

```powershell
Set-Location ..\period3
uv sync
$env:OLLAMA_MODEL = "qwen3:0.6b"
uv run python memory_chat.py
```

`나>`가 나오면 아래 문장을 차례로 입력한다. PowerShell 명령을 입력하는 곳과 구분한다.

```text
수업용 이름은 student01이고 좋아하는 색은 파랑이야.
내가 좋아하는 색은 무엇이야?
/bye
```

화면에서 “보내는 메시지”가 첫 질문에 2개, 두 번째에 4개로 늘어나는지 확인한다. `outputs/conversation.json`을 열면 `system` → `user` → `assistant` → `user` → `assistant` 순서로 저장되어 있다.

**코드에서 읽을 세 줄:**

```python
request = [*messages, user]
messages.extend([user, {"role": "assistant", "content": answer}])
save_messages(path, messages)
```

첫 줄은 이전 대화와 새 질문을 묶는다. 두 번째는 새 질문과 답을 목록에 더한다. 세 번째는 그 목록을 파일로 저장한다. 실제 코드에는 기억을 끄는 비교 모드도 들어 있다.

## 4. 종료하고 다시 실행해 보기

같은 `period3` 폴더에서 다시 실행한다.

```powershell
uv run python memory_chat.py
```

이번에는 색을 먼저 알려 주지 말고 바로 “내가 좋아하는 색은 무엇이야?”라고 묻는다. 시작할 때 “불러온 대화: 2회”가 표시되는지 보고, 저장 파일의 앞선 내용이 요청에 포함되는지 확인한다.

프로그램이 파일을 읽고 다시 전달하기 때문에 재실행 후에도 대화가 이어진다. **파일에 저장하기만 하고 다음 요청에 넣지 않으면 모델은 그 내용을 보지 못한다.**

대화를 지우고 새로 시작하려면 채팅 안에서 `/reset`을 입력한다. 현재 파일의 기록을 초기화하므로 필요한 증거를 먼저 복사해 둔다. 새로운 파일을 지정해 대화를 분리할 수도 있다.

```powershell
uv run python memory_chat.py --session outputs/new-conversation.json
```

기존 파일이 있으면 그 안에 저장된 시스템 프롬프트를 사용한다. `--system`으로 바꾼 규칙은 새 파일 또는 `/reset` 후에 적용된다.

## 5. 기억을 끄고 비교하기

먼저 `/bye`로 종료하고 다른 파일을 쓰는 비교 모드로 실행한다.

```powershell
uv run python memory_chat.py --no-memory --session outputs/no-memory.json
```

이 모드에서도 대화 기록은 파일에 남지만, 모델에는 **시스템 프롬프트와 이번 질문 두 개만** 보낸다. 같은 순서로 색을 알려 주고 다시 묻는다. 화면의 메시지 수가 계속 2개인지 확인한다.

| 확인 항목 | 기억 켜기 | 기억 끄기 |
|---|---|---|
| 두 번째 질문에 보낸 메시지 수 | 직접 기록 | 직접 기록 |
| 색을 다시 말했는가 | 직접 기록 | 직접 기록 |
| 앞 대화가 요청에 포함되는가 | 코드에서 확인 | 코드에서 확인 |

모델이 우연히 색을 맞히거나, 앞 대화를 받아도 잘못 답할 수 있다. 정답 여부만으로 기억 동작을 판단하지 않는다. **어떤 메시지를 보냈는지**와 함께 확인한다.

대화가 길어지면 모델이 읽을 수 있는 길이를 넘을 수 있다. 이번에는 2~3번의 짧은 대화로 확인한다. 오래된 대화를 줄이거나 요약하는 방법, 문서에서 필요한 내용을 찾는 RAG는 이후에 다룬다.

## 6. 선택: 답을 조금씩 보여 주기

기본 실습을 끝냈으면 `hello.py`를 복사해 `hello_stream.py`로 만들고 호출 부분을 다음처럼 바꿔 본다. 기존 `client`와 `settings`를 만드는 코드는 그대로 둔다.

```python
for part in client.chat(
    model=settings.model,
    messages=[{"role": "user", "content": "파이썬 공부 계획을 세 문장으로 알려 줘."}],
    think=False,
    stream=True,
):
    print(part.message.content or "", end="", flush=True)
print()
```

```powershell
uv run python hello_stream.py
```

`stream=True`는 답이 완성될 때까지 기다렸다가 한 번에 보여 주는 대신, 도착하는 조각을 순서대로 보여 준다. 처음에는 스트리밍 없이 역할과 대화 목록부터 이해한다.

## 막혔을 때

- `No module named 'ollama'`: 해당 예제 폴더에서 `uv sync`를 실행하고 `uv run python ...`으로 실행했는지 확인한다.
- 연결 실패: 시작 메뉴에서 Ollama를 켠 뒤 `ollama list`로 확인한다.
- 모델 없음: `ollama list`에 있는 정확한 이름을 `--model` 또는 `OLLAMA_MODEL`로 지정한다.
- 대화 파일 읽기 실패: JSON을 손으로 수정했다면 형식과 메시지 순서를 확인한다. 원본을 보존하고 `--session`으로 새 파일을 지정할 수 있다.
- `hello.py`는 첫 호출을 읽기 쉽게 보여 주는 최소 예제로 오류 처리 코드가 없다. 상세 오류는 `prompt_chat.py`와 `memory_chat.py`의 안내를 확인한다.

## 이번 실습에서 남길 것

1. 첫 Python 질문과 답.
2. 직접 만든 시스템 프롬프트 하나, 사용자 질문 두 개, 답변 비교.
3. 기억 켜기·끄기 비교표와 재실행 후 대화가 이어진 기록.

실명 대신 `student01` 같은 수업용 이름을 쓴다. 대화 파일은 `outputs/`에 저장되며 Git에서 제외된다. 제출할 때는 개인정보가 없는 짧은 기록만 골라 `evidence/`에 복사한다.

기존 `chat.py`·`stream.py`는 HTTP 요청과 응답 구조를 직접 살펴보는 심화 예제다. Python 라이브러리로 대화할 수 있게 된 뒤 읽는다.
