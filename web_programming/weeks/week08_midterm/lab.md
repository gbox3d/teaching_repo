# 8주차 실습 — 리허설과 중간 실기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week08_midterm

1일차는 시험과 같은 모양의 **리허설**이다. 문제 네 개를 60분 안에 풀고, 새 저장소를 만들어 Pages로 배포하는 절차까지 오늘 끝낸다.
2일차 60분이 **본시험**이다. 문제지는 시험 시간에 받는다. 작업 폴더는 `my-web/exam/` 하나다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. `student01`은 예시 아이디이므로 본인 아이디로 바꾼다.

## 1일차 — 리허설과 저장소 준비 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `midterm-practice`를 만들어 **File › Open Folder**로 열고, 리허설 starter 세 파일을 넣는다 |
| 5–15분 | 문제 1: `활동` 아래에 `ul`·`li` 세 줄과 2열 3행 `table`을 넣는다 |
| 15–25분 | 문제 2: `.card` 규칙, `nav`를 `display: flex`, `@media (max-width: 600px)`에서 세로 |
| 25–37분 | 문제 3: 버튼 두 개 — 글자 바꾸기(`textContent`)와 다크 모드(`classList.toggle`) |
| 37–45분 | 문제 4: 신청하기 → `#result`에 `이름: 신청 이유`, 이름이 비면 안내하고 커서 이동 |
| 45–50분 | [해답](examples/rehearsal_solution)과 한 줄씩 맞춰 본다. 먼저 끝났으면 더 일찍 시작한다 |
| 50–60분 | `git init` → `git branch -M main` → `git config` 두 줄 → `git add .` → `git commit` → GitHub에 새 저장소 `midterm-practice` 만들기 → `git remote add origin <HTTPS URL>` → `git push -u origin main`(첫 push는 브라우저 로그인) → **Settings › Pages**(`main`·`/(root)`) → 공개 주소 열기 → 공용 PC면 자격 증명 삭제 |

시험 당일에는 이 마지막 줄(저장소 만들기·Pages 켜기)을 **하지 않는다.** 오늘 한 번 해 두는 것이 목적이다.

### 1. starter 세 파일 넣기 (`index.html` · `styles.css` · `app.js`)

