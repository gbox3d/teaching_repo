# 2주차 실습 — GitHub에 올리고 브랜치로 나눠 올리기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

이번 주에는 1주차에 만든 세 파일짜리 페이지를 GitHub에 올리고 공개 주소를 만든다.
2일차에는 브랜치를 만들어 소개 페이지를 따로 올린 뒤 main에 합친다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.

## 1일차 — GitHub에 올리고 공개하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | `my-web` 폴더에 세 파일을 만들고 `git init → add → commit`까지 한다 (1주차 복습) |
| 10–20분 | GitHub 계정을 만들거나 로그인하고 빈 저장소 `my-web`을 만든다 |
| 20–35분 | `git remote add origin` → `git push -u origin main` → 브라우저 로그인 → 저장소에 세 파일 확인 (캡처 1) |
| 35–45분 | 제목 한 줄을 고쳐 `add → commit → push` 하고 GitHub에서 바뀐 줄을 확인한다 |
| 45–55분 | **Settings › Pages**를 켜고 공개 URL을 연다 (캡처 2) |
| 55–60분 | 캡처 2장을 저장하고 `git status`가 clean인지 본다 |

### 1. 세 파일과 첫 commit

새 폴더 `my-web`에 `index.html`, `styles.css`, `app.js`를 만들고 `git init → git branch -M main → git add . → git commit`까지 한다.
[따라하기 1~3단계](walkthrough.md#1-연습-폴더-만들기)를 본다.

- `index.html`의 `<h1>`은 일부러 `내 첫 페이지`로 둔다. 4번에서 고친다.
- `git log --oneline`에 `첫 페이지 만들기` 한 줄이 보이면 다음으로 간다.
- 파일 내용이 기억나지 않으면 [examples/day1](examples/day1)을 열어 옮겨 적되, `<h1>`만 `내 첫 페이지`로 바꾼다.

### 2. GitHub 빈 저장소

GitHub에 로그인하고 **+ › New repository**로 `my-web`을 만든다. [따라하기 4~5단계](walkthrough.md#4-github-계정-만들기)를 본다.

- **Public**, **Add a README file**은 체크하지 않는다. `.gitignore`와 license는 **None**.
- 만든 뒤 화면의 "…or push an existing repository from the command line" 세 줄을 닫지 말고 둔다.
- 아이디에 실명·학번이 들어가지 않는지 본다. 아이디는 공개 주소에 그대로 들어간다.

### 3. remote 연결과 첫 push

저장소 화면의 HTTPS 주소를 복사해 `git remote add origin <URL>`을 하고 `git push -u origin main`을 한다.
[따라하기 6~7단계](walkthrough.md#6-remote-연결하기)를 본다.

- push 전에 `git remote -v`로 주소의 아이디와 저장소 이름이 맞는지 본다.
- **Connect to GitHub** 창이 뜨면 **Sign in with your browser**. 비밀번호·토큰을 터미널에 치지 않는다.
- 저장소 화면을 새로고침해 세 파일이 보이면 **캡처 1**을 저장한다.

### 4. 제목 한 줄 고쳐 push

`<h1>`을 `내 첫 GitHub 페이지`로 바꾸고 `git status → add → commit → push`를 한다. [따라하기 8단계](walkthrough.md#8-제목-한-줄-고치고-push-하기)를 본다.

- 이번에는 `git push`만 친다. 7단계의 `-u`가 기억하고 있다.
- GitHub에서 `index.html`을 열어 바뀐 줄을 확인한다. commit 수가 2가 되어야 한다.
- 바뀌지 않았다면 `git status`를 읽는다. `Your branch is ahead of 'origin/main' by 1 commit`이면 push를 아직 안 한 것이다.

### 5. Pages 켜기

**Settings › Pages › Build and deployment**에서 Branch를 `main` · `/(root)`로 고르고 **Save**한다. [따라하기 9단계](walkthrough.md#9-github-pages-켜기)를 본다.

- 1분쯤 기다렸다가 새로고침해 "Your site is live at …"가 보이면 **Visit site**를 누른다.
- `https://student01.github.io/my-web/`에서 `내 첫 GitHub 페이지`와 방문 버튼이 동작하면 **캡처 2**를 저장한다.
- 주소를 직접 칠 때는 아이디, 저장소 이름, 끝의 `/`를 확인한다.

### 6. 오늘 확인할 것

- [ ] `git remote -v`에 본인 저장소 주소가 두 줄 보인다.
- [ ] GitHub 저장소에 세 파일과 commit 2개가 보인다.
- [ ] 공개 URL에서 `내 첫 GitHub 페이지`가 열린다.
- [ ] 캡처 1·2를 저장했다.

저장소는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 브랜치로 소개 페이지 올리기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | `my-web`을 열고 `git status`가 clean, `git log --oneline`이 두 줄인지 본다 |
| 5–15분 | `git branch about` → `git switch about` → `git branch`에서 `* about` 확인 |
| 15–30분 | `about.html`을 만들고 `index.html`에 링크 한 줄을 넣어 브라우저로 확인한 뒤 commit |
| 30–40분 | `git push -u origin about` → GitHub 브랜치 드롭다운에서 main·about 비교 (캡처 3) |
| 40–50분 | `git switch main` → `git merge about` → `git push` → 공개 페이지의 링크 확인 (캡처 4) |
| 50–55분 | (선택) `git branch -d about`, GitHub에서 브랜치 삭제 |
| 55–60분 | 캡처 4장을 정리해 제출한다 |

### 1. about 브랜치 만들기

`git branch about`, `git switch about`을 하고 `git branch`로 `*`의 위치를 본다. [따라하기 10~11단계](walkthrough.md#10-저장소-다시-열기)를 본다.

- 시작 전 `git status`가 `nothing to commit, working tree clean`이어야 한다. 아니면 먼저 commit한다.
- `Switched to branch 'about'`이 보이고 폴더의 파일은 그대로다.

### 2. 소개 페이지 만들고 commit

`about.html`을 새로 만들고 `index.html`에 `<p><a href="about.html">소개 페이지 보기</a></p>` 한 줄을 넣는다.
[따라하기 12~13단계](walkthrough.md#12-abouthtml-추가하고-링크-넣기)를 본다.

- `about.html`은 `styles.css`만 연결한다. 제목은 `소개`, 문장은 본인 소개 한 줄(실명 없이), `index.html`로 돌아가는 링크를 넣는다.
- 브라우저에서 두 링크가 모두 동작한 뒤에 `git add .` → `git commit -m "소개 페이지 추가"`를 한다.
- `git status`의 첫 줄이 `On branch about`인지 commit 전에 확인한다. `On branch main`이면 1번으로 돌아간다.

### 3. about 브랜치 push 하고 GitHub에서 비교

`git push -u origin about`을 하고 GitHub에서 브랜치 드롭다운을 연다. [따라하기 14단계](walkthrough.md#14-about-브랜치-push-하기)를 본다.

| 드롭다운에서 고른 브랜치 | `about.html`이 보이는가 |
|---|---|
| `main` | 없다 |
| `about` | 있다 |

- **2 Branches**를 눌러 브랜치 목록에 `main`과 `about`이 보이는 화면을 **캡처 3**으로 저장한다.
- 공개 페이지는 아직 그대로다. Pages는 `main`만 배포하기 때문이다.
- 노란 배너의 **Compare & pull request**는 누르지 않는다. 합치기는 4번에서 내 PC에서 한다.

### 4. main에 합쳐 공개 페이지에 반영

`git switch main` → `git merge about` → `git push`를 한다. [따라하기 15단계](walkthrough.md#15-main으로-돌아가-merge-하고-push-하기)를 본다.

- `git switch main` 직후 `about.html`이 사라진 것을 확인하고, merge 뒤 돌아오는 것을 본다.
- merge 출력에 `Fast-forward`와 `2 files changed`가 있어야 한다.
- 1분쯤 뒤 공개 페이지를 새로고침해 **소개 페이지 보기** → `소개` 카드가 열리면 **캡처 4**를 저장한다.

### 5. 브랜치 정리 (선택)

`git branch -d about`으로 지우고 `git branch`에 `* main`만 남는지 본다. GitHub 브랜치 목록에서도 휴지통 아이콘으로 지울 수 있다.
[따라하기 16단계](walkthrough.md#16-브랜치-정리하기-선택)를 본다. 지우지 않아도 감점은 없다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| **Compare & pull request**를 눌러 GitHub에서 merge해 버렸다 | 화면을 그대로 두고 강의자에게 보여 준다. 내 PC에서 `git merge`를 다시 하지 않는다 |
| `error: src refspec main does not match any` | commit이 하나도 없거나 브랜치 이름이 `main`이 아니다. `git log --oneline`이 비어 있으면 `git add .` → `git commit`, `git branch`에 `master`만 있으면 `git branch -M main` |
| `error: remote origin already exists.` | `origin`이 이미 적혀 있다. `git remote -v`의 주소가 맞으면 그대로 push한다. 틀렸으면 `git remote remove origin` 뒤 다시 `git remote add origin <URL>` |
| `fatal: 'origin' does not appear to be a git repository` | `git remote add origin`을 아직 안 했거나 다른 폴더에서 실행했다. 프롬프트의 폴더 이름과 `git remote -v`를 본다 |
| `! [rejected]  main -> main (fetch first)` 또는 `Updates were rejected because the remote contains work that you do not have locally` | 저장소를 만들 때 **Add a README file**을 체크했다. GitHub **Settings** 맨 아래 **Delete this repository**로 지우고 README 없이 다시 만든 뒤 push한다 |
| `Author identity unknown` / `Please tell me who you are.` | 1주차처럼 `git config user.name "student01"`, `git config user.email "본인 이메일"`을 설정하고 commit을 다시 한다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시와 `git log --oneline`을 본다 |
| 로그인 창이 안 뜨고 `Username for 'https://github.com':`가 나온다 | Git Credential Manager가 없는 환경(macOS 등)이다. 비밀번호를 쳐도 되지 않는다(GitHub는 비밀번호 로그인을 받지 않는다). 강의자 안내를 따른다 |
| `remote: Permission to student01/my-web.git denied to <다른 아이디>` | 공용 PC에 이전 사용자의 로그인이 남아 있다. Windows **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거하고 다시 push한다 |
| `fatal: invalid reference: about` | about 브랜치를 아직 만들지 않았다. `git branch about` 뒤에 `git switch about` |
| `fatal: The current branch about has no upstream branch.` | `git push`만 쳤다. 처음 올리는 브랜치는 `git push -u origin about` |
| `On branch main`인 채로 `about.html`을 commit했다 | 브랜치를 옮기기 전에 commit한 것이다. 강의자에게 보여 주고 함께 되돌린다. 이번 주 결과물(공개 페이지)에는 영향이 없다 |
| `error: the branch 'about' is not fully merged` | merge하기 전에 지우려 했다. `git switch main` → `git merge about`을 먼저 한다 |
| `merge: about - not something we can merge` | about 브랜치를 merge 전에 지웠다. `git branch about origin/about`으로 되살리고 4번부터 다시 한다 |
| `git switch main` 뒤 `about.html`이 사라졌다 | 정상이다. about 브랜치에만 있는 파일이다. `git merge about` 뒤에 돌아온다 |
| 공개 URL이 404 | **Settings › Pages**에 "Your site is live at"이 있는지, 1~2분 기다렸는지, 주소의 아이디·저장소 이름·끝의 `/`, 저장소 맨 위에 `index.html`이 있는지 본다 |
| 공개 페이지가 옛 내용이다 | `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다. push했다면 1분 기다리고 **Ctrl+F5** |
| 공개 페이지에서 **소개 페이지 보기**가 404 | GitHub `main` 브랜치에 `about.html`이 보이는지 본다. 없으면 `git switch main` → `git merge about` → `git push` |

한 번에 한 곳만 고치고 다시 실행한다. 해결되지 않으면 터미널 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 네 장

1. **저장소 화면**: `github.com/<아이디>/my-web`에 `index.html`·`styles.css`·`app.js`가 보이는 화면
2. **공개 페이지**: `https://<아이디>.github.io/my-web/`에 `내 첫 GitHub 페이지`가 열린 화면
3. **브랜치 목록**: GitHub 브랜치 목록에 `main`과 `about`이 보이는 화면
4. **소개 페이지**: 공개 페이지에서 **소개 페이지 보기**를 눌러 `about.html`이 열린 화면

완료 기준은 공개 페이지에서 소개 페이지 링크가 동작하는 것이다. 캡처 1·2만 있으면 부분 통과이며, 3·4는 예제와 도움을 받아 마무리해도 된다.
캡처에 이메일·실명이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: `<p>` 문장을 다른 내용으로 바꿔 `add → commit → push` 하고, 1분 뒤 공개 페이지가 따라 바뀌는지 본다.
- 1일차: `styles.css`의 `background: #eef2ff`를 다른 색으로 바꿔 push해 본다. CSS만 바꿔도 공개 페이지가 바뀐다.
- 2일차: `contact` 브랜치를 만들어 `contact.html`을 같은 순서(`branch → switch → 파일 → commit → push -u → switch main → merge → push`)로 올려 본다.
- 2일차: 두 브랜치가 **같은 줄**을 서로 다르게 고친 뒤 merge하면 git이 멈추고 충돌(conflict)을 알린다. 이번 주에는 다루지 않으며, 같은 줄을 두 곳에서 고치지 않으면 생기지 않는다.
- 집에서 이어 하려면 슬라이드의 **다른 PC에서 이어 할 때**(`git clone`, `git pull`)를 본다.

추가 과제는 선택 사항이다.
