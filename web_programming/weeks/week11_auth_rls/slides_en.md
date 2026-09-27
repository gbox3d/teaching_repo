---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 11"
footer: "Objects and localStorage · object, JSON.stringify, localStorage"
---

# Objects and localStorage

In Week 10, the guestbook **list disappeared on refresh.** Each value was also a single string, like `student01: Hello`.
This week we turn each entry into an object and write it to browser storage.

```text
guestbook.js   items = ['Haneul: Hello']                ← Week 10
               items = [{ name, message, date }]        ← Day 1 today
               saved & restored via localStorage['guestbook']  ← Day 2 today
```

You only edit two files: `guestbook.html` and `guestbook.js`.

---

# Day 1 — Turn Entries into Objects

`30 min explanation & demo → 60 min lab`

1. Today's syntax — objects and dot notation
2. Objects inside an array
3. Turn a guestbook entry into an object
4. Name, message, and date on one list line

---

## Day 1 · 0–5 min — Today's Syntax: Objects and Dot Notation

```js
const item = { name: 'Haneul', message: 'Hello', date: '2026. 9. 16.' };

console.log(item.name);      // Haneul
console.log(item.date);      // 2026. 9. 16.
```

- An object `{ }` groups together **labeled values** as one unit.
- Write `name: value` pairs separated by commas. Here there are three labels: `name`, `message`, `date`.
- To read a value, use **dot notation**, like `item.name`. Don't put quotes around the label.
- An array `[ ]` holds several values in order; an object `{ }` holds one labeled group.

---

## Day 1 · 5–12 min — Objects Inside an Array

```js
let items = [];
items.push({ name: 'Haneul', message: 'Hello', date: '2026. 9. 16.' });
items.push({ name: 'Bada', message: 'Great to see this', date: '2026. 9. 16.' });

console.log(items.length);       // 2
console.log(items[0].name);      // Haneul
console.log(items[1].message);   // Great to see this
```

- The array from Week 10 stays the same. Only what it holds changes, from strings to **objects**.
- Use `items[i]` to get one group, then add `.name` to read one value inside it.
- `items[0].name` means "the name in the first entry." Numbering starts **at 0**.

---

## Day 1 · 12–18 min — Turn a Guestbook Entry into an Object

```js
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
```

- In Week 10 you stored one sentence. Now you store **three values, each with a label**.
- `new Date().toLocaleDateString()` turns today's date into something like `2026. 9. 16.`. It's a **copy-paste template**, one line.
- We also clean up the notice text today. Combine the two checks into one: `if (name === '' || message === '')`.
- `||` means **or**. If either field is empty, show the notice and stop with `return`.
- Remove `<p id="empty">`. Show the empty-list notice in the same spot as the count (`#count`).

---

## Day 1 · 18–25 min — Name, Message, and Date on One List Line

```js
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

```text
Haneul: Hello (2026. 9. 16.)             [Delete]
Bada: Great to see this (2026. 9. 16.)   [Delete]
2 items
```

- In `showList()`, **this is the only line that changes**. Everything else stays as it was in Week 10.
- Drop the dot notation and write only `items[i]`, and the screen shows `[object Object]`.
- The count spot now does two jobs: an empty-list notice, or a count like `2 items`.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--항목을-객체로-바꾸기-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

1. Change the value passed to `items.push` into a **name/message/date object**.
2. Rewrite the list line with dot notation so all three values show together.
3. Combine the notice checks into one line, and move the empty-list notice to the count spot.

**Explanation total: 5+7+6+7+5 = 30 min**

Today the list still disappears on refresh. We add saving tomorrow.

---

# Day 2 — Save to the Browser and Restore It

`30 min explanation & demo → 60 min lab`

1. Why the list disappears on refresh
2. `JSON.stringify` and `saveList()`
3. Restore the list when the page opens
4. The Application tab and Clear All

---

## Day 2 · 0–6 min — Why the List Disappears on Refresh

```text
① Screen (memory)      gone after a refresh                ← through yesterday
② Browser storage       stays, same browser + same address  ← today
③ Internet server DB    visible on other people's PCs too    ← optional special lecture
```

- `let items = [];` **starts over as an empty array** every time the page opens.
- Each address has its own small storage box in the browser. This is `localStorage`.
- Only **strings** can go in that storage box. An array can't go in as-is.
- So today we do two things: turn the array into a string, and turn the string back into an array.

---

## Day 2 · 6–13 min — JSON.stringify and saveList()

```js
function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}
```

```text
Key     guestbook
Value   [{"name":"Haneul","message":"Hello","date":"2026. 9. 16."}]
```

- `JSON.stringify(items)` turns the array into **one string**.
- `localStorage.setItem('key', 'value')` writes that string into the browser.
- **Fix** the key name as `guestbook`. A different name would store it in a different box.
- Call `saveList()` in **two places**: after adding and after deleting.

---

## Day 2 · 13–20 min — Restore the List When the Page Opens

```js
let items = JSON.parse(localStorage.getItem('guestbook')) || [];
```

- `getItem('guestbook')` returns the **string** you stored. If nothing was ever stored, it returns `null`.
- `JSON.parse(...)` turns that string back into an **array**.
- `|| []` means "if there's nothing, use an empty array." A first-time visitor lands here.
- This one line is a **copy-paste template**. Swap it in for `let items = [];`.
- `showList();` at the end of the file draws the restored array. It's the line you already added in Week 10.

---

## Day 2 · 20–25 min — The Application Tab and Clear All

```js
clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});
```

- In **F12 › Application › Local Storage**, look at the `guestbook` key and its value.
- `removeItem('guestbook')` clears the storage box; `items = [];` empties the array on screen.
- On a shared PC, the same `github.io` address under one ID **shares** the same storage box.
- If you see a previous person's entries, click **[Clear All]** first, then screenshot **only your own entries**.

---

## Day 2 · 25–28 min — Your List Lives Only in Your Browser

```text
My PC's browser    localStorage['guestbook']   visible only on my screen
Neighbor's PC       empty                       has none of my entries
```

- The list you save today lives **only inside your own browser**. You are the only owner of it.
- Even if your neighbor opens the same public address, they won't see your entries.
- To share the list across PCs, you'd need **an internet server database and login**.
- Server databases and login are covered in the optional special lecture. This course's storage stops here.

---

## Day 2 · 28–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--브라우저에-저장하고-되살리기-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls

1. Write `saveList()` and call it after adding and after deleting.
2. Replace the `let items = ...` line with the copy-paste template so the list survives a refresh.
3. Add the **[Clear All]** button and take your screenshot at the public address.

**Explanation total: 6+7+7+5+3+2 = 30 min**

From today on, check and screenshot **only at the public address**.

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/my-web/guestbook.html
A screen with 3 entries left, refreshed, with F12 › Application › Local Storage open together

Haneul: Hello (2026. 9. 16.)   [Delete]      3 items
Key: guestbook
Value: [{"name":"Haneul","message":"Hello","date":"2026. 9. 16."}, …]
```

Take the screenshot with the address bar visible. If you see a previous person's entries, click **[Clear All]** first.
Make sure your screenshot shows no real name, student ID, or real email.

---

## Next Week Preview

The list now stays **inside your own browser**. But only you can see those entries.

In Week 12, you create a `data/projects.json` file, load it with **fetch**, and draw the values as cards.
The JSON file's format looks just like the value you saw in the Application tab today.
In Week 12 too, you check and screenshot at the public address.
