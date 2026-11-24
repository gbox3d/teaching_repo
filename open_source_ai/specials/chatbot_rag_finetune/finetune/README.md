# 특강 학습: Qwen2.5-0.5B-Instruct LoRA 학습과 병합

7주차와 같은 torch·transformers·peft 버전으로 원광대 챗봇용 LoRA를 학습하고, GGUF로 바꿔 Ollama에 등록한다. 학습 예시는 옆 폴더 [examples](../examples/README.md)의 `ex06`이 특강 폴더의 `outputs/sft/`에 만든다.

| 명령 | 진입점 | 하는 일 |
|---|---|---|
| `uv run prepare` | [shared](src/shared/__init__.py) | 기본 모델을 고정 commit으로 `models/Qwen2.5-0.5B-Instruct/`에 받는다(수업 전) |
| `uv run ft01` | [ft01_train](src/ft01_train/__init__.py) | `outputs/sft/train.jsonl`로 LoRA를 학습해 `adapters/wku-run-001/`에 저장한다 |
| `uv run ft02` | [ft02_merge](src/ft02_merge/__init__.py) | 어댑터를 기본 모델에 합쳐 `models/wku-lora-merged/`에 저장한다 |

명령은 `pyproject.toml`이 있는 이 폴더에서 실행한다. GGUF 변환, `Modelfile.base`·`Modelfile.lora`로 하는 `ollama create`, 7주차와 달라진 설정, 기준 PC 실측은 [따라하기](../walkthrough.md)에 있다.

이 폴더의 `adapters/`, `models/`, `outputs/`, `tools/llama.cpp/`는 학습·변환 산출물과 내려받은 도구라 커밋하지 않는다. CUDA용 PyTorch는 7주차와 같은 cu128 저장소에서 받으며, `uv run python -c "import torch; print(torch.version.cuda, torch.cuda.is_available())"`가 `12.8 True`를 출력하는지 수업 전에 확인한다.
