---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 14"
footer: "Final Project Presentation · check with comparison examples, then a 3-minute demo"
---

# Final Project Presentation

Put the site you built from Week 3 to Week 13 into a new repository, `web-week14`, and show it on Day 2 from one public address in **3 minutes**.

Same method as before: look at **3 comparison examples**, then **assemble** the home list, the public-address row, and the README on top of last week's files.

```text
3-min demo   public URL → four pages → button → form notice → list → reload → cards → Commits
Report       README.md (final version) in the repository
```

- No new syntax this week. All 90 minutes of Day 2 are presentations.
- Worth **20 points**: presentation 12 + report 8.

---

# Day 1 — Preparing the Talk and the Last Assembly

`30 min explanation & demo → 60 min lab`

1. Presentation order and the 3-minute rule · the 20-point rubric
2. ex01 — the demo order as a numbered list on the home page
3. ex02 — if the public URL won't open: local demo with the server
4. ex03 — saved entries are separate for each address and window
5. Good and bad openings · assembly

---

## Day 1 · 0–4 min — Presentation order and the 3-minute rule

```text
0:00  open the public URL, one-line intro     1:15  add an entry, delete one
0:20  nav through the four pages              1:45  reload — the list stays
0:40  click [다크 모드]                        2:05  project cards
0:55  [남기기] with empty fields → notice      2:35  Commits tab and README
```

- Eight steps, 20–30 seconds each. One minute longer than Week 9 (list, saving, cards).
- Don't show code. Show only **screens working at the public URL**.
- Open your tabs in advance. Typing an address also uses up your 3 minutes.

**A fixed order, followed as planned, is how you stay within 3 minutes.**

---

## Day 1 · 4–10 min — The 20-point rubric (talk 12 · report 8)

| Presentation 12 | Pts | Report 8 | Pts |
|---|---:|---|---:|
| URL & page navigation | 2 | URL & one-line intro | 1 |
| Click event & form notice | 3 | Five features listed | 2 |
| List add/delete & kept after reload | 3 | Three screenshots | 2 |
| JSON cards | 2 | Technologies & build history | 1 |
| Time & explanation (incl. oral) | 2 | Three lines of problems & fixes | 2 |

The report is your repo's `README.md`: change three spots from Week 13 ([rubric](rubric.md)).
**Actually press reload. Saying it without doing it loses that point.**

---

## Day 1 · 10–15 min — ex01 The demo order as a numbered list

[examples/day1/ex01_order_list.html](examples/day1/ex01_order_list.html) · [3-minute demo outline](demo_outline.md)

```html
<ol>                                          <!-- 1. numbered list -->
    <li>위 메뉴로 네 페이지를 오갑니다.</li>    <!-- no number typed -->
</ol>
<ul> … the same five lines … </ul>            <!-- 2. bulleted list -->
```

- You don't write the numbers. The browser numbers the lines in order.
- Rows 2–7 of the demo outline become five lines on the home page.
- Try: delete `</ol>`. The heading and list after it move inside box 1.

**If the order means something, use `<ol>`; otherwise use `<ul>`.**

---

## Day 1 · 15–20 min — ex02 If the public URL won't open: local demo with the server

[ex02_server.html](examples/day1/ex02_server.html) · [ex02_server.js](examples/day1/ex02_server.js) · [ex02_message.json](examples/day1/ex02_message.json)

```text
① The day before, the TA opens every submitted public URL
② Opens only on your own screen → open it in a new incognito window
③ Still won't open → local demo: node server.mjs → http://localhost:8000/ (same points)
```

```js
const response = await fetch('ex02_message.json');   // 1. opened through the server: it reads the file
// 2. double-clicked file:// page: it can't read, so it goes to catch
```

- Double-click to open, and Console shows a red `… blocked by CORS policy` line. On your site, the cards don't appear.

**`fetch` reads files only on pages opened through a server or a public URL.**

---

## Day 1 · 20–24 min — ex03 Saved per address and window

[ex03_storage.html](examples/day1/ex03_storage.html) · [ex03_storage.js](examples/day1/ex03_storage.js)

```js
let countVar = 0;                                                      // 1. variable
let countSaved = JSON.parse(localStorage.getItem('ex03-count')) || 0;  // 2. storage
```

- Three clicks, then reload: No. 1 is 0, No. 2 is 3. Storage (Week 11) survives.
- Server address or new incognito window: No. 2 starts at 0. Same-ID `github.io` addresses (`web-week13`·`web-week14`) share one storage.
- So add the entries right before your talk, **in the window you present in**.

**Entries that survive a reload live in the storage of that address and that window.**

---

## Day 1 · 24–27 min — Good and bad openings

