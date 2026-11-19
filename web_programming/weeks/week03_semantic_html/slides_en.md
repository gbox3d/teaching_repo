---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 3"
footer: "Semantic HTML and Forms · a three-page about-me site"
---

# Semantic HTML and Forms

Add a static guestbook to Week 2's home and about pages in `my-web`.
Edit personal content and label connections in the supplied HTML.

```text
my-web/
  index.html      ← introduction
  about.html      ← information table
  guestbook.html  ← static form
  images/profile.png
  styles.css  app.js  ← preserved files
```

The home has no CSS or JS link. Only Day 1's about page still uses last week's CSS.
By the end of Day 2, all three pages have no CSS or JS links.

---

# Day 1 — Semantic Structure and Introduction

`60 min lecture/demo → 30 min student practice`

- Lecture: setup 5, structure 15, headings/text 10, links/images 15, lists 10, guidance 5
- Required: open scaffold 5, edit heading/text/alt/hobbies 15, two links 5, check 5
- Supplied: HTML, image, and preserved CSS/JS; distribute before class
- Demo: assemble an empty document and compare incorrect paths
- Optional: compare `ul` with `ol` in the hobby list

---

## Day 1 · 0–5 min — Check Preparation

Prepare `my-web` on `main` and the supplied Day 1 files before class.

- `git pull` on the same PC or `git clone` on a new PC reviews Week 2.
- Use the first five minutes to check files, not start Raw downloads.
- The home scaffold is supplied; about, CSS, and JS come from Week 2.
- Check that `images/profile.png` is available.

Repeat the learned `add`, `commit`, and `push` steps after class.
There is no new Git branch command this week.

---

## Day 1 · 5–20 min — header, nav, main, footer

```html
<body>
  <header>
    <h1>student01's Web Practice Site</h1>
    <nav><a href="about.html">About</a></nav>
  </header>
  <main>… this page's content …</main>
  <footer>… a closing line …</footer>
</body>
```

`header` introduces, `nav` groups links, `main` holds content, and `footer` closes.
This example places `nav` inside `header` and uses one `main`.
The instructor assembles the structure; students locate it in the supplied file.

---

## Day 1 · 20–30 min — Headings and Paragraphs

```html
<h1>student01's Web Practice Site</h1>
<h2>About</h2>
<p>I am <strong>student01</strong>, learning web programming.</p>
<h3>This semester's goals</h3>
```

- The example uses one `h1` page title; `h2` introduces sections.
- `h3` introduces a smaller section within `h2`; see the lecture comparison.
- `p` is a paragraph; `strong` marks important text.
- Required edits: the classroom alias and introduction text.

Text sizes and layout are covered with CSS in Week 4.

---

## Day 1 · 30–45 min — Relative Links and Images

```html
<a href="about.html">About</a>
<img src="images/profile.png" alt="Person icon for student01" width="160">
```

- Use the file name for a page in the same folder.
- Use the image already supplied as `images/profile.png`.
- `alt` describes the image and conveys its meaning without seeing it.
- The instructor demonstrates a bad path, then restores the correct path.

During practice, edit `alt`, check the two home links, and return from About.

---

## Day 1 · 45–55 min — ul, ol, li

```html
<ul>
  <li>Taking photos</li>
  <li>Board games</li>
  <li>Evening walks</li>
</ul>
```

`ul` is unordered; `ol` is ordered.
The `li` items in this example belong inside the list.

Required: replace the supplied hobbies with your own.
Optional: change `ul` to `ol`, observe numbering, and restore `ul`.

---

## Day 1 · 55–60 min — Practice Guidance

