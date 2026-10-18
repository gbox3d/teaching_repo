---
marp: true
theme: default
paginate: true
header: Mobile Programming · Week 8
footer: Midterm · Individual Hands-on Exam
---

# Midterm: Redo What You Did in Class, On Your Own

Practice with a problem bank made from what you **actually submitted** in Weeks 1–7, then take the exam with the same problems and new values.
No new syntax. You rebuild things in your own `StudentCard` project, **alone and within the time**.

```text
My Info
Name: Hong Gildong
3
[-1] [Reset] [+1]      ← 3 survives rotation
```

- No answer keys; every problem has **Checks** and a **Hint**.
- An answer is the edited code + emulator screenshots + a 1–2 sentence explanation.

---

# Day 1 — Practicing with the Problem Bank

`30 min talk → 60 min practice`

1. This week's two days and the range
2. The seven bank problems, how to read one
3. Checking — run, screenshot, Logcat
4. The 20-point rubric and today's order

---

## Day 1 · 0–5 min — This Week's Two Days and the Range

| Day | 30 min | 60 min |
|---|---|---|
| Day 1 | the bank, reading, checking, rubric | **practice** (no points) |
| Day 2 | rules (class notice), what goes in the answer, PC check | **midterm** (20 points) |

- The range is **up to the week we covered in class** within Weeks 1–7. The notice says how far.
- Exam problems are **the same problems with different values**: text, ids, numbers, key names change.
- What we did in class: Kotlin output, LinearLayout screens, `findViewById`, button counters, `count` that survives rotation.

---

## Day 1 · 5–12 min ① — The Seven Bank Problems

[Problem bank list](examples/README.md)

| Range | Problem | What we did in class |
|---|---|---|
| Week 1 | [a01](examples/a01_kotlin_card/README.md) student card | `val`·`$variable`·`if/else`·`fun` |
| Week 2 | [a02](examples/a02_info_screen/README.md) my info screen | vertical LinearLayout·TextView |
| Week 2 | [a03](examples/a03_name_button/README.md) change text, one button | `id`·`findViewById`·listener·`var` |
| Week 2 | [a04](examples/a04_counter_three/README.md) three-button counter | `+1`·`-1`·`Reset` |
| Week 3 | [a05](examples/a05_keep_rotation/README.md) count survives rotation | `onSaveInstanceState`·`?.`·`?:`·`Log.d` |
| Weeks 3–4 | [a06](examples/a06_input_toast/README.md) input field and Toast | `EditText`·`Toast` (if covered) |
| Weeks 5–6 | [a07](examples/a07_delay_message/README.md) text after 3 seconds | `postDelayed`·`isEnabled` (if covered) |

**Solve a bank problem and you have solved the exam problem once.**

---

## Day 1 · 5–12 min ② — Reading One Problem: a03_name_button

[a03 problem](examples/a03_name_button/README.md) — every problem has the same order

```text
Tasks          XML part (View·id·text) → Kotlin part (findViewById·listener·variable)
Checks         what you verify on screen and in Logcat; this replaces the answer key
Hint           read when stuck; the exam's explanation questions are this content
Values         what changes in the exam — nameText · Hong Gildong · countText · 0 · plusButton · +1 · 3
Explanation    what you answer in 1–2 sentences in the exam
```

- **Copy and paste** ids, text, and numbers from the problem. One wrong character means `Unresolved reference`.
- Check examples: at start `Name: Hong Gildong`·`0`, `+1` three times → `3`, no red lines in Logcat.

---

## Day 1 · 12–17 min — Checking: Run, Screenshot, Logcat

```text
Save (Ctrl+S) → Run ▶ → go through the checks on screen → screenshot the required state
Logcat tab → type the tag (Life) in the filter → only those lines show
Rotate → the rotate button on the emulator toolbar
```

