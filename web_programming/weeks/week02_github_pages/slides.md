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

`강의·시연 60분 → 개별 실습 30분`

1. 준비 5분: 배부 파일·계정 확인 (계정·설치는 사전 준비)
2. remote(`origin`)를 적고 첫 push 하기
3. 고치고 push 하면 GitHub가 바뀐다
4. GitHub Pages로 공개 주소 만들기

강의: 준비 5 + GitHub·remote 15 + 첫 push 15 + Pages 15 + 공개 경로 5 + 안내 5분.
학생은 세 파일을 복사하고 h1 한 줄을 바꿉니다. CSS·JS는 제공 코드입니다.

---

## 1일차 · 5–20분 ① — 내 PC의 저장소를 GitHub에 올리면

```text
내 PC                                    GitHub (인터넷)
my-web/.git  ──── git push ────▶  github.com/student01/my-web
 commit 1                            commit 1   ← 같은 기록
```

- Git은 내 PC에 기록을 남기는 **도구**, GitHub는 그 기록을 올려 두는 **서비스**입니다.
- 올려 두면 다른 PC에서도 받을 수 있고, Pages로 **공개 주소**가 생깁니다.
- push하기 전에는 GitHub에 아무것도 없습니다. 저장만 한 파일은 가지 않고 **commit한 것만** 갑니다.

---

## 1일차 · 5–20분 ② — GitHub 계정과 빈 저장소 만들기

1. 사전 준비한 GitHub 계정으로 로그인 (가입은 강의자 준비 지원)
2. 오른쪽 위 **+ › New repository**
3. Repository name: `my-web` · **Public**
4. **Add a README file**, .gitignore, license는 모두 **끄기**
5. **Create repository**

만들면 "…or push an existing repository from the command line" 아래에 명령 세 줄이 보입니다.
이후 슬라이드에서 remote·push 명령을 확인합니다. 아이디는 공개 주소에 들어가므로 실명·학번을 넣지 않습니다.

---

## 1일차 · 5–20분 ③ — remote와 origin

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

## 1일차 · 20–35분 ① — 첫 push와 브라우저 로그인

```bash
git push -u origin main
```

- Git Credential Manager 인증이 필요하면 브라우저 로그인 → 요청된 인증·권한 확인을 진행합니다. 문구는 버전에 따라 다를 수 있습니다.
- 인증이 저장되어 있으면 로그인 창이 생략될 수 있습니다. 비밀번호·토큰을 명령에 적지 않습니다.
- `-u`: 다음부터 `git push`만 쳐도 `origin`의 `main`으로 가게 기억합니다.

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

GitHub 저장소 화면을 새로고침하면 세 파일이 보입니다.

---

## 1일차 · 20–35분 ② — 고치고 push 하면 GitHub가 바뀐다

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
- GitHub에서 `index.html`을 열면 바뀐 줄이 보이고, 제목 변경 commit을 확인합니다. 새 폴더에서 안내대로 시작했다면 2개입니다.
- 저장만 하고 push하지 않으면 GitHub는 그대로입니다.

---

## 1일차 · 35–55분 — GitHub Pages 켜기

Settings › Pages › Build and deployment

1. Source: `Deploy from a branch`
2. Branch: `main` · 폴더 `/(root)` · Save
3. 배포 완료 뒤 Visit site (반영에 최대 10분)

`https://student01.github.io/my-web/`

- 35–50분: Pages 설정·배포 상태 시연
- 50–55분: 저장소 하위 경로·직접 주소 확인
- 루트에 `index.html`을 두고 주소의 대소문자를 맞춥니다.
- main에 push하면 다시 배포됩니다.

---

## 1일차 · 55–60분 — 실습 안내

