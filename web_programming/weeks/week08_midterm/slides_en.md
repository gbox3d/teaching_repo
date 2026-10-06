---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 8"
footer: "Midterm Hands-on Exam · practice with the problem bank, then the same problems with changed values"
---

# Midterm Hands-on Exam

Practice with a **problem bank** built from the Weeks 1–7 lab submissions, then take the exam alone in 60 minutes on Day 2.

```text
Day 1  60 min problem-bank practice + new repository web-week08 · Pages
Day 2  60 min midterm — bank problems with the values changed
```

- Exam problems keep the **statement, tasks, and checks**. Only the values differ.
- Answers aren't published. Pass every **"확인할 것" (What to check)** item and you're done.
- The weight is **20 points (draft)**. Not the weekly lab scores.

---

# Day 1 — Practicing with the Problem Bank

`30 min explanation & demo → 60 min lab`

1. The bank and the exam — only the values change
2. Reading one problem — w05_greeting_card
3. Checking — the server; F12 Console · Network · Elements; device mode
4. Today's plan, the new repository web-week08 · Pages

---

## Day 1 · 0–8 min — Bank and Exam: Same Problems, New Values

[Problem bank list](examples/README.md) — seven problems from the Weeks 1–7 labs

| Area | Bank problems |
|---|---|
| A HTML, 4 pts | [w01](examples/w01_link_fix/README.md) file links · [w02](examples/w02_about_page/README.md) new page · [w03](examples/w03_guestbook_form/README.md) sign-up form |
| B CSS, 4 pts | [w04](examples/w04_responsive_css/README.md) responsive menu and cards |
| C JavaScript·DOM, 5 pts | [w05](examples/w05_greeting_card/README.md) greeting card · [w06](examples/w06_dark_mode/README.md) dark mode |
| D Forms, 3 pts | [w07](examples/w07_form_result/README.md) form result in one line |

- Each area gets one bank problem with **changed values** only.
- No published answers: pass every "확인할 것" (What to check) item.

**Solve the bank problems and you've solved the exam problems once.**

---

## Day 1 · 8–16 min — Reading One Problem: w05

[w05_greeting_card statement](examples/w05_greeting_card/README.md) — five sections, same order in every problem

```text
시작 파일      Starter: what you get; "do not edit" files stay as is
할 일          Tasks: which file, where, what — in the listed order
확인할 것      Checks: screen and F12 results, instead of answers
이 문제의 값   Values: what the exam changes — w05: guest07 · 15 · welcome
받기와 올리기  Get it: Raw into web-week08/w05_greeting_card/
```

- Checks, e.g.: the card shows `반가워요, guest07님. 즐거운 오후예요.`; the Console prints `15` and the same line.
- **Copy and paste** values from the table. One wrong character fails a check.

**The exam keeps everything except the Values table.**

---

## Day 1 · 16–24 min — Checking: Server and F12

[server.mjs](../../tools/static-server/server.mjs) at the top of `web-week08` → `node server.mjs` → `http://localhost:8000/<problem id>/`

```text
Console      red lines (Uncaught) · console.log · try hello(12)
Network      Status 200 / 404 per file (server or public URL only)
Elements     tags · class · href; Styles · Computed · box diagram
Device mode  Ctrl+Shift+M — problem's widths (w04: 1280 · 500 · 480 · 375)
Application  saved values — Week 11; not in the Week 8 bank
```

- Each "확인할 것" item says where to look. Match it character by character.
- No Node? Double-click to open. Status numbers won't show then.

**Checks are results on screen and in F12. Any code that gets them is correct.**

---

## Day 1 · 24–30 min — Plan, web-week08, Pages

