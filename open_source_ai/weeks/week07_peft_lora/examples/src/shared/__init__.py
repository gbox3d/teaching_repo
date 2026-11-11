"""예제들이 함께 쓰는 학습용 모델 설정·대화 함수·데이터 경로. system 지시의 기본값은 SYSTEM_PROMPT다."""

from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
SYSTEM_PROMPT = "당신은 그리스·로마 신화를 소개하는 안내자입니다. 한국어로 짧게 답하세요."
MAX_NEW_TOKENS = 120
DEVICE = "auto"  # "cpu"로 바꾸면 GPU 없이 실행한다.
DATA_DIR = Path(__file__).parent / "data"
ADAPTER_DIR = Path("adapters/run-001")
MERGED_DIR = Path("models/merged-run-001")


def load_model():
    device = DEVICE
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32)
    model = model.to(device).eval()
    print(f"모델: {MODEL_ID} / 장치: {device}")
    return tokenizer, model


def messages(question, system=SYSTEM_PROMPT):
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]


def answer(model, tokenizer, question, system=SYSTEM_PROMPT):
    inputs = tokenizer.apply_chat_template(
        messages(question, system), add_generation_prompt=True,
        tokenize=True, return_dict=True, return_tensors="pt",
    ).to(model.device)
    with torch.inference_mode():
        output = model.generate(
            **inputs, max_new_tokens=MAX_NEW_TOKENS, do_sample=False,
            temperature=None, top_p=None, top_k=None,
            pad_token_id=tokenizer.pad_token_id,
        )
    new_tokens = output[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def questions():
    print("질문을 입력하세요. 종료: /bye (각 질문은 독립적으로 보냅니다.)")
    while True:
        try:
            question = input("나> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if question == "/bye":
            return
        if question:
            yield question


def prepare():
    """수업 전에 학습용 모델과 토크나이저를 다운로드한다."""
    load_model()
    print("모델 준비 완료. 다음 실행부터 다운로드한 파일을 재사용합니다.")
