---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 8"
footer: "Midterm hands-on exam · practice with the problem bank, then the same problems with new values"
---

# Midterm Hands-on Exam

Practice with a **problem bank** built from what you **actually submitted** in Weeks 1–7, then take the exam on Day 2 with the same problems and new values.

```text
Day 1  Practice with the bank, 60 min — the problems for the weeks we covered
Day 2  Midterm exam — bank problems with changed values (time and count: class notice)
```

- Exam problems have the **same text, tasks, and checks** as the bank problems; only the values differ.
- No answer keys. Every problem has **Checks** and a **Hint**.
- The level is the lab work you did in class. Worth **20 points**, separate from weekly lab points.

---

# Day 1 — Practicing with the Problem Bank

`30 min talk and demo → 60 min practice`

1. This week: the bank and the exam — same problems, new values
2. Reading one problem — w04_box_style
3. Checking — open the page, F12 Console·Network·Elements
4. Today's order

---

## Day 1 · 0–8 min — Bank and Exam: Same Problems, New Values

[Problem bank list](examples/README.md) — one problem per Weeks 1–7 submission, seven problems

| Section | Bank problems |
|---|---|
| A HTML | [w01](examples/w01_first_page/README.md) first page · [w02](examples/w02_push_repo/README.md) edit and push · [w03](examples/w03_second_page/README.md) new page and link |
| B CSS | [w04](examples/w04_box_style/README.md) styled box, centered text · [w05](examples/w05_box_position/README.md) box position in a frame |
| C JavaScript·DOM | [w06](examples/w06_click_text/README.md) button changes text and count |
| D Forms | [w07](examples/w07_form_line/README.md) read inputs into one line |

- The range is **up to the week we covered in class**. The notice says how far.
- The exam uses these bank problems with **changed values only**. Text, tasks, and checks stay the same.

**Solve a bank problem and you have solved the exam problem once.**

---

## Day 1 · 8–16 min — Reading One Problem: w04_box_style

[w04_box_style problem](examples/w04_box_style/README.md) — six sections, every problem in the same order

```text
Starter files   what you download and its current state; "do not change" files stay as they are
Tasks           which file and where, what to write; do them in order
Checks          what you verify yourself on screen and in F12; this replaces the answer key
Hint            read it when stuck; the exam's explanation questions are this content
Values          what changes in the exam. w04: 300 · black · lightgreen · 4px solid gold …
Get and push    download with Raw into web-week08/w04_box_style/
```

- Check examples: background `black`, text `lightgreen`, border `4px solid gold`, three lines centered both ways.
- **Copy and paste** values from the table. One different character and a check fails.

**Text, tasks, and checks are the same in the exam. Only the Values table changes.**

---

## Day 1 · 16–24 min — Checking: Open the Page and F12

Double-click to open (`file://`), or [server.mjs](../../tools/static-server/server.mjs) → `node server.mjs` → `http://localhost:8000/<problem id>/`

```text
Console      red lines (Uncaught) · console.log · try document.querySelectorAll('li').length
Network      Status 200 / 404 per file — visible only on a server or the public URL
Elements     tags, ids, href, Styles values, the box diagram (padding·border·content size)
```

- Every check says where to look. Open that place and match every character.
- Box problems (w04·w05): the Elements box diagram and the position on screen. Button and form problems (w06·w07): click and read the Console.
- PCs without Node open the file by double-click. Only the Status numbers are missing then.

**Checks are results you see on screen and in F12. Same result, any code shape.**

---

## Day 1 · 24–30 min — Today's Order

