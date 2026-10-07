# Windows에서 Ollama 설치하고 첫 대화하기

**처음 사용하는 학생은 이 문서부터 시작한다.** Windows 10 22H2 이상 또는 Windows 11에서, 설치 파일을 이용해 로컬 모델을 실행하는 절차다. 설치 화면은 버전에 따라 조금 달라질 수 있다. 공식 확인일: 2026-10-08.

## 1. 무엇을 설치하는가

Ollama는 내 PC에서 언어 모델을 실행하는 프로그램이다. 설치한 뒤 모델을 내려받으면 터미널에서 질문하고 답을 받을 수 있다. 나중에는 Python 프로그램에서도 같은 모델을 호출한다.

| 준비할 것 | 하는 일 | 이번에 필요한 시점 |
|---|---|---|
| Ollama Windows 프로그램 | 모델을 불러와 답을 생성한다 | 첫 채팅부터 |
| 모델 `qwen3:0.6b` | 실제 답을 만드는 모델 파일 | 첫 채팅부터 |
| uv와 Python | Python 예제를 실행한다 | 2교시부터 |
| Python 패키지 `ollama` | Python 코드에서 Ollama에 질문한다 | 2교시부터 |

**Ollama 프로그램 설치와 Python 패키지 설치는 별개의 작업이다.** `uv add ollama`만 실행하면 모델 실행 프로그램이 설치되는 것은 아니다. 로컬 실습에는 계정 가입이나 API 키가 필요 없다.

