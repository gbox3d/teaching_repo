---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 2주차"
footer: "GitHub와 공개 배포 · push, Pages, 브랜치"
---

# GitHub와 공개 배포

1주차에는 세 파일을 **내 컴퓨터**에서 commit했습니다.
이번 주에는 GitHub에 올려 **누구나 여는 주소**를 만들고, 브랜치로 다른 내용을 따로 올립니다.

```text
내 PC: my-web ── git push ──▶ github.com/student01/my-web
                                       │ GitHub Pages
                                       ▼
                        https://student01.github.io/my-web/
```

---

# 1일차 — GitHub에 올리고 공개하기

`30분 설명·시연 → 60분 실습`

1. GitHub 계정과 빈 저장소 만들기
2. remote(`origin`)를 적고 첫 push 하기
3. 고치고 push 하면 GitHub가 바뀐다
4. GitHub Pages로 공개 주소 만들기

---

## 1일차 · 0–5분 — 내 PC의 저장소를 GitHub에 올리면

```text
내 PC                                    GitHub (인터넷)
my-web/.git  ──── git push ────▶  github.com/student01/my-web
 commit 1                            commit 1   ← 같은 기록
```

- Git은 내 PC에 기록을 남기는 **도구**, GitHub는 그 기록을 올려 두는 **서비스**입니다.
- 올려 두면 다른 PC에서도 받을 수 있고, Pages로 **공개 주소**가 생깁니다.
- push하기 전에는 GitHub에 아무것도 없습니다. 저장만 한 파일은 가지 않고 **commit한 것만** 갑니다.

---

## 1일차 · 5–15분 ① — GitHub 계정과 빈 저장소 만들기

1. https://github.com/signup → 이메일·비밀번호·아이디 → 확인 메일의 코드 입력
2. 오른쪽 위 **+ › New repository**
3. Repository name: `my-web` · **Public**
4. **Add a README file**, .gitignore, license는 모두 **끄기**
5. **Create repository**

만들면 "…or push an existing repository from the command line" 아래에 명령 세 줄이 보입니다.
다음 두 슬라이드가 그 세 줄입니다. 아이디는 공개 주소에 들어가므로 실명·학번을 넣지 않습니다.

---

## 1일차 · 5–15분 ② — remote와 origin

```bash
git remote add origin https://github.com/student01/my-web.git
git remote -v
```

```text
origin  https://github.com/student01/my-web.git (fetch)
origin  https://github.com/student01/my-web.git (push)
```

- remote: 내 저장소가 기억하는 **인터넷 저장소 주소**
- `origin`: 그 주소에 붙인 이름. 첫 remote는 관례로 `origin`
- URL은 GitHub 화면의 **HTTPS** 탭에서 복사합니다. `student01`은 본인 아이디입니다.
- 주소를 적어 둘 뿐, 아직 아무것도 보내지 않습니다.

---

## 1일차 · 15–25분 ① — 첫 push와 브라우저 로그인

```bash
git push -u origin main
```

- 처음 push하면 **Connect to GitHub** 창 → **Sign in with your browser** → 브라우저에서 **Authorize** (Git Credential Manager)
- 로그인은 PC에 저장되어 다음 push부터 묻지 않습니다. 비밀번호·토큰을 명령에 적지 않습니다.
- `-u`: 다음부터 `git push`만 쳐도 `origin`의 `main`으로 가게 기억합니다.

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

GitHub 저장소 화면을 새로고침하면 세 파일이 보입니다.

---

## 1일차 · 15–25분 ② — 고치고 push 하면 GitHub가 바뀐다

```html
<h1>내 첫 GitHub 페이지</h1>
```

```bash
git status
git add index.html
git commit -m "제목을 내 첫 GitHub 페이지로 바꾸기"
git push
```

- 1주차의 `add → commit`에 **`push` 한 줄**이 붙었습니다.
- GitHub에서 `index.html`을 열면 바뀐 줄이 보이고, commit 수가 2가 됩니다.
- 저장만 하고 push하지 않으면 GitHub는 그대로입니다.

---

## 1일차 · 15–25분 ③ — GitHub Pages 켜기

**Settings › Pages › Build and deployment**

1. Source: **Deploy from a branch**
2. Branch: **main** · 폴더 **/(root)** · **Save**
3. 1분쯤 기다렸다가 새로고침 → **Visit site**

```text
https://student01.github.io/my-web/
```

- 저장소 이름이 주소 끝에 붙습니다. 대문자·띄어쓰기가 없어야 합니다.
- 맨 위에 `index.html`이 있어야 첫 화면이 됩니다.
- push할 때마다 다시 배포됩니다. 보통 1분, 길면 10분 걸립니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--github에-올리고-공개하기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

1. `my-web` 폴더에 세 파일을 만들고 commit합니다 (1주차 복습).
2. GitHub 빈 저장소 → `git remote add origin` → `git push -u origin main`.
3. 제목 한 줄을 고쳐 push하고, Pages를 켜 공개 URL을 엽니다.

**설명 합계: 5+10+10+5 = 30분**

막히면 `git status`와 `git remote -v`부터 읽습니다.

---

# 2일차 — 브랜치로 소개 페이지 올리기

`30분 설명·시연 → 60분 실습`

1. 브랜치를 만들어 옮겨 가기
2. `about.html`을 브랜치에서 commit·push 하기
3. main에 합쳐 공개 페이지에 반영하기

---

