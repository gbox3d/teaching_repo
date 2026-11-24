"""학습 명령들이 함께 쓰는 모델·경로 설정. 7주차 shared와 같은 역할이다. 명령은 finetune/ 루트에서 실행한다."""

import json
from pathlib import Path
from urllib.request import ProxyHandler, build_opener

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"  # 같은 파일을 받도록 Hugging Face commit을 고정한다.
BASE_DIR = Path("models/Qwen2.5-0.5B-Instruct")  # prepare가 받는 기본 모델. 학습·병합·GGUF 변환이 함께 쓴다.
SFT_DIR = Path("../outputs/sft")  # examples/의 ex06이 만든 학습 파일 위치
ADAPTER_DIR = Path("adapters/wku-run-001")
# ADAPTER_DIR = Path("adapters/wku-run-002")
MERGED_DIR = Path("models/wku-lora-merged")
# MERGED_DIR = Path("models/wku-lora-merged-002")  # 바꾸면 GGUF 변환 명령의 입력 폴더도 같이 바꾼다.
DEVICE = "auto"  # "cpu"로 바꾸면 GPU 없이 실행한다(매우 느리다).


def device() -> str:
    if DEVICE != "auto":
        return DEVICE
    return "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"


def load_model(dtype=torch.float32):
    if not (BASE_DIR / "config.json").exists():
        raise SystemExit(f"{BASE_DIR}에 기본 모델이 없습니다. 먼저 uv run prepare를 실행하세요.")
    # 7주차와 같이 Transformers 4.57.x의 로컬 Qwen 오탐 경고를 피하고 원래 토큰 분할 규칙을 유지한다.
    tokenizer = AutoTokenizer.from_pretrained(BASE_DIR, fix_mistral_regex=False)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(BASE_DIR, dtype=dtype)
    print(f"모델: {MODEL_ID}@{REVISION[:7]} / dtype: {dtype} / 장치: {device()}")
    return tokenizer, model.to(device())


def loaded_ollama_models() -> list[str]:
    """Ollama가 GPU 메모리에 올려 둔 모델 이름. Ollama가 꺼져 있으면 빈 목록이다."""
    try:
        with build_opener(ProxyHandler({})).open("http://127.0.0.1:11434/api/ps", timeout=5) as response:
            return [model["name"] for model in json.load(response).get("models", [])]
    except OSError:
        return []


def prepare() -> None:
    """수업 전에 기본 모델을 BASE_DIR에 받는다. 이미 받은 파일은 다시 받지 않는다."""
    from huggingface_hub import snapshot_download

    snapshot_download(MODEL_ID, revision=REVISION, local_dir=BASE_DIR)
    print(f"기본 모델 준비 완료: {BASE_DIR}")
