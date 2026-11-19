---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 6"
footer: "DOM and Events · see the principle through comparison examples, then assemble at the end"
---

# DOM and Click Events

Week 5's code ran **once**, when the page opened. This week the page changes **every time you click**.

Same method as last week: look at **6 comparison examples** one at a time, then **assemble** `index.html`, `styles.css`, and `app.js` in a new repository, `web-week06`, built on last week's files.

- The browser reads the HTML file and builds the **DOM** (element boxes). JS finds those boxes and changes them.
- Results show on screen, in **Console**, and in the **Elements** tab, which is new this week.
- Required edits: six counter lines on Day 1; two CSS values and three event-handler lines on Day 2. Extra comparisons are optional.

---

# Day 1 — The DOM and Clicks

`60 min lecture & demo → 30 min student lab`

1. Example folders — three files: `index.html`, `styles.css`, `app.js`
2. ex01 — HTML file vs. DOM: Elements and page source
3. ex02 — change on open vs. change on click
4. ex03 — counting clicks: keep the variable outside the function

---

## Day 1 · 0–5 min — One example folder, three files

Use the first five minutes to check the pre-supplied folders and server. Each example has the same three file names as your site.

```text
ex01/
  index.html   screen — the spots the example uses
  styles.css   look — a background color on each spot (.card)
  app.js       behavior — this week's ideas live here
```

- Open `index.html`. In `<head>`, `<link>` and `<script src … defer>` load the other two files.
- Edit the code in `app.js`; see the result by reloading `index.html`.
- The names match your site's top-level files. Tell them apart by the path bar above the editor (`ex › ex01`).

**Screen in HTML, look in CSS, behavior in JS — three files in one folder.**

---

## Day 1 · 5–20 min — ex01 The HTML file and the DOM

[examples/day1/ex01/index.html](examples/day1/ex01/index.html) · [styles.css](examples/day1/ex01/styles.css) · [app.js](examples/day1/ex01/app.js)

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

## Day 1 · 20–35 min — ex02 Change on open vs. change on click

[examples/day1/ex02/index.html](examples/day1/ex02/index.html) · [styles.css](examples/day1/ex02/styles.css) · [app.js](examples/day1/ex02/app.js)

```js
message.textContent = '1. 열자마자 바꾼 글자';        // 1. once, on open

btn.addEventListener('click', function () {
    message.textContent = '2. 버튼을 눌러 바꾼 글자';  // 2. on every click
});
```

- No. 1 on open, No. 2 on every click. Same as A·C and B in Week 5 ex01.
- Try: move the No. 2 line below `});`. On open you see text No. 2; the button only logs to the Console.

**Put the changing line inside `addEventListener` and it runs on every click.**

---

## Day 1 · 35–50 min — ex03 Counting clicks: variable outside the function

[examples/day1/ex03/index.html](examples/day1/ex03/index.html) · [styles.css](examples/day1/ex03/styles.css) · [app.js](examples/day1/ex03/app.js)

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

## Day 1 · 50–60 min — Your turn

[Day 1 lab](lab.md#1일차) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

Minutes 50–55: demonstrate a wrong ID and an inside count. Minutes 55–60: lab handoff.

1. Match button IDs: 5 minutes.
2. Write six count/textContent lines in the [ex03 starter](examples/day1/ex03/app.start.js): 15 minutes.
3. Three clicks → 3; reload → 0: 10 minutes.

The completed example's inside variable and console logs are supplied demo code. Prepare files and the repository before class; upload after class.

**Lecture 5+15+15+15+5+5 = 60 min; lab 5+15+10 = 30 min**

---

# Day 2 — Classes, Functions, and Assembly

`60 min lecture & demo → 30 min student lab`

1. ex04 — `classList.add / remove / toggle`
2. ex05 — dark mode: the `body.dark` rule and `toggle('dark')`
3. ex06 — one function for two buttons
4. About the Week 8 midterm practical
5. Assembly — `index.html`, `styles.css`, `app.js` in `web-week06`

---

## Day 2 · 0–20 min — Setup 5 min and ex04 demo 15 min

[examples/day2/ex04/index.html](examples/day2/ex04/index.html) · [styles.css](examples/day2/ex04/styles.css) · [app.js](examples/day2/ex04/app.js)

```css
.on { background-color: gold; }
```

```js
box.classList.add('on');      // 1. adds it; no change if already there
box.classList.remove('on');   // 2. removes it; no change if not there
box.classList.toggle('on');   // 3. removes if there, adds if not
```

- In Elements, `class="on"` appears and disappears on the `<div id="box">` line.
- Try: change only the color of `.on` in `styles.css`. `app.js` is the same, but the color changes.

**CSS rules decide the look; JS only adds and removes the class name.**

---

## Day 2 · 20–35 min — ex05 Dark mode: one class on body

[examples/day2/ex05/index.html](examples/day2/ex05/index.html) · [styles.css](examples/day2/ex05/styles.css) · [app.js](examples/day2/ex05/app.js)

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
- Try: delete rule 2 in `styles.css`. Only the card stays white (a descendant selector, like `nav a` in Week 4).

The home page supplies `body.dark` rules for h1, h2, and nav a (`#a7c5ff`), and footer (`#c8d4eb`). Elements with their own color do not inherit the body color.

---

## Day 2 · 35–50 min — ex06 One function for two buttons

[examples/day2/ex06/index.html](examples/day2/ex06/index.html) · [styles.css](examples/day2/ex06/styles.css) · [app.js](examples/day2/ex06/app.js)

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

## Day 2 · 50–55 min — About the Week 8 midterm practical

- Week 8 is an individual midterm practical. Questions come from a problem bank built from Weeks 1–7 lab submissions, with the values changed.
- The problem bank is already public: [Week 8 examples](../week08_midterm/examples/README.md). Each problem has starter files, the task, and what to check.
- Answers are not published. Doing each week's lab **yourself** is the practice.
- You may look at the course materials during the exam. Scope: Pages, HTML, CSS, DOM, and W3.CSS (through Week 7).
- Adding and deleting list items is Week 10; keeping data after reload is Week 11.

**Each week's lab is your exam prep.**

---

## Day 2 · 55–60 min — Assembly: web-week06, then the lab

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

[Day 2 lab](lab.md#2일차) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

1. Change two supplied dark-mode CSS values: 5 minutes.
2. Connect three toggle/countUp lines in the [home starter](examples/day2/web-week06/app.start.js): 10 minutes.
3. Check both buttons at 375/1280px: 10 minutes; capture: 5 minutes.

HTML, greet, hello, countUp, and listener skeletons are supplied. Do not rewrite the whole app.js.

**Lecture 5+15+15+15+5+5 = 60 min; lab 5+10+10+5 = 30 min**

---

## What to Submit

Submit **one** screenshot from localhost or a file URL during class. Commit and push after class, then check this public URL.

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

In Week 7 you restyle today's guestbook using W3.CSS: a CDN stylesheet and classes for inputs, buttons, cards, and navigation.
The form behavior is supplied. Keep the IDs used by JavaScript while changing the visual classes.
