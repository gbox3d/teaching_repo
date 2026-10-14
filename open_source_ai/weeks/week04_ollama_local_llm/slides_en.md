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
Each block: 20 min talk & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Block | 20 min talk & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | How a model runs | Run a model in the terminal, read the numbers |
| Block 2 | Chatting with the Python library | Run and change `ex01`–`ex05` |
| Block 3 | Image input, tool calling, Modelfile | `ex06`·`ex07`, add a function, my helper model |

This week's question: **what do I need to run a public open-source model on my PC and use it from my own program?**

---

<!-- _class: lead -->

# Block 1 · 20 min talk
## How a Model Runs

---

## 0–3 min · Today We Use, Not Build

| What | Open source | License |
|---|---|---|
| Program that runs the model | Ollama | MIT |
| Model (weights) | Qwen3.5 2B | Apache-2.0 |
| Tool to call it from Python | `ollama` library | MIT |

- The model is **downloaded before class** (`ollama pull qwen3.5:2b`, about 2.7 GB).
- We don't write servers, HTTP, or error handling. We **read, run, and change** what others have shared.

**Question:** When we "run a model," what exactly moves from disk into memory?

---

## 3–6 min · Three Pieces of an LLM Run

```text
text ─ tokenizer ─▶ token IDs ─▶ [weights × context] ─▶ next-token probabilities ─▶ one token
                                       ▲                                              │
                                       └──────────────── append and repeat ───────────┘
```

| Piece | What it is | What sets its size |
|---|---|---|
| Weights | Trained matrices of numbers | Parameters × bytes per parameter |
| Tokenizer | Text ↔ token ID table | Vocabulary size |
| Context | Tokens so far and the compute cache | Conversation length |

Generation is **one token at a time, repeated**. That's why speed is in tokens/s.

---

## 6–9 min · Quantization: Same Model, Different Bytes

| Tag | Bytes per parameter | `qwen3.5:2b` download |
|---|---:|---:|
| `2b-bf16` | 2 | 4.6 GB |
| `2b` = `2b-q8_0` | about 1 | 2.7 GB |
| `2b-q4_K_M` | about 0.6 | 2.0 GB |

- Less precise numbers make the model smaller and faster, but **answer quality drops a little.**
- This model's file also includes a part that reads images (projector) (Block 3).

**Question:** If `ollama list` SIZE and `ollama ps` SIZE differ, what was added?

---

## 9–12 min · Parameter Count → Rough Memory Estimate

```text
memory needed ≈ weight size + context + headroom
```

| Model (Qwen3.5) | Download | On an 8 GB GPU |
|---|---:|---|
| `0.8b` | 1.3 GB | Plenty of room. Fine on CPU too |
| `2b` | 2.7 GB | Plenty of room. **This week's model** |
| `4b` | 3.3 GB | Plenty of room |
| `9b` | 6.6 GB | Tight |
| `27b` | 17.5 GB | Won't fit. Shares with CPU → very slow |

These are estimates. **`ollama ps` gives the real number.**

---

## 12–15 min · Ollama's Four Parts

```text
Ollama server (:11434) ◀── ollama run/show/ps/list   (terminal, Block 1)
        │              ◀── Python ollama library     (my program, Blocks 2·3)
        ├─ model store   %USERPROFILE%\.ollama\models
        └─ Modelfile → ollama create                 (Block 3)
```

- Terminal commands and the Python library are both **clients** asking the same server. If the server is off, neither works.
- On Windows, if the Ollama app is running, the server is running.
- Model names are `name:tag` (`qwen3.5:2b`). The tag means size and quantization.

---

## 15–17 min · Five Commands for Today

```powershell
ollama list                            # downloaded models and file sizes
ollama show qwen3.5:2b                 # parameters, quantization, Capabilities
ollama run qwen3.5:2b --think=false    # chat. /set verbose shows speed, /bye exits
ollama ps                              # loaded models, SIZE, GPU/CPU
ollama pull qwen3.5:2b                 # download — once, before class
```

- `--think=false`: turns off the thinking text printed before the answer.
- A slow first reply is **load time** (moving the model into memory). It's fast after that.

---

## 17–20 min · Lab Handoff

