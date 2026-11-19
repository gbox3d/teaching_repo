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

`60 min lecture/demo → 30 min individual lab`

1. Preparation check: files and account (5 min; install and verify the account before class).
2. Set a remote (`origin`) and do your first push.
3. Edit and push, and GitHub changes.
4. Create a public address with GitHub Pages.

Lecture: preparation 5 + GitHub/remote 15 + push 15 + Pages 15 + public paths 5 + handoff 5 min.
Copy the provided files; edit one h1 line. CSS and JS are supplied.

---

## Day 1 · 5–20 min ① — Pushing Your PC's Repository to GitHub

```text
Your PC                                  GitHub (internet)
my-web/.git  ──── git push ────▶  github.com/student01/my-web
 commit 1                            commit 1   ← the same history
```

- Git is the **tool** that records history on your PC; GitHub is the **service** that hosts that history.
- Once pushed, other PCs can fetch it too, and Pages gives you a **public address**.
- Before you push, GitHub has nothing. Only saved-but-not-committed files stay behind; **only committed content** goes.

---

## Day 1 · 5–20 min ② — Create a GitHub Account and Empty Repository

1. Sign in with the account prepared before class; request setup support if needed.
2. Top right **+ › New repository**
3. Repository name: `my-web` · **Public**
4. Turn **off** Add a README file, .gitignore, and license
5. **Create repository**

Once created, you'll see three command lines under "…or push an existing repository from the command line."
The following slides explain remote and push. Your username appears in the public address, so don't use your real name or student ID.

---

## Day 1 · 5–20 min ③ — Remote and origin

```bash
git remote add origin https://github.com/student01/my-web.git
git remote -v
```

```text
origin  https://github.com/student01/my-web.git (fetch)
origin  https://github.com/student01/my-web.git (push)
```

- A remote is a saved repository address; `origin` is its name.
- Copy the HTTPS URL and replace `student01` with your username.
- This records the address. No commits have been sent yet.

---

## Day 1 · 20–35 min ① — First Push and Browser Login

```bash
git push -u origin main
```

- If Git Credential Manager requires authentication, follow its browser sign-in and authorization prompts. Labels can vary by version.
- Saved credentials may skip the login window. Never type a password or token into a command.
- `-u`: remembers so that from now on, plain `git push` goes to `main` on `origin`.

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

Refresh the GitHub repository page and you'll see the three files.

---

## Day 1 · 20–35 min ② — Edit and Push, and GitHub Changes

```html
<h1>내 첫 GitHub 페이지</h1>
```

```bash
git status
git add index.html
git commit -m "제목을 내 첫 GitHub 페이지로 바꾸기"
git push
```

- One more step, **`push`**, has been added to Week 1's `add → commit`.
- Open `index.html` on GitHub and you'll see the changed line, and the title-change commit. A fresh repository following these steps has two commits.
- If you only save but don't push, GitHub stays unchanged.

---

## Day 1 · 35–55 min — GitHub Pages

Settings › Pages › Build and deployment

1. Source: `Deploy from a branch`
2. Branch: `main` · folder `/(root)` · Save
3. Deployment completes → Visit site (up to 10 min)

`https://student01.github.io/my-web/`

- 35–50 min: setup and deployment status.
- 50–55 min: project paths and direct URLs.
- Keep `index.html` at the root; match the path's case.
- A push to main starts another deployment.

---

## Day 1 · 55–60 min — Lab Instructions

