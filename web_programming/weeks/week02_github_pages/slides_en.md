---
marp: true
theme: default
paginate: true
header: "Web Programming · Week 2"
footer: "GitHub and Public Deployment · push, Pages, branches"
---

# GitHub and Public Deployment

In Week 1, you committed three files **on your own computer**.
This week you push them to GitHub to create **an address anyone can open**, and use a branch to publish different content separately.

```text
Your PC: my-web ── git push ──▶ github.com/student01/my-web
                                       │ GitHub Pages
                                       ▼
                        https://student01.github.io/my-web/
```

---

# Day 1 — Push to GitHub and Go Public

`30 min explanation & demo → 60 min lab`

1. Create a GitHub account and an empty repository.
2. Set a remote (`origin`) and do your first push.
3. Edit and push, and GitHub changes.
4. Create a public address with GitHub Pages.

---

## Day 1 · 0–5 min — Pushing Your PC's Repository to GitHub

```text
Your PC                                  GitHub (internet)
my-web/.git  ──── git push ────▶  github.com/student01/my-web
 commit 1                            commit 1   ← the same history
```

- Git is the **tool** that records history on your PC; GitHub is the **service** that hosts that history.
- Once pushed, other PCs can fetch it too, and Pages gives you a **public address**.
- Before you push, GitHub has nothing. Only saved-but-not-committed files stay behind; **only committed content** goes.

---

## Day 1 · 5–15 min ① — Create a GitHub Account and Empty Repository

1. https://github.com/signup → email, password, username → enter the code from the confirmation email
2. Top right **+ › New repository**
3. Repository name: `my-web` · **Public**
4. Turn **off** Add a README file, .gitignore, and license
5. **Create repository**

Once created, you'll see three command lines under "…or push an existing repository from the command line."
The next two slides show those three lines. Your username appears in the public address, so don't use your real name or student ID.

---

## Day 1 · 5–15 min ② — Remote and origin

```bash
git remote add origin https://github.com/student01/my-web.git
git remote -v
```

```text
origin  https://github.com/student01/my-web.git (fetch)
origin  https://github.com/student01/my-web.git (push)
```

- remote: the **internet repository address** your repository remembers
- `origin`: the name given to that address. By convention, the first remote is `origin`
- Copy the URL from the **HTTPS** tab on the GitHub page. `student01` is your own username.
- This only records the address; nothing is sent yet.

---

## Day 1 · 15–25 min ① — First Push and Browser Login

```bash
git push -u origin main
```

- On your first push: **Connect to GitHub** window → **Sign in with your browser** → **Authorize** in your browser (Git Credential Manager)
- Your login is saved on the PC, so later pushes won't ask again. Never type a password or token into a command.
- `-u`: remembers so that from now on, plain `git push` goes to `main` on `origin`.

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

Refresh the GitHub repository page and you'll see the three files.

---

## Day 1 · 15–25 min ② — Edit and Push, and GitHub Changes

```html
<h1>My First GitHub Page</h1>
```

```bash
git status
git add index.html
git commit -m "change title to My First GitHub Page"
git push
```

- One more step, **`push`**, has been added to Week 1's `add → commit`.
- Open `index.html` on GitHub and you'll see the changed line, with the commit count now at 2.
- If you only save but don't push, GitHub stays unchanged.

---

## Day 1 · 15–25 min ③ — Turning On GitHub Pages

**Settings › Pages › Build and deployment**

1. Source: **Deploy from a branch**
2. Branch: **main** · folder **/(root)** · **Save**
3. Wait about a minute, refresh → **Visit site**

```text
https://student01.github.io/my-web/
```

- The repository name appears at the end of the address. No capital letters or spaces allowed.
- `index.html` must be at the top level to become the first page.
- Every push redeploys the site. Usually 1 minute, sometimes up to 10.

---

## Day 1 · 25–30 min — Try It Yourself

