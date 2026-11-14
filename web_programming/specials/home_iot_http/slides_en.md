---
marp: true
theme: default
paginate: true
header: "Web Programming · HTTP Home IoT Research"
footer: "GET · PATCH · Automatic control · Experiment records"
---

# Home IoT Control over HTTP

Study requests, state, and control policies in a Node.js virtual room.

- Control a light and a fan with HTTP requests.
- Extend manual commands to polling and automatic control.
- Compare policies with identical inputs; observe failure and recovery.
- Summer research class: no fixed duration or session count.

[Research lab](lab.md) · [Walkthrough](walkthrough.md)

---

## Foundations and research stages

| Stage | Evidence of progress |
|---|---|
| Requests and state | Explain GET/PATCH requests and responses. |
| Sensor input and decisions | Determine fan state from a temperature rule. |
| Polling | Compare intervals, request counts, and response delay. |
| Policy comparison | Test single threshold and hysteresis with identical inputs. |
| Failure and recovery | Observe retry and stop behavior. |

Use observations to choose the next experiment. No fixed report length.

---

## The server holds the state

Browser → HTTP request → Node server → JSON response → view

- The server stores the light, fan, and temperature in memory.
- The dashboard and student pages use the same server.
- Temperature is a simulated sensor value entered by the student.
- Turning on the fan does not lower the temperature.
- Restarting the server resets device state and request history.

---

## Run the local server

Working directory: home_iot_http. Requirement: Node.js 24 or later.

```bash
node examples/simulator/server.mjs
```

- Open http://localhost:8014/ for the virtual room.
- No package installation or external account is required.
- Keep the entire lesson folder so the exercise links work.
- Verify execution locally. GitHub Pages cannot run this Node server.

---

## ex01: Read current state with GET

```js
const response = await fetch('/api/state');
if (!response.ok) throw new Error('Could not read state.');
const state = await response.json();
```

- The first await waits for a response; the second parses JSON.
- GET reads the current state stored on the server.
- At /examples/ex01/, compare responses before and after a change.

---

## Compare JSON with Network details

```js
state.light.on                    // true or false
state.light.brightness            // integer: 0–100
state.fan.on                      // true or false
state.environment.temperature     // number: 10–40
```

F12 → Network → read state button

Find GET, /api/state, status 200, and the JSON response.
Compare the values in the view with the response from the server.

---

## ex02: Change the light with PATCH

```js
const response = await fetch('/api/devices/light', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ on: true, brightness: 65 })
});
```

In /examples/ex02/app.js, change brightness to 20 and then 90.
Save → reload → run the button; inspect the request body and state.

---

## Invalid requests preserve state

Send brightness 101 and compare it with a valid request.

| Observation | Expected result |
|---|---|
| Response status | 400 |
| Response body | Allowed range message |
| Server brightness | Last valid value remains |

fetch does not throw just because an HTTP response has status 400.
Check response.ok and inspect the failed response in Network.

---

## ex03: Read temperature and decide once

```js
const shouldRun = state.environment.temperature >= 28;
await fetch('/api/devices/fan', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ on: shouldRun })
});
```

Apply 27°C and 29°C, clicking the control button after each input.
Change the threshold to 30°C and compare the same inputs.
This example checks only when its button is clicked.

---

## Complete the basic student code

Edit examples/student/app.js.

- Read and display the state with GET.
- Turn on the light and set brightness to 40% with PATCH.
- Control the fan using a 27°C threshold.
- Check requests and results at 26°C and 29°C.

Use the [reference implementation](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/home_iot_http/examples/reference/app.js) to compare code.
Distinguish input temperature, threshold, and actual server fan state.

---

## Polling in the automatic controller

Address: /examples/automatic/

- Start with a single threshold of 27.5°C and a 2000ms wait.
- Read temperature and actual fan state, then decide the next state.
- Send PATCH only when the decision differs from actual state.
- Read and control counters accumulate separately.
- Run only one automatic controller at a time.

Multiple controllers make it harder to attribute a state change to a policy.

---

## Schedule the next cycle after completion

```text
GET → decision → PATCH if needed → wait → next GET
```

- The runner schedules the next cycle with setTimeout.
- It waits for the current GET and any PATCH to finish.
- The actual period includes request time plus the configured wait.
- Start is disabled while the controller is active.
- Stop cancels the next schedule and the current response wait.

Find the scheduling point in runner.js before adding a repeating timer.

---

## Experiment: Interval and response delay

Compare waits of 500, 2000, and 5000ms using the same input sequence.

| Changed variable | Fixed conditions | Observations |
|---|---|---|
| Polling wait | Policy, inputs, observation window | GET count, reaction delay |

Change temperature just after a read and just before the next read.
Record how shorter waits affect request counts and reaction delay.
Use both Network details and the controller observation history.

---

## A single threshold switches at one boundary

```js
return temperature >= settings.threshold;
```

