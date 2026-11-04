---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Block 1 · 20 min talk
## Finding Text with Embeddings

---

## 0–2 min · A Model Knows Only What It Learned

We asked the Week 4 model `메두사를 죽인 영웅은 누구야?` (Which hero killed Medusa?)

> The hero who killed Medusa … there are two versions. The first is Hera … the second is Athena …
> (qwen3.5:2b, no documents, answer shortened)

Small models confidently make up what they do not know.
This week, we **find text that contains the answer and put it into the prompt.** The model stays the same.

---

## 2–4 min · Embeddings: Sentences as Numbers

```python
embeddings = create_embeddings()   # shared: bge-m3
vector = embeddings.embed_query("제우스는 하늘에서 번개를 던진다.")
len(vector)      # 1024
vector[:5]       # [0.004, 0.041, -0.052, -0.021, -0.016]
```

One sentence becomes 1024 numbers. This bundle of numbers is an **embedding** (vector).
Sentences with similar meanings become similar bundles of numbers.

---

## 4–6 min · Similarity: Closeness as One Number

| Sentence (English gloss) | Similarity to `헤라는 결혼의 여신이다.` |
|---|---:|
| Hades rules the world of the dead. | 0.493 |
| Zeus throws lightning from the sky. | 0.488 |
| Poseidon rules the sea and earthquakes. | 0.427 |
| Python lists are made with square brackets. | 0.350 |
| Today's lunch at the student cafeteria is kimchi stew. | 0.273 |

Scores are for the Korean sentences in `SENTENCES` (ex01); `헤라는 결혼의 여신이다.` = Hera is the goddess of marriage.
Cosine similarity: how closely two vectors point the same way. Near 1 = similar meaning.
Myth sentences are closer even with no shared words.

---

## 6–8 min · This Week's Two Models

| Model | Role | Size |
|---|---|---|
| `qwen3.5:2b` | Reads the question and **generates** an answer (Weeks 4–5) | about 2.7 GB |
| `bge-m3` | Turns text **into vectors only**; makes no answers | about 1.2 GB |

```python
from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="bge-m3")
```

Both models run on the same Ollama server. Compare only vectors made by the same embedding model.
Many texts go through `embed_documents(list)`; one question goes through `embed_query(sentence)`.

---

## 8–10 min · Vector Store: Add, Then Search

```python
store = InMemoryVectorStore(embeddings)
store.add_texts(texts, metadatas)                 # a vector for each text
store.similarity_search_with_score(question, k=3) # 3 closest texts
```

Turn the 50 texts into vectors once; then turn one question into a vector and pull out the closest texts.
The score is the same cosine similarity as in ex01. It is not a probability or a percentage.
At this week's scale, memory is enough. A vector database server becomes worth it only at tens of thousands of texts.

---

## 10–13 min · Data: 50 Greek and Roman Myths

```text
## 페르세우스와 메두사의 머리
페르세우스는 황금 비로 변한 제우스와 다나에 사이에서 태어났다. ...
```

Each `## 제목` (title) in `src/shared/data/myths.md` is one search unit. `load_myths()` reads 50 (title, body) pairs.

Anyone may retell the plots of the myths, so we wrote new summaries for the course. Copyrighted text, such as sentences from translated books or novels, is left out.
Small models often get the details wrong here, so the effect of the documents is visible.

---

## 13–16 min · Demo: It Finds, and It Misses

```text
나> 메두사를 죽인 영웅은 누구야?
  0.572  메두사와 고르곤 자매: ...
  0.532  페르세우스와 메두사의 머리: ...
  0.529  벨레로폰과 페가소스: ...
나> 겨울이 생긴 이유를 설명하는 신화는?
  0.468  야누스: ...                         ← miss
나> 페르세포네가 석류 씨를 먹어서 생긴 일은?
  0.572  페르세포네와 사계절: ...            ← hit
```

Search finds text close to **the wording of the question**. Even if the answer is there, search misses it when the question is worded far from the text.

---

## 16–18 min · Six Commands in One Project

Check the structure with `uv init --package --python 3.12 --vcs none my-rag`.

| Command | One concept | Values to change |
|---|---|---|
| ex01 · ex02 | Embedding, search | `SENTENCES`, `TOP_K` |
| ex03 · ex04 | Answers with documents, sources and refusal | `TOP_K`, `RULES` |
| ex05 · ex06 | Splitting long text, my documents | `CHUNK_SIZE`, `src/shared/data/` files |

