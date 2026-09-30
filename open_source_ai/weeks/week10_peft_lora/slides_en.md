---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 10"
footer: "Lightweight Fine-Tuning with PEFT/LoRA"
---

# Week 10
## Lightweight Fine-Tuning with PEFT/LoRA

**Three 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Session | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Changing a small part instead of relearning everything | Attaching an adapter and counting trainable parameters |
| Block 2 | How data reaches the model: templates, masking, Trainer | LoRA-training a class-assistant tone |
| Block 3 | Saving, comparing, and logging adapters | Before/after comparison and the run-001 experiment log |

This week's question: **what must you fix, and what must you log, for a training run that takes only minutes to be reproducible?**

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Changing a Small Part Instead of Relearning Everything

---

## 0–3 min · Three Ways to Adapt a Model

```text
Prompting:        weights stay fixed, only the instructions change   (Week 4 Modelfile)
Full fine-tuning: every weight is retrained                          (tens of GB of VRAM)
PEFT:             weights are frozen, only a small add-on is trained (this week)
```

- Reusing a pretrained model's knowledge is transfer learning.
- The question isn't "what do we change" but **"what do we freeze."**

**Question:** What was something you couldn't do with a Week 4 system prompt?

---

## 3–6 min · Full Fine-Tuning vs. PEFT

| Item | Full fine-tuning | PEFT (LoRA) |
|---|---|---|
| Trainable parameters | 100% | 0.1–2% |
| Optimizer state | parameter count × 8 bytes | only the trainable ones |
| Saved artifact | a full copy of the model | an adapter, tens of MB |
| Reverting to the original | needs a separate backup | just detach the adapter |

You can **swap several adapters** onto the same base model.

---

## 6–10 min · LoRA Intuition: ΔW = BA

```text
Original layer: y = W x                 W: (out × in), frozen
LoRA layer:     y = W x + (alpha / r) · B A x
                A: (r × in)  B: (out × r)   r ≪ in, out
```

- `r` (rank): the inner dimension. Larger means more capacity and more parameters together.
- `alpha`: scales the adapter's output. Convention: `alpha = 2r`.
- `target_modules`: names of the linear layers to attach to — usually `q_proj, k_proj, v_proj, o_proj`.

After training, `W + (alpha/r)·BA` lets you **merge** back into the original shape.

---

## 10–13 min · Four Chunks of Training Memory

```text
Weights:      parameter count × 2 bytes (bf16)
Gradients:    trainable parameters × 4 bytes
Optimizer:    trainable parameters × 8 bytes (Adam's 1st and 2nd moments)
Activations:  batch × sequence length × hidden × layers × (a constant)
```

- Full fine-tuning applies the first three lines to **every** parameter.
- With LoRA, lines two and three shrink to about 1%, while **activations stay the same**.

**Question:** For full fine-tuning a 0.5B model, how many GB is the optimizer state alone?

---

## 13–16 min · What Fits in 12 GB

