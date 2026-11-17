---
marp: true
theme: default
paginate: true
header: Android Programming · 13
footer: RoomControl · LAN
---

# Room-control scenarios and project plan

Week 13

Day 1: study, bedtime, and leaving checks

Day 2: current app demo and project plan

No new transport API is required.

---

# Day 1 · 0–5 min · Starting screen

Choose a lamp, turn it on or off, and apply brightness.

Use the Week 12 RoomControl screen.

The app starts from a new Empty Views Activity project.

New starters can use the supplied files and shared setup.

---

# Day 1 · 5–10 min · Study setup

1. Select the desk lamp.
2. Apply maximum brightness.
3. Select the bedside lamp.
4. Turn it off.

Check: LED 0 bright, LED 1 off.

---

# Day 1 · 10–15 min · Bedtime setup

1. Select the desk lamp and turn it off.
2. Select the bedside lamp.
3. Apply low brightness.

Check: LED 0 off, LED 1 dim.

Tap Apply after moving the slider.

---

# Day 1 · 15–19 min · Leaving the room

Tap All room lights off.

```text
off -1
```

Every LED turns off regardless of selection.

Check the completion result and the simulator together.

---

# Day 1 · 19–23 min · Explain a command

```text
Selection: desk lamp
Sent: pwm 0 128
Reply: {"result":"ok","ms":"pwm set"}
Display: lamp setting complete
```

Find the command construction and reply display code.

---

# Day 1 · 23–27 min · Partner check

Give a partner only the steps for a situation.

Check whether the same light state is reproduced.

Match instructions to the actual button labels.

For a mismatch, compare lamp selection and command first.

---

# Day 1 · 27–30 min · Lab results

Use the next 60 minutes to reproduce the scenarios.

- Study setup capture
- Bedtime setup capture
- All lights off check
- Explanation of two code locations

Focus on repeatable behavior.

---

# Day 2 · 0–5 min · The finished app

Connection screen: address and Start control.

Control screen: lamp selection and brightness.

Week 14: room temperature, humidity, and call display.

The emulator and simulator support all required functions.

---

# Day 2 · 5–10 min · One-page plan

- App purpose and two screens
- Working lamp controls
- Planned sensor and call display
- Buttons mapped to commands
- Remaining schedule and run environment

A separate slide presentation is unnecessary.

---

# Day 2 · 10–14 min · UI and command

| UI | Command or input |
|---|---|
| Desk on | on 0 |
| Bedside off | off 1 |
| Desk medium brightness | pwm 0 128 |
| All lights off | off -1 |
| Read room conditions | dht11 |
| Show a call | Simulator input button |

---

# Day 2 · 14–18 min · Remaining schedule

| When | Work |
|---|---|
| Week 14 | Sensor and call display |
| Before Week 15 | Run steps and captures |
| Week 15 | Submit app and report |

Input functions can still be planned at this stage.

---

# Day 2 · 18–22 min · Three-minute talk

First minute: connect and control the lamps.

Second minute: explain planned work and schedule.

Final minute: explain code and answer questions.

Twenty students fit in 60 minutes. Follow the class schedule.

---

# Day 2 · 22–26 min · Assessment

| Part | Points |
|---|---|
| Plan and current app talk | 10 |
| Final functional demo | 12 |
| Reproduction report | 8 |

No physical board, UDP discovery, or contacts requirement.

---

# Day 2 · 26–30 min · Submission prep

Separate working functions from planned functions.

Record one item of feedback after the talk.

Final submission: source project, three captures, and report.

Exclude accounts, passwords, and personal contacts.

---

# Next class · Room inputs

Read current temperature and humidity with one button.

Show a call when the simulator input button is pressed.

Reuse the connection screen and lamp controls.

See the project brief and rubric.