- Screenshots: the camera button on the emulator toolbar, or Win+Shift+S / ⌘+Shift+4.
- The design preview (Split) is for layout only. Screenshots must show the **running app**.
- Read red lines from the first one. The [When stuck](lab.md#막혔을-때) table lists the common ones.

**Checks are results you see on screen and in Logcat. Same result, any code shape.**

---

## Day 1 · 17–22 min — The 20-Point Rubric: Behavior, Code, Explanation

| What | Share | How |
|---|---:|---|
| Behavior (checks) | about 60% | item by item, from screenshots and code |
| Code | about 20% | pasted XML·Kotlin matches the screenshots and contains the required parts |
| Explanation | about 20% | 1–2 sentences in your own words |

- Two problems: 10 points each. Four problems: 5 each. The notice says which.
- One cause is deducted once. Comment out a line that will not build, screenshot the running state, and paste the original code and error in the answer.
- Details: [rubric.md](rubric.md)

---

## Day 1 · 22–27 min — Today's Order

[Day 1 practice](lab.md#1일차--문제-은행으로-연습하기-60분) · [Walkthrough](walkthrough.md#1일차)

```text
0–5    open StudentCard and run · check the range in the bank list
5–13   a01 student card      13–23  a02 my info screen       23–33  a03 change text and a button
33–43  a04 three-button counter   43–53  a05 count survives rotation
53–60  note the checks you missed · classes that covered them go on to a06·a07
```

- Ten minutes per problem. When time is up, note what is left and move on. This rehearses "skip when stuck".
- a02 → a03 → a04 → a05 continue in the same project.

---

## Day 1 · 27–30 min — Start Practicing

1. Open `StudentCard`, start the emulator, and run.
2. Start with a01. For each problem: read → XML → Kotlin → run → checks → screenshot.
3. When stuck: hint → the "when stuck" table → raise your hand.

**Talk total: 5+7+5+5+5+3 = 30 min**

No points today. Where you get stuck today is where you would get stuck in the exam.

---

# Day 2 — Exam Instructions and the Actual Exam

`30 min instructions → exam (time in the notice)`

1. Where people got stuck in practice
2. Exam rules — the class notice decides
3. Reading order, what goes in the answer
4. PC check, all together

---

## Day 2 · 0–5 min — Where People Commonly Got Stuck

| Symptom | Cause |
|---|---|
| `Unresolved reference 'nameText'.` | differs from the name after `@+id/` in XML |
| `Unresolved reference 'name님'.` | Korean right after `$variable` — write `"${name}님"` |
| the number does not change on click | `countText.text = "$count"` is missing |
| rotation resets to `0` | `putInt`·`getInt` keys differ, or `count` lives inside `onCreate` |

Mistakes that still build only show up **when you run and tap**. That is why the checks exist.

---

## Day 2 · 5–12 min — Exam Rules: the Class Notice Decides

```text
Problems  2–4 bank problems with changed values     Time    30–60 min (start and end in the notice)
Range     up to the week covered in class            Submit  LMS answer box — code · screenshots · explanation
```

- What you may look at (course materials, your project, official docs) and whether AI tools are allowed follow the notice.
- Problems are independent. **If stuck for long, move on.**
- Even if unfinished, submit code, screenshots, and what you tried. Partial credit exists.
- Questions: wording, submission, failures only. Answers go to **everyone as one notice**.
- Details: [exam_structure.md](exam_structure.md)

---

## Day 2 · 12–17 min — Reading Order: Where the Values Differ

```text
bank a03      nameText · Hong Gildong · countText 0 · plusButton +1 · three taps → 3
exam problem  nameText · Kim Minji    · countText 10 · plusButton +2 · three taps → 16   ← only values differ
```

1. Read only for the first 3 minutes. Mark the values that differ from the bank problem.
2. XML → Kotlin → save and run → checks → screenshot. The same order as Day 1.
3. If a check fails, go back to the task it points to.

**Copy and paste values. One wrong character in an id is a red line.**

---

## Day 2 · 17–22 min — What Goes in the Answer: Code, Screenshots, Explanation

```text
① Code          select all in activity_main.xml · MainActivity.kt → copy → paste into the answer box
② Screenshots   the emulator in the required state (plus rotation or Logcat when asked)
③ Explanation   1–2 sentences in your own words for the explanation question (hint-level content)
```

- Example: "On rotation the Activity is destroyed and created again, so `count = 0` runs again."
- Comment out a line that will not build, screenshot the running state, and paste the original code and error.
- After the last change, **save → Run ▶ → go through the checks** once more.

**Behavior, code, and explanation for every problem.**

---

## Day 2 · 22–27 min — PC Check: Project Run and Emulator

1. Open the `StudentCard` project.
2. When the progress bar (Sync) finishes, press Run ▶.
3. Confirm the screen appears on the emulator and the Logcat window opens. Open the LMS answer box too.

```text
☐ Sync done   ☐ emulator on   ☐ Run succeeded   ☐ Logcat visible   ☐ LMS answer box open
```

A PC that fails here moves seats **before the exam**. Leave the emulator running when you start.

---

## Day 2 · 27–30 min — The Exam Begins

[Day 2 exam](lab.md#2일차--중간고사-60분-가운데-공지한-시간) · [Walkthrough](walkthrough.md#2일차)

1. Arrange your browser tabs as the notice says.
2. When the problems appear, note the time. The first 3 minutes are for reading and marking values.
3. The last 5 minutes are for tidying and submitting. Stop editing before then.

**Talk total: 5+7+5+5+5+3 = 30 min**

---

## Next Week Preview

Every screen so far has been an **Activity**.

In Week 9, **App Components and the Project 1 Presentation**, we compare Service, BroadcastReceiver, and ContentProvider side by side with Activity.

The grading axes of Project 1 (normal flow, surviving rotation, explaining the code) are what you practiced in this exam.
