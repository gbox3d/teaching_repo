---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 13"
footer: "Simulator Control Evaluation, Improvement, and Streamlit"
---

# Week 13
## Simulator Control Evaluation, Improvement, and Streamlit

Three 60-minute blocks

Evaluate the Week 12 Needle 3 LoRA through calls and actual state.


---

## Schedule

| Block | 0–20 min explanation/demo | 20–50 min lab |
|---|---|---|
| 1 | Controlled before/after comparison | `uv run ex01` evaluation |
| 2 | Error categories and reasons for changes | `uv run ex02` correction dialogue |
| 3 | Cache, sessions, and reruns | `uv run ex03` Streamlit |

Breaks run from 50–60 min in each block. [lab.md](lab.md) defines lab timing.


---

## Block 1, 0–4 min: Models and artifacts

Build on Week 4 dialogue, Week 7 LoRA, and Week 9 Streamlit.

Read files in Week 12 `examples/models/` without copying them.

- `adapter.safetensors`: learned changes
- `baseline_adapter.safetensors`: B=0, unchanged base weights
- `baseline.cact` and `tuned.cact`: inference archives for comparison

<!-- Source: https://cactuscompute.com/blog/finetuning-needle ; paths and baseline export are course code -->

---

## Block 1, 4–8 min: Matched evaluation conditions

Compare base and tuned archives at 4 bits and 20 layers.

- 16 cases: 8 Korean, 8 English; 10 call, 6 no-call
- Same cases, order, descriptions, and generation settings; `reset()` per request
- Restore and read initial LEDs `[0, 64, 128, 255]` for every case

No exact string overlap with 48 training prompts. This does not prove semantic independence.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle ; case composition is course data -->

---

## Block 1, 8–12 min: Call validation before execution

| Allowed function | Argument range |
|---|---|
| `turn_on(index)` | Integer 0–3 |
| `turn_off(index)` | Integer 0–3 |
| `set_brightness(index, value)` | Integer 0–3, integer 0–255 |
| `read_environment()` | No arguments |

The model proposes calls. Validate every name, type, and range before execution.
A valid shape can still express the wrong intent.


---

## Block 1, 12–16 min: Calls and actual results

- Compare the expected call with the proposed function and arguments.
- Read LED state with `GET /state` after execution.
- Read temperature and humidity from the actual `read_environment()` return.
- Keep one TCP connection for the dialogue or session.

Disconnecting resets the LEDs. Restore the next comparison's initial state.


---

## Block 1, 16–20 min: Running and reading evaluation

`uv run ex01` evaluates 16 cases automatically. Results from one CPU run:

| Metric | baseline | tuned |
|---|---:|---:|
| Actual control success | 9/16 (56.25%) | 10/16 (62.5%) |
| False-call rate | 1/6 | 0/6 |
| Median | 68.5ms | 69.6ms |
| p95 | 206.8ms | 236.9ms |

Each model has one 256-token budget error, included in the 16 cases.
p95 is the maximum here. One changed case does not establish general improvement.

<!-- Source: course-preparation measurement with fresh-process restoration and actual control, 2026-11-13. Mac arm64 CPU, JAX 0.12.0.1, cactus-compute 4.2.0. -->

---

## Block 1, 20–50 min: Before/after control evaluation lab