[Lab](lab.md#1일차--github에-올리고-공개하기-30분) · [Walkthrough](walkthrough.md#1일차)

| Individual lab | Time |
|---|---:|
| Copy files into my-web; check local commit | 5 min |
| Empty remote repository, remote and push | 10 min |
| Edit one h1 line, commit and push | 5 min |
| Pages, visit button, screenshots 1–2 | 10 min |

The lab totals 30 min. If publication is delayed, check local output and the GitHub commit first.

---

# Day 2 — Publish an About Page with a Branch

`60 min lecture/demo → 30 min individual lab`

1. Create a branch and switch to it.
2. Commit and push `about.html` on the branch.
3. Merge into main to reflect it on the public page.

Lecture: preparation 5 + branch/switch 15 + add file 10 + merge 15 + Pages comparison 10 + handoff 5 min.
Required edits: the supplied introduction and round-trip links, plus Git commands.

---

## Day 2 · 5–20 min ① — A Branch Is a Separate Line of Work

```text
Before: main → [change title] → [add about page] ← about
After:                         [add about page] ← main, about
                               push main → Pages
```

- Branch: **a separate line of work for content you publish on its own**. This lab names the branch with `git branch -M main`.
- Committing on `about` leaves `main` unchanged. GitHub also uploads it separately.
- Once done, you go back to `main` and **merge** it in.

---

## Day 2 · 5–20 min ② — Create a Branch and Switch to It

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

## Day 2 · 20–30 min — Add about.html and Commit

```html
<!-- about.html: new file -->
<h1>소개</h1>
<p><a href="index.html">첫 페이지로 돌아가기</a></p>

<!-- index.html: one line added -->
<p><a href="about.html">소개 페이지 보기</a></p>
```

```bash
git add .
git commit -m "소개 페이지 추가"
```

This is an excerpt. Copy [the provided HTML](examples/day2/about.html), edit one introduction line and check both links. UI literals match the Korean example files.

---

## Day 2 · 30–45 min ① — Push about

```bash
git push -u origin about
```

Use GitHub's branch dropdown to compare files before merging.

| Branch | Files |
|---|---|
| `main` | index.html · styles.css · app.js |
| `about` | the same three files + about.html |

- View all branches → screenshot 3.
- Pages still serves main; it has not changed yet.
- Merge locally in the next step. Do not use the PR button.

---

## Day 2 · 30–55 min — Merge and Publish

```bash
git switch main
git merge about
git push
```

```text
Fast-forward
 about.html | 17 +++++++++++++++++
 index.html |  1 +
```

- 30–45 min: merge demo; 45–55 min: compare branches and Pages.
- Switching to main hides about.html; merging restores it.
- After main is deployed, `소개 페이지 보기` opens the about page.
- If delayed, use local output and commit evidence first.

---

## After Class / Optional — Cleaning Up the Branch (optional)

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
- Save screenshot 3 first. Deletion is optional; continue on main in Week 3.

---

## Day 2 · 55–60 min — Try It Yourself

[Day 2 lab](lab.md#2일차--브랜치로-소개-페이지-올리기-30분) · [Walkthrough](walkthrough.md#2일차)
Lab page: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

1. Create and switch to about: 5 min.
2. Supplied introduction and round-trip links: 10 min.
3. Commit, push about, screenshot 3, merge into main and push: 10 min.
4. Public introduction and screenshot 4: 5 min.

**Individual lab: 30 min.** Branch deletion and SSH are optional.

---

## What to Submit

Week 2 keeps the four-screenshot exception. Submit them together after Day 2.

1. The GitHub repository `my-web` showing the three files
2. `https://<your-id>.github.io/my-web/` open in the browser
3. The GitHub branch list showing `about`
4. The public page with **소개 페이지 보기** clicked, showing `about.html` open

If deployment is delayed, submit local output and the GitHub commit, then add the public view.
Make sure your email and real name aren't visible in the screenshots. Your username can be visible.

---

## After Class / Optional — clone and pull

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

## After Class / Optional — Logging In with an SSH Key

```bash
ssh-keygen -t ed25519 -C "student01@example.com"
```

- Paste the contents of the generated `~/.ssh/id_ed25519.pub` into **Settings › SSH and GPG keys › New SSH key**.
- Change the address with `git remote set-url origin git@github.com:student01/my-web.git`, then push.
- This week's lab uses **HTTPS + browser login**. SSH is outside the required lab; follow the official docs in the README if you'd like to try it.
- Pages can also deploy from a separate branch called `gh-pages`. This week we only use `main` · `/(root)`.

---

## Next Week Preview

Now a single `add → commit → push` updates your public page.

Week 3 continues with the four day2 files on main: **semantic HTML and a static form**. Keep CSS/JS files and remove only their HTML connections.
Prepare files before class; use the 30-minute lab for edits, local checks and screenshots. Upload after class; keep the public address.
