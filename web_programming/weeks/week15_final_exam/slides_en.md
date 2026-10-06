---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 15"
footer: "Final Exam · Weeks 1–14 Problem Bank · Same Problems, New Values"
---

# Final Hands-on Exam

Nothing new this week. Practice with a **problem bank** made from the Week 1–14 lab submissions, then take the exam.

- Day 1: pick problems from the bank and solve them. Instead of answers, each has **What to check**.
- Day 2: the 60-minute final exam. One problem per area A–E, **with only the values changed**.
- Problems don't depend on each other. Each uses only what its own week taught.
- This week's one repository is `web-week15`. Create it at the end of Day 1; the exam goes in it too.

[Problem bank list](examples/README.md) · 13 problems · 8–12 min suggested each

---

# Day 1 — Practicing with the Problem Bank

`30 min explanation & demo → 60 min practice`

1. Bank and exam — same problems, only the values change
2. How to read one problem — with w12_fetch_cards
3. How to check — open it from the server, look in F12
4. Today's order and this week's repository, `web-week15`

---

## Day 1 · 0–8 min — Bank and Exam: Same Problems, New Values

| Area | Points | [Bank problems](examples/README.md) (no. = week) |
|---|---:|---|
| A Page (HTML · CSS · README) | 3 | w01 · w02 · w03 · w04 · w09 · w14 |
| B DOM | 3 | w05 · w06 · w13 |
| C Forms · lists | 4 | w07 · w10 |
| D Storage (localStorage) | 2 | w11 |
| E Loading (fetch) | 3 | w12 |

- One problem per area, **only the values change** (w01–w07: new values, unlike Week 8).
- No answers are published. **확인할 것** (What to check) tells you.

**Don't memorize values. Learn the tasks and how to check them.**

---

## Day 1 · 8–16 min — How to Read One Problem: w12_fetch_cards

[examples/w12_fetch_cards/](examples/w12_fetch_cards/README.md) · from the Week 12 lab submission · E Loading (fetch) · 9 min

```text
Starting files  app.js: only loadCards() is empty. Don't edit the rest
Tasks           ① fetch ② not OK → notice ③ JSON → showCards ④ try / catch
What to check   3 cards · Network 200 · no red line · no file → notice text
Values          data/html-docs.json · doc-list · …   ← the exam changes these
```

- Find what to edit in Starting files, do Tasks in order, check items top to bottom.
- Copy values from the "이 문제의 값" (Values) table. The exam changes only these.

**Every problem: same parts, same order. Only the values change.**

---

## Day 1 · 16–24 min — How to Check: Server and F12

Put [server.mjs](../../tools/static-server/server.mjs) at the top of `web-week15` and run `node server.mjs`

```text
http://localhost:8000/w12_fetch_cards/    ← one such address per problem
Console      no red line (Uncaught), and the printed text
Network      every file request is 200, no 404
Elements     text · class · href, colors and spacing in Computed
Application  the key and the saved value in Local Storage
Device mode  Ctrl+Shift+M → width 375, no horizontal overflow
```

- `fetch` problems (w12) are blocked on `file://`. Check on the server or the public address.
- README problems (w09 · w14): use **Open Preview**, then check on GitHub after pushing.

**Judge by the text on screen and the values in F12, not by eye.**

---

## Day 1 · 24–30 min — Today's Order and web-week15

