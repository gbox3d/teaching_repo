---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 5"
footer: "JavaScript · 60 + 30"
---

# JavaScript Data and Functions

Keep Week 4's three pages and custom CSS; display a greeting on the home page.

- Each session: 60 min lecture/demo + 30 min student lab
- Day 1 required: four values in ex03/ex05 and one error repair
- Day 2 required: one condition, one greeting return, one output line
- Keep all ten comparison examples; other edits are demos or optional.

Buttons and screen output are supplied. Use the Console for execution order and errors.

---

# Day 1: Scripts and Values

| Lecture/demo | Time |
|---|---|
| Check prepared files and server | 0–5 min |
| Execution order and defer | 5–15 min |
| let/const | 15–30 min |
| Numbers and strings | 30–45 min |
| Template literals | 45–55 min |
| Lab handoff | 55–60 min |

Then a 30-minute student lab. var and parseInt are optional comparisons.

---

## Day 1, 0–5 min: Preparation Check

Prepare Week 4 files, the new web-week05 repository, and ex01–ex10 before class.
Node.js 24+ and server.mjs are also prepared in advance. No new Git instruction.

```text
ex/ex03/index.html  → open in the browser
ex/ex03/app.js      → edit and save
Screen button      → check the result
F12 > Console      → logs, errors, file:line
```

HTML supplies content, CSS appearance, JavaScript behavior.
Save and reload the page from the same folder.

---

## Day 1, 5–10 min: ex01 Execution Order

[Run ex01](examples/day1/ex01/index.html) · [Notes](examples/day1/ex01/README.md)

```js
console.log('A. 페이지를 열자마자 실행된다');
document.getElementById('btn').addEventListener('click', function () {
    console.log('B. 버튼을 누를 때마다 실행된다');
});
console.log('C. A 바로 다음에 실행된다. B 보다 먼저');
```

Excerpt only; screen output in the actual file is supplied support code.
Initially A, C. Three clicks append B three times.
Registering a click function does not execute it. Students write events in Week 6.

---

## Day 1, 10–15 min: ex02 defer

[Run ex02](examples/day1/ex02/index.html) · [Notes](examples/day1/ex02/README.md)

```html
<script src="app.js" defer></script>
```

- Normal script in head: document.body is null before body is parsed.
- Script at the end of body: body exists.
- Deferred external script: runs after HTML parsing.

Output: `1: null → 2: body → 3: body`.
Instructor removes defer: `1: null → 3: null → 2: body`.
Restore defer afterwards. The output-button connection is supplied.

---

## Day 1, 15–30 min: ex03 let/const

[Run ex03](examples/day1/ex03/index.html) · [Notes](examples/day1/ex03/README.md)

```js
let a = 0;
const b = 0;
// Inside the click function
b = b + 1;
```

let permits reassignment. const does not.
Clicking const produces `Assignment to constant variable.`
The remaining statements in that callback do not run.

Students set a=10 and b=20. Repair const to let, reload, click: 20→21.
var is optional and excluded from required implementation and assessment.

---

## Day 1, 30–45 min: ex04 Numbers and Strings

[Run ex04](examples/day1/ex04/index.html) · [Notes](examples/day1/ex04/README.md)

```js
1 + 2                                    // 3
'1' + 2                                  // '12'
num1.value + num2.value                   // join strings
Number(num1.value) + Number(num2.value)   // add numbers
```

Inputs 1 and 2 produce 12 or 3; inputs 10 and 5 produce 105 or 15.
An input value is a string. Convert with Number before addition.

parseInt('12px') returns 12; Number('12px') returns NaN.
This comparison is optional, not required implementation or assessment.

---

## Day 1, 45–55 min: ex05 Template Literals

[Run ex05](examples/day1/ex05/index.html) · [Notes](examples/day1/ex05/README.md)

```js
const name = 'student01';
const hour = 9;
`안녕하세요, ${name}님! 지금은 ${hour}시입니다.`
'안녕하세요, ${name}님!'
`한 시간 뒤는 ${hour + 1}시입니다.`
```

Backticks evaluate ${}; single quotes keep it literal.
Students set name=student02 and hour=15.
Click the supplied output button: student02 and 15시. The Console's next hour is 16시.

---

## Day 1, 55–60 min: Lab Handoff

