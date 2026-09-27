---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 9"
footer: "Project 1 Presentation and Branch Review · 2-Minute Demo and README"
---

# Project 1 Presentation and Branch Review

The Week 8 midterm was built alone, inside the `exam/` folder.
What you show this week is the **main `my-web` site** you built in Weeks 3–7.

```text
Presentation, 2 min   Public URL → three pages → button & form → Commits tab
Report                README.md, first version (5 sections)
```

The weight is **10 points**: 5 for the presentation, 5 for the report.

---

# Day 1 — Preparing the Presentation and README v1

`30 min explanation & demo → 60 min lab`

1. How to give a 2-minute presentation
2. Three places data can live
3. Today's 10-minute Git: one lap around a feature branch
4. A good opening, and one to avoid
5. README v1: 5 sections

---

## Day 1 · 0–6 min — How to Give a 2-Minute Presentation

```text
0:00–0:20  Open the public URL and introduce it in one line
0:20–0:50  Move through the three pages with nav (Home → About Me → Guestbook)
0:50–1:30  One button, one form (including the empty-value message)
1:30–2:00  The GitHub Commits tab and README
```

- Don't show the code. Show the **screen working at the public URL**.
- Open all three tabs before you present. Even typing the address counts toward your 2 minutes.
- Close any tab showing a login screen or personal information before you start.

---

## Day 1 · 6–12 min — Three Places Data Can Live

```text
① The screen           What you've learned so far. Gone on reload
② Browser storage       Stays only in your browser        → Week 11
③ A server on the internet  Everyone sees the same data    → optional special lecture
```

- Today, guestbook entries live in **①**. Reload, and it goes back to `아직 남긴 글이 없습니다.`
- Learn **②** in Week 11, and entries survive a reload on your PC. No one else can see them.
- To let other people's entries show up too, you need **③**. That's not required in this course.
- In your presentation, it's enough to say "this is still ① for now."

---

## Day 1 · 12–22 min ① — Creating and Merging a Feature Branch

```bash
git switch -c readme
git add .
git commit -m "README v1 and 2 screenshots"
git push -u origin readme
```

```text
Switched to a new branch 'readme'
 * [new branch]      readme -> readme
```

- The same order as `about` in Week 2, `guestbook` in Week 3, and `dark-mode` in Week 6.
- Add `-u` because this is the first time you push this branch. `git push -u` covers `--set-upstream-to` for you.
- The public page stays as it is at this point. Pages only deploys `main`.

---

## Day 1 · 12–22 min ② — Deleting a Merged Branch

```bash
git switch main
git merge readme
git push
git branch -d readme
git push origin --delete readme
```

```text
Fast-forward
Deleted branch readme (was 1f74687).
 - [deleted]         readme
```

- `branch -d` deletes it on **your PC**, `push origin --delete` deletes it on **GitHub**. You delete the two separately.
- Try to delete an unpushed branch before merging and you get `error: the branch 'readme' is not fully merged`. For an already-pushed branch it only warns and still deletes — so merge first.
- Its commits stay on main even after you delete the branch. Deleting only removes the label.

---

## Day 1 · 22–26 min — A Good Opening, and One to Avoid

A good opening:

> This is student01's web practice site. It has three pages, and you can leave a line in the guestbook.

An opening to avoid:

> I did the HTML, and the CSS, and the JavaScript. Uh... this part isn't working, though.

- In the first 20 seconds, say **what you built** in one sentence.
- Don't lead with what doesn't work. Show what works first.
- Read it out loud once beforehand — you'll see how short 20 seconds really is.

---

## Day 1 · 26–30 min — README v1 and the Lab Handoff

[Day 1 lab](lab.md#1일차--readme-1차판과-브랜치-한-바퀴-60분) · [Walkthrough](walkthrough.md#1일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project

```text
# Title            ## Public URL    ## Pages (3)
## Features (2 lines)  ## Screens (2 screenshots)  ## What I learned this time (3 lines)
```

- The report isn't a separate document — it's one page, the repository's `README.md`.
- You only use three bits of Markdown: `#`, `-`, and `[visible text](https://주소)`.
- Presentation order and times are announced once the headcount is confirmed.

**Explanation total: 6+6+10+4+4 = 30 min**

---

# Day 2 — The 2-Minute Presentation

`30 min briefing → 60 min presentations`

1. Today's order and preparation
2. Rubric: 10 points
3. Watch one 2-minute demo
4. If the public URL won't open

---

## Day 2 · 0–6 min — Today's Order and Preparation

```text
Tab 1  https://student01.github.io/my-web/
Tab 2  https://github.com/student01/my-web          ← the first screen shows README
Tab 3  https://github.com/student01/my-web/commits  ← Commits tab
```

- Open your three tabs **two people** before your turn.
- Start with the guestbook **empty**. Leave one entry live, during the presentation.
- If you use dark mode, turn it off beforehand. The first screen needs to be light so the text reads well.

---

## Day 2 · 6–12 min — Rubric: 10 Points

| Presentation, 5 | Points |
|---|---:|
| The public URL opens | 1 |
| You move through three pages with nav | 1 |
| A button and a form change the screen | 2 |
| You stay within 2 minutes | 1 |

Report, 5 = README's **5 sections, 1 point each** (public URL / pages / features / screens / what you learned).

Full criteria are in the [rubric](rubric.md).

---

## Day 2 · 12–18 min — Watch One 2-Minute Demo

```text
"This is student01's web practice site. It has three pages."         (0:20)
Home → About Me → Guestbook → Home                                    (0:50)
Click [인사 바꾸기] → the sentence and click count change              (1:10)
Guestbook: enter name & message → [남기기] → one line displayed        (1:30)
Leave the name blank, press [남기기] → the empty-value message          (1:40)
Commits tab → README                                                  (2:00)
```

- Click while you talk. Click, then explain, and your time doubles.
- Show the empty-value message too, and the 2 form points come in one move.

---

## Day 2 · 18–24 min — If the Public URL Won't Open

| What happened | What to do |
|---|---|
| Pages still shows the old screen after 5+ minutes | Accept a local screen plus the **Commits** tab at the same score |
| The public URL shows 404 | Check first whether `index.html` is on `main` in the repository |
| The internet drops | Move to a later slot and present again then |
| A button doesn't work | Show what does work, and explain the cause in the time left |

Don't spend your presentation time fixing it yourself. Raise your hand instead.

---

## Day 2 · 24–30 min — Questions and Presentations Begin

[Day 2 lab](lab.md#2일차--2분-발표-60분) · [Walkthrough](walkthrough.md#2일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project

- Questions we'll answer: presentation order, timing, how to submit, what to do if something breaks.
- There's one oral question during each presentation. For example: "Which file runs when this button is pressed?"
- The audience follows along with the rubric too. One round of applause per presenter.

**Explanation total: 6+6+6+6+6 = 30 min**

---

## What to Submit

```text
① Presentation, 2 min (during Day 2 class)
② Public URL   https://student01.github.io/my-web/
③ Repository URL  https://github.com/student01/my-web
④ 1 screenshot   the repository's first screen — showing README's 5 sections and 2 screenshots
```

Make sure your real name, student ID, and real email address are not visible in the screenshot. Your ID may be visible.

---

## Next Week Preview

Right now, the guestbook loses the first entry the moment you leave a second one.

In Week 10, you **stack** entries in an array and draw them as a list, and you can delete entries.
In Week 11, that list survives a reload, and in Week 12, you load data from a JSON file.
The README you wrote today becomes its final version in Week 13.
