---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 1"
footer: "How the Web Runs and Git State"
---

# Week 1
## How the Web Runs and Git State

**Twice a week × 90 min**<br>
Each session: 30 min explanation & walkthrough + 60 min lab

Course site: https://gbox3d.github.io/teaching_repo/webprg/

---

## This Week's Plan

1. **Day 1** — See what the browser receives when you type an address, then build a three-file about-me page.
2. **Day 2** — Record history in a practice folder: from `git init` to 3 commits.

```text
[Screenshot 1] Your about-me page + Status 200 in the course site's Network tab
[Screenshot 2] 3 commit lines from git log --oneline + your practice page
```

You submit these two screenshots. No other files are required.
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

---

<!-- _class: lead -->

# Day 1 · 30 min explanation
## What Does the Browser Receive to Build a Page?

---

## Day 1 · 0–4 min — Reading a URL

```text
https://gbox3d.github.io:443/teaching_repo/webprg/index.html
└─┬─┘   └───────┬──────┘ └┬┘└──────────────┬───────────────┘
scheme        host       port            path
```

- **scheme**: how data is exchanged. `https` for the internet, `file` for files on your PC
- **host**: the name of the computer (server) that holds the file
- **port**: that computer's reception desk number. `https` uses 443, so it's usually omitted
- **path**: where the file lives inside the server

**Question:** if you double-click `index.html` in your own folder, what will the address bar start with?

---

## Day 1 · 4–9 min — Request and Response, 200 and 404

```text
GET  /teaching_repo/webprg/              →  200  received the HTML
GET  /teaching_repo/webprg/nothing.html  →  404  no file at that address
```

- The browser sends a **request** for each address, and the server answers with a **status code + content**.
- `200` means "found it and sent it"; `404` means "no file at that address."
- If the page looks wrong, first check **which request returned 404**. Usually it's a wrong file name or path.
- `200`/`404` are codes **sent by a server**. Files on your own PC (`file://`) don't go through a server, so check these on the course site.

---

## Day 1 · 9–14 min — Three Files: HTML, CSS, JavaScript

| File | Job | In today's example |
|---|---|---|
| `index.html` | content and structure | title `<h1>`, intro paragraph `<p>`, a button |
| `styles.css` | appearance | card look, colors, font weight |
| `app.js` | behavior | click count goes up when you press the button |

- The browser fetches `index.html` first, then fetches the two files it references.
- Splitting things up makes it easier to find what to fix: wrong look → CSS, button not working → JavaScript.
- This week you only **read `app.js` and watch the result**. JavaScript syntax comes in later weeks.

---

## Day 1 · 14–21 min — Open and Edit in VS Code

```html
<link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script>
```

- Seeing these two lines in `index.html`, the browser fetches `styles.css` and `app.js` next.
- Use **File › Open Folder** to open the `week01` folder, then **New File** to create the three files.
- Double-click `index.html` in the file explorer → the address bar shows `file:///…/week01/index.html`.
- Change `<h1>` to your own intro and **save (Ctrl+S)** → **refresh (F5)** the browser.
- If you don't save (a `●` on the tab title), refreshing won't change anything.

---

## Day 1 · 21–27 min — Three DevTools Tabs (F12)

- **Elements**: the current page's HTML. See where `<h1>` sits.
- **Console**: messages left by JavaScript, plus red error lines.
- **Network**: the list of files the browser fetched, with their **Status**.

```text
Name                    Type         Status
webprg/                 document     200
assets/library.css      stylesheet   200
assets/course.js        script       200
nothing.html            document     404
```

Try one error yourself: save with a typo, `href="style.css"` → refresh → the card style disappears
→ check the red line in Console → fix it back to `href="styles.css"` → refresh.

---

## Day 1 · 27–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--세-파일로-내-소개-페이지-만들기-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

1. Create the three files in a `week01` folder and open `index.html` in your browser.
2. Change `<h1>` and the intro paragraph to your own info (use a class alias like `student01`), then save and refresh.
3. On the course site, check `200` in the Network tab and `404` for a missing address.
4. Break the `styles.css` filename once, then fix it back.

**Explanation total: 4+5+5+7+6+3 = 30 min**

If you get stuck, compare the path and filename in the address bar character by character.

---

<!-- _class: lead -->

# Day 2 · 30 min explanation
## Git Records State Changes, Not Files

---

## Day 2 · 0–3 min — Saving and Committing Are Different

- **Saving (Ctrl+S)**: overwrites the file with its current content. The old content is gone.
- **Commit**: records "the state of the folder at this moment" together with a one-line description.
- As records build up, you get a list of what changed and when.

Today you leave three commits in a new folder, `week01-practice`.