[Day 1 lab](lab.md#1일차-30분-실습) · [Walkthrough](walkthrough.md#1일차)

| 30-minute lab | Student work |
|---|---|
| 0–15 min | Four values: a/b in ex03, name/hour in ex05 |
| 15–25 min | Run output buttons; repair const b to let b |
| 25–30 min | Verify 11, 21 and student02, 15시 |

Output support and button connections are supplied.
Students do not modify every comparison example.
Public upload is after-class cleanup.

---

# Day 2: Conditions and Functions

| Lecture/demo | Time |
|---|---|
| Check supplied starter | 0–5 min |
| Comparisons and if | 5–20 min |
| Functions, return, supplied date line | 20–40 min |
| querySelector and textContent | 40–50 min |
| Server requests | 50–55 min |
| Lab handoff | 55–60 min |

Then a 30-minute student lab. HTML wiring and function scaffolding are supplied.

---

## Day 2, 5–10 min: ex06 Comparisons

[Run ex06](examples/day2/ex06/index.html) · [Notes](examples/day2/ex06/README.md)

```js
1 === '1'   // false
12 >= 12    // true
12 > 12     // false
```

A comparison returns true or false. === requires matching type and value.
Use hour >= 12 to include noon in the afternoon.
A single = assigns: if (hour = 12) does not compare hours.

== and lexicographic string comparisons are demos/optional.
== performs applicable type conversions; “checks only the value” is not a general rule.

---

## Day 2, 10–20 min: ex07 if/else

[Run ex07](examples/day2/ex07/index.html) · [Notes](examples/day2/ex07/README.md)

```js
if (hour >= 12) {
    m2 = '오후';
} else {
    m2 = '오전';
}
```

9 is morning; 12 and 15 are afternoon.
An if chain executes the first true branch only.

Demo: ex07 case 3 checks >=18 first and gives evening at 20.
Case 4 checks >=12 first and gives afternoon even at 20.

---

## Day 2, 20–35 min: ex08 Functions and return

[Run ex08](examples/day2/ex08/index.html) · [Notes](examples/day2/ex08/README.md)

```js
function greet(name) {
  return `안녕하세요, ${name}님!`;
}
greet('student01');
```

Defining a function does not execute it. Call it with parentheses.
The parameter name receives the value passed at the call.
return sends a value back to the caller; without it the result is undefined.

Students edit one return expression in greet in the supplied starter.

---

## Day 2, 35–40 min: ex10 Supplied Date Line

[Run ex10](examples/day2/ex10/index.html) · [Notes](examples/day2/ex10/README.md)

```js
const hour = new Date().getHours();
```

Read the hour, from 0 to 23, when the page executes.
Repeated output clicks show that same value; reload to read it again.
Other Date methods are optional comparisons.

During verification only, temporarily set hour to 9, then 15.
Check morning/afternoon and restore the current-time expression.

---

## Day 2, 40–50 min: ex09 Elements and Text

[Run ex09](examples/day2/ex09/index.html) · [Notes](examples/day2/ex09/README.md)

```js
document.querySelector('#greeting').textContent = message;
```

querySelector finds an element using a CSS selector; # means id.
textContent writes text. Even `<b>` is displayed as literal characters.
A missing id returns null, so textContent assignment fails.

Students edit one output expression in the supplied starter.
getElementById and innerText are optional and excluded from required assessment.

---

## Day 2, 50–55 min: Supplied Server

Node.js 24+ and [server.mjs](../../tools/static-server/server.mjs) are prepared before class.

```bash
node server.mjs
```

Open localhost:8000. HTML, CSS, JS, and images are separate requests.
Missing files return 404. Favicon requests and request order can vary.

This week's examples also run from file URLs. Inspect HTTP requests on localhost.
Repair missing preparation first; implementing the server is not a student task.

---

## Day 2, 55–60 min: Three Edits

[Day 2 lab](lab.md#2일차-30분-실습) · [Supplied starter](examples/day2/start/README.md)

| 30-minute lab | Student work |
|---|---|
| 0–18 min | One greet return, one hello condition, one textContent output |
| 18–25 min | Compare hour=9 and 15; restore current time |
| 25–30 min | Verify on localhost and capture |

HTML defer/greeting, date, function scaffolding, message, and logs are supplied.
Do not rewrite the whole app.js.
var, ==, parseInt, and other DOM methods are excluded from required assessment.

---

## Submission and After-Class Cleanup

Make one screenshot during class.

```text
URL: http://localhost:8000/
Card: 안녕하세요, student01님! 좋은 아침입니다.
Console: hour number / matching greeting; no errors
```

The afternoon greeting after noon is also correct.
If unfinished, submit ex01's A/C/B after a click as temporary evidence and finish during the next opening check.
Upload publicly after class; verify the Pages URL afterwards.
Keep real names, student IDs, and real email addresses out of public files and captures.

---

## Handoff to Next Week

Prepare the Week 6 folder from this week's finished files before class.

- Keep three HTML pages, custom CSS, and the image.
- Keep greet(name), hello(hour), and #greeting.
- Keep the supplied server.mjs.
- The static guestbook practices input and does not save messages.

Week 6 adds click events, counts, and dark mode.
Hand off the [finished files](examples/day2/web-week05/index.html), not the starter app.js.
