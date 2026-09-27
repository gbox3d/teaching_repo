---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 15
footer: Final Exam · Individual Hands-On
---

# Final Exam: 60 Minutes Solo, Demo in Front of the Board

You rewrite, on your own, three features of the **Smart I/O Controller** you built in weeks 2–14.
There's no new syntax. Day 1 is a **public rehearsal**; Day 2 is the **real exam**.

```text
Permission check  [권한 확인] → request prompt → 권한 OK / "권한이 필요합니다" dialog
LED toggle        on 3 → 응답: {"result":"ok","ms":"led(s) on"}
Timeout           still connecting after 10s → 연결 시간이 초과되었습니다
```

The 15-point implementation is graded by running it in Fake mode; the 5-point demo happens **in front of a real board**.

---

# Day 1 — Scope, Rubric, the Starter, and a Public Rehearsal

`30 min explanation → 60 min rehearsal`

1. Final exam scope (weeks 2–14) and the two days
2. The 20-point rubric: implementation 15 + demo 5
3. Starter structure: screens / provided `bleuno/` / constants
4. The rehearsal's three features and the nine TODOs

---

## Day 1 · 0–5 min — This Week's Two Days and the Exam Scope

| Day | 30 min | 60 min |
|---|---|---|
| Day 1 | Scope, rubric, starter | **Public rehearsal** (ungraded) |
| Day 2 | Procedure, board handout, demo order | **Real exam**: implementation + individual demo & oral questions (20 pts) |

- Scope is **weeks 2–14**: screens/events, rotation, coroutines, StateFlow, permissions/storage, BLE commands and responses.
- The real exam has the **same shape** as today's rehearsal — only the wording, numbers, and details differ.
- Three features: ① the permission-check flow ② toggling an LED number and showing the response ③ connect-timeout guidance
- The final exam is 20% of the grade = implementation 15 + demo 5. It isn't part of the weekly-lab score.

---

## Day 1 · 5–12 min ① — Implementation (15 pts): Graded by Running in Fake Mode

| Item | Pts | How it's checked |
|---|---:|---|
| UI/events | 3 | Toast on empty field, 0.3s button block right after sending, wording matches the question |
| State preservation/StateFlow | 3 | State text and buttons survive rotation; timeout still fires after rotating mid-connect |
| Coroutine timeout/cancel/errors | 3 | Timeout warns and disconnects; stays quiet once ready; the `Job` is stored and canceled |
| Permissions/SharedPreferences | 3 | Permission OK / request prompt, denial dialog / settings screen, last device |
| `send`/`onMessage`/reconnect | 3 | Sending `on 3`, showing the response line/errors, allowed numbers, [재연결] |

Graders drop your **two submitted files** into the starter and run it with `useFake = true`.
Features already in the starter (S1, S2, P3) must **still work** in your submission — they get credit too. Submitting the unmodified starter earns only these three.
Detailed criteria: [rubric.md](rubric.md)

---

## Day 1 · 5–12 min ② — Demo (5 pts) and the Base Score (5 pts)

| Demo | Pts | In front of the board |
|---|---:|---|
| Output control | 2 | Turn an LED on/off by command, show the response line in the log |
| Input reception | 2 | 2 lines of `dht11` input history, stop with [중지] |
| Oral question | 1 | One question: "when does this callback get called?" |

- **Base score**: even if your implementation score would be lower than 5, you get implementation 5 as long as each TODO spot shows **an attempt at implementing it**.
- This applies even to a submission that doesn't build. A TODO comment left untouched, with no attempt, doesn't count.
- Still, a **submission that builds** earns more. Leave the parts you don't know empty, but keep it buildable.

---

## Day 1 · 12–18 min — Starter Structure: Screens / Provided bleuno / Constants

```text
com.example.smartio
├─ MainActivity.kt      Screen: connection  (TODO(1) permission · TODO(3) timeout)
├─ ControlActivity.kt   Screen: control  (TODO(2) LED toggle · response)
├─ ContactsReader.kt    provided (week 11)
└─ bleuno/              8 provided files: Bleuno · BleunoClient · BleunoMessage · ConnState …
res/layout   activity_main.xml · activity_control.xml     (do not modify)
res/values   strings.xml · colors.xml (log_ok · log_error)  constants
```

