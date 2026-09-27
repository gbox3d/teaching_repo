---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 6"
footer: "DOM · Events · Browser CRUD · Click Counter and Dark Mode"
---

# DOM, Events, and Browser CRUD

Week 5 code ran **once**, when the page loaded.
This week we write code that runs **when a button is clicked**.

```text
my-web/
  index.html   ← 2 buttons and <p id="count">
  app.js       ← querySelector · textContent · addEventListener
  styles.css   ← body.dark rule (Day 2)
```

Do this work on the `dark-mode` branch and merge it into main at the end of Day 2.

---

# Day 1 — A Page That Changes When You Click

`30 min explanation & demo → 60 min lab`

1. Create the feature branch `dark-mode`
2. Are HTML and the DOM the same thing?
3. Find elements with `querySelector`
4. Change text with `textContent`
5. `addEventListener('click')` and the click count

---

## Day 1 · 0–5 min — Today's 5-Minute Git: Feature Branch dark-mode

```bash
git pull
git switch -c dark-mode
```

```text
Switched to a new branch 'dark-mode'
```

- Same method as the `guestbook` branch in Week 3. `-c` means "create it and switch to it."
- This week's work builds up on this branch. main stays as it is, and **the public page stays as it is too**.
- At the end of Day 2 you switch back to main and `merge` it in. That's when the public page changes.
- Keeping the public page untouched while you build a new feature is the whole point of a branch.

---

## Day 1 · 5–11 min — Are HTML and the DOM the Same Thing?

```html
<p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

```text
The HTML file you wrote  ──read──▶  Element boxes the browser builds (the DOM)
                                        │
                          JavaScript finds one and changes its text
```

- **HTML**: the text you wrote in a file. It stays there once you save it.
- **DOM**: the **element boxes** the browser builds after reading that text. What you see on screen comes from here.
- What DevTools' **Elements** tab shows is the DOM. Changes you make there are not saved to the file.
- Reloading makes the browser read the file again and rebuild the DOM. That's why it goes back to `클릭 0회` (0 clicks).

---

## Day 1 · 11–17 min — Finding Elements with querySelector

```js
const greeting = document.querySelector('#greeting');

console.log(greeting);
```

- `document` is the **whole page**. The browser creates it for you in advance.
- `querySelector('#greeting')` finds and returns the **one** element whose `id` is `greeting`.
- `#` marks an `id` lookup — the same shape as the CSS selectors from Week 4.
- Store what you find in a `const`, and use that name from then on.
- If nothing matches, you get `null`. That's the `Cannot set properties of null` error from Week 5.

---

## Day 1 · 17–22 min — Changing Text with textContent

```js
greeting.textContent = `${greet(name)} ${hello(hour)}`;
```

- `.textContent` is the **text** inside an element.
- Put it on the right of `=` to read it, and **on the left to replace it.**
- The one-line copy-paste template from Week 5 splits into two lines today: first **find it** (`querySelector`), then **change it** (`textContent`).
- What changes is the screen (the DOM), not the HTML file. Reloading brings back the file's original text.

---

## Day 1 · 22–28 min — addEventListener('click') and the Click Count

```js
let count = 0;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
});
```

- You hand the browser a function and say "run this **when this button is clicked**."
- It does not run at the moment you hand it over — only each time the button is pressed does the code inside the braces run.
- Declare `let count` **outside** the function. Inside it, the count would restart at 0 on every click.
- The `() =>` you saw in Week 2's `app.js` was shown only as a pattern to recognize. Our course code writes `function () { }`.

---

## Day 1 · 28–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--클릭하면-바뀌는-페이지-만들기-60분) · [Walkthrough](walkthrough.md#1일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

1. Create today's working branch with `git switch -c dark-mode`.
2. Add a button and `<p id="count">` to `index.html`, then find and change the text in `app.js`.
3. Count the clicks, then deliberately cause both `null` errors and fix them.

**Explanation total: 5+6+6+5+6+2 = 30 min**

Today's commits build up on `dark-mode`. The public page still shows Week 5's screen.

---

# Day 2 — Dark Mode and Reusing a Function

`30 min explanation & demo → 60 min lab`

