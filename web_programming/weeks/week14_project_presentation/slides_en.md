---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 14"
footer: "Final Project Presentation · 3-minute demo and README"
---

# Final Project Presentation

In Week 9, you showed three pages in **2 minutes**.
Since then you've added lists, saving, and JSON cards, and the site has grown to four pages.

```text
Presentation, 3 min   public address → four pages → button → form notice → list → refresh → cards → Commits
Report                the repository's final README.md
```

Total score is **20 points**: 12 for the presentation, 8 for the report.

---

# Day 1 — Presentation Prep and Final Touches

`30 min explanation & demo → 60 min lab`

1. Presentation order and the 3-minute rule
2. The 20-point rubric
3. The 8-line, 3-minute demo flow
4. When the public address won't open
5. A good opening vs. one to avoid

---

## Day 1 · 0–5 min — Presentation Order and the 3-Minute Rule

```text
0:00  open the public address, one-line intro     1:15  post an entry, delete one line
0:20  four pages via nav                            1:45  refresh — the list is still there
0:40  click **[Dark Mode]**                         2:05  project cards
0:55  submit an empty form → notice                 2:35  Commits tab and README
```

- There are eight beats, about 20–30 seconds each.
- Don't show your code. Show only **the screen working at the public address**.
- Open your tabs ahead of time. Typing the address also counts against your 3 minutes.
- One minute longer than Week 9 — that extra minute covers the list, saving, and cards.

---

## Day 1 · 5–12 min — The 20-Point Rubric (12 Presentation · 8 Report)

| Presentation, 12 | Points | Report, 8 | Points |
|---|---:|---|---:|
| URL and page navigation | 2 | URL and one-line intro | 1 |
| Click events and form notice | 3 | Feature list of 5 items | 2 |
| Add/delete list, survives refresh | 3 | 3 screenshots | 2 |
| JSON cards | 2 | Tech used and `git log` | 1 |
| Timing and narration (including spoken answers) | 2 | 3-line problems-and-fixes | 2 |

The report is a single page: your repository's `README.md`. The final version you wrote in Week 13 **is** the report.
Full criteria are in the [rubric](rubric.md).

---

## Day 1 · 12–18 min — The 8-Line, 3-Minute Demo Flow

Copy the [3-minute demo flow table](demo_outline.md) onto paper, and rewrite only the **What to say** column in your own words.

| Time | Screen / action | What to say |
|---|---|---|
| 0:40–0:55 | **[Dark Mode]** | "Clicking this button changes the background color and raises the click count." |
| 1:45–2:05 | Refresh | "The list is unchanged, because it's saved in the browser." |

- **Also add the eight-line order as a list on your home page.** You'll add this in today's lab.
- Then you can see what's coming next on screen while you present.
- Actually click refresh. Just talking about it doesn't count for points.

---

## Day 1 · 18–24 min — When the Public Address Won't Open

| What happens | What to do |
|---|---|
| TA checks everyone (the day before) | Open every submitted URL, and notify any student whose page won't open |
| Yours opens, but a friend's doesn't | Open it in a **new incognito window**. If the repository is Private, this is where it fails |
| Still won't open in incognito | Switch to a local demo. **You get the same score** |
| Pages shows an old screen | Deploys take 1–3 minutes. Past 5 minutes, also show the **Commits** tab |

For a local demo, use Live Server (**Go Live**) or `python3 -m http.server 8000`.
Don't try to fix it alone during your slot. Just raise your hand.

---

## Day 1 · 24–27 min — A Good Opening vs. One to Avoid

A good opening:

> This is `student01`'s web practice site. It has four pages, and guestbook entries survive a refresh.

An opening to avoid:

> Um... the list usually works. Let me try again. The JSON isn't loading...

- In the first 20 seconds, say **what you built** in one sentence.
- Don't lead with what's broken. Show what works first.
- Read your opening out loud once, and you'll see how short 20 seconds really is.

---

## Day 1 · 27–30 min — Questions and a Preview of the Week 15 Final Scope

[Day 1 lab](lab.md#1일차--최종-통합과-3분-리허설-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation

Today's lab touches only three files: `index.html`, `about.html`, `README.md`.

The Week 15 final exam covers **Weeks 2–13**. It's not today's `my-web` —
you build the form, list, saving, and fetch solo, in a fresh test folder in a new repository. Implementation 15 + demo 5.

**Explanation total: 5+7+6+6+3+3 = 30 min**

---

# Day 2 — The 3-Minute Presentations

`All 90 minutes are presentation time`

```text
0–5 min     instructions
5–68 min    3-minute presentations × 21 students
68–80 min   general feedback and a Week 15 preview
80–90 min   buffer for delays
```

This isn't split into 30 min explanation + 60 min lab. If the class size differs, the order and times will be announced again.

---

## Day 2 · 0–2 min — Today's Order and Setup

```text
Tab 1  https://student01.github.io/my-web/            ← open in an incognito window
Tab 2  https://github.com/student01/my-web             ← the front page showing your README
Tab 3  https://github.com/student01/my-web/commits      ← the Commits tab
```

- Open your three tabs **two people before** your turn.
- Start with the guestbook holding **two or three existing entries**. During your slot, add one and delete one.
- Start with dark mode off. Turn it on at 0:40 to show the change.

---

## Day 2 · 2–4 min — The Rubric and One Spoken Question

- Presentation, 12 points: URL/navigation 2 / click & form notice 3 / list/delete/refresh 3 / JSON cards 2 / timing & narration 2
- Report, 8 points: the grader opens only the `README.md` on your repository's front page.
- One spoken question, e.g.: "Which function runs when you click this button?"

Even if the answer doesn't come immediately, it only affects the 2 timing/narration points.
Two spots lose the most points: **skipping the refresh**, and **a screenshot taken before the action happened**.

---

## Day 2 · 4–5 min — If the Public Address Won't Open

| Symptom | What to do |
|---|---|
| 404 in an incognito window | Check whether `index.html` exists on the `main` branch |
| Old screen | Also show the **Commits** tab. Past 5 minutes, switch to a local demo |
| Cards don't render | The file was opened by double-clicking. Reopen it at the public address |
| List is empty | Your PC's screen and the public address don't share storage. Add one entry right there |

Don't spend your presentation time trying to fix it alone. Raise your hand.

---

## Day 2 · 5–29 min — Presentations Begin (1–8)

[Day 2 lab](lab.md#2일차--3분-발표-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation

- Student 1 starts, 3 minutes each. A signal is given once at 1:45 and once at 2:35.
- The next two students keep their three tabs open.
- Listeners follow along with the rubric, and applaud once when each presentation ends.
- Don't edit your own code during someone else's presentation.

**Explanation total: 2+2+1 = 5 min** — the remaining 85 minutes are presentations (5–68), feedback (68–80), and buffer (80–90)

---

## What to Submit

```text
① 3-minute presentation (during the Day 2 class)
② Public address    https://student01.github.io/my-web/
③ Repository address https://github.com/student01/my-web
④ 1 screenshot       the repository's front page — showing the final README and its 3 screenshots
```

Make sure your screenshot shows no real name, student ID, or real email. Your ID may be visible.
The assignment scope is in the [Project 2 brief](project_brief.md).

---

## Next Week Preview

Week 15 is the **final individual exam**.

Its scope is Weeks 2–13, and you build it solo in a **new repository**, not today's `my-web`.
On Day 1, you create the repository, turn on Pages, and rehearse; Day 2's 60 minutes is the actual exam.
Implementation 15 + demo 5, where the demo 5 comes from the grader opening your submitted public address directly plus one spoken question.
