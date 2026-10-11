---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 6"
footer: "DOM and Events · see the principle through comparison examples, then assemble at the end"
---

# DOM, Events, and Browser CRUD

Week 5's code ran **once**, when the page opened. This week the page changes **every time you click**.

Same method as last week: look at **6 comparison examples** one at a time, then **assemble** `index.html`, `styles.css`, and `app.js` in a new repository, `web-week06`, built on last week's files.

- The browser reads the HTML file and builds the **DOM** (element boxes). JS finds those boxes and changes them.
- Results show on screen, in **Console**, and in the **Elements** tab, which is new this week.
- One file = one idea. The lab is about **changing values** and watching.

---

# Day 1 — The DOM and Clicks

`30 min explanation & demo → 60 min lab`

1. The picker page — one `index.html`, turn on one script line
2. ex01 — HTML file vs. DOM: Elements and page source
3. ex02 — change on open vs. change on click
4. ex03 — counting clicks: keep the variable outside the function

---

## Day 1 · 0–4 min — The picker page: turn on one script line

[examples/day1/index.html](examples/day1/index.html) — all three examples use the same screen (a text spot, a button, a count spot).

```html
<script src="ex01_dom.js"></script>
<!-- <script src="ex02_click_write.js"></script> -->
<!-- <script src="ex03_counter.js"></script> -->
```

