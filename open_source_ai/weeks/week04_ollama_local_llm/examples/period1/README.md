# 1교시 — 터미널에서 모델 실행하고 숫자 읽기

코드는 없다. Ollama 명령만으로 모델을 돌려 보고 화면에 나오는 숫자를 읽는다. 설치가 안 됐으면 [Windows 설치 안내](../../windows_setup.md)부터 한다.

## 1. 모델 정보 보기

```powershell
ollama list
ollama show qwen3.5:2b
```

`ollama show`에서 parameters(파라미터 수), quantization(양자화), context length(한 번에 읽는 길이)를 찾아 적는다.

## 2. 대화하면서 속도 보기

```powershell
ollama run qwen3.5:2b --think=false
```

`--think=false`는 Qwen3.5가 답 전에 늘어놓는 생각 출력을 끈다.

`>>>`가 나오면 차례로 입력한다.

```text
/set verbose
파이썬이 무엇인지 두 문장으로 설명해 줘.
/bye
```

답 아래에 나오는 `eval rate`가 초당 토큰 수(tokens/s)다.

## 3. 메모리에 올라간 모델 보기

`/bye` 직후 PowerShell에서 실행한다.

```powershell
ollama ps
```

`SIZE`는 차지한 메모리, `PROCESSOR`는 GPU와 CPU 중 어디서 돌았는지다.

## 기록

| 항목 | 값 |
|---|---|
| 파라미터 수 | |
| 양자화 | |
| eval rate (tokens/s) | |
| ollama ps SIZE | |
| PROCESSOR | |

시간이 남으면 `ollama run`을 끝내고 5분 뒤 `ollama ps`를 다시 실행해 본다. 목록이 비어 있으면 모델이 메모리에서 내려간 것이다.
