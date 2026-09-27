---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 15"
footer: "Final Individual Exam · Implementation 15 + Demo 5"
---

# Final Individual Exam

You won't touch the site you presented in Week 14 anymore.
This week is a solo exam: rebuild the Weeks 2–13 features on a **starter you've never seen**.

```text
web-final/
  index.html       ← skeleton, form, list spots
  styles.css       ← colors, flex, @media
  app.js           ← TODO 1–4
  data/items.json  ← recommendation list data
```

Day 1 is a **rehearsal** with the same shape; Day 2 is the **60-minute real exam**.

---

# Day 1 — Exam Briefing and Rehearsal

`30 min briefing → 60 min rehearsal`

1. Exam scope and the public starter
2. The 20-point rubric
3. Three things to submit, and what to finish today
4. Allowed materials and fallback plans

---

## Day 1 · 0–8 min ① — Exam Scope Is Weeks 2–13

| Week | What's tested |
|---|---|
| 2 | Repository push and Pages publishing |
| 3 | Skeleton, list, table, form |
| 4 | Colors, boxes, `flex`, `@media` |
| 6 | Click → `textContent` · `classList` |
| 7 · 10 | Reading form values, empty-value notice, list add/delete |
| 11 | Saving and restoring with `localStorage` |
| 12 | Loading JSON with `fetch` and error notices |

Nothing from the Week 14 presentation or new syntax appears on the exam.

---

## Day 1 · 0–8 min ② — The Public Starter's Four Files

```text
web-final/
  index.html        already has spots for h1 · form · ul
  styles.css         a body.dark rule and one @media block
  app.js             TODO 1–4 (only [Dark Mode] works right now)
  data/items.json    3 recommendations
```

- Same structure as the [rehearsal_starter](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam/examples/rehearsal_starter) released in Week 13.
- The Console has **zero** errors. Features are missing, but nothing is broken.
- The storage key is `final-items`. It's a different name from `my-web`'s `guestbook`, so the two don't mix.

---

## Day 1 · 8–16 min — The 20-Point Rubric

| Item | Points |
|---|---:|
| HTML/CSS | 3 |
| DOM events | 3 |
| Form, list add/delete | 4 |
| localStorage | 2 |
| fetch and error notice | 3 |
| URL reproduction (the grader opens your public address) | 3 |
| Spoken question (1 minute, at your seat) | 2 |

Full text is in the [rubric](rubric.md). The point values are a **draft**, pending approval.

---

## Day 1 · 16–24 min ① — Three Things to Submit

```text
1. https://student01.github.io/web-final/   ← public address
2. https://github.com/student01/web-final   ← repository address
3. dd80e4c…(40 characters)                   ← last commit hash
```

```bash
git log -1 --format=%H
```

- Your submission is **whatever is saved, pushed, and shown at the public address**.
- Submit them together with one screenshot (with the address bar visible).

---

## Day 1 · 16–24 min ② — Finish These Today

1. Create the `web-final` repository on GitHub (**Public**, with the README checkbox off).
2. `git clone` → add the starter's four files → `git push -u origin main`.
3. **Settings › Pages** → `main` · `/(root)` → **Save** → open the public address.

- You won't create a repository or turn on Pages on exam day. Finish that today.
- Also resolve any shared-PC login issues today (Credential Manager).
- The public address is your source of truth. Local preview (Live Server, `python3 -m http.server 8000`) is optional.

---

## Day 1 · 24–30 min ① — Allowed Materials and Fallback Plans

| Category | Details |
|---|---|
| Allowed | This course site · your own repository (`my-web`) · MDN. Search/AI tool scope is announced in class |
| Not allowed | Other students' code, messaging apps, someone else's repository as an answer key |
| Pages delay | If nothing shows after 5 minutes, a local screenshot plus your commit hash is accepted |
| Credential conflict | Remove `git:https://github.com` and log in again; if still blocked, submit a zip archive |
| Network outage | For that session only, the `fetch` question is graded against a hardcoded array in `app.js` instead |

Don't try to resolve a problem alone — raise your hand and have the time logged.

---

## Day 1 · 24–30 min ② — Try It Yourself

