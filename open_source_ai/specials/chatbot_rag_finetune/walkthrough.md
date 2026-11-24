# 특강 따라하기: 수업 전 준비, 검색 관찰, 학습·등록

1교시와 4교시의 명령과 출력 읽는 법은 [1교시 안내](examples/period1/README.md)와 [4교시 안내](examples/period4/README.md)에 있다. 두 교시에 쓰는 모델과 프로젝트는 아래 수업 전 준비에서 함께 준비한다.

명령은 두 uv 프로젝트에서 나눠 실행한다. `examples/`는 평가·검색·학습 예시 만들기이고, `finetune/`은 학습·병합·GGUF 변환이다. 두 프로젝트 모두 저장소 전체를 clone한 위치에서 실행한다. `ex04`~`ex07`은 `examples/`에서, `prepare`·`ft01`·`ft02`·변환·`ollama create`는 `finetune/`에서 실행한다.

이 문서는 두 가지를 구분해 쓴다. 학습 문항은 `lab_shared/data`의 질문·정답 JSON이고, 학습 예시는 `ex06`이 학습 문항으로 만든 대화 한 줄(`outputs/sft/train.jsonl`)이다. 기본 모델은 학습할 원본 `Qwen/Qwen2.5-0.5B-Instruct`이고, 학습 전 모델(`wku-base`)은 기본 모델을, 학습한 모델(`wku-lora`)은 `ft02`가 어댑터를 합친 병합 모델을 GGUF로 바꿔 Ollama에 등록한 것이다.

## 수업 전 준비

### 두 프로젝트 설치와 모델 받기

```powershell
cd open_source_ai/specials/chatbot_rag_finetune/examples
uv sync
cd ../finetune
uv sync
uv run prepare
ollama pull qwen3.5:2b
ollama pull bge-m3
```

`uv run prepare`는 기본 모델을 고정 commit으로 `finetune/models/Qwen2.5-0.5B-Instruct/`에 받는다(약 1GB). 7주차처럼 Hugging Face 캐시만 쓰지 않고 폴더로 받는 이유는 두 가지다. 같은 폴더를 학습·병합·GGUF 변환이 함께 쓰고, PC마다 다른 캐시 위치를 몰라도 된다. 다만 토큰 파일은 여전히 Hugging Face 캐시 폴더(`HF_HOME`, 기본값은 사용자 폴더의 `.cache/huggingface`)에서 읽는다. 그 폴더가 없는 드라이브를 가리키면 `prepare`가 `OSError`로 멈춘다. 이때는 `HF_HOME`을 쓸 수 있는 폴더로 정하고 다시 실행한다.

### GGUF 변환기

변환기는 7주차와 같은 llama.cpp commit의 Python 스크립트를 쓴다. 저장소 전체를 받으면 경로가 길어 Windows의 260자 제한에 걸릴 수 있다. 변환에 필요한 `gguf-py`와 `conversion` 폴더만 받는다. `finetune/`에서 실행한다.

```powershell
git clone --depth 1 --filter=blob:none --sparse https://github.com/ggml-org/llama.cpp.git tools/llama.cpp
git -C tools/llama.cpp sparse-checkout set gguf-py conversion
git -C tools/llama.cpp fetch --depth 1 origin ccd360f060a0f17b87ee0d4c5d91ee84cfdff484
git -C tools/llama.cpp checkout ccd360f060a0f17b87ee0d4c5d91ee84cfdff484
git -C tools/llama.cpp log -1 --format=%H
```

마지막 줄이 `ccd360f060a0f17b87ee0d4c5d91ee84cfdff484`를 출력해야 한다. 이 commit의 변환기는 `convert_hf_to_gguf.py` 하나가 아니라 `conversion/` 패키지와 함께 동작하므로 두 폴더가 모두 있어야 한다. `tools/llama.cpp/`는 커밋하지 않는다.

### 학습 전 모델 등록(wku-base)

