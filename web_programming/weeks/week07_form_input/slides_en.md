---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 7"
footer: "Applied CSS"
---

# Applied CSS

Style cards and navigation, then arrange guestbook posts in a newest-first feed.

- Day 1: W3.CSS classes, cards, navigation and a timeline
- Day 2: style the guestbook feed and check authors, timestamps and post text on mobile
- Each day: **60 min lecture and demo + 30 min lab**

Read and run the supplied form JS. Later lessons reuse its input-processing flow.

---

# Day 1 W3.CSS Basics

| Lecture time | Topic |
|---|---|
| 0–10 min | CDN and CSS classes |
| 10–25 min | ex01 before and after connecting CSS |
| 25–40 min | ex02 inputs and buttons |
| 40–47 min | ex03 cards and mobile navigation |
| 47–55 min | ex03b timeline and post spacing |
| 55–60 min | Classes, IDs, and execution checks |

A 30 min lab follows. Download files and prepare Git before class. Use the first 5 min of the opening block for file/server checks and the last 5 min for lab instructions.

---

## Day 1 · 0–10 min Connect CSS from a CDN

W3.CSS provides styles selected by class names.

```html
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
```

- Add the version-pinned CDN URL to `<head>`.
- Network: Disable cache → reload → confirm `w3.min.css` returns 200.
- Internet access is required. Do not store a library copy in the repo.

