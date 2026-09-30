"""2교시 — 자체 작성 SFT 데이터로 LoRA 어댑터를 학습한다.

실행 예:
  uv run python train_lora.py --inspect                 # 템플릿·라벨 마스킹만 확인하고 종료
  uv run python train_lora.py                           # 기본 2 epoch, adapters/run-001/
  uv run python train_lora.py --device cpu --max-steps 5 --batch-size 1   # GPU 없을 때
결과: adapters/<run-name>/ (어댑터·토크나이저·run_config.json), outputs/train-<run-name>.json
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from typing import Any

# common 이 .env 를 읽는다. HF_HOME·HF_HUB_OFFLINE 은 huggingface 라이브러리가 import 될 때
# 한 번만 읽히므로, common 을 datasets·peft·transformers 보다 먼저 import 해야 .env 값이 적용된다.
from common import (
    DEFAULT_TARGET_MODULES,
    OUTPUTS_DIR,
    build_messages,
    cuda_peak_mb,
    gpu_name,
    load_jsonl,
    load_tokenizer,
    load_tokenizer_and_model,
    model_id_from_env,
    resolve_device,
    resolve_dtype,
    split_modules,
    write_json,
)

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments, set_seed

IGNORE_INDEX = -100  # 손실 계산에서 제외할 라벨 값(transformers 관례)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LoRA SFT 학습")
    parser.add_argument("--model", default=model_id_from_env())
    parser.add_argument("--data", default="data/sample_sft.jsonl")
    parser.add_argument("--run-name", default="run-001")
    parser.add_argument("--output-dir", default="adapters")
    parser.add_argument("--rank", type=int, default=8)
    parser.add_argument("--alpha", type=int, default=16)
    parser.add_argument("--dropout", type=float, default=0.05)
    parser.add_argument("--target-modules", default=DEFAULT_TARGET_MODULES)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--max-steps", type=int, default=-1, help="양수면 epoch 대신 이 step 수만 학습")
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--grad-accum", type=int, default=2)
    parser.add_argument("--max-len", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--logging-steps", type=int, default=1)
    parser.add_argument("--gradient-checkpointing", action="store_true")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="auto", choices=["auto", "fp32", "bf16", "fp16"])
    parser.add_argument("--inspect", action="store_true", help="첫 샘플의 템플릿·마스킹만 출력하고 종료")
    return parser.parse_args()


def encode_example(tokenizer: Any, row: dict[str, Any], max_len: int) -> dict[str, list[int]]:
    """instruction/output 한 쌍을 chat template로 감싸고, 프롬프트 구간 라벨을 -100으로 가린다."""
    prompt_text = tokenizer.apply_chat_template(
        build_messages(row["instruction"]), tokenize=False, add_generation_prompt=True
    )
    full_text = tokenizer.apply_chat_template(
        build_messages(row["instruction"], row["output"]), tokenize=False
    )
    prompt_ids = tokenizer(prompt_text, add_special_tokens=False)["input_ids"]
    full_ids = tokenizer(full_text, add_special_tokens=False)["input_ids"][:max_len]
    labels = list(full_ids)
    for index in range(min(len(prompt_ids), len(labels))):
        labels[index] = IGNORE_INDEX
    return {"input_ids": full_ids, "attention_mask": [1] * len(full_ids), "labels": labels}


def show_inspect(tokenizer: Any, row: dict[str, Any], encoded: dict[str, list[int]]) -> None:
    masked = sum(1 for value in encoded["labels"] if value == IGNORE_INDEX)
    print("=== chat template 적용 결과 (첫 샘플) ===")
    print(tokenizer.apply_chat_template(build_messages(row["instruction"], row["output"]), tokenize=False))
    print(f"=== 토큰 수 {len(encoded['input_ids'])} · 라벨 가림 {masked} · 학습 대상 {len(encoded['input_ids']) - masked} ===")
    learn_ids = [tok for tok, lab in zip(encoded["input_ids"], encoded["labels"]) if lab != IGNORE_INDEX]
    print("학습 대상 토큰만 복원:", repr(tokenizer.decode(learn_ids)))


def main() -> None:
    args = parse_args()
    if args.device == "cpu":
        # CUDA 초기화 전에 가려야 Trainer도 CPU만 본다.
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    device = resolve_device(args.device)
    dtype = resolve_dtype(args.dtype, device)
    set_seed(args.seed)

    rows = load_jsonl(Path(args.data))
    if args.inspect:
        # 템플릿·마스킹 확인에는 토크나이저만 있으면 된다. 모델 가중치를 읽지 않아 CPU에서도 바로 끝난다.
        tokenizer = load_tokenizer(args.model)
        print(f"모델: {args.model} · 데이터 {len(rows)}건 · --inspect: 학습하지 않고 첫 샘플만 확인한다")
        show_inspect(tokenizer, rows[0], encode_example(tokenizer, rows[0], args.max_len))
        return

    tokenizer, model = load_tokenizer_and_model(args.model, device, dtype)
    print(f"모델: {args.model} · 장치: {device} · dtype: {dtype} · 데이터 {len(rows)}건")

    dataset = Dataset.from_list(rows)
    dataset = dataset.map(lambda row: encode_example(tokenizer, row, args.max_len), remove_columns=dataset.column_names)
    lengths = [len(item) for item in dataset["input_ids"]]
    print(f"토큰 길이: 최소 {min(lengths)} · 최대 {max(lengths)} · 평균 {sum(lengths) / len(lengths):.1f}")

    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()
        model.config.use_cache = False

    lora_config = LoraConfig(
        r=args.rank, lora_alpha=args.alpha, lora_dropout=args.dropout,
        target_modules=split_modules(args.target_modules), bias="none", task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    adapter_dir = Path(args.output_dir) / args.run_name
    use_bf16 = device.type == "cuda" and dtype == torch.bfloat16
    use_fp16 = device.type == "cuda" and dtype == torch.float16
    training_args = TrainingArguments(
        output_dir=str(OUTPUTS_DIR / f"trainer-{args.run_name}"),
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_steps=0.05,  # 1 미만이면 전체 step 대비 비율(5%)로 해석된다
        logging_steps=args.logging_steps,
        save_strategy="no",
        report_to="none",
        seed=args.seed,
        bf16=use_bf16,
        fp16=use_fp16,
        remove_unused_columns=False,
        dataloader_pin_memory=device.type == "cuda",
    )
    collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True, label_pad_token_id=IGNORE_INDEX)
    trainer = Trainer(model=model, args=training_args, train_dataset=dataset, data_collator=collator)

    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    result = trainer.train()
    elapsed = round(time.perf_counter() - started, 1)

    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    losses = [{"step": log["step"], "loss": log["loss"]} for log in trainer.state.log_history if "loss" in log]
    run_config = {
        "run_name": args.run_name, "model": args.model, "data": args.data, "data_rows": len(rows),
        "lora": {"r": args.rank, "alpha": args.alpha, "dropout": args.dropout, "target_modules": split_modules(args.target_modules)},
        "train": {"epochs": args.epochs, "max_steps": args.max_steps, "lr": args.lr, "batch_size": args.batch_size,
                  "grad_accum": args.grad_accum, "max_len": args.max_len, "seed": args.seed},
        "env": {"device": str(device), "gpu": gpu_name(), "dtype": str(dtype)},
        "result": {"global_steps": trainer.state.global_step, "train_loss": round(result.training_loss, 4),
                   "elapsed_sec": elapsed, "max_vram_mb": cuda_peak_mb(),
                   "first_loss": losses[0]["loss"] if losses else None, "last_loss": losses[-1]["loss"] if losses else None},
        "loss_history": losses,
    }
    write_json(adapter_dir / "run_config.json", run_config)
    out_path = write_json(OUTPUTS_DIR / f"train-{args.run_name}.json", run_config)
    print(f"\n학습 완료: {trainer.state.global_step} step · {elapsed}s · 최대 VRAM {cuda_peak_mb()} MB")
    print(f"loss {run_config['result']['first_loss']} → {run_config['result']['last_loss']}")
    print(f"어댑터: {adapter_dir} · 기록: {out_path}")


if __name__ == "__main__":
    main()