[Day 1 lab](lab.md#1차시-실습-30분) · [Walkthrough](walkthrough.md#1차시)

| 30 min student practice | Task |
|---|---|
| 5 min | Open the supplied home scaffold |
| 15 min | Edit heading, paragraph, alt, and hobbies |
| 5 min | Check two links and return from About |
| 5 min | Save, reload, and check image and text |

Preserve the supplied CSS/JS. Upload after class.
Rewriting all HTML is demonstration/review material, not required typing.

---

# Day 2 — Table and Static Guestbook Form

`60 min lecture/demo → 30 min student practice`

- Lecture: setup 5, table 10, form/label 20, inputs/submit 15, links 5, guidance 5
- Required: two table rows 5, three label/control pairs 15, navigation 5, capture 5
- Supplied: about/form HTML and the added home menu link
- Demo: assemble table/form and observe native email validation
- Optional: add one row of fictional information

Use files distributed before class; edit HTML on `main`.

---

## Day 2 · 0–15 min — Setup 5 and Table 10

First check the three HTML files, menu, and image for five minutes.

```html
<table>
  <tr><th>Item</th><th>Value</th></tr>
  <tr><td>Username</td><td>student01</td></tr>
</table>
```

- `tr` is a row, `th` a heading cell, and `td` a content cell.
- The supplied table has two columns and four rows, including headings.
- Required: edit the username and interests rows.
- Keep the fictional email row. Borders come from CSS in Week 4.

---

## Day 2 · 15–35 min — form and label Connections

```html
<form>
  <label for="name">Name</label>
  <input id="name" type="text">
  <label for="message">Message</label>
  <textarea id="message" rows="4"></textarea>
</form>
```

Matching `label for` and control `id` makes a label click focus the control.
Temporarily empty the three `for` values, then restore them and compare.
Keep the three pairs: `name`, `email`, and `message`.

---

## Day 2 · 35–50 min — Input Types and Native Submission

```html
<input id="email" type="email">
<button type="submit">Leave message</button>
```

- Use single-line `text`, `email`, and multiline `textarea`.
- An email such as `abc` blocks submission through native validation, not JS.
- There is no `required`, so empty controls are accepted.
- Empty or valid email submits a default GET to this page and resets inputs.
- The URL may end with `?`. No message is added or saved.

Controls have no `name` attributes, so their values are not put in the query.
JS syntax starts in Week 5; guestbook message creation starts in Week 7.

---

## Day 2 · 50–55 min — Three-Page Navigation

```html
<nav>
  <a href="index.html">Home</a>
  <a href="about.html">About</a>
  <a href="guestbook.html">Guestbook</a>
</nav>
```

Check all three links from each page: nine routes in total.
Match file-name spelling and case.

Add only the menu link to your home; preserve your Day 1 content.
Creating and merging a branch is not part of this week's practice.

---

## Day 2 · 55–60 min — Practice Guidance

[Day 2 lab](lab.md#2차시-실습-30분) · [Walkthrough](walkthrough.md#2차시)

| 30 min student practice | Task |
|---|---|
| 5 min | Edit username and interests in two table rows |
| 15 min | Connect three label/control pairs; check focus and email |
| 5 min | Navigate between the three pages |
| 5 min | Capture the local guestbook |

Complete and check the supplied form. Adding or saving messages is not assigned.

---

## Submission and After-Class Upload

Submit one local guestbook screenshot during class.

```text
Local file or class local server: guestbook.html
Menu: Home, About, Guestbook
Fields: name, email, message; submit button
Include the address bar in the screenshot
```

After class, repeat `add`, `commit`, and `push` to update `my-web`.
Public result: `https://<username>.github.io/my-web/guestbook.html`
Review account or publishing problems in the next class's first five minutes.

---

## Handoff to Week 4

Preserve this week's result in `my-web`.

Before the next class, copy the three HTML files, image, CSS, and JS to a new
`web-week04` folder. Do not copy `.git`. Prepare the repository and files in advance.

In Week 4, edit the supplied CSS starter and link it to the three pages.
Learn colors, boxes, flex, and viewport conditions using this week's HTML structure.

Next week's public result: `https://<username>.github.io/web-week04/`
W3.CSS is introduced in Week 7.