[Day 1 lab](lab.md#1일차--문제-은행으로-연습하기-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

```text
0–5    folder web-week08 · server.mjs · check the range in the bank list
5–15   w01 first page        15–25  w04 styled box        25–35  w05 box position
35–45  w03 new page and link   45–55  w02 edit and push (repository and push check)
55–60  note the checks you missed · classes that learned JavaScript go on to w06·w07
```

- Download problem folders into `web-week08/<problem id>/` with **Raw**. Do not download `README.md`.
- Ten minutes per problem. When time is up, note what is left and move on. This rehearses "skip when stuck".

**No points today. The goal is to know where you got stuck.**

**Talk total: 8+8+8+6 = 30 min**

---

# Day 2 — Midterm Exam

`30 min talk and demo → exam (time in the notice)`

1. Exam rules — the class notice decides
2. Reading order — mark where the values differ
3. What goes in the answer — code, screenshots, explanation
4. Submission and before you finish

---

## Day 2 · 0–8 min — Exam Rules: the Class Notice Decides

```text
Problems  2–4 bank problems with changed values     Time    30–60 min (start and end in the notice)
Range     up to the week covered in class            Submit  LMS answer box or repository web-week08/exam/
```

- What you may look at (course site, your files, MDN) and whether AI tools are allowed follow the notice.
- Problems are independent. **If you are stuck for long, move to the next problem.**
- Even if unfinished, submit the code, screenshots, and what you tried (error messages). Partial credit exists.
- Questions: only wording, file location, submission, and failures. We do not say whether code is right.

**The rules fit on one notice. Read it again before you start.**

---

## Day 2 · 8–16 min — Reading Order: Where the Values Differ

```text
bank w04      box 300×300 · black · lightgreen · 4px solid gold · padding 8
exam problem  box 320×200 · navy  · yellow     · 3px dashed white · padding 12   ← only values differ
```

1. Read the whole problem and mark the values that differ from the bank problem.
2. If there are starter files, download them into the problem folder as on Day 1.
3. Do the tasks one chunk at a time → save → reload → Console.
4. Match the checks one by one. If one fails, go back to the task it points to.

**Finish reading within 3 minutes, and copy-paste the values.**

---

## Day 2 · 16–24 min — What Goes in the Answer: Code, Screenshots, Explanation

[Rubric](rubric.md) — results (checks) about 60% · evidence (screenshots) about 20% · explanation about 20%

```text
① Code          the whole edited file, or code where the change is clear
② Screenshots   the browser in the required state — address bar visible; F12 items with that panel
③ Explanation   1–2 sentences in your own words answering what the problem asks (hint-level content)
```

- Grading uses the checks: full · partial (as much as matched) · none.
- One cause is deducted once. Attempts and explanations earn points even without a running result.
- Example explanation: "In row direction, `justify-content` handles horizontal and `align-items` vertical."

**We grade results, screenshots, and explanations, not code shape.**

---

## Day 2 · 24–30 min — Submission and Before You Finish

[Day 2 lab](lab.md#2일차--중간-실기-공지한-시간) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm)

```text
5 min before the end   check that every problem has code → screenshots → explanation
LMS method             paste in that order into the answer box and submit
Repository method      git add . → git commit -m "midterm end" → git push → public URL · repo URL · Commits tab screenshot
```

- Unsaved files are not pushed. Keep real names, student IDs, and real emails out of screenshots.
- If Pages is slow, submit local screenshots. No deduction.
- On a shared PC, delete the credentials before leaving.

**Talk total: 8+8+8+6 = 30 min**

---

## What to Submit

After the Day 2 exam, submit where the class notice says. [Submission](lab.md#제출)

```text
LMS answer box    code · screenshots · explanation for each problem
Repository        ① public URL https://student01.github.io/web-week08/exam/
                  ② repository URL https://github.com/student01/web-week08
                  ③ one Commits tab screenshot — top commit's hash and time visible
```

Day 1 practice folders are not submitted and are not graded.
Keep real names, student IDs, and real emails out of screenshots. The deadline is the time in the notice.

---

## Next Week Preview

Week 9 is the **Project 1 presentation**.

Not this week's problem folders, but **your own site** built week by week in Weeks 3–7, shown at its public URL for two minutes.
Page navigation → styled boxes → buttons and the form (for classes that learned them) → the GitHub **Commits** tab.
The report is the first `README.md` on the repository front page: public URL, pages, features, screenshots, and what you learned.
