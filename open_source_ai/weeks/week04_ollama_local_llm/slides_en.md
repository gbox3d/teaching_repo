---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 4"
footer: "Ollama and Local LLMs"
---

# Week 4
## Ollama and Local LLMs

**3 × 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Block | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | How a model actually runs | Run two models and measure them |
| Block 2 | Talking over the REST API | Talk over the REST API and handle failures |
| Block 3 | Modelfile, system prompts, Project 1 | Build a class-assistant model and check the project |

This week's question: **how does a language model actually run on my PC's GPU, and how does my program talk to it?**

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## How a Model Actually Runs

---

## 0–3 min · Carrying Over: From Config to Calling It

Week 3's `config.py` reads `OLLAMA_HOST`/`OLLAMA_MODEL`, but hasn't called anything yet.

```text
Week 3: read config    → config.py
Week 4: actually call  → ollama run … → /api/chat → Modelfile
```

- Today's model is **already cached before class**. Don't run `ollama pull` during the lab
- The default model name is set by the `OLLAMA_MODEL` environment variable (textbook default `qwen3:8b`, CPU fallback `qwen3:0.6b`)

**Question:** When we say "run a model," what exactly moves from disk into memory?

---

## 3–6 min · Three Pieces of an LLM's Execution

```text
text ─ tokenizer ─▶ token IDs ─▶ [weights × context] ─▶ next-token probabilities ─▶ one token
                                        ▲                                  │
                                        └──────── append and repeat ───────┘
```

| Piece | What it is | What sets its size |
|---|---|---|
| Weights | Trained matrices of numbers | Parameter count × bytes per parameter |
| Tokenizer | Text ↔ token ID conversion table | Vocabulary size |
| Context | Tokens seen so far and the compute cache (KV) | `num_ctx` × number of layers |

Generation is **one token at a time, repeated**. That's why speed is measured in tokens/s.

---

## 6–9 min · Quantization: Same Model, Different Bytes

| Notation | Bytes per parameter | 8B model weights |
|---|---:|---:|
| FP16/BF16 | 2 | about 16 GB |
| Q8_0 | about 1 | about 8 GB |
| Q4_K_M | about 0.6 | about 5 GB |

- GGUF is the file format the llama.cpp family uses, and most Ollama library models use it
- Going down to Q4 improves size and speed, but **answer quality drops a bit**. How much depends on the model and the task

**Question:** For the same `qwen3:8b`, `ollama list`'s SIZE and `ollama ps`'s SIZE differ. What got added?

---

## 9–12 min · Parameter Count → Rough VRAM Estimate

```text
memory needed ≈ parameter count × bytes per parameter + context (KV cache) + headroom
```

| Model | Q4 weights | On a 12 GB GPU |
|---|---:|---|
| 0.6B | about 0.5 GB | Plenty of room. Usable on CPU too |
| 4B | about 2.5 GB | Plenty of room |
| 8B | about 5.2 GB | Plenty of room. This week's default model |
| 14B | about 9 GB | Need to lower `num_ctx` |
| 32B | about 20 GB | Doesn't fit. Falls back to CPU → very slow |

The numbers are estimates — **`ollama ps` gives the real measurement.**

**Question:** To fit a 14B model into 12 GB, what has to give?

---

## 12–15 min · Ollama's Four Parts

```text
ollama serve (server, :11434) ◀── ollama run/show/ps/list (CLI = client)
        │                   ◀── my program (HTTP, Block 2)
        ├─ model storage  %USERPROFILE%\.ollama\models  (blobs + manifests)
        └─ Modelfile  → ollama create (Block 3)
```

- The CLI is also a **client** sending HTTP to the server. If the server dies, neither the CLI nor my code works
- Storage location can be moved with `OLLAMA_MODELS`. Lab PCs use whatever path the environment reference table sets
- Library naming is `name:tag` (`qwen3:8b`). The tag encodes size and quantization

---

## 15–17 min · Five CLI Commands for Today

```powershell
ollama list              # cached models and file sizes
ollama show qwen3:8b     # parameters, quantization, context length
ollama run qwen3:8b      # chat. /set verbose shows speed, /bye exits
ollama ps                # models loaded in memory, SIZE, GPU share
ollama pull qwen3:0.6b   # download — don't use this during class
```

A slow first reply from `ollama run` is **load time**. It's fast from the second reply on.

---

## 17–20 min · Lab Handoff