[examples/rehearsal_starter](examples/rehearsal_starter)의 세 파일을 새 폴더에 그대로 넣는다. [따라하기 2단계](walkthrough.md#2-starter-세-파일-넣기)를 본다.

- `index.html`을 더블클릭해 열고 F12 **Console**에 `리허설 starter 준비 완료`가 보이면 준비가 끝난 것이다.
- 지금은 꾸며지지 않은 화면이 정상이다. 버튼을 눌러도 아무 일도 일어나지 않는다.
- 세 파일은 **같은 폴더에 나란히** 둔다. 폴더를 하나 더 만들지 않는다.

### 2. 문제 1 — 목록과 표 (`ul` · `li` · `table` · `tr` · `th` · `td`)

`index.html`의 `문제 1-1`·`문제 1-2` 주석을 지우고 그 자리에 넣는다. [따라하기 3단계](walkthrough.md#3-문제-1-목록과-표-넣기)를 본다.

- `li` 세 줄 앞에 점(•)이 붙으면 `ul` 안에 있는 것이다.
- 표는 줄(`tr`)을 세 개 쌓고, 첫 줄만 `th` 두 개로 만든다. 나머지 두 줄은 `td` 두 개다.
- 선이 없는 것이 정상이다. 선은 문제 2에서 `.card`의 `border`로 한 번만 그린다.

### 3. 문제 2 — 카드 색과 nav 가로 배치 (`.class` · `flex` · `@media`)

`styles.css`의 `문제 2-1`~`2-3` 주석 자리에 규칙 세 개를 쓴다. [따라하기 4단계](walkthrough.md#4-문제-2-카드-색과-nav-가로-배치)를 본다.

- `.card`는 `main`에 이미 붙어 있다. class 이름 앞의 점(`.`)을 빠뜨리면 아무 일도 일어나지 않는다.
- `nav`에 `display: flex`를 주면 링크 세 개가 가로로 선다. `gap`으로 사이를 벌린다.
- F12 → 기기 모드에서 **375px**로 줄여 링크가 세로로 서면 `@media`가 맞은 것이다. 1280px에서는 다시 가로다.

### 4. 문제 3 — 버튼 두 개 (`addEventListener` · `textContent` · `classList`)

`app.js`의 `문제 3-1`·`3-2` 주석 자리에 쓴다. [따라하기 5단계](walkthrough.md#5-문제-3-버튼으로-글자와-색-바꾸기)를 본다.

- 변수 `noticeButton`·`noticeText`·`darkButton`은 파일 맨 위에 이미 만들어져 있다. 다시 만들지 않는다.
- 클릭할 때마다 할 일은 `function () { }` 안에 쓴다. 5·6주에 쓴 그 모양이다.
- 다크 모드 CSS(`body.dark`)는 `styles.css`에 이미 있다. JavaScript는 class를 붙였다 떼기만 한다.
- 빨간 줄에 `null`이 보이면 선택자 철자와 `#`을 본다.

### 5. 문제 4 — 폼 입력 표시와 빈값 안내 (`submit` · `value` · `trim` · `focus`)

`app.js`의 `문제 4-1`·`4-2` 주석 자리에 쓴다. [따라하기 6단계](walkthrough.md#6-문제-4-폼-입력-표시와-빈값-안내)를 본다.

- **신청하기**를 눌렀을 때 화면이 처음으로 돌아가고 주소 끝에 `?`가 붙으면 `event.preventDefault()`가 빠진 것이다.
- 이름 칸이 비었는지는 `trim()` 한 값이 `''`인지로 본다. 빈칸만 넣은 경우도 걸러야 한다.
- 안내를 띄운 뒤에는 `return`으로 멈춘다. 멈추지 않으면 빈 이름이 그대로 표시된다.

### 6. 오늘 확인할 것

- [ ] 리허설 화면에 목록·표·카드 테두리가 보이고 375px에서 메뉴가 세로로 선다.
- [ ] 버튼 두 개가 각각 글자와 배경을 바꾼다.
- [ ] 이름을 비우고 누르면 안내가 뜨고, 채워서 누르면 `이름: 신청 이유`가 뜬다.
- [ ] Console에 빨간 줄이 없다.
- [ ] `https://<아이디>.github.io/midterm-practice/`가 열린다.

1일차 결과는 점수에 들어가지 않는다. **어디서 막혔는지 알고 가는 것**이 목적이다.

## 2일차 — 중간 실기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 문제지를 끝까지 읽고 요구 사항에 번호를 매긴다. 아직 코드를 쓰지 않는다 |
| 5–15분 | HTML: 뼈대·목록·표·폼 |
| 15–25분 | CSS: 선택자·박스·`flex`·`@media` |
| 25–50분 | DOM과 폼: 클릭 → `textContent`·`classList`, 제출 → 표시·빈값 안내 |
| 50–55분 | `git add .` → `git commit -m "중간 실기"` → `git push` |
| 55–60분 | 예비: 공개 주소 새로고침·캡처·`git log -1 --oneline` 적기 |

시작 전 `my-web`에서 `git pull`을 하고 `exam` 폴더를 만든 뒤, 받은 starter 세 파일을 넣고 첫 commit(`중간 실기 시작`)까지 해 둔다. [따라하기 9단계](walkthrough.md#9-my-web에-exam-폴더-만들기)와 [10단계](walkthrough.md#10-starter-세-파일-넣고-첫-commit-하기)를 본다.

### 시험 규칙

- 작업 폴더는 `my-web/exam/` 하나다. 파일은 `index.html`·`styles.css`·`app.js` 세 개다.
- **저장 → push → 공개 주소를 새로고침해서 보이는 것이 제출본**이다. 저장하지 않은 파일은 commit되지 않는다.
- commit은 두 번 이상 한다. 시작 전 starter를 넣은 첫 commit(`중간 실기 시작`)과 마지막 commit(`중간 실기`)이면 된다.
- 범위 밖(배열 목록·`localStorage`·`fetch`·모듈·외부 라이브러리)은 쓰지 않는다. 가점이 없고, 화면이 멈추면 감점이다.
- 볼 수 있는 것: 교재 사이트, 본인 `my-web` 저장소, MDN. 그 밖은 강의자 공지를 따른다.
- 한 문제에 5분 넘게 막히면 다음 문제로 간다. 문제끼리 이어져 있지 않다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 `git log -1 --oneline` 출력을 같은 점수로 인정한다. `git status`에 `Your branch is ahead`가 있으면 push를 안 한 것이다 |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | `querySelector`가 아무것도 못 찾았다. 선택자의 `#`과 철자를 `index.html`의 `id`와 대소문자까지 비교한다. `<script src="app.js" defer>`에서 `defer`가 빠져도 같은 줄이 나온다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | 글을 넣을 곳을 못 찾았다. `#result`·`#notice-text` 같은 `id`의 철자를 본다 |
| `Uncaught ReferenceError: nameinput is not defined` | 변수 이름의 대소문자가 다르다. 만든 이름은 `nameInput`이다 |
| `Uncaught TypeError: Cannot read properties of undefined (reading 'toggle')` | `classList`를 `classlist`로 썼다. 가운데 `L`이 대문자다 |
| **신청하기**를 누르면 화면이 처음으로 돌아가고 주소 끝에 `?`가 붙는다 | `event.preventDefault()`가 없다. `function (event) { event.preventDefault(); … }` |
| 이름을 비우고 눌렀는데 `: 사진이 좋아서`가 표시된다 | 안내 뒤에 `return`이 없다. `if` 블록 안에서 멈춰야 한다 |
| 화면이 전혀 꾸며지지 않는다 | `Uncaught`로 시작하는 JS 빨간 줄은 없고, 대신 `Failed to load resource: net::ERR_FILE_NOT_FOUND`(공개 주소에서는 404) 한 줄이 뜬다. 이 줄은 파일을 못 찾았다는 뜻이므로 `<link rel="stylesheet" href="styles.css">` 줄의 파일 이름과 파일 위치를 본다 |
| `! [rejected]        main -> main (fetch first)` | GitHub에 내가 모르는 commit이 있다. `git pull` 뒤 다시 `git push` |
| `fatal: 'origin' does not appear to be a git repository` | 주소를 아직 안 적었다. `git remote -v`가 비어 있으면 `git remote add origin <HTTPS URL>`을 먼저 하고 다시 push한다 |
| `error: remote origin already exists.` | 주소가 이미 적혀 있다. `git remote -v`의 주소가 맞으면 그대로 push한다 |
| `nothing to commit, working tree clean` | 파일을 저장하지 않았거나 이미 commit했다. VS Code 탭 제목의 ● 표시를 본다 |
| `Everything up-to-date` | 새 commit이 없다. `git log -1 --oneline`으로 마지막 commit이 방금 것인지 본다 |
| `remote: Permission to student01/my-web.git denied to <다른 아이디>` | 공용 PC에 이전 사용자의 로그인이 남아 있다. **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 제거하고 다시 push한다 |
| 공개 주소 `…/my-web/exam/`이 404 | GitHub `main`의 `exam/` 폴더에 `index.html`이 있는지 본다. 파일 이름은 소문자 `index.html`이다 |

한 번에 한 곳만 고치고 다시 확인한다. 10분 넘게 같은 자리에 있으면 손을 든다. 환경·제출 문제는 함께 본다.

## 제출 — 네 가지

1. **공개 URL**: `https://<아이디>.github.io/my-web/exam/`
2. **저장소 URL**: `https://github.com/<아이디>/my-web`
3. **마지막 commit SHA**: `git log -1 --oneline`의 앞 일곱 글자 (예: `1ea3c2e`)
4. **캡처 1장**: 완성 화면과 **주소창**이 함께 보이게 찍는다

캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.
Pages가 늦어 1번을 만들 수 없으면 로컬 화면 캡처 + 3번으로 대신 인정한다.

## 먼저 끝났다면

- 1일차: 리허설 페이지의 `@media` 폭을 `600px` 대신 다른 값으로 바꿔 보고, 기기 모드에서 언제 세로로 바뀌는지 확인한다.
- 1일차: 다크 모드를 켠 채 375px로 줄여 두 가지가 같이 동작하는지 본다.
- 1일차: `이름` 칸에 빈칸만 넣고 눌러 본다. `trim()`이 없으면 어떻게 되는지 지우고 확인한 뒤 되돌린다.
- 2일차: 남는 시간에는 새 기능을 넣지 않는다. 링크를 모두 눌러 404가 없는지, Console이 깨끗한지, 캡처가 찍혔는지만 본다.

1일차 확장 과제는 채점하지 않는다.
