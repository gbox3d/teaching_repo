---
marp: true
theme: default
paginate: true
header: "Open Source AI Applications · Week 12"
footer: "Needle3 Tool Calling with LoRA"
---

# Week 12

## Needle3 Tool Calling with LoRA

Edit command-to-call data, then save and restore the model.

Three 60-minute blocks
20 min explanation/demo + 30 min lab + 10 min break

---

## Full Schedule

| Block | Explanation/demo, 0–20 min | Lab, 20–50 min |
|---|---|---|
| 1 | Data and function calls | Edit data, `uv run ex01` |
| 2 | LoRA and saving | Short training, `uv run ex02` |
| 3 | Restore and fair comparison | Same cases, `uv run ex03` |

50–60 min is a break in every block.
Build on Weeks 4 and 7, then connect control evaluation and Streamlit in Week 13.

---

## Block 1, 0–4 min · The Control Model Workflow

Choose functions and arguments from a user command.

- Block 1: edit data and try the base Needle model
- Block 2: train LoRA and export inference archives
- Block 3: compare the same cases in a new process

Distinguish proposed calls, execution checks, and actual state.

---

## Block 1, 4–8 min · The Four Function Contracts

| Function | Arguments |
|---|---|
| `turn_on(index)` | integer 0–3 |
| `turn_off(index)` | integer 0–3 |
| `set_brightness(index, value)` | index 0–3, value 0–255, both integers |
| `read_environment()` | none |

The executor checks the allowlist, argument names, types, and ranges.
Read sensors from function results and verify state with `GET /state`.

---

## Block 1, 8–12 min · Commands and Target Calls

`src/shared/data/train_examples.jsonl`: 48 training examples

- `query`: the command
- `answers`: exact functions and arguments, or `[]` for unsupported input
- `reasoning`: the command span supporting each value

Define tool schemas once in shared code rather than in every source row.
“LED 1 brightness 80” targets `set_brightness(index=1, value=80)`.
Record edits and reasons. Keep evaluation cases separate.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle Data format. Example count and shared schemas are course design. -->

---

## Block 1, 12–16 min · The uv Project and Entry Points

Clone the whole repository and run from this week's `examples/`.
The local dependency in `tools/bleuno-control` requires the full tree.

`main()`: entry function, `[project.scripts]`: command mapping
`uv_build`: package build/install, rerun `uv sync` after script edits

Inspect a package once in a separate practice directory.
```powershell
uv init --package --python 3.12 --vcs none week12-package-check
```
Read `.python-version`, `pyproject.toml`, and `src/`.

---

## Block 1, 16–20 min · Needle Dialogue and Execution

```powershell
uv run ex01
```

Start at `main()` in `src/ex01_data/__init__.py`.
Enter a command, inspect the call, and repeat. Blank input is skipped. Enter `/bye` to exit.
The example resets history for each input, so commands are independent.

A valid format can still reverse the user's on/off intent.
Keep TCP open for the dialogue. Disconnecting resets the LEDs.

<!-- Source: https://cactuscompute.com/blog/needle-python-docs Calls and history. Independent inputs, checks, and TCP are course design. -->

---

## Block 1, 20–50 min · Data Editing and Dialogue Lab

[Lab](lab.md) · [Block 1 source guide](examples/period1/README.md)

Check commands and target calls, then explain your edits.
Use `uv run ex01` to inspect repeated inputs, empty calls, and exit behavior.
Explain the difference between repeated input and conversation history.

Use `lab.md` for the detailed 30-minute schedule.

---

## Block 1, 50–60 min · Break

Keep your edited data and observations.

Continue in the same `examples/` project next block.

---

## Block 2, 0–4 min · LoRA and Base Weights

Freeze the base weights and train LoRA updates.
Local training uses all 20 layers with 4-bit numerics.

`models/checkpoints/needle3.safetensors`: base checkpoint
`models/adapter.safetensors`: learned updates

Dependency: `cactus-compute[train]==4.2.0`
Prepare the engine and checkpoint before class.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle Local training and checkpoint. Version and paths are course specifications. -->

---

## Block 2, 4–8 min · Training Module Constants

`src/ex02_train/__init__.py`

| Constant | Current initial value | Role |
|---|---:|---|
| `EPOCHS` | 4 | training passes |
| `BATCH_SIZE` | 4 | examples per step |
| `MAX_LEN` | 1024 | preflight length limit |
| `LEARNING_RATE` | 1e-4 | update scale |

These starting values were used in the measured run and may be adjusted for the data and environment.

---

## Block 2, 8–12 min · Length Checks for Every Example

`models/training_input.jsonl` combines command examples
with the common tool descriptions as training input.

Check the longest rendered example before training.
Abort if any example exceeds `MAX_LEN`. Do not train on truncated rows.
Review training data length or the limit, then check again.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle Length risks. Full preflight checks and abort behavior are course design. -->

---

## Block 2, 12–16 min · Saved Files for Comparison

