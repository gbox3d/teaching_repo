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

1. The picker page — one `index.html`, turn on one script line
2. ex01 — objects `{ }` and dot notation (today's syntax)
3. ex02 — objects inside an array · the date template line
4. ex03 — an object as one list line

---

## Day 1 · 0–4 min — The picker page: turn on one script line

[examples/day1/index.html](examples/day1/index.html) — all three examples use the same screen (two list spots).

```html
<script src="ex01_object.js"></script>
<!-- <script src="ex02_array_objects.js"></script> -->
<!-- <script src="ex03_list_line.js"></script> -->
```

- Same as Week 6. Put the cursor on a line and press **Ctrl+/** (macOS ⌘+/) to turn it on or off.
- Turn on **one line only**. Two lines mix the Console, or the same name clashes and a red line appears.
- ex01 and ex02 write to the Console; ex03 writes to the two lists on screen.

**One `script` line decides which code is loaded.**

---

## Day 1 · 4–11 min — ex01 Objects and dot notation

[examples/day1/ex01_object.js](examples/day1/ex01_object.js)

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

[examples/day1/ex02_array_objects.js](examples/day1/ex02_array_objects.js)

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

[examples/day1/ex03_list_line.js](examples/day1/ex03_list_line.js)

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

[Day 1 lab](lab.md#1일차--객체와-점-표기-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

1. New folder `web-week11` with last week's files; today's four files in `ex/`.
2. ex01–ex03 — turn on one line, change values. Say what will change first.
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

As yesterday, open the examples from one picker page, `index.html` (turn on one of the four script lines).

---

## Day 2 · 0–7 min — ex04 localStorage storage

[examples/day2/index.html](examples/day2/index.html) (picker page, ex04 line on) · [ex04_storage.js](examples/day2/ex04_storage.js)

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

[examples/day2/ex05_json.js](examples/day2/ex05_json.js) — turn on only the ex05 line in the picker page.

```js
localStorage.setItem('ex05-raw', items);                      // 1.
localStorage.setItem('ex05-json', JSON.stringify(items));     // 2.
const back = JSON.parse(localStorage.getItem('ex05-json'));   // 3.
```

- No. 1 stores `[object Object],[object Object]`. Stored as is, the contents are lost.
- No. 2 stores `[{"name":"하늘",…}]`. Bring it back with `JSON.parse` (No. 3); then `back[0].name` works.
- Remember the double-quoted `"name"` shape. It matches the JSON file in Week 12.

**stringify when you put it in, parse when you take it out.**

---

## Day 2 · 13–18 min — ex06 || (or) (today's syntax)

[examples/day2/ex06_or.js](examples/day2/ex06_or.js) — turn on only the ex06 line in the picker page.

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

[examples/day2/ex07_remove.js](examples/day2/ex07_remove.js) — turn on only the ex07 line in the picker page.

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
- To share it across PCs you need **an internet server DB and login** (optional special session).
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

[Day 2 lab](lab.md#2일차--저장-칸에-남기고-되살리기-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls)

1. Save the picker page and the ex04–ex07 `.js` files in `ex/` (it replaces yesterday's `index.html`), change values (until minute 29).
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

In Week 12 you start a new repository, `web-week12`, from today's files, load `data/projects.json` with `fetch`, and draw cards.
The JSON file looks just like the value you saw in the Application tab today. Check and capture on the public address in Week 12, too.
