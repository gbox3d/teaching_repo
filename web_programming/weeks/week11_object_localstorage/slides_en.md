---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 11"
footer: "Objects and localStorage · see the principle through comparison examples, then assemble at the end"
---

# Objects and localStorage

In Week 10, each guestbook line was **one lump of text**, and the list disappeared on reload.

Same method as last week: look at **7 comparison examples** one at a time, then **assemble** `guestbook.html` and `guestbook.js` in a new repository, `web-week11`, built on last week's files.

- Day 1: turn each line into an **object** with a name, a message, and a date.
- Day 2: keep the list in the browser's **storage** (`localStorage`) so it survives a reload.
- **From this week, check and capture on the public address only.** Your PC and the public address have different storage.

---

# Day 1 — Objects and Dot Notation

`30 min explanation & demo → 60 min lab`

1. Example folders — two files: `index.html`, `app.js`
2. ex01 — objects `{ }` and dot notation (today's syntax)
3. ex02 — objects inside an array · the date template line
4. ex03 — an object as one list line

---

## Day 1 · 0–4 min — One example folder, two files

One folder per example, with the same two file names as your site.

```text
ex01/
  index.html   screen — the spots the example uses
  app.js       behavior — this week's ideas live here
```

- Open `index.html`. In `<head>`, `<script src="app.js" defer>` loads `app.js`.
- Edit the code in `app.js`; see the result by reloading `index.html`.
- ex01 and ex02 write to the Console; ex03 writes to the two lists on screen.
- The names match your site's top-level files. Tell them apart by the path bar above the editor (`ex › ex01`).

**Screen in HTML, behavior in JS — two files in one folder.**

---

## Day 1 · 4–11 min — ex01 Objects and dot notation

[examples/day1/ex01/index.html](examples/day1/ex01/index.html) · [app.js](examples/day1/ex01/app.js)

```js
const item = { name: '하늘', message: '안녕하세요', date: '2026. 11. 11.' };
console.log(item.name);    // 2. 하늘
console.log(item.nmae);    // 4. undefined — no red line
const item5 = { name: name, message: message, date: '…' };   // 5.
```

- Inside `{ }`, join `label: value` pairs with commas. An array `[ ]` is ordered; an object `{ }` has labels.
- Read a value with **dot notation**, `item.name`. No quotes around the label.
- `name: name` — the left is the label, the right is the variable.

**An object is a bundle of labeled values; write the label after the dot to get its value.**

---

## Day 1 · 11–19 min — ex02 Objects in an array · date template

[examples/day1/ex02/index.html](examples/day1/ex02/index.html) · [app.js](examples/day1/ex02/app.js)

```js
texts.push('하늘: 안녕하세요');                  // 1·2. Week 10: one lump
const today = new Date().toLocaleDateString();  // the date template
items.push({ name: '하늘', message: '안녕하세요', date: today });   // 3.
console.log(items[0].name);                     // 4. 하늘
```

- `texts[0]` is one lump, `'하늘: 안녕하세요'`. You cannot take out just the name.
- `items[0]` picks **which** bundle; `.name` picks **which value**. Brackets come first.
- `toLocaleDateString()` is a **template**: today as text, like `2026. 11. 11.`.

**Brackets pick which one; the dot picks which value.**

---

## Day 1 · 19–27 min — ex03 An object as one list line

[examples/day1/ex03/index.html](examples/day1/ex03/index.html) · [app.js](examples/day1/ex03/app.js)

```js
li1.textContent = items[i];   // 1. the object as is
li2.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

```text
1. [object Object]       2. 하늘: 안녕하세요 (2026. 11. 11.)
```

- Put a whole object in a text spot and you get `[object Object]`. **It is not an error**, so the Console stays quiet.
- Put dot-notation values inside backticks and `${ }` (Week 5) to write all three in one line.

**Put dot-notation values in a text spot, not the object itself.**

---

## Day 1 · 27–30 min — Your turn

[Day 1 lab](lab.md#1일차--객체와-점-표기-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_object_localstorage)

1. New folder `web-week11` with last week's files; three example folders in `ex/`.
2. ex01–ex03 — open each folder's `index.html`, change values in `app.js`. Say what will change first.
3. Create the new repository `web-week11`, push, and turn on Pages.

**Total explanation: 4+7+8+8+3 = 30 min**

---

# Day 2 — Saving, Restoring, and Assembly

`30 min explanation & demo → 60 min lab`

1. ex04 — `localStorage` storage and the **Application** tab
2. ex05 — `JSON.stringify` / `JSON.parse`
3. ex06 — `||` (or) (today's syntax)
4. ex07 — `removeItem`
5. My list lives only in my browser
6. Assembly — `guestbook.html` and `guestbook.js` in `web-week11`

As yesterday, open each example folder's `index.html` (`ex/ex04/` to `ex/ex07/`).

---

## Day 2 · 0–7 min — ex04 localStorage storage

[examples/day2/ex04/index.html](examples/day2/ex04/index.html) · [app.js](examples/day2/ex04/app.js)

```js
let memo = '(처음 값)';                 // 1. variable: restarts on open
localStorage.getItem('ex04-memo');      // 2. read; null if none
localStorage.setItem('ex04-memo', '안녕하세요');   // write (key, value)
```

- Save → reload: No. 1 is `(처음 값)`, No. 2 is `안녕하세요`.
- **F12 › Application › Local Storage** › the current address: keys and values in a table.
- Storage is separate **for each address** and holds **text only**.

**A variable starts over on reload; what you write in storage stays.**

---

## Day 2 · 7–13 min — ex05 JSON: array to text, text to array

[examples/day2/ex05/index.html](examples/day2/ex05/index.html) · [app.js](examples/day2/ex05/app.js)

```js
localStorage.setItem('ex05-raw', items);                      // 1.
localStorage.setItem('ex05-json', JSON.stringify(items));     // 2.
const back = JSON.parse(localStorage.getItem('ex05-json'));   // 3.
```

- No. 1 stores `[object Object],[object Object]`. Stored as is, the contents are lost.
- No. 2 stores `[{"name":"하늘",…}]`. Bring it back with `JSON.parse` (No. 3); then `back[0].name` works.
- Remember the double-quoted `"name"` shape. Week 12 REST responses are JSON too.

**stringify when you put it in, parse when you take it out.**

---

## Day 2 · 13–18 min — ex06 || (or) (today's syntax)

[examples/day2/ex06/index.html](examples/day2/ex06/index.html) · [app.js](examples/day2/ex06/app.js)

```js
if (name === '' || message === '') { … }    // 1. either one is empty
const items = JSON.parse(localStorage.getItem('ex06-none')) || [];   // 3.
```

- `||` means **or**. Inside an if: "true if either one is true".
- In a value spot: "if the left is missing (`null`), use the right". A first visitor's storage is empty.
- Without `|| []`, reading `length` of `null` gives a red line (comment No. 4).

**For first visitors, end the restore line with `|| []`.**

---

## Day 2 · 18–23 min — ex07 removeItem: clearing storage

[examples/day2/ex07/index.html](examples/day2/ex07/index.html) · [app.js](examples/day2/ex07/app.js)

```js
items = [];                             // 1. array emptied, storage kept
localStorage.removeItem('ex07-list');   // 2. key removed → null
```

- Clear-all does **both**. Empty only the array and the list comes back on reload.
- `removeItem` removes **one** key. Other keys (`ex07-other`) stay.
- `github.io` addresses of the same ID **share** storage. That is why the example keys start with `ex07-`.

**The array and the storage are separate. Clear both.**

---

## Day 2 · 23–26 min — My list lives only in my browser

```text
Chrome on my PC    my posts in 'guestbook'   only I see them
PC next to me      empty                     my posts are not there
file:// on my PC   a different box           check on the public address
```

- **You alone** own the saved list. Someone opening the same address does not see it.
- Sharing across PCs requires server storage. In Weeks 12–14, we use the instructor's shared API.
- On a shared lab PC, the preview address (`localhost:8000`, etc.) may still hold the previous student's posts: same PC, same address, same storage.

**localStorage is storage for this browser and this address only.**

---

## Day 2 · 26–30 min — Assembly: web-week11, then the lab

```text
guestbook.html  remove #empty · [전체 지우기] button   ← Week 10 · ex04
guestbook.js    if (name === '' || message === '')     ← ex06 No. 1
                const today · push({ name: name, … })  ← ex02 · ex01 No. 5
                li.textContent = `${items[i].name}: …`  ← ex03 No. 2
                saveList() — setItem + JSON.stringify   ← ex04 · ex05
                let items = JSON.parse(getItem(…)) || [] ← ex05 · ex06 No. 3
                clear-all: items = [] + removeItem      ← ex07
```

[Day 2 lab](lab.md#2일차--저장-칸에-남기고-되살리기-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_object_localstorage)

1. Save the four example folders ex04–ex07 in `ex/`, change values (until minute 29).
2. Assemble → push → check on the **public address** → screenshot.

**Total explanation: 7+6+5+5+3+4 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week11/guestbook.html
Three posts, reloaded, with F12 › Application › Local Storage open
하늘: 안녕하세요 (2026. 11. 11.)  [삭제]   …   3개
Key: guestbook   Value: [{"name":"하늘","message":"안녕하세요",…}, …]
```

Include the address bar. If posts from your check are still there, press **[전체 지우기]** first.
Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

The list now stays **inside your browser**. But only you can see it.

In Week 12, start `web-week12` from today's files and read the server guestbook with a REST GET request.
Display the JSON array as a list. After connecting the shared HTTPS API, check the same list in another browser.
