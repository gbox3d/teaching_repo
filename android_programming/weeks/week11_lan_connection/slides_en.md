---
marp: true
theme: default
paginate: true
header: Android Programming · Week 11
footer: RoomControl · LAN/TCP
---

# My Room Control
## Week 11 · LAN Connection and Desk Light

Enter an address → connect → open controls → switch a light.

Create a new `RoomControl` app.
WlEno runs on the PC and displays the LED state.

---

# Learning objectives

- Connect using an address and port.
- Open the control screen after a successful connection.
- Turn the desk light on and off.

Socket, thread, and discovery code is provided.
Start a new project.

---

# Day 1 · 0–5 min: Connection screen

```text
My Room Control
Simulator address
[10.0.2.2:8266        ]
[Start control]
Status: Ready
```

Today, verify a successful connection on this screen.

---

# Day 1 · 5–10 min: Two programs

| Program | Role |
|---|---|
| Android app | Connects and sends commands |
| WlEno on the PC | Accepts connections and updates the simulator |

A LAN may use Ethernet or Wi-Fi.
The emulator and simulator can also run on the same PC.

TCP handles commands. UDP discovery is optional.

---

# Day 1 · 10–15 min: Start WlEno

Run from `tools/wleno` in the repository.

```powershell
uv run main
```

Keep the window with four LEDs open.
Each student uses a simulator on their own PC.

---

# Day 1 · 15–20 min: Address and port

| Environment | Address |
|---|---|
| Android emulator on the same PC | `10.0.2.2:8266` |
| Android phone | `PC_LAN_IPv4:8266` |

`10.0.2.2` refers to the host PC from the emulator.
`8266` is the simulator's TCP port.

Do not add `http://`.

---

# Day 1 · 20–25 min: Project and connect button

Empty Views Activity · `RoomControl`
Package: `com.example.roomcontrol`

```kotlin
val address = binding.addressEdit.text.toString().trim()
client.connect(address)
```

Keep the empty-input check from the example.
Place the provided AAR in `app/libs/`.
Follow the [shared setup](../../../tools/wleno/android/README.md) for Gradle and ViewBinding.

---

# Day 1 · 25–30 min: Connection result

| State | Action |
|---|---|
| Connecting / Checking response | Wait |
| Ready | Confirm success |
| Lost | Check simulator and address; reconnect |

Day 1: disconnect and connect again.
Day 2: keep the connection when opening the control screen.

---

# Day 1 · 60-minute lab

| Time | Task |
|---|---|
| 0–15 min | Prepare the simulator and project |
| 15–35 min | Build the connection screen |
| 35–50 min | Disconnect, fail, and retry |
| 50–60 min | Capture the Ready screen |

[Walkthrough](walkthrough.md) · [Lab](lab.md)

---

# Day 2 · 0–5 min: Light controls

```text
My Room Control
Desk light (LED 0)
[Light on]   [Light off]
Status: Ready
[Connection screen]
```

Watch both the app and simulator LED.

---

# Day 2 · 5–10 min: Open controls after success

```kotlin
startActivity(
    Intent(this@MainActivity, ControlActivity::class.java)
)
```

Run this after `ConnState.READY`.
Stay on the connection screen after a failure.

Use the provided code to preserve the socket during navigation.

---

# Day 2 · 10–15 min: Two buttons, two commands

```kotlin
binding.onButton.setOnClickListener { send("on 0") }
binding.offButton.setOnClickListener { send("off 0") }
```

| Command | Action |
|---|---|
| `on 0` | Turn LED 0 on |
| `off 0` | Turn LED 0 off |

0 is the first LED's label in the simulator.

---

# Day 2 · 15–20 min: From button to LED

1. Tap Light on.
2. The app sends `on 0`.
3. Simulator LED 0 turns on.
4. The app displays the response.

```json
{"result":"ok","ms":"led(s) on"}
```

Display the raw response this week.

---

# Day 2 · 20–25 min: Lost connection

Press Disconnect clients in the simulator.

- The app shows Lost.
- Light buttons become disabled.
- Return to the connection screen and reconnect.

LEDs reset to off on connection.
Send Light on again after reconnecting.

---

# Day 2 · 25–30 min: Leaving the screen

Going home from the control screen disconnects.
Rotation also requires a new connection in this example.

Return to the connection screen and tap Start control.

This lab focuses on controls while the app is visible.

---

# Day 2 · 60-minute lab

| Time | Task |
|---|---|
| 0–15 min | Add the control layout and Activity |
| 15–30 min | Navigate after connection success |
| 30–45 min | Turn the light on and off |
| 45–55 min | Reconnect after a drop |
| 55–60 min | Submit screenshots and source |

---

# Submission and next lesson

Submit the connection screen, controls with the lit LED,
two Activities, and two layout files.

Demonstrate connect → navigate → turn on and off.

Next week, add light selection and brightness controls.