[Day 1 lab](lab.md#1일차--github에-올리고-공개하기-60분) · [Walkthrough](walkthrough.md#1일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

1. Create the three files in a `my-web` folder and commit them (Week 1 review).
2. Create an empty GitHub repository → `git remote add origin` → `git push -u origin main`.
3. Edit the title line, push, then turn on Pages and open the public URL.

**Explanation total: 5+10+10+5 = 30 min**

If you get stuck, start by reading `git status` and `git remote -v`.

---

# Day 2 — Publish an About Page with a Branch

`30 min explanation & demo → 60 min lab`

1. Create a branch and switch to it.
2. Commit and push `about.html` on the branch.
3. Merge into main to reflect it on the public page.

---

## Day 2 · 0–5 min — A Branch Is a Separate Line of Work

```text
main:  [first page] ─ [change title] ──────────────── [merge] ─▶ Pages
                                \                     /
about:                           [add about page] ──┘
```

- Branch: **a separate line of work for content you publish on its own**. `main` is the default branch that exists from the start.
- Committing on `about` leaves `main` unchanged. GitHub also uploads it separately.
- Once done, you go back to `main` and **merge** it in.

---

## Day 2 · 5–15 min ① — Create a Branch and Switch to It

```bash
git branch about
git switch about
git branch
```

```text
* about
  main
```

- `git branch about`: creates the `about` branch. You're still on `main`.
- `git switch about`: switches to `about`. `*` marks the branch you're currently on.
- The files look the same. Commits from now on pile up on `about`.

---

## Day 2 · 5–15 min ② — Add about.html and Commit

```html
<!-- about.html: new file -->
<h1>About</h1>
<p><a href="index.html">Back to home</a></p>

<!-- index.html: one line added -->
<p><a href="about.html">View about page</a></p>
```

```bash
git add .
git commit -m "add about page"
```

The full file is in [Walkthrough Step 12](walkthrough.md#12-abouthtml-추가하고-링크-넣기).

---

## Day 2 · 15–25 min ① — Push the about Branch

```bash
git push -u origin about
```

```text
 * [new branch]      about -> about
branch 'about' set up to track 'origin/about'.
```

Select it from the **branch dropdown** (`main ▾`) at the top left of the GitHub repository page.

| Branch selected | Files shown |
|---|---|
| `main` | index.html · styles.css · app.js |
| `about` | the three files above + **about.html** |

Click **2 Branches** next to the dropdown to see the branch list. Take a screenshot of this.

Don't click the **Compare & pull request** button in the yellow banner. Merging is done on **your own PC** in the next step.

---

## Day 2 · 15–25 min ② — Merge into main and Reflect on Pages

```bash
git switch main
git merge about
git push
```

```text
Updating 911638a..c5fdc17
Fast-forward
 about.html | 17 +++++++++++++++++
 index.html |  1 +
```

- When you `switch main`, `about.html` briefly disappears from the folder. That's normal.
- After merging and pushing, the **View about page** link appears on your public page about a minute later.

---

## Day 2 · 15–25 min ③ — Cleaning Up the Branch (optional)

```bash
git branch -d about
git push origin --delete about
```

```text
Deleted branch about (was c5fdc17).
 - [deleted]         about
```

- A merged branch can be deleted; its commits stay on `main`.
- On GitHub, you can also delete it with the trash icon in the **Branches** list.
- You don't have to delete it. Next week you'll create another branch with a new name anyway.

---

## Day 2 · 25–30 min — Try It Yourself

[Day 2 lab](lab.md#2일차--브랜치로-소개-페이지-올리기-60분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

1. Create the `about` branch and commit `about.html` with the link.
2. `git push -u origin about`, then take a screenshot of the GitHub branch list.
3. Merge and push from `main`, then screenshot the link on the public page.

**Explanation total: 5+10+10+5 = 30 min**

---

## What to Submit

Submit 4 screenshots together at the end of Day 2.

1. The GitHub repository `my-web` showing the three files
2. `https://<your-id>.github.io/my-web/` open in the browser
3. The GitHub branch list showing `about`
4. The public page with **View about page** clicked, showing `about.html` open

Make sure your email and real name aren't visible in the screenshots. Your username can be visible.

---

## Continuing on Another PC — clone and pull

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

```bash
git pull
```

- `clone`: downloads the whole GitHub repository to a new PC (once, the first time).
- `pull`: fetches new commits from GitHub into a folder you already have.
- If you pushed from home, run `git pull` first in the lab room.

---

## Instructor Demo / Optional — Logging In with an SSH Key

```bash
ssh-keygen -t ed25519 -C "student01@example.com"
```

- Paste the contents of the generated `~/.ssh/id_ed25519.pub` into **Settings › SSH and GPG keys › New SSH key**.
- Change the address with `git remote set-url origin git@github.com:student01/my-web.git`, then push.
- This week's lab uses **HTTPS + browser login**. SSH is shown only as a demo; follow the official docs in the README if you'd like to try it.
- Pages can also deploy from a separate branch called `gh-pages`. This week we only use `main` · `/(root)`.

---

## Next Week Preview

Now a single `add → commit → push` updates your public page.

From Week 3, you'll add pages to this `my-web` and learn **semantic HTML and forms**.
Check each week's result at the same address, `https://<your-id>.github.io/my-web/`.
