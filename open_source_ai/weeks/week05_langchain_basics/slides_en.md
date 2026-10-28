---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Block 1 · 20 min talk
## Introduction to LangChain and Ollama

---

## 0–2 min · LangChain for LLM Applications

LangChain is an open-source framework for building applications and agents with language models.

It provides components for prompts, model calls, and response processing. Applications can also connect document retrieval and external tools.

This week, build a **terminal chatbot** to learn the basic connections. Next week, extend the workflow with document retrieval for RAG.

[Official overview](https://docs.langchain.com/oss/python/langchain/overview) · [Components](https://reference.langchain.com/python/langchain-core)

---

## 2–4 min · Model, Ollama, and LangChain

| Component | Role in this course |
|---|---|
| Qwen model | Generate an answer from the input messages |
| Ollama | Run the model locally and expose an API |
| LangChain | Connect prompts, model calls, and response processing |

`ChatOllama` connects the LangChain code to the Ollama server.
Reuse the server and model prepared in Week 4.

[Official ChatOllama guide](https://docs.langchain.com/oss/python/integrations/chat/ollama)

---

## 4–6 min · Connect the Steps Around a Call

In Week 4, we sent messages to `ollama.chat()` and printed the response.
To reuse prompt formats and process responses, compose separate steps.

```python
chain = prompt | model | StrOutputParser()
```

Build messages from a question → call the model → extract answer text.
Change the role in the prompt and reuse the rest of the chain.

Block 2 runs this code and examines each step's input and output.

---

## 6–8 min · The Two Packages in This Example

| Package in pyproject.toml | Components used here |
|---|---|
| `langchain-core` | Prompt templates, messages, and string output parsing |
| `langchain-ollama` | `ChatOllama` for calling Ollama |

The official documentation also covers agents that choose tools to run.
This example uses these two packages to learn a **sequence we define**.

[Packages and APIs](https://reference.langchain.com/python/)

---

## 8–10 min · Three Commands in One Project

Check the structure with `uv init --package --python 3.12 --vcs none`.

scripts maps a command to the package's `main()`. build-system defines installation. After `uv sync`, run `uv run ex01` from the root.

---

## 10–12 min · Keep Model Settings Together

```python
from shared import create_model
model = create_model()
```

`shared` reads `OLLAMA_MODEL` and `OLLAMA_HOST`. The default is Week 4's `qwen3.5:2b`. `reasoning=False` disables reasoning output.

This local example runs without an API key or an external tracing account.

---

## 12–15 min · Send Messages with invoke

```python
response = model.invoke([
    ("system", "한국어로 짧게 답한다."),
    ("human", question),
])
print(response.content)
```

system supplies rules; human supplies the user's question.

---

## 15–18 min · Enter More Questions

Follow `나>` → answer → next `나>`. Blank input is skipped; `/bye` exits.

`ex01` sends only the current question. Repeated input is not conversation memory; history is added in Block 3.

---

## 18–20 min · Lab Handoff

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