- Code lives in the `.js` files; the screen is the one `index.html`. Same as Week 5 Day 2.
- Put the cursor on a line and press **Ctrl+/** (macOS ⌘+/) to turn it on or off. Turn on **one line only**.
- Edit the code in `.js`; see the result by reloading `index.html`.

**One `script` line decides which code is loaded.**

---

## Day 1 · 4–12 min — ex01 The HTML file and the DOM

[examples/day1/ex01_dom.js](examples/day1/ex01_dom.js)

```text
HTML file (page source)  ──read──▶  element boxes (DOM)  ──▶  screen
     unchanged                      JS finds and changes them
```

```js
const message = document.querySelector('#message');
message.textContent = '3. JavaScript 가 바꾼 글자';
```

- **Elements** tab: the DOM right now. It shows the changed text.
- **Page source** (Ctrl+U): the file. It still has the original text.
- Try: change `'#message'` to `'#msg'` → `null` and a red line.

**JS changes the DOM the browser built, not the file.**

---

## Day 1 · 12–20 min — ex02 Change on open vs. change on click

[examples/day1/ex02_click_write.js](examples/day1/ex02_click_write.js)

```js
message.textContent = '1. 열자마자 바꾼 글자';        // 1. once, on open

btn.addEventListener('click', function () {
    message.textContent = '2. 버튼을 눌러 바꾼 글자';  // 2. on every click
});
```

- No. 1 on open, No. 2 on every click. Same as A·C and B in Week 5 ex01.
- Try: move line 2 below `});`. On open you see text No. 2, and the button has nothing to do.

**Put the changing line inside `addEventListener` and it runs on every click.**

---

## Day 1 · 20–28 min — ex03 Counting clicks: variable outside the function

[examples/day1/ex03_counter.js](examples/day1/ex03_counter.js)

```js
let count = 0;                     // 1. outside the function
btn.addEventListener('click', function () {
    count = count + 1;
    countBox.textContent = `클릭 ${count}회`;
    let inside = 0;                // 2. inside the function
    inside = inside + 1;
});
```

- Three clicks: No. 1 is 1·2·3, No. 2 is 1·1·1. The `+ 1` line is the same.
- Reload → back to `클릭 0회`: the DOM and variables are rebuilt.

**To keep counting across clicks, put the variable outside the function.**

---

## Day 1 · 28–30 min — Your turn

[Day 1 lab](lab.md#1일차--dom-과-클릭-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud)

1. New folder `web-week06` with last week's files; today's four files in `ex/`.
2. ex01–ex03 — turn on one line, change values. Say what will change first.
3. Create the new repository `web-week06`, push, and turn on Pages.

**Total explanation: 4+8+8+8+2 = 30 min**

---

# Day 2 — Classes, Functions, and Assembly

`30 min explanation & demo → 60 min lab`

1. ex04 — `classList.add / remove / toggle`
2. ex05 — dark mode: the `body.dark` rule and `toggle('dark')`
3. ex06 — one function for two buttons
4. About the Week 8 midterm practical
5. Assembly — `index.html`, `styles.css`, `app.js` in `web-week06`

---

## Day 2 · 0–7 min — ex04 classList: add and remove a class

[examples/day2/ex04_classlist.html](examples/day2/ex04_classlist.html) · [ex04_classlist.js](examples/day2/ex04_classlist.js)

```css
.on { background-color: gold; }
```

```js
box.classList.add('on');      // 1. adds it; no change if already there
box.classList.remove('on');   // 2. removes it; no change if not there
box.classList.toggle('on');   // 3. removes if there, adds if not
```

- In Elements, `class="on"` appears and disappears on the `<div id="box">` line.
- Try: change only the color in `.on`. JS is the same, but the color changes.

**CSS rules decide the look; JS only adds and removes the class name.**

---

## Day 2 · 7–14 min — ex05 Dark mode: one class on body

[examples/day2/ex05_dark.html](examples/day2/ex05_dark.html) · [ex05_dark.js](examples/day2/ex05_dark.js)

```css
body.dark { background-color: #222222; color: #eeeeee; }   /* 1 */
body.dark .card { background-color: #222222; }             /* 2 */
```

```js
darkButton.addEventListener('click', function () {
    document.body.classList.toggle('dark');
});
```

- `document.body` is the `<body>` element. Use it directly; no need to find it.
- Try: delete rule 2. Only the card stays white (a descendant selector, like `nav a` in Week 4).

**Write the colors in CSS ahead of time; JS is one line, `toggle('dark')`.**

---

## Day 2 · 14–20 min — ex06 One function for two buttons

[examples/day2/ex06_reuse.html](examples/day2/ex06_reuse.html) · [ex06_reuse.js](examples/day2/ex06_reuse.js)

```js
function countUp() {
    count = count + 1;
    countBox.textContent = `클릭 ${count}회`;
}
// inside both the A and B click functions
countUp();
```

- Mix A and B clicks; the count keeps going as one. To change it, edit the one function.
- Try: `countUp;` (no parentheses) → nothing happens and there's no error. Call with parentheses.

**Write the shared job in one function and call it from several places.**

---

## Day 2 · 20–25 min — About the Week 8 midterm practical

- Week 8 is an **individual midterm practical**. Questions come from a **problem bank** built from Weeks 1–7 lab submissions, **with the values changed**.
- The problem bank is already public: [Week 8 examples](../week08_midterm/examples/README.md). Each problem has starter files, the task, and what to check.
- Answers are not published. Doing each week's lab **yourself** is the practice.
- You may look at the course materials during the exam. Scope: Pages, HTML, CSS, DOM, and forms (through Week 7).
- Adding and deleting list items is Week 10; keeping data after reload is Week 11.

**Each week's lab is your exam prep.**

---

## Day 2 · 25–30 min — Assembly: web-week06, then the lab

```text
index.html  two buttons · #count card              ← ex02 · ex03
styles.css  body.dark, body.dark .card { … }       ← ex05
app.js      four const … = querySelector('#…')     ← ex01
            let count = 0;                          ← ex03 No. 1
            function countUp() { … }                ← ex06
            greeting.textContent = `…`;             ← ex02 No. 1
            hello button: change text + countUp()   ← ex02 No. 2 · ex06
            dark button: toggle('dark') + countUp() ← ex05 · ex06
```

[Day 2 lab](lab.md#2일차--class-와-함수-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud)

1. Save ex04–ex06 `.html` and `.js` in `ex/`, change values (until minute 29).
2. Assemble → check at 375 and 1280 and with the server → push → dark-mode screenshot.

**Total explanation: 7+7+6+5+5 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/web-week06/
Dark screen ─ [인사 바꾸기] [다크 모드]
Card: 반갑습니다. 오늘도 좋은 하루 되세요.
Card: 클릭 2회 (1 or more is fine)
Include the address bar in the screenshot
```

Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

Today the buttons showed **text we wrote in advance**.

In Week 7 you start a new repository, `web-week07`, from today's files and show **text the user types** into the guestbook form.
You keep using today's `addEventListener` and `textContent`, and listen for the form's `submit` instead of `click`.