기본 실습은 작은 모델 하나로 시작한다. GPU가 없어도 CPU로 실행할 수 있지만 답이 느릴 수 있다. NVIDIA GPU가 있는 PC는 드라이버를 먼저 확인한다. 지원 조건은 [공식 Windows 문서](https://docs.ollama.com/windows)에서 확인한다.

## 2. 설치 전에 확인하기

1. `Win + I`로 Windows 설정을 열고 **시스템 → 정보**에서 Windows 버전을 확인한다.
2. 파일 탐색기에서 **내 PC**를 열고 C: 드라이브의 여유 공간을 확인한다. 공식 문서는 프로그램 설치에 최소 4GB의 공간을 요구하며, 모델 저장 공간은 별도로 필요하다고 안내한다. 이 수업은 여유를 두어 10GB 이상을 확보하는 것을 권장한다.
3. 모델을 내려받을 인터넷 연결을 확인한다. 학교 PC에서 설치가 제한되면 조교에게 설치 권한을 요청한다.
4. 1교시에는 Python이 없어도 된다. 2교시 전에 PowerShell에서 `uv --version`을 확인한다. uv가 없다면 [uv 설치 가이드](../../uv_guide.md)를 먼저 따른다.

## 3. Windows 설치 파일 받기

1. 웹 브라우저에서 [Ollama Windows 다운로드 페이지](https://ollama.com/download/windows)를 연다.
2. **Windows**가 선택되어 있는지 확인한다.
3. **Download manually** 또는 Windows 설치 파일 다운로드 버튼을 누른다. 화면에 PowerShell 설치 명령이 먼저 보여도, 이 수업에서는 설치 파일 경로를 사용한다.
4. 받은 파일의 이름이 `OllamaSetup.exe`인지 확인한다. ZIP 압축판은 이번 실습에 사용하지 않는다.
5. 브라우저의 다운로드 목록에서 해당 파일을 열거나, 파일 탐색기에서 받은 설치 파일을 더블 클릭한다.

공식 사이트에서 받은 파일인지 확인한다. 학교 보안 정책 때문에 실행이 막히면 경고를 임의로 우회하지 말고 조교에게 확인한다.

## 4. 설치하고 Ollama 실행하기

1. 설치 창에서 **Install**을 누른다. 설치가 끝날 때까지 기다린다.
2. 시작 메뉴에서 **Ollama**를 검색해 실행한다. 이미 실행 중이면 다시 켤 필요 없다.
3. 작업 표시줄 오른쪽의 숨겨진 아이콘 표시(`^`)를 열고 Ollama 아이콘을 확인한다. 앱 창을 닫아도 백그라운드에서 실행될 수 있다.
4. 열려 있던 PowerShell을 닫고 새로 연다. VS Code 터미널을 쓸 경우 **VS Code 전체를 종료한 뒤 다시 연다.** 설치 때 추가된 명령 검색 경로(PATH)를 새 프로그램이 읽어야 하기 때문이다.

공식 설치 프로그램은 보통 관리자 권한 없이 사용자 계정에 설치한다. Windows에서는 Ollama가 백그라운드에서 서버도 실행한다. [공식 설치 안내](https://docs.ollama.com/windows)

## 5. PowerShell 열고 설치 확인하기

1. 시작 메뉴에서 **PowerShell**을 검색해 연다. 관리자 모드로 열 필요는 없다.
2. 아래 명령을 한 줄씩 입력하고 Enter를 누른다. `PS C:\...>` 같은 앞부분은 입력하지 않는다.

```powershell
ollama --version
ollama list
```

첫 명령은 `ollama version is ...`처럼 버전을 보여 준다. 숫자는 설치한 버전에 따라 다르다. 두 번째 명령은 설치된 모델 목록을 보여 준다. 처음에는 `NAME`, `ID`, `SIZE`, `MODIFIED` 열만 있고 모델이 없어도 정상이다.

`ollama --version`은 명령을 찾는지, `ollama list`는 실행 중인 서버와 통신하는지 확인한다. 두 가지 확인이 끝나야 모델을 내려받는다.

## 6. 작은 모델 하나 내려받기

PowerShell에서 다음을 실행한다.

```powershell
ollama pull qwen3:0.6b
ollama list
```

`pull`은 모델 파일을 내려받는 명령이다. 진행률이 끝나고 성공 메시지가 나올 때까지 기다린다. `qwen3:0.6b`는 공식 모델 페이지 기준 다운로드 크기가 약 523MB인 소형 모델이다. 실제 크기와 속도는 모델 갱신·네트워크 상태에 따라 달라질 수 있다. [모델 정보](https://ollama.com/library/qwen3:0.6b)

두 번째 명령의 목록에 `qwen3:0.6b`가 나타나면 준비 완료다. 모델을 다시 내려받을 필요 없이 다음 시간에도 사용할 수 있다. 모델 파일은 기본적으로 사용자 홈의 `.ollama\models`에 저장되며 Python 프로젝트의 `.venv`와는 별개다.

다운로드는 수업 전 준비 시간 또는 1교시 설치 구간에서 진행한다. 여러 PC가 같은 네트워크를 쓸 때는 조교가 시간을 나누어 준비한다. 모델이 없는 상태에서 이후 실습을 시작하지 않는다.

## 7. 첫 채팅하기

PowerShell에서 모델을 실행한다.

```powershell
ollama run qwen3:0.6b
```

입력 표시가 `>>>`로 바뀌면 **Ollama 대화창 안**이다. 아래 문장을 하나씩 입력한다.

```text
안녕. 한국어로 짧게 인사해 줘. /no_think
나는 수업용 이름 student01이야. 좋아하는 색은 파랑이야. /no_think
내가 좋아하는 색은 무엇이야? /no_think
```

`/no_think`는 이 Qwen3 모델에 답변 전의 긴 생각 출력을 줄이도록 요청하는 표식이다. Python 예제에서는 같은 목적에 `think=False`를 사용한다. 다른 모델에서 그대로 동작한다고 가정하지 않는다. 답 문장은 매번 달라도 된다. 작은 모델은 한국어·지시 따르기가 서툴 수 있으므로 결과를 직접 관찰한다.

같은 대화 안에서 색을 다시 말하는지 확인한 뒤 다음을 입력한다.

```text
/bye
```

PowerShell로 돌아오면 `ollama run qwen3:0.6b`를 다시 실행한다. 이번에는 색을 먼저 알려 주지 않고 “내가 좋아하는 색은 무엇이야?”라고 묻는다. 앞 대화 내용이 새 대화에 자동으로 이어지는지 비교한다. 우연히 파랑이라고 답하더라도 기억의 증거는 아니다.

## 8. 자주 쓰는 명령

| PowerShell 명령 | 언제 쓰는가 |
|---|---|
| `ollama --version` | 설치된 버전 확인 |
| `ollama list` | 내려받은 모델 이름 확인 |
| `ollama pull qwen3:0.6b` | 모델 다운로드 |
| `ollama run qwen3:0.6b` | 채팅 시작 |
| `ollama show qwen3:0.6b` | 모델 정보 확인 |
| `ollama ps` | 현재 메모리에 올라온 모델 확인 |
| `ollama stop qwen3:0.6b` | 실행 중인 모델을 메모리에서 내리기 |

`/bye`는 Ollama 대화 안에서 입력한다. `ollama list` 같은 명령은 PowerShell에서 입력한다. 헷갈리면 입력 표시가 `>>>`인지 `PS ...>`인지 먼저 본다.

## 9. 막혔을 때 확인할 것

### “ollama 용어가 … 인식되지 않습니다”

설치 직후 열어 둔 터미널을 계속 사용했을 수 있다. PowerShell과 VS Code를 완전히 닫고 다시 연다. 여전히 실패하면 다음으로 설치 파일을 확인한다.

```powershell
Test-Path "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
```

기본 경로에 설치했다면 `True`가 나와야 한다. `False`이면 설치 완료 여부·설치 경로를 확인한다. `True`인데 명령만 안 잡히면 아래 직접 경로 실행을 시도하고 조교에게 PATH 점검을 요청한다.

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
```

### “could not connect to ollama” / 연결 실패

시작 메뉴에서 Ollama를 실행하고 잠시 기다린 뒤 `ollama list`를 다시 실행한다. 앱 실행이 안 되는 경우에만 새 PowerShell 하나에서 `ollama serve`를 실행해 둔다. 그 창은 서버용으로 남겨 두고 다른 PowerShell에서 실습한다.

`ollama serve`에서 `address already in use`가 나오면 보통 기존 서버가 이미 포트를 쓰고 있다. 서버를 계속 추가 실행하지 말고 다른 창에서 `ollama list`로 확인한다. Python의 기본 서버 주소는 `http://localhost:11434`다.

### 모델이 없다는 오류 / 모델 이름을 못 찾음

`ollama list`에 나오는 이름과 코드의 이름이 같은지 확인한다. `qwen3`와 `qwen3:0.6b`를 같은 다운로드 크기의 모델이라고 생각하면 안 된다. 이번에는 정확히 `qwen3:0.6b`를 사용한다.

### 다운로드가 멈추거나 디스크가 부족함

인터넷 연결·남은 공간을 확인하고 같은 `ollama pull qwen3:0.6b`를 다시 실행한다. 학교 네트워크의 차단·프록시 문제이면 조교에게 문의한다. C: 공간이 부족하면 아래 선택 절차로 모델 저장 위치를 먼저 바꾼다.

### 답이 느리거나 나오다 끊김

첫 질문에는 모델을 메모리에 올리는 시간이 포함된다. 짧은 질문으로 다시 시도한다. GPU가 없어도 기본 소형 모델로 진행할 수 있다. Python에서 시간 초과가 나면 `.env`의 `OLLAMA_TIMEOUT`을 늘린다. 모델이 출력 제한에 도달하면 답이 끊길 수 있으므로 긴 보고서 대신 짧은 대화를 실습한다.

## 10. 선택: 모델 저장 위치를 D:로 바꾸기

C: 공간이 충분하면 이 단계는 건너뛴다. **새 모델을 다운로드하기 전에** 설정하는 편이 쉽다.

1. 파일 탐색기에서 `D:\ollama-models` 폴더를 만든다.
2. 작업 표시줄의 Ollama 아이콘 메뉴에서 종료(Quit)를 선택한다.
3. 시작 메뉴에서 “환경 변수”를 검색하고 **계정의 환경 변수 편집**을 연다.
4. 사용자 변수에서 **새로 만들기**를 누른다.
5. 변수 이름은 `OLLAMA_MODELS`, 값은 `D:\ollama-models`로 입력한다.
6. 확인을 눌러 모든 설정 창을 닫는다.
7. 시작 메뉴에서 Ollama를 다시 실행하고 PowerShell도 새로 연다.
8. `ollama pull qwen3:0.6b`와 `ollama list`로 확인한다.

이 설정은 기존 파일을 자동으로 옮기지 않는다. 이전 위치에 모델이 있었다면 새 위치에서는 목록이 비어 보일 수 있다. 위 순서는 새 위치에 다시 받는 방법이다. Python 프로젝트의 `.env`에 `OLLAMA_MODELS`만 적어서는 이미 실행 중인 Windows 앱의 저장 위치가 바뀌지 않는다. [공식 저장 위치 변경 안내](https://docs.ollama.com/windows#changing-model-location)

## 설치 완료 체크

- [ ] 새 PowerShell에서 `ollama --version`이 나온다.
- [ ] `ollama list`에 `qwen3:0.6b`가 보인다.
- [ ] `ollama run qwen3:0.6b`에서 한국어 질문에 답을 받았다.
- [ ] `/bye`로 PowerShell에 돌아왔다.

이제 [Python 라이브러리와 프롬프트·기억 실습](python_library.md)으로 이어간다.

## 출처

- [Windows 설치·요구사항·문제 해결](https://docs.ollama.com/windows)
- [Ollama 명령 사용법](https://docs.ollama.com/cli)
- [Qwen3 소형 모델](https://ollama.com/library/qwen3:0.6b)
- [Qwen3 생각 출력 제어](https://docs.ollama.com/capabilities/thinking)
- [공식 Python 라이브러리](https://github.com/ollama/ollama-python)