## 2일차 · 0–5분 — 브랜치는 따로 올리는 작업선

```text
main:  [첫 페이지] ─ [제목 바꾸기] ──────────────── [merge] ─▶ Pages
                                \                     /
about:                           [소개 페이지 추가] ──┘
```

- 브랜치: **다른 내용을 따로 올리는 작업선**. `main`은 처음부터 있는 기본 브랜치
- about에서 commit해도 main은 그대로입니다. GitHub에도 따로 올라갑니다.
- 다 되면 main으로 돌아와 **merge**로 합칩니다.

---

## 2일차 · 5–15분 ① — 브랜치 만들고 옮겨 가기

```bash
git branch about
git switch about
git branch
```

```text
* about
  main
```

- `git branch about`: about 브랜치를 만듭니다. 아직 main에 있습니다.
- `git switch about`: about으로 옮겨 갑니다. `*`가 지금 있는 브랜치입니다.
- 파일은 그대로 보입니다. 지금부터의 commit이 about에 쌓입니다.

---

## 2일차 · 5–15분 ② — about.html 추가하고 commit

```html
<!-- about.html: 새 파일 -->
<h1>소개</h1>
<p><a href="index.html">첫 페이지로 돌아가기</a></p>

<!-- index.html: 한 줄 추가 -->
<p><a href="about.html">소개 페이지 보기</a></p>
```

```bash
git add .
git commit -m "소개 페이지 추가"
```

전체 파일은 [따라하기 12단계](walkthrough.md#12-abouthtml-추가하고-링크-넣기)에서 붙여 넣습니다.

---

## 2일차 · 15–25분 ① — about 브랜치 push 하기

```bash
git push -u origin about
```

```text
 * [new branch]      about -> about
branch 'about' set up to track 'origin/about'.
```

GitHub 저장소 화면 왼쪽 위 **브랜치 드롭다운**(`main ▾`)에서 고릅니다.

| 고른 브랜치 | 보이는 파일 |
|---|---|
| `main` | index.html · styles.css · app.js |
| `about` | 위 세 파일 + **about.html** |

드롭다운 옆 **2 Branches**를 누르면 브랜치 목록이 보입니다. 이 화면을 캡처합니다.

노란 배너의 **Compare & pull request** 버튼은 누르지 않습니다. 합치는 것은 다음 단계에서 **내 PC**에서 합니다.

---

## 2일차 · 15–25분 ② — main에 합쳐 Pages에 반영하기

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

- `switch main` 하면 폴더에서 `about.html`이 잠시 사라집니다. 정상입니다.
- merge 뒤 push → 1분쯤 뒤 공개 페이지에 **소개 페이지 보기** 링크가 생깁니다.

---

## 2일차 · 15–25분 ③ — 브랜치 정리하기 (선택)

```bash
git branch -d about
git push origin --delete about
```

```text
Deleted branch about (was c5fdc17).
 - [deleted]         about
```

- merge가 끝난 브랜치는 지워도 commit은 main에 남아 있습니다.
- GitHub에서는 **Branches** 목록의 휴지통 아이콘으로도 지울 수 있습니다.
- 지우지 않아도 됩니다. 다음 주에는 새 이름으로 브랜치를 또 만듭니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--브랜치로-소개-페이지-올리기-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

1. about 브랜치를 만들어 `about.html`과 링크를 commit합니다.
2. `git push -u origin about` 뒤 GitHub 브랜치 목록을 캡처합니다.
3. main에서 merge·push 하고 공개 페이지의 링크를 캡처합니다.

**설명 합계: 5+10+10+5 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 4장을 한 번에 제출합니다.

1. GitHub 저장소 `my-web`에 세 파일이 보이는 화면
2. `https://<아이디>.github.io/my-web/`이 열린 화면
3. GitHub 브랜치 목록에 `about`이 보이는 화면
4. 공개 페이지에서 **소개 페이지 보기**를 눌러 `about.html`이 열린 화면

캡처에 이메일·실명이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 다른 PC에서 이어 할 때 — clone과 pull

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

```bash
git pull
```

- `clone`: GitHub의 저장소를 새 PC에 통째로 내려받습니다 (처음 한 번).
- `pull`: 이미 받은 폴더에 GitHub의 새 commit을 가져옵니다.
- 집에서 push했다면 실습실에서는 먼저 `git pull`을 합니다.

---

## 강의자 시연·선택 — SSH 키로 로그인하기

```bash
ssh-keygen -t ed25519 -C "student01@example.com"
```

- 만들어진 `~/.ssh/id_ed25519.pub` 내용을 **Settings › SSH and GPG keys › New SSH key**에 붙여 넣습니다.
- `git remote set-url origin git@github.com:student01/my-web.git`으로 주소를 바꾼 뒤 push합니다.
- 이번 주 실습은 **HTTPS + 브라우저 로그인**으로 합니다. SSH는 시연으로만 보고, 원하면 README의 공식 문서를 따라 해 봅니다.
- Pages는 `gh-pages`라는 별도 브랜치에서 배포하는 방식도 있습니다. 이번 주는 `main` · `/(root)`만 씁니다.

---

## 다음 주 미리 보기

이제 `add → commit → push` 한 번이면 공개 페이지가 바뀝니다.

3주차부터는 이 `my-web`에 페이지를 늘려 가며 **시맨틱 HTML과 form**을 배웁니다.
매주 결과는 같은 주소 `https://<아이디>.github.io/my-web/`에서 확인합니다.