A good opening:

> `student01`의 웹 연습장입니다. 네 페이지가 있고, 방명록에 남긴 글이 새로고침해도 남습니다.

An opening to avoid:

> 어… 목록이 원래 되는데요. 다시 해 볼게요. JSON이 안 불러와져서…

- In the first 20 seconds, say **what you built** in one sentence.
- Don't start with what's broken. Show what works first.
- Read it aloud once and you'll feel how short 20 seconds is.

**The first sentence says what you built.**

---

## Day 1 · 27–30 min — Assembly: web-week14, then your turn

```text
index.html   <h2> + <ol class="card"> five lines     ← ex01 No. 1 · Week 13 .card
about.html   <tr> public-address row (two <td>)     ← a row of the Week 13 table
README.md    public URL · home line · Week 14 history ← same lines in Week 13 README
```

[Day 1 lab](lab.md#1일차--비교-예제-조립-3분-리허설-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

1. Last week's files in `web-week14`; today's six files in `ex/`. Change values.
2. Assemble → push `web-week14` **at minute 31** and turn on Pages (Day 2 is the talk).
3. Public URL check, new `home.png` → TA check, 3-minute rehearsal → end routine.

**Total explanation: 4+6+5+5+4+3+3 = 30 min**

---

# Day 2 — 3-Minute Presentations

`All 90 minutes are presentations`

```text
0–5 min    instructions
5–68 min   presentations, 3 min × 21 students
68–80 min  wrap-up and Week 15 preview
80–90 min  buffer for delays
```

Not split into 30 + 60. If the class size differs, the order and times are announced again.

---

## Day 2 · 0–2 min — Today's order and three tabs

```text
tab 1  https://student01.github.io/web-week14/            ← the window you present in
tab 2  https://github.com/student01/web-week14            ← front page with the README
tab 3  https://github.com/student01/web-week14/commits    ← Commits tab
```

- Open the three tabs **two turns before** yours.
- Start with **two or three guestbook entries**. An incognito window forgets them when closed, so add them again in that window (ex03).
- Start with dark mode off. Click it at 0:40 to show the change.

---

## Day 2 · 2–4 min — The rubric and one oral question

- Presentation 12: URL & navigation 2 / click & form notice 3 / list, delete & reload 3 / JSON cards 2 / time & explanation 2
- Report 8: the grader opens only the `README.md` on the repository front page.
- The oral part is **one question**, e.g. "이 버튼을 누르면 어느 함수가 실행됩니까?"

Follow it: button → its `id` in Elements → the line in `.js` that finds that `id` → the function inside `addEventListener`.

The two places that lose the most points: **skipping the reload** and **screenshots taken before anything happened**.

---

## Day 2 · 4–5 min — If the public URL won't open

| Symptom | What to do |
|---|---|
| 404 in an incognito window | Check that `index.html` is at the top of the `web-week14` repository |
| Old version shows | Show the **Commits** tab too. After 5 minutes, switch to a local demo |
| Cards don't appear | It was opened by double-click. Reopen at the public URL or with `node server.mjs` (ex02) |
| The list is empty | Incognito and other addresses have their own storage. Add an entry right there (ex03) |

Don't spend your presentation time fixing it alone. Raise your hand. A local demo earns **the same points**.

---

## Day 2 · 5–30 min — Presentations begin (from No. 1)

[Day 2 lab](lab.md#2일차--3분-발표-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

- Starting with No. 1, 3 minutes each. A signal at 1:45 and at 2:35.
- The next two presenters keep their three tabs open.
- Listeners follow the rubric too, and clap once at the end.
- Don't edit your own code during someone else's talk.

From minute 30, presentations continue on the Day 2 schedule in the lab.

**Total explanation: 2+2+1+25 = 30 min** (25 min are presentations No. 1–8)

---

## What to Submit

```text
① 3-minute presentation (Day 2 class)
② Public URL       https://student01.github.io/web-week14/
③ Repository URL   https://github.com/student01/web-week14
④ One screenshot   repository front page — README (final) and its three screenshots visible
```

Keep your real name, student ID, and real email out of the screenshot. Your ID may show.
The project scope is in the [project brief](project_brief.md).

---

## Next Week Preview

Week 15 is the **individual final practical**.

It covers Weeks 1–14, and you solve it alone in a **new repository**, `web-week15`.
On Day 1 you practice with the [problem bank](../week15_final_exam/examples/README.md), create the repository, and turn on Pages. Day 2's 60 minutes are the practical: one bank problem per area, with only the values changed.
Implementation 15 + demo 5; the demo 5 is the grader opening your submitted public URL plus one oral question.
