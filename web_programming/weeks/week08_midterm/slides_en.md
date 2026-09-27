---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 8"
footer: "Midterm Hands-on Exam · Rehearsal and the Actual Exam"
---

# Midterm Hands-on Exam

Build what you learned in Weeks 2–7 **alone, in 60 minutes**, and put it up at a public URL.

```text
Day 1  60 min rehearsal + create repository, turn on Pages   ← finish prep today
Day 2  60 min actual exam (my-web/exam/)                     ← only building
```

The weight is **20 points**. Not the weekly lab scores.

---

# Day 1 — Exam Briefing and Rehearsal

`30 min explanation → 60 min rehearsal`

1. Exam scope and rubric
2. Submission format and the 60-minute budget
3. The actual exam happens in `my-web/exam/`
4. Allowed resources and what to do if something breaks

---

## Day 1 · 0–8 min — Exam Scope and Rubric

The scope is **Weeks 2–7**: Pages, HTML, CSS, DOM, forms.

| Area | Points |
|---|---:|
| Pages deployment, 2+ commits | 3 |
| HTML structure (skeleton, list, table, form) | 4 |
| CSS (selectors, the box model, flex, `@media`) | 4 |
| DOM events (click → `textContent`, `classList`) | 5 |
| Form input, empty-value message | 3 |
| No Console errors | 1 |

Out of scope: array-based lists (Week 10), `localStorage` (Week 11), `fetch` (Week 12), modules.

---

## Day 1 · 8–16 min — Submission Format and the 60-Minute Budget

```text
① Public URL       https://student01.github.io/my-web/exam/
② Repository URL   https://github.com/student01/my-web
③ Last commit SHA  git log -1 --oneline
④ One screenshot of the finished screen (with the address bar)
```

| Exam, 60 min | What you do |
|---|---|
| 0–5 · 5–15 · 15–25 | Read the questions · HTML · CSS |
| 25–50 · 50–55 · 55–60 | DOM & forms · push · **buffer** |

The 5-minute buffer absorbs Pages propagation (1–3 min) and logging back in.

---

## Day 1 · 16–24 min — The Actual Exam Happens in my-web/exam/

```bash
cd my-web
mkdir exam
```

- You do not create a new repository. `my-web` **already has a working repository, login, and Pages**.
- During the exam, you never create a repository, log into the browser, or turn on Pages.
- The public URL simply gets the folder name appended: `https://<your-id>.github.io/my-web/exam/`.
- You do the repository setup and turn on Pages once more **today, during the rehearsal**.

```text
my-web/  index.html  about.html  guestbook.html  styles.css  …
         exam/  index.html  styles.css  app.js     ← exam answer
```

---

## Day 1 · 24–30 min — Allowed Resources, What to Do If Something Breaks, and the Lab Handoff

[Day 1 lab](lab.md#1일차--리허설과-저장소-준비-60분) · [Walkthrough](walkthrough.md#1일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

- Allowed: the course site, your own `my-web` repository, MDN. Anything else follows the instructor's announcement.
- If Pages is slow, a local screenshot plus the commit SHA is accepted instead.
- Today's work: solve the 4 rehearsal questions → check them against the answers → new repository `midterm-practice` → Pages.

**Explanation total: 8+8+8+6 = 30 min**

---

# Day 2 — The Actual Exam

`30 min briefing → 60 min exam`

1. The procedure, and what "your submission" means
2. If something breaks
3. Copy the starter into `exam/` and confirm it runs
4. Questions → the exam begins

---

## Day 2 · 0–8 min — The Procedure and What "Your Submission" Means

```text
Save → push → reload the public URL → what you see = your submission
```

- A screen that only shows up in your editor is not your submission. **A file you haven't saved is not committed.**
- Changes you haven't committed aren't pushed, and commits you haven't pushed aren't at the public URL.
- There is one working folder: `my-web/exam/`. Files in any other folder are not graded.
- Seating, moving around, and how to ask questions are explained before the exam starts.

---

## Day 2 · 8–16 min — If Something Breaks

| What happened | What to do |
|---|---|
| Pages still shows the old screen after 5+ minutes | Submit a local screenshot + `git log -1 --oneline` |
| `Permission ... denied to <another id>` | Remove `git:https://github.com` from Credential Manager, then push again |
| `! [rejected] main -> main (fetch first)` | `git pull`, then `git push` again |
| Push itself fails | Raise your hand. Note the time and submit the folder as a zip |

Don't wrestle with it alone for more than 10 minutes. Raising your hand only gets you help with **environment issues**.

---

## Day 2 · 16–24 min — Copy the Starter into exam/ and Confirm It Runs

```bash
cd my-web
git pull
mkdir exam
```

1. Put the three deployed starter files into `exam/`.
2. Double-click `exam/index.html` in File Explorer — it opens as `file://`.
3. Check that there are no red lines in the F12 **Console**.
4. Make your **first commit**: `git add .` → `git commit -m "Start midterm exam"` → `git push`.
5. Once this all works, the exam begins.

- If it doesn't open now, the problem isn't the question sheet — it's the **file location**. All three files need to sit side by side inside `exam/`.

---

## Day 2 · 24–30 min — Questions and the Exam Begins

[Day 2 lab](lab.md#2일차--중간-실기-60분) · [Walkthrough](walkthrough.md#2일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

- Questions we'll answer: what a question means, where a file goes, how to submit, technical problems.
- Questions we won't answer: how to build something, whether this code is correct.
- If you get stuck on one question, **move on to the next.** The questions don't depend on each other.

**Explanation total: 8+8+8+6 = 30 min**

---

## What to Submit

When the exam ends, submit four things.

```text
① https://student01.github.io/my-web/exam/
② https://github.com/student01/my-web
③ 1ea3c2e            ← git log -1 --oneline
④ 1 screenshot (finished screen + address bar)
```

Make sure your real name, student ID, and real email address are not visible in the screenshot. Your ID may be visible.

---

## Next Week Preview

Week 9 is your **Project 1 presentation**.

You demo, for 2 minutes, not today's `exam/` folder but the **main `my-web` site** you built in Weeks 3–7.
Open the public URL → move through the three pages → button and form → the GitHub **Commits** tab.
Your report is a single page: the repository's `README.md`.
