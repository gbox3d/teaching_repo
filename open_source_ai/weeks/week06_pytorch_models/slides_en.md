---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 6"
footer: "Using PyTorch Models"
---

# Week 6
## Using PyTorch Models

**Three 60-minute blocks**<br>
Each block: 20 min explanation & demo + 30 min hands-on lab + 10 min break

---

## This Week's Three Blocks

| Session | 20 min explanation & demo | 30 min hands-on lab |
|---|---|---|
| Block 1 | Observing tensor movement and autograd | `tensor_basics.py` time/memory comparison |
| Block 2 | Small MLP training loop and overfitting | `train_loop.py` learning curves and the overfitting point |
| Block 3 | Sentence embeddings and experiment logging | `pretrained_embed.py` similarity matrix and experiment log |

Last week's one-line `pipeline` call — this week we **open it up** and look inside.

---

## This Week's Question

> Behind one line of `pipeline`, how does a tensor move to the GPU and get computed, and what does a training loop repeat?

- Week 5: we only looked at the result of `pipeline(...)`.
- Week 6: we touch tensor -> model -> loss -> backward by hand.
- Week 7: we turn today's embeddings into document search and RAG.

**Question:** When you ran the pipeline last week, at what moment did GPU memory usage go up?

---

<!-- _class: lead -->

# Block 1 · 20 min explanation
## Observing Tensor Movement and Autograd

---

## 0–3 min · Opening Up One Line of pipeline

```text
"sentence" ─tokenizer─▶ input_ids [1, T] ─model─▶ logits [1, C] ─softmax─▶ label
string                  integer tensor         float tensor           probability
```

- Every step's input and output is a **Tensor**.
- A tensor lives in one place: CPU memory or GPU memory.
- A model is also just a bundle of tensors (parameters).

Carried over from last week: the CPU/GPU timing table from `pipeline_demo.py` (Week 5).

---

## 3–6 min · Three Tensor Properties

```python
import torch
x = torch.tensor([[1.0, 2.0, 3.0]])
x.shape    # torch.Size([1, 3])  — how many, in what shape
x.dtype    # torch.float32       — how many bytes per element
x.device   # device(type='cpu')  — which memory it lives in
```

- Most error messages come from a mismatch in one of these three.
- `shape` mismatch -> matmul fails; `dtype` mismatch -> the operation is rejected; `device` mismatch -> a "same device" error.

**Key point: when you see a tensor, read these three properties first.**

---

## 6–9 min · Moving Between CPU and GPU, and Timing It

```python
a = torch.randn(2048, 2048)     # CPU
a_gpu = a.to("cuda")            # a copy — the original stays on CPU
c = a_gpu @ a_gpu               # runs a GPU kernel (asynchronous)
torch.cuda.synchronize()        # wait for it to finish, then measure time
```

- `.to()` is a **copy**, not a move. It takes time, and the tensor now exists in two places.
- GPU operations are asynchronous. A time measured without `synchronize()` is misleading.
- For small matrices, CPU can be faster because of copy and kernel-launch overhead.

**Question:** For a 256×256 matmul, is the GPU faster, and by how much — or could it actually be slower?

---

## 9–12 min · dtype and Memory

| dtype | Bytes | Representation of 1/3 | Use |
|---|---:|---|---|
| float32 | 4 | 0.33333334 | Default training/computation |
| float16 | 2 | 0.33325195 | Inference, half the memory |
| bfloat16 | 2 | 0.33398438 | Half precision for training |
| int64 | 8 | (integer) | Token IDs, labels |

- VRAM = number of parameters × bytes + activations + gradients + optimizer state.
- A 0.5B model: 2 GB in float32, 1 GB in float16 — the Week 1 calculation comes back here.
- Convert with `x.to(torch.float16)`. Float -> int **truncates**; it does not round.

---

## 12–15 min · Autograd and `no_grad`

```python
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = (x ** 2).sum()      # a computation graph is recorded
y.backward()            # fills x.grad with dy/dx
x.grad                  # tensor([2., 4., 6.])

with torch.no_grad():   # inference: no graph is built
    z = (x ** 2).sum()  # z.grad_fn is None
```

- Any operation involving a tensor with `requires_grad=True` **stores intermediate values for backprop**.
- If you forget `no_grad` during inference-only code, memory usage roughly doubles.

**Question:** In one line, why is `x.grad` equal to `2x`?

---

## 15–17 min · A Model = Parameters + `forward`

```python
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))
sum(p.numel() for p in model.parameters())   # 4*8+8 + 8*2+2 = 58
out = model(torch.randn(3, 4))               # forward → [3, 2]
```

| PyTorch | TensorFlow (for comparison only) |
|---|---|
| `torch.Tensor` | `tf.Tensor` |
| `nn.Parameter` | `tf.Variable` |
| `backward()` | `tf.GradientTape` |
| `nn.Module` | `keras.Model` |

