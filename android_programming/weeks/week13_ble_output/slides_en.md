---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 13
footer: BLE Output Control · String Commands and Responses
---

# BLE Output Control: String Commands and Responses

In week 12, tapping a list row connected you to the board up to `준비됨` (Ready).
This week, you use that connection to **send commands** and **receive the board's replies.**

```text
상태: 준비됨                         보드
[3        ]  LED (●)   ──"on 3"──▶   LED 3 on
명령 로그                ◀──JSON──
on 3
응답: {"result":"ok","ms":"led(s) on"}
```

Even without a board, you can practice the same way with `useFake = true`.

---

# Day 1 — Sending Commands and Receiving Responses

`30 min explanation & demo → 60 min lab`

1. Preview: `listOf(0, 1, 2, 3).contains(index)`
2. The bleuno command convention: command name + a space + LED number
3. How the special lecture's write/notify are wrapped as `send`/`onMessage`
4. Switch → `send`, receive responses in `onStart`, release in `onStop`

---

## Day 1 · 0–5 min — Today's Syntax: listOf(0, 1, 2, 3).contains(index)

```kotlin
val index = 9
if (listOf(0, 1, 2, 3).contains(index)) {
    println("보낼 수 있는 번호: $index")
} else {
    println("허용되지 않는 번호: $index")
}
```

| `index` | `listOf(0, 1, 2, 3).contains(index)` |
|---|---|
| `3` | `true` |
| `9` / `-1` | `false` |

- `true` if the value **is in** the list. Put the **same kind** of value (numbers) inside the parentheses.
- `listOf` creates a list you don't change afterward. We add it to the app on Day 2.

---

## Day 1 · 5–13 min ① — The bleuno Command Convention

| Text sent | Meaning | Board's response |
|---|---|---|
| `on 3` | Turn on LED 3 | `{"result":"ok","ms":"led(s) on"}` |
| `off 3` | Turn off LED 3 | `{"result":"ok","ms":"led(s) off"}` |
| `off -1` | Turn off all | `{"result":"ok","ms":"led(s) off"}` |
| `pwm 0 128` | Brightness of LED 0 (0–255) | `{"result":"ok","ms":"pwm set"}` |
| `dht11` | Read temperature/humidity (week 14) | `{"result":"ok","value":"[24.5,40.0]"}` |
| `on3`, `hello` | Unknown command | `{"result":"fail","ms":"unknown command"}` |

- Rule: **command name + one space + number.** The library appends the trailing `\n`.
- **Each** command gets **one line** of JSON response.
- Full table: [bleuno README section 2](../../bleuno/README.md#2-명령과-응답)

---

## Day 1 · 5–13 min ② — N Is the LED Number; the Response Is One JSON Line

| LED number | 0 | 1 | 2 | 3 | -1 |
|---|---|---|---|---|---|
| Board pin | GPIO4 | GPIO3 | GPIO1 | GPIO0 | all |

- The `3` in `on 3` is not a GPIO pin — it's the **LED number**. The classroom board has 4 LEDs.
- The board **does not check** whether the number is in range. Your app must block bad numbers before sending (Day 2).
- Today's Day 1 code has no check yet. `9` is **Fake-only** — a real board only accepts `0`–`3`.

| `result` | Meaning |
|---|---|
| `ok` / `err` / `fail` | success / right command, wrong value / unknown command |

---

## Day 1 · 13–20 min ① — The Special Lecture's write/notify as send/onMessage

```text
App (ControlActivity)       Inside RealBleunoClient (special-lecture code)      Board
send("on 3")        ──▶  writeCharacteristic("on 3\n")        ──▶  LED 3 on
                         onCharacteristicWrite → next command
onMessage { json } ◀──  onCharacteristicChanged (notify)     ◀──  {"result":"ok",…}
```

- The `writeCharacteristic` call and notification callback you wrote by hand in the special lecture are **still there, unchanged**, inside the library.
- We only handle **the text we send** and **the text we receive**. UUIDs and byte conversion are the library's job.
- The library calls `onMessage`'s braces on the **main thread** (like week 5's `Handler`).

---

## Day 1 · 13–20 min ② — The Write Queue: Commands Go Out One at a Time

```text
send: queued "on 3" (1 waiting)
writeCharacteristic("on 3") called, result=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","ms":"led(s) on"}
```

- BLE needs the write-finished callback (`onCharacteristicWrite`) before it can write the **next** value.
- So `send` puts commands in a **queue** and sends them in order. Tap fast enough and you'll see `2 waiting`.
- Fake log: `writeCharacteristic(가짜): "on 3"` → 300ms later `onCharacteristicChanged(가짜): {…}`
- A command sent while not `준비됨` is **dropped**, logged as `send(가짜): 준비되지 않아 무시함`.

---

## Day 1 · 20–27 min ① — Flip the Switch, Call send

```kotlin
} else if (isChecked) {
    val index = pin.toInt()
    Bleuno.client?.send("on $index")
    binding.logText.append("on $index\n")
} else {
    val index = pin.toInt()
    Bleuno.client?.send("off $index")
    binding.logText.append("off $index\n")
}
```

- Keep week 4's `append` line as a **record of the command sent**, and add one `send` line above it.
- `Bleuno.client` can be `null`, as in week 12, so use `?.`. [전체 끄기] (All Off) is `send("off -1")`.
- The input field id is still week 4's `pinEdit`; it now means **LED number**. `maxLength="2"` allows up to two digits.