| Model size | Method | Rough VRAM | Fits in 12 GB? |
|---|---|---|---|
| 0.5B | LoRA · bf16 · seq 512 | 3–5 GB | Plenty of room |
| 1.5B | LoRA · bf16 · seq 512 | 6–10 GB | Possible with a smaller batch |
| 7B | LoRA · bf16 | 16+ GB | Not possible |
| 7B | 4-bit quantization + LoRA (QLoRA) | 6–10 GB | Possible (outside this course's scope) |

This week's attitude: **build a prediction table, then correct it with measurements.**

---

## 16–18 min · What a Prompt Can Do, and What Needs LoRA

- Prompting is enough for: role instructions, output language, one or two formatting rules.
- LoRA is needed for: a **consistent format or tone** the model keeps failing to follow, domain vocabulary, shortening a long instruction.
- Even LoRA can't do: adding facts the model doesn't know (-> RAG, Week 7).

Demo: `uv run python lora_setup.py --ranks 4,8,16`

```text
trainable params: 1,081,344 || all params: 495,114,112 || trainable%: 0.2184
```

---

## 18–20 min · Handoff to Lab

[Block 1 lab — Attaching an Adapter and Counting Trainable Parameters](lab.md#1교시-실습--어댑터-붙이고-학습-파라미터-세기) · [Period files](examples/period1/README.md)

Completion criteria:

1. A table of trainable parameter counts and percentages for r=4, 8, 16.
2. A VRAM prediction table broken into weights, training state, activations, and total.
3. One sentence on how the percentage changes when you shrink `target_modules`.

30 min lab, then a 10 min break; Block 2 follows.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## How Data Reaches the Model: Templates, Masking, Trainer

---

## 0–3 min · SFT Data: A Question-Answer Pair

```json
{"instruction": "Why do I need to commit the uv.lock file?",
 "output": "Key point: …\nReason: …\nNext step: …"}
```

- `data/sample_sft.jsonl`: about 50 self-written Korean Q&A pairs about the course.
- Every answer follows the same **key point / reason / next step** three-line format — that's the "tone" we're changing.
- No real people or institutions are named. The same rule applies to your team's data.

**Question:** With 50 examples, what can it learn, and what can't it?

---

## 3–7 min · The chat Template: How a String Becomes Input

```text
<|im_start|>system
You are the assistant for the Open Source AI Applications course. …<|im_end|>
<|im_start|>user
Why do I need to commit the uv.lock file?<|im_end|>
<|im_start|>assistant
Key point: uv.lock is …<|im_end|>
```

- `tokenizer.apply_chat_template(messages)` adds the model's special tokens.
- The template used in training **must match** the template used at inference.
- Fix the system prompt to the **same sentence** across training and comparison too.

---

## 7–10 min · Label Masking: Learning Only the Answer

```text
Tokens: [system…] [user…] [assistant\n] [Key point: …] [<|im_end|>]
Labels:  -100 …     -100 …   -100          kept as-is    kept as-is
```

- Loss is computed only where the label isn't `-100`.
- If you train on the prompt too, the model spends capacity **imitating the question**.
- Demo: `uv run python train_lora.py --inspect`

**Question:** If every label is `-100`, what happens to the loss?

---

## 10–14 min · Trainer Structure

```text
TrainingArguments  ─ lr, epochs, batch, accumulation, seed, bf16, log interval
Dataset            ─ input_ids · attention_mask · labels
DataCollator       ─ pads each batch to a matching length (labels padded with -100)
Trainer.train()    ─ repeats forward → loss → backward → optimizer.step()
```

```python
trainer = Trainer(model=model, args=training_args,
                  train_dataset=dataset, data_collator=collator)
trainer.train()
trainer.state.log_history   # per-step loss
```

This turns the training loop you wrote by hand in Week 6 **into configuration**.

---

## 14–17 min · Five Hyperparameters

| Name | Default | If you change it |
|---|---|---|
| `--lr` | 2e-4 | Too high: loss spikes. Too low: no change. |
| `--epochs` | 2 | Too many: it memorizes (shows up in the Week 11 eval) |
| `--batch-size` | 4 | Scales with VRAM |
| `--grad-accum` | 2 | Effective batch = batch × accum |
| `--rank` | 8 | See the Block 1 table |

Change **only one at a time**, and give the run a new name.

---

## 17–18 min · seed and Reproducibility

```powershell
uv run python train_lora.py --seed 42 --run-name run-001
```

- `set_seed(42)` fixes the randomness in initialization, shuffling, and dropout.
- Same seed, data, and settings -> nearly identical loss curves (GPU kernel differences remain).
- `adapters/run-001/run_config.json` automatically saves the full configuration.

---

## 18–20 min · Handoff to Lab

[Block 2 lab — LoRA-Training a Class-Assistant Tone](lab.md#2교시-실습--수업-도우미-말투로-lora-학습하기) · [Period files](examples/period2/README.md)

Completion criteria:

1. From the `--inspect` output, you recorded the number of masked tokens and the number of trainable tokens.
2. `adapters/run-001/` contains the adapter and `run_config.json`.
3. `outputs/train-run-001.json` records the first and last loss, and the measured peak VRAM.

30 min lab, then a 10 min break; Block 3 follows.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Saving, Comparing, and Logging Adapters

---

## 0–3 min · What's Inside an Adapter Folder

```text
adapters/run-001/
├─ adapter_config.json          r, alpha, target_modules, base model name
├─ adapter_model.safetensors    just the B·A matrices (a few MB)
├─ tokenizer*.json, …           the same tokenizer, for comparison and serving
└─ run_config.json              the training config and loss history this run leaves behind
```

- The base model's weights are **not** included — you need the same base model to reattach it.
- Commit the **log**, not the adapter, to the repository (`adapters/` is in `.gitignore`).

---

## 3–7 min · Three Paths: Load, Disable, Merge

```python
model = PeftModel.from_pretrained(base, "adapters/run-001")
with model.disable_adapter():     # same object, base-model output
    base_text = generate(...)
lora_text = generate(...)         # output with the adapter on
merged = model.merge_and_unload() # W + (alpha/r)·BA → a standalone model
```

- For comparison, use `disable_adapter()` — you never load the model twice.
- For serving or conversion, use `merge_and_unload()` then `save_pretrained()`.

**Question:** Between a merged model and the adapter form, which one takes more storage?

---

## 7–11 min · Designing a Fair Before/After Comparison

| Fix this | Value |
|---|---|
| Prompts | the same 5 (`data/eval_prompts.json`) |
| System prompt | the same sentence used in training |
| Decoding | greedy (`do_sample=False`), same `max_new_tokens` |
| seed / dtype / device | the same values |

- Mix in a **question outside the training topic** among the 5 (p4, p5).
- Look at what got worse — repetition, unsupported claims — alongside what got better.

---

## 11–15 min · Experiment Log Format: Only What Reproduction Needs

```text
1 Purpose            what this experiment is meant to check
2 Fixed values        model ID/revision, data version, system prompt, seed, device
3 Configuration        r/alpha/dropout, targets, lr, epochs, batch×accum
4 Results             steps, time, VRAM predicted vs. measured, loss start->end
5 Sample outputs       3+ before/after pairs + format-compliance rate
6 Observations/failures  what differed from expectations, the first line of any error
7 Next experiment      the one variable to change next
```

Copy `EXPERIMENT_TEMPLATE.md` into `experiments/run-001.md`. **Weeks 11–12 and Project 3 reuse this exact format.**

---

## 15–17 min · Failures Are Data Too

| Symptom | Check first |
|---|---|
| Loss never goes down | Is `trainable params` 0? Are all labels -100? |
| Loss is NaN | Halve the lr; switch fp16 to bf16 |
| CUDA out of memory | Halve batch, double accum, shrink `--max-len` |
| Before/after outputs are identical | The adapter path, or where `disable_adapter()` is called |
| The answer loops forever | Too many epochs; check `max_new_tokens` and eos |

**Question:** What do you lose by deleting a failed run from your log?

---

## 17–18 min · Extending: Importing into GGUF / Ollama

```text
merge.py  →  models/merged-run-001/ (safetensors)
          →  imported via FROM in an Ollama Modelfile   (official import docs)
          →  or converted to GGUF, then FROM ./model.gguf
```

- The same flow as Week 4's `ollama create` — reused in the Week 12 service.
- Check the exact procedure and supported architectures against Ollama's official documentation.

---

## 18–20 min · Handoff to Lab

[Block 3 lab — Before/After Comparison and the run-001 Experiment Log](lab.md#3교시-실습--전후-비교와-실험-기록-run-001) · [Period files](examples/period3/README.md)

Completion criteria:

1. `outputs/compare-run-001.md` has before/after outputs for all 5 prompts, and the format-compliance count.
2. All 7 sections of `experiments/run-001.md` are filled in with real measured values.
3. `git log` shows only log files committed — not the adapter weights.

30 min lab, then a 10 min break, leading into this week's summary.

---

## This Week's Summary

```text
Fix:  model ID/revision, data version, system prompt, seed, decoding settings
Log:  trainable-parameter ratio, VRAM predicted vs. measured, loss curve, before/after outputs, failures
```

- LoRA is a way to learn by attaching **a small matrix next to frozen weights**.
- Evidence that training worked isn't the loss — it's a **before/after comparison under matched conditions**.
- Next week (Week 11): clean and split this data, then evaluate the before/after models quantitatively and qualitatively.