An `nn.Module` holds the parameters, and `forward` defines the order of computation. `.to(device)` moves every parameter at once.

---

## 17–20 min · Handoff to Lab

[Block 1 lab — Observing Tensor Movement and Autograd](lab.md#1교시-실습--텐서-이동과-자동미분-관찰) · [Block 1 files](examples/period1/README.md)

Completion criteria:

1. `outputs/tensor_report.json` exists, and you read the matmul CPU/GPU time (CPU only if no GPU).
2. You built a comparison table using three different `--size` values.
3. You explained, in one sentence, the difference `no_grad` makes — using a memory number or `grad_fn`.

Write down your prediction before you run it. **30 min lab, then a 10 min break.**

---

<!-- _class: lead -->

# Block 2 · 20 min explanation
## Small MLP Training Loop and Overfitting

---

## 0–3 min · A Training Loop Is Five Lines, Repeated

```text
for epoch in range(E):
    for x, y in loader:             # 1 pull out one batch
        logits = model(x)           # 2 forward
        loss = criterion(logits, y) # 3 how wrong are we
        loss.backward()             # 4 which direction to fix (grad)
        optimizer.step()            # 5 nudge the parameters
```

- `backward()` from Block 1 is step 4; `no_grad` is used during validation.
- The remaining questions: what do we pull out, how do we measure being wrong, and when do we stop?

Carried over: the `device` value from Block 1's `tensor_report.json`.

---

## 3–6 min · Dataset and DataLoader

```python
class MoonDataset(Dataset):
    def __len__(self):         return len(self.y)
    def __getitem__(self, i):  return self.x[i], self.y[i]

loader = DataLoader(ds, batch_size=32, shuffle=True)
```

- A Dataset only answers two questions: **its length**, and **item i**.
- The DataLoader shuffles, batches, and reads in parallel when needed.
- This week's data is 300 2D points generated by a script — no download needed.

**Question:** Should `shuffle=True` also be turned on for validation data?

---

## 6–9 min · Loss Function and Optimizer

```python
criterion = nn.CrossEntropyLoss()                 # logits + integer labels
optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
optimizer.zero_grad()   # clear grads from the last batch — otherwise they accumulate
```

- `CrossEntropyLoss` **includes softmax internally** -> the model's output stays as raw logits.
- The optimizer looks at `grad` and moves each parameter by `lr`.
- Too large an `lr` diverges; too small is slow — judge it from the curve.

**Key point: never change the order `zero_grad -> backward -> step`.**

---

## 9–12 min · epoch, batch, and the train/val Split

```text
300 points ─┬─ train 210  → used for training, log loss/acc
            └─ val    90  → never used for training, only log loss/acc
```

- 1 epoch = one full pass over the training data. With batch size 32, that's 7 steps.
- The val score is the only evidence of "how well it does on data it has never seen."
- If val leaks into training, the score goes up and its meaning disappears.

**Question:** Between a model with lower val loss and one with lower train loss, which do you choose?

---

## 12–15 min · Signs of Overfitting (Example Numbers)

| epoch | train loss | val loss | Reading |
|---:|---:|---:|---|
| 10 | 0.45 | 0.48 | Both go down — still training |
| 40 | 0.31 | 0.47 | Near the val minimum |
| 200 | 0.18 | 0.90 | Only train goes down — **overfitting** |
| 400 | 0.10 | 1.80 | Even noisy labels got memorized |

- Signal: val loss hits a minimum and then **rises again**. The gap between train and val widens.
- Remedies: stop at the minimum (early stopping), add more data, shrink the model, regularize.
- In the lab, you build this table yourself by increasing the number of epochs.

---

## 15–17 min · Fixing the seed and Logging the Curve

```python
torch.manual_seed(42)          # fixes initial weights and shuffle order
history.append({"epoch": e, "train_loss": tl, "val_loss": vl})
json.dump({"config": vars(args), "history": history}, f)
```

- Same seed, same code -> same curve on CPU. GPU can differ slightly.
- An experiment with no log can be neither reproduced nor compared — keep config and curve **in one file**.
- Put a timestamp and a tag in the filename (`train-…-overfit.json`) so you never overwrite it.

---

## 17–20 min · Handoff to Lab

[Block 2 lab — Small MLP Training Loop and Overfitting](lab.md#2교시-실습--소형-mlp-학습-루프와-과적합) · [Block 2 files](examples/period2/README.md)

Completion criteria:

1. You have separate `outputs/train-*.json` files for the default settings and for the long-epoch run.
2. You recorded, in a table, the val loss at its minimum epoch and at the final epoch.
3. You wrote one sentence on "when overfitting started," backed by numbers.

**30 min lab, then a 10 min break.**

---

<!-- _class: lead -->

# Block 3 · 20 min explanation
## Sentence Embeddings and Experiment Logging

---

## 0–3 min · Three Lines, No pipeline

```python
from transformers import AutoTokenizer, AutoModel
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).to(device).eval()
out = model(**tok(sentences, padding=True, return_tensors="pt").to(device))
```

- `AutoModel` gives you only the **body**, with no classification head -> `last_hidden_state`.
- `eval()` turns off dropout; `no_grad` turns off the graph — you need both.
- Read the model ID from the `HF_EMBED_MODEL` environment variable (see the environment reference table for its value).

Carried over: the embedding model's license row from `model_cards.md` (Week 5).

---

## 3–6 min · Token IDs -> Hidden State

```text
input_ids          [5, 18]        5 sentences × up to 18 tokens (short ones padded)
attention_mask     [5, 18]        1 = real token, 0 = pad
last_hidden_state  [5, 18, 384]   a 384-dim vector per token
```

- Sentences differ in length, so **padding** evens them out, and the mask tells real tokens from pad.
- The hidden state is "a vector per token" — not yet a single vector for the sentence.

**Question:** What changes if you include the pad tokens' vectors in the average?

---

## 6–9 min · Pooling -> Sentence Embedding -> Cosine Similarity

```python
m = mask.unsqueeze(-1).float()
emb = (hidden * m).sum(1) / m.sum(1)   # mean pooling — pad excluded
emb = F.normalize(emb, dim=1)          # scale to unit length
sim = emb @ emb.T                      # cosine similarity matrix [5, 5]
```

- Mean pooling: average of the real tokens' vectors. CLS pooling: just the first token.
- Dot product of normalized vectors = cosine -> one matmul gives the similarity of **every pair**.
- For e5-family models, the model card recommends prefixing sentences with `query: `.

---

## 9–12 min · logits -> softmax

```python
scores = sim[0, 1:]                          # scores of the other 4 sentences, from s1's view
probs = torch.softmax(scores / 0.05, dim=0)  # probabilities that sum to 1
```

- A classification model ends the same way: `logits [1, C]` -> softmax -> probabilities -> argmax.
- The smaller the temperature (the divisor), the more probability piles onto the top result — the ranking stays the same.
- The `score` the Week 5 pipeline showed you is exactly this probability.

**Question:** Does a softmax probability of 0.9 mean "90% correct"?

---

## 12–15 min · Habits for Logging Experiments

| Item | Example | If missing |
|---|---|---|
| Model ID / revision | `intfloat/multilingual-e5-small`, commit hash | Can't identify which weights were used |
| seed / device / dtype | 42, cuda, float32 | Can't reproduce |
| Input version | `sentences.txt`, 5 sentences | Can't compare results |
| Time / peak memory | 1.2 s, 310 MB | Can't judge scale |
| Result file path | `outputs/embed-….json` | Have to rebuild the results table |

- Log peak memory with `torch.cuda.max_memory_allocated()`.
- The Week 10 LoRA experiment log format grows out of this table.

---

## 15–17 min · `runlog.py` — Logging as Code

```python
from runlog import RunLog, pick_device, set_seed
set_seed(42); device = pick_device("auto")
run = RunLog("embed", config={"model": model_id, "seed": 42}, device=device)
...                                  # the experiment
run.finish({"infer_ms": 12.3})       # outputs/runs/timestamp-embed.json
```

- On creation, it records the start time and resets the GPU peak-memory counter; `finish` writes the file.
- `uv run python runlog.py` shows all logs so far as a table.
- Week 7's `ragcore.py` and Week 10's `common.py` log the same fields — copy this file into your own project.

**Key point: add the logging code before you have results.**

---

## 17–20 min · Handoff to Lab

[Block 3 lab — Sentence Embeddings and Experiment Logging](lab.md#3교시-실습--문장-임베딩과-실험-기록) · [Block 3 files](examples/period3/README.md)

Completion criteria:

1. You printed the 5-sentence similarity matrix and noted whether the most similar pair matched your prediction.
2. You ran it two more times: once with your own 5 sentences, once with a different pooling (or prefix).
3. `outputs/runs/` has 3 or more log entries, confirmed in the `runlog.py` table.

**30 min lab, then a 10 min break.** After the break, we move into next week.

---

## This Week's Summary

```text
Tensor:    shape/dtype/device -> .to(device) -> measure after synchronize
Training:  zero_grad -> forward -> loss -> backward -> step; only look at val
Embedding: token IDs -> hidden [B,T,H] -> pooling -> normalize -> matmul = similarity
Logging:   model/revision/seed/device/time/peak memory in one JSON file
```

Next week (`week07_embeddings_rag`) grows today's similarity matrix into **document search**.
