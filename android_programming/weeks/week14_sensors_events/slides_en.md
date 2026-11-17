---
marp: true
theme: default
paginate: true
header: Android Programming · 14
footer: RoomControl · LAN/TCP
---

# Room status and call events

Week 14 · RoomControl

Connect on the connection screen.
Use the control screen to check your room.

Desk lamp → indoor temperature and humidity → call history

---

# Day 1 schedule

30 minutes of explanation and demonstration + 60 minutes of practice

1. Connect and check the lamp
2. Add the sensor button
3. Display the response
4. Change the sliders and request again

---

# Day 1 · 0–5 min: Connect and open controls

Run WlEno on the PC.

Emulator: `10.0.2.2:8266`
Physical device: PC LAN IPv4 + `:8266`

Reuse the connection screen.

---

# Day 1 · 5–10 min: Request room readings

[Check temperature/humidity] → `dht11` → response → display

```kotlin
binding.sensorButton.setOnClickListener {
    send("dht11")
}
```

One click sends one request.

---

# Day 1 · 10–18 min: Read two values

```json
{"result":"ok","value":"[24.5,40.0]"}
```

The value field is a string containing an array.

```kotlin
val values = JSONArray(WlenoMessage.value(line) ?: return)
val temperature = values.getDouble(0)
val humidity = values.getDouble(1)
```

---

# Day 1 · 18–25 min: Units and update timing

Temperature: 24.5 °C / Humidity: 40.0 %

Moving a simulator slider does not update the app immediately.
Press the sensor button again to get the new values.

Do not hard-code sensor readings.

---

# Day 1 · 25–30 min: Check behavior

| Action | App result |
|---|---|
| Request readings | Current values |
| Change sliders | Previous values remain |
| Request again | Updated values |

Practice: add controls → process response → capture before/after

---

# Day 2 · 0–8 min: Calls start in the simulator

Use WlEno [Input button] as the room call button.

```json
{"event":"input","index":0,"value":1}
```

An event arrives without an app request.
The next press changes value to 0.

---

# Day 2 · 8–16 min: Separate events and replies

```kotlin
if (WlenoMessage.event(line) == "input") {
    showInput(line)
    return@onMessage
}
```

Classify input events first.
Do not add sensor replies to call history.

---

# Day 2 · 16–23 min: Display call history

Input index 0 · value 1
Input index 0 · value 0

Append one row for each input.
Keep the latest 20 rows for this control screen.
A new control screen starts a new history.

---

# Day 2 · 23–30 min: Recover after disconnect

Simulator [Disconnect] → controls disabled

[Connection screen] → connect again → use controls

Backgrounding or rotating also closes the connection.
Missed calls are not replayed after reconnection.

---

# Practice submission

- Before/after sensor screenshots
- Two call-history rows
- `ControlActivity.kt` and `activity_control.xml`
- One sentence comparing requests and external events

Reuse the provided connection screen and communication library.