[W3.CSS on cdnjs](https://cdnjs.com/libraries/w3-css)

---

## Day 1 · 10–25 min ex01 Before and After

[Before HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex01/before.html) · [After HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex01/index.html) · [Shared JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex01/app.js)

```html
<button id="button" class="w3-button w3-teal">클릭</button>
```

Both buttons have the same classes. The page connected to the CDN receives their styles.

1. Click the button on each page and check the count.
2. The instructor changes `w3-teal` to `w3-blue`; students may try this optionally.
3. Check both the color and the click behavior.

---

## Day 1 · 25–40 min ex02 Inputs and Buttons

[HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex02/index.html) · [Supplied JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex02/app.js)

```html
<input id="name" class="w3-input w3-border" type="text">
<button class="w3-button w3-teal" type="submit">미리보기</button>
```

- `w3-input`: input styling; `w3-border`: border
- `w3-button`: button styling; `w3-teal`: color
- Enter a name and message, then preview. The input values remain.

Change one button color and confirm that the same result appears.

---

## Day 1 · 40–47 min ex03 Cards and Navigation

[HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex03/index.html) · [Notes](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day1/ex03/README.md)

| Classes | Use |
|---|---|
| `w3-container`, `w3-padding` | Content spacing |
| `w3-content`, `w3-card` | Content width and card appearance |
| `w3-bar`, `w3-bar-item`, `w3-button` | Navigation and its items |
| `w3-mobile` | Stack items at widths of 600px or less |

Compare navigation at 375px and 1280px. Both cards remain stacked at all widths. The preview JS is the same as ex02.

---

## Day 1 · 47–55 min Reading a Timeline

[Open the ex03b timeline](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input/examples/day1/ex03b_list)

1. Find the author and time next to the avatar. Read the text below them. The divider marks the start of the next post.
2. Compare the same post at 375px and 1280px. Its lines should wrap while its author stays with the post.
3. Change `.post` padding-block from `0.5rem` to `1rem`. Compare the space between posts.

**55–60 min check** · Identify one styling class and one ID used by the supplied JavaScript.

---

# Day 1 Lab · 30 min

| Time | Task |
|---|---|
| 0–5 min | ex01: compare CDN connection and click behavior |
| 5–10 min | ex02: change a button color or input border |
| 10–15 min | ex03: change navigation or card styling |
| 15–25 min | ex03b: change post spacing and compare 375px with 1280px |
| 25–30 min | Check CDN status 200 and Console |

[Lab](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/lab.md) · [Walkthrough](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/walkthrough.md)

Read the same post at both widths and compare where its lines wrap.

---

# Day 2 Restyle the Existing Guestbook

| Lecture time | Topic |
|---|---|
| 0–10 min | Run the existing guestbook in ex04 |
| 10–20 min | Read the supplied JS flow |
| 20–30 min | Restyle the form in ex05 |
| 30–40 min | Restyle cards and navigation |
| 40–50 min | Confirm identical JS and preserve IDs |
| 50–60 min | Check behavior and the mobile screen |

A 30 min lab follows. Start from the unconverted `guestbook.html`. Within these blocks, reserve the first 5 min for preparation checks and the final 5 min for lab/next-lesson instructions.

---

## Day 2 · 0–10 min ex04 Working Guestbook

[Before HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex04/index.html) · [Supplied JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex04/app.js)

Check the existing behavior before changing its CSS.

1. Submit with an empty name: a notice appears; no item is added.
2. Submit a name and message: one item is added to the list.
3. Submit again: the new post appears above the previous one.
4. After submission, fields clear and focus returns to the name.

Keep this behavior while changing the HTML stylesheet link and classes.

---

## Day 2 · 10–20 min Read the Supplied JS

| Code | Behavior |
|---|---|
| `submit` · `preventDefault()` | Handle submission without reopening the page |
| `.value.trim()` | Read input; remove leading/trailing whitespace |
| Empty-value checks · `return` | Show a notice; stop before adding an item |
| `textContent` · `prepend` | Display author and body as text, then insert the post at the top |
| `reset()` · `focus()` | Restore initial values; focus the name input |
| `input` · `clearNotice` | Clear the notice when typing resumes |

Later lessons reuse this flow. Keep the supplied JS unchanged.

---

## Day 2 · 20–30 min ex05 Restyle the Form

[After HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex05/index.html)

Replace the `styles.css` link with the W3.CSS CDN link.

| Target | Classes |
|---|---|
| Name, email, and message inputs | `w3-input w3-border` |
| Submit button | `w3-button w3-teal` |
| Notice `#notice` | `w3-text-red` |
| List `#list` | Apply `w3-ul example-output feed-list` |

Keep IDs and the `guestbook.js` link. Email is optional and the JS does not read it. If entered, an invalid email format blocks submission in the browser.

---

## Day 2 · 30–40 min Cards and Navigation

Move navigation immediately after the header. Wrap the form/notice and the list in separate sections.

| Target | Classes |
|---|---|
| Navigation | `w3-bar w3-white w3-card` |
| Each navigation item | `w3-bar-item w3-button w3-mobile` |
| main | `w3-content w3-padding` |
| Both sections | `w3-container w3-card w3-white w3-margin-top` |

Change one heading or button color. The remaining mapping is in the [walkthrough](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/walkthrough.md).

---

## Day 2 · 40–50 min Same JS and IDs

[ex04 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex04/app.js) · [ex05 JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/ex05/app.js) · [Site JS](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/web-week07/guestbook.js)

In VS Code: Select for Compare → Compare with Selected.
All three files contain the same code.

```text
IDs selected by JS
guestbook-form · name · message · notice · list
```

JS still finds the same elements after styling changes. Home and About keep their existing CSS. In `shared/examples.css`, the `.post` grid places the avatar beside the text. `.post-body` preserves the author’s line breaks.

---

## Day 2 · 50–60 min Execution Checks

| Check | Expected result |
|---|---|
| Empty name or message | Notice appears; no item added |
| Submit two entries | Newest first, with author, timestamp and body; fields reset |
| 375px screen | Stacked navigation; no horizontal input overflow |
| Network and Console | CDN 200; no example-code errors |

Reloading clears the list. Persistence is covered in Week 11.

Lecture total: **10 + 10 + 10 + 10 + 10 + 10 = 60 min**

---

# Day 2 Lab · 30 min

Work on `guestbook.html`, copied from `guestbook.before.html`.
Keep the completed version as `guestbook.reference.html` for comparison.

| Time | Task |
|---|---|
| 0–5 min | Replace the existing CSS link with the specified CDN |
| 5–18 min | Apply mapped classes; change one color |
| 18–25 min | Check empty inputs, two entries, and 375px |
| 25–30 min | Capture the running page |

[Starter HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/web-week07/guestbook.before.html) · [Reference HTML](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/examples/day2/web-week07/guestbook.html) · [Lab](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/weeks/week07_form_input/lab.md)

---

## Submit One Screenshot

Capture the 375px screen with these items visible:

- The address and the W3.CSS guestbook
- The newer post by `student02` above the post by `student01`
- The button or heading color you changed

Check empty-input notices during the lab. No separate comparison table or source listing is required. Do not use real names, student IDs, or real email addresses.

After class, push, publish with Pages, and check the public URL.

---

## Next Lessons and References

- Week 8: [midterm exercise bank](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm/examples). Check your section’s announcement for the exam scope.
- Week 9: reuse the completed `web-week07` web files, rather than the exam answers.
- Week 10: manage an array list. Week 11: save/restore one form; the full persistent guestbook is a supplied demo.

[W3.CSS inputs](https://www.w3schools.com/w3css/w3css_input.asp) · [Containers](https://www.w3schools.com/w3css/w3css_containers.asp) · [Navigation](https://www.w3schools.com/w3css/w3css_navigation.asp) · [cdnjs](https://cdnjs.com/libraries/w3-css)