Model settings and data loading live in `shared`. There are no options; edit the constants at the top of the file.

---

## 18–20 min · Lab Handoff

[Block 1 lab](lab.md#1교시-실습--임베딩과-신화-검색)

Put your own sentences into `ex01` and check the similarity order. In `ex02`, compare the top result for two differently worded questions. Change `TOP_K` to 1. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 2 · 20 min talk
## Answering with Retrieved Documents

---

## 0–3 min · Asking Without Documents

```text
나> 헤라클레스의 열두 과업 중 다섯 번째는 무엇이야?
자료 없이> 헤라클레스의 열두 과업 중 다섯 번째 과업은 **아테네城的 벽을 쌓기**입니다. ...
자료 넣고> 헤라클레스의 열두 과업 중 다섯 번째 과업은 아우게이아스 왕의 외양간을 하루에 청소하는 것이었습니다.
찾은 자료: 헤라클레스의 열두 과업, 헤라클레스의 탄생, 헤르메스
```

Same model, same question. The only difference is the three documents added to the prompt. The answer without documents even mixed in Chinese characters.

---

## 3–6 min · RAG: Retrieve, Insert, Generate

```text
question ─▶ embed ─▶ 3 closest texts ─▶ [docs + question] ─▶ model ─▶ answer
                        (Block 1)           (Block 2)
```

Retrieval, Augmented, Generation: augment the prompt with retrieved text, then generate.
The model is not retrained. Change the text and the answer changes. The sources are already known at the retrieval step.

---

## 6–9 min · Where the Documents Go

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", RULES),
    ("human", "자료:\n{context}\n\n질문: {question}"),
])
chain = prompt | create_model() | StrOutputParser()
```

The same chain as Week 5. `{context}` receives the three retrieved texts, and `{question}` the question.

```python
context = "\n\n".join(doc.page_content for doc in docs)
chain.invoke({"context": context, "question": question})
```

---

## 9–12 min · One Rule Line and Sources

```python
RULES = ("너는 그리스·로마 신화 안내자다. 자료에서 질문의 답을 찾아 한국어로 짧게 답한다. "
         "자료에 답이 없을 때만 \"자료에 없습니다.\"라고 답한다.")
```

```text
AI> 히포메네스는 아탈란테가 앞설 때마다 **황금 사과**를 하나씩 던졌다.
[출처] 아탈란테의 경주 0.60 / 아킬레우스의 발뒤꿈치 0.49 / 헤라클레스의 열두 과업 0.49
```

The **program attaches the sources from the search results**; the model does not write them. The `**` is a Markdown mark the model added for bold.
All three texts go to the model regardless of score. Content from unrelated texts can slip into the answer, so check it against the top text.

---

## 12–15 min · Demo: A Question Not in the Documents

```text
나> 토르의 망치 이름은 무엇이야?
AI> 자료에 없습니다.
[출처] 헤르메스 0.40 / 메두사와 고르곤 자매 0.40 / 이아손과 황금 양털 0.39
```

Search always returns three texts. Scores all near 0.4 signal that nothing relevant exists.
Remove the refusal sentence from the rules and some questions get made-up answers (course test PC: a Harry Potter question). Check it yourself in the lab.

---

## 15–18 min · One Rule Sentence Changes the Answers

```text
① You are a Greek-Roman myth guide. Answer in Korean based only on
   the documents below. If something is not in them, do not make it
   up; just reply "자료에 없습니다."
② You are a Greek-Roman myth guide. Find the answer in the documents
   and answer briefly in Korean. Reply "자료에 없습니다." only when
   the answer is not there.           ← ex04 (ex06: no first sentence)
