---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Block 1 · 20 min talk
## Connect the Same Ollama Model

---

## 0–3 min · Connect the Prepared Model

Reuse the Ollama server and model from Week 4. No new training is needed.

`ChatOllama` connects LangChain to Ollama. API keys and external tracing accounts are not required.

---

## 3–6 min · Three Commands in One Project

Check the structure with `uv init --package --python 3.12 --vcs none`.

scripts maps a command to the package's `main()`. build-system defines installation. After `uv sync`, run `uv run ex01` from the root.

---

## 6–9 min · Keep Model Settings Together

```python
from shared import create_model
model = create_model()
```

`shared` reads `OLLAMA_MODEL` and `OLLAMA_HOST`. The default is Week 4's `qwen3.5:2b`. `reasoning=False` disables reasoning output.

---

## 9–12 min · Send Messages with invoke

```python
response = model.invoke([
    ("system", "한국어로 짧게 답한다."),
    ("human", question),
])
print(response.content)
```

system supplies rules; human supplies the user's question.

---

## 12–16 min · Enter More Questions

Follow `나>` → answer → next `나>`. Blank input is skipped; `/bye` exits.

`ex01` sends only the current question. Repeated input is not conversation memory; history is added in Block 3.

---

## 16–20 min · Lab Handoff

[Block 1 lab](lab.md#1교시-실습--ollama-연결)

Ask about lists and tuples. Compare with Week 4's `ollama.chat()` and confirm the same server and model. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 2 · 20 min talk
## Connect a Prompt and Model

---

## 0–3 min · Use Variables for Changes

```text
You are {role}.
{question}
```

Pass the role and question as prompt variables instead of concatenating them manually.

---

## 3–6 min · Create Messages from a Template

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 {role}이다. 한국어로 짧게 답한다."),
    ("human", "{question}"),
])
```

Variable names must match the input keys passed to invoke.

---

## 6–9 min · Three Steps in a Chain

```python
chain = prompt | model | StrOutputParser()
```

Input dictionary → messages → model response → string.

`|` passes each step's output to the next step.

---

## 9–12 min · Match the Input Keys

```python
answer = chain.invoke({
    "role": ROLE,
    "question": question,
})
```

This example handles the current question and does not automatically store previous turns.

---

## 12–16 min · Change One Role

Change `ROLE` to a Python tutor who explains with analogies, then ask the same question.

Keep the chain unchanged. Record the actual output if the model ignores the answer-length rule.

---

## 16–20 min · Lab Handoff

[Block 2 lab](lab.md#2교시-실습--프롬프트-연결)

Enter two questions and compare roles. Explain the input and output of each chain step. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 3 · 20 min talk
## Conversation History and Streaming

---

## 0–3 min · The Program Sends History

As in Week 4, send earlier questions and answers to preserve context.

Using LangChain does not automatically create persistent memory. This example keeps `history` in a program list.

---

## 3–6 min · Add a Place for History

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "한국어로 짧게 답한다."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
```

Order: rules → previous turns → current question.

---

## 6–9 min · Print Each Part as It Arrives

```python
for part in chain.stream(inputs):
    print(part, end="", flush=True)
    answer += part
```

Print the parsed string pieces while collecting the complete answer.

---

## 9–12 min · Keep the Question and Full Answer

```python
history.extend([
    ("human", question),
    ("ai", answer),
])
```

Send this list on the next request. A new program run starts with an empty list.

---

## 12–16 min · Compare with Empty History

Tell the model a color, then ask for it. Exit, change the request to `"history": []`, and repeat.

Distinguish a lucky guess from history being sent. Check both the answer and request code.

---

## 16–20 min · Add Retrieval Next Week

[Block 3 lab](lab.md#3교시-실습--대화-기억과-스트리밍)

This week connects prompts, models, and string output. Week 6 adds retrieved documents as context and checks sources. Lab: 30 minutes; break: 10 minutes.
