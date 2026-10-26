---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 9"
footer: "Project 1 Presentation and README · assemble README v1 from Markdown comparison examples, then a 2-minute talk"
---

# Project 1 Presentation and README

This is the Project 1 week. Put the site you built in Weeks 3–7 (the Week 7 final files) into a new repository, `web-week09`, and write `README.md` v1 to introduce it.

```text
Talk, 2 min   public URL → three pages → button & form → README & Commits tab
Report        README.md v1 on the repository's front page (5 sections)
```

- The README is written in **Markdown**. Look at `#`, `-`, and links one at a time in **3 comparison examples** (`.md`), then **assemble** at the end of Day 1.
- It is worth **10 points** (talk 5 + report 5). It is not part of the weekly lab score.

---

# Day 1 — Three Markdown Marks and README v1

`30 min explanation & demo → 60 min lab`

1. How a 2-minute talk goes
2. Three places data can go
3. ex01 — heading `#`: the number of hashes and the space
4. ex02 — list `-`: no mark means one paragraph
5. ex03 — link `[보이는 글](주소)`
6. Assembly — `README.md` at the top of `web-week09`

---

## Day 1 · 0–4 min — How a 2-Minute Talk Goes

```text
0:00–0:20  Open the public URL and introduce the site in one line
0:20–0:50  Three pages with nav (Home → About Me → Guestbook)
0:50–1:30  One button, one form
1:30–1:40  Empty the name → [남기기] → the empty-value message
1:40–2:00  The 5 README sections on the front page; the Commits tab briefly
```

- You show the public URL of the new repository `web-week09`. The site files are the same as Week 7.
- Do not show code. Show **the screen working at the public URL**.
- The Week 8 exam repository `web-week08` has nothing to do with this project.

**A talk is a fixed order: click while you speak.**

---

## Day 1 · 4–9 min — Three Places Data Can Go

```text
① screen (this tab)    today's guestbook post; gone on reload
② browser storage      stays only in this browser          → Week 11
③ server DB online     many people see it together         → optional special
```

- Leave a guestbook line and reload: it is back to `아직 남긴 글이 없습니다.` A new tab has nothing either.
- The site files are pushed to GitHub, so everyone gets the same files. A visitor's post does not go into those files.
- In your talk it is enough to say "this post is still only on ① the screen".

**Today the site's text lives only on the screen. ② keeps it; ③ shares it.**

---

## Day 1 · 9–15 min — ex01 Headings: # Count and Space

[examples/day1/ex01_heading.md](examples/day1/ex01_heading.md)

```text
source            rendered
# 공개 주소       공개 주소       ← 1. one hash: largest heading
## 공개 주소      공개 주소       ← 2. two hashes: one size smaller
#공개 주소        #공개 주소      ← 3. no space: plain text
```

- In VS Code, **Ctrl+K** then **V** opens the preview beside the source.
- Try: `##` → `###` (smaller). A space in `#공개 주소` → like No. 1.

**The `#` count at the line start sets the size. One space after `#`.**

---

## Day 1 · 15–21 min — ex02 Lists: No Mark Means One Paragraph

[examples/day1/ex02_list.md](examples/day1/ex02_list.md)

```text
source (3 lines)         rendered
- 홈 / - 내 정보 / …     • 홈  • 내 정보  • 방명록   ← 1. a three-line list
홈 / 내 정보 / 방명록    홈 내 정보 방명록          ← 2. joined into one line
-홈 / -내 정보 / …       -홈 -내 정보 -방명록       ← 3. plain text
```

- Just breaking lines in the source joins them into one paragraph. A blank line separates paragraphs.
- Without `-`, the README's two feature lines run together as one paragraph.

**A line that starts with `- ` becomes one list item.**

---

## Day 1 · 21–26 min — ex03 Links: Brackets Are the Text, Parentheses Are the Destination

[examples/day1/ex03_link.md](examples/day1/ex03_link.md)

```text
[MDN 웹 문서](https://developer.mozilla.org/ko/)   ← 1. web address
[ex01 제목 예제](ex01_heading.md)                  ← 2. file in the same folder
[ex01 제목 예제] (ex01_heading.md)                 ← 3. No. 2 plus one space: not a link
```

- In the README you write `[홈 (index.html)](index.html)` and `[홈 화면 캡처](screenshots/home.png)` (the same path style as `images/profile.png` in Week 3).
- Match upper and lower case exactly. GitHub treats `Home.png` and `home.png` as different files.

**For a file in the same repository, put just its name (path) in the parentheses.**

---