[Lab](lab.md#1교시-실습-학습-전후-제어-평가) · [Example guide](examples/period1/README.md)

`uv run ex01`

Evidence to inspect:

- Same unseen cases, 4-bit/20-layer models, and initial state
- Expected calls, proposed calls, function returns, and actual state
- Total attempts and causes of failure

Follow the lab's detailed timing. Disconnect when finished.


---

## Block 1, 50–60 min: Break

Confirm that the control connection is disconnected.

Carry the evaluation's error cases into Block 2.
Mark unexecuted items as unverified.


---

## Block 2, 0–4 min: Error categories

| Observation | Category |
|---|---|
| `turn_on` for an off request | Wrong function |
| `turn_off` with the wrong LED index | Wrong argument meaning |
| Proposed brightness of 300 | Range validation failure |
| Correct call, failed state read | Connection or execution error |

These are illustrative cases. Classify your own observed results.


---

## Block 2, 4–8 min: Re-entering a corrected request

```sh
uv run ex02
```

`src/ex02_improve/__init__.py` reads Week 12 `tuned.cact`.

Re-enter the request with explicit index, action, and brightness.
Compare original and revised inputs, calls, and state from the same initial state.
Keep revised-request success separate from the original evaluation score.

---

## Block 2, 8–12 min: Repeated input and context

`ex02` accepts repeated inputs, but every request is independent.

- The shared predictor calls `reset()` for each request.
- Do not infer the index of “that LED” from prior context.
- Re-entering requests does not train the weights.

Skip blank input and enter `/bye` to exit.

<!-- Source: https://cactuscompute.com/blog/needle-python-docs ; reset and exit behavior are course design -->

---

## Block 2, 12–16 min: Tool descriptions and training data

Change tool descriptions in `ex02_improve`'s `DESCRIPTIONS = {}`.
Record before/after results with separate development examples.

Keep descriptions identical in a LoRA before/after comparison.
Keep unseen evaluation prompts and answers out of training data.

The UI uses saved `tuned.cact` and the shared default descriptions.
It does not automatically inherit description changes from `ex02`.

---

## Block 2, 16–20 min: Retraining and reevaluation

Follow the [Week 12 procedure](../week12_ai_service_deploy/README.md) for retraining.

Start with `EPOCHS=4`, `BATCH_SIZE=4`, `MAX_LEN=1024`, `LEARNING_RATE=1e-4`.
Stop before training if the longest example exceeds `MAX_LEN`; do not truncate it.

Save adapters and `.cact`, restore in a fresh process, and evaluate unseen cases.
Lower loss alone does not establish better control. `confidence=None` is not zero.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle ; constants and length checks are course code -->

---

## Block 2, 20–50 min: Error analysis and correction lab

[Lab](lab.md#2교시-실습-오류-분석과-수정-대화) · [Example guide](examples/period2/README.md)

`uv run ex02`

Record original requests, corrected requests, and actual state together.
Explain the change, its reason, and conditions for checking it again.

Distinguish repeated input, conversation context, and weight training.
Follow lab timing and disconnect on exit.


---

## Block 2, 50–60 min: Break

Keep your before/after notes and disconnect.

In Block 3, inspect the same control flow in Streamlit.


---

## Block 3, 0–4 min: Starting Streamlit

```sh
uv run ex03
```

Open `http://127.0.0.1:8501` manually after the headless server starts.

Click “시뮬레이터 연결”, enter a “제어 요청”, and click “요청 실행”.
Use only one control window per PC.

---

## Block 3, 4–8 min: Model cache and session connections

- Cache model preparation with `st.cache_resource`.
- Reuse TCP connections through `st.session_state`.
- Group `reset()` and `complete()` inside the shared `Lock`.
- Reset conversation context for every request.

Keep sockets out of the global model cache.
Separate windows do not receive separate simulator state.

---

## Block 3, 8–12 min: Reruns and duplicate calls

Process a new call when the user submits with “요청 실행”.
Read current LED state when the page reruns.

- A rerun without input must not execute the same control call again.
- Reuse the session's TCP connection.
- The same sentence submitted again is a new input.

Unchanged LEDs alone do not prove that no duplicate occurred.

---

## Block 3, 12–16 min: Evidence on screen

Display the original request, proposed calls, and validation result.

Read function returns and `GET /state` to display actual LED state.
Compare sensor values with the `read_environment()` return.

Distinguish blank input, no-call responses, and validation failures.
Do not display model-generated numbers as sensor readings.


---

## Block 3, 16–20 min: Disconnecting and verification scope

Click “연결 해제” and confirm the LED reset.
Then stop the server with `Ctrl+C` in the terminal.
Closing a browser tab alone does not guarantee disconnection.

After Week 12 retraining overwrites the same model path, stop the server
and restart with `uv run ex03`. A browser refresh alone does not update the model.

---

## Block 3, 20–50 min: Streamlit control UI lab

[Lab](lab.md#3교시-실습-streamlit-제어-ui) · [Example guide](examples/period3/README.md)

`uv run ex03`

Compare requests, calls, function returns, and actual state.
Check reruns without input separately from new submissions.
Confirm explicit disconnection and the LED reset.

Follow the lab's detailed timing. Record which items you could not run.


---

## Block 3, 50–60 min: Break

Disconnect control and stop the Streamlit server.

Week 14 introduces the final chatbot's public evaluation specification.
Keep the Week 12 control-model assignment separate from the Week 15 WKU introduction chatbot final.