```

| `RULES` | 11 myth questions (ex04) | 7 chunk questions (ex06) |
|---|---:|---:|
| ① | 7 correct | 3 correct |
| ② example code | 10 correct | 7 correct |

Most ① misses refused although the answer was in the documents (course test PC; varies per run).
Even with documents, the model may pick the wrong sentence. Check it in the `[출처]` texts.

---

## 18–20 min · Lab Handoff

[Block 2 lab](lab.md#2교시-실습--자료를-넣어-답하기)

In `ex03`, check both answers against the data file. In `ex04`, record the refusal and source scores for a question not in the documents. Remove the refusal sentence from `RULES` and run again. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 3 · 20 min talk
## Splitting Long Text, Then Your Own Documents

---

## 0–3 min · Split Long Text into Chunks

Each myth was one piece. Real documents run on at length without titles.

- Inserting the whole text brings in unrelated parts, blurs the answer, and wastes tokens
- When one vector represents a long text, search scores blur too
- So split it into **pieces** (chunks) and make a vector for each chunk

Today's text: Odysseus's homecoming, about 3,900 characters (`odyssey.md`)

---

## 3–6 min · Chunk Size and Overlap

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(text)
```

It looks for boundaries in the order paragraph → line → space and cuts within `chunk_size` characters.
When a cut falls mid-paragraph, `chunk_overlap` repeats up to the last 50 characters of the previous chunk in the next one. Chunks split at a paragraph boundary do not overlap.

| `CHUNK_SIZE` (overlap 50) | 150 | 300 | 600 | 1000 |
|---|---:|---:|---:|---:|
| Chunks | 39 | 19 | 10 | 5 |
| Top score, Aeolus question | 0.566 | 0.583 | 0.583 | 0.532 |

---

## 6–9 min · Demo: Where the Chunks Are Cut

```text
글자 3905개를 최대 300자 조각 19개로 나눴습니다.
  조각 2 (298자): 다음에 닿은 섬은 … 아무 일도 없는 줄 알고 돌아갔다. 아침에 거인이 양을
  조각 3 (182자): 나를 해쳤다"고 외치자 그들은 아무 일도 없는 줄 알고 … 해 달라고 빌었다.
나> 아이올로스가 준 선물은 무엇이었어?
  0.583  조각 4: 바람의 신 아이올로스는 오디세우스를 한 달 동안 대접한 뒤 ...
```

Chunk 2 ends mid-sentence, and chunk 3 starts by repeating the last 47 characters of chunk 2 (`아무 일도 없는 줄 알고`). Chunks 0, 1, and 2 meet at paragraph boundaries, so they do not overlap.
Too small breaks the context (0.566 at 150); too large mixes in unrelated content and blurs the score (0.532 at 1000).

---

## 9–12 min · My Document Assistant: Blocks 1 and 2 Combined

```python
for path in sorted(DATA_DIR.glob("*.md")):
    chunks = splitter.split_text(path.read_text(encoding="utf-8"))
    store.add_texts(chunks, [{"source": f"{path.name}#{n}"} for n in range(len(chunks))])
```

Read every `.md` in the folder, split it into chunks, and store them. The source is `filename#chunk-number`.
The rest is the same as Block 2: search → documents and question → model → answer and `[출처]`.

---

## 12–15 min · Demo: Asking Two Files

```text
myths.md: 조각 45개
odyssey.md: 조각 12개
나> 오디세우스는 칼립소의 섬에 몇 년 있었어?
AI> 7 년
[출처] odyssey.md#6, myths.md#30, odyssey.md#3, odyssey.md#1
나> 나우시카는 누구야?
AI> 나우시카는 오디세우스의 아내입니다.
[출처] myths.md#7, myths.md#21, myths.md#10, odyssey.md#7
```

The Nausicaa chunk (`odyssey.md#7`) came in 4th, yet the model got it wrong (Nausicaa is a Phaeacian princess).
No chunk with the answer in `[출처]` means a **retrieval failure**; a wrong answer despite one means **a model limitation**.

---

## 15–18 min · Add Your Own Writing

- Save text written in Notepad as a UTF-8 `.md` file in `src/shared/data/` and run again
- Course materials include only public-domain text. Use copyrighted text only on your own PC
- Do not put real names, contact details, or account information in the data

Week 7 goes the other way: instead of changing the documents, LoRA changes the model slightly. In Week 9, this assistant gets a Streamlit interface.

---

## 18–20 min · Lab Handoff

[Block 3 lab](lab.md#3교시-실습--긴-글-나누기와-내-문서-도우미)

In `ex05`, change `CHUNK_SIZE` to 150 and 1000 and tabulate the chunk counts and results. Add your own writing to `ex06` and ask questions. Lab: 30 minutes; break: 10 minutes.
