---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Block 1 · 20 min talk
## My Evaluation Questions and Failure Classification

---

## 0–3 min · The Task

Question set → content check → Week 14 evaluator → failure-type table → one thing to fix.

Score the 20 public questions and your own questions with the same evaluator, then split the lost points by failure type. Final performance is measured on hidden questions of the same format, so use your own questions to check whether a change tuned on the 20 public questions also raises the score on differently worded questions.

The questions and record sheet you make in this block carry over to Blocks 2 to 4.

---

## 3–6 min · Keep Evaluation Questions Apart from Training Questions

| `QUESTION_SET` | Files | Used for |
|---|---|---|
| `"public"` | Week 14's 20 public questions | Same questions as the `ex02` public evaluation |
| `"mine"` | `my_questions.json`, `my_answers.json` | Your own evaluation (20 sample questions) |
| `"train"` | `train_questions.json`, `train_answers.json` | Block 3 training (40 sample questions) |

Keep evaluation questions (`public`, `mine`) out of training. Scoring again on trained questions only measures memorized answers. The published `mine` and `train` sets are samples that show how to build them; adding questions is part of the assignment.

---

## 6–9 min · Same id in the Question File and the Answer File

In `my_questions.json`, mine-16 has the category `composite` and the question "신입생 퀴즈에 원광초급대학 설립 연도와 원광대학교 교색을 문제로 내려 합니다. 두 정답을 알려 주세요." ("For a freshman quiz, I want to ask the founding year of Wonkwang Junior College and Wonkwang University's school color. Give me both answers."). `my_answers.json` holds this entry under the same `id`:

```json
{"id": "mine-16", "expected": [["1951", "1951년"], ["황금색", "금색"]],
 "sources": ["wku-history", "wku-symbols"], "abstain": false,
 "fact_sources": ["wku-history", "wku-symbols"]}
```

`expected` holds one alias group per fact (`황금색`, `금색` = golden, gold), and `fact_sources` lists each fact's source document in the same order. Unanswerable questions have empty `expected`, `sources`, and `fact_sources`, with `abstain` set to `true`. [Question writing rules](examples/src/lab_shared/data/README.md)

---

## 9–12 min · ex04 Calls the Week 14 Evaluator Unchanged

```python
BOT = "student_bot"    # "rag_bot" in Block 2
QUESTION_SET = "mine"  # one of "public", "mine", "train"
```

`uv run ex04` checks the content of `mine` and `train` before scoring. If a source document ID is missing from `corpus.json`, or a question matches a public question or another question in the same set, evaluation does not start. Scoring is done by Week 14's `evaluate`, so on the 20 public questions you can compare the score with `uv run ex02`, which is installed in the same project.

---

## 12–15 min · Split Lost Points into Seven Types

| `ex04` label | Meaning | Lost points counted |
|---|---|---|
| `시간 초과` | `status=timeout` | 100 |
| `실행 오류` | `status=error` | 100 |
| `형식 오류` | `status=invalid_response` | 100 |
| `답변 불가인데 답함` | Unanswerable question that did not score 100 | 100 |
| `답할 수 있는데 거절` | Refused an answerable question (`abstain=true`) | 100 |
| `사실 누락·불필요한 답` | Answer F1 below 1 (missing or extra facts) | 80 − `answer_points` |
| `출처 누락·불필요한 출처` | Source F1 below 1 (missing or extra sources) | 20 − `source_points` |

If no fact is correct, the source points are 0 as well, so all 100 points go to `사실 누락·불필요한 답`. Dividing a type's total lost points by the number of questions gives its "points taken from the overall mean" (`전체 평균에서 빠진 점수`). The seven rows add up to 100 minus the overall mean.

---

## 15–18 min · Compare the Largest Loss Under the Same Conditions

| Hypothesis | Where to check |
|---|---|
| The source document never reached the model | Block 2 `ex05` retrieval observation |
| The document arrived, but the model picked the wrong answer | `SYSTEM_PROMPT`, Block 3 training |
| The format broke, or a timeout or run error occurred | Block 4 `ex07` inference check |

Pick the type with the largest "points taken from the overall mean" and write one hypothesis. Run again without changing anything to see the run-to-run variation. Count a difference as an improvement only if it is larger than that variation, and keep a change only if both `public` and `mine` go up.

---

## 18–20 min · Lab Handoff

1. With `QUESTION_SET = "public"`, run `ex04` and `ex02` and compare the scores.
2. Add a few questions of your own and run with `"mine"`.
3. Pick the largest loss in the failure-type table and write a hypothesis.
4. Run once more with the same settings and fill in the record sheet.