At 27.5°C, enter 27.4 → 27.6 → 27.4 → 27.6°C.

- Wait until each value is observed before applying the next one.
- The fan changes state whenever input crosses the boundary.
- Input fluctuations near the boundary can cause frequent switching.

The temperature slider uses 0.1°C steps. Arrow keys allow fine adjustment.

---

## Hysteresis uses two boundaries

```js
if (temperature >= settings.high) return true;
if (temperature <= settings.low) return false;
return currentOn;
```

- At or above the upper boundary, 29°C: on
- At or below the lower boundary, 26°C: off
- Between 26°C and 29°C: keep the previous state

The same 27°C can produce different results depending on previous state.

---

## Compare policies with identical inputs

Initial conditions: fan off, temperature 26°C, other controllers stopped

```text
26 → 27 → 28 → 27 → 28 → 29 → 28 → 27 → 26°C
```

1. Apply the sequence using a single 27.5°C threshold.
2. Save the observations and restore the initial conditions.
3. Repeat with hysteresis: lower 26°C, upper 29°C.
4. Explain differences in fan transitions and control counts.

Wait for each temperature to appear in the observation history.

---

## Separate accumulated records by experiment

Starting and stopping do not reset counters or observations.

- Download the records and reload the controller between experiments.
- Alternatively, subtract the starting counters from the final counters.
- Save needed records before reloading.
- Use start/stop entries and recorded settings to identify each run.

Do not interpret accumulated single-threshold counts as hysteresis-only data.

---

## Implement the student policy function

Edit examples/automatic_student/policy.js.

```js
function decideFan(temperature, currentOn, settings) {
  // Single threshold / upper / lower / previous state
  return null; // Complete TODOs; return true or false.
}
```

Reuse the provided HTTP, start/stop, and retry runner.
If the unfinished function returns null, the runner explains and stops.
Implement both policies and compare with the reference on the same inputs.

---

## Distinguish communication failure from state

A failed request does not mean 0°C or a stopped fan.

- Last successful response: last confirmed device state
- Communication failure: current state cannot be confirmed
- Retry wait: time before the next attempt

Each cycle has a 3-second response deadline.
AbortController cancels the browser's response wait.
It does not undo a PATCH already applied by the server.

---

## Increase the wait after repeated failures

Observe repeated failures with the default 2000ms wait.

```text
Failure → 4000ms → failure → 8000ms → failure → 10000ms
```

- Retry waits are capped at 10000ms.
- The next retry is scheduled only after the current request ends.
- Success clears the failure count and restores the normal interval.
- After Stop, restored connectivity does not restart control.

Check Network for overlapping requests or immediate retry loops.

---

## Experiment: Stop and restart the server

1. Start control and enable Preserve log in Network.
2. Press Ctrl+C in the server terminal.
3. Keep the browser page open; record failures and retry waits.
4. Restart Node with the same command.
5. Confirm successful retry and return to the normal interval.

Server memory resets to 24°C with the fan off.
Distinguish this reset from changes caused by the control policy.

---

## Experiment: Stop during a failure

- Select Offline in Network and observe a communication failure.
- Press Stop on the automatic controller page.
- Restore connectivity and check for new requests.
- Control should resume only after Start is pressed.

Use Network throttling for an additional slow-connection experiment.
A PATCH sent before Stop may already have been applied by the server.
Read the actual state with GET after reconnecting.

---

## Observation limits

| Evidence | Retention |
|---|---|
| Dashboard request history | Last 12 PATCH requests; GET excluded |
| Automatic controller view | Last 30 observations |
| Downloaded observation JSON | Last 500 observations |
| Network | Depends on browser settings and recording state |

Reloading clears observations. Download during long experiments.
Keep as many screenshots, code changes, Network records, and JSON files as needed.

---

## Research record

| Item | What to record |
|---|---|
| Hypothesis | Expected difference after a change |
| Changed variable | Condition changed in this experiment |
| Fixed conditions | Initial state, input sequence, other controllers |
| Observations | Times, states, request counts, failure and recovery |
| Interpretation and limits | Supporting evidence, counterexamples, model limits |

Separate observation from interpretation; use unexplained differences for follow-up.

---

## Scope of this simulator

- Temperature is entered manually; there is no physical cooling model.
- Fewer switches do not demonstrate better cooling performance.
- Browser timers do not guarantee precise real-time control periods.
- Real sensor error, power use, and network conditions are not modeled.
- This special lesson is excluded from the week 15 examination.

Cooling research needs a model of heat input, thermal capacity, and fan effects.

---

## Design a follow-up experiment

- Change the boundary gap; compare retained states and transition counts.
- Repeat identical inputs to examine reproducibility.
- Measure polling interval and communication delay effects separately.
- Write a policy combining temperature and brightness conditions.
- Distinguish manual-input experiments from physical-model experiments.

[Research lab](lab.md) · [Example and editable files](examples/README.md)
