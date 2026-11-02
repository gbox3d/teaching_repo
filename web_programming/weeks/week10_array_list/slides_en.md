---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 10"
footer: "Drawing Array Data as a List · see the principle through comparison examples, then assemble at the end"
---

# Drawing Array Data as a List

In Week 9 the guestbook appended one list line per entry, but **only on screen**, so no single line could be deleted. This week we keep entries in an **array**, **redraw** the list from it, and add a **[삭제]** (delete) button to every line and a count below the list.

Same method as before: look at **7 comparison examples** one at a time, then **assemble** `guestbook.html` and `guestbook.js` in a new repository, `web-week10`, built on last week's files.

- Keep many values in one array; make each line on screen and attach it.
- Results show on screen, in **Console** (type `items` in the input line), and in the **Elements** tab.
- One example = one idea. The lab is about **changing values** and watching.

---

# Day 1 — Arrays and One List Line

`30 min explanation & demo → 60 min lab`

1. ex01 — arrays: `[]`, `push`, `length`, `items[i]` (today's syntax)
2. ex02 — `for`: from first to last (today's syntax)
3. ex03 — one list line: create it, fill in the text, attach it (Week 7 ex08 review)
4. ex04 — add on every click, and the count
5. Three places data can go

---

## Day 1 · 0–5 min — ex01 Arrays: many values in order

[examples/day1/ex01/index.html](examples/day1/ex01/index.html) · [app.js](examples/day1/ex01/app.js)

```js
let items = [];                          // 1. empty array, count 0
items.push('student01: 안녕하세요');      // 2. push adds one at the end
items.push('student02: 고맙습니다');      //    three times → count 3
items.push('student03: 반갑습니다');
console.log('3. 첫 번째 items[0] :', items[0]);
console.log('4. 마지막 items[2] :', items[2]);
console.log('5. 없는 번호 items[3] :', items[3]);   // undefined
```

- Three values have numbers 0, 1, 2 and a count of 3. **Last number = count - 1**.
- No. 6, `['student01', 'student02']`, starts filled: values split by commas.

**An array keeps values in order, and numbering starts at 0.**

---

## Day 1 · 5–10 min — ex02 for: from first to last

[examples/day1/ex02/index.html](examples/day1/ex02/index.html) · [app.js](examples/day1/ex02/app.js)

```js
// the array holds 4 values
for (let i = 0; i < 3; i++) {              // 1. a number → misses the 4th
    console.log('1.', i, items[i]);
}
for (let i = 0; i < items.length; i++) {   // 2. length → to the end
    console.log('2.', i, items[i]);
}
```

- `let i = 0` start · `i < items.length` keep going · `i++` add 1 each round.
- We use this form **to get the position `i`**: `items[i]` is its value.

**Write the end as `items.length`, not as a number.**

---

## Day 1 · 10–17 min — ex03 One list line: create, fill, attach (Week 7 ex08 review)

[examples/day1/ex03/index.html](examples/day1/ex03/index.html) · [app.js](examples/day1/ex03/app.js)

```js
const li2 = document.createElement('li');   // create (not on screen yet)
li2.textContent = '2. 만들고 붙인 줄';       // fill in the text
list.append(li2);                           // attach at the end → visible
```

- No. 1 (`li1`) is only created, so it shows in Console but not on screen or in **Elements**.
- `append` always attaches **at the end**. No. 3 lands below No. 2.
- The same three lines as Week 7 ex08 No. 2. Today we set them beside No. 1, which is only created.

**A created element shows only after you attach it with `append`.**

---

## Day 1 · 17–23 min — ex04 Add on every click, and the count

[examples/day1/ex04/index.html](examples/day1/ex04/index.html) · [app.js](examples/day1/ex04/app.js)

```js
addButton.addEventListener('click', function () {
    const text = textInput.value;
    items.push(text);                          // 1. put it in the array
    const li = document.createElement('li');   // 2. attach it on screen
    li.textContent = text;
    list.append(li);
    count.textContent = `${items.length}개`;   // 3. count from the array
});
```

- Array and screen are **separate**; count with **`items.length`**, not lines.

**The array is the original; the screen only reflects it.**

---

## Day 1 · 23–27 min — Three places data can go

```text
① screen (array)        today     gone on reload
② browser storage       Week 11   stays in my browser
③ internet server DB    special   many people see it
```

- Today's list is **①** — only in the array and on screen.
- ③ is covered in the [optional Supabase special session](../../specials/supabase_guestbook/README.md).

**Today's list lives only on screen. A reload starts it over.**

---

## Day 1 · 27–30 min — Your turn

[Day 1 lab](lab.md#1일차--배열과-목록-한-줄-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_array_list)

1. New folder `web-week10` with last week's files; four example folders in `ex/` (`index.html` and `app.js` in each).
2. ex01–ex04 — open each folder's `index.html`, change values in `app.js`. Type `items` in the Console input line.
3. Create the new repository `web-week10`, push, and turn on Pages (same steps as Week 2).

**Total explanation: 5+5+7+6+4+3 = 30 min**

---

# Day 2 — Redrawing, Delete Buttons, and Assembly

`30 min explanation & demo → 60 min lab`

1. To delete, you must change two places
2. ex05 — clear, then redraw: `list.innerHTML = ''`
3. ex06 — `showList()`: the screen follows the array
4. ex07 — the delete-button template
5. Assembly — `guestbook.html` and `guestbook.js` in `web-week10`

---

## Day 2 · 0–4 min — To delete, you must change two places

```text
Week 9: leave  → append one <li> on screen (no array, can't delete)
Day 1:  add    → push into the array     + append one <li> on screen
today:  delete → take one out of array   + take that line off screen
```

- Change only one side and the array and screen disagree, just as in Day 1's ex04.
- So instead of removing one line, we **clear the whole list and redraw it from the array.**
- Adding and deleting then call the same one function. In Week 11 this array is what we save.

**When the array changes, redraw the screen.**

---

## Day 2 · 4–10 min — ex05 Clear, then redraw

[examples/day2/ex05/index.html](examples/day2/ex05/index.html) · [app.js](examples/day2/ex05/app.js)

```js
// 2. clear, then draw
list.innerHTML = '';                        // empty the whole list
for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
}
```

- No. 1 (no clearing) grows by three lines every click; No. 2 stays at three lines however often you click.
- In this course `innerHTML` is used **only to clear (`= ''`)**. Put text in with `textContent`.

**Clear first, then redraw.**

---

## Day 2 · 10–17 min — ex06 showList(): the screen follows the array

[examples/day2/ex06/index.html](examples/day2/ex06/index.html) · [app.js](examples/day2/ex06/app.js)

```js
function showList() {
    list.innerHTML = '';                       // clear
    for (let i = 0; i < items.length; i++) {   // make and attach each line
        …
    }
    count.textContent = `${items.length}개`;   // count and notice too
    if (items.length === 0) { … } else { … }
}
showList();                                    // 1. once, on open
```

- No. 2: clicking **더하기** (add) calls `showList();` after `items.push(…)`. The notice disappears and the count goes up.

**Everything on screen is rebuilt from the array.**

---

## Day 2 · 17–24 min — ex07 The delete-button template

[examples/day2/ex07/index.html](examples/day2/ex07/index.html) · [app.js](examples/day2/ex07/app.js)

```js
const removeButton = document.createElement('button');
removeButton.textContent = '삭제';
removeButton.addEventListener('click', function () {
    items.splice(i, 1);     // take the i-th value out of the array
    showList();             // redraw from the changed array
});
li.append(removeButton);    // attach the button inside that line
```

- These seven lines are a **template you copy as is**. Put them between the `li.textContent` line and the `list.append(li)` line.
- Delete the middle line and only that line goes; the count drops with it, `3개` → `2개`.

**When `showList()` redraws, it gives every button a fresh number.**

---

## Day 2 · 24–30 min — Assembly: web-week10, then the lab

```text
guestbook.html  2 lines under #list (#empty · #count)  ← ex06
guestbook.js    const empty · count (list: Week 9)     ← ex06
                let items = [];                        ← ex01
                showList(): clear · for · li           ← ex05 · ex02 · ex03
                  + delete template · count · notice   ← ex07 · ex04 · ex06
                submit: 3 append lines → push · showList ← ex04 · ex06
                last line: showList();                 ← ex06
```

[Day 2 lab](lab.md#2일차--다시-그리기와-삭제-버튼-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week10_array_list)

1. Save the ex05–ex07 example folders in `ex/`, change values (until minute 29).
2. Assemble → check at 375 and 1280 and with the server → push → add 3, delete the middle, screenshot `2개`.

**Total explanation: 4+6+7+7+6 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week10/guestbook.html
After adding 3 entries, click [삭제] on the middle line
· student01: 안녕하세요 [삭제]
· student03: 반갑습니다 [삭제]
2개
Include the address bar in the screenshot
```

Keep your real name, student ID, and real email out of the screenshot. A reload empties the list, so take it right on that screen.

---

## Next Week Preview

Today's list lives **only on screen**. A reload brings back the empty list.

In Week 11 you start a new repository, `web-week11`, from today's files and turn each one-line entry into an **object** holding a name, a message, and a date.
Then you keep it in the browser's `localStorage` so **the list survives a reload**. From then on, check and capture **only at the public address**.
