---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 5"
footer: "Hugging Face Hub and Analyzing Public Resources"
---

# Week 5
## Hugging Face Hub and Analyzing Public Resources

**3 × 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Block | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Hub structure and model cards | Model card analysis table and a cache report |
| Block 2 | First inference with a Transformers pipeline | Run classification and generation with a pipeline |
| Block 3 | datasets and recording sources | Explore a dataset and record its sources |

This week's question: **what documents and information tell you whether a public model or dataset is really usable in your project?**

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Hub Structure and Model Cards

---

## 0–3 min · Carrying Over: Beyond the Ollama Library

Week 4's `OLLAMA_MODEL` was a name inside the Ollama library. Today we go to where the original lives.

```text
huggingface.co/
 ├─ models/    Qwen/Qwen2.5-0.5B-Instruct   weights + tokenizer + model card
 ├─ datasets/  org/name                     data files + data card
 └─ spaces/    org/appname                  demo apps
```

- One repo = a **Git repository** (large files via LFS). Addressed as `org/name`
- Today's model is cached before class. Don't fetch a new one during the lab

**Question:** Where does the original weights behind the GGUF file that `ollama pull qwen3:8b` downloads actually live?

---

## 3–6 min · The Order to Read a Model Card

| Order | Item | Question to answer |
|---|---|---|
| 1 | License | Is commercial use, redistribution, modification allowed? |
| 2 | Intended and prohibited uses | Is my use case within the allowed range? |
| 3 | Training data | What was it trained on, and is that public? |
| 4 | Evaluation, limits, bias | What kinds of input is it weak on? |
| 5 | Language, size, format | Korean support, VRAM, whether it's safetensors |

If the card is empty, the answer is **"unknown,"** not "fine."

---

## 6–9 min · Card Metadata Is Also a Search Filter

```yaml
license: apache-2.0
language:
  - en
pipeline_tag: text-generation
base_model: Qwen/Qwen2.5-0.5B
```

- The YAML between the two `---` lines at the top of the card (README.md) is the source of the Hub's search filters, license badge, and task badge
- `license: other` plus a separate terms file is a signal you need to **read the terms directly**
- `base_model` is the lineage. A derived model inherits the original's terms

**Question:** What happens if a model with no `ko` in `language` gets used for Korean?

---

## 9–12 min · Gated Models and Tokens

```text
Reading the card      ── anyone
Downloading the files ── agree to terms (gated) → account token → HF_TOKEN in .env
```

- Llama Community License, Gemma Terms of Use: **open weight**, but with conditions attached
- For licenses not in the SPDX list, write `LicenseRef-name` and summarize the terms in one line
- Keep the token only in `.env`. Never put it in code, slides, or a commit
- You can read the card without a token. Start your analysis without one

**Key point:** clicking "agree" is your signature that you **read the terms**.

---

## 12–14 min · Pinning with a Revision

```python
from transformers import pipeline

clf = pipeline("text-classification", model=MODEL_ID,
               revision="a1b2c3d4e5f6")  # commit hash
```

- `main` moves. The card changes and the weights sometimes get replaced
- A reproducible record = model ID + **commit hash**
- Find the hash on the repo's Files and Versions tab, or in the cache's snapshots folder name

**Question:** What plays the same role here that `uv.lock` played in Week 3?

---

## 14–17 min · Cache Structure, Size, and Offline Mode

```text
HF_HOME/hub/models--Qwen--Qwen2.5-0.5B-Instruct/
 ├─ blobs/                    actual files (named by content hash)
 ├─ refs/main                 → commit hash
 └─ snapshots/COMMIT_HASH/    config.json, model.safetensors → links to blobs
```

- Changing `HF_HOME` moves the cache location. Lab PCs may use a shared location
- Windows can't use symlinks by default, so it **stores files directly in snapshots instead of blobs** (enable Developer Mode for links)
- Rough size: 0.5B parameters × 2 bytes (fp16) ≈ 1 GB. Tokenizer/config files add a bit more
- With `HF_HUB_OFFLINE=1`, only the cache is used, no network. A missing model fails immediately
- `scan_cache_dir()` returns this structure as a table

---

## 17–20 min · Lab Handoff

