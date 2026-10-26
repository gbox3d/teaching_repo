---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 7"
footer: "Reading Form Input and Displaying Results · see the principle through comparison examples, then assemble at the end"
---

# Reading Form Input and Displaying Results

In Week 6 a button showed **text we wrote in advance**. This week the guestbook form shows **text the user types**.

Same method as last week: look at **7 comparison examples** one at a time, then **assemble** `guestbook.html` and `guestbook.js` in a new repository, `web-week07`, built on last week's files.

- When a form is sent, the browser **opens the page again**. Stop that, or the result disappears.
- Results show on screen, in the **address bar**, and in **Console**.
- One file = one idea. The lab is about **changing values** and watching.

---

# Day 1 — Form Submit and Input Values

`30 min explanation & demo → 60 min lab`

1. The Week 3 form again — press [남기기] and `?` appears at the end of the address
2. ex01 — form submit and `event.preventDefault()`
3. ex02 — the input's `value`: on open vs. on submit
4. ex03 — `trim()`: cutting spaces at both ends

---

## Day 1 · 0–5 min — The Week 3 form again

`guestbook.html` from last week's files — the form you made in Week 3.

```text
Type a name and message, press [남기기]
  → address: …/guestbook.html?   ← a ? at the end
  → fields empty, page back to start   no red line in Console
```

- It is not an error. The browser tried to **send** the form, so it opened the same file again.
- Today: **stop** that, and **read** what was typed with our own code.

**Sending a form makes the browser open the page again.**

---

## Day 1 · 5–13 min — ex01 Form submit and preventDefault

[examples/day1/ex01_submit.html](examples/day1/ex01_submit.html) · [ex01_submit.js](examples/day1/ex01_submit.js)

```js
form2.addEventListener('submit', function (event) {
    event.preventDefault();          // 2. stop the reopening
    out2.textContent = '2. 제출을 받았다';
});
```

- Form 1 (not stopped): `?` at the end, the changed text is gone. Form 2: it stays.
- `'submit'` takes the place of Week 6's `'click'`. A button press or **Enter** both fire the form's `submit`.
- Turn on Console ⚙ › **Preserve log** and Console lines stay even when the page reopens.

**Stop it with `event.preventDefault()` on the listener's first line, or the result won't stay.**

---

## Day 1 · 13–21 min — ex02 The input's value

[examples/day1/ex02_value.html](examples/day1/ex02_value.html) · [ex02_value.js](examples/day1/ex02_value.js)

```js
const atOpen = nameInput.value;             // 1. once, on open
form.addEventListener('submit', function (event) {
    event.preventDefault();
    const atSubmit = nameInput.value;       // 2. on every submit
    const message = messageInput.value;     // 3. textarea uses value too
});
```

- On first open No. 1 is empty; No. 2 is what is typed now. Same idea as Week 6 ex02 (on open vs. on click).
- Text typed into a textarea is in `value`, not `textContent`.

**The text in a field is `value`. Read it inside the listener.**

---

## Day 1 · 21–28 min — ex03 trim(): cut spaces at both ends

[examples/day1/ex03_trim.html](examples/day1/ex03_trim.html) · [ex03_trim.js](examples/day1/ex03_trim.js)

```js
const raw = nameInput.value;              // 1. [  student01  ]
const trimmed = nameInput.value.trim();   // 2. [student01]
```

- Spaces only: No. 1 is `[   ]`, No. 2 is `[]`. A field with only spaces becomes the empty string `''`.
- A space in the middle (`student 01`) stays. Count spaces inside Console's `[ ]`.
- Drop the parentheses (`.trim`) and you get the function, not a value. Call with parentheses.

**`trim()` returns the value with only the end spaces cut.**

---

## Day 1 · 28–30 min — Your turn