```text
① create the title   ② add intro paragraph and link   ③ connect style and script
```

Next week you push the same kind of repository to GitHub.

---

## Day 2 · 3–8 min — `git init`: the Repository and Untracked Files

```bash
git init           # creates .git/ in this folder = the repository itself
git branch -M main # rename the default branch to main
```

```text
$ git status
On branch main
No commits yet
Untracked files:
        index.html
nothing added to commit but untracked files present
```

- `.git/` is the entire history. Working files and history are **different things**.
- Being inside the folder doesn't mean it's recorded. `index.html` is still **untracked**.
- A commit works even without a name/email set. But your PC account name ends up in the record, so we set this at 18–22 min.

---

## Day 2 · 8–13 min — Three Areas

```text
untracked ─┐
           ├─ git add ─▶ staging area ─ git commit ─▶ repository(.git)
modified ──┘             candidate for next commit      confirmed history
 working tree
```

- **working tree**: the files in the folder you're editing now
- **untracked**: a new file Git doesn't know about yet. `git add` registers it for the first time
- **staging area**: holds only what you've chosen for the next commit
- **repository**: where confirmed history from `git commit` piles up
- The same file can have both staged and unstaged changes at once (next slide)

---

## Day 2 · 13–18 min — `git status` Tells You the Answer

```text
Changes to be committed:          ← staging area
        modified:   index.html
Changes not staged for commit:    ← working tree (tracked)
        modified:   index.html
Untracked files:                  ← working tree (not tracked)
        notes.txt
```

- The same `index.html` can appear under **both** sections at once, because a commit records the content **at the moment of `git add`**, not the file itself.
- The note under each heading tells you the command to undo that area. Before the first commit it's `git rm --cached`; after, it's `git restore --staged`.
- Before typing a command, first check **which heading the file is under right now**. (No need to recreate this state on purpose in today's lab.)

---

## Day 2 · 18–22 min — `git config`: Set Your Name for This Repository Only

```bash
git config user.name "student01"
git config user.email "student01@example.com"
```

```text
[main (root-commit) 4701d1b] create the title
 Committer: student <student@student-pc.local>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
```

- A commit **works** even without this. But your PC account name and machine name end up in the record instead.
- **Without** `--global`, this applies only to the repository in this folder. Don't use `--global` on a shared PC.
- It applies per repository, so **set it again** in next week's new folder too.
- Your name stays in every commit's record. Use your class alias, not your real name.

---

## Day 2 · 22–25 min — `git add` and `git commit -m`

```bash
git status
git add index.html
git commit -m "create the title"
```

```text
[main (root-commit) 708c9ec] create the title
 1 file changed, 13 insertions(+)
 create mode 100644 index.html
```

- `git add`: choose this file to **go into the next commit**
- `git commit -m "description"`: confirm the chosen content as history, with a description
- If the message has spaces, wrap it in **quotes**.

---

## Day 2 · 25–27 min — `git log --oneline`

```text
2041aef (HEAD -> main) connect style and script
cfa0792 add intro paragraph and link
708c9ec create the title
```

- The top line is the most recent. The first seven characters are the commit hash, and they differ per PC.
- A good message: `add intro paragraph and link` — shows what changed in one line.
- Messages to avoid: `update`, `final`, `fix1` — they give you no clue later.

---

## Day 2 · 27–29 min — Viewing Changed Lines with `git diff` (optional)

```bash
git diff
```

```text
       <h1>student01's Git Practice</h1>
+      <p>A practice page built one commit at a time.</p>
+      <p><a href="https://gbox3d.github.io/teaching_repo/webprg/">…</a></p>
```

- Lines starting with `+` are the lines **added** this time.
- Today's lab only needs `status → add → commit → log`. Just look at `git diff`, no need to run it.

---

## Day 2 · 29–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--git으로-commit-3개-남기기-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

1. In the `week01-practice` folder: `git init` → `git branch -M main` → `git config`.
2. Commit ① the title → ② intro paragraph and link → ③ style and script connections.
3. Each time: `git status` → `git add` → `git commit -m "..."` → `git log --oneline`.

**Explanation total: 3+5+5+5+4+3+2+2+1 = 30 min**

At the end, capture the 3 commit lines and your practice page in one screenshot.

---

## Week Summary

```text
Web : URL → request → response (200 · 404) → index.html + styles.css + app.js → screen
Git : git init → git config → git status → git add → git commit -m → git log --oneline
```

- Submit: 2 screenshots (1 from Day 1 + 1 from Day 2). No other files are required.
- If the page looks wrong, check the filename and address first; if a commit fails, check `git status` first.
- Next week: add `push` to the `add → commit` you learned today, to make an address anyone can open.
