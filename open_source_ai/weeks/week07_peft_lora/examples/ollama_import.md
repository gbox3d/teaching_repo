# GGUF 변환과 Ollama 실행

**`ex05` 병합 → GGUF 변환 → 파일 확인 → Ollama 등록 → 대화**의 전체 순서다. `ex05`는 Hugging Face 형식의 모델 폴더를 저장하고 `ex06`은 그 폴더를 Python에서 읽는다. 두 명령 모두 GGUF 파일은 만들지 않으며, 이 문서의 변환 명령을 별도로 실행해야 한다.

학생 필수 실습은 `ex04`의 저장·복원·전후 비교까지다. Ollama 경로는 시연 또는 선택 실습이며, 변환기는 수업 전에 준비한다. 이 문서의 변환·등록 명령은 `pyproject.toml`과 `Modelfile`이 있는 예제 프로젝트 루트에서 실행한다.

## 병합 모델을 GGUF로 변환

병합 전이면 `uv run ex05`로 `models/merged-run-001/`을 만든다. 이미 병합했다면 `ex05`를 건너뛰고 기존 폴더를 이어 쓴다. 기존 병합 폴더를 덮어쓰지 않는다. `uv run ex06`에서 질문 → 응답 → 다음 질문 → `/bye`를 확인한 뒤, Ollama에서도 실행하려면 아래 변환을 선택한다.

병합 폴더는 Hugging Face 형식이다. Ollama의 Safetensors 직접 가져오기는 모델 구조와 실행기에 따라 지원 여부가 다르므로, 이 예제의 기본 연결 경로는 GGUF 파일이다.

## 변환기 준비