[Day 1 lab](lab.md#1일차--리허설과-시험용-저장소-준비-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

1. Create the `web-final` repository, push the starter's four files, and turn on Pages.
2. Fill in TODO 1–4 in order. If stuck, look only at that part of the [solution](examples/rehearsal_solution/app.js).
3. In the last 5 minutes, push and refresh the public address to confirm it.

**Explanation total: 8+8+8+6 = 30 min**

Today's rehearsal isn't graded. It's practice for tomorrow.

---

# Day 2 — The 60-Minute Exam

`30 min briefing → 60 min exam`

1. Today's procedure and what "submitted" means
2. One spoken question
3. Confirming the starter runs
4. How to spend the 60 minutes

---

## Day 2 · 0–8 min ① — Today's Procedure

1. The proctor hands out four exam files. **Overwrite** them into your `web-final` folder.
2. The questions have the same shape as yesterday's rehearsal — only the values and screen topic differ.
3. You implement for 60 minutes and push in the last 5.
4. Late in the exam, the proctor comes to your seat and asks one short question (1-minute spoken check).

- Yesterday's rehearsal commits stay in your history. Overwriting doesn't erase them.
- Questions are answered only for wording and environment issues — not for how to implement something.

---

## Day 2 · 0–8 min ② — What's Saved and Refreshed Is What's Submitted

```text
Save in VS Code → git add . → git commit → git push
                                   │ 1–3 min
                                   ▼
        https://student01.github.io/web-final/   ← what the grader opens
```

- Saving alone changes neither GitHub nor your public address (same as Week 2).
- If you commit but don't push, the grader never sees it.
- `Your branch is ahead of 'origin/main' by 1 commit.` in `git status` means you haven't pushed yet.

---

## Day 2 · 8–16 min — 1-Minute Spoken Check: What This Line Does

- During the last 30 minutes, the instructor visits each seat, **1 minute per student**.
- They'll point to one line on your own screen. Just explain what that line does.
- Your implementation time stays a full 60 minutes — you don't have to stop working.

| Line pointed at | Expected answer |
|---|---|
| `event.preventDefault();` | Stops the page from reloading on submit |
| `localStorage.setItem('final-items', …)` | Saves the list to the browser as text |
| `if (!response.ok)` | Sends the flow to the error notice if the file wasn't found |

---

## Day 2 · 16–24 min ① — 3-Minute Starter Check

1. `git pull` yesterday's `web-final` (or `git clone` if the folder is missing). Overwrite the four exam files.
2. Open `index.html` in a browser once. Check that the page loads and the Console has zero errors.
3. Check `git status` for changed files.

```text
Changes not staged for commit:
	modified:   app.js
	modified:   data/items.json
	modified:   index.html
```

- The number of changed files depends on the question set. Seeing a few of the four is normal.
- If you see an error here, raise your hand. Resolve it **before you start implementing**.
- Pages you turned on yesterday is still live. Don't turn it on again.

---

## Day 2 · 16–24 min ② — Spend the 60 Minutes Like This

| Time | Task |
|---|---|
| 0–5 min | Read the questions, confirm the starter runs |
| 5–15 min | HTML/CSS questions |
| 15–35 min | Form, list add/delete |
| 35–45 min | localStorage |
| 45–52 min | fetch and error notice |
| 52–57 min | Push and submit |
| 57–60 min | Buffer (waiting for Pages to update) |

If you get stuck on one question, move to the next. Questions don't block each other.

---

## Day 2 · 24–30 min — Questions and Start

[Day 2 lab](lab.md#2일차--본시험-구현과-제출-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

- Questions are answered only for wording and environment issues.
- Submit your public address, repository address, last commit hash, and one screenshot.
- Reminders come at 10, 5, and 1 minute before the deadline.

**Explanation total: 8+8+8+6 = 30 min**

---

## What to Submit

1. Public address `https://<your-id>.github.io/web-final/`
2. Repository address `https://github.com/<your-id>/web-final`
3. Last commit hash — the 40 characters from `git log -1 --format=%H`
4. One screenshot — the public address above, open (with the address bar visible)

Make sure your screenshot shows no real name, student ID, or real email. Your ID may be visible.

---

## Wrapping Up the Semester

Over 15 weeks, you built up one site, `my-web`, created in Week 2.

```text
Week 2 publish → Week 3 three pages → Week 4 CSS → Weeks 5–6 JS and the DOM
→ Weeks 7 & 10 forms and lists → Week 11 saving → Week 12 fetch → Week 13 audit
```

Keep both repositories, `my-web` and `web-final` — don't delete them.
What to continue over the break is written in the "problems and fixes" section of your README.