[Block 1 Lab — Run a Model in the Terminal and Read the Numbers](lab.md#1교시-실습--터미널에서-모델-실행하고-숫자-읽기) · [Block 1 guide](examples/period1/README.md)

Completion criteria:

1. You copied the parameter count, quantization, and Capabilities from `ollama show`.
2. You wrote down the `/set verbose` eval rate and the `ollama ps` SIZE and PROCESSOR.
3. You wrote one sentence on why `ollama list` SIZE and `ollama ps` SIZE differ.

30-minute lab, then a 10-minute break. Block 2 after the break.

---

<!-- _class: lead -->

# Block 2 · 20 min talk
## Chatting with the Python Library

---

## 0–3 min · The First Question Is One Call

```python
import ollama

MODEL = "qwen3.5:2b"

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "안녕. 한국어로 한 문장만 인사해 줘."}],
    think=False,
)
print(response.message.content)
```

- The server address, request format, and reply parsing are **done by the library.** We only call `ollama.chat()`.
- If the server is off, the library tells you `Failed to connect to Ollama`.

---

## 3–6 min · Three Message Roles

| `role` | Whose words | Example |
|---|---|---|
| `system` | The helper's role and answer rules | "Python tutor for beginners. One analogy, two sentences." |
| `user` | What the user is asking now | "What is a list?" |
| `assistant` | The model's earlier answer | "A list holds several values in order…" |

`ex02_system_prompt.py`: type at `나>` and compare answers, **changing only system**. Ask another question after the replies; `/bye` exits.

**Question:** system says "in two sentences," but you got five. What does that tell you?

---

## 6–9 min · Streaming: Show It as It Arrives

```python
stream = ollama.chat(model=MODEL, messages=[...], think=False, stream=True)
for part in stream:
    print(part.message.content, end="", flush=True)
```

- With `stream=True`, you don't wait for the full answer. **Pieces** arrive one by one.
- This is the text flowing out in a chatbot window. Total time is the same, but **waiting feels shorter**.
- `ex03_stream.py`: question at `나>` → streamed reply → next question. Exit with `/bye`.

---

## 9–12 min · options and think

```python
ollama.chat(model=MODEL, messages=[...], think=False,
            options={"temperature": 0})
```

| Key | Meaning |
|---|---|
| `temperature` | 0 gives only the most likely answer; higher gives more variety |
| `num_predict` | Max answer length (in tokens) |
| `think` | `False` gives just the answer, no thinking text |

`ex04_temperature.py`: type at `나>`; it asks that question **twice each** at temperature 0 and 1, then waits for more input. `/bye` exits.

**Question:** Which temperature fits an exam-grading helper, and which fits a story-idea helper?

---

## 12–15 min · Memory = Stack the Messages and Resend

```python
messages = [{"role": "system", "content": "한국어로 짧게 답한다."}]
while True:
    messages.append({"role": "user", "content": input("나> ")})
    response = ollama.chat(model=MODEL, messages=messages, think=False)
    messages.append({"role": "assistant", "content": response.message.content})
```

- `ex02`–`ex04` send only the current question. `ex05` also sends earlier questions and answers. Exit with `/bye`.
- Long chats grow the context until it hits the limit. Handling long material: Week 7 RAG.

---

## 15–17 min · The Numbers in the Response

```python
response.message.content   # the answer
response.eval_count        # tokens generated
response.eval_duration     # time spent generating (nanoseconds)
```

```text
tokens/s = eval_count ÷ (eval_duration ÷ 1e9)
```

Same value as the eval rate from Block 1's `/set verbose`. The terminal and Python see **the same numbers from the same server**.

---

## 17–20 min · Lab Handoff

[Block 2 Lab — Chatting from Python](lab.md#2교시-실습--python에서-대화하기) · [Block 2 examples](examples/period2/README.md)

Completion criteria:

1. You added your own role to `ex02_system_prompt.py` and wrote down how the answers differ.
2. You wrote one sentence on the difference between temperature 0 and 1.
3. With memory on and off, you compared the number of "messages sent" and the answers.

30-minute lab, then a 10-minute break. Block 3 after the break.

---

<!-- _class: lead -->

# Block 3 · 20 min talk
## Image Input, Tool Calling, and Modelfile

---

## 0–3 min · What This Model Can Do

```text
ollama show qwen3.5:2b

  Capabilities
    completion     answer in text
    vision         read images
    thinking       show its reasoning
    tools          ask for a function call
```

- Block 2 used only `completion`. Block 3 uses **`vision` and `tools`**.
- Each model has different Capabilities. Check with `ollama show` before using one.

---

## 3–6 min · Image Input: Attach a Picture to the Message

```python
response = ollama.chat(
    model=MODEL,
    messages=[{
        "role": "user",
        "content": "이 화면의 마지막 오류 줄을 그대로 옮겨 적고, 무슨 뜻인지 한 문장으로 설명해 줘.",
        "images": ["error_screen.png"],
    }],
    think=False,
)
```

- A model that reads text and images together is a **VLM** (Vision Language Model).
- `ex06` attaches the image to your first question at `나>` and resends that history for follow-up questions. `/bye` exits.

---

## 6–9 min · What VLMs Do Well, and What to Watch

| Does well | Watch out for |
|---|---|
| Copying text from screens and photos | Tiny text, handwriting |
| Describing what's in a picture | Counting, comparing positions |
| Summarizing tables and graphs | Making up things not in the picture |

Demo: shown an error screen, it reads `ModuleNotFoundError: No module named 'ollama'` exactly. Ask "how do I fix it?" and it may give a **wrong fix**.

**Question:** When reading is right but judgment is wrong, how far should a program trust a VLM?

---

## 9–12 min · Tool Calling: Hand Off What the Model Can't Do

```text
① my program → model    question + function list (get_current_time, multiply)
② model → my program    "please call multiply(a=1234, b=5678)"   ← tool_calls
③ my program            runs the function itself → 7006652
④ my program → model    sends the result as role "tool"
⑤ model → person        "1234 × 5678 = 7,006,652"
```

- The model doesn't know the current time and often gets big math wrong.
- The model **only asks**. **My program** always runs the function.
- In `ex07`, follow up with `그 계산 결과에 2를 곱해 줘.` (multiply that result by 2). `/bye` exits.

---

## 12–14 min · Tool Calling Code: Pass the Function Itself

```python
def multiply(a: float, b: float) -> float:
    """두 수를 곱한다."""
    return a * b

response = ollama.chat(model=MODEL, messages=messages, tools=[multiply], think=False)
for call in response.message.tool_calls or []:
    result = multiply(**call.function.arguments)
    messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})
```

- The library reads the function's **name, types, and docstring** and sends them as a manual to the model.
- Functions taking numbers work well. Small models often miss when text must match exactly.

---

## 14–17 min · Modelfile: Put a Role in a Model Name

```text
FROM qwen3.5:2b
SYSTEM """너는 '오픈소스 AI 응용' 수업의 실습 도우미다. 한국어로 다섯 문장 이내로 답한다."""
PARAMETER temperature 0.3
```

```powershell
ollama create student01-helper -f Modelfile
ollama run student01-helper --think=false
```

- No weights are copied or retrained. It's a **new name** with settings attached.
- A system prompt only changes tone and format. It **doesn't add missing knowledge** (Week 7 RAG, Week 10 LoRA).

---

## 17–20 min · Project 1 and Lab Handoff

[Assignment brief](assignment_brief.md) · [Rubric](assignment_rubric.md) · [Block 3 lab](lab.md#3교시-실습--이미지-인식-툴-콜링-내-도우미-모델) · [Block 3 examples](examples/period3/README.md)

| Deliverable | Where it comes from |
|---|---|
| Collaborative repo (LICENSE, README, Issue, PR, Review) | Week 2 |
| uv project (`pyproject.toml`, `uv.lock`) | Week 3 |
| Chat (memory), image, tool-calling features, `Modelfile`, `week04_report.md` | Week 4 |

Lab done when: your image result, a log of your added function being called, and your model vs. the base model.

---

## This Week's Summary

```text
ollama show / run / ps        read size, capabilities, speed, memory as numbers
ollama.chat(messages=…)       system·user·assistant, stream, temperature, memory = stacked messages
images=[…] / tools=[func]     let it read images; hand what it can't do to my functions
Modelfile → ollama create     role in config, knowledge in RAG, fixed style in LoRA
```

Before building, **find what's already public and use it.** Check results with numbers and comparisons.