| Output | Role |
|---|---|
| `models/adapter.safetensors` | learned LoRA updates |
| `models/baseline_adapter.safetensors` | B=0, preserves base weights |
| `models/baseline.cact` | base, 4bit and 20L |
| `models/tuned.cact` | tuned, 4bit and 20L |

The provided shared function handles merging and export.
Pass a `.cact` archive to inference `weights=`.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle Merge and export. B=0 comparison files are course design. -->

---

## Block 2, 16–20 min · Loss and Unseen Cases

Loss tracks the training objective, separately from unseen-case success.
Consider overfitting if training loss falls while validation loss rises.

One Mac arm64 CPU run: 42 training rows, 6 validation rows, 44 steps.
Longest example: 305 tokens; padded length: 512.
339.4 seconds includes preparation and downloads. Other machines may differ.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle Loss and backend support. Measured run: 2026-11-13 course preparation, JAX 0.12.0.1 and cactus-compute 4.2.0. -->

---

## Block 2, 20–50 min · Local Training and Saving Lab

[Lab](lab.md) · [Block 2 source guide](examples/period2/README.md)

```powershell
uv run ex02
```

Check data, four constants, and lengths. Observe actual loss.
Verify adapter saving and `.cact` export separately.
A 30-minute lab does not guarantee completion. Record any blocked step.

---

## Block 2, 50–60 min · Break

Keep the actual output paths and your observations.

Check whether the training process has exited.

---

## Block 3, 0–4 min · Model Restoration in a New Process

```powershell
uv run ex03
```

`src/ex03_restore/__init__.py` loads both `.cact` files in turn.
Restore from saved files in a fresh process.
`ex03` evaluates 16 cases without interactive input.

Check file existence and successful loading separately.
Verify compatibility between the engine and export package.

<!-- Source: https://cactuscompute.com/blog/needle-python-docs Weights and compatibility. Module and evaluation command are course design. -->

---

## Block 3, 4–8 min · Identical Cases and Conditions

Compare base 4bit/20L with tuned 4bit/20L.
A shipped 2-bit base versus a 4-bit tuned model mixes in quantization effects.

16 cases: 8 Korean, 8 English, 10 call cases, 6 no-call cases
Their strings differ from the 48 training rows. This alone does not prove semantic independence.

Keep tool descriptions, generation settings, and history resets identical.
Restore LEDs to `[0, 64, 128, 255]` before every case.

<!-- Source: https://cactuscompute.com/blog/finetuning-needle Local 4-bit and shipped 2-bit. Conditions and cases are course design. -->

---

## Block 3, 8–12 min · Calls and Actual State Metrics

| Metric | Evidence |
|---|---|
| Function accuracy | expected names and call-list order |
| Exact calls | argument names, values, and order |
| Actual-state success | exact calls, execution, LED/sensor state |
| False-call rate | calls on no-call cases |
| Median and p95 | measured latency, units, and denominator |

Distinguish JSON dictionary key order from function-call list order.
Read sensor values from function results. Local LoRA confidence is `None`.

<!-- Source: https://cactuscompute.com/blog/needle-python-docs Local LoRA confidence. Metrics follow the course shared code. -->

---

## Block 3, 12–16 min · Error Analysis and Improvement

| Observation | Base 4bit/20L | Tuned 4bit/20L |
|---|---:|---:|
| Actual control success | 9/16 (56.25%) | 10/16 (62.5%) |
| Korean / English | 2/8 / 7/8 | 3/8 / 7/8 |
| Calls on no-call cases | 1/6 | 0/6 |
| Median / p95 | 68.5 / 206.8 ms | 69.6 / 236.9 ms |

Each denominator includes one token-budget error. Here p95 is the maximum.
This is one run. Analyze the remaining function and argument errors.

<!-- Source: 2026-11-13 course preparation: fresh-process restoration and actual control. Same 16 cases, schema, initial state and engine. No general improvement guarantee. -->

---

## Block 3, 16–20 min · Assignment Results and Explanations

[Assignment](assignment_brief.md) · [Qualitative rubric](assignment_rubric.md)

Explain data edits, training, saving, and restoration in a new process.
Record before/after calls on the same unseen cases and analyze causes.
Attempts, specific questions, and verification also provide evidence.

Full marks require the requested results and accurate explanations.
University notices set points and deadlines. This differs from the Week 15 chatbot final.

---

## Block 3, 20–50 min · Restoration and Comparison Lab

[Lab](lab.md) · [Block 3 source guide](examples/period3/README.md)

Use `uv run ex03` to load both files and compare the same 16 cases.
Record expected, base, and tuned calls side by side.
Explain actual metrics, errors, and the next verification step.

Leave unmeasured results marked unmeasured.
Use `lab.md` for the detailed 30-minute schedule.

---

## Block 3, 50–60 min · Break

Explicitly disconnect and verify the LED reset.

Continue with control evaluation, error improvement, and Streamlit in Week 13.
