---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 3"
footer: "Semantic HTML and Forms · a three-page about-me site"
---

# Semantic HTML and Forms

In Week 2, you published a single-card `index.html`.
This week you grow the same `my-web` into **three pages** and add input fields for a name and a message.

```text
my-web/
  index.html      ← about me (rewritten)
  about.html      ← my info table (rewritten)
  guestbook.html  ← guestbook form (new file)
  images/profile.png
```

`styles.css` and `app.js` stay as files but **are not linked yet**. This week is HTML only.

---

# Day 1 — Skeleton and About-Me Page

`30 min explanation & demo → 60 min lab`

1. Start and end routines (`git pull` / `git clone`)
2. `header` · `nav` · `main` · `footer`
3. Headings, paragraphs, emphasis
4. Links, images, lists

---

## Day 1 · 0–5 min — Today's 5-Minute Git: Start and End Routines

```bash
git pull                                           # continuing on the same PC
git clone https://github.com/student01/my-web.git  # starting on a different PC
```

- From this week on, lab **minutes 0–5 are always one of these two lines**. A review of the Week 2 bonus slide.

```bash
git add .
git commit -m "build about-me page"
git push
```

- Lab **minutes 55–60 are always this**. push → refresh the public address → screenshot.
- On a shared PC, before you leave, clear `git:https://github.com` from **Credential Manager › Windows Credentials**.

---

## Day 1 · 5–10 min — The Page Skeleton: header, nav, main, footer

```html
<body>
  <header> … title and menu … </header>
  <main>   … this page's content … </main>
  <footer> … a closing line … </footer>
</body>
```

- Week 2's single `<main class="card">` block is now **split into four parts**.
- `nav` means a group of links, and it lives inside `header`.
- There is only one `main` per page.
- Only the names are split so far; the page still stacks top to bottom. Styling comes in Week 4.

---

## Day 1 · 10–16 min — Headings h1–h3 and Paragraphs p, strong

```html
<h1>student01's Web Practice Site</h1>
<h2>About</h2>
<p>I am <strong>student01</strong>, learning web programming.</p>
```

- There is **only one** `h1` per page. The larger sections under it are `h2`, and sections under those are `h3`.
- Don't pick `h1` just to make text bigger. Size is handled by CSS in Week 4.
- `p` is a paragraph; `strong` marks important text inside a paragraph.

---

## Day 1 · 16–22 min — Links a href and Images img alt

```html
<a href="about.html">About Me</a>
<img src="images/profile.png" alt="Profile photo of student01" width="160">
```

- For a file in the same folder, write **just the file name** (a relative path). Same as the Week 2 about link.
- Put images in an `images/` folder and refer to them as `images/profile.png`.
- `alt` is the text read aloud when the image can't be shown. Don't just write "photo" or "image."
- A wrong path shows only the `alt` text where the image should be. That's how you check it.

---

## Day 1 · 22–27 min — Lists ul, ol, li

```html
<ul>
  <li>Taking photos</li>
  <li>Board games</li>
</ul>
```

- `ul`: an unordered list (bullets). `ol`: an ordered list (1, 2, 3).
- Each line is one `li`. `li` only goes **inside** `ul` or `ol`.
- The "steps to write" list in Day 2's `guestbook.html` should be an `ol`.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--세-페이지의-뼈대와-자기소개-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

1. Remove Week 2's content and the `link`/`script` lines from `index.html`, and build the four skeleton parts.
2. `h1`, intro paragraph with `strong`, profile image, two menu links.
3. A 3-item hobby `ul`, a `footer`, and the end routine.

**Explanation total: 5+5+6+6+5+3 = 30 min**

Don't open `styles.css` or `app.js` today. Leave the files but remove their link lines.

---

# Day 2 — My Info Table and Guestbook Form

`30 min explanation & demo → 60 min lab`

1. Build a two-column table with `table`
2. `form` · `label` · `input` · `textarea`
3. What `button type="submit"` does right now
4. `guestbook` branch → merge

---

## Day 2 · 0–6 min — Tables: table, tr, th, td

```html
<table>
  <tr><th>Item</th><th>Value</th></tr>
  <tr><td>Username</td><td>student01</td></tr>
</table>
```

- Stack rows (`tr`) inside `table`, and put cells inside each row.
- `th` is a header cell (bold, centered); `td` is a content cell.
- No border is normal for now. Lines and spacing come from CSS in Week 4.
- Don't put a real email, student ID, or phone number in the table. Use fictional info for class.

---

## Day 2 · 6–14 min — form, and label for / input / textarea

```html
<form>
  <label for="name">Name</label>
  <input id="name" type="text">
  <label for="message">Message</label>
  <textarea id="message" rows="4"></textarea>
</form>
```

- `form` is the area that groups input fields.
- `label`'s `for` and `input`'s `id` must **match** so clicking the label moves the cursor into the field.
- `type="text"` is one line, `type="email"` is for email, `textarea` is multiple lines.
- If the cursor doesn't move, compare the spelling of `for` and `id`, including case.

---

## Day 2 · 14–19 min — button type submit, and What Doesn't Happen Yet

```html
<button type="submit">Leave message</button>
```

```text
before clicking: …/guestbook.html
after clicking : …/guestbook.html?      ← only the address bar changes
```

- Right now, clicking it **does nothing visible on screen**. Only a `?` gets added to the end of the address.
- Showing what you typed on screen is done with JavaScript in **Week 7**.
- Today's goal is just "build the input fields correctly."

---

## Day 2 · 19–25 min — Today's 5-Minute Git: the guestbook Branch and 404

```bash
git switch -c guestbook     # create and switch in one step
```

```bash
git switch main
git merge guestbook
git push
```

- `-c` combines Week 2's `git branch` + `git switch` into one line.
- Week 2's last slide said "next week you'll create another branch with a new name" — today is that day.
- If a link is 404, check the **spelling and case of the file name**. `Guestbook.html` opens on your PC but returns 404 on the public address.

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--내-정보-표와-방명록-form-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

1. `git pull` → `git switch -c guestbook`.
2. Rewrite `about.html` as a 2-column, 4-row table, and create a new `guestbook.html`.
3. Match the menu across all three pages, then `merge` → `push` → screenshot from the public address.

**Explanation total: 6+8+5+6+5 = 30 min**

If you get stuck, check the image and link paths on the page first.

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

```text
https://student01.github.io/my-web/guestbook.html
Menu: Home · About · Guestbook
Fields: name · email · message + [Leave message]
Capture it with the address bar visible
```

Make sure your real name, student ID, and real email aren't visible in the screenshot. Your username can be visible.

---

## Next Week Preview

The three pages you built today are unstyled.

In Week 4, you'll empty out `styles.css`, rewrite it, and link it to all three pages,
styling them with colors, boxes, `display: flex`, and `@media`.
Today's `header`, `nav`, `main`, `footer`, `ul`, and `table` become the target of that CSS.
