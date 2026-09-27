---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 12"
footer: "Loading JSON with fetch · data/projects.json, await, try/catch"
---

# Loading JSON with fetch

In Week 11, you put guestbook entries into a **browser storage box**.
This week you keep the screen's content in a **file** and load it in.

```text
data/projects.json ── fetch ──▶ projects.js ──▶ projects.html
   title · description · image · link      read and turned into cards      3 cards
```

---

# Day 1 — Read a JSON File and Draw Cards

`30 min explanation & demo → 60 min lab`

1. Check Pages first (today's 5-minute tool)
2. JSON files and the double-quote rule
3. The `loadProjects()` template — fetch · json · `console.log`
4. The Console error you get from opening with `file://`

---

## Day 1 · 0–5 min — Today's Tool: Check Pages First

```text
My PC ── git push ──▶ GitHub ── Pages ──▶ https://student01.github.io/my-web/
```

- This week, **checking and screenshotting is based on the public address**. `fetch` only works from a server address.
- Optional preview while you work: VS Code extension **Live Server** → status bar **Go Live** → `http://127.0.0.1:5500/`
- If the extension is blocked, use `python3 -m http.server 8000` in the terminal.
- Neither is required. **Fix one thing at a time, push it**, and check the public address.

---

## Day 1 · 5–11 min — What Is a JSON File

```json
[
  { "title": "About-Me Page", "description": "This is the home screen." },
  { "title": "My Info Table", "description": "A table of my ID and email." }
]
```

- This has the same shape you saw in **Application › Local Storage** in Week 11.
- Use **only double quotes `"`** for names and string values. Single quotes are an error.
- Don't leave a trailing comma after the last item.
- Keep the file as `projects.json` inside the `data/` folder.

---

## Day 1 · 11–19 min ① — Draw the Loaded Values as Cards

```js
function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    article.append(title);
    projectList.append(article);
  }
}
```

Same order as `showList()` in Week 10: clear it → classic `for` loop → build and append.

---

## Day 1 · 11–19 min ② — The loadProjects() Template

```js
async function loadProjects() {
  const response = await fetch('data/projects.json');
  const projects = await response.json();
  console.log(projects);
  showProjects(projects);
}

loadProjects();
```

- `async` and `await` come in pairs. This week, treat them as a **copy-paste template**.
- `await` means "wait until it arrives." Both lines need to wait.
- Use `console.log(projects)` to check first that the array arrived.

---

## Day 1 · 19–25 min — Opening with file:// Gives No Cards

```text
Access to fetch at 'file:///…/data/projects.json' from origin 'null'
has been blocked by CORS policy: Cross origin requests are only
supported for protocol schemes: chrome, chrome-extension, …, http, https

Uncaught (in promise) TypeError: Failed to fetch     projects.js:18
```

- A page opened by double-clicking has a `file://` address, so `fetch` is blocked. The page looks empty.
- It works as expected from a **public address (https)** or Live Server (`http://127.0.0.1:5500/`).
- `projects.js:18` at the end of the error line is the **file name and line number** — read it the same way you read `app.js:6` in Week 5.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--json-파일을-만들어-카드로-그리기-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

1. Write three projects into `data/projects.json`.
2. Create `projects.html` and `projects.js`, and check with `console.log`.
3. Draw the cards, then push and check them at the **public address**.

**Explanation total: 5+6+8+6+5 = 30 min**

If you get stuck, start with the first red line in the Console and the `file name:line number` at its end.

---

# Day 2 — Error Handling and Finishing the Cards

`30 min explanation & demo → 60 min lab`

1. Catch errors with `try / catch` and show a notice
2. `response.ok` and 404
3. Add an image and a **View page** link to each card
4. Announce the Week 14 final project

---

## Day 2 · 0–6 min — Catch Errors with try / catch

```js
async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    const projects = await response.json();
    showProjects(projects);
  } catch (error) {
    notice.textContent = 'Could not load the projects.';
  }
}
```

- If an error happens inside `try`, execution doesn't stop — it jumps to `catch`.
- The sentence shown on screen is fixed to one line: `Could not load the projects.`

---

## Day 2 · 6–12 min — response.ok and 404

```js
if (!response.ok) {
  notice.textContent = 'Could not load the projects.';
  return;
}
```

```text
Uncaught (in promise) SyntaxError: Unexpected token '<',
"<!DOCTYPE "... is not valid JSON
```

- If the file name is wrong, the server sends a 404 and an **HTML error page**.
- `response.json()` tries to read that HTML and throws the error above. Check `response.ok` first to catch it early.
- A path starting with `/`, like `/data/projects.json`, gives a 404 at the public address.

---

## Day 2 · 12–19 min ① — Add an Image and a Link to Each Card

```js
const image = document.createElement('img');
image.src = projects[i].image;
image.alt = `${projects[i].title} screenshot`;
image.width = 240;
const link = document.createElement('a');
link.href = projects[i].link;
link.textContent = 'View page';
article.append(image, title, description, link);
```

- Items stack inside the card **in the order** you pass them to `append`.
- `alt` is the text read aloud when the image doesn't load. We revisit it in Week 13.

---

## Day 2 · 12–19 min ② — Reuse .card As Is

```css
.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}
```

- This rule was made in Week 4. **Don't add a new rule** to `styles.css`.
- One line, `article.classList.add('card')`, gives it the same look.
- If the card doesn't look like a white box, check the spelling of `classList.add` first.

---

## Day 2 · 19–25 min — Announcing the Week 14 Final Project

**Required features** (the Week 9 site + Week 10–12 features)

1. Three pages + CSS + click behavior + form input with empty-value notice
2. Guestbook add/delete and count (Week 10)
3. A guestbook that survives a refresh (Week 11)
4. Cards drawn by reading `data/projects.json` (Week 12)

**Final README**: public address · page list · features · three `screenshots/` · what you learned

The presentation is a 3-minute demo. Full details come in Week 13.

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--오류-안내와-카드-완성-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_persistent_crud

1. Add a notice spot to `projects.html` and add `try / catch` and `response.ok`.
2. Add an image and a **View page** link to each card.
3. Add a `projects.html` link to all four pages' nav, and push.

**Explanation total: 6+6+7+6+5 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

- Public address `https://<your-id>.github.io/my-web/projects.html`
- Three cards are visible (image · title · description · **View page**)
- `projects.json` shows **Status 200** in **F12 › Network**
- Take the screenshot with the address bar visible

Make sure your screenshot shows no email or real name. Your ID may be visible.

---

## Next Week Preview

Now the screen's content lives in a file outside your HTML.

In Week 13, you audit all four pages: revisit `textContent` (which shows typed text as-is),
image `alt`, and form `label for`, and compute an admission year with `about.js`.
You'll also finalize the repository `README.md` and its three `screenshots/`.

---

## Minimum Compliance — the Syllabus's "Persistent CRUD and Relational Features"

| Syllabus wording | What this course does |
|---|---|
| Persistent | Week 11 `localStorage` — a guestbook that survives a refresh |
| CRUD | Weeks 10–11 — add, list, delete, and clear all guestbook entries |
| Relational features | Week 12 — card → detail page link (`link.href`) |

Server databases and login are covered in this course's optional special lecture.
