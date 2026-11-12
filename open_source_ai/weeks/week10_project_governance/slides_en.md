---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 10"
footer: "Python functions and Ollama tool calls"
---

<!-- _class: lead -->

# Period 1 · 20-minute explanation
## Direct Python control

---

## 0–3 min · Separate control functions

Manual commands and natural language use different forms.
The LED action and validation rules stay the same.

Shared control functions let us change the input method.
We begin with direct Python control.

---

## 3–6 min · Four functions and valid inputs

| Function | Input |
|---|---|
| `turn_on(index)` / `turn_off(index)` | Integer 0–3 |
| `set_brightness(index, value)` | Index 0–3, integer value 0–255 |
| `read_environment()` | No arguments |

Reject `True` and `False` for numeric arguments.

---

## 6–9 min · One project and a shared library

Create a Python 3.12 package with `uv init --package --python 3.12 --vcs none`.
Use a full clone of `teaching_repo` for the lab.

Scripts connect `ex01`–`ex03` to package `main()` functions.
`uv_build` installs them. Run `uv sync` after script changes.

Weekly `shared` imports the relative path dependency `bleuno_control`.

---

## 9–12 min · Simulator and two connections

In a separate terminal at the repository root:

```powershell
uv run --python 3.12 tools/bleuno-sim/sim.py --bind 127.0.0.1
```

TCP 8266 sends commands. HTTP 8080 serves `GET /state`.
Add `--no-window` for checks without a window.

---

## 12–15 min · Persistent connection and events

A `hello` event arrives after connection.
Skip event lines while waiting for command replies.

Keep the same TCP connection during control.
New connections and disconnections reset the LEDs.

Read the state before ending the program.

---

## 15–18 min · Manual command and observed state

Run `uv run ex01` and follow its manual command syntax.

Turn on LED 0, set LED 1 to 128, turn off LED 0, read sensors.
Refresh `http://127.0.0.1:8080/state` after each command.

Record arguments, command replies, and observed state.

---

## 18–20 min · Period 1 lab

Follow the manual control tasks in the [lab](lab.md).

Compare boundary values and invalid inputs.
Check empty input, another command, and exit.
Record why functions are shared and the state before exit.

Lab: 30 minutes. Break: 10 minutes.

---

<!-- _class: lead -->

# Period 2 · 20-minute explanation
## Ollama tool calling

---

## 0–3 min · Natural language and call proposals

“Turn on LED 0.”

The model proposes `turn_on` with `index=0`.
Python validates the arguments and executes an allowed function.
Then it reads the actual state.

A proposal alone does not change the device.

---

## 3–6 min · Tool names and arguments

Give the model each tool's name, description, and argument schema.

`index`: LED number 0–3.
`value`: integer brightness 0–255.

Declare only the four control functions.
Do not expose sensor mutation with `POST /set`.

---

## 6–9 min · Connect the same Ollama model

Use `qwen3.5:2b`.
`models.ollama_predict` requests tool calls from Ollama.

`uv run ex02`

Read the proposed function name and arguments.
Compare the actual state before the next request.

---

## 9–12 min · Validation before execution

Is the function allowed?
Are required arguments present without extra arguments?
Are values integers in range, excluding booleans?

Execute only validated calls.
Record a bad proposal separately from successful blocking.

---

## 12–15 min · Rejected requests and state checks

`Turn on LED 4.`
`Set the temperature to 30 degrees.`

Request an invalid index and an unavailable operation.
Separate the proposal, validation, and actual state.

A blocked bad proposal remains a model error.

---

## 15–18 min · Repeated input and conversation state

Accept another request after each response. Skip empty lines.
Repeated input and retained conversation are different.

Distinguish “Turn it off” from “Turn off LED 0.”
Evaluation items do not rely on earlier conversation.

Device connection state and model history are separate.

---

## 18–20 min · Period 2 lab

Enter requests in `uv run ex02`.

Compare valid, out-of-range, and unsupported requests.
Record actual responses to Korean and English inputs.
Separate success text from state agreement.

Lab: 30 minutes. Break: 10 minutes.

---

<!-- _class: lead -->

# Period 3 · 20-minute explanation
## Repeated checks on the same inputs

---

## 0–3 min · A fixed set of 16 cases

Use the shared `control_cases.json`.

8 Korean cases and 8 English cases.
10 call cases and 6 no-call cases.

Keep inputs and expected outputs fixed.
Do not change answers to match model outputs.

---

## 3–6 min · Initial state and warm-up

Restore LEDs to `[0, 64, 128, 255]` over TCP before each case.
Process model cases independently.

Exclude one warm-up from scoring and timings.
Record model preparation time separately.

Compare sensor reads with the current simulator state.

---

## 6–10 min · Selection, exact match, and control

Function selection: which functions did the model choose?
Exact match: do names, arguments, and call order all match?
Control success: exact match plus matching actual state.

False-call rate: proposals on the 6 no-call cases.
Count bad proposals even when validation blocks them.

---

## 10–14 min · Median and p95 inference time

Measure only model inference.
Exclude LED restoration, execution, and HTTP state reads.

Median is the middle value. p95 is the 95th percentile.
Handle warm-up and preparation separately.

Record numbers only after measurement.

---

## 14–17 min · Run evaluation and reproduce failures

`uv run ex03`: fixed evaluation of the same model.
`uv run ex02`: interactive reproduction of a failed input.

Separate proposal, validation, transport, and state failures.
Repeat the same input and record differences.

Keep failed cases in the record.

---

## 17–20 min · Period 3 lab

Run the same 16 cases twice.
Record accuracy metrics and inference median/p95 separately.

Reproduce one failure in `ex02`.
If all pass, explain one case's call and state evidence.

Lab: 30 minutes. Break: 10 minutes.