- Only **nine spots' bodies** are emptied out from your finished week-14 app. Scan, connect, disconnect, [재연결], temp/humidity, and last device are already complete.
- Constants: the five `ConnState` states, `strings.xml`, `colors.xml`. No new ids, no new files.

---

## Day 1 · 18–25 min ① — The Rehearsal's Three Features and Nine TODOs

| TODO | File · spot (comment number) | To do |
|---|---|---|
| (1) 4 spots | `MainActivity`, step 13 `hasBlePermissions()` · step 14 `showPermissionDialog()` · the `permissionLauncher` result · step 12 [권한 확인] | Check permission with `for`, show the denial dialog, handle the result, request it |
| (2) 3 spots | `ControlActivity`, step 12 `isAllowedIndex()` · step 2 the LED switch · step 8 the response branch | Allowed numbers, `send`, log the response/show errors |
| (3) 2 spots | `MainActivity`, step 50 `startConnectTimeout()` · step 51 `waitConnectTimeout()` | Store the `Job`, warn and disconnect after 10 seconds |

Fill order: **the function that's called → the place that calls it.** Each spot you finish keeps the build working.
Hints live inside the starter: step 40 `showLocationDialog()`, step 7 [전체 끄기], step 52 `listOf(…).contains(…)`.

---

## Day 1 · 18–25 min ② — Three Rules to Follow in the Starter

1. **Don't delete grayed-out imports.** `Uri`/`delay` (connection screen) and `AlertDialog`/`ContextCompat` (control screen) get used once you fill in the TODOs.
2. **Keep the `return true` / `return false` lines.** Delete only the TODO comment, and write your code **above** them.
3. **Try a shorter number for the timeout.** Fake reaches `준비됨` in 2 seconds, so the 10-second warning not appearing is expected behavior.

```text
MainActivity.kt:478:9 Unresolved reference 'delay'.     ← if you break rule 1
MainActivity.kt:398:5 Missing return statement.         ← if you break rule 2
```

`delay(10000)` → `delay(1000)` to check, then **be sure to change it back.**

---

## Day 1 · 25–30 min — The Rehearsal Begins

