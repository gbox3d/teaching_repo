---
marp: true
theme: default
paginate: true
header: "Open-Source AI Applications · Week 7"
footer: "LoRA with our own answer examples"
---

# Week 7
## Learning LoRA with our own answer examples

Ollama chat → edit data and train → save and reload → chat again

Three 60-minute blocks: 20-minute lesson + 30-minute lab + 10-minute break

---

## This week’s sequence

| Period | 20-minute lesson and demo | 30-minute lab |
|---|---|---|
| 1 | Inference and training tools | Chat with Ollama and a small model |
| 2 | Example answers and LoRA | Edit data, train, and save |
| 3 | Reload, compare, and run a merged model | Compare matching questions and record |

Required: edit your data and chat with a saved adapter.
Rank, VRAM estimates, and masking internals are optional.

---

## Before class · CUDA PyTorch in TOML

`examples/pyproject.toml` already declares `torch>=2.6,<3` in `dependencies`.
These settings select the package download source:

```toml
[[tool.uv.index]]
name = "pytorch-cuda"
url = "https://download.pytorch.org/whl/cu128"
explicit = true

[tool.uv.sources]
torch = [
  { index = "pytorch-cuda", marker = "sys_platform == 'win32' or sys_platform == 'linux'" },
]
```

Installing a CUDA build and choosing the runtime device are separate steps.

<!-- Source: https://docs.astral.sh/uv/guides/integration/pytorch/ -->

---

## Before class · What the TOML options mean

| Setting | Meaning |
|---|---|
| `cu128` | CUDA 12.8 wheels; the existing course example |
| `explicit = true` | Use this index only for packages explicitly assigned to it |
| `tool.uv.sources` | Assign `torch` to the `pytorch-cuda` index |
| `marker` | Apply on Windows/Linux; macOS uses PyPI and can use MPS |

Choose the CUDA build for the course baseline, GPU, and NVIDIA driver.
For an unchanged copy: `uv sync --locked`.
After editing the index: `uv lock` → `uv sync`; distribute the updated lock too.