[Day 1 lab](lab.md#1일차--문제-은행으로-연습하기-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

```text
0–5    from the bank list, one problem per area — weakest first
5–20   problem 1: get it → open via server → tasks → match the checks
20–35  problem 2      35–50  problem 3
50–60  new repo web-week08 → push → Pages → re-check at the public URL
```

- Save each problem folder via **Raw** into `web-week08/<problem id>/`. Skip `README.md`.
- Push in the Week 2 order. On a shared PC, delete your credentials.

**Set up the repository and Pages today, not on Day 2.**

**Explanation total: 8+8+8+6 = 30 min**

---

# Day 2 — Midterm Exam

`30 min explanation & demo → 60 min exam`

1. Exam rules — resources, scope, moving on, the 60-minute schedule
2. exam folder → top of the repository → open the index → first push
3. Points and grading — by "확인할 것" (What to check)
4. Before you finish — last push and the three submissions

---

## Day 2 · 0–8 min — Exam Rules and Schedule

```text
0–5 read · 5–15 A · 15–27 B · 27–39 C · 39–50 D
50–55 last push · 55–60 buffer (Pages delay · logging in again)
```

- Allowed: the course site, your own repository, MDN. Anything else: per the instructor.
- Scope: the Weeks 1–7 bank problems. Out-of-scope features earn nothing extra.
- Problems are independent. **Stuck for more than 5 minutes? Move on.**
- We answer only about wording, file locations, submitting, and technical trouble — not about your code.

**One schedule row = one problem. Skip when stuck; come back later.**

---

## Day 2 · 8–16 min — The exam Folder, First Push

```text
web-week08/
  server.mjs   w05_greeting_card/ …   ← Day 1 practice folders. Leave them
  exam/                                ← the folder you receive, as is
    index.html   README.md   a/  b/  c/  d/
```

1. Put the `exam` folder **as is** at the top of `web-week08`. Got `exam/exam/`? Use the inner one.
2. Open `http://localhost:8000/exam/` — the index should appear.
3. Push right away: `git add .` → `git commit -m "중간 실기 시작"` → `git push`
4. Statements: `exam/README.md`. Edit only each problem's own folder.

**Push once at the start. In the exam, no new repo, no Pages setup.**

---

## Day 2 · 16–24 min — Grading by the Checks

[Rubric](rubric.md)

```text
Submission & public URL 3   A HTML 4   B CSS 4   C JavaScript·DOM 5
D Forms 3   No Console errors 1                   Total 20 pts (draft)
Submission 3 = three items · index and pages open · start + end push
```

- Graded at your public URL, item by item of **"확인할 것"**.
- Fully met (all) · partly met (working partial result) · not met (won't open · unrelated · none).
- One cause, one deduction. Console point: only `Uncaught` red lines.
- No deduction for Pages delays. The 5-point floor (5 if you tried) is undecided.

**Grading checks the results, not how the code looks.**

---

## Day 2 · 24–30 min — Last Push and Submission

[Day 2 lab](lab.md#2일차--중간-실기-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

```text
min 50  git add .  →  git commit -m "중간 실기 끝"  →  git push
        reload the public URL …/web-week08/exam/ → check each problem
        capture GitHub › Commits tab — the top commit's ID and time
```

- Submission = the last commit before the deadline, at the public URL. Unsaved files aren't pushed.
- Pages still old after 5 minutes? Send a local screenshot + a Commits tab capture.
- On a shared PC, delete your credentials before leaving.

**Explanation total: 8+8+8+6 = 30 min**

---

## What to Submit

Submit **three** things when the Day 2 exam ends. [Submission — three items](lab.md#제출--세-가지)

```text
① Public URL       https://student01.github.io/web-week08/exam/
② Repository URL   https://github.com/student01/web-week08
③ 1 Commits tab capture — top commit's ID and time visible
```

The top commit is your last push, `중간 실기 끝` (midterm end).
Only `exam/` is graded. Leave the Day 1 practice folders as they are.
Keep your real name, student ID, and real email out of the capture. Where and by when to submit follow the class notice; the commit deadline is the end of the exam.

---

## Next Week Preview

Week 9 is the **Project 1 presentation**.

Not the problem folders: open **your own site** from Weeks 3–7 at its public URL and show it in 2 minutes.
Three pages → a button → the form (with the empty-value message) → the GitHub **Commits** tab.
The report is a first-draft `README.md` on your repository's front page: your site's structure — URL, pages, features, screenshots, what you learned.
