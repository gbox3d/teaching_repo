# Ollama 연결 시연 준비

강의자가 수업 전에 준비하는 변환 경로다. 학생 필수 실습은 `ex04`의 저장·복원·전후 비교까지이며, 변환 도구를 수업 중 새로 설치하게 하지 않는다. 이 문서는 예제 프로젝트 루트에서 실행한다.

## 병합 모델을 GGUF로 변환

병합 전이면 `uv run ex05`로 `models/merged-run-001/`을 만든다. 이미 병합했다면 `ex05`를 건너뛰고 기존 폴더를 이어 쓴다. 기존 병합 폴더를 덮어쓰지 않는다. `uv run ex06`에서 질문 → 응답 → 다음 질문 → `/bye`를 확인한 뒤, Ollama에서도 실행하려면 아래 변환을 선택한다.

병합 폴더는 Hugging Face 형식이다. Ollama의 Safetensors 직접 가져오기는 모델 구조와 실행기에 따라 지원 여부가 다르므로, 이 예제의 기본 연결 경로는 GGUF 파일이다.

변환기는 [llama.cpp의 공식 스크립트](https://github.com/ggml-org/llama.cpp/blob/master/convert_hf_to_gguf.py)를 쓴다. 아래는 교재 예제 명령이 아니라 외부 도구의 준비·변환 명령이다. Python 버전·학습 패키지는 현재 uv 프로젝트를 사용하며 추가 두 패키지만 해당 실행에 포함한다. 프로젝트의 의존성을 변경하지 않는다.

처음 준비할 때 별도 도구 폴더에 저장소를 받는다. 이미 있는 개인 폴더를 덮어쓰지 않는다.

```powershell
git clone https://github.com/ggml-org/llama.cpp.git C:\classwork\tools\llama.cpp
git -C C:\classwork\tools\llama.cpp checkout ccd360f060a0f17b87ee0d4c5d91ee84cfdff484
```

이 commit으로 아래 변환을 확인했다(macOS, Windows). Windows에서는 2026-11-12에 Ollama 0.40.16으로 새로 학습·병합한 모델의 GGUF 변환, 등록, `ex01`의 두 질문과 종료까지 확인했다. 다른 버전이나 PC에서는 변환과 실제 응답을 수업 전에 다시 확인한다.

```powershell
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 python C:\classwork\tools\llama.cpp\convert_hf_to_gguf.py models/merged-run-001 --outfile models/week07-lora.gguf --outtype f16
```

macOS·Linux에서는 도구 경로를 자신의 checkout 경로로 바꾼다. `f16` 파일도 약 1GB가 필요하고, 등록하면 Ollama 저장소에 같은 크기가 한 번 더 저장된다. `shared`의 `MERGED_DIR`을 바꿨다면 변환 명령의 입력 경로도 맞춘다. 어댑터 파일 자체를 변환기의 입력으로 주지 않는다.

## 등록과 실제 응답 확인

```powershell
ollama create week07-lora -f Modelfile
ollama run week07-lora
```

`Modelfile`의 `FROM`은 `./models/week07-lora.gguf`다. 같은 이름의 개인 모델이 있으면 새 모델 이름을 사용한다. `아테나를 소개해 줘.` 등 두 질문을 입력하고 실제 응답을 확인한다. 등록 성공만으로 시연 준비 완료로 보지 않는다.

이어서 `src/ex01_ollama/__init__.py`의 `MODEL`을 `"week07-lora"`로 바꾸고 `uv run ex01`에서 질문 → 응답 → 다음 질문 → `/bye`를 확인한다. `ex01`의 `PROMPT`가 `SYSTEM_PROMPT`로 되돌려져 있는지 확인한다. 학습·비교와 같은 system 지시를 써야 한다. Ollama 내 대화는 이력을 누적하지만 ex01은 질문을 독립적으로 보낸다.

## 가져오기 오류 구분

- 이 Qwen 예제의 `incorrect regex pattern` 경고: 고정 변환기에서도 Transformers 4.57.6의 [로컬 Qwen 오탐](README.md#병합한-모델로-python에서-대화하기)이 출력될 수 있다. 예제 로더의 설정은 외부 변환기에 적용되지 않는다. 위 Windows 검증에서는 이 경고가 있어도 변환과 실제 응답을 확인했다. 경고 문구만 보고 Qwen에 Mistral 보정을 적용하지 않는다.
- `unsupported ... architecture`: Safetensors 폴더 직접 가져오기의 지원 여부를 확인한다. 이 안내의 GGUF 경로로 변환했는지 먼저 본다.
- 파일 없음: 프로젝트 실행 위치, Modelfile의 상대 경로, 실제 GGUF 생성 여부를 확인한다.
- 등록은 되지만 응답 실패: 기본 모델·변환기·Ollama 버전과 오류를 기록한다. 해당 환경은 시연 준비 완료로 처리하지 않는다.

자료: [Ollama 가져오기](https://docs.ollama.com/import), [Modelfile](https://docs.ollama.com/modelfile).