학습 전후를 같은 경로로 비교하려고 기본 모델도 GGUF로 바꿔 등록해 둔다. `finetune/`에서 실행한다.

```powershell
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 `
  python tools/llama.cpp/convert_hf_to_gguf.py `
  models/Qwen2.5-0.5B-Instruct --outfile models/wku-base.gguf --outtype f16
ollama create wku-base -f Modelfile.base
```

PowerShell에서는 앞의 세 줄이 한 명령이다. 줄 끝 백틱 뒤에 공백을 두지 않는다. macOS·Linux에서는 백틱을 빼고 한 줄로 쓴다.

`Modelfile.base`와 `Modelfile.lora`에는 `FROM`과 `PARAMETER temperature 0` 두 줄만 있다. 7주차 `Modelfile`을 복사하면 신화 안내자 `SYSTEM`과 `num_predict 120`도 함께 등록된다. `rag_bot`은 요청마다 `num_predict 512`를 보내므로 120은 쓰이지 않지만, `ollama run`처럼 이 값을 보내지 않는 실행에는 등록한 값이 쓰인다. 요청에 system 메시지가 있을 때 Modelfile의 `SYSTEM`이 어떻게 처리되는지는 확인하지 않았으므로 `SYSTEM` 없이 등록한다([추론 버그 잡기](examples/debugging.md#7주차-modelfile을-복사할-때-따라오는-값)).

### 수업 전 점검과 정리

`finetune/`에서 학습 환경이 GPU를 잡는지 본다.

```powershell
uv run python -c "import torch; print(torch.version.cuda, torch.cuda.is_available())"
```

`12.8 True`가 나와야 한다. 이어서 아래 3교시 명령을 끝까지 한 번 실행해 시간을 잰다. 잰 뒤에는 `wku-base`는 남기고 학습 산출물을 지운다. 남겨 두면 수업 중 `ft01`·`ft02`가 이미 있다며 멈춘다. `examples/`에서 바꾼 상수(`ex04`의 `BOT`, `rag_bot`의 `MODEL`, `ex07`의 `BOT`)도 기본값으로 되돌리고 `git status --short -- src`로 바뀐 파일이 없는지 확인한다.

```powershell
cd ../finetune
Remove-Item -Recurse -Force adapters/wku-run-001, models/wku-lora-merged, models/wku-lora.gguf, ../outputs/sft
ollama rm wku-lora
```

## 2교시: 검색 관찰(examples/)

```powershell
cd ../examples
uv run ex05
```

`ex05`는 내 문항(`mine`)과 공개 20문항(`public`)에서 `student_bot`과 `rag_bot`의 검색 결과를 문항마다 보여 준다. 참고 자료가 문서 5개뿐이라 `TOP_K` 3이면 두 검색 모두 평가 문항의 근거를 대부분 보낸다. `ex05`의 `SETS`에 `"train"`을 더하면 학습 문항에서 두 검색의 차이가 드러난다.

점수는 `src/ex04_my_eval/__init__.py`의 `BOT`을 `"rag_bot"`으로 바꿔 `uv run ex04`로 잰다. 기본값(`TOP_K = 3`, `MIN_SCORE = 0.0`)으로 `QUESTION_SET`을 `"mine"`과 `"public"`으로 한 번씩 잰 뒤, `rag_bot`의 상수를 하나만 바꿔 다시 잰다. 2교시 끝에 3교시에 쓸 검색 설정을 하나 정해 `rag_bot`에 남긴다.

## 3교시: 학습 예시 만들기에서 등록까지

### 1. 학습 예시 만들기(examples/)

```powershell
cd ../examples
uv run ex06
ollama ps
ollama stop bge-m3
```

`ex06`은 학습 문항마다 `rag_bot.retrieve`로 문서를 찾고 `rag_bot.messages`로 실제 요청과 같은 대화를 만든 뒤 정답 JSON을 붙인다. 결과는 특강 폴더의 `outputs/sft/train.jsonl`에, 만든 때의 검색 설정은 같은 폴더의 `settings.json`에 저장된다. 평가 문항(공개 20문항, 내 평가 문항)과 같은 학습 문항이 있으면 모두 보여 주고 멈춘다. 검색이 근거 문서를 놓친 문항은 학습에서 빼고 이유를 출력한다.

`ex06`은 검색에 `bge-m3`를 써서 Ollama에 모델이 올라가 있다. `ft01`은 Ollama가 올린 모델이 있으면 멈추므로 `ollama ps`에 나온 모델을 모두 `ollama stop`으로 내린 뒤 실행한다. `ft01`이 도는 동안 다른 터미널에서 `ex04`·`ex05`를 실행하지 않는다. 모델이 다시 올라가 VRAM을 나눠 쓴다.

`rag_bot`의 `TOP_K`, `MIN_SCORE`, `EMBED_MODEL`을 바꾸면 모델이 받는 입력이 달라진다. 이때는 `ex06`과 학습을 다시 실행한다.

### 2. 학습과 병합(finetune/)

```powershell
cd ../finetune
uv run ft01
uv run ft02
```

`ft01`은 7주차 `ex03`과 같은 순서로 LoRA를 학습해 `adapters/wku-run-001/`에 저장한다. 7주차와 다른 값은 다음과 같다.

| 값 | 7주차 | 이 특강 | 이유 |
|---|---|---|---|
| `MAX_LENGTH` | 256 | 1024 | 검색 문서 3개가 든 예시가 기준 PC에서 600~761토큰이었다 |
| `DTYPE` | float32 | bfloat16 | 8GB GPU에서 메모리를 줄인다 |
| `GRADIENT_CHECKPOINTING` | 없음 | True | 중간 계산을 다시 해서 메모리를 줄인다 |
| `RANK`, 대상 층 | 8, q·v | 16, 7개 선형층 | 형식과 답 고르기를 함께 학습한다 |
| `LEARNING_RATE` | 5e-4 | 2e-4 | LoRA에서 흔히 쓰는 값으로 정했다. 두 값을 비교해 재지는 않았다 |
| `gradient_accumulation_steps` | 2 | 4 | step마다 예시 4건을 본다. 30 step이면 학습 예시 40건(`ex06`이 뺀 문항이 없을 때)을 세 바퀴 돈다 |
| 패딩 | 없음 | 64토큰 단위(`pad_to_multiple_of=64`) | 길이가 제각각인 예시로 step을 많이 돌리면 GPU 메모리 조각이 쌓인다 |

시작할 때 예시 수와 최소·최대 토큰 수, 학습 파일을 만든 때의 검색 설정을 출력한다. 끝에는 `{'train_runtime': …}`(학습 시간, 초), `GPU 최대 할당 메모리`, `GPU 최대 예약 메모리`를 출력한다. 예약이 할당보다 훨씬 크면 메모리 조각이 쌓인 것이다. `ft02`는 7주차 `ex05`와 같이 어댑터를 기본 모델에 합쳐 `models/wku-lora-merged/`에 저장한다.

다시 학습할 때는 `finetune/src/shared`의 `ADAPTER_DIR`·`MERGED_DIR`을 새 이름으로 바꾼다. 아래 변환 명령의 입력 폴더도 `ft02`가 출력한 `병합 완료: <폴더>`로 바꾼다. 그대로 두면 이전 병합 모델을 다시 변환해 같은 이름으로 등록한다.

### 3. GGUF 변환과 등록(finetune/)

```powershell
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 `
  python tools/llama.cpp/convert_hf_to_gguf.py `
  models/wku-lora-merged --outfile models/wku-lora.gguf --outtype f16
ollama create wku-lora -f Modelfile.lora
ollama list
```

`--outtype q8_0`으로 바꾸면 파일이 작아진다(기준 PC의 0.5B에서 994MB → 531MB). 이때는 `wku-base`도 q8_0으로 다시 만들어 같은 양자화끼리 비교한다. Ollama 0.40.17의 `ollama create -q`(등록할 때 양자화)는 GGUF 입력을 거부하고, 병합한 safetensors 폴더를 바로 등록하는 방법도 Qwen2 구조를 거부한다. 그래서 변환기에서 GGUF로 만든 뒤 등록한다.

### 4. 같은 채점기로 재기(examples/)

`src/ex04_my_eval/__init__.py`의 `BOT`이 `"rag_bot"`인지 확인한다. `"student_bot"`이면 `rag_bot`의 `MODEL`을 바꿔도 점수가 달라지지 않는다. 그다음 `src/rag_bot/__init__.py`의 `MODEL`을 `"wku-lora"`로 바꾸고 `uv run ex04`로 잰다. 출력 첫 줄의 `평가 대상: BOT=rag_bot`과 끝의 '평가 뒤 올라가 있는 모델'에 `wku-lora`가 있는지 본다. `MODEL`만 `"wku-base"`, `"qwen3.5:2b"`로 바꿔 같은 문항으로 다시 재면 학습 전후와 2B 생성 모델을 비교할 수 있다.

답이 이상한 문항은 4교시에 본다. `ex07`의 `BOT`을 `"rag_bot"`으로 두고, `rag_bot`의 `MODEL`을 답이 이상했던 모델(예: `"wku-lora"`)로 되돌린 뒤 `uv run ex07`로 요청과 응답을 본다. 증상별로 확인할 값은 [추론 버그 잡기](examples/debugging.md)에 있다.

## 모델 바꾸기

예제가 쓰는 모델은 생성 `qwen3.5:2b`, 임베딩 `bge-m3`, 학습 `Qwen/Qwen2.5-0.5B-Instruct`다. 어떤 모델을 쓸지는 학생이 고르고, 과제의 모델 규칙은 강좌 공지를 따른다. 모델 크기는 `ollama show <모델 이름>`의 `parameters`로 확인한다(예제 모델은 1.9B, 566.70M, 494.03M). 아직 등록하지 않은 학습용 모델은 Hugging Face 모델 카드의 파라미터 수로 본다. 바꿀 값은 모두 파일 위쪽의 대문자 상수다.

| 바꿀 것 | 상수 | 함께 바꿀 곳 |
|---|---|---|
| 답을 만드는 Ollama 모델 | `rag_bot`의 `MODEL` | `ollama list`에 있는 이름이어야 한다. 학습한 모델이면 `ollama create`로 등록한 이름 |
| 검색에 쓰는 임베딩 모델 | `rag_bot`의 `EMBED_MODEL` | 수업 밖에서 `ollama pull`로 받아 둔다. 바꾼 뒤 `ex05`로 검색 결과를 다시 보고, `ex06`과 학습을 다시 실행한다 |
| 학습할 기본 모델 | `finetune/src/shared`의 `MODEL_ID`, `REVISION`, `BASE_DIR` | `uv run prepare`로 다시 받는다. `ft01`의 `TARGETS`(층 이름은 모델 구조마다 다르다)와 `MAX_LENGTH`(토크나이저가 다르면 토큰 수도 다르다), 변환할 폴더, `Modelfile`의 `FROM`, 등록 이름 |

모델을 바꿀 때 알아 둘 사실이다. 기준 PC에서 확인한 것과 확인하지 않은 것을 나눠 적는다.

- 확인함: 7주차 lock의 transformers 4.57.6에는 Qwen3.5 구조(`qwen3_5`)가 없다. Qwen3.5 계열을 학습하려면 transformers 5.x가 필요하다(임시 환경에 5.24.0을 설치해 구조가 있는 것만 확인했다).
- 확인함: llama.cpp `ccd360f`의 변환기에는 `Qwen3_5ForConditionalGeneration`이 등록되어 있다(코드만 확인했다).
- 확인하지 않음: Qwen3.5 계열의 LoRA 학습 메모리·시간, GGUF 변환, Ollama 등록, 채점 점수.
- 확인함: 기준 PC(Windows 11)에서 0.5B를 fp32·체크포인팅 없이 학습하면 torch가 잡는 메모리가 8GB를 넘었다. 이때 오류 없이 step 시간만 늘어났다. 더 큰 모델은 같은 설정에서 더 쉽게 넘친다고 예상하지만 재지 않았다.
- 확인함: `qwen3.5:2b`(Q8_0, ID `0689d44085e0`)와 `bge-m3`(ID `790764642607`)를 `rag_bot`으로 함께 쓰면 Ollama 0.40.17의 `/api/ps` 기준 VRAM에 2.20GiB와 0.64GiB가 모두 올라갔고, 공개 20문항이 문항당 1초 안에 끝났다.
- 확인하지 않음: 2B 모델을 기준 PC(8GB)에서 LoRA로 학습할 때와 f16 GGUF로 등록해 `bge-m3`와 함께 올릴 때의 메모리. 2B f16 가중치만 4GB 안팎이라 빠듯할 수 있다.
- 확인함: Ollama 0.40.17은 Qwen2 구조의 safetensors 폴더를 바로 등록하지 못한다. GGUF로 바꿔 등록한다.

## 기준 PC 실측

Windows 11, RTX 5060 8GB, Ollama 0.40.17, `finetune/`의 lock(torch 2.11.0+cu128, transformers 4.57.6, peft 0.18.1)에서 이 문서의 명령으로 2026-11-23에 잰 값이다. 학습 문항은 `lab_shared/data`의 공개 학습 문항 40건(v0)이다. 다른 PC에서는 수업 전에 다시 잰다.

| 단계 | 값 |
|---|---|
| `uv run ft01` | 600~761토큰, 30 step, `train_runtime` 33.5초(명령 전체 43초). torch 최대 할당 2,485MiB, nvidia-smi 최고 6,299MiB(측정 전 1,042MiB 포함) |
| `uv run ft02` | 29초 |
| f16 GGUF 변환 | 24초, 994MB |
| `ollama create wku-lora` | 2초 안팎 |

## 막히는 곳

| 증상 | 확인할 것 |
|---|---|
| `error: Failed to spawn: ft01`(`program not found`) | 다른 프로젝트 폴더에서 실행했다. `ex04`~`ex07`은 `examples/`, `prepare`·`ft01`·`ft02`·변환·`ollama create`는 `finetune/`에서 실행한다 |
| `ft01`이 Ollama 모델 이름을 알려 주고 멈춤 | `ollama ps`에 나온 모델을 `ollama stop <이름>`으로 내린다 |
| `prepare`가 `OSError: [Errno 22] ... huggingface\token`으로 멈춤 | `HF_HOME`이 없는 드라이브를 가리킨다. 쓸 수 있는 폴더로 정한다 |
| Hugging Face 캐시로 받다가 `WinError 1314`(심볼릭 링크 권한)로 끊김 | `prepare`처럼 `local_dir`로 받는다 |
| `ImportError`가 패키지 안의 빈 파일에서 남 | uv 캐시 파일이 손상됐을 수 있다. `uv cache clean <패키지>` 뒤 `uv sync --reinstall-package <패키지>` |
| 학습 step 시간이 점점 늘어남(오류 없음) | VRAM이 넘쳐 시스템 RAM을 쓰고 있다. `DTYPE`·`GRADIENT_CHECKPOINTING`과 다른 앱의 VRAM 사용량을 본다 |
| 다시 학습했는데 점수가 그대로 | 변환 명령이 이전 병합 폴더를 읽었는지 본다. 입력 폴더를 새 `MERGED_DIR`로 바꾼다 |
| `ollama create -q ...`가 `only supported for safetensors imports`로 실패 | GGUF는 변환기의 `--outtype`으로 양자화한다 |