1. `merge` and cleaning up branches
2. `classList.add / remove / toggle`
3. The `body.dark` rule and `classList.toggle('dark')`
4. One function shared by two buttons
5. Preview: Week 8 midterm hands-on exam

---

## Day 2 · 0–5 min — Today's 5-Minute Git: merge and Branch Cleanup

```bash
git switch main
git merge dark-mode
git push
git branch -d dark-mode
```

```text
Updating e1bf03b..9a76325
Fast-forward
 app.js     | 23 +++++++++++++++++++----
```

- Same order as the `about` branch in Week 2. Switch **back** to main, then merge.
- Push `dark-mode` before merging. That way the final `branch -d` deletes it cleanly.
- The **public page** only changes after you push following the merge. Today's screenshot is that screen.

---

## Day 2 · 5–11 min — classList.add / remove / toggle

```js
document.body.classList.add('dark');
document.body.classList.remove('dark');
document.body.classList.toggle('dark');
```

- A tool for working with the **list of class names** attached to an element.
- `add` only attaches a class, `remove` only detaches one.
- `toggle` **attaches it if missing, detaches it if present.** Perfect for one button that switches something on and off.
- Attaching a class does not change the look by itself. You need a **CSS rule that uses that class.**
- In DevTools' **Elements** panel, you can watch it change to `<body class="dark">`.

---

## Day 2 · 11–17 min — The body.dark Rule and classList.toggle('dark')

```css
body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

```js
darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});
```

- `body.dark` means "when `<body>` has the class `dark`." No space between them.
- `body.dark .card` targets the cards inside it. A space means "descendant of" (the Week 4 selectors).
- JavaScript only attaches or detaches a single class. CSS is what decides the colors.

---

## Day 2 · 17–22 min — One Function Shared by Two Buttons

```js
function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}
```

- Both buttons do the same thing: "add 1 to the count and write it to the screen." Don't write the same code twice.
- Wrap it in a `function`, as you learned in Week 5, and **call** `countUp()` from both listeners.
- If you need to change something, you change it **in one place**. To show `클릭 ${count}번` instead, for example, you edit a single line.
- There is no value to return, so no `return` here — it's a function that only does something, and returns nothing.

---

## Day 2 · 22–27 min — Preview: Week 8 Midterm Hands-on Exam

| Item | Details |
|---|---|
| Scope | Weeks 2–7 — GitHub Pages, HTML, CSS, DOM, forms |
| Weight | 20 points. 3 points for form input and the empty-value message |
| Where you work | Not a new repository — build it in `my-web/exam/` and push |
| Released | The rehearsal starter and rubric are released on **Week 7, Day 1** |

- Today's `querySelector`, `textContent`, and `addEventListener` all appear on the exam as-is.
- List **add/remove is Week 10**, and **storage that survives a reload is Week 11**. Neither is in the midterm scope.
- Once you read form input and display it in Week 7, the whole midterm scope is covered.

---

## Day 2 · 27–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--다크-모드와-함수-재사용-60분) · [Walkthrough](walkthrough.md#2일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud

1. Build a `[다크 모드]` button and a `body.dark` rule, and switch it on and off with `classList.toggle('dark')`.
2. Refactor both buttons to share a single `countUp()` function.
3. Push `dark-mode`, then on main run `merge` → `push` → `branch -d`.

**Explanation total: 5+6+6+5+5+3 = 30 min**

---

## What to Submit

At the end of Day 2, submit **one** screenshot.

```text
https://student01.github.io/my-web/
Screen with a dark background · [인사 바꾸기] [다크 모드]
Card: 반갑습니다. 오늘도 좋은 하루 되세요.
Card: 클릭 3회
Capture it with the address bar visible
```

It should read **1 or more**, not `클릭 0회` (0 clicks) — that's what shows you actually clicked it.
Make sure your real name, student ID, and real email address are not visible in the screenshot.

---

## Next Week Preview

This week you changed the screen when a **button** was clicked.

In Week 7, you change the screen when a **form is submitted**.
That's the exact spot occupied by the **[남기기]** button on the `guestbook.html` form you built in Week 3 — the one we noted back then only changed the address bar and did nothing else.
You'll keep using `addEventListener`, but with `'submit'` instead of `'click'`, and learn `input.value` for reading what's in an input field.
