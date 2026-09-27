---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 10"
footer: "Drawing Array Data as a List · push, createElement, showList"
---

# Drawing Array Data as a List

In Week 7, leaving a second guestbook entry made **the first one disappear.**
That was because the card was a single line. This week, you stack entries in an array and draw them as a list.

```text
guestbook.html   <ul id="list"></ul> · <p id="count">0개</p>   ← where the list goes
guestbook.js     let items = []  →  push  →  build an <li> and append it
```

Only two files change: `guestbook.html` and `guestbook.js`.

---

# Day 1 — Stacking into an Array and Drawing a List

`30 min explanation & demo → 60 min lab`

1. Today's grammar — arrays: `push`, `length`, `[i]`, `for`
2. `createElement`, `textContent`, `append`
3. Adding five lines to the Week 7 code
4. The item count, and three places data can live

---

## Day 1 · 0–5 min — Today's Grammar: Stacking into an Array

```js
let items = [];
items.push('student01: 안녕하세요');
items.push('student02: 고맙습니다');
console.log(items.length);   // 2
console.log(items[0]);       // student01: 안녕하세요

for (let i = 0; i < items.length; i++) {
  console.log(i, items[i]);
}
```

- An array `[ ]` is a box that holds **more than one** value; `push` adds one more to the end.
- `length` is the count, and `items[0]` is the first value. Counting starts **at 0**.
- You use `for` because you need **which position you're at (`i`)**. Today you just build this; you'll use it on Day 2.

---

## Day 1 · 5–12 min — createElement, textContent, append

```js
const li = document.createElement('li');
li.textContent = 'student01: 안녕하세요';
list.append(li);
```

```html
<ul class="card" id="list"></ul>   <!-- leave it empty in the HTML -->
```

- `createElement('li')` makes a new `<li>` that **isn't on the screen yet**.
- `textContent` sets the text inside it. Same as what you used in Week 7.
- Only after you `append` it inside `<ul>` does it actually appear on screen. These three lines are one unit.
- Don't change the order: create, set the text, then append.

---

## Day 1 · 12–20 min — Adding Five Lines to the Week 7 Code

```js
  clearNotice();
  const text = `${name}: ${message}`;
  items.push(text);
  const li = document.createElement('li');
  li.textContent = text;
  list.append(li);
```

- Delete Week 7's single line, `last.textContent = …`, and put these five lines in its place.
- The same sentence goes into **two places**: the array and the screen. That's why you build it once, with `const text`.
- Leave the empty-value check, `focus()`, and `form.reset()` exactly as they were in Week 7.
- Remove the two `<p id="last">` lines from the HTML and replace them with `<ul id="list">`.

---

## Day 1 · 20–25 min — The Item Count, and Three Places Data Can Live

```js
  count.textContent = `${items.length}개`;
```

```text
① The screen           Where today's list is. Gone on reload
② Browser storage       Stays in your browser        → Week 11
③ A server on the internet  Everyone sees the same data  → optional special lecture
```

- Don't count what's on screen. Just show the **array's length** directly (a review from Week 9).
- Today's list is **①**. Reload, and it goes back to an empty list.
- The key idea today: the data lives in the array, and the screen just reflects that array.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--배열에-쌓아-목록으로-그리기-60분) · [Walkthrough](walkthrough.md#1일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

1. Replace the last two lines of `guestbook.html` with `<ul id="list">` and `<p id="count">`.
2. Stack entries into `let items = []`, then create an `<li>` and append it to the list.
3. Check that `N개` (N items) goes up with each entry, and that leaving the name blank still shows the Week 7 message.

**Explanation total: 5+7+8+5+5 = 30 min**

If you get stuck, start with the **first red line** in the Console and a line number like `guestbook.js:31`.

---

# Day 2 — Redrawing the List and a Delete Button

`30 min explanation & demo → 60 min lab`

1. Deleting means changing two places
2. `showList()` — clear it, then redraw
3. A copy-paste template for the delete button
4. Just checking it once you've pasted it in

---

## Day 2 · 0–5 min — Deleting Means Changing Two Places

```text
Yesterday:  submit → push to items       + append one <li> to the screen
Today:      delete → remove one from items + remove that same line from the screen
```

- Yesterday was **only adding**, so appending one line to the screen was enough.
- Deleting has to keep the array and the screen **both** in sync. Change only one, and the count and the screen disagree.
- Instead of removing just one line, you **clear the whole list and redraw it from the array.**
- Since there's only one method, adding and deleting can both call the same function.

---

## Day 2 · 5–12 min — showList(): Clear It, Then Redraw

```js
function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
  }
  count.textContent = `${items.length}개`;
}
```

- `list.innerHTML = ''` **clears** the list. In this course, `innerHTML` is only ever used to clear something.
- The five lines that were inside yesterday's submit handler move into this function, leaving only two lines in submit.
- Standardize on the name `showList`. Call this function after both adding and deleting.

---

## Day 2 · 12–19 min — A Copy-Paste Template for the Delete Button

```js
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
```

- `splice(i, 1)` removes **exactly one** value at position `i` from the array.
- Call `showList()` right after removing it, and the screen redraws to match the new array.
- Every time `showList()` redraws, **it reattaches a fresh number to each button.**
- These seven lines are a **template you copy as-is.** We won't dig into how it works today.

---

## Day 2 · 19–25 min — Just Checking It Once You've Pasted It In

```text
student01: 안녕하세요   [삭제]        3개
student02: 고맙습니다   [삭제]   →   click the middle [삭제]
student03: 반갑습니다   [삭제]
```

```text
student01: 안녕하세요   [삭제]        2개   ← the count drops too
student03: 반갑습니다   [삭제]
```

- Delete the middle line, and the remaining rows' buttons **don't shift out of place.** That's because the list redrew itself.
- The item count just uses `items.length` directly, so you never add or subtract it separately.
- Add one more line so that deleting everything shows `아직 남긴 글이 없습니다.`

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--다시-그리기와-삭제-버튼-60분) · [Walkthrough](walkthrough.md#2일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_supabase_data

1. Move yesterday's five lines out of submit and into a `showList()` function, leaving just two lines in submit.
2. Attach the delete-button template and try removing the middle item.
3. Make sure an empty list shows `아직 남긴 글이 없습니다.`, then push and take a screenshot.

**Explanation total: 5+7+7+6+5 = 30 min**

---

## What to Submit

At the end of Day 2, submit **one** screenshot.

```text
https://student01.github.io/my-web/guestbook.html
Leave 3 entries, then click [삭제] on the middle one

Entries
· student01: 안녕하세요   [삭제]
· student03: 반갑습니다   [삭제]
2개
```

Capture it with the address bar visible. Make sure your real name, student ID, and real email address are not visible in the screenshot.

---

## Next Week Preview

Right now, the list only exists **on screen.** Reload, and it goes back to an empty list.

In Week 11, you turn each entry into an `{ 이름, 메시지, 날짜 }` (name, message, date) **object** and save it to `localStorage`,
so it survives a reload. From then on, you check and screenshot **only at the public URL.**
In Week 12, you load data from a JSON file and draw it as cards.