In the model column of the record sheet, write the name and the first 12 characters of the digest. Even with the same tag, a different digest means a different build.

[Block 1 lab](lab.md#1교시--내-평가-문항과-실패-분류). Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 2 · 20 min talk
## Embedding RAG and Observing Retrieval

---

## 0–3 min · The Task

Question → pick documents (retrieval) → write an answer (model) → scoring.

Of the failures you classified in Block 1, look separately at the ones caused by retrieval. `rag_bot` has the same response contract, system instructions, and request-body values as Week 14's `student_bot`, but its retrieval differs.

---

## 3–6 min · Word-Overlap Search Counts Matching Pieces

```python
terms = search_terms(question)  # Korean words and two-character pieces
score = len(terms & search_terms(doc["title"] + " " + doc["text"]))
```

For "원광대의 뿌리가 된 학교는 어디인가요?" ("Which school did Wonkwang University grow out of?"), the history document scores 3, lower than the location document (4). Even among the documents tied at 3, data order pushes it back to 4th, outside the `TOP_K` of 3.

---

## 6–9 min · Embedding Search Finds Documents Close in Meaning

```python
vectors = embed([f"{doc['title']}: {doc['text']}" for doc in corpus])
query = embed([question])[0]
ranked = sorted(((cosine(query, v), doc) for doc, v in zip(corpus, vectors)), ...)
```

For the same question, bge-m3 (ID `790764642607`, Ollama 0.40.17) ranked the history document 1st. Document vectors are built once, on the first search. In a scoring run, they are built during the warm-up question (up to 120 seconds).

---

## 9–12 min · Same Job as the Week 6 LangChain Example

| Week 6 | rag_bot |
|---|---|
| `OllamaEmbeddings(model="bge-m3")` | `EMBED_MODEL`; `embed()` calls `/api/embed` |
| `InMemoryVectorStore.add_texts` | `index`, built on the first search |
| `similarity_search_with_score` | `rank()`, `retrieve()` |

Why `urllib`: `student_bot` uses it too, so no extra packages are needed and the code can be copied unchanged into `student_bot` in your assignment folder.

---

## 12–16 min · Measure Retrieval Alone

```text
[문항 ID] fact 근거 wku-history
    student_bot 놓침 wku-history | rag_bot 포함(최고 유사도 0.xxx)
rag_bot: 근거 문서를 모두 찾은 문항 n/16, 답변 불가 문항에 보낸 문서 평균 n개
```

Output labels: `문항 ID` = question ID, `근거` = sources, `놓침` = missed, `포함` = included, `최고 유사도` = highest similarity. Summary line: questions with all source documents found, n/16; average documents sent for unanswerable questions, n.

`ex05` does not generate answers. It checks whether the expected answer's source documents (`fact_sources`) appear in the search results and counts how many documents were sent for unanswerable questions. The block above shows the output format. With only five documents, a `TOP_K` of 3 brings in most of the evaluation questions' sources. The difference shows up in the training questions (`train`).

---

## 16–18 min · Two Constants to Try Changing

```python
TOP_K = 3        # number of documents to send to the model
MIN_SCORE = 0.0  # documents below this similarity are not sent
```

If there are no documents to send, the bot abstains without calling the model. Sending more documents makes it more likely that the source documents are included, but the input gets longer and unrelated documents are sent as well.

---

## 18–20 min · Lab Handoff

1. Compare the two searches with `uv run ex05`, then add `"train"` to `SETS` and run it again.
2. Set `BOT = "rag_bot"` in `ex04` (retrieval constants at their defaults) and score `mine` and `public`.
3. Change only one of `TOP_K` or `MIN_SCORE` and rerun `ex05` and `ex04`. Keep a change only if both scores go up.
4. Keep one retrieval setting in `rag_bot` to use in Block 3.

[Block 2 lab](lab.md#2교시--임베딩-rag와-검색-관찰). Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 3 · 20 min talk
## Training Examples, LoRA Training, and Registration

---

## 0–3 min · The Task

`ex06` training examples → `ft01` training → `ft02` merge → GGUF conversion → `ollama create` → `ex04` scoring.

What to check: Do training examples make the 0.5B model follow the response contract (three JSON keys) and pick short answers? Compare the trained model with `wku-base`, the model before training, on the same questions. Training happens in `finetune/`; building training examples and scoring happen in `examples/`.

---

## 3–6 min · Build Training Examples from the Conversations rag_bot Sends

```python
documents = rag_bot.retrieve(question)
messages = rag_bot.messages(question, documents)
row = {"messages": messages + [{"role": "assistant", "content": target(item)}]}
```

For each training question (question/answer JSON), build the same conversation as the real request. If any training question matches an evaluation question, all matches are shown and the run stops. Questions where retrieval missed a source document are left out of training.

---

## 6–9 min · Settings Changed from Week 7 for Length and Memory

| Constant | Week 7 | This special lecture |
|---|---|---|
| `MAX_LENGTH` | 256 | 1024 |
| `DTYPE` | float32 | bfloat16 |
| `GRADIENT_CHECKPOINTING` | not used | True |
| Padding | not used | multiples of 64 tokens |

Examples that contain retrieved documents do not fit in 256 tokens. On the reference PC (Windows 11), overflowing memory slowed training down without an error. Before training, unload the models Ollama has loaded. The full table of differences is in the walkthrough.

---

## 9–12 min · Merge and Convert to GGUF

```powershell
uv run ft02
uv run --locked --with sentencepiece==0.2.3 --with protobuf==7.36.2 `
  python tools/llama.cpp/convert_hf_to_gguf.py `
  models/wku-lora-merged --outfile models/wku-lora.gguf --outtype f16
```

Ollama 0.40.17 could not register the merged safetensors folder directly. Convert it to GGUF, then register it.

---

## 12–15 min · Register and Score with the Same Evaluator

```text
FROM ./models/wku-lora.gguf
PARAMETER temperature 0
```

Register it with `ollama create wku-lora -f Modelfile.lora`. Check that `BOT` in `ex04` is `"rag_bot"`, then change `MODEL` in `rag_bot` to `"wku-lora"` and score. Also score `wku-base`, the model before training, on the same questions. Copying Week 7's `Modelfile` also registers its mythology-guide `SYSTEM` and `num_predict 120`.

---

## 15–18 min · Demo: Reading the ft01 Output

Run `uv run ft01` on the instructor's PC and point out:

- Near the start (after the `모델:` (model) line): the number of training examples and the minimum and maximum token counts
- Each step: whether the loss goes down
- Near the end: `train_runtime` (seconds) and `GPU 최대 할당 메모리` (peak allocated GPU memory)

If step times keep growing, VRAM has overflowed.

---

## 18–20 min · Lab Handoff

1. (examples/) `ex06` → `ollama stop bge-m3`
2. (finetune/) `ft01` → `ft02` → conversion → `ollama create wku-lora`
3. (examples/) Score `wku-lora` and `wku-base` on the same questions with `ex04`.

In Block 4, look into questions with odd answers using `ex07`. The published training questions are only a subset; expanding them is part of the assignment. Keep evaluation questions out of the training data. For the assignment's model rules, follow the course announcements.

[Block 3 lab](lab.md#3교시--학습-예시와-lora-학습등록). Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 4 · 20 min talk
## Catching Inference Bugs

---

## 0–3 min · The Task

Failed question → reproduce it with `ex07` → symptom and evidence in [6] → where to fix → planting bugs.

When training and registration are done but the answers look wrong, look at the requests the bot actually sent to Ollama and the responses it got back before training the model again. Check your own model registered in Block 3 and the baseline bot (Week 14's `student_bot`) with the same question, then plant bugs on purpose to match symptoms with causes. Run every command in `examples/`.

---

## 3–6 min · ex07 Shows What the Bot Sent and Received

| Section | What it shows |
|---|---|
| [1] `호출 목록` | Call list: path, model, HTTP status, time |
| [2] `생성 호출` | Generation calls: settings and messages sent, model info, context, response, time |
| [3] `임베딩 호출` | Embedding calls: model, number of inputs, vectors and their dimension |
| [4] `실행 위치` | Where it runs: GPU share and context_length from `/api/ps` |
| [5] `최종 판정` | Final verdict: return value, response contract, time without model load, evaluator status (`채점기 status`) |
| [6] `의심되는 문제와 고칠 곳` | Suspected problems and fixes: symptom, evidence, fix; a note line at the end |

`ex07` does not change the bot's code. While `answer(question)` runs once, it intercepts the requests sent through `urllib`. After editing the bot file, quit with `/bye` and rerun.

---

## 6–9 min · Reproduce a Failed Question on Its Own

```text
[mine-xx] fact  점수 n  status=…  실패: …
    질문 원광대학교 …
    응답 {"answers": …}
```

`점수` = score, `실패` = failure, `질문` = question, `응답` = response. For a failed question, `ex04` also prints the `질문` line. Paste that sentence at the `질문>` prompt of `ex07` as it is. Keep `BOT` in `ex07` and `MODEL` in `rag_bot` the same as when you scored with `ex04`. The evaluator sends each question on its own, so do not rely on earlier questions.

| [5] status | Scoring | Block 1 failure type |
|---|---|---|
| `ok` | Scored against the expected answer | Answer content (facts, sources, abstaining) |
| `invalid_response`, `timeout`, `error` | 0 points | Format error, timeout, run error |

---

## 9–12 min · Read [6] as Symptom, Evidence, Fix

```text
[6] 의심되는 문제와 고칠 곳
  - <symptom> | 근거: <values in [2]–[5]> | 고칠 곳: <constant or request value to change>
  참고: 요청이 덮어쓰지 않은 Modelfile 값 | <model> <name>=<value>, … | 영향이 의심되면 …
```

`근거` = evidence, `고칠 곳` = where to fix, `참고` = note, `요청이 덮어쓰지 않은 Modelfile 값` = Modelfile values the request did not override, `영향이 의심되면 …` = if you suspect an effect …. Read the problem lines from the top and match each piece of evidence against [2]–[5]. Symptom names and fixes are in the table in [Catching Inference Bugs](examples/debugging.md#증상별-확인할-값과-고칠-곳). If there is no problem line but the answer is wrong, check the retrieved documents (`ex05`) and `SYSTEM_PROMPT`. `모델 새로 적재` (model newly loaded) on the first question is the time spent loading the model, and the evaluator excludes it by sending a warm-up question first.

---

## 12–14 min · The Model Decides What the Request Leaves Out

```powershell
ollama show <model>               # capabilities, thinking mode, max context, template source
ollama show <model> --parameters  # PARAMETER values in the Modelfile
```

Values in the request options apply to that request; values left out come from the Modelfile used when the model was registered. The same bot code can behave differently when only `MODEL` changes. In [2], values under `Modelfile 기본값` (Modelfile defaults) without the `(요청이 덮어씀)` (overridden by the request) mark are such values, and the note line at the end of [6] collects them per model. Temperature is checked by a separate rule, `온도를 모델 기본값에 맡김` (temperature left to the model default). The note only tells you such values exist. To learn their effect on answers, put a value with the same name into the request options and score with `ex04`.

---

## 14–16 min · Plant One Bug at a Time and Compare with Your Prediction

| Bug | Value to change in `rag_bot` |
|---|---|
| 1. Turn on thinking | `"think": False` → `"think": True` |
| 2. Lower the output limit | `"num_predict": 512` → half of question A's eval_count (integer) |
| 3. Nonexistent model name | `MODEL` → the current name with one character wrong |

Question A is "원광대학교를 상징하는 새는 무엇인가요?" ("What bird symbolizes Wonkwang University?"). Record `git diff -- src/rag_bot/__init__.py` before planting → write a prediction → plant one bug → question A in `ex07`, failure-type table in `ex04` → revert to the value before planting and check that `git diff` matches the record. The same bug can give different results depending on the model `MODEL` points to.

---

## 16–18 min · Demo: Reading the ex07 Output

Run `uv run ex07` without bugs on the instructor's PC, enter one question, and point out from the top:

- [1]: call order and HTTP status
- [2]: think, stream, and options sent; model info; done_reason and eval_count in the response
- [5]: total time and time without model load; evaluator status
- [6]: problem lines and the note line

Then show how to record the state before planting with `git diff -- src/rag_bot/__init__.py`.

---

## 18–20 min · Lab Handoff

1. (examples/) Paste a failed question's `질문` line from `ex04` into `ex07` (`BOT = "rag_bot"`, `MODEL` set to your model).
2. Set `BOT = "student_bot"`, enter the same question, and compare the two outputs.
3. Set `ex07` back to `BOT = "rag_bot"`, record `git diff` and question A's baseline before planting, then plant bugs 1–3 one at a time, observe with `ex07` and `ex04`, and revert.
4. Write down the symptom, the values you checked, and where to fix it in the Block 4 tables of the lab sheet.

During the assignment period, pick any of the remaining bugs to try (optional). When your trained model misbehaves, narrow it down with [Catching Inference Bugs](examples/debugging.md).

[Block 4 lab](lab.md#4교시--추론-버그-잡기). Lab: 30 minutes; break: 10 minutes.