[Block 1 Lab — Model Card Analysis Table and a Cache Report](lab.md#1교시-실습--모델-카드-분석표와-캐시-보고) · [Block 1 files](examples/period1/README.md)

Completion criteria:

1. `model_cards.md` has 3 models' license, SPDX, intended use, whether training data is public, and limits filled in
2. You recorded the cache location, total size, and commit hash from `cache_report.py`'s output
3. You wrote one sentence on "which of the three we can't use in our project, and why"

30-minute lab, then a 10-minute break. Block 2 after the break.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## First Inference with a Transformers Pipeline

---

## 0–3 min · Carrying Over: From Card to Code

The model ID and commit hash you picked in Block 1 are now arguments in code.

```text
"This class is fun"
   ─ tokenizer ─▶ [101, 9302, …]
   ─ model ─────▶ logits
   ─ postprocess ▶ {"label": "positive", "score": 0.93}
```

```python
from transformers import pipeline
clf = pipeline("text-classification", model=MODEL_ID, revision=COMMIT)
clf("This class is fun")
```

One task name selects preprocessing, model class, and postprocessing as a bundle. In Week 6, we'll split these three steps apart ourselves.

---

## 3–6 min · Task Types and Naming the Model

| Task | Input → output | This week |
|---|---|---|
| `text-classification` | sentence → label + score | sentiment classification |
| `text-generation` | prompt → continuation | class-assistant answers |
| `feature-extraction` | sentence → vector | Week 7 |
| `token-classification` | sentence → per-word tags | comparison only |
| `image-classification` | image → label | comparison only |

Like `pipeline("text-classification")`, omitting the model lets the library pick a default. Convenient, but you didn't choose its license or revision.

**Key point:** always pass `model=` and `revision=`.

---

## 6–9 min · Choosing a Korean Model

Three lines to check on the card:

1. Does `language:` include `ko` or `multilingual`?
2. Does the training data **actually** contain Korean (sometimes it's just a tag)?
3. What do the label names mean — `LABEL_0`, or `positive`/`negative`?

- A multilingual tokenizer can split Korean text, but that's different from understanding it well
- If results look off, check the card's language list before blaming the model

**Question:** If labels only show as `LABEL_0`, `LABEL_1`, where do you find what they mean?

---

## 9–12 min · device and dtype

```python
pipeline(task, model=MODEL_ID, device=0)      # 0: first GPU, -1: CPU
model.to(device="cuda:0", dtype=torch.float16)
```

| dtype | Per parameter | 0.5B model | Notes |
|---|---|---|---|
| float32 | 4 bytes | about 2 GB | default when loading |
| float16 | 2 bytes | about 1 GB | mainly for GPU generation, narrow range |
| bfloat16 | 2 bytes | about 1 GB | wide range, recent GPUs |

- `device_map="auto"` (accelerate) is for splitting across multiple devices. With one 12 GB card, `device=0` is enough
- The dtype argument name is `dtype` or `torch_dtype` depending on version. The examples standardize on `.to()`

---

## 12–15 min · Calling a Generation Model

```python
messages = [{"role": "system", "content": "You are a class assistant. Answer briefly in Korean."},
            {"role": "user", "content": "What should I check before using a model?"}]
prompt = gen.tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True)
out = gen(prompt, max_new_tokens=120, do_sample=False,
          return_full_text=False)
out[0]["generated_text"]
```

- The chat template turns Week 4's system/user roles into the model's own special-token format
- `do_sample=False` is the same as temperature 0. It's the baseline for comparison experiments
- There's no switch like Ollama's `think` option. If the model outputs its reasoning, that's part of the answer too

---

## 15–17 min · Reading Warning Messages and Timing Runs

| Message | Meaning | Action |
|---|---|---|
| `Some weights ... were not used` | Head mismatch | Check that the task and model match |
| `Setting pad_token_id to eos_token_id` | No padding token defined | Usually harmless for generation |
| `sequence length is longer than` | Input truncated | Shorten or split the input |
| `401`/`gated repo` | Terms/token | Agree on the card, set `.env` |

- The first call is a warm-up. **Time from the second call onward**
- GPU timing is only accurate after `torch.cuda.synchronize()`

---

## 17–20 min · Lab Handoff

[Block 2 Lab — Run Classification and Generation with a Pipeline](lab.md#2교시-실습--pipeline으로-분류와-생성-실행하기) · [Block 2 files](examples/period2/README.md)

Completion criteria:

1. Outputs for 5 classification sentences and 1 generation are saved in `outputs/pipeline-*.json`
2. You made a table comparing load/warm-up/inference time on CPU and GPU (or CPU twice)
3. You summarized in one line the failure message for a wrong revision or being offline

30-minute lab, then a 10-minute break. Block 3 after the break.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## datasets and Recording Sources

---

## 0–3 min · Carrying Over: From Model to Data

The commit hash from Block 2's JSON becomes one row in `SOURCES.md`. Now let's fill in the data row.

```python
from datasets import load_dataset

ds = load_dataset("org/name", "config_name", split="train")
ds                 # Dataset({features: [...], num_rows: N})
ds[0]              # first row as a dict
ds.features        # field name → type
ds.info.license    # usually empty — check where it actually lives
```

- A Hub dataset is also a repo: files (parquet, jsonl, csv) + a dataset card
- `split` is a division like train/validation/test. `config` is a sub-dataset within one repo

---

## 3–6 min · Local Files Use the Same API

```python
ds = load_dataset("json", data_files="data/sample_qa.jsonl", split="train")
```

- `json`, `csv`, `parquet`, `text`: your own files become the **same kind of object** as a Hub dataset
- This week's example is 12 hand-written Korean Q&A pairs. Block 3 runs with no network
- Week 10's LoRA training data uses the same format (`jsonl`) too

**Question:** What's the difference between a field shown as `Value('string')` versus `Sequence` in `features`?

---

## 6–9 min · Streaming — Look Without Downloading Everything

```python
from itertools import islice

ds = load_dataset("org/name", split="train", streaming=True)
for row in islice(ds, 5):
    print(row)
```

- `streaming=True` gives an `IterableDataset`. No indexing, no `num_rows`
- Use it to judge the structure and license of a tens-of-GB corpus by just looking at the first 5 rows
- Nothing is cached, so it saves disk space in the lab

**Key point:** for data whose structure you don't know, look at 5 rows first.

---

## 9–12 min · Reading a Dataset Card

| Item | Question to answer |
|---|---|
| Summary, source | Who collected it and how (crawling, human-written, synthetic) |
| Structure | Do the fields, splits, and counts match the card and the actual data? |
| Collection/annotation method | Who labeled it, and are there guidelines? |
| Personal/sensitive info | Does it contain names, contact info, accounts? |
| License | Do the data itself and the annotations have different licenses? |

If the card's row count differs from `dataset_peek.py`'s, **the version differs** or the card is out of date.

---

## 12–15 min · Data Licenses and Risk

| License | Commercial use | Conditions |
|---|---|---|
| CC0-1.0 | Allowed | None |
| CC-BY-4.0 | Allowed | Attribution |
| CC-BY-SA-4.0 | Allowed | Attribution + share derivatives under the same terms |
| CC-BY-NC-4.0 | **Not allowed** | Non-commercial only |
| Research-only, `other` | Usually not allowed | Read the terms yourself |

- Crawled data still carries **the original author's rights**, license or not
- Data containing personal information can't be used regardless of license — this leads into Week 11's PII checks

**Question:** What terms does a model trained on CC-BY-SA data inherit? (There isn't a single fixed answer)

---

## 15–17 min · SOURCES.md — A Source-Tracking Table

```text
| Name | Type | Source URL | Version/revision | License (SPDX) | Use | Changes |
```

- Gather models, data, and even code snippets into **one table**
- Put the commit hash or dataset revision in the version column. Never write "latest"
- Changes column: filtering, cleaning, translation, merging — anything you did to it
- Week 8's Project 2 license-analysis report starts from this table

**Key point:** a source you didn't record **can't be found later**.

---

## 17–20 min · Lab Handoff

[Block 3 Lab — Explore a Dataset and Record Its Sources](lab.md#3교시-실습--데이터셋-살펴보기와-출처-기록표) · [Block 3 files](examples/period3/README.md)

Completion criteria:

1. You recorded the field structure, row count, and 5 samples from `dataset_peek.py`'s output
2. You found the license, collection method, and personal-info items in one public dataset's card
3. `SOURCES.md` lists 2 models + 1 dataset, each with revision, license, and use

30-minute lab, then a 10-minute break. Next week: the tensors and training loop inside the pipeline.

---

## This Week's Summary

```text
Read the card → judge license/use/data → pin a revision → cache and offline mode
pipeline(model=, revision=, device=) → record timing, warnings, commit hash
load_dataset(streaming=) → peek at 5 rows → dataset card → SOURCES.md
```

Being public and **being usable** are different things. Documents and hashes are what you base that judgment on.
