---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 7"
footer: "Reading Form Input and Displaying Results · submit, value, empty-value message"
---

# Reading Form Input and Displaying Results

In Week 6, you changed the screen **when a button was clicked**.
This week, you change the screen **when a form is submitted**.

```text
my-web/
  guestbook.html  ← <form id="guestbook-form"> · <p id="notice"> · <p id="last">
  guestbook.js    ← New file. submit · preventDefault · value · trim
  README.md       ← Created on the GitHub web UI, then pulled (Day 2)
```

The form you built in Week 3 — the one where we wrote "clicking it only changes the address bar" — finally works today.

---

# Day 1 — Handling Form Submission in Your Own Code

`30 min explanation & demo → 60 min lab`

1. Revisit the Week 3 form
2. `addEventListener('submit')` and `event.preventDefault()`
3. Reading values with `value` and `trim()`
4. Displaying results, empty-value messages, `focus()`, `reset()`
5. Week 8 midterm hands-on exam released

---

## Day 1 · 0–5 min — Revisit the Week 3 Form

```html
<form>
  <label for="name">이름</label> <input id="name" type="text">
  <label for="email">이메일</label> <input id="email" type="email">
  <textarea id="message" rows="4"></textarea>
  <button type="submit">남기기</button>
</form>
```

- This is the form you built in Week 3. Right now, pressing **[남기기]** appends a `?` to the address and reloads the page back to the top.
- That happens because the browser tries to **send** the form. Even with no destination (no server), it still changes the address and reloads.
- Today you do two things: **stop** that default behavior, and **capture the input values in your own code**.
- Start by giving `<form>` an `id="guestbook-form"`. You have to be able to find it before you can hand it a listener.

---

## Day 1 · 5–12 min — addEventListener('submit') and preventDefault

```js
form.addEventListener('submit', function (event) {
  event.preventDefault();
});
```

- `'submit'` takes the place of Week 6's `'click'`. The way you hand off the listener is exactly the same.
- `submit` fires both when you press **[남기기]** and when you hit **Enter** inside an input field.
- The `event` in the parentheses is a name carrying **whatever just happened**.
- `event.preventDefault()` means "don't do what the browser was about to do (change the address and reload)."
- Without this one line, even if the code below runs, the screen jumps straight back to the top.

---

## Day 1 · 12–18 min — Reading Values with value and trim

```js
const nameInput = document.querySelector('#name');

const name = nameInput.value.trim();
```

- `.value` is **whatever text is currently typed** in that field. It works the same for `textarea`.
- `.trim()` returns the value with leading and trailing spaces removed, so a field filled with only spaces still counts as empty.
- Put the line that reads the value **inside** the listener. Each submission needs a fresh read of the current value.
- Misspell it as `.velue` and you get `Cannot read properties of undefined (reading 'trim')`.

---

## Day 1 · 18–24 min — Displaying Results, Empty-Value Messages, focus, reset

```js
  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
```

- **Today's 5-minute grammar note**: `return` means "end this function right here." Without it, the lines below still run even after the message is shown.
- `focus()` moves the cursor into that field, and `form.reset()` clears the form. You clear it **after** reading and displaying the value, not before.
- `guestbook.html` loads `guestbook.js`, and `index.html` loads `app.js`. **Each page has its own single JS file.**

---

## Day 1 · 24–30 min ① — Week 8 Midterm Hands-on Exam Released

| Item | Details |
|---|---|
| Scope | Weeks 2–7 — GitHub Pages, HTML, CSS, DOM, forms |
| Weight | 20 points. 3 points for today's form input and empty-value message |
| Where you work | Not a new repository — build it in `my-web/exam/` and push |
| Released today | [Rubric](../week08_midterm/rubric.md) · [Exam structure](../week08_midterm/exam_structure.md) · [Rehearsal starter](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm/examples/rehearsal_starter) |

- List **add/remove is Week 10**, storage that **survives a reload is Week 11**, and `fetch` is **Week 12** — none of these are in scope.
- Today, during minutes 48–55 of the lab, just open the rehearsal starter to look at it. You solve the questions on Day 2 and on Week 8, Day 1.

---

## Day 1 · 24–30 min ② — Try It Yourself