[Day 1 lab](lab.md#1일차--폼-제출과-입력-값-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

1. New folder `web-week07` with last week's files; today's six files (three `.html`·`.js` pairs) in `ex/`.
2. ex01–ex03 — change values. Say what will change first. Turn on Preserve log.
3. Create the new repository `web-week07`, push, and turn on Pages.

**Total explanation: 5+8+8+7+2 = 30 min**

---

# Day 2 — Empty-Field Notices, the Next Entry, and Assembly

`30 min explanation & demo → 60 min lab`

1. The picker page — four examples share one form
2. ex04 — `form.reset()` and `focus()`: getting ready for the next entry
3. ex05 — empty-field check and `return`
4. ex06 — the `'input'` event: every time the text changes
5. ex07 — hand over only the function's name
6. Assembly — `guestbook.html` and `guestbook.js` in `web-week07`

---

## Day 2 · 0–3 min — The picker page: four examples share one form

[examples/day2/index.html](examples/day2/index.html) — a guestbook-style form, the notice spot `#notice`, the result spot `#last`.

```html
<script src="ex04_reset_focus.js"></script>
<!-- <script src="ex05_empty.js"></script> -->
<!-- <script src="ex06_input.js"></script> -->
<!-- <script src="ex07_pass_name.js"></script> -->
```

- Same method as Weeks 5 and 6. Use **Ctrl+/** (macOS ⌘+/) and turn on **one line only**.
- Two lines on: same `const` names clash; the second file errors and stops.

**One `script` line decides which code is loaded.**

---

## Day 2 · 3–9 min — ex04 reset and focus: ready for the next entry

[examples/day2/ex04_reset_focus.js](examples/day2/ex04_reset_focus.js)

```js
// 1. read before emptying → [student01]
console.log(`1. 비우기 전 : [${nameInput.value}] …`);
form.reset();            // empties every field in the form
// 2. read after emptying → []
console.log(`2. 비운 뒤 : [${nameInput.value}] …`);
nameInput.focus();       // 3. cursor to the name field
```

- Read after `reset()` and you get empty text. So **read first, then empty**.
- `focus()` moves the cursor. The next note can be typed right away.

**`reset()` empties the fields and `focus()` moves the cursor. Read before you empty.**

---

## Day 2 · 9–15 min — ex05 Empty-field check and return

[examples/day2/ex05_empty.js](examples/day2/ex05_empty.js)

```js
if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    return;                                  // 1. stop here
}
if (message === '') { … return; }            // 2.
last.textContent = `${name}: ${message}`;    // 3. only when both are filled
```

- Checks go from the top. If both are empty, only notice No. 1 shows.
- Without `return`, the lines below run too and `: 안녕하세요` is left behind.

**If a field is empty, show a notice and stop right there with `return`.**

---

## Day 2 · 15–19 min — ex06 The input event: every time the text changes

[examples/day2/ex06_input.js](examples/day2/ex06_input.js)

```js
// 1. name field — every letter typed or deleted (2. textarea too)
nameInput.addEventListener('input', function () {
    notice.textContent = '';
    console.log('1. 이름 칸 input :', nameInput.value);
});
```

- Type `abc` letter by letter: three No. 1 lines; notice gone after `a`.
- Misspell the event name (`'inptu'`): nothing happens, no red line.

**`'input'` fires every time the text in a field changes.**

---

## Day 2 · 19–23 min — ex07 Hand over only the function's name

[examples/day2/ex07_pass_name.js](examples/day2/ex07_pass_name.js)

```js
function clearNotice() { notice.textContent = ''; }
// 1. call it with parentheses inside function () { }
nameInput.addEventListener('input', function () { clearNotice(); });
// 2. hand over the name only — the browser calls it on every change
messageInput.addEventListener('input', clearNotice);
```

- No. 1 and No. 2 do the same job. Type in either field and the notice goes away.
- Hand it over as `clearNotice()` and it runs once on that line, and that's all. Typing leaves the notice, with no red line.

**To hand over a function, write only its name; to call it, add parentheses.**

---

## Day 2 · 23–26 min — Assembly ① guestbook.html

```text
<head>  <script src="guestbook.js" defer>   ← Week 6 app.js line
<form id="guestbook-form">                  ← ex01 · ex02
delete <p>지금은 눌러도 …</p>, and in its place
  <div id="notice"></div>                   ← ex05 spot
  <h3>마지막으로 남긴 글</h3>
  <div class="card" id="last">…</div>       ← ex05 · .card
```

- One js per page: `index.html` loads `app.js`, `guestbook.html` loads `guestbook.js`.
- `index.html`, `app.js`, `styles.css`, and `about.html` stay as they were in Week 6.

**In HTML, only add the `id`s to find and the spots to write results.**

---

## Day 2 · 26–30 min — Assembly ② guestbook.js, then the lab

```text
const form·nameInput·messageInput·notice·last     ← ex02 · ex05
function clearNotice() { … }                      ← ex07
submit listener + event.preventDefault()          ← ex01 No. 2
const name·message = … .value.trim()              ← ex02 · ex03
if name · if message { notice · focus() · return } ← ex05 · ex04
clearNotice() · one result line · reset() · focus() ← ex07 · ex05 · ex04
two input listeners (clearNotice, name only)       ← ex06 · ex07 No. 2
```

[Day 2 lab](lab.md#2일차--빈값-안내와-다음-입력-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

1. ex04–ex07 (to min 29) → assemble → check → push → screenshot.
2. Week 8 reuses the [problem bank](../week08_midterm/examples/README.md) with new values; today's form too.

**Total explanation: 3+6+6+4+4+3+4 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week07/guestbook.html
Name student01 · message 안녕하세요, then [남기기]
마지막으로 남긴 글
Card: student01: 안녕하세요
Include the address bar in the screenshot
```

The empty-field notice (`이름을 입력하세요.`) is for checking during the lab; it need not be in the screenshot.
Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

Week 8 is the **individual midterm practical**. Day 1 is practice with the problem bank; Day 2 is the practical. The repository is `web-week08`.

The [problem bank](../week08_midterm/examples/README.md) is public. Instead of answers, each problem has a "what to check" list to test yourself.

Right now a second note replaces the first. Keeping a list of notes is Week 10; keeping them after reload is Week 11.
The "async" in this week's folder name is covered with `fetch` in Week 12; modules (`import`/`export`) are outside this course.
