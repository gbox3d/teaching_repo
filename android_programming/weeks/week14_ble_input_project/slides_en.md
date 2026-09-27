---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 14
footer: Input, Disconnects, Reconnecting, and the Project 2 Presentation
---

# Input Reception, Disconnects, Reconnecting, and the Project 2 Presentation

In week 13, you **sent** commands to the board and received its replies.
This week, you **receive and collect** data from the board, and **reconnect** when it drops.

```text
Input history                  Connection screen
12:00:03 [24.5,40.0]           끊김
12:00:06 [25.0,41.0]           [다시 시도]
12:00:10 입력=1                [재연결] [끊김 시험]
```

On Day 2, you present **Project 2** with the Smart I/O Controller you've built so far.

---

# Day 1 — Receiving Input, Disconnects, and Reconnecting

`30 min explanation & demo → 60 min implementation and demo rehearsal`

1. `split(" ")`, `[0]`/`[1]`, and `BleunoMessage.value`/`event`
2. Send `dht11` every 3 seconds and collect it in the input history
3. Alert and show [재연결] (Reconnect) when `끊김`
4. Warn on timeout if not `준비됨` within 10 seconds
5. Presentation prep and a preview of the code-explanation question

---

## Day 1 · 0–5 min ① — Today's Syntax: split(" ") and [0]/[1]

```kotlin
val line = "12:00:03 [24.5,40.0]"
val parts = line.split(" ")
println(parts[0])
println(parts[1])
```

| Expression | Result |
|---|---|
| `line.split(" ")` | `[12:00:03, [24.5,40.0]]` — a list cut at every space |
| `parts[0]` / `parts[1]` | `12:00:03` / `[24.5,40.0]`. Indices start **at 0** |
| `parts[2]` | No such slot → the app crashes if you run this |

- `parts[0]` is "get by index," the same idea as week 12's `addresses.get(position)`.

---

## Day 1 · 0–5 min ② — Pulling Values from JSON with the Provided Helper

| Received JSON | `BleunoMessage.event(json)` | `BleunoMessage.value(json)` |
|---|---|---|
| `{"event":"input","index":0,"value":1}` | `"input"` | `"1"` |
| `{"result":"ok","value":"[24.5,40.0]"}` | `null` | `"[24.5,40.0]"` |
| `{"result":"ok","ms":"led(s) on"}` | `null` | `null` |

- Same shape as week 13's `BleunoMessage.result(json)`. A missing key returns `null`.
- Don't cut JSON with `split`. Pull values with the **provided helper**.
- Input events also carry `"value"`, so check `event` **first**.
- Only the Fake board sends input events, every 10 seconds. A real board sends them as `dht11` responses.

---

## Day 1 · 5–13 min ① — Sending dht11 Every 3 Seconds

```kotlin
binding.inputStartButton.setOnClickListener {
    binding.inputStartButton.isEnabled = false
    binding.inputStopButton.isEnabled = true
    inputJob = lifecycleScope.launch {
        while (isActive) {
            Bleuno.client?.send("dht11")
            delay(3000)
        }
    }
}
```

- Same shape as week 6's `scanJob = lifecycleScope.launch { }`. `while (isActive)` means "repeat until canceled."
- Call `stopInput()` → `inputJob?.cancel()` on [중지] (Stop), on disconnect, and in `onStop`. No receiving means no sending either.

---

## Day 1 · 5–13 min ② — Splitting a Received Line Three Ways

```kotlin
val result = BleunoMessage.result(json)
val event = BleunoMessage.event(json)
val value = BleunoMessage.value(json)
if (event == "input") {
    addHistory("입력=$value")
} else if (value != null) {
    addHistory(value)
} else if (result != null) {
    binding.logText.append("응답: $json\n")
    // … same error color/AlertDialog as week 13
}
```

- Input event → history `입력=1` / `dht11` response → history `[24.5,40.0]` / command response → command log
- Swap the order and an event lands in history as `12:00:10 1`. It still builds, which makes the bug harder to spot.

---

## Day 1 · 5–13 min ③ — Timestamping Entries in the Input History

```kotlin
private fun addHistory(text: String) {
    val time = SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())
    history.add("$time $text")
    historyAdapter.notifyDataSetChanged()
}
```

```xml
<ListView
    android:id="@+id/inputList"
    android:transcriptMode="alwaysScroll" />
```

- `SimpleDateFormat(…).format(Date())` is the **pattern** for turning the current time into `12:00:03`. `Date` is `java.util.Date`.
- Same device-list pattern as week 11: `mutableListOf` → `ArrayAdapter` → `add` → `notifyDataSetChanged()`.
- `history` is used in `onStart` too, so keep it at the class level. Rotation restarts it as an empty list.

---

