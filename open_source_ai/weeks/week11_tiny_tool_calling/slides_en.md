---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 11"
footer: "Needle3 tool calls and model comparison"
---

<!-- _class: lead -->

# Period 1 · 20-minute explanation
## Needle3 tool calling

---

## 0–3 min · Changing the proposal model

Keep the control functions, validation, and state checks from Week 10.
Replace the call proposal model with Needle3.

Observe differences on the same inputs.
Small size does not guarantee quality or speed.

---

## 3–6 min · Needle3 and call output

Needle3 is a tiny model for proposing tool calls.
The course uses `cactus-compute==4.2.0`.

`complete()` returns `function_calls`.
This week uses the baseline 2-bit engine.

[Official Python documentation](https://cactuscompute.com/blog/needle-python-docs)

---

## 6–9 min · Python project and setup

Python 3.12, one `examples/` project, `ex01`–`ex03`.
Use `main()`, scripts, and `uv_build`. Sync after script changes.

In a full clone, weekly `shared` imports `bleuno_control`.
Prepare packages and model downloads before class.

Keep the simulator running in another terminal.

---

## 9–12 min · Tools and independent cases

```python
agent = Cactus(tools=tools, auto_date=False)
agent.reset()
result = agent.complete(text)
```

`tools` is a list of the four function schemas.
`reset()` clears model history. LED restoration is separate.

---

## 12–15 min · Validate calls and read state

Python checks names and arguments in `function_calls`.
Validated calls execute the corresponding control functions.

Do not use automatic execution with `run()`.
Keep TCP 8266 open and skip `hello`/event lines.
Read actual results with `GET /state` on HTTP 8080.

---

## 15–18 min · Empty calls and confidence

An empty call list means there is no function to execute.
It may be a correct refusal or a missed call.

`confidence` is a model confidence output.
Measure accuracy and state agreement separately.

High confidence alone does not establish success.

---

## 18–20 min · Period 1 lab

Enter English and Korean requests in `uv run ex01`.
Observe on, brightness, off, and sensor operations.

Distinguish correct refusals from missed valid calls.
Record proposals, validation, and state.

Lab: 30 minutes. Break: 10 minutes.

---

<!-- _class: lead -->

# Period 2 · 20-minute explanation
## Decision models and shared-input evaluation

---

## 0–3 min · Kev makes decisions over English options

Kev-0.8B reads an English state and supplied options.
It returns probabilities over those options.

Example format: classify a request as LED, sensor, or other.
This illustrates the output format, not a measured result.

[Official Kev card](https://huggingface.co/jaredpalmer/kev-0.8b)

---

## 3–6 min · Decisions versus general tool calling

| Comparison | Needle tool calls | Kev decisions |
|---|---|---|
| Output | Function names and arguments | Probabilities over supplied options |
| Lab | Execute and evaluate | Optional card reading |

Kev lists non-English inputs and tool-call routing as out of scope.
No Kev measurements belong in this week's results table.

---

## 6–9 min · Compare the same 16 cases

`uv run ex02`: Ollama `qwen3.5:2b` versus Needle3.

Shared set: 8 Korean and 8 English cases.
10 call cases and 6 no-call cases.

Keep inputs, tools, and expected outputs fixed.
Do not give extra hints to only one model.

---

## 9–12 min · Initial conditions and inference timing

Restore LEDs to `[0, 64, 128, 255]` before every case.
Use Needle `reset()` to isolate cases.

Exclude one warm-up from scores and timings.
Record model preparation time separately.
Compare median and p95 of inference only.

---

## 12–15 min · Metrics separate different failures

Function selection accuracy.
Exact match of names, arguments, and order.
Control success requiring exact calls and matching state.
False-call rate on no-call cases.

Read language-specific cases and failure evidence too.

---

## 15–18 min · Interpret measured results

| Model | Success | False calls | Median | p95 |
|---|---|---|---|---|
| Ollama | 9/16 | 4/6 | 296.2ms | 658.2ms |
| Needle3 | 10/16 | 1/6 | 60.6ms | 179.9ms |

M1 Max, after CPU training, 256-token cap. Preparation and warm-up excluded.
p95 is the maximum of 16 values. One run includes Korean failures.
[Conditions, errors, and results by language](lab.md#수업-준비-실측)

---

## 18–20 min · Period 2 lab

Evaluate both models with `uv run ex02`.

Record proposals, states, and the five metric groups.
Explain evidence for cases that differ.
Distinguish Kev decisions from general tool calls.

Lab: 30 minutes. Break: 10 minutes.

---

<!-- _class: lead -->

# Period 3 · 20-minute explanation
## Changing tool descriptions

---

## 0–3 min · Tool descriptions and model weights

Tool descriptions are part of the model input.
Editing them does not train model weights.

This period changes descriptions for the same Needle3 model.
Keep functions, arguments, and Python validation fixed.

---

## 3–6 min · One entry in DESCRIPTIONS

Read `DESCRIPTIONS` in `ex03_descriptions`.

Translate one English description into equivalent Korean.
Or state the index and brightness ranges explicitly.
Change one condition at a time.

Keep the request language fixed during the comparison.

---

## 6–10 min · Restart with a new instance

Run `uv run ex03` with the baseline description and record results.
Exit, edit the description, and start the same command again.

Changed tools require a new `Cactus(...)` instance.
`reset()` does not replace existing tool definitions.

Compare proposals and actual state for each request.

---

## 10–14 min · Recheck valid and no-call requests

Compare names, arguments, and state on the same valid input.
Also check invalid indices, brightness, and sensor writes.

Keep boolean rejection and the four-function limit.
Do not expose `POST /set` to the model.

Look for regressions on other cases.

---

## 14–17 min · Record changes and observations

Record the edited description and its rationale.
Compare calls and actual state before and after.
Give evidence for improvement, regression, or no change.

Do not alter answers or remove unfavorable cases.
Do not report confidence as measured accuracy.

---

## 17–20 min · Period 3 lab

Record baseline results in `uv run ex03` first.
Edit one `DESCRIPTIONS` entry and restart.

Compare valid and no-call inputs under the same conditions.
Explain description editing versus weight training.

Lab: 30 minutes. Break: 10 minutes.
