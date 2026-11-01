---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 14
footer: Safe Command Sending, Input Reception, and Reconnecting
---

# Safe Command Sending, Input Reception, and Reconnecting

In week 13, you **sent** commands to the board and received its replies.
On Day 1 you **block what must not be sent**; on Day 2 you **receive and collect** data and **reconnect** when it drops.

```text
Day 1                                 Day 2
허용되지 않는 번호   ← Toast           Input history          Connection screen
보드가 오류를 알렸습니다 ← dialog       12:00:03 [24.5,40.0]   끊김
command log turns red / green         12:00:10 입력=1         [재연결]
```

On both days you can finish without a board, using the fake client (`useFake = true`).

---

# Day 1 — Blocking, Alerting, and Showing It in Color

`30 min explanation & demo → 60 min lab`

1. Allowed-number check: don't send `9`, show a Toast instead
2. Only when `준비됨`; block the buttons for 300ms right after sending
3. An AlertDialog and a red `colors.xml` log when `result` isn't `ok`
4. (Extension) `SeekBar` for `pwm 0 V`

---

## Day 1 · 0–6 min ① — Check the Number Before Sending

```kotlin
if (pin.isEmpty()) {
    Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
} else if (isAllowedIndex(pin.toInt()) == false) {
    Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
} else if (isChecked) {
    // Week 13 step 5: send("on $index")
```

- Order: **empty field → allowed number → on/off.** Calling `toInt()` on an empty string crashes the app, so the empty check comes first.
- If a check fails, there's no command and no log line. The proof is that Logcat shows **no** `writeCharacteristic` line.
- `== false` still means "if not," as in week 12.

---

## Day 1 · 0–6 min ② — Wrapping It in isAllowedIndex()

```kotlin
private fun isAllowedIndex(index: Int): Boolean {
    if (listOf(0, 1, 2, 3).contains(index)) {
        return true
    }
    if (index == -1) {
        return true
    }
    return false
}
```

- A function that **returns true/false**, like week 10's `hasBlePermissions()`. Put it at the end of the class.
- `-1` (all) is also an accepted number, since it's a reserved value. The input field can't type `-`, so only [전체 끄기] sends it.
- Passing **text** as in `contains(pin)` gives a `Type inference failed …` error — use `pin.toInt()`.

---

## Day 1 · 6–14 min ① — Only Enabled When Ready

```kotlin
Bleuno.client?.connectionState?.collect { state ->
    binding.stateText.text = "상태: $state"
    binding.ledSwitch.isEnabled = false
    binding.allOffButton.isEnabled = false
    if (state == ConnState.READY) {
        binding.ledSwitch.isEnabled = true
        binding.allOffButton.isEnabled = true
    }
}
```

- Add this inside week 12's collect, step 4. Like MainActivity's step 8: **turn everything off first, then turn it on if ready.**
- Set `android:enabled="false"` on `ledSwitch`/`allOffButton` in the XML, so they're off even before state arrives.
- The `"준비되지 않아 무시함"` line you saw in week 13 no longer appears.

---

## Day 1 · 6–14 min ② — A 300ms Pause Right After Sending

```kotlin
private fun pauseButtons() {
    binding.ledSwitch.isEnabled = false
    binding.allOffButton.isEnabled = false
    lifecycleScope.launch {
        delay(300)
        if (Bleuno.client?.isReady == true) {
            binding.ledSwitch.isEnabled = true
            binding.allOffButton.isEnabled = true
        }
    }
}
```

- Week 5's `isEnabled` + week 6's `launch { delay() }`. Call `pauseButtons()` right after each of the three `send` calls.
- If the connection drops during those 300ms, don't turn the buttons back on. `?. … == true` follows week 7's `scanJob?.isActive == true` shape.

---

## Day 1 · 14–22 min ① — colors.xml and R.color

```xml
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

```kotlin
binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
```

- `app › res › values › colors.xml` already exists in a new project. Add just **two lines**.
- `colors.xml` → `R.color`, the same way `strings.xml` → `R.string`. `#AARRGGBB`; a leading `FF` means opaque.
- This changes the color of **the whole** log field's text. Coloring a single line isn't covered here.

---

## Day 1 · 14–22 min ② — An AlertDialog When result Isn't ok

```kotlin
if (result != "ok") {
    val message = BleunoMessage.message(json) ?: ""
    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
    AlertDialog.Builder(this)
        .setTitle("보드가 오류를 알렸습니다")
        .setMessage("응답: $result · $message")
        .setPositiveButton("확인", null)
        .show()
} else {
    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_ok))
}
```

- Add this inside week 13's `if (result != null)`, below `append`. Both `err` and `fail` fall into this branch.
- `message` is `String?`, so use week 3's `?:`. Responses only arrive between `onStart` and `onStop`, so it's safe to show a dialog.

---

## Day 1 · 14–22 min ③ — Deliberately Triggering an Error to Check It

Normal use only ever produces `ok`. Change **just one spot** to produce an error response, check it, then change it back.