변환기는 [검증한 버전의 llama.cpp 공식 스크립트](https://github.com/ggml-org/llama.cpp/blob/ccd360f060a0f17b87ee0d4c5d91ee84cfdff484/convert_hf_to_gguf.py)를 쓴다. 아래는 외부 도구의 준비·변환 명령이다. Python 버전·학습 패키지는 현재 uv 프로젝트를 사용하며 추가 두 패키지만 해당 실행에 포함한다. 프로젝트의 의존성을 변경하지 않는다.

처음 준비할 때 별도 도구 폴더에 저장소를 받는다. 이미 `../tools/llama.cpp`에 같은 버전으로 준비했다면 clone과 checkout을 다시 하지 않는다. 다른 작업에 쓰던 폴더가 같은 위치에 있으면 새 도구 폴더를 쓰고 아래 변환 명령의 스크립트 경로도 바꾼다.

`examples/`에서 실행하면 `../tools/llama.cpp`는 `examples`와 나란한 `tools` 폴더 아래에 생긴다. 뒤의 변환 명령도 같은 작업 폴더에서 실행한다.

```powershell
git clone https://github.com/ggml-org/llama.cpp.git ../tools/llama.cpp
git -C ../tools/llama.cpp checkout ccd360f060a0f17b87ee0d4c5d91ee84cfdff484
```

이 commit으로 아래 변환을 확인했다(macOS, Windows). Windows에서는 2026-11-12에 Ollama 0.40.16으로 새로 학습·병합한 모델의 GGUF 변환, 등록, `ex01`의 두 질문과 종료까지 확인했다. 다른 버전이나 PC에서는 변환과 실제 응답을 수업 전에 다시 확인한다.

## GGUF 파일 생성과 확인

① `examples/`에서 아래 변환 명령을 실행한다. 변환기는 `ex05`가 저장한 `models/merged-run-001/` 폴더를 읽어 `models/week07-lora.gguf` 파일 하나를 만든다. `--outfile`은 저장할 경로이고, `--outtype f16`은 가중치를 16비트 부동소수점 형식으로 저장하라는 뜻이다.

PowerShell에서는 아래 세 줄이 한 명령이다. 줄 끝의 백틱 뒤에는 공백을 두지 않는다. macOS·Linux 터미널에서는 백틱을 빼고 세 줄을 한 줄로 이어서 실행한다.

```powershell
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 `
  python ../tools/llama.cpp/convert_hf_to_gguf.py `
  models/merged-run-001 --outfile models/week07-lora.gguf --outtype f16
```

② 변환이 오류 없이 끝나면, 같은 폴더에서 방금 만든 파일을 확인한다. PowerShell의 `Get-Item`은 지정한 파일의 정보를 보여 준다. 아래 명령은 그중 이름과 크기를 표시한다.

```powershell
Get-Item ./models/week07-lora.gguf | Select-Object Name, Length
```

`Name`에는 `week07-lora.gguf`, `Length`에는 파일 크기가 **바이트 단위**로 표시된다. 이 예제 모델을 f16으로 변환하면 약 1 GB이므로 10억 바이트 안팎의 숫자가 나온다. macOS·Linux에서는 `ls -lh ./models/week07-lora.gguf`로 파일 이름과 크기를 확인한다. 파일을 찾을 수 없거나 크기가 0이면 위 변환 명령의 오류와 `--outfile` 경로를 확인한다.

병합 폴더 경로를 바꿨다면 변환 명령에도 그 경로를 넣는다. 기존 GGUF 파일을 보존하려면 `--outfile`에 새 파일 이름을 쓰고 아래 `Modelfile`의 `FROM`도 같은 경로로 바꾼다. Ollama에 등록할 때는 모델 파일 크기만큼 디스크 공간이 추가로 필요하다.

## 등록과 실제 응답 확인

③ 방금 만든 파일을 내 PC의 Ollama에서 `week07-lora`라는 이름으로 쓰려면 다음 명령을 실행한다. `-f Modelfile`로 지정한 설정 파일에는 `FROM ./models/week07-lora.gguf`가 들어 있다. Ollama는 이 줄을 읽어 가져올 파일을 찾는다. 이미 같은 이름으로 등록한 모델을 보존하려면 `ollama create`와 `ollama run`에 새 모델 이름을 쓴다.

```powershell
ollama create week07-lora -f Modelfile
```

④ `ollama list`로 내 PC의 모델 목록을 연다. `NAME` 열에 `week07-lora:latest`가 보이면 `ollama run week07-lora`로 대화를 시작한다.

```powershell
ollama list
ollama run week07-lora
```

대화 입력창에 `아테나를 소개해 줘.`를 입력한다. 답이 나오면 다른 질문도 입력해 보고 `/bye`로 종료한다.

이어서 `src/ex01_ollama/__init__.py`의 `MODEL`을 `"week07-lora"`로 바꾸고 `uv run ex01`에서 질문 → 응답 → 다음 질문 → `/bye`를 확인한다. `ex01`의 `PROMPT`가 `SYSTEM_PROMPT`로 되돌려져 있는지 확인한다. 학습·비교와 같은 system 지시를 써야 한다. Ollama 내 대화는 이력을 누적하지만 ex01은 질문을 독립적으로 보낸다.

## 가져오기 오류 구분

- 이 Qwen 예제의 `incorrect regex pattern` 경고: 고정 변환기에서도 Transformers 4.57.6의 [로컬 Qwen 오탐](README.md#병합한-모델로-python에서-대화하기)이 출력될 수 있다. 예제 로더의 설정은 외부 변환기에 적용되지 않는다. 위 Windows 검증에서는 이 경고가 있어도 변환과 실제 응답을 확인했다. 경고 문구만 보고 Qwen에 Mistral 보정을 적용하지 않는다.
- `unsupported ... architecture`: Safetensors 폴더 직접 가져오기의 지원 여부를 확인한다. 이 안내의 GGUF 경로로 변환했는지 먼저 본다.
- 파일 없음: 프로젝트 실행 위치, Modelfile의 상대 경로, 실제 GGUF 생성 여부를 확인한다.
- 등록은 되지만 응답 실패: 기본 모델·변환기·Ollama 버전과 오류를 기록한다. 해당 환경은 시연 준비 완료로 처리하지 않는다.

자료: [Ollama 가져오기](https://docs.ollama.com/import), [Modelfile](https://docs.ollama.com/modelfile).
