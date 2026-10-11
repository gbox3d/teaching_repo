---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 12"
footer: "Loading JSON with fetch · see the principle through comparison examples, then assemble at the end"
---

# Loading JSON with fetch

In Week 11 you put guestbook posts in **browser storage**. This week you write the page content in a **file** and load it with `fetch` to draw cards.

Same method as before: look at **6 comparison examples** one at a time, then **assemble** `data/projects.json`, `projects.html`, and `projects.js` in a new repository, `web-week12`, built on last week's files.

- JSON is **text**. Only text that follows the double-quote rule becomes an array.
- `fetch` **requests** a file. It is blocked on a page opened by double-clicking (`file://`) and works on a server address.
- Results show on screen, in **Console**, and in the **Network** tab, which is new this week.

---

# Day 1 — JSON Files and fetch

`30 min explanation & demo → 60 min lab`

1. The picker page and the server — this week's examples open at `http://localhost:8000/ex/`
2. ex01 — JSON text rules: double quotes and the last comma
3. ex02 — the fetch template: `await fetch` → `await response.json()`, the Network tab
4. ex03 — `file://` vs. `http://`: double-clicking blocks it

---

## Day 1 · 0–4 min — The picker page and opening with the server

[examples/day1/index.html](examples/day1/index.html) — three examples, one screen (one text spot). Server: [server.mjs](../../tools/static-server/server.mjs)

```html
<script src="ex01_json_rule.js"></script>
<!-- <script src="ex02_fetch.js"></script> -->
<!-- <script src="ex03_file_http.js"></script> -->
```

- Turn on **one** `script` line at the bottom (Ctrl+/). Same as Week 6.
- Open `http://localhost:8000/ex/` served by `node server.mjs`, because `fetch` requests a file (ex03).
- Check and capture on the **public address**; the server is a preview.

**Open pages that use fetch on a server address or the public address.**

---

## Day 1 · 4–11 min — ex01 JSON text rules

[ex01_json_rule.js](examples/day1/ex01_json_rule.js) — lines 7–8 (No. 1) · 13–14 (No. 2) · 18–19 (No. 3)

```js
const text1 = `[{"title": "자기소개 페이지"}, {"title": "방명록"}]`;
const projects1 = JSON.parse(text1);
// const text2 = `[{'title': '자기소개 페이지'}, {'title': '방명록'}]`;
// const projects2 = JSON.parse(text2);
// const text3 = `[{"title": "자기소개 페이지"}, {"title": "방명록"},]`;
// const projects3 = JSON.parse(text3);
```

- JSON is **text**. No. 1: **double quotes**. No. 2: single quotes. No. 3: comma after the last `}`.
- Uncomment No. 2 or 3: `JSON.parse` fails with a red line; No. 1 stays.

**Only text that follows the rules becomes an array.**

---

## Day 1 · 11–19 min — ex02 The fetch template and the Network tab

[examples/day1/ex02_fetch.js](examples/day1/ex02_fetch.js) · [ex02_projects.json](examples/day1/ex02_projects.json)

```js
async function loadProjects() {   // await works only inside async
    const response = await fetch('ex02_projects.json');  // 1. request and wait
    const projects = await response.json();              // 2. text → array
    result.textContent = `2. ${projects.length}개를 불러왔다 …`;
}
loadProjects();                   // without this line, nothing happens
```

- **F12 › Network**: one `ex02_projects.json` row, Status **200**, Type `fetch`.
- Without `await` you get a value that has not arrived yet (`Promise`).

**fetch requests the file; json() turns the text it got into an array.**

---

## Day 1 · 19–26 min — ex03 file:// vs. http://

[examples/day1/ex03_file_http.js](examples/day1/ex03_file_http.js) · [ex03_projects.json](examples/day1/ex03_projects.json)

```text
http://localhost:8000/ex/   → screen 3. 2개를 불러왔다
file:///…/ex/index.html     → screen 1. 불러오는 중 … (stuck)
  Access to fetch at 'file:///…' … has been blocked by CORS policy …
  Uncaught (in promise) TypeError: Failed to fetch
```

- Same code, different **address**. On a page opened as `file://`, the browser blocks the request.
- Lines below the failing line (No. 2) do not run, so the screen stays at No. 1.
- "The code is the same but it doesn't work" → look at the **address bar** first.

**fetch works only on a server address (http, https).**

---

## Day 1 · 26–30 min — Your turn