[Day 1 lab](lab.md#1일차--공개-리허설-60분) · [Walkthrough](walkthrough.md#1일차)

1. Drop the two starter files into week 14's `SmartIO` and run it (0–5 min).
2. Fill in TODO (1) → (2) → (3), in that order. Open the walkthrough only when you're stuck.
3. Check yourself with the checklist, then compare against `rehearsal_solution` to self-grade.

**Explanation total: 5+7+6+7+5 = 30 min**

There's no score today. Wherever you get stuck today is where you'll get stuck tomorrow.

---

# Day 2 — Exam Guidance, Board Handout, and the Real Exam

`30 min guidance → 60 min real exam (implementation + demo)`

1. Where people got stuck most in the rehearsal
2. Exam procedure, allowed materials, and what to do if something fails
3. Board handout and device checks, demo order, and oral questions

---

## Day 2 · 0–5 min — Where People Got Stuck Most in the Rehearsal

| Symptom | Cause |
|---|---|
| `Missing return statement.` | Deleted the `return true` line along with the TODO comment |
| `Unresolved reference 'delay'.` | A grayed-out import got auto-removed → use Alt+Enter |
| `Suspend function 'suspend fun waitConnectTimeout(): Unit' should be called only from a coroutine or another suspend function.` | Called it without `lifecycleScope.launch { }` |
| The app crashes when you tap the switch on an empty field | `toInt()` ran before the empty-field check |
| Red `응답: {"result":"fail","ms":"unknown command"}` | `"on$index"` — the space is missing |

A build that succeeds but behaves wrong only shows up when you **actually tap through it.** That's why there's a checklist.

---

## Day 2 · 5–10 min — Exam Procedure and the Submission Standard

```text
0–5 min    open the starter → Sync → Run ▶ (emulator, Fake) → read the question sheet and TODOs
5–20 min   feature 1          20–35 min  feature 2          35–45 min  feature 3
45–52 min  checklist (try a shorter timeout, then change it back)
52–55 min  save → run again
55–60 min  submit: MainActivity.kt, ControlActivity.kt
```

- Graders drop your **two submitted files** into the distributed starter and run it. The XML and `strings.xml` are not modified.
- When your demo slot (5–55 min) arrives, stop coding and demo. Everyone gets the same 3 minutes, so the deadline is 60 minutes for everyone (only time lost to equipment failure gets extended).
- Raise your hand if the question wording is unclear. Answers are given as **one announcement to everyone**.

---

## Day 2 · 10–15 min ① — Allowed Materials and Prohibited Actions

| Allowed | Prohibited |
|---|---|
| This course's public materials (weeks 2–15, including examples and completed rehearsal code) | Generative AI (in the browser or in Android Studio) |
| Opening your own `SmartIO` project | Sending code over messenger, email, or the cloud |
| Android Developers / Kotlin official docs | Talking with others; phones (only for the demo device, and only during the demo) |
| Autocomplete, Alt+Enter, Logcat | Search engines, blogs, Q&A sites |

If the exam announcement differs from this table, **the announcement wins.**

---

## Day 2 · 10–15 min ② — If Something Fails

| Situation | What to do |
|---|---|
| Emulator/PC freezes | Raise your hand → Cold Boot or a spare PC, log the time |
| Sync/build fails even before you've touched anything | Raise your hand → get a fresh starter |
| Board isn't blinking blue / can't be found | Raise your hand → after the instructor checks, swap the board or demo with Fake |
| Upload to the LMS fails | Raise your hand → a TA copies it to a USB drive, log the time |

- A TA logs the **time, symptom, and action taken**, and lost time is extended based on that record.
- Red underlines, build errors, or your app crashing are **your own code's fault** — not equipment failure.
- Firmware is not fixed or reflashed during the exam.

---

## Day 2 · 15–22 min — Board Handout and Device Checks

1. Get your board (and a loaner device if needed) per the seating chart. Note the `ESP32_BLE…` name on your board.
2. In Day 1's `SmartIO`, set `useFake = false` and Run ▶ on the **real device** → [권한 확인] (Check Permission) → allow.
   If you didn't finish rehearsal TODO (1)/(2), first swap in the two files from `rehearsal_solution`.
3. [검색] (Scan) → tap **your board's name** → `준비됨` → [제어 화면] → enter `0` + flip the switch → LED 0 turns on.
4. [온습도 받기 시작] (Start Receiving Temp/Humidity) → 2 lines of input history → [중지]. Leave this app **on the device** (it's for the demo).
5. Set `useFake = true` back, and set the Run target back to the emulator.

```text
☐ device recognized   ☐ 권한 OK   ☐ my board 준비됨   ☐ LED on   ☐ 2 history lines
```

Swap out boards or devices **before the exam** if something doesn't work.
Anyone not done by 22 minutes continues with a TA in the exam's first 5 minutes, and demos last.

---

## Day 2 · 22–27 min — Demo Order and the Oral Question

`T_demo = ceil(N / E) × D ≤ 50 min` (N people, E evaluators, D minutes per demo)
The demo window is the exam's 5–55 min block. Example: D = 3 min, E = 2 → N ≤ 32. Add evaluators if you exceed that.
Everyone gets the same D minutes once, so the submission deadline is 60 minutes for everyone. Only the D minutes lost to equipment failure are made up after the 60-minute mark.

| Step | What to do (D = 3 min) |
|---|---|
| ① 30s | Demo device's app → [검색] (Scan) → your board → `준비됨` → [제어 화면] |
| ② 1 min | Output control: turn an LED on/off, point at the response line in the log |
| ③ 1 min | Input reception: [온습도 받기 시작] → 2 lines → [중지] |
| ④ 30s | Oral: one sentence on **when** the callback the evaluator points to gets called |

Evaluators move seat to seat in seating-chart order. The order is posted on the board and the LMS.

---

## Day 2 · 27–30 min — The Real Exam Begins

[Day 2 lab](lab.md#2일차--본시험-60분) · [Walkthrough](walkthrough.md#2일차)

1. Phones go in your bag (the demo device only shows the app screen); keep only the allowed-materials tab open in your browser.
2. Note the time once you receive the question sheet and starter. 0–5 min is for opening and running it.
3. The last 5 minutes are for submitting. Finish editing before then.

**Explanation total: 5+5+5+7+5+3 = 30 min**
