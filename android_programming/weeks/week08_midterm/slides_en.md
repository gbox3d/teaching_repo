---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 8
footer: Midterm · Individual Hands-on Exam
---

# Midterm: Solo, 60 Minutes, Graded on the Submitted Files

You rebuild what you did in SmartIO through week 7 as **one small app**.
There is no new syntax. You write the code from weeks 2–7 **alone, within the time limit**.

```text
Rehearsal
Counting down
Time left: 3
[Start] [Cancel]      ← keeps going even if you rotate
```

---

# Day 1 — Exam Scope, Rubric, and a Public Rehearsal

`30 min explanation → 60 min rehearsal`

1. Exam scope and the 20-point rubric.
2. What counts as your submission: save, then run again.
3. The 60-minute time budget.
4. The five TODOs in the rehearsal starter.

---

## Day 1 · 0–5 min — This Week's Two Days and the Exam Scope

| Day | 30 min | 60 min |
|---|---|---|
| Day 1 | Scope, rubric, time budget | **Public rehearsal** (ungraded) |
| Day 2 | Procedure, allowed resources, what if something breaks | **Actual exam** (20 points) |

- The scope is **weeks 2–7**: buttons, ViewBinding, `isEnabled` / rotation / coroutines / ViewModel and StateFlow.
- The actual exam has the **same shape** as today's rehearsal. Only screen names, wording, and small requirements differ.
- Two threads run through it: ① button → coroutine (delay, cancel, error) ② surviving rotation (ViewModel + StateFlow).

---

## Day 1 · 5–12 min ① — The 20-Point Rubric, Revealed

| Item | Points | How it's checked |
|---|---:|---|
| UI & events | 5 | Tapping works, buttons enable/disable per state, text is correct |
| Lifecycle & restoration | 5 | Text, numbers, and buttons survive a **rotation** mid-run |
| Coroutine delay/cancel/error | 5 | Counts down every second, stops after [Cancel], doesn't crash on failure |
| StateFlow collect | 3 | Values live in the ViewModel; the screen reads them via `collect { }` |
| Runs & submitted | 2 | The submitted files build and run; files and screenshots are submitted on time |

Grading is done by **running the app**. Code length is not scored.
Detailed criteria: [rubric.md](rubric.md)

---

## Day 1 · 5–12 min ② — Where Each Item Is Checked in the Code

```kotlin
private val viewModel: RehearsalViewModel by viewModels()  // restoration
job = viewModelScope.launch {                              // coroutine
    for (i in 5 downTo 1) {
        _seconds.value = i                                 // StateFlow
        delay(1000)
    }
}
viewModel.seconds.collect { seconds ->                     // collect
    binding.timeText.text = "Time left: $seconds"          // UI
}
```

- If one root cause breaks several checks, points are deducted **only once**.
- If it doesn't build, there's nothing to run. Leave a TODO you don't know **blank** so the project still builds.

---

## Day 1 · 12–17 min — What Counts as Your Submission: Save, Then Run Again

```text
Edit → Save (Ctrl+S) → Run ▶ again → check off the checklist → submit two files
```

- The grader drops **your submitted files** into the same starter and runs it. It is not a screenshot of your own emulator.
- Submit: `MainActivity.kt`, `○○ViewModel.kt`, and whatever screenshots the question asks for.
- Don't edit `activity_main.xml` or `strings.xml`. Even if you do, grading uses the starter's original versions.
- Code you haven't **run once more** after your last edit is code that hasn't been verified.

---

## Day 1 · 17–22 min — The 60-Minute Time Budget

| Time | Task |
|---|---|
| 0–5 min | Open and run the starter; read the questions and TODOs |
| 5–25 min | ViewModel-side TODOs (coroutine, cancel) |
| 25–40 min | Screen-side TODOs (buttons, collect) |
| 40–50 min | Checklist: start, complete, cancel, rotate |
| 50–55 min | Save → run again |
| 55–60 min | Submit the two files and screenshots |

If the ViewModel side isn't done by minute 25, **move on to the screen side**. Points reflect what actually works.

---

## Day 1 · 22–27 min — A Look at the Rehearsal Starter

| TODO | File · location | Task |
|---|---|---|
| (1) | `RehearsalViewModel.kt` `startCountdown()` | guard + `launch` + 5→1 + completion |
| (2) | `RehearsalViewModel.kt` `cancelCountdown()` | `job?.cancel()` + cancelled state |
| (3) | `MainActivity.kt` listeners 1 & 2 | call the ViewModel functions |
| (4) | `MainActivity.kt` collect block 3 | text + enabling/disabling buttons |
| (5) | `MainActivity.kt` collect block 4 | `Time left: 3` |

Already in place: dependencies, XML, imports, `by viewModels()`, `_state`/`state`, the `repeatOnLifecycle` block.
Fill things in from **the value producer (ViewModel) to the receiver (screen)**.