[Day 1 lab](lab.md#1일차--json-파일과-fetch-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

1. New folder `web-week12` with last week's files and `server.mjs`; today's six files in `ex/`.
2. `node server.mjs` → turn on one line for ex01–ex03 and change values. Say what will change first.
3. Create the new repository `web-week12`, push, turn on Pages → open `…/ex/` on the public address too.

**Total explanation: 4+7+8+7+4 = 30 min**

---

# Day 2 — Cards, Error Messages, and Assembly

`30 min explanation & demo → 60 min lab`

1. ex04 — building cards: `img`, `h3`, `p`, `a` inside an `article`
2. ex05 — `try / catch`: catch the error and tell the user on screen
3. ex06 — `response.ok`: a 404 is not an error
4. About the Week 14 final project
5. Assembly — `data/projects.json`, `projects.html`, `projects.js` in `web-week12`

---

## Day 2 · 0–7 min — ex04 Building cards

[examples/day2/ex04_cards.html](examples/day2/ex04_cards.html) · [ex04_cards.js](examples/day2/ex04_cards.js) · [ex04_picture.png](examples/day2/ex04_picture.png)

```js
const article = document.createElement('article');  // one card
article.classList.add('card');                       // the .card rule (Week 6)
const image = document.createElement('img');         // 1. src · alt · width
const title = document.createElement('h3');          // 2. title
const description = document.createElement('p');     // 3. a real sentence, so p
const link = document.createElement('a');            // 4. href
article.append(image, title, description, link);     // in the order given
```

- Same order as Week 10 `showList`: empty → `for` → create and append.
- `alt` is the text shown when the picture cannot be found. Week 13 comes back to it.

**One item in the array becomes one card.**

---

## Day 2 · 7–13 min — ex05 try / catch: tell the user

[ex05_try_catch.html](examples/day2/ex05_try_catch.html) · [ex05_try_catch.js](examples/day2/ex05_try_catch.js) · [ex05_projects.json](examples/day2/ex05_projects.json)

```js
try {   // an error in here skips the lines below and goes to catch
    const response = await fetch('ex05_projects.json');
    const projects = await response.json();
    notice.textContent = `1. try: ${projects.length}개를 불러왔다`;
} catch (error) {
    notice.textContent = '2. catch: 프로젝트를 불러오지 못했습니다.';
}
```

- Server: No. 1; `file://`: No. 2. Day 1 ex03's red `Uncaught` line is gone.

**Catch the error and tell the user on screen.**

---

## Day 2 · 13–19 min — ex06 response.ok: a 404 is not an error

[ex06_response_ok.html](examples/day2/ex06_response_ok.html) · [ex06_response_ok.js](examples/day2/ex06_response_ok.js) · [ex06_projects.json](examples/day2/ex06_projects.json)

```js
const response = await fetch(fileName);
if (!response.ok) {                 // false for a 404
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
    return;                         // do not go on to json()
}
const projects = await response.json();
```

- Even a missing file gets an **answer** (404 + HTML), so `fetch` goes on.
- Read it unchecked and `json()` fails on the HTML: `Unexpected token '<'`.

**Before reading, ask response.ok whether the answer is normal.**

---

## Day 2 · 19–24 min — About the Week 14 final project

Week 14 is the **final presentation**. Nothing new to build: you demo the site you have made so far. Three things are required.

1. Three pages + CSS + a click feature + form input with an empty-input message
2. Guestbook add/delete with a count (Week 10) · a guestbook that survives reload (Week 11)
3. Cards drawn from `data/projects.json` (Week 12)

- The report is the final `README.md` in your repository. We write it together in Week 13.
- The syllabus phrase "persistent CRUD and relations" = Week 11 `localStorage` (persistent) + the card's **페이지 열기** link (relations).
- A server database and login are covered in an optional special session.

**Each week's finished files add up to the final project.**

---

## Day 2 · 24–30 min — Assembly: web-week12, then the lab

```text
data/projects.json  3 objects · double quotes   ← ex01 · ex02 · ex04
projects.html       #notice · #project-list     ← last week's guestbook.html · ex04 · ex05
projects.js         showProjects(projects)      ← ex04
                    loadProjects: try · fetch   ← ex02 · ex05
                    if (!response.ok) … return  ← ex06
                    catch → message · loadProjects(); ← ex05 · ex02
nav on four pages   <a href="projects.html">    ← last week's nav
```

[Day 2 lab](lab.md#2일차--카드와-오류-안내-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud)

1. Save the nine ex04–ex06 files in `ex/`, change values (until minute 28).
2. Assemble → check with the server at 375 and 1280 → push → screenshot of the cards and Network on the public address.

**Total explanation: 7+6+6+5+6 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week12/projects.html
3 cards ─ picture · title · description · 페이지 열기
F12 › Network ─ projects.json   200
Include the address bar in the screenshot
```

Check and capture on the public address. Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

Today you loaded content from a file outside the HTML and drew cards.

In Week 13 you start a new repository, `web-week13`, from today's files and review your four pages.
You check that typed text goes in with `textContent` (security) and that pictures have `alt` and inputs have `label for` (accessibility), then write the final `README.md`.