[Day 1 lab](lab.md#1일차--문제-은행으로-연습하기-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

1. 0–5 min: three problems from different areas, weakest first, one or more from Weeks 9–14.
2. 5–50 min: 15 min each. Download → open from the server → Tasks → What to check.
3. 50–60 min: create `web-week15`, push in the Week 2 order, and turn on Pages.

```text
web-week15/
  server.mjs
  w12_fetch_cards/      ← folder name = the problem id, exactly
  w05_greeting_card/    ← public address …/web-week15/w05_greeting_card/
```

**Explanation total: 8+8+8+6 = 30 min**

---

# Day 2 — The Final Exam

`30 min briefing → 60 min exam`

1. Exam rules and the timetable
2. The `exam` folder — receive, put at the top, open the index, first push
3. Areas, points, grading — implementation 15 + demo 5 (URL reproduction 3 · oral 2)
4. Before you finish — the last push and the three submissions

Open yesterday's `web-week15` folder in VS Code. If the PC doesn't have it: `git clone https://github.com/student01/web-week15.git`, then **File › Open Folder**.

---

## Day 2 · 0–8 min — Exam Rules and Timetable

| Time | Task |
|---|---|
| 0–3 min | Put in `exam` → first push → skim `exam/README.md` |
| 3–51 min | Problems A–E. Stuck for over 5 minutes? Move on |
| 51–56 min | Last push → check the public address → Commits tab capture |
| 56–60 min | Buffer |

- Allowed: this course site, your repositories, MDN. Otherwise: the instructor's notice.
- Scope: the Week 1–14 lab submissions. Extra features earn no extra points.
- Questions: only about a problem's meaning, file locations, submitting, or outages.

**Problems don't depend on each other. If you're stuck, move on.**

---

## Day 2 · 8–16 min — The exam Folder: Put In, Open, Push

```text
web-week15/
  exam/              ← handed out at the start; same name, at the top
    README.md        ← the full text of all five problems
    index.html       ← the index: one link per problem
    a/ b/ c/ d/ e/   ← problem folders; starting files only
  w12_fetch_cards/   ← leave your Day 1 practice folders as they are
```

1. `node server.mjs` → open the index at `http://localhost:8000/exam/`.
2. Push right away: `git add .` → `git commit -m "기말 실기 시작"` → `git push`
3. After 1–3 min, the index shows at `https://student01.github.io/web-week15/exam/`.

**For each problem, edit only the files in its own folder (`exam/a/` …).**

---

## Day 2 · 16–24 min ① — Implementation 15: By "What to Check"

[Rubric](rubric.md) · 20 points (draft) = implementation 15 (A 3 · B 3 · C 4 · D 2 · E 3) + demo 5

```text
Fully met       every What to check item is right
Partially met   a partial result runs — some items are right
Not met         doesn't open · unrelated to the problem · missing
```

- One cause behind several failed items is deducted once, never beyond the area's points.
- Whether "any visible attempt earns at least 5 points" applies is not decided yet.

**If What to check is right, it's right, even if you wrote it differently.**

---

## Day 2 · 16–24 min ② — Demo 5: URL Reproduction 3 · Oral 2

```text
URL reproduction 3   the grader opens …/web-week15/exam/ in a new private window
                     → do all five problems work as required from the index?
Oral 2               last 30 min of the exam, 1 minute at your seat
                     → say what one line of your code, picked for you, does
                     → that minute is added back to your deadline
```

- Grading is done at the public address. What only works on your PC isn't submitted.
- A slow Pages update costs no points. The grader opens it again the next day.

**The oral check isn't a memorized answer. It's reading one line of your own code.**

---

## Day 2 · 24–30 min — Before You Finish: Last Push, Three Items

[Day 2 lab](lab.md#2일차--기말-실기-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

```text
51 min  git add .  →  git commit -m "기말 실기 끝"  →  git push
        refresh …/web-week15/exam/ → open each problem from the index
        GitHub repository › Commits tab capture — top commit's hash and time
```

- Your submission is the **last commit** before the deadline, opened at the public address.
- Push as often as you like, but never after the deadline.
- On a shared PC, remove your saved credentials before leaving.

**Explanation total: 8+8+8+6 = 30 min**

---

## What to Submit

When the Day 2 exam ends, submit **three things**.

```text
① Public address      https://student01.github.io/web-week15/exam/
② Repository address  https://github.com/student01/web-week15
③ One capture         Commits tab — top commit's hash, time, and the address bar
```

If Pages is slow, a local screenshot plus the Commits tab capture is accepted. No deduction.
Day 1 practice folders are for checking only and are not submitted.
Keep your real name, student ID, and real email out of captures. Where and by when to submit follow the class notice; the commit deadline is the end of the exam.

---

## Next — Wrapping Up the Semester

Week 15 is the last class. There are no more classes after this.

```text
Weeks 1–4    file links · public address · semantic HTML, forms · responsive CSS
Weeks 5–7    values and functions · clicks and classes · reading form input
Weeks 9–14   README · lists · localStorage · fetch · text as text · presentation
```

- Keep `web-week15` until grades are out, and don't push to it after the deadline.
- How scores are released and reviewed follows the class notice.
- Redo bank problems you skipped with values you change yourself. What to check is the standard.