[Setup details](examples/README.md#cuda용-pytorch-설치-설정) · [uv PyTorch guide](https://docs.astral.sh/uv/guides/integration/pytorch/)

---

## Before class · Check GPU access

Run in your personal project copy on a Windows/Linux NVIDIA PC:

```powershell
nvidia-smi
uv sync --locked
uv run python -c "import torch; print(torch.version.cuda, torch.cuda.is_available())"
uv run prepare
```

- `12.8 True`: this CUDA build can use the GPU.
- `None False`: CPU build; CUDA version + `False`: check GPU and driver compatibility.
- `prepare` should report `장치: cuda`; auto selection otherwise uses MPS or CPU.

Ollama using the GPU does not confirm that Python's PyTorch can use it.

<!-- Sources: https://pytorch.org/get-started/locally/ ; https://docs.astral.sh/uv/guides/integration/pytorch/ -->

---

<!-- _class: lead -->

# Period 1 · 20-minute lesson
## Connecting Ollama chat to training tools

---

## 0–3 min · Previous work and today’s task

Weeks 4–5: ask an Ollama model and receive an answer.
Week 6: retrieve myth passages and include them in the question.

Today: **train a small model on answer examples we edit**.

Edit data → train → save → reload and chat

We keep the mythology topic and the question input loop.

---

## 3–6 min · Prompting, RAG, and LoRA

| Method | What changes | Example |
|---|---|---|
| Prompting | Instructions in the input | Ask for a three-line introduction |
| RAG | Reference text in the input | Retrieve a myth passage |
| LoRA | A small set of trainable weights | Learn the answer format from examples |

Use prompting when it already solves the problem.
If a small model ignores the instruction, teach the format with example answers.
LoRA neither replaces retrieval nor guarantees factual answers.

---

## 6–9 min · Roles of the tools

| Tool | Role |
|---|---|
| Ollama | Run a prepared model and expose a chat API |
| Transformers | Load models/tokenizers and generate in Python |
| PEFT | Add LoRA to the base model |
| Trainer | Run training on prepared examples |

We load the model in Python to access the trainable parts.
The PyTorch special lecture is not a prerequisite, and you do not write a training loop.

---

## 9–12 min · Familiar Ollama chat

```powershell
uv run ex01
```

Question: `아테나를 소개해 줘.` (“Introduce Athena.”)

Append a format instruction to `PROMPT` in `ex01_ollama` and rerun:

```python
PROMPT = SYSTEM_PROMPT + " 이름, 소개, 기억할 점을 한 줄씩 답하세요."
```

(Name, introduction, and a fact to remember: one line each.)

Only the instruction changed. No training. Exit with `/bye`.

---

## 12–15 min · A small model for training

Opening chat: `qwen3.5:2b` from the earlier weeks
Training and comparison: `Qwen/Qwen2.5-0.5B-Instruct` (small enough to train in class)

```powershell
# After /bye in ex01, unload the Ollama model (8 GB GPU)
ollama stop qwen3.5:2b
uv run ex02
```

Add the same format instruction to `PROMPT` in `ex02`.
Course test PC: the 2B model answered in three lines; the 0.5B model in one or two sentences.
When a small model ignores the instruction, **teach the format with example answers**.

No training yet. Measure training effects on the same 0.5B model.

---

## 15–18 min · Tokens and answer generation

Read `load_model()` and `answer()` in `shared`.

```text
Question + system instruction
    ↓ tokenizer.apply_chat_template
Tokens the model can read
    ↓ model.generate
Newly generated tokens
    ↓ tokenizer.decode
An answer to display
```

Load the model once, then repeat the question loop.

---

## 18–20 min · Period 1 lab handoff

[Period 1 lab](lab.md#1교시-실습--ollama-대화와-학습-도구-연결) · [Source guide](examples/period1/README.md)

- `ex01`: answers before and after the format instruction
- `ex02`: two questions → blank input → `/bye` → same format instruction
- Explain inference versus training in one sentence
- Save two questions to ask again later

Each question is independent; this example has no chat memory.
30-minute lab, then a 10-minute break.

---

<!-- _class: lead -->

# Period 2 · 20-minute lesson
## Training LoRA on edited answer examples

---

## 0–3 min · A question and its target answer

`src/shared/data/sample_sft.jsonl`

```json
{"instruction":"제우스는 누구야?",
 "output":"이름: 제우스\n소개: ...\n기억할 점: ..."}
```

The actual file stores one JSON object per line.
`\n` means a line break in the answer.

24 myth summaries written for this course; the target is a three-line format.

---

## 3–6 min · What students change

In all 24 answers, replace `기억할 점:` (“a fact to remember”) with a label of your own.
VS Code `Ctrl+H` → Replace All

```text
기억할 점: 올빼미와 올리브나무가 상징입니다.
    ↓
한 줄 요약: 올빼미와 올리브나무가 상징입니다.
```

In period 3, check whether the answers after training use the new label.
Editing one fact is optional; check it separately from the format.
Do not add the evaluation answers to the training file.

---

## 6–9 min · What LoRA trains

```text
Base model: keep the pretrained weights fixed
    +
LoRA adapter: small weights updated on our examples
    ↓
Answer after training
```

We are not training a whole model from scratch.
The saved adapter needs **the same base model**.
Rank calculations belong to the optional advanced exercise.

---

## 9–12 min · Three operations in the training code

`src/ex03_train/__init__.py`

```python
model = get_peft_model(base, LoraConfig(...))
# Pass the prepared data and model to Trainer
trainer.train()
model.save_pretrained(ADAPTER_DIR)
```

Attach → train → save

`shared/training.py` handles tokenization and answer-only labels.
Students read that implementation in the optional exercise.

---

## 12–15 min · Settings and execution

Constants at the top of `ex03_train`:

```python
STEPS = 30
LEARNING_RATE = 5e-4
RANK = 8
```

```powershell
uv run ex03
```

For the first run, edit only the data and keep settings fixed.
The 3-step CPU path checks training, saving, and reloading.

---

## 15–18 min · Loss and saved files

Loss measures fit to the training answers.

- It can go up and down during training.
- Lower loss does not guarantee better answers to new questions.

```text
adapters/run-001/
  adapter_config.json
  adapter_model.safetensors
  tokenizer files
```

Use a new `ADAPTER_DIR` for another training run.

---

## 18–20 min · Period 2 lab handoff

[Period 2 lab](lab.md#2교시-실습--내-답변-예시로-lora-학습) · [Source guide](examples/period2/README.md)

- Rename the label and record why you chose it
- Run `ex03`; check the new label in the first output and the actual loss
- Check the adapter configuration and weights
- Record the model, device, and settings used

Successful training and improved answers are separate checks.
30-minute lab, then a 10-minute break.

---

<!-- _class: lead -->

# Period 3 · 20-minute lesson
## Reloading and chatting with the result

---

## 0–3 min · Reloading the saved adapter

```python
tokenizer, base = load_model()
model = PeftModel.from_pretrained(base, ADAPTER_DIR).eval()
```

```powershell
uv run ex04
```

A new process loads the base model and the saved adapter.
No retraining. Do not attach it to a different base model.

---

## 3–6 min · Before and after on the same question

`ex04` prints two answers for each question.

```text
나> 아테나를 소개해 줘.
학습 전> (answer with the adapter disabled)
학습 후> (answer with the adapter enabled)
```

`나>` = you, `학습 전>` = before training, `학습 후>` = after training

Fixed: base model, question, system text, length, greedy decoding
Changed: whether the adapter is enabled

Do not use the 2B Ollama answer as the 0.5B baseline.

---

## 6–9 min · Check format and facts separately

| Observation | What to check |
|---|---|
| Format | Three lines that use your new label |
| Facts | Whether the description matches reference material |
| Side effects | Repetition, truncation, or forced myth formatting |

Not in the training data: `다이달로스를 소개해 줘.` (“Introduce Daedalus.”)
Outside mythology: `uv.lock 파일은 어떤 역할을 해?` (“What does the uv.lock file do?”)
Read questions from `shared/data/eval_prompts.json` and type them.

A changed format does not guarantee factual accuracy.
With RAG, check both retrieved evidence and the answer.

---

## 9–12 min · Python chat with the merged model

```text
Base model + LoRA adapter
    ↓ merge_and_unload() → save_pretrained()
models/merged-run-001/
```

```powershell
uv run ex05
uv run ex06
```

`ex06` loads the model and tokenizer from `MERGED_DIR` with Transformers.
Question → answer → next question → `/bye`. Each question is independent.
The full model is about 2 GB (adapter: about 2 MB). Optional; check disk space first.

---

## 12–15 min · Optional: running the result in Ollama

```powershell
ollama create week07-lora -f Modelfile
ollama run week07-lora
```

After checking `ex06` chat, convert to GGUF. [Prepare the converter](examples/ollama_import.md) before class.
`Modelfile`: `FROM ./models/week07-lora.gguf`

Set `MODEL = "week07-lora"` in `ex01` to reuse
the original `uv run ex01` chat code.

Importing is not training. Verify support before class.

---

## 15–18 min · Experiment record and limits

`experiments/run-001.md`

- The new label, why you chose it, and actual training settings
- Loss observations and save/reload checks
- Before/after answers and fact checks
- What stayed the same or got worse; one thing to change next

Running it in Ollama checks deployment behavior.
Use `ex04` under matching conditions for training comparisons.
A short run and a few questions do not prove general improvement.

---

## 18–20 min · Period 3 lab handoff

[Period 3 lab](lab.md#3교시-실습--저장한-결과로-다시-대화) · [Source guide](examples/period3/README.md)

- Compare before/after answers with `ex04`
- Exit and restart to check save/reload behavior
- Record format, facts, and side effects separately
- Optional: `ex05` merge → `ex06` Python chat → Ollama import

Record unchanged or worse results too.
30-minute lab, then a 10-minute break.

---

## Next class and optional topics

Week 9 uses Streamlit to let users chat with a prepared model.
We revisit this experiment in the later data and evaluation labs.

[Rank, memory, and masking](examples/advanced.md)

References: [PEFT](https://huggingface.co/docs/peft/quicktour) · [Model card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) · [Ollama import](https://docs.ollama.com/import)
