---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Reasoning Tips and Tricks
## Start with input → model call → output

Python · LangChain · Ollama · `qwen3.5:2b`

```powershell
cd open_source_ai/specials/reasoning_tips/examples
uv sync --locked
uv run ex01
```

Input: **딸기 3개에서 두 사람이 1개씩 먹으면 몇 개 남나요?**
“Two people each eat one of three strawberries. How many are left?” Expected answer: one.
Exit with `/bye`, then try the same Korean question in `uv run ex02` and `uv run ex03`.

---

## ex01 · Receive the complete response in main

`uv run ex01` · call flow in `src/ex01_baseline/__init__.py`:

```python
model = create_model()
question = input("나> ").strip()
reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
print("AI>", reply.text if reply.text.strip() else EMPTY_ANSWER)
```

The `while` in `main()` repeats input; `/bye` ends it.
`invoke()` receives one complete response. `reply.text` is the answer string.

Send only the current question. Reasoning is enabled but unread.
An empty body produces a notice. Unhandled reasoning is not disabled reasoning.

---

## ex02 · Inspect the complete response

`uv run ex02` · `src/ex02_observe/__init__.py`:

```python
reply = model.invoke([("system", CHAT_PROMPT), ("human", question)])
thought = reply.additional_kwargs.get("reasoning_content") or ""
done_reason = reply.response_metadata.get("done_reason") or "미제공"
if thought:
    print("추론>", thought)
```

After completion: `추론>` raw reasoning → counts/end reason → `AI>` body.
Skip raw reasoning when empty. This is not live output.

One independent question per request.
`length` means the generation limit was reached. It does not prove a loop.
In ex01/ex02, `/clear` reports that there is no history to clear.

---

## ex03 · Put generation control in a recovery function

`uv run ex03` · call in `src/ex03_recover/__init__.py`:

```python
from shared.recovery import answer_with_recovery
answer = answer_with_recovery(model, messages)
```

`main()` handles input/history. The function displays reasoning/body and returns the body string.
Details: `src/shared/recovery.py` uses `model.stream()` to check during generation.

Before the answer starts, stop if reasoning reaches 2,048 characters or a sentence repeats three times.
If no answer arrived, continue once from the collected reasoning. If reasoning is empty, resend the original messages.
Display up to 2,048 reasoning characters across both requests. History keeps only questions and final answers.

Chunks can vary in length. [Recovery rules and basis](README.md#ex03--main에서-복구-함수-호출)

---

## A typewriter effect in the terminal

ex03 displays body chunks with `shared.type_text()` as they arrive.
From `examples/`, edit `src/shared/__init__.py`:

```python
TYPE_DELAY = 0.03
```

A real terminal prints one character at a time, pausing 0.03 seconds.
Set `0` to disable the delay. Non-TTY output prints chunks without delay too.

Print raw reasoning chunks immediately after `추론>`, with no typing delay.
Use a new `추론>` label if the next attempt emits reasoning.
The effect does not measure inference speed or model token intervals.

---

## Observe the same question

Use the cover's question independently in ex01/ex02; start a new chat in ex03.

| Example | Call | Record |
|---|---|---|
| ex01 | `invoke` | Complete body or empty-answer notice |
| ex02 | `invoke` | Raw reasoning, counts, and end reason |
| ex03 | `stream` | Reasoning chunks, retry notice, and body display |

Shared `NUM_PREDICT=128` is the per-request **token** budget for reasoning + body.
An ex03 retry gets that budget again. Total budgets are unequal.
With optional `REASONING=False`, all three request only once.

Normal answers are observations too. [Run, simulated tests, ex03 history, and sources](README.md)
