---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 1주차"
footer: "웹 실행 구조와 Git 상태"
---

# 1주차
## 웹 실행 구조와 Git 상태

**주 2회 × 90분**<br>
매회 설명·함께 따라하기 30분 + 천천히 연습하기 60분

교재 사이트: https://gbox3d.github.io/teaching_repo/webprg/

---

## 이번 주에 할 일

1. **1일차** — 주소를 넣으면 브라우저가 무엇을 받아 오는지 보고, 세 파일로 내 소개 페이지를 만듭니다.
2. **2일차** — 연습 폴더에 `git init`부터 commit 3개까지 기록을 남깁니다.

```text
[캡처 1] 내 소개 페이지 + 교재 사이트 Network의 Status 200
[캡처 2] git log --oneline 의 commit 3줄 + 연습 페이지
```

제출물은 이 캡처 두 장입니다. 다른 제출 파일은 없습니다.
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

---

<!-- _class: lead -->

# 1일차 · 설명 30분
## 브라우저는 무엇을 받아 화면을 만드는가

---

## 1일차 · 0–4분 — URL을 읽는 법

```text
https://gbox3d.github.io:443/teaching_repo/webprg/index.html
└─┬─┘   └───────┬──────┘ └┬┘└──────────────┬───────────────┘
scheme        host       port            path
```

- **scheme**: 주고받는 방식. 인터넷은 `https`, 내 PC 파일은 `file`
- **host**: 파일을 가지고 있는 컴퓨터(서버)의 이름
- **port**: 그 컴퓨터의 접수 창구 번호. `https`는 443이라 보통 생략합니다
- **path**: 서버 안에서 파일이 있는 위치

**질문:** 내 폴더의 `index.html`을 더블클릭하면 주소창은 무엇으로 시작할까요?

---

## 1일차 · 4–9분 — 요청과 응답, 200과 404

```text
GET  /teaching_repo/webprg/              →  200  HTML을 받았다
GET  /teaching_repo/webprg/nothing.html  →  404  그 주소에 파일이 없다
```

- 브라우저는 주소마다 **요청**을 보내고, 서버는 **상태 번호 + 내용**으로 답합니다.
- `200`은 "찾아서 보냈다", `404`는 "그 주소에 파일이 없다"입니다.
- 화면이 이상하면 먼저 **어떤 요청이 404인지** 봅니다. 파일 이름이나 경로를 잘못 적은 경우가 대부분입니다.
- `200`·`404`는 **서버가 보내는 번호**입니다. 내 PC 파일(`file://`)은 서버를 거치지 않으므로 교재 사이트에서 봅니다.

---

## 1일차 · 9–14분 — HTML·CSS·JavaScript 세 파일

| 파일 | 맡는 일 | 오늘 예제에서 |
|---|---|---|
| `index.html` | 내용과 구조 | 제목 `<h1>`, 소개 문단 `<p>`, 버튼 |
| `styles.css` | 모양 | 카드 모양, 색, 글자 굵기 |
| `app.js` | 동작 | 버튼을 누르면 클릭 횟수가 올라감 |

- 브라우저는 `index.html`을 먼저 받고, 그 안에 적힌 두 파일을 이어서 받습니다.
- 나눠 두면 고칠 곳을 찾기 쉽습니다. 모양이 이상하면 CSS, 버튼이 안 되면 JavaScript.
- `app.js`는 이번 주에 **읽고 결과만** 봅니다. JavaScript 문법은 뒤 주차에서 배웁니다.

---

## 1일차 · 14–21분 — VS Code로 열고 고치기

```html
<link rel="stylesheet" href="styles.css">
<script src="app.js" defer></script>
```

- `index.html`의 이 두 줄을 보고 브라우저가 `styles.css`와 `app.js`를 이어서 가져옵니다.
- **File › Open Folder**로 `week01` 폴더를 열고, **New File**로 세 파일을 만듭니다.
- 탐색기에서 `index.html`을 더블클릭 → 주소창이 `file:///…/week01/index.html`입니다.
- `<h1>`을 내 소개로 고치고 **저장(Ctrl+S)** → 브라우저 **새로고침(F5)**.
- 저장하지 않으면(탭 제목에 ●) 새로고침해도 화면은 그대로입니다.