[Day 1 lab](lab.md#1일차--폼-제출을-받아-화면에-표시하기-60분) · [Walkthrough](walkthrough.md#1일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

1. Add the `id`s and a spot for the result to `guestbook.html`, then link `guestbook.js`.
2. Capture the submission, prevent the reload, read the values, and display them as one `이름: 메시지` line.
3. Show a message and move the cursor if the name is empty, then use `form.reset()` to prepare for the next entry.

**Explanation total: 5+7+6+6+6 = 30 min**

If you get stuck, start with the **first red line** in the Console and a line number like `guestbook.js:7`.

---

# Day 2 — Polishing Both Fields to the End

`30 min explanation & demo → 60 min lab`

1. Create `README.md` on the GitHub web UI, then `git pull`
2. One SSH key (optional, personal laptops)
3. Validating both fields and clearing the message
4. Using `reset` and `focus` to prepare for the next entry
5. Time budget for the rehearsal and the actual exam (60 min)

---

## Day 2 · 0–8 min ① — Today's 8-Minute Git: Creating README on the GitHub Web UI

**Repository page › Add file › Create new file › `README.md` › Commit changes**

```bash
git pull
```

```text
Updating a69bc37..3d51f0c
Fast-forward
 README.md | 8 ++++++++
 1 file changed, 8 insertions(+)
 create mode 100644 README.md
```

- A file created on the GitHub website exists **only on GitHub**. You need `git pull` to get it onto your PC.
- This is a review of the `clone`/`pull` you saw in the Week 2 appendix. Until now, you've only ever pushed.
- Skip the pull and commit, and your next push gets rejected. **Pulling comes first.**

---

## Day 2 · 0–8 min ② — Logging In with an SSH Key (Optional, Personal Laptops)

```bash
ssh-keygen -t ed25519 -C "student01@example.com"
```

- An alternative if `Username for 'https://github.com':` pops up every time you push from your personal laptop.
- Paste the contents of `~/.ssh/id_ed25519.pub` into **Settings › SSH and GPG keys › New SSH key**.
- Change the remote address with `git remote set-url origin git@github.com:student01/my-web.git`.
- On lab PCs, keep using **HTTPS + browser login** as before. This section is **not graded.**
- Never send your private key file (`id_ed25519`) to anyone. Don't even display it on screen.

---

## Day 2 · 8–15 min — Validating Both Fields and Clearing the Message

```js
  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }
```

```js
nameInput.addEventListener('input', clearNotice);
```

- Validation runs **top to bottom, in order**. If the name is empty, it stops there and never reaches the message check.
- Write a different message for each field. You should be able to tell which field to fix just from the message.
- `'input'` fires every time the text changes. Only the **event name** changed from Week 6's `addEventListener`.
- Don't add parentheses to `clearNotice` when you hand it off. Writing `clearNotice()` means "run this once, right here."

---

## Day 2 · 15–21 min — Using reset and focus to Prepare for the Next Entry

```js
  clearNotice();
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
```

- Order matters. You clear the form **after** reading and displaying the values. Clear it first, and you display empty values.
- `form.reset()` clears the whole form, including the email field. Use `focus()` to send the cursor back to the name field.
- Leave a second entry and **the first one disappears.** That's because the card is only one line.
- Stacking entries into a list is **Week 10**; making them survive a reload is **Week 11**.

---

## Day 2 · 21–26 min ① — Time Budget for the Rehearsal and the Actual Exam (60 min)

| Time | What you do |
|---|---|
| 0–5 | Read the whole question sheet |
| 5–15 | HTML: skeleton, list, table, form |
| 15–25 | CSS: selectors, the box model, flex, `@media` |
| 25–50 | DOM & forms: click, submit, empty-value message |
| 50–55 | `add → commit → push` |
| 55–60 | Buffer (Pages propagation delay, re-login) |

- On Week 8, Day 1, you solve four rehearsal questions, and **creating the new repository and turning on Pages are also finished that day.**
- On exam day, you just build inside the `my-web/exam/` folder and push.

---

## Day 2 · 21–26 min ② — Where Async and Modules Fit in This Course

```text
Week 7   Form submit → read values → display on screen   ← today
Week 12  fetch a JSON file                                ← async lives here
—        ES modules (import/export), bundlers             ← outside this course's scope
```

- Today's flow — reacting to something that happened on screen — is the foundation for Week 12's `fetch`.
- **Async is covered in Week 12's `fetch`.** You load a single file and render it as cards.
- **Modules (`import`/`export`) are outside this course's scope.** We only ever use a single `<script src="…" defer>`.
- Attaching one JS file per page, the way we do now, is the standard for this semester.

---

## Day 2 · 26–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--두-칸-검사와-안내-문구-다듬기-60분) · [Walkthrough](walkthrough.md#2일차)
Practice page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules

1. Create `README.md` on the GitHub web UI and pull it down with `git pull`.
2. Add validation for the message field, and clear the message as soon as the user types again.
3. Solve one rehearsal question (the form one), push, and take your screenshot from the public URL.

**Explanation total: 8+7+6+5+4 = 30 min**

---

## What to Submit

At the end of Day 2, submit **one** screenshot.

```text
https://student01.github.io/my-web/guestbook.html
Name student01 · Message 안녕하세요, then press [남기기]

Last entry left
student01: 안녕하세요
Capture it with the address bar visible
```

The empty-value message (`이름을 입력하세요.`) is something you verify visually during the lab — it doesn't need to be in the screenshot.
Make sure your real name, student ID, and real email address are not visible in the screenshot.

---

## Next Week Preview

This week fills in the last piece of the **Week 8 midterm scope (Weeks 2–7)**.

Week 8, Day 1 is a **rehearsal** shaped just like the real exam, and Day 2 is the **actual 60-minute exam**.
For the actual exam, you don't create a new repository — you work inside the `my-web/exam/` folder and push.
The rubric and rehearsal starter were released today, so read them before you come.