## Day 1 · 26–30 min — Assembly: README v1 → Lab

```text
# 내 사이트 이름 · one intro sentence       ← ex01 No.1 · ex02 No.2
## 공개 주소 · 페이지 · 기능 · 화면 · 이번에 배운 것   ← ex01 No.2
- [https://student01.github.io/web-week09/](…)  ← ex02 No.1 · ex03 No.1
- [홈 (index.html)](index.html) — description   ← ex02 No.1 · ex03 No.2
```

[Day 1 lab](lab.md#1일차--마크다운-세-가지로-readme-1차판-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project)

1. Week 7 files in `web-week09`, three in `ex/` → change values (by min 23).
2. Two screenshots → assemble README v1 (by min 43) → pair practice.
3. Push `web-week09` · Pages → one front-page screenshot (submission).

**Total explanation: 4+5+6+6+5+4 = 30 min**

---

# Day 2 — 2-Minute Talks

`30 min briefing → 60 min talks`

1. Today's order and three tabs
2. The 10-point rubric
3. Watch one 2-minute demo
4. If the public URL does not open
5. Questions, then the talks begin

---

## Day 2 · 0–6 min — Today's Order and Three Tabs

```text
tab 1  https://student01.github.io/web-week09/
tab 2  https://github.com/student01/web-week09          ← front page with the README
tab 3  https://github.com/student01/web-week09/commits  ← Commits tab
```

- Open the three tabs **two speakers before** your turn. Typing addresses counts toward your 2 minutes.
- Start with the guestbook **empty**. Leave one line during the talk.
- If you use dark mode, turn it off first. A light first screen is easier to read.

**Tabs opened in advance give the full 2 minutes to the talk.**

---

## Day 2 · 6–12 min — The 10-Point Rubric

| Talk 5 | Points |
|---|---:|
| The public URL opens | 1 |
| Moves through three pages with nav | 1 |
| Button and form change the screen | 2 |
| Keeps to 2 minutes | 1 |

Report 5 = **1 point for each of the 5 README sections** (public URL / pages / features / screens / what I learned). Details are in the [rubric](rubric.md).

**Where most points are lost: screenshots taken before anything was clicked, and a README copied from the example.**

---

## Day 2 · 12–18 min — Watch One 2-Minute Demo

```text
"student01의 웹 연습장입니다. 세 페이지가 있습니다."   (0:20)
Home → About Me → Guestbook → Home                    (0:50)
click [인사 바꾸기] → sentence and click count change  (1:10)
name & message in the guestbook → [남기기] → one line  (1:30)
empty name → [남기기] → notice sentence                (1:40)
5 README sections → Commits tab briefly                (2:00)
```

- In the first 20 seconds say **what you made** in one sentence. Do not start with "I did HTML, I did CSS…".
- Click while you speak. Explaining after each click doubles the time.

**Show what works first, and click while you speak.**

---

## Day 2 · 18–24 min — If the Public URL Does Not Open

| What happened | What to do |
|---|---|
| Pages still old after 5 min | Local screen + **Commits** tab, same score |
| The public URL is 404 | Check `web-week09`, Pages, `index.html` at top |
| The internet is down | Present later in the order |
| A button does not work | Show what works; explain the cause after |

Do not spend talk time fixing things alone. Raise your hand.

**Failures have a fixed fallback. The time point stays.**

---

## Day 2 · 24–30 min — Questions, Then the Talks Begin

[Day 2 lab](lab.md#2일차--2분-발표-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project)

- Questions we take now: order, time, how to submit, what to do if something fails.
- During each talk there is one oral question, e.g. "Which file runs when you press this button?"
- "Does the post disappear on reload?" → "Yes, it is still only on the screen (① of the three places)."
- Listeners follow the rubric too. Fix things during the closing routine at minutes 55–60.

**Total explanation: 6+6+6+6+6 = 30 min**

---

## What to Submit

```text
① 2-minute talk     during the Day 2 class
② public URL        https://student01.github.io/web-week09/
③ repository URL    https://github.com/student01/web-week09
④ one screenshot    repository front page — README 5 sections and 2 screenshot links visible
```

Keep your real name, student ID, and real email out of the screenshot. Your ID may show.

---

## Next Week Preview

Right now the guestbook **loses the first post** when you leave a second one, and loses everything on reload (① of the three places).

In Week 10 you start a new repository, `web-week10`, from this week's final files, **stack** posts in an array, draw them as a list, and delete them.
In Week 11 you keep that list in ② browser storage. Today's README is rewritten as the final version in Week 13.