---

## 1일차 · 21–27분 — DevTools 세 탭 (F12)

- **Elements**: 지금 화면의 HTML. `<h1>`이 어디 있는지 봅니다.
- **Console**: JavaScript가 남긴 메시지와 빨간 오류 줄.
- **Network**: 브라우저가 받아 온 파일 목록과 **Status**.

```text
Name                    Type         Status
webprg/                 document     200
assets/library.css      stylesheet   200
assets/course.js        script       200
nothing.html            document     404
```

오류 하나만 따라 해 보기: `href="style.css"`로 틀리게 저장 → 새로고침 → 카드 모양이 사라짐
→ Console의 빨간 줄 확인 → `href="styles.css"`로 되돌리기 → 새로고침.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--세-파일로-내-소개-페이지-만들기-60분) · [따라하기](walkthrough.md#1일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

1. `week01` 폴더에 세 파일을 만들고 `index.html`을 브라우저로 엽니다.
2. `<h1>`과 소개 문단을 내 소개(`student01` 같은 수업용 별칭)로 고치고 저장·새로고침합니다.
3. 교재 사이트에서 Network의 `200`과 없는 주소의 `404`를 봅니다.
4. `styles.css` 이름을 한 번 틀리게 해 보고 원래대로 되돌립니다.

**설명 합계: 4+5+5+7+6+3 = 30분**

막히면 주소창의 경로와 파일 이름을 한 글자씩 비교합니다.

---

<!-- _class: lead -->

# 2일차 · 설명 30분
## Git은 파일이 아니라 상태 변화를 기록한다

---

## 2일차 · 0–3분 — 저장과 commit은 다르다

- **저장(Ctrl+S)**: 파일을 지금 내용으로 덮어씁니다. 이전 내용은 남지 않습니다.
- **commit**: "이 순간의 폴더 상태"를 설명 한 줄과 함께 기록으로 남깁니다.
- 기록이 쌓이면 무엇을 언제 바꿨는지 목록으로 볼 수 있습니다.

오늘은 새 폴더 `week01-practice`에 commit 세 개를 남깁니다.

```text
① 제목 만들기   ② 소개 문단과 링크 추가   ③ 스타일과 스크립트 연결
```

다음 주에는 같은 순서로 만든 저장소를 GitHub에 올립니다.

---

## 2일차 · 3–8분 — `git init`: 저장소와 untracked

```bash
git init           # 이 폴더에 .git/ 을 만든다 = 저장소 본체
git branch -M main # 기본 브랜치 이름을 main으로
```

```text
$ git status
On branch main
No commits yet
Untracked files:
        index.html
nothing added to commit but untracked files present
```

- `.git/`이 기록 전체다. 작업 파일과 기록은 **다른 것**이다.
- 폴더 안에 있다고 기록되지 않는다. `index.html`은 아직 **untracked**다.
- 이름·이메일을 적지 않아도 commit은 된다. 대신 PC 계정 이름이 기록에 남으니 18–22분에서 설정한다.

---

## 2일차 · 8–13분 — 세 영역

```text
untracked ─┐
           ├─ git add ─▶ staging area ─ git commit ─▶ repository(.git)
modified ──┘             다음 기록 후보                 확정된 기록
 working tree
```

- **working tree**: 지금 편집하고 있는 폴더의 파일
- **untracked**: Git이 아직 모르는 새 파일. `git add`로 처음 등록된다
- **staging area**: 다음 commit에 담기로 고른 것만 모이는 곳
- **repository**: `git commit`으로 확정한 기록이 쌓이는 곳
- 같은 파일이 staged와 unstaged 변경을 동시에 가질 수도 있다 (다음 장)

---

## 2일차 · 13–18분 — `git status`가 답을 알려 준다

```text
Changes to be committed:          ← staging area
        modified:   index.html
Changes not staged for commit:    ← working tree (추적 중)
        modified:   index.html
Untracked files:                  ← working tree (추적 전)
        notes.txt
```

- 같은 `index.html`이 위아래에 **동시에** 나올 수 있다. commit은 파일이 아니라 `git add` 한 순간의 내용을 기록하기 때문이다.
- 각 제목 밑 괄호 안내문이 그 영역에서 되돌리는 명령을 알려 준다. 첫 commit 전에는 `git rm --cached`, 그 뒤에는 `git restore --staged`다.
- 명령을 치기 전에 **"이 파일이 지금 어느 제목 아래에 있는가"**를 먼저 본다. (오늘 실습에서 이 상태를 일부러 만들 필요는 없다)

---

## 2일차 · 18–22분 — `git config`: 이 저장소에만 이름 적기

```bash
git config user.name "student01"
git config user.email "student01@example.com"
```

```text
[main (root-commit) 4701d1b] 제목 만들기
 Committer: student <student@student-pc.local>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
```

- 적지 않아도 commit은 **됩니다**. 대신 PC 계정 이름과 PC 이름이 그대로 기록에 남습니다.
- `--global`을 **붙이지 않으면** 지금 이 폴더의 저장소에만 적용됩니다. 공용 PC에서는 붙이지 않습니다.
- 저장소마다 따로 적용되므로 **다음 주 새 폴더에서도 다시** 적습니다.
- 이름은 commit마다 기록에 남습니다. 실명 대신 수업용 별칭을 씁니다.

---

## 2일차 · 22–25분 — `git add`와 `git commit -m`

```bash
git status
git add index.html
git commit -m "제목 만들기"
```

```text
[main (root-commit) 708c9ec] 제목 만들기
 1 file changed, 13 insertions(+)
 create mode 100644 index.html
```

- `git add`: 이 파일을 **다음 commit에 넣겠다**고 고르는 것
- `git commit -m "설명"`: 고른 내용을 설명과 함께 기록으로 확정하는 것
- 메시지에 띄어쓰기가 있으면 반드시 **따옴표**로 감쌉니다.

---

## 2일차 · 25–27분 — `git log --oneline`

```text
2041aef (HEAD -> main) 스타일과 스크립트 연결
cfa0792 소개 문단과 링크 추가
708c9ec 제목 만들기
```

- 위가 가장 최근입니다. 앞의 일곱 글자는 commit 번호이며 PC마다 다릅니다.
- 좋은 메시지: `소개 문단과 링크 추가` — 무엇이 바뀌었는지 한 줄로 보입니다.
- 피할 메시지: `update`, `최종`, `수정1` — 나중에 아무 단서도 되지 않습니다.

---

## 2일차 · 27–29분 — `git diff`로 바뀐 줄 보기 (선택)

```bash
git diff
```

```text
       <h1>student01의 Git 연습</h1>
+      <p>commit을 하나씩 쌓아 가며 만든 연습 페이지입니다.</p>
+      <p><a href="https://gbox3d.github.io/teaching_repo/webprg/">…</a></p>
```

- `+`로 시작하는 줄이 이번에 **추가한 줄**입니다.
- 오늘 실습은 `status → add → commit → log`만 하면 됩니다. `git diff`는 눈으로만 봅니다.

---

## 2일차 · 29–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--git으로-commit-3개-남기기-60분) · [따라하기](walkthrough.md#2일차)
실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week01_web_git

1. `week01-practice` 폴더에서 `git init` → `git branch -M main` → `git config`.
2. commit ① 제목 → ② 소개 문단과 링크 → ③ 스타일과 스크립트 연결.
3. 매번 `git status` → `git add` → `git commit -m "..."` → `git log --oneline`.

**설명 합계: 3+5+5+5+4+3+2+2+1 = 30분**

마지막에 commit 3줄과 연습 페이지를 한 화면에 캡처합니다.

---

## 이번 주 정리

```text
웹  : URL → 요청 → 응답(200 · 404) → index.html + styles.css + app.js → 화면
Git : git init → git config → git status → git add → git commit -m → git log --oneline
```

- 제출: 캡처 2장(1일차 1장 + 2일차 1장). 다른 제출 파일은 없습니다.
- 화면이 이상하면 파일 이름과 주소를, commit이 안 되면 `git status`를 먼저 봅니다.
- 다음 주: 오늘 배운 `add → commit`에 `push`를 붙여 누구나 여는 주소를 만듭니다.
