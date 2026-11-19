---
marp: true
theme: default
paginate: true
header: Android Programming · 12
footer: RoomControl · LAN
---

# Choose room lights and brightness

Week 12

Connect on the first screen. Control room lights on the second.

Day 1: desk and bedside lamps

Day 2: brightness and all lights off

---

# Day 1 · 0–5 min · The control screen

- Desk lamp: LED 0
- Bedside lamp: LED 1
- Turn on / Turn off
- Result after the reply

The user chooses a lamp by its room function.

---

# Day 1 · 5–9 min · Open the controls

1. Start WlEno on the PC.
2. Check the simulator address in the app.
3. Tap Start control.
4. The control screen opens after connection.

Reuse the supplied connection screen and client.

---

# Day 1 · 9–13 min · One selection group

Place two RadioButtons in one RadioGroup.

| ID | Lamp | LED |
|---|---|---|
| deskRadio | Desk | 0 |
| bedRadio | Bedside | 1 |

Select the desk lamp by default.

---

# Day 1 · 13–17 min · Selection to index

```kotlin
private fun selectedLamp(): Int {
    return if (binding.deskRadio.isChecked) 0 else 1
}
```

Desk selected: 0

Bedside selected: 1

---

# Day 1 · 17–21 min · Build the command

```kotlin
binding.onButton.setOnClickListener {
    send("on ${selectedLamp()}")
}
binding.offButton.setOnClickListener {
    send("off ${selectedLamp()}")
}
```

Turning on the bedside lamp sends `on 1`.

---

# Day 1 · 21–26 min · Confirm the reply

```json
{"result":"ok","ms":"led(s) on"}
```

After a tap: waiting for a reply.

After an `ok` reply: lamp setting complete.

Small text below shows the command and raw JSON.

---

# Day 1 · 26–30 min · Check the sequence

Turn on the desk lamp, turn on the bedside lamp, then turn off only the desk lamp.

| Check | Expected |
|---|---|
| Desk | Off |
| Bedside | On |
| Completion | After the server reply |

Implement the controls during the next 60 minutes.

---

# Day 2 · 0–5 min · Lighting for a situation

Study: bright desk lamp, bedside lamp off.

Bedtime: desk lamp off, dim bedside lamp.

Leaving: all room lights off.

Choose a lamp and brightness on the same screen.

---

# Day 2 · 5–10 min · Brightness slider

`brightnessBar` is a SeekBar.

| Position | Value | Result |
|---|---|---|
| Left | 0 | Off |
| Initial | 128 | Medium |
| Right | 255 | Maximum |

XML: `max="255"`, `progress="128"`

---

# Day 2 · 10–15 min · Apply brightness

```kotlin
binding.pwmButton.setOnClickListener {
    send("pwm ${selectedLamp()} " +
        "${binding.brightnessBar.progress}")
}
```

`pwm 0 128`: desk lamp, brightness 128.

Move the slider, then tap Apply once.

---

# Day 2 · 15–19 min · Turn all lights off

```kotlin
binding.allOffButton.setOnClickListener {
    send("off -1")
}
```

`-1` means every LED.

This command ignores the current lamp selection.

---

# Day 2 · 19–23 min · Result and evidence

Large result: lamp setting complete.

Small command text: `pwm 0 128`

Raw reply:
```json
{"result":"ok","ms":"pwm set"}
```

Read `result` using `WlenoMessage.result(line)`.

---

# Day 2 · 23–27 min · Finish and reconnect

Returning to the connection screen closes the control connection.

Tap Start control again to use it.

WlEno preserves LED states on connection and disconnection.

Reconnect after leaving the app or rotating the screen.

---

# Day 2 · 27–30 min · Lab checks

1. Create the study and bedtime settings.
2. Capture the app and WlEno together.
3. Explain both numbers in `pwm 0 128`.
4. Ask a partner to repeat the steps.

Implement brightness during the next 60 minutes.

---

# Submission and next class

Submit ControlActivity, its XML layout, and two scene captures.

Explain where the selected lamp and brightness enter the command.

Next: check room-control scenarios and present a project plan.

See the walkthrough and lab sheets.
