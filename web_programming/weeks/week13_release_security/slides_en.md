---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 13"
footer: "Security, Accessibility, and Release Checks · textContent, alt·label, final README"
---

# Security, Accessibility, and Release Checks

By Week 12 you had built four pages. This week you **stop adding features and audit them**.

```text
How is typed text inserted? ── textContent  (shown as plain text)
Do images and inputs have text? ── alt · label for
Do all the links open? ── 404 · Console · 375px
What you hand in ── final README + 3 screenshots
```

---

# Day 1 — Audit and Fix the Pages

`30 min explanation & demo → 60 min lab`

1. Today's syntax, 5 min — `Number` · `isNaN` · `getFullYear`
2. Inserting as text vs. inserting as HTML
3. What not to put in a public repository
4. Two accessibility basics — `alt` and `label for`
5. Audit order — links → Console → 375px

---

## Day 1 · 0–5 min — Today's Syntax: Number and isNaN

```js
const text = yearInput.value.trim();
const year = Number(text);
if (text === '' || isNaN(year)) { … }
const thisYear = new Date().getFullYear();
```

- `Number('2023')` → `2023`, `Number('twenty twenty-three')` → `NaN` (not a number)
- `isNaN(value)`: `true` if the value is `NaN`. This filters out non-numeric input.
- `new Date().getFullYear()`: pulls just the **year** out of today's date. In 2026, this is `2026`.
- Same order as the Week 7 form: `preventDefault` → `trim` → notice and `return` → write to the screen.

---

## Day 1 · 5–11 min — Inserting as Text vs. Inserting as HTML

```js
output.textContent = input.value;   // <b>Hi</b> shown as plain text
output.innerHTML = input.value;     // Hi shown in bold
```

- Same input, same spot — only **one word** is different.
- `innerHTML` **interprets** the text it receives **as HTML**. Tags someone else typed run on your page.
- So when you show typed text, use `textContent`.
- Use `innerHTML` only to **clear a list** (`innerHTML = ''`), as in Week 10.
- Check the `li.textContent = …` line in your own `guestbook.js` directly.

---

## Day 1 · 11–15 min — What Not to Put in a Public Repository

| Don't include | Use instead |
|---|---|
| Real name, student ID, phone number | `student01` |
| A real email address | `student01@example.com` |
| Passwords or login keys | Don't write these down at all |

- Your repository is **Public**. A value that's ever been committed stays in history even after you delete it.
- The same rule applies to screenshots. Your ID in the address bar is fine to show.
- The values in your info table were always **fictional, for-class information**. Leave them as they are.

---

## Day 1 · 15–21 min — Two Accessibility Basics: alt and label for

```html
<img src="images/profile.png" alt="Profile photo of student01" width="160">

<label for="year">Admission year</label>
<input id="year" type="text">
```

- `alt`: the text read aloud when an image doesn't load. Don't leave it empty.
- The value of `label for` and the `input`'s `id` **must match, character for character**.
- To check: click the label text. If the cursor jumps to the input field, they're connected.
- One more thing — write **link and button text** so it makes sense read on its own, out of context.

---

## Day 1 · 21–27 min — Audit Order: Links → Console → 375px

1. **Click every** nav link on all four pages (there should be no 404s).
2. On each page, check **F12 › Console** for red lines.
3. In **F12 › Device mode** at width **375**, check that nothing overflows sideways.

```text
link.textContent = 'View page';                    ← Week 12: all three cards say the same thing
link.textContent = `View ${projects[i].title}`;    ← Week 13: now you can tell where it goes
```

Follow the order. If you check the Console while a link is still broken, the causes get mixed up.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--페이지-점검하고-입학-연도-계산하기-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

1. Add an admission-year form to `about.html` and use `about.js` to compute how many years it's been.
2. Post `<b>Hi</b>` to the guestbook and check that it's shown as plain text.
3. Fix `alt`, `label for`, and link text, then audit links, Console, and 375px.

**Explanation total: 5+6+4+6+6+3 = 30 min**

If you get stuck, start with the first red line in the Console and the `file (line number)` at its end.

---

# Day 2 — Final README and Presentation Prep