[Block 1 Lab — Run Two Models and Measure Them](lab.md#1교시-실습--모델-두-개를-실행하고-측정하기)

Completion criteria:

1. You copied the default model's parameter count, quantization, context length, and file size from `ollama show`/`ollama list`
2. You recorded `/set verbose`'s eval rate and `ollama ps`'s SIZE/PROCESSOR for 2 models
3. `model_report.md` has one sentence per question comparing the two models' answers to the same 3 questions

30-minute lab, then a 10-minute break. Block 2 after the break.

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Talking Over the REST API

---

## 0–3 min · Carrying Over: Is the Server Alive?

In Block 1 you chatted with `ollama run`. Now **my code** talks to the same server.

```powershell
Invoke-RestMethod http://localhost:11434/api/tags |
  Select-Object -ExpandProperty models | Format-Table name, size
```

- `/api/tags` lists cached models. If this one line works, you've confirmed the server, port, and model name all at once
- If a day has passed, the model won't be in memory. A slow first call is normal

---

## 3–6 min · `/api/generate` vs. `/api/chat`

| | `/api/generate` | `/api/chat` |
|---|---|---|
| Input | one `prompt` string | a `messages` array (with roles) |
| Conversation history | you append it yourself | just push onto the array |
| Response body | `response` | `message.content` |
| Used for | one-shot transform/summary | assistants and chatbots |

Both use the same model and return the same metadata (`eval_count`, etc.). This week's client uses **`/api/chat`**.<br>
There's also an OpenAI-compatible path (`/v1/chat/completions`), but we don't use it this week.

---

## 6–9 min · Message Roles and History

```json
{"model": "qwen3:8b",
 "messages": [
   {"role": "system",    "content": "Answer in Korean, in three sentences or fewer."},
   {"role": "user",      "content": "What is uv?"},
   {"role": "assistant", "content": "uv is …"},
   {"role": "user",      "content": "How is it different from pip?"}
 ],
 "stream": false, "think": false, "options": {"temperature": 0.2}}
```

- `system`: role and constraints. Stays in effect for the whole conversation
- The server doesn't remember history. **The client sends the full history every time.**

**Question:** As the conversation grows longer, what eventually exceeds `num_ctx`?

---

## 9–12 min · Streaming: JSON, Line by Line

With `"stream": true`, the response doesn't arrive all at once — it comes as **one JSON object per line (NDJSON)**.

```text
{"message":{"role":"assistant","content":"u"},"done":false}
{"message":{"role":"assistant","content":"v "},"done":false}
…
{"message":{"role":"assistant","content":""},"done":true,"eval_count":57,"eval_duration":812345678}
```

- Concatenate the pieces to get the full answer. The metadata only appears on **the last line**
- The perceived delay to the user is the time to the first chunk (load + prompt processing)

**Question:** If you only print each chunk to the screen without collecting them, what do you lose?

---

## 12–15 min · options and think

| Key | Meaning | Lab default |
|---|---|---|
| `temperature` | 0 picks only the highest-probability token; higher means more variety | 0.2 |
| `num_ctx` | Context window token count (KV cache size) | 4096 |
| `num_predict` | Max tokens to generate | 256 |
| `seed` | Same value gives the same sampling sequence | none |

```json
"think": false
```

Turn off the **thinking text** so only the answer shows, and leave your reasoning as a code comment instead.

- The default model `qwen3:8b` is **hybrid**, so this one line actually turns thinking off
- `qwen3:4b`/`30b`/`235b` without a suffix are reasoning-only builds and can't be turned off ([tag-selection guidance](../README.md#생성-모델-태그를-고를-때))

---

## 15–17 min · Response Metadata and Two Kinds of Failure

```text
tokens/s = eval_count ÷ (eval_duration ÷ 1e9)      duration is in nanoseconds
```

- `prompt_eval_count`/`eval_count`: input/output token counts
- `done_reason`: `stop` (the model finished) or `length` (hit `num_predict`)

| Failure | What the code gets | What to tell the user |
|---|---|---|
| Server down / wrong port | `ConnectError` | Check the server and `OLLAMA_HOST` |
| Wrong model name | HTTP 404 | Check the name with `ollama list` |

**Question:** If `done_reason` is `length`, what should you change in the code?

---

## 17–20 min · Lab Handoff

[Block 2 Lab — Talk Over the REST API and Handle Failures](lab.md#2교시-실습--rest-api로-대화하고-실패를-다루기)

Completion criteria:

1. You found `eval_count`/`eval_duration` in `chat.py`'s `outputs/chat-*.json` and computed tokens/s by hand
2. Both a connection failure and a missing model produced a human-readable message and a nonzero exit code
3. After adding `--seed`, you wrote a paragraph on how the answers differ between temperature 0 and 1

30-minute lab, then a 10-minute break. Block 3 after the break.

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Modelfile, System Prompts, and Project 1

---

## 0–3 min · Carrying Over: Where Does the Role Live?

Block 2's `chat.py` sent the role via `--system` every time. Bake the same role **into a model's name**, and any client gets the same assistant.

```text
Method A: a system message per request  → the client's responsibility (Block 2)
Method B: Modelfile → ollama create      → the server's responsibility (today)
Method C: fine-tuning (Week 10)          → the weights' responsibility
```

**Question:** How much more disk space does a model built with Method B take up?

---

## 3–6 min · Four Modelfile Instructions

```text
FROM qwen3:8b                          # base model (cached name or GGUF path)
SYSTEM """You are a lab assistant for this class. …"""   # system prompt
PARAMETER temperature 0.3              # default option; the request's options wins
PARAMETER num_ctx 4096
# TEMPLATE: the prompt-assembly template. Usually left as inherited from FROM
```

- `ollama show qwen3:8b --modelfile` shows the base model's full Modelfile
- Instructions are uppercase; multi-line strings use `"""`. `#` is a comment

---

## 6–9 min · `ollama create` Doesn't Copy the Weights

```powershell
ollama create osa-helper -f Modelfile
ollama list                 # osa-helper shows up
ollama show osa-helper      # a System entry is attached
ollama rm osa-helper        # delete it — the base model stays
```

- The weight blobs are **shared with the base model**; only a new system-prompt/parameter layer is created
- Use lowercase, digits, and `-` for names. Prefix with a team name to avoid clashes (`team-a-helper`)

**Question:** If you `ollama rm qwen3:8b`, what happens to `osa-helper`?

---

## 9–12 min · Designing a System Prompt

| Element | Bad example | Good example |
|---|---|---|
| Role | "A helpful AI" | "A lab assistant for Open Source AI Applications" |
| Constraints | "Answer well" | "5 sentences or fewer, in Korean, say so if unsure" |
| Output format | None | "Commands as a single PowerShell code block" |
| Safety | None | "Never ask for tokens or passwords" |

**Change one thing at a time and compare before/after with the same question** — that's the only way to know what actually worked.

---

## 12–14 min · What a Prompt Can and Can't Do

- Works: tone, length, language, output format, refusal rules, role-play
- Doesn't work well: knowledge the model **doesn't have**, obeying dozens of rules at once, consistent domain terminology
- Knowledge → Week 7's RAG (feed in documents); fixing tone/format → Week 10's LoRA (change the weights)

**Question:** Why can't "tell me our class's assignment deadline" be solved with a prompt alone?

---

## 14–17 min · Project 1

[Assignment brief](assignment_brief.md) · [Rubric](assignment_rubric.md)

| Deliverable | Where it comes from |
|---|---|
| Collaborative repo (LICENSE, README, Issue, PR, Review) | Week 2 |
| uv project (`pyproject.toml`, `uv.lock`, `.env.example`) | Week 3 |
| `chat`/`stream` subcommand CLI + error handling + `outputs/` | Week 4 Block 2 |
| `model_report.md` + before/after Modelfile comparison | Week 4 Blocks 1 & 3 |

Submit **the repo URL + the final commit id + the README's reproduction steps**. Weights and deadlines follow the school's course documents.

---

## 17–20 min · Lab Handoff

[Block 3 Lab — Build a Class-Assistant Model and Check the Project](lab.md#3교시-실습--수업-도우미-모델-만들기와-과제-점검)

Completion criteria:

1. Your custom model shows up in `ollama list`, and you called it by passing its name to `chat.py --model`
2. You made a comparison table of the base model, custom model, and the answer after a one-line SYSTEM change, all for the same 3 questions
3. You listed the blank items on the Project 1 checklist and your plan to fill them

30-minute lab, then a 10-minute break. End of this week.

---

## This Week's Summary

```text
weights × quantization → VRAM        measured with ollama show / ps
server :11434 ← CLI ← my code        /api/chat + stream + think:false + options
Modelfile → ollama create            role on the server, knowledge in RAG, tone fixed with LoRA
```

Estimate the numbers, then **confirm them by measuring**. Turn failure messages into sentences a person can read.