---

## Day 1 · 27–30 min — Start the Rehearsal

[Day 1 rehearsal](lab.md#1일차--공개-리허설-60분) · [Walkthrough](walkthrough.md#1일차)

1. Drop the starter files into a new `Rehearsal` project and run it (0–10 min).
2. Fill in TODOs (1) → (5) in order. Open the walkthrough only when you're stuck.
3. Check yourself against the checklist and compare with `rehearsal_solution`.

**Explanation total: 5+7+5+5+5+3 = 30 min**

There's no score today. Wherever you get stuck today is where you'll get stuck on tomorrow's exam.

---

# Day 2 — Exam Instructions and the Actual Exam

`30 min briefing → 60 min actual exam`

1. Where people commonly got stuck in the rehearsal.
2. Exam order, allowed resources, and what to do if something breaks.
3. A group PC check (running your own Rehearsal).

---

## Day 2 · 0–5 min — Where People Commonly Got Stuck in the Rehearsal

| Symptom | Cause |
|---|---|
| `Unresolved reference 'seconds초'.` | `"$seconds초"` — Hangul placed directly after `$variable` |
| [Cancel] doesn't enable (expected) | the comparison text differs from `"카운트다운 중"` |
| the number keeps counting down after [Cancel] | it wasn't stored with `job = viewModelScope.launch {` |
| rotating resets to `Waiting` (expected) | it was created directly instead of with `by viewModels()` |

The build can succeed and still be wrong — you only see that by **running it and tapping around**. That's why there's a checklist.

---

## Day 2 · 5–12 min — Exam Order

```text
0–5 min    receive starter → File › Open → Sync → Run ▶ → check the first screen
5–25 min   ViewModel-side TODOs
25–40 min  screen-side TODOs
40–50 min  checklist: start, complete, cancel, rotate (and failure, if the question has one)
50–55 min  save → run again
55–60 min  submit: MainActivity.kt, ○○ViewModel.kt, screenshots
```

- You receive the question sheet and the starter when the exam begins.
- If wording is unclear, raise your hand. Answers go out as **one announcement to everyone**.
- Full procedure: [exam_structure.md](exam_structure.md)

---

## Day 2 · 12–17 min — Allowed Resources and Prohibited Actions

| Allowed | Prohibited |
|---|---|
| This course's public materials (weeks 2–8, including examples) | Generative AI (in the browser or in Android Studio) |
| Opening your own `SmartIO` project | Sending code via messenger, email, or the cloud |
| Android Developers / Kotlin official docs | Talking with others, phones |
| Autocomplete, Alt+Enter, Logcat | Search engines, blogs, Q&A sites |

If an exam announcement differs from this table, **the announcement wins**.

---

## Day 2 · 17–22 min — If Something Breaks

| Situation | What to do |
|---|---|
| Emulator won't start / freezes | Raise your hand → Cold Boot → if that fails, move to a spare PC |
| Sync/build already failing before you touch anything | Raise your hand → get a fresh copy of the starter |
| PC freezes | Raise your hand → restart and reopen (save with Ctrl+S as you go) |
| Upload to the LMS fails | Raise your hand → the TA copies it via USB and logs the time |

- The TA records **the time, the symptom, and what was done**, and extends your time based on that record.
- Things caused **by your own code** — red underlines, build errors — do not count as a technical issue.

---

## Day 2 · 22–27 min — PC Check: Run Your Own Rehearsal

1. Open the `Rehearsal` project you built yesterday.
2. Wait for the progress indicator (Sync) at the bottom to finish, then press Run ▶.
3. Confirm the `Rehearsal` screen appears on the emulator and the Logcat window opens.

```text
☐ Sync finished   ☐ Emulator running   ☐ Run succeeded   ☐ Logcat visible
```

Move to a different seat **before the exam** if any of these fail on your PC. Leave the emulator running when the exam starts.

---

## Day 2 · 27–30 min — The Actual Exam Begins

[Day 2 actual exam](lab.md#2일차--본시험-60분) · [Walkthrough](walkthrough.md#2일차)

1. Put your phone away, and leave only the allowed-resources tab open in your browser.
2. Note the time when you receive the question sheet and the starter. 0–5 min is for opening and running it.
3. The last 5 minutes are for submission. Finish editing before then.

**Explanation total: 5+7+5+5+5+3 = 30 min**

---

## Next Week Preview

Every screen you've built so far has been an **Activity**.

In week 9, **Comparing App Components and Project 1 Presentations**, we put Service, BroadcastReceiver, and ContentProvider side by side with Activity and compare them.

Project 1's scoring criteria (normal flow, failure and retry, survives rotation, code walkthrough) are the same ones you practiced in this exam.