`30 min explanation & demo → 60 min lab`

1. Four kinds of README markdown
2. Adding images to `screenshots/`
3. Pasting your history in with `git log --oneline`
4. Two ways a Pages address gets built
5. The Week 14 3-minute flow and the Week 15 rehearsal announcement

---

## Day 2 · 0–8 min — Four Kinds of README Markdown

```markdown
# Heading
- one list line
[public address](https://student01.github.io/my-web/)
```

- For an image, add `!` before the link. Inside the parentheses, use just the file name, like `screenshots/home.png`.

**Sections to include in the final version**

| Section | Content |
|---|---|
| Public address | `https://<your-id>.github.io/my-web/` |
| Pages | The four pages, one line each |
| Features | Five lines |
| Screens | Three images |
| Tech used · problems & fixes · how it was built | About three lines each |

---

## Day 2 · 8–13 min — The screenshots Folder and Adding Images

```text
my-web/
  screenshots/
    home.png   guestbook.png   projects.png
```

- An image line is a link line with `!` in front. Without the `!`, it becomes a **link** instead of an image.
- Keep file names lowercase, with no Korean characters or spaces.
- `home.png` and `Home.png` are **different files**. This is the most common reason images break on GitHub.
- The two images you took in Week 9 had a three-page nav, so **retake them**. Add `projects.png` for three images total.

---

## Day 2 · 13–18 min — Pasting Your History with git log --oneline

```bash
git log --oneline
```

```text
8f31c4a check guestbook text and fix alt/label
5c0b7e2 add notice text to project cards
2a94d16 load projects.json and draw cards
7e12b05 save the guestbook to localStorage
4d6a893 build add/delete for the guestbook list
```

- Copy the most recent five lines into the README's last section, each with a leading `- `.
- The seven characters at the start differ on every PC. Use **the values on your own screen**.

---

## Day 2 · 18–22 min — Two Ways a Pages Address Gets Built

**Settings › Pages › Build and deployment**

| Source | Files that get published | In this course |
|---|---|---|
| Deploy from a branch · `main` · `/(root)` | Files on the `main` branch | **Course standard** (since Week 2) |
| Deploy from a branch · `gh-pages` | Files on the `gh-pages` branch | Shown briefly in the Week 2 appendix |

- Both ways give the same public address. Only the branch that gets published differs.
- Today, just look at the screen — **don't change anything**. Changing it makes the address 404 for a while.

---

## Day 2 · 22–26 min — The Week 14 3-Minute Presentation Flow

```text
Open the public address → move between pages (nav) → dark mode → form empty-value notice
→ add/delete guestbook entries → list survives a refresh → JSON cards → Commits tab
```

- There's nothing new to build. The presentation is **showing what's already there, in order**.
- Your report is the final `README.md` you write today. There's no separate document to submit.
- Don't explain in words — **click through the screen**. Three minutes is shorter than it sounds.

---

## Day 2 · 26–30 min — Announcing the Week 15 Rehearsal · Try It Yourself

[Day 2 lab](lab.md#2일차--readme-최종판과-발표-준비-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security

1. Write the final `README.md` and add the three `screenshots/`.
2. Push it, then check the repository's front page for broken images.
3. Do one 3-minute rehearsal with a partner.

The Week 15 final-exam rehearsal materials (`rehearsal_starter`) and rubric are released today.

**Explanation total: 8+5+5+4+4+4 = 30 min**

---

## What to Submit

Submit **one** screenshot at the end of Day 2.

- Public address `https://<your-id>.github.io/my-web/guestbook.html`
- **F12 › Device mode, 375px**
- An entry with name `student02` and message `<b>Hi</b>` shows **as plain text, exactly as typed**
- No red lines in **F12 › Console**
- Take the screenshot with the address bar visible

Make sure your screenshot shows no email or real name. Your ID may be visible.

---

## Next Week Preview

`my-web` is now ready to show.

In Week 14, you open this same public address for a **3-minute demo**.
Your report is the final `README.md` you wrote today — there's nothing new to build.
The Week 15 final exam is a solo test that builds the same structure from scratch, in a new folder.
