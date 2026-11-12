"""내가 수정한 답변 예시로 LoRA를 학습하고 어댑터를 저장한다."""

from peft import LoraConfig, get_peft_model
from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments, set_seed

from shared import ADAPTER_DIR, DATA_DIR, DEVICE, load_model
from shared.training import training_examples

STEPS = 30  # 느린 CPU에서는 3으로 줄여 저장·불러오기부터 확인한다.
# STEPS = 300  # 선택 실험. 횟수를 늘려도 답변 품질 개선을 보장하지 않는다.
LEARNING_RATE = 5e-4
RANK = 8
MAX_LENGTH = 256
SEED = 42


def main():
    if ADAPTER_DIR.exists():
        raise SystemExit("이미 저장한 어댑터가 있습니다. shared의 ADAPTER_DIR을 run-002 등으로 바꾸세요.")
    set_seed(SEED)
    tokenizer, base = load_model()
    examples = training_examples(tokenizer, DATA_DIR / "sample_sft.jsonl", MAX_LENGTH)
    model = get_peft_model(base, LoraConfig(
        task_type="CAUSAL_LM", r=RANK, lora_alpha=2 * RANK,
        target_modules=["q_proj", "v_proj"],
    ))
    model.config.use_cache = False
    model.print_trainable_parameters()
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir="outputs/trainer", max_steps=STEPS,
            per_device_train_batch_size=1, gradient_accumulation_steps=2,
            learning_rate=LEARNING_RATE, logging_steps=1,
            save_strategy="no", report_to="none", seed=SEED,
            use_cpu=DEVICE == "cpu", dataloader_pin_memory=False,
            optim="adamw_torch",
        ),
        train_dataset=examples,
        data_collator=DataCollatorForSeq2Seq(tokenizer, label_pad_token_id=-100),
    )
    trainer.train()
    model.save_pretrained(ADAPTER_DIR)
    tokenizer.save_pretrained(ADAPTER_DIR)
    print(f"어댑터 저장 완료: {ADAPTER_DIR}. uv run ex04로 다시 불러와 비교하세요.")
