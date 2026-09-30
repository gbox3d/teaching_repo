---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 5"
footer: "JavaScript Data and Functions · see the principle through comparison examples, then assemble at the end"
---

# JavaScript Data and Functions

Through Week 4, `my-web` changed only in **what you see**. This week is JavaScript.

This week: look at **10 comparison examples** one at a time, then **assemble** `my-web`'s `index.html` and `app.js` at the end.

- JavaScript runs **inside the browser**. It starts running the moment you open the page.
- Check results in two places: the **screen** and **F12 › Console**.
- One file = one idea. Siblings that do the same thing a different way sit side by side.
- The lab is about **changing values** and watching. Guess what will change first, then check.

Same order as last year's examples: a button and `console.log` → a counter → an adder page (two inputs and a button that adds two numbers).

---

# Day 1 — Scripts and Values

`30 min explanation & demo → 60 min lab`

1. ex01 — lines that run on open vs. lines that run on click
2. ex02 — script position: runs the instant it's read; `defer` waits until reading is done
3. ex03 — `let` · `const` · `var`: can you assign again?
4. ex04 — `+` means add or join; an input's `value` is always a string
5. ex05 — template strings: only `${}` inside backticks gets computed

---

## Day 1 · 0–4 min — Where JS Runs: Screen and Console

```text
Screen   ← find an element and change its text (innerText · textContent)
Console  ← console.log(value) prints here. Errors show a red line + file:line
document ← the whole page the browser has loaded
  document.getElementById('output')   ← find the element with id output
  output.innerText = inputName.value + '님 (function)';   ← change the text
```

- Week 1's three languages: HTML is **content**, CSS is **appearance**, JS is **behavior**.
- Code inside `<script>` runs top to bottom, one line at a time.
- `console.log` prints to the Console only. The screen doesn't change.
- Console: right-click › Inspect, or F12 (laptop: Fn+F12; macOS: ⌘+Option(⌥)+I).