```kotlin
Bleuno.client?.send("on$index")     // dropped the space (change back to "on $index" after checking)
```

```text
Log    on 3
       응답: {"result":"fail","ms":"unknown command"}      ← red
Dialog 보드가 오류를 알렸습니다 / 응답: fail · unknown command
Logcat writeCharacteristic(가짜): "on3"
```

- The app log shows `on 3`, but the **text actually sent** is `"on3"`, visible in Logcat.
- Check this on the first action right after entering the control screen. Sending [전체 끄기] afterward gives `ok` and turns the log green again.

---

## Day 1 · 22–26 min — (Extension) pwm 0 V with a SeekBar

```kotlin
binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
    override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) { }
    override fun onStartTrackingTouch(seekBar: SeekBar?) { }
    override fun onStopTrackingTouch(seekBar: SeekBar?) {
        val value = binding.pwmSeekBar.progress
        Bleuno.client?.send("pwm 0 $value")
        binding.logText.append("pwm 0 $value\n")
        pauseButtons()
    }
})
```

- The same anonymous-object pattern as week 10's `object : BroadcastReceiver()`. Write all **three** functions.
- Sending on every drag tick would queue up dozens of commands. Send **once, on release**. In XML, `android:max="255"`.

---

## Day 1 · 26–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--번호-검사와-오류-표시-60분) · [Walkthrough](walkthrough.md#1일차)

1. Two colors in `colors.xml` → allowed-number check → Screenshot 1 (`9` and the Toast)
2. `enabled="false"` and collect step 13, `pauseButtons()`
3. The error display in step 16 → verify with `"on$index"`, take Screenshot 2, then change it back
4. If time remains: the (extension) `SeekBar` brightness control

**Explanation total: 6+8+8+4+4 = 30 min**

Tomorrow you receive what the board sends. The week 15 final submission is described in the [project brief](../week13_ble_output/project_brief.md).

---

# Day 2 — Receiving Input, Disconnects, and Reconnecting

`30 min explanation & demo → 60 min lab`

1. `split(" ")`, `[0]`/`[1]`, and `BleunoMessage.value`/`event`
2. Send `dht11` every 3 seconds and collect it in the input history
3. Alert and show [재연결] (Reconnect) when `끊김`
4. Warn on timeout if not `준비됨` within 10 seconds

---

## Day 2 · 0–5 min ① — Today's Syntax: split(" ") and [0]/[1]

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

## Day 2 · 0–5 min ② — Pulling Values from JSON with the Provided Helper

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

## Day 2 · 5–13 min ① — Sending dht11 Every 3 Seconds

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

## Day 2 · 5–13 min ② — Splitting a Received Line Three Ways

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
    // … same error color/AlertDialog as Day 1
}
```

- Input event → history `입력=1` / `dht11` response → history `[24.5,40.0]` / command response → command log
- Swap the order and an event lands in history as `12:00:10 1`. It still builds, which makes the bug harder to spot.

---

## Day 2 · 5–13 min ③ — Timestamping Entries in the Input History

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

## Day 2 · 13–19 min ① — Alert and Show [재연결] on Disconnect

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

## Day 2 · 13–19 min ② — Saving the Address for [재연결]

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

## Day 2 · 19–25 min ① — Setting a 10-Second Connect Timeout

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

## Day 2 · 19–25 min ② — Warn and Disconnect if Still Connecting After 10s

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

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--입력-받기끊김재연결-60분) · [Walkthrough](walkthrough.md#2일차)

1. Control screen: add the input history spot → split received lines → [온습도 받기 시작] (Start Receiving Temp/Humidity) / [중지]
2. Connection screen: save the address · [재연결] · (test) [끊김 시험] → disconnect Toast on the control screen
3. `split` a history line for a Toast → the connect timeout (verify with `delay(1000)`, then revert)
4. Two screenshots: 2 input-history lines, and `끊김` + [재연결]

**Explanation total: 5+8+6+6+5 = 30 min**

**Steps 1–2 must be done by 52 min.** Push step 3 later if you're behind. Take screenshots in portrait.

---

## What to Submit

Submit once on Day 1 and once on Day 2.

1. **Day 1**: `ControlActivity.kt`, `activity_control.xml`, Screenshot 1 (`9` and the `허용되지 않는 번호` Toast), Screenshot 2 (the red log and the error dialog)
2. **Day 2**: `ControlActivity.kt`, `MainActivity.kt`, `activity_control.xml`/`activity_main.xml`, Screenshot 1 (2 input-history lines), Screenshot 2 (`끊김` and [재연결])

Take screenshots in portrait, and keep account names and notification contents out of them.

---

## Next Week Preview

Week 15 is the **final exam (individual, hands-on)** and the **project's final submission**.

- On top of a public starter (screens / provided `bleuno/` / constants), you build three features: the permission-check flow, number-toggle with `send` and response display, and connect-timeout guidance.
- For the project, you submit the app finished to the plan you presented in week 13, plus the screenshot set and the report ([project brief](../week13_ble_output/project_brief.md)).
