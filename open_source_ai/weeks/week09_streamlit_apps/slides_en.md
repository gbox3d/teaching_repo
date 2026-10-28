---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Block 1 · 20 min talk
## A First Page and Input Widgets

---

## 0–3 min · Connect Terminal Features to a Page

After Ollama, LangChain, RAG, and LoRA, expose working features on a page users can interact with.

---

## 3–6 min · Launch the Packaged App

Use Python 3.12 and a uv package project. main starts the command, scripts maps it, and build-system installs it. Run ex01 from the root; Ctrl+C stops the server.

---

## 6–9 min · Place Inputs and Outputs

Use text_input, button, and write. Enter a classroom alias and press the button to see output.

---

## 9–12 min · Widgets Trigger Reruns

Widget events rerun the script. This differs from a terminal input loop. Save a source edit and observe the page refresh.

---

## 12–16 min · Edit the First App

Change the title and one output sentence. Identify which code controls each visible element.

---

## 16–20 min · Lab Handoff

[Block 1 lab](lab.md#1교시-실습--첫-화면). Verify inputs, buttons, and reruns. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 2 · 20 min talk
## A Chat App with Session History

---

## 0–3 min · Reuse the Local Model

Reuse Week 5 ChatOllama and the same server and model. Shared settings read OLLAMA_MODEL and OLLAMA_HOST.

---

## 3–6 min · Chat Input and Messages

chat_input receives a question; chat_message renders user and assistant messages. Do not add a blocking terminal input loop to the page.

---

## 6–9 min · Preserve State across Reruns

Store messages in session_state and render them on the next rerun. Check both page persistence and history being sent to the model.

---

## 9–12 min · Render Answer Chunks

Feed string pieces to write_stream and store the complete answer. Call the model only when a new question is submitted.

---

## 12–16 min · Clear and Compare

Tell the model a color, ask for it, then clear the chat. A browser session is not permanent storage.

---

## 16–20 min · Lab Handoff

[Block 2 lab](lab.md#2교시-실습--채팅-앱). Verify two turns and clearing history. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 3 · 20 min talk
## Ask Questions about a Document

---

## 0–3 min · Start with a Small Document

Use the fictional library guide or upload a UTF-8 txt file. Blank-line-separated paragraphs form the retrieval units.

---

## 3–6 min · Reuse Embeddings and Retrieval

As in Week 6, embed paragraphs and the question, then rank by cosine similarity. The selected model uses query: and passage: prefixes.

---

## 6–9 min · Cache Repeated Work

Cache the embedding model as a resource and document vectors as data. Prepare dependencies and models before class.

---

## 9–12 min · Show Answers with Retrieved Evidence

Expand retrieved paragraphs and compare source numbers with the answer. Similarity is not probability; check out-of-context questions.

---

## 12–16 min · Optional Extensions after Completion

Choose one extension: face or image similarity, speech input/output, or a small-model comparison. Present a visible input → model → output flow.

---

## 16–20 min · Lab Handoff

[Block 3 lab](lab.md#3교시-실습--문서-검색-앱). Change the document and compare evidence with answers. Lab: 30 minutes; break: 10 minutes.
