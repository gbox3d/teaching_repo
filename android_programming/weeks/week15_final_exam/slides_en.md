---
marp: true
theme: default
paginate: true
header: Android Programming · 15
footer: RoomControl · LAN/TCP
---

# RoomControl final practice

Week 15 · RoomControl

Connect → open controls → check lamps, readings, and calls

Day 1 rehearsal / Day 2 final practice and project submission

---

# Day 1 · 0–5 min: Assessment scope

Implementation 15 points + demonstration/explanation 5 points

- Lamp button handlers
- Sensor display
- Call history

Connection screen and communication library are provided.

---

# Day 1 · 5–10 min: Starter code

Copy `examples/rehearsal_starter` into the project.

Both screens run.
Three TODO sections in ControlActivity are incomplete.

Actual exam questions are announced separately for each term.

---

# Day 1 · 10–15 min: TODO 1 lamp buttons

With the desk lamp selected:

[On] → `on 0`
[Off] → `off 0`

Call the existing send helper.
Verify simulator LED 0 changes.

---

# Day 1 · 15–20 min: TODO 2 sensor display

[Check readings] → `dht11`

value string → JSONArray → two numbers

Display °C for temperature and % for humidity.
Change the sliders and request again.

---

# Day 1 · 20–25 min: TODO 3 call history

Simulator [Input button] → event: input

Read index and value.
Append one row per input.

Do not append sensor responses to call history.

---

# Day 1 · 25–30 min: Rehearsal checks

| Check | Expected result |
|---|---|
| Lamp on/off | LED changes |
| Sensor request | Slider values displayed |
| Two inputs | Two call rows |
| Disconnect | Controls disabled |

---

# 60-minute rehearsal

0–10 min: connection check
10–25 min: lamp handlers
25–40 min: sensor display
40–50 min: call history
50–60 min: self-check and compare with solution

---

# Day 2 · 0–10 min: Environment check

Start WlEno and the emulator.
Check the LAN address and TCP port 8266.
Open the control screen.

Report equipment problems to the instructor for recording.

---

# Day 2 · 10–20 min: Assessment process

60-minute final practice

Read task → implement → demonstrate/explain → save/submit

Edit the announced files.
Follow exam rules for use of the public solution.

---

# Day 2 · 20–30 min: Demonstration order

1. Connect from the connection screen
2. Turn the desk lamp on and off
3. Refresh sensor readings
4. Press the input button twice
5. Explain when one button or receive callback runs

---

# Submission check

Final practice code and the final project are separate submissions.

Save the code and run it once more.
Check file names and the submission location.

Use the Week 13 project brief for project requirements.
