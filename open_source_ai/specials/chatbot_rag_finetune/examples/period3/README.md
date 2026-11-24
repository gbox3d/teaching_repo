# 특강 3교시: 학습 예시와 LoRA 학습·등록

학습 예시는 `examples/` 루트에서, 학습·병합·변환·등록은 `finetune/` 루트에서 실행한다. 기본 모델 받기, GGUF 변환기 준비, 학습 전 모델(`wku-base`) 등록은 수업 전에 끝내 둔다. 순서와 명령은 [따라하기](../../walkthrough.md)에 있다.

읽을 파일은 [ex06_make_sft](../src/ex06_make_sft/__init__.py), [학습](../../finetune/src/ft01_train/__init__.py), [병합](../../finetune/src/ft02_merge/__init__.py), [학습 설정](../../finetune/src/shared/__init__.py)이다. 학습·병합 코드는 7주차 `ex03`·`ex05`와 순서가 같다. 7주차와 달라진 값은 [따라하기의 표](../../walkthrough.md#2-학습과-병합finetune)에서 확인한다.

학습 문항은 `src/lab_shared/data`의 질문·정답 JSON이고, 학습 예시는 `ex06`이 학습 문항으로 만든 대화(특강 루트의 `outputs/sft/train.jsonl`)다.

## 목표

- 공개된 학습 문항으로 `rag_bot`이 실제로 보낼 대화를 만들고, 평가 문항이 섞이지 않았는지 확인한다.
- Qwen2.5-0.5B-Instruct를 LoRA로 학습해 GGUF로 바꾸고 Ollama에 등록한다.
- 학습 전(`wku-base`)과 학습 뒤(`wku-lora`)를 같은 채점기와 같은 문항으로 잰다.

## 실행

```powershell
# examples/에서
uv run ex06
ollama ps
ollama stop bge-m3
cd ../finetune
uv run ft01
uv run ft02
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 `
  python tools/llama.cpp/convert_hf_to_gguf.py `
  models/wku-lora-merged --outfile models/wku-lora.gguf --outtype f16
ollama create wku-lora -f Modelfile.lora
ollama list
cd ../examples
```

`ex06`은 검색에 `bge-m3`를 써서 Ollama에 모델이 올라가 있다. `ft01`은 Ollama가 올린 모델이 있으면 이름을 알려 주고 멈추므로, `ollama ps`에 나온 모델을 모두 내린 뒤 실행한다.

등록한 뒤 `src/ex04_my_eval/__init__.py`의 `BOT`이 `"rag_bot"`인지 확인하고, `src/rag_bot/__init__.py`의 `MODEL`을 `"wku-lora"`로 바꿔 `uv run ex04`로 잰다. `BOT`이 `"student_bot"`이면 `MODEL`을 바꿔도 점수가 달라지지 않는다. `MODEL`만 `"wku-base"`로 바꿔 한 번 더 재면 학습 전후를 비교할 수 있다.

## 30분 실습 흐름

1. 학습 문항을 훑고 `ex06`으로 학습 예시를 만든다. 제외된 문항이 있으면 이유를 기록한다.
2. Ollama 모델을 내리고 `finetune/`으로 옮겨 `ft01`을 실행한다. 도는 동안 7주차 `ex03`과 달라진 상수를 읽는다.
3. `ft02`, GGUF 변환, `ollama create` 순서로 등록하고 `ollama list`로 확인한다.
4. `examples/`로 돌아와 `ex04`로 `wku-lora`와 `wku-base`를 각각 `mine`·`public`으로 재고 기록표에 적는다.

`wku-lora`가 틀린 문항은 `id`를 실습지 3교시 표에 적고 `ex04` 출력을 파일로 남긴다([1교시 안내](../period1/README.md#터미널-출력을-파일로-남기기)). 4교시에는 `ex07`의 `BOT`을 `"rag_bot"`으로 두고, 3교시 끝에 `"wku-base"`로 바꿔 둔 `rag_bot`의 `MODEL`을 자기 모델(예: `"wku-lora"`)로 되돌린 뒤 그 문항의 `질문` 줄을 그대로 입력한다. 증상별로 확인할 값은 [추론 버그 잡기](../debugging.md)에 있다.

공개된 학습 문항은 일부다. 학습 문항을 늘리고 다듬는 일은 과제에서 학생이 한다. 평가 문항(공개 20문항, 내 문항, 비공개 문항)을 학습 데이터에 그대로 옮기지 않는다.
