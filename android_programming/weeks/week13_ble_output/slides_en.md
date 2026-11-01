---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 13
footer: BLE Output Control · The Project Plan Presentation
---

# BLE Output Control and the Project Plan Presentation

In week 12, tapping a list row connected you to the board up to `준비됨` (Ready).
On Day 1 you use that connection to **send commands** and **receive the board's replies.**

```text
상태: 준비됨                         보드
[3        ]  LED (●)   ──"on 3"──▶   LED 3 on
명령 로그                ◀──JSON──
on 3
응답: {"result":"ok","ms":"led(s) on"}
```

Even without a board, you can practice the same way with `useFake = true`.
On Day 2 you present your **project plan** using the very app you have built so far.

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
- `listOf` creates a list you don't change afterward. We add it to the app in week 14, Day 1.

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
- The board **does not check** whether the number is in range. Your app must block bad numbers before sending (week 14).
- This week's code has no check yet. `9` is **Fake-only** — a real board only accepts `0`–`3`.

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

# Day 2 — The Project Plan Presentation

`30 min briefing → 60 min presentation block`

1. How today runs: 3 minutes each (2 min talk + 1 min questions)
2. The five things your plan must cover, and the 10-point rubric
3. Code questions come from the code you have already written
4. Pre-presentation checklist → start

---

## Day 2 · 0–4 min — How Today Runs

```text
Now (30 min)    How it runs · what the plan covers · rubric · questions · checklist
Then (60 min)   10 min to get ready → 40 min of talks → 10 min wrap-up
                3 min each (2 min talk + 1 min questions). Groups run at the same time
```

| Students N | Evaluators E | ceil(N / E) × 3 | Against the 40 min |
|---|---|---|---|
| 20 | 1 | 60 min | Too long → E = 2 → 30 min |
| 26 | 2 | 39 min | Fits |
| 45 | 4 | 36 min | Fits (E = 3 would be 45 min) |

- One evaluator can hear **13 students**. Groups and the order were announced on Day 1.
- There is **one** project. Today it's the plan; in week 15 you submit the finished app.

---

## Day 2 · 4–12 min — The Five Things Your Plan Covers

The plan is **one page** — one A4 sheet or one screen is enough.

| # | What to include | Example |
|---|---|---|
| 1 | One line about the app | "An app that turns board LEDs on and reads temperature/humidity" |
| 2 | Screens and features | Buttons on the connect and control screens, and what each does |
| 3 | Board command list | `on 3` · `off -1` · `pwm 0 128` · `dht11` |
| 4 | Plan for the two remaining weeks | What to do in week 14 / before the week 15 deadline |
| 5 | Where you expect to get stuck, and a fallback | "If I can't get a board, I'll show the same flow with Fake" |

- In item 2, mark **which screen** each of the seven required features belongs to.
- Pick item 3 from the table in [bleuno README §2](../../bleuno/README.md#2-명령과-응답). The board doesn't know commands outside it.
- The [project brief](project_brief.md) explains all five in detail.

---

## Day 2 · 12–18 min — Rubric: 10 Points for the Plan Presentation

| Item | Points |
|---|---|
| The app, its screens and features | 2 |
| Board command list | 2 |
| Plan for the two remaining weeks | 1.5 |
| Where you expect to get stuck, and a fallback | 1.5 |
| Demo of what already works | 1.5 |
| Code explanation (spoken, individual) | 1.5 |

- **Completeness is not graded.** You lose nothing for features that don't work yet.
- You lose points when you haven't decided what to build, or the plan conflicts with the required features.
- Full table with partial credit: [rubric](rubric.md). The 20 points for the final submission come in week 15.

---

## Day 2 · 18–24 min — How the Code Question Works

You get one question about **the code you have already written.** Nothing you haven't built yet.

| Question | Where the answer lives |
|---|---|
| Why does the connection survive a rotation? | `Bleuno.client ?: Bleuno.create(…)` |
| Which line keeps only names starting with `ESP32_BLE`? | `startsWith` inside `onFound` |
| Which address do you connect to when a row is tapped? | `addresses.get(position)` → `connect` |
| Which line enables [제어 화면] only when `준비됨`? | The `ConnState.READY` branch inside collect |
| (If you did Day 1) Which lines separate the command sent from the reply received? | `send("on $index")` and `onMessage { }` |

- Open the file, **point at the line**, and answer in one sentence. Showing only the screen doesn't earn this item.
- Students who started from the week 12 solution get the same question.

---

## Day 2 · 24–27 min — Pre-Presentation Checklist

- [ ] My one-page plan has all five items.
- [ ] My command text follows the convention (name + one space + number).
- [ ] I ran the app once up to `준비됨`. Right before presenting, I leave it on the first screen.
- [ ] `MainActivity.kt` and `ControlActivity.kt` are open in editor tabs.
- [ ] I timed myself saying all five items within 2 minutes.

Finish this checklist while the person before you is presenting.
Don't build slides. You use the one-page plan, the app, and the code editor.

---

## Day 2 · 27–30 min — Presentations Start

[Day 2 lab](lab.md#2일차--과제-계획안-발표-60분) · [Project brief](project_brief.md) · [Rubric](rubric.md)

```text
0:00–0:20  Your name, one line about the app
0:20–1:00  What already works — [검색] → tap a row → 준비됨 (→ 제어 화면)
1:00–1:40  The plan — screens/features and the board command list
1:40–2:00  The two remaining weeks, where you expect to get stuck
2:00–3:00  One question → open the file → point at the line → answer in one sentence
```

**Explanation total: 4+8+6+6+3+3 = 30 min**

The first 10 minutes are for checking the order and finishing your one-page plan. Talks start at minute 10.
At 2 minutes we stop and move to the question. The week 15 submission is worth 20 points: app, screenshots, report.

---

## What to Submit

Submit the result of the Day 1 lab.

1. **`ControlActivity.kt`**, **`activity_control.xml`**
2. **Screenshot 1**: `상태: 준비됨`, with `on 3` and `응답: {"result":"ok","ms":"led(s) on"}` in the log
3. **Photo**: the board with LED 3 on (skip if you have no board/device)

The one-page project plan is handed in separately after the Day 2 presentation. Place and deadline follow the class announcement.

---

## Next Week Preview

Today, `result != null` **skipped** a line: `{"event":"input","index":0,"value":1}`.

In week 14, Day 1, the app blocks numbers that aren't allowed and reports error replies with a dialog and color.

On Day 2 you'll collect this input event and the `dht11` readings into a list, and [재연결] (Reconnect) when it goes `끊김`.
