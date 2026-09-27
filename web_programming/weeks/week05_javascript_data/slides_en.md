---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 5"
footer: "JavaScript Data and Functions · variables, if, functions"
---

# JavaScript Data and Functions

Through Week 4, you used HTML and CSS to build **what you see**.
This week you bring `app.js` back to life to **build values and assemble sentences**.

```text
my-web/
  index.html   ← bring back the script line (+ Day 2: <p id="greeting">)
  app.js       ← emptied and rewritten (variables · template strings · if · functions)
  styles.css   ← unchanged from Week 4
```

Day 1 uses **only the Console**. Showing it on screen is Day 2.

---

# Day 1 — Build Values and Check Them in the Console

`30 min explanation & demo → 60 min lab`

1. Bringing back the `script` line, and `console.log`
2. Reading a red error line in the Console (`app.js:6`)
3. Storing strings and numbers in `const`/`let`
4. Building sentences with template strings

---

## Day 1 · 0–5 min — Where JS Runs, and Bringing Back the script Line

```html
<link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script>
```

- Week 1's three languages: HTML is **content**, CSS is **appearance**, JavaScript is **behavior**.
- JavaScript runs **inside the browser**. It starts running when you open the page.
- Bring back the `script` line you removed in Week 3, right before `</head>` in `index.html`.
- `defer` means "run this **after** the HTML has fully loaded."
- **Delete all** of Week 2's counter code in `app.js` and write fresh code today.

---

## Day 1 · 5–12 min — console.log and Console Error Lines

```js
console.log('app.js has run');
```

```text
Uncaught ReferenceError: nmae is not defined      app.js:6
```

- `console.log(value)` prints the value inside the parentheses to the **Console tab**. Nothing on screen changes.
- Open Console with **F12** (or right-click › Inspect) → the **Console** tab.
- `app.js:6` to the right of the red line is the **file name and line number**. Start there.
- `is not defined` means "no such name exists." Usually it's a typo.
- Execution stops at the line with the error. Any `console.log` below it won't print.

---

## Day 1 · 12–20 min — let and const, Numbers and Strings

```js
const name = 'student01';
let hour = 9;

hour = 15;
```

- A variable gives a value a name. Start with `const`; use `let` only when you'll assign a new value later.
- To assign a new value, don't write `let` again. Just write the name and put the new value after `=`.
- Reassigning a `const` gives `Uncaught TypeError: Assignment to constant variable.`
- Text in quotes is a string; text without quotes is a number. `'9'` and `9` are different.
- `=` doesn't mean "equals" — it means **"assign."**

---

## Day 1 · 20–27 min — Building Sentences with Template Strings

```js
const greeting = `Hello, ${name}!`;
console.log(greeting);
console.log(`It is ${hour}:00 now.`);
```

```text
Hello, student01!
It is 15:00 now.
```