[실습지](lab.md#1일차--github에-올리고-공개하기-30분) · [따라하기](walkthrough.md#1일차)

| 학생 실습 | 시간 |
|---|---:|
| `my-web`에 파일 복사·로컬 commit 확인 | 5분 |
| 빈 원격 저장소·remote·push | 10분 |
| h1 한 줄 변경·commit·push | 5분 |
| Pages·방문 버튼·캡처 1·2 | 10분 |

학생 실습은 30분입니다. 배포가 늦으면 로컬 화면·GitHub commit을 먼저 확인합니다.

---

# 2일차 — 브랜치로 소개 페이지 올리기

`강의·시연 60분 → 개별 실습 30분`

1. 브랜치를 만들어 옮겨 가기
2. `about.html`을 브랜치에서 commit·push 하기
3. main에 합쳐 공개 페이지에 반영하기

강의: 준비 5 + branch·switch 15 + 파일 추가 10 + merge 15 + Pages 비교 10 + 안내 5분.
필수는 제공 소개 한 줄·왕복 링크와 Git 명령입니다.

---

## 2일차 · 5–20분 ① — 브랜치는 따로 올리는 작업선

```text
merge 전: main → [제목 바꾸기] → [소개 페이지 추가] ← about
merge 후:                       [소개 페이지 추가] ← main, about
                                main push → Pages
```

- 브랜치: **다른 내용을 따로 올리는 작업선**. 이번 실습은 `git branch -M main`으로 이름을 정합니다.
- about에서 commit해도 main은 그대로입니다. GitHub에도 따로 올라갑니다.
- 다 되면 main으로 돌아와 **merge**로 합칩니다.

---

## 2일차 · 5–20분 ② — 브랜치 만들고 옮겨 가기

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

## 2일차 · 20–30분 — about.html 추가하고 commit

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

위 코드는 부분 발췌입니다. [제공 HTML](examples/day2/about.html)을 복사해 소개 한 줄을 수정하고 왕복 링크를 확인합니다.

---

## 2일차 · 30–45분 ① — about 브랜치 push

```bash
git push -u origin about
```

GitHub의 브랜치 드롭다운에서 merge 전 파일을 비교합니다.

| 브랜치 | 파일 |
|---|---|
| `main` | index.html · styles.css · app.js |
| `about` | 위 세 파일 + about.html |

- View all branches로 목록을 열어 캡처 3을 저장합니다.
- Pages는 main을 배포하므로 아직 그대로입니다.
- 합치기는 다음 단계에서 내 PC의 `git merge`로 합니다. PR 버튼은 누르지 않습니다.

---

## 2일차 · 30–55분 — main에 합쳐 Pages에 반영하기

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
- 30–45분: merge 시연. 45–55분: main·about 파일과 Pages 비교.
- main push와 배포가 끝나면 **소개 페이지 보기** 링크가 생깁니다. 반영 지연은 로컬 화면·commit으로 먼저 확인합니다.

---

## 수업 뒤 선택 — 브랜치 정리하기 (선택)

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
- 캡처 3을 먼저 저장합니다. 삭제는 선택이며, 3주에는 main에서 이어 갑니다.

---

## 2일차 · 55–60분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--브랜치로-소개-페이지-올리기-30분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week02_github_pages

1. about 브랜치 생성·전환: 5분
2. 제공 소개 문구·왕복 링크: 10분
3. commit·about push·캡처 3·main merge·push: 10분
4. 공개 소개 확인·캡처 4: 5분

**학생 실습 합계: 30분.** 브랜치 삭제·SSH는 필수가 아닙니다.

---

## 제출하기

2주는 네 장을 제출하는 예외입니다. 2일차 끝에 모아 제출합니다.

1. GitHub 저장소 `my-web`에 세 파일이 보이는 화면
2. `https://<아이디>.github.io/my-web/`이 열린 화면
3. GitHub 브랜치 목록에 `about`이 보이는 화면
4. 공개 페이지에서 **소개 페이지 보기**를 눌러 `about.html`이 열린 화면

배포가 늦으면 로컬 화면·GitHub commit을 제출하고 공개 화면을 보완합니다.
캡처에 이메일·실명이 보이지 않게 합니다. 아이디는 보여도 됩니다.

---

## 수업 뒤 선택 — clone과 pull

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

## 수업 뒤 선택 — SSH 키로 로그인하기

```bash
ssh-keygen -t ed25519 -C "student01@example.com"
```

- 만들어진 `~/.ssh/id_ed25519.pub` 내용을 **Settings › SSH and GPG keys › New SSH key**에 붙여 넣습니다.
- `git remote set-url origin git@github.com:student01/my-web.git`으로 주소를 바꾼 뒤 push합니다.
- 이번 주 실습은 **HTTPS + 브라우저 로그인**으로 합니다. SSH는 정규 필수 범위 밖이며, 원하면 README의 공식 문서를 따라 해 봅니다.
- Pages는 `gh-pages`라는 별도 브랜치에서 배포하는 방식도 있습니다. 이번 주는 `main` · `/(root)`만 씁니다.

---

## 다음 주 미리 보기

이제 `add → commit → push` 한 번이면 공개 페이지가 바뀝니다.

3주는 day2의 네 파일을 main에서 이어 쓰며 **시맨틱 HTML과 정적 form**을 배웁니다. CSS·JS는 연결만 해제합니다.
파일 준비는 사전, 코드 수정·로컬 확인·캡처는 실습 30분, 업로드는 수업 뒤 정리입니다. 공개 주소는 유지합니다.
