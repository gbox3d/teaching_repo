"""ex06이 만든 학습 파일로 LoRA를 학습하고 어댑터를 저장한다. 7주차 ex03과 같은 순서다.
7주차와 다른 점: 학습 예시가 system·user·assistant 대화 전체이고, 검색 문서가 들어가 길이가 길다."""

import json

import torch
from peft import LoraConfig, get_peft_model
from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments, set_seed

from shared import ADAPTER_DIR, DEVICE, SFT_DIR, load_model, loaded_ollama_models

STEPS = 30
LEARNING_RATE = 2e-4
RANK = 16
MAX_LENGTH = 1024  # 검색 문서 3개가 든 예시가 들어가는 길이. 7주차 256으로는 모자란다.
SEED = 42
DTYPE = torch.bfloat16  # 8GB GPU 기준. torch.float32로 바꾸면 메모리가 더 든다.
GRADIENT_CHECKPOINTING = True  # 중간 계산을 다시 해서 메모리를 아낀다. 끄면 빨라지지만 메모리가 늘어난다.
TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def training_examples(tokenizer) -> list[dict]:
    path = SFT_DIR / "train.jsonl"
    if not path.exists():
        raise SystemExit(f"{path}가 없습니다. examples/에서 uv run ex06으로 학습 파일을 먼저 만드세요.")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    examples = []
    for row in rows:
        prompt_ids = tokenizer.apply_chat_template(row["messages"][:-1], add_generation_prompt=True)
        full_ids = tokenizer.apply_chat_template(row["messages"])
        # 대화 앞부분(system·user)은 정답이 아니다. assistant의 JSON 토큰만 loss 계산에 쓴다.
        labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]
        examples.append({"input_ids": full_ids, "attention_mask": [1] * len(full_ids), "labels": labels})
    lengths = [len(example["input_ids"]) for example in examples]
    print(f"학습 예시 {len(examples)}건, 토큰 수 최소 {min(lengths)} 최대 {max(lengths)} (MAX_LENGTH {MAX_LENGTH})")
    if max(lengths) > MAX_LENGTH:
        raise SystemExit("MAX_LENGTH보다 긴 예시가 있습니다. rag_bot의 TOP_K를 줄여 ex06을 다시 실행하세요.")
    settings = json.loads((SFT_DIR / "settings.json").read_text(encoding="utf-8"))
    print("학습 파일을 만든 때의 rag_bot 설정:", settings)
    return examples


def main():
    if ADAPTER_DIR.exists():
        raise SystemExit("이미 저장한 어댑터가 있습니다. shared의 ADAPTER_DIR을 wku-run-002 등으로 바꾸세요.")
    loaded = loaded_ollama_models()
    if loaded:
        raise SystemExit(f"Ollama가 GPU에 올려 둔 모델이 있습니다: {', '.join(loaded)}. "
                         "ollama stop <모델 이름>으로 내린 뒤 다시 실행하세요.")
    set_seed(SEED)
    tokenizer, base = load_model(DTYPE)
    examples = training_examples(tokenizer)
    model = get_peft_model(base, LoraConfig(
        task_type="CAUSAL_LM", r=RANK, lora_alpha=2 * RANK, target_modules=TARGETS,
    ))
    model.config.use_cache = False
    if GRADIENT_CHECKPOINTING:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        model.enable_input_require_grads()
    model.print_trainable_parameters()
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="outputs/trainer", max_steps=STEPS,
            per_device_train_batch_size=1, gradient_accumulation_steps=4,
            learning_rate=LEARNING_RATE, logging_steps=1,
            save_strategy="no", report_to="none", seed=SEED,
            use_cpu=DEVICE == "cpu", dataloader_pin_memory=False,
            optim="adamw_torch", bf16=DTYPE == torch.bfloat16,
        ),
        train_dataset=examples,
        # 길이를 64토큰 단위로 맞춘다. 길이가 제각각이면 GPU 메모리 조각이 쌓여 step이 많을 때 VRAM을 넘긴다.
        data_collator=DataCollatorForSeq2Seq(tokenizer, label_pad_token_id=-100, pad_to_multiple_of=64),
    )
    trainer.train()
    model.save_pretrained(ADAPTER_DIR)
    tokenizer.save_pretrained(ADAPTER_DIR)
    if torch.cuda.is_available():
        print(f"GPU 최대 할당 메모리: {torch.cuda.max_memory_allocated() / 2**20:.0f} MiB")
        # 예약은 PyTorch가 잡아 둔 메모리다. 할당보다 훨씬 크면 메모리 조각이 쌓인 것이다.
        print(f"GPU 최대 예약 메모리: {torch.cuda.max_memory_reserved() / 2**20:.0f} MiB")
    print(f"어댑터 저장 완료: {ADAPTER_DIR}. uv run ft02로 기본 모델과 병합하세요.")