**A syntax mistake or undefined name shows a red line. A wrong result alone (ex04's 12) stays silent — check both the screen and the Console.**

---

## Day 1 · 4–10 min — ex01: Run Now vs. Run on Click

[examples/ex01_click.html](examples/ex01_click.html)
Siblings: Console A (open) / D (after A) / B (btn 1, `function`) / C (btn 2, `() =>`)

```js
console.log('A. 페이지를 열자마자 실행된다');
btn1.addEventListener('click', function () {
    console.log('B. 1번 버튼을 누를 때마다 실행된다');
    output.innerText = inputName.value + '님 (function)';
});
```

- On open: A → D. B, C print per click. Button 2's `() => {}` = last year's style.
- Try it: type `student01`, click both buttons → `student01님 (function)` / `(화살표)`.

**A script runs top to bottom, once. `addEventListener`'s code is only registered — it runs later, per click.**

---

## Day 1 · 10–16 min — ex02 Script Position: Read Now, defer Later

[examples/ex02_script_position.html](examples/ex02_script_position.html) · [ex02_script_position.js](examples/ex02_script_position.js)
Siblings: 1. script in head / 2. script at end of body / 3. file in head with `defer`

```text
head <script>        console.log('1. …', document.getElementById('msg'));
head                 <script src="ex02_script_position.js" defer></script>
body                 <p id="msg">p#msg — this text changes if …</p>
body-end <script>    console.log('2. …', document.getElementById('msg'));
```

- Console order: 1 (`null` = found nothing) → 2 → 3. `<p id="msg">` isn't read yet at step 1.
- Try it: uncomment the head line → red error, read `file:line`. Remove `defer` → order becomes 1→3→2.

**A script runs the instant the browser reads that line. `defer` waits until the HTML is fully read.**

---

## Day 1 · 16–21 min — ex03 let · const · var: Reassignable?

[examples/ex03_let_const.html](examples/ex03_let_const.html)
Siblings: 1. `let` / 2. `const` / 3. `var` — each button adds 1

```js
const b = 0;    // once assigned, cannot be assigned again (let a and var c can)
document.getElementById('btn-const').addEventListener('click', function () {
    b = b + 1;  // this line runs on click, and execution stops right here
});
```

- No. 2 → `Uncaught TypeError: Assignment to constant variable.` `ex03_let_const.html:30`. Still shows 0.
- Try it: `const b` → `let b` → No. 2 counts up too. No error when it opened.

**`let` and `var` can be reassigned; `const` can't. The error hits when that line runs; the lines below it never run.**

---

## Day 1 · 21–26 min — ex04 +: Add or Join?

[examples/ex04_plus.html](examples/ex04_plus.html)
Siblings: `1 + 2` / `'1' + '2'` / `'1' + 2` / `Number('1') + 2` / `parseInt('12px') + 1` / inputs No. 6·7

```js
1 + 2                                     // number + number → adds
'1' + 2                                   // one string is enough to join
num1.value + num2.value                   // an input's value is always a string
Number(num1.value) + Number(num2.value)   // convert to numbers, then add
```

- Results: 3 · 12 · 12 · 3 · 13. Types: number · string · string · number · number.
- Try it: fields 1·2 → No. 6 `12`, No. 7 `3`. No. 5 → `Number('12px')` → `NaN` (still a number).

**`+` adds numbers, joins strings. An input's `value` is always a string.**

---

## Day 1 · 26–28 min — ex05 Template Strings: ${} Works Only in Backticks

[examples/ex05_template.html](examples/ex05_template.html)
Siblings: 1. `+` joins / 2. backticks / 3. `${}` in single quotes / 4. `${hour + 1}`

```js
'안녕하세요, ' + name + '님! 지금은 ' + hour + '시입니다.'   // 1
`안녕하세요, ${name}님! 지금은 ${hour}시입니다.`   // wrapped in `
'안녕하세요, ${name}님!'     // wrapped in ' → ${} stays literal text
`한 시간 뒤는 ${hour + 1}시입니다.`   // inside ${} gets computed
```

- No. 1, 2 are the same sentence. In No. 3, `${name}` stays literal; No. 4 shows `10시`.
- Try it: change the `'` in No. 3 to backticks (key below `Esc`). `₩` means switch to English input.

**Only backticks (`` ` ``) compute what's inside `${}`. In quotes, it stays literal text.**

---

## Day 1 · 28–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--스크립트와-값-60분) · [Walkthrough](walkthrough.md#1일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

1. Create `my-web/week05/` and save ex01–ex05 as **Raw** (ex02 needs its `.js` file too).
2. Change at least one value per file and watch how the screen and Console change.
3. Push, then open `https://student01.github.io/my-web/week05/ex01_click.html`.

Git: `git pull` at 0–5 min, `git add .` → `git commit` → `git push` at 55–60 min.
If a result looks wrong, **open the Console first**. Follow the `file:line` to the right of the red line.

**Explanation total: 4+6+6+5+5+2+2 = 30 min**

---

# Day 2 — Conditions and Functions, Then Assembly

`30 min explanation & demo → 60 min lab`

1. Today's Git — `restore` before a commit, `revert` after one
2. ex06 · ex07 — a comparison is `true`/`false`; `if` runs only the first match
3. ex08 — `function`: define · call · `return`
4. ex09 · ex10 — find first, then change; `new Date()` holds the current time
5. Assembly — gather two lines of `my-web`'s `index.html` and `app.js` from the ex files

---

## Day 2 · 0–4 min — Today's Git: restore vs. revert

```bash
git restore app.js   # a mistake only saved, not committed → back to the last commit
git revert HEAD      # a mistake already committed → makes a new commit that undoes it
```

```text
[main e9f3b26] Revert "change greeting text"
 Date: Wed Sep 30 10:41:07 2026 +0900
 1 file changed, 1 insertion(+), 1 deletion(-)
```

- `revert` makes a new commit; `git log --oneline` keeps both.
- If an editor window opens, save and close it with the default message `Revert "…"` as-is.
- `git reset HEAD^` erases history. Doing that after a push makes your local history disagree with GitHub's, so your next `git push` is rejected. After pushing, use `revert` instead.

---

## Day 2 · 4–9 min — ex06 Comparisons: true or false

[examples/ex06_compare.html](examples/ex06_compare.html)
Siblings: `1 == '1'` / `1 === '1'` / `12 >= 12` / `12 > 12` / `'10' > '9'` / `Number('10') > Number('9')`

```js
1 == '1'                     // only checks the value, calls it equal
1 === '1'                    // must match in type (number vs. string) too
12 >= 12                     // greater than or equal
'10' > '9'                   // strings compare from the first character: '1' < '9'
```

- Results: true · false · true · false · false · true. A single `=` is assignment, not comparison.
- Try it: No. 2 → `1 === 1`, No. 4 → `12 > 11` → which turn true?

**A comparison's result is `true`/`false`. `===` needs matching types too. Strings compare from the first character.**

---

## Day 2 · 9–14 min — ex07 if / else: First Match Wins

[examples/ex07_if_else.html](examples/ex07_if_else.html)
Siblings: 1. `if` alone / 2. `if/else` / 3. `else if` (largest first) / 4. No. 3, reordered

```js
if (hour >= 12) {
    m4 = '오후';     // 20 is true here too → the lines below are never checked
} else if (hour >= 18) {
    m4 = '저녁';     // this line can never be reached
}
```

- At 20:00: No. 3 **저녁**, No. 4 **오후**. At 9:00: No. 1 `(담긴 것 없음)`; `else` needs all above false.
- Try it: enter 9 · 12 · 15 · 20 → when do the lines disagree?

**Conditions are checked top-down; only the first true one runs, so order matters.**

---

## Day 2 · 14–19 min — ex08 function: Define · Call · return

[examples/ex08_function.html](examples/ex08_function.html)
Siblings: 1. `greetLog`, no `return` / 2. `greet`, has `return` / 3·4. called with different values

```js
function greetLog(name) { console.log('안녕하세요, ' + name + '님!'); }  // no return
function greet(name) { return `안녕하세요, ${name}님!`; }             // gives a value back
const a = greetLog('student01');    // call: prints to the Console, a becomes undefined
const b = greet('student01');       // call: nothing in the Console, b holds the sentence
```

- Screen No. 1 shows `undefined` ("nothing stored yet"); No. 2 shows the sentence. `name` is the value passed in at the call.
- Try it: add a `return` to `greetLog`. Call `neverCalled();` → one line in the Console.

**Defining just gives a function a name. Calling it with parentheses is what runs it. No `return` means `undefined` comes back.**

---

## Day 2 · 19–24 min — ex09: Find, Then Change

[examples/ex09_dom_write.html](examples/ex09_dom_write.html)
Siblings: 1. `getElementById`+`innerText` / 2. `querySelector`+`textContent` / 3. a tag / 4. `value`

```js
const p1 = document.getElementById('p1');   // find by id (no '#')
const p2 = document.querySelector('#p2');   // find with a CSS selector
p2.textContent = '2. textContent 로 바꿨다';
p3.textContent = '<b>3. 굵게 될까?</b>';        // shown as literal text, not a tag
```

- Click → No. 1, 2 both change (finding method differs). `#` means id (Week 4 ex01). No. 3: `<b>` stays literal; No. 4 uses `value`.
- Try it: `.textContent` on missing `#p9` → `Cannot set properties of null`.

**Find first, then change it. A missing element gives `null`, and `null` can't be changed.**

---

## Day 2 · 24–27 min — ex10 new Date(): The Current Moment

[examples/ex10_date.html](examples/ex10_date.html)
Siblings: `getHours()` · `getMinutes()` · `getFullYear()` · `getMonth()` · `getMonth() + 1` · `getDay()`

```js
const now = new Date();     // a value holding the date and time when this line ran
now.getHours()              // ask the value, "what hour is it?"
now.getMonth()              // month — counted from 0 (January is 0)
now.getMonth() + 1          // the month number people actually read
```

- Opened at 8:47 on Sep 28: 8 · 47 · 2026 · 8 · 9 · 1. `getDay()` gives 0 = Sunday.
- Try it: refresh → new reading. Add a `getSeconds()` line. `my-web`'s `new Date().getHours()` chains the two lines above.

**`new Date()` holds the moment it ran. `.getHours()` is a question you ask that value.**

---

## Day 2 · 27–30 min — Assembly: my-web app.js

```text
<script src="app.js" defer>  <p class="card" id="greeting">  ← ex02 · ex09
const name · const hour = new Date().getHours();  ← ex03 · ex10
function greet(name) { return `안녕하세요, ${name}님!`; }  ← ex08 · ex05
function hello(hour) { if (hour >= 12) … else … }  ← ex07 · ex06
const message = `${greet(name)} ${hello(hour)}`;  ← ex05 · ex08
console.log(hour); console.log(message);  ← ex01
document.querySelector('#greeting').textContent = message;  ← ex09 No. 2
```

[Day 2 lab](lab.md#2일차--조건과-함수-그리고-조립-60분) · [Walkthrough](walkthrough.md#2일차) · [Lab page](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

1. Save ex06–ex10 in `week05/`, change values (until minute 33).
2. Assemble: two lines in `index.html`; empty and rebuild `app.js` in table order.
3. Try both ways to undo → `git push` → capture the card and Console lines.

**Explanation total: 4+5+5+5+5+3+3 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/my-web/
Card: 안녕하세요, student01님! 좋은 아침입니다. (Hello, student01! Good morning.)
F12 Console: two console.log lines (hour as a number / message as a sentence)
Capture it with the address bar, the card, and the Console all visible
```

If you open it after 12:00, you'll see `좋은 오후입니다.` (Good afternoon.) instead. Either one is correct.
If you couldn't finish Day 2, submit a screenshot from `…/my-web/week05/ex01_click.html` showing A, D, B printed in the Console instead.
Keep your real name, student ID, and real email out of the screenshot.

---

## Next Week Preview

Today's `app.js` runs **once**, when the page loads.

In Week 6, you'll bring `addEventListener` from ex01 into `my-web` — code that runs on every click.
It builds on today's `#greeting`, `greet(name)`, and `hello(hour)` to add a "Change Greeting" button and a click counter.
Dark mode joins too, reusing the `.card` color you picked in Week 4.