- Wrapping text in **backticks** (`` ` ``) lets you insert `${variable}` into a sentence.
- Wrapping in single quotes prints `${name}` **literally**, as plain text. Check the quote type first.
- The backtick key is to the left of `1`, below `Esc`. In Korean input mode, a different character appears there.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--값을-만들어-console에-찍기-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

1. Bring back the `script` line in `index.html` and empty out `app.js`.
2. Build `console.log`, `const name`, and `let hour`, and check them in the Console.
3. Build a greeting sentence with a template string, then make a deliberate typo and read the red error line.

**Explanation total: 5+7+8+7+3 = 30 min**

Today you **don't touch the screen.** Check everything in the Console.

---

# Day 2 — Building a Greeting with if and Functions

`30 min explanation & demo → 60 min lab`

1. Undoing with `git revert HEAD`
2. `if` / `else` and comparisons `>=`, `===`
3. Defining and calling `function`, and `return`
4. Showing one line on screen in `#greeting` with a template snippet

---

## Day 2 · 0–5 min — Today's 5-Minute Git: git revert HEAD

```bash
git revert HEAD
```

```text
[main a519cac] Revert "change greeting text"
 Date: Wed Sep 16 10:24:31 2026 +0900
 1 file changed, 1 insertion(+), 1 deletion(-)
```

- The middle `Date:` line is always added by `git revert`. Your date, time, and hash will differ.
- This command **creates a new commit that undoes** a bad commit.
- So there's just one thing to undo, **commit today's work first**, then commit the wrong sentence separately after.
- If an editor window opens, save and close it with the default message `Revert "…"` as-is.
- `git log --oneline` keeps **both** the original commit and the revert commit.
- `git reset HEAD^` erases history itself. **Don't use it on commits you've already pushed and shared.**

---

## Day 2 · 5–12 min — if / else and Comparisons

```js
const hour = new Date().getHours();

if (hour >= 12) {
  console.log('Good afternoon.');
} else {
  console.log('Good morning.');
}
```

- `if (condition) { } else { }`: the top braces run if the condition holds, otherwise the bottom braces run.
- Comparisons: `>=` greater than or equal · `<=` less than or equal · `===` equal in value. A single `=` means "assign."
- `new Date().getHours()` is **today's copy-paste snippet**. It gives the current hour as a number from 0–23.
- To see both branches, plug in a number directly, like `const hour = 9;`.

---

## Day 2 · 12–19 min — Defining and Calling a function

```js
function hello(hour) {
  if (hour >= 12) {
    return 'Good afternoon.';
  } else {
    return 'Good morning.';
  }
}

console.log(hello(15));
```

- `function name(parameter) { }` gives a name to a piece of work. Defining it alone doesn't run it.
- Adding parentheses after the name, as in `hello(15)`, runs it **at that moment** (calling it).
- `hour` in the parentheses is the value the function receives. The value you pass in at the call goes there.

---

## Day 2 · 19–25 min — return and greet(name)

```js
function greet(name) {
  return `Hello, ${name}!`;
}

const message = `${greet(name)} ${hello(hour)}`;
console.log(message);
```

```text
Hello, student01! Good morning.
```

- `return` is the value a function **gives back**. Store the returned value in a variable to use it again.
- A function with only `console.log` and no `return` gives back `undefined`.
- Join the results of two functions with a template string to build one sentence.

---

## Day 2 · 25–28 min — A One-Line Screen Snippet

```html
<p class="card" id="greeting">Preparing your greeting…</p>
```

```js
document.querySelector('#greeting').textContent = message;
```

- Add one paragraph with `id="greeting"` as the first line inside `<main>` in `index.html`.
- The last line is a **copy-paste snippet**: "replace the text at `#greeting` with `message`."
- What this line means is taught in **Week 6**. Use it as-is for now.
- If the text doesn't change and "Preparing your greeting…" stays there, the line above it has an error.

---

## Day 2 · 28–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--if와-함수로-인사말-만들기-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data

1. Add the `#greeting` paragraph in `index.html` and pick a morning/afternoon greeting with `if`.
2. Build two functions, `greet(name)` and `hello(hour)`, and assemble the sentence.
3. Show it on screen with the one-line snippet and commit; commit a wrong sentence, then undo it with `git revert HEAD`.

**Explanation total: 5+7+7+6+3+2 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/my-web/
Card line: Hello, student01! Good morning.
F12 Console: 10 / Hello, student01! Good morning.
Capture it with the address bar and Console both visible
```

After 12:00, you'll see "Good afternoon." instead. Either one is correct.
If you couldn't finish Day 2, a Day 1 Console screenshot is accepted instead.

---

## Next Week Preview

Today's code runs **once**, when the page loads.

In Week 6, you'll write code that runs **when a button is pressed**.
Today's copy-paste snippet, `document.querySelector` and `textContent`, becomes a proper topic,
and `#greeting`, `greet(name)`, and `hello(hour)` carry over to build a click counter and dark mode.