---

## Day 1 · 20–27 min ② — Receiving Responses in onStart

```kotlin
override fun onStart() {
    super.onStart()
    Bleuno.client?.onMessage { json ->
        val result = BleunoMessage.result(json)
        if (result != null) {
            binding.logText.append("응답: $json\n")
        }
    }
}
```

- `json` is one line of text sent by the board. Append it **as is** with `"응답: $json"`.
- `BleunoMessage.result(json)`: the `"result"` value, or `null` if there isn't one.
- In Fake mode, `{"event":"input",…}` arrives every 10 seconds while `준비됨`. It has no `result`, so it's **skipped** (week 14).

---

## Day 1 · 20–27 min ③ — Releasing in onStop, and the Path In

```kotlin
override fun onStop() {
    super.onStop()
    Bleuno.client?.onMessage(null)
}
```

- Week 10's Receiver pairing rule: **register in `onStart` ↔ unregister in `onStop`.**
- Both functions go **outside** onCreate's closing `}`, inside the class. Put them inside it and the build fails.
- You reach the control screen through **tap a list row → `준비됨` → [제어 화면]**.
- Arriving without a connection (row not tapped, or [연결] after [해제]) means `연결 안 됨`, so commands get dropped.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--명령-보내고-응답-받기-60분) · [Walkthrough](walkthrough.md#1일차)

1. `strings.xml`/`activity_control.xml`: input field hint, `maxLength`, a spot for [전체 끄기] (All Off)
2. Add `send` to the switch listener; check the sent text and response in Logcat `tag:BLE`
3. Receive and release responses in `onStart`/`onStop` → `응답: {…}` in the log
4. [전체 끄기] → `off -1` → Screenshot 1 (a photo of the LED if you have a board)

**Explanation total: 5+8+7+7+3 = 30 min**

Take the screenshot on the **first action right after entering** the control screen — once the log fills up, new lines scroll out of view.

---

# Day 2 — Blocking, Alerting, and Showing It in Color

`30 min explanation & demo → 60 min lab`

1. Allowed-number check: don't send `9`, show a Toast instead
2. Only when `준비됨`; block the buttons for 300ms right after sending
3. An AlertDialog and a red `colors.xml` log when `result` isn't `ok`
4. (Extension) `SeekBar` for `pwm 0 V`, and the Project 2 announcement

---

## Day 2 · 0–6 min ① — Check the Number Before Sending

```kotlin
if (pin.isEmpty()) {
    Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
} else if (isAllowedIndex(pin.toInt()) == false) {
    Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
} else if (isChecked) {
    // Day 1 step 5: send("on $index")
```

- Order: **empty field → allowed number → on/off.** Calling `toInt()` on an empty string crashes the app, so the empty check comes first.
- If a check fails, there's no command and no log line. The proof is that Logcat shows **no** `writeCharacteristic` line.
- `== false` still means "if not," as in week 12.

---

## Day 2 · 0–6 min ② — Wrapping It in isAllowedIndex()

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

## Day 2 · 6–14 min ① — Only Enabled When Ready

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
- The `"준비되지 않아 무시함"` line you saw on Day 1 no longer appears.

---

## Day 2 · 6–14 min ② — A 300ms Pause Right After Sending

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

## Day 2 · 14–22 min ① — colors.xml and R.color

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

## Day 2 · 14–22 min ② — An AlertDialog When result Isn't ok

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

- Add this inside Day 1's `if (result != null)`, below `append`. Both `err` and `fail` fall into this branch.
- `message` is `String?`, so use week 3's `?:`. Responses only arrive between `onStart` and `onStop`, so it's safe to show a dialog.

---

## Day 2 · 14–22 min ③ — Deliberately Triggering an Error to Check It

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

## Day 2 · 22–26 min — (Extension) pwm 0 V with a SeekBar

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

## Day 2 · 26–30 min — Project 2 Announcement and Try It Yourself

[Day 2 lab](lab.md#2일차--번호-검사와-오류-표시-60분) · [Walkthrough](walkthrough.md#2일차)

- **Project 2**: presented on week 14, Day 2. A 2–3 minute Smart I/O Controller demo + a report
- Required: permission guidance · scan/connect/disconnect/state · **at least one output control** · input reception · disconnect/timeout guidance with retry · the command convention
- Team setup, presentation order, and the rubric will be announced separately in class.

1. Two colors in `colors.xml` → allowed-number check → Screenshot 2 (`9` and the Toast)
2. `enabled="false"` and collect step 13, `pauseButtons()`
3. The error display in step 16 → verify with `"on$index"`, then change it back → submit

**Explanation total: 6+8+8+4+4 = 30 min**

---

## What to Submit

Submit once, at the end of Day 2.

1. **`ControlActivity.kt`**, **`activity_control.xml`**
2. **Screenshot 1**: `상태: 준비됨`, with `on 3` and `응답: {"result":"ok","ms":"led(s) on"}` in the log
3. **Screenshot 2**: `9` in the input field, the Toast `허용되지 않는 번호`, and no `on 9` in the log
4. **Photo**: the board with LED 3 on (skip if you have no board/device)

---

## Next Week Preview

Today, `result != null` **skipped** a line: `{"event":"input","index":0,"value":1}`.

In week 14, you'll **receive and collect** this input event and the `dht11` temperature/humidity response,

and if the board loses power and goes `끊김`, you'll [재연결] (Reconnect). Then you'll present Project 2.