## Day 1 · 13–19 min ① — Alert and Show [재연결] on Disconnect

```kotlin
ConnState.LOST -> {
    binding.scanButton.isEnabled = true
    binding.retryButton.visibility = View.VISIBLE
    binding.reconnectButton.visibility = View.VISIBLE
    showLostToast()
}
```

```kotlin
private fun showLostToast() {
    Toast.makeText(this, "연결이 끊겼습니다. [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
}
```

- Add two lines to the `LOST` branch of week 12's collect, step 7. [재연결] (Reconnect) shows only when disconnected.
- Inside the collect block, `this` isn't the screen, so the Toast is pulled out into **a screen-level function** and called from there.

---

## Day 1 · 13–19 min ② — Saving the Address for [재연결]

```kotlin
// When a list row is tapped (step 43): capture and save it
lastAddress = address
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
// onCreate (step 48): read it back
lastAddress = prefs.getString("lastAddress", "") ?: ""
// [재연결] button listener (step 47): connect
client.connect(lastAddress)
```

- Save it when a list row is tapped, read it back in `onCreate`, and connect from [재연결] (week 11's pattern).
- Keeping it only in a variable resets it to `""` on rotation. Saving it survives even a full app restart.
- The disconnect Toast appears **again** on rotation, [뒤로] (Back), or returning from home — the StateFlow replays its last value.
- A real board is disconnected by cutting its power. Fake mode has a test button, [끊김 시험] (Simulate Lost): `val fake = client as FakeBleunoClient` → `fake.simulateLost()`.
- Disconnecting on the control screen shows the Toast `연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요`.

---

## Day 1 · 19–25 min ① — Setting a 10-Second Connect Timeout

```kotlin
private fun startConnectTimeout() {
    connectTimeoutJob?.cancel()
    connectTimeoutJob = lifecycleScope.launch {
        waitConnectTimeout()
    }
}
```

- Call this from both places a connection starts: tapping a list row, and [재연결].
- Same shape as week 6's `scanJob = lifecycleScope.launch { countDown() }`.
- Cancel the previous timer first, so an old connection's 10 seconds doesn't cut off a new one.
- Rotation clears the pending job along with the screen, so re-arm it in `onCreate` if still `연결 중`.

---

## Day 1 · 19–25 min ② — Warn and Disconnect if Still Connecting After 10s

```kotlin
private suspend fun waitConnectTimeout() {
    delay(10000)
    val state = client.connectionState.value
    if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
        Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
        client.disconnect()
        binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
        // … hide the ProgressBar, enable [검색], show [다시 시도]
    }
}
```

- Only while `연결 중`/`서비스 확인 중`. Don't override a screen that already reached `끊김` or `준비됨`.
- `this` inside the function is the screen, so the Toast works directly. It's `suspend` because it uses `delay`; `10000` is milliseconds.
- Fake reaches `준비됨` in 2 seconds — temporarily change the check to `delay(1000)` to test, then change it back.

---

## Day 1 · 25–30 min ① — Presentation Prep and a Preview of the Code Question

| Project 2 | Details |
|---|---|
| Required features | permission guidance · scan/connect/disconnect/state · at least one output · input reception · disconnect/timeout guidance with retry · command convention · 2–3 min demo procedure |
| Presentation | 5 minutes per person = get set up, confirm board connection + a 2–3 min demo + one code-explanation question |
| Score | Presentation 12 + report 8 = 20 · [Project brief](project_brief.md) · [Rubric](rubric.md) |

Sample code-explanation questions — **open the file → point at the line → one sentence**

- Why does the loop stop when you tap [중지]? / Why doesn't an input event land as a single numeric line?
- Why does [재연결] use the same address even after rotation? / Which line alerts you when 10 seconds pass?

---

## Day 1 · 25–30 min ② — Try It Yourself

[Day 1 lab](lab.md#1일차--입력-받기끊김재연결과-시연-리허설-60분) · [Walkthrough](walkthrough.md#1일차)

1. Control screen: add the input history spot → split received lines → [온습도 받기 시작] (Start Receiving Temp/Humidity) / [중지]
2. Connection screen: save the address · [재연결] · (test) [끊김 시험] → disconnect Toast on the control screen
3. If time remains: `split` a history line for a Toast → the connect timeout (verify with `delay(1000)`, then revert)
4. At 47 min: capture your screenshots, run through the 2–3 min demo once

**Explanation total: 5+8+6+6+5 = 30 min**

**Steps 1–2 must be done by 47 min.** Push step 3 later if you're behind. The timeout is a required feature, so add it before your presentation.
If your implementation is running behind, stop at 47 min and rehearse once anyway. Finish your own project before you present.

---

# Day 2 — Project 2 Presentation

`30 min presentation guidance & checks → 60 min presentations`

1. Today's order and presentation capacity
2. Rubric recap: presentation 12 + report 8
3. Preview of the code-explanation question
4. Pre-presentation checks, falling back to Fake if the real board fails → presentations begin

---

## Day 2 · 0–5 min — Today's Order and Presentation Capacity

| Step | What to do | Time |
|---|---|---|
| 1 | While the person before you presents, have your app on its first screen and the board blinking blue | while waiting |
| 2 | Get set up, confirm the board connection | ~1 min |
| 3 | Demo: permission → list → ready → LED → 2 input lines → disconnect → [재연결] → [해제] | 2–3 min |
| 4 | One code-explanation question | 1 min |

```text
Presentation time = ceil(N / E) × 5 min ≤ 60 min     N = number presenting, E = simultaneous evaluators
e.g. N = 24, E = 2 → 12 × 5 = 60 min
e.g. N = 30, E = 2 → 15 × 5 = 75 min → add a TA evaluator, E = 3 → 10 × 5 = 50 min
```

---

## Day 2 · 5–12 min — Rubric Recap: Presentation 12 + Report 8

| Presentation item | Points | Report item | Points |
|---|---|---|---|
| Connection flow (permission, list, state, disconnect) | 3 | How to run it and the demo procedure | 2 |
| Output control and the command convention | 2 | Screenshots of required features and code locations | 3 |
| Input reception and input history | 2 | Logcat evidence | 1 |
| Disconnect, reconnect, timeout | 2 | Record of bugs fixed | 1 |
| Code explanation (spoken, individually) | 3 | Test environment and known limitations | 1 |

- The demo stops at 3 minutes. Anything you couldn't show can be covered with report screenshots, but that item caps at **half credit** (running over time still gets full credit via report screenshots).
- Anything missed due to equipment failure (logged by a TA) can still earn full credit through a Fake demo or screenshots.
- Fake and a real board are graded by the same standard. The same cause isn't penalized twice.

---

## Day 2 · 12–20 min — Where Code-Explanation Questions Come From

| Sample question | Where to point |
|---|---|
| Why does the loop stop when you tap [중지]? | `inputJob = lifecycleScope.launch {` and `inputJob?.cancel()` in `stopInput()` |
| How do you tell an input event from a temp/humidity response? | The order `if (event == "input")` → `else if (value != null)` |
| Which line pulls just the time out of a history entry? | `history[position].split(" ")` and `parts[0]` |
| Which line makes [재연결] appear on disconnect? | The `ConnState.LOST ->` branch of the connection-state collect |
| What alerts you when a connection passes 10 seconds? | `delay(10000)` and `contains(state)` in `waitConnectTimeout()` |
| Why isn't the Toast called directly inside collect? | The `showLostToast()` function, and what `this` is inside the collect block |

Answering order: **open the file → point at the line → one sentence.** "That's just how it works" earns no credit.

---

## Day 2 · 20–27 min — Pre-Presentation Checks and Falling Back from a Real Board

- [ ] Save → re-run `Run ▶`, app opens on its first screen (`연결 안 됨`)
- [ ] `useFake` matches today's demo method (real board `false` / emulator `true`)
- [ ] Logcat `package:mine tag:BLE` is on, and both Activity tabs are open in the editor
- [ ] The report has screenshots of 2 input lines, disconnect + [재연결], and the timeout

If the real board fails: **raise your hand** → a TA logs the time, symptom, and last Logcat line → switch to `useFake = true` and demo the same sequence

If it works in Fake mode, your app is fine and it's an equipment issue (logged as a failure). If it fails in Fake mode too, it's a bug in your code.

---

## Day 2 · 27–30 min — Presentations Begin

[Day 2 lab](lab.md#2일차--2차-과제-발표-60분) · [Walkthrough](walkthrough.md#2일차)

1. The first three presenters keep their app and board on and ready.
2. Once you've presented, listen quietly and confirm your report and source were submitted.
3. Raise your hand if equipment stalls. Your app crashing from your own bug is not equipment failure.

**Explanation total: 5+7+8+7+3 = 30 min**

---

## What to Submit

Project 2 has three deliverables ([report details in the project brief](project_brief.md#레포트)).

1. **Report PDF**: how to run it and the demo procedure, screenshots of required features and code locations, Logcat evidence, a record of bugs fixed, test environment and known limitations
2. **Source archive**: the project's `app/src/main` folder
3. **Presentation**: 5 minutes per person on Day 2

---

## Next Week Preview

Week 15 is the **final exam (individual, hands-on)**.

- On top of a public starter (screens / provided `bleuno/` / constants), you build three features: the permission-check flow, number-toggle with `send` and response display, and connect-timeout guidance.
- Day 1's lab is a rehearsal; Day 2 is the real exam with an individual demo and oral questions.
