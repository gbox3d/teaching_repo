# 8주차 따라하기 — 리허설 풀이와 시험 폴더 준비

처음에는 그대로 따라 하고, 결과가 나오면 본인 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

1일차는 **리허설**이다. 여기 있는 코드는 시험 답안이 아니라 연습 답안이다.
2일차 본시험 문제지는 이 문서에 없다. 시험 시간에 따로 받는다. 2일차 단계(9~12)는 문제지를 받기 전후에 하는 **공통 절차**다.

## 1일차

### 1. 리허설 폴더 만들기

`my-web`과 섞이지 않게 **새 폴더**에서 연습한다. 현재 폴더: 문서(Documents) 폴더 등 원하는 위치

```bash
mkdir midterm-practice
cd midterm-practice
```

**File › Open Folder**로 방금 만든 `midterm-practice` 폴더를 연다. VS Code가 다시 열리면 **Terminal › New Terminal**을 다시 연다.

**예상 결과** — 프롬프트 끝이 `midterm-practice>`이다 (macOS는 `midterm-practice %`). 이제부터 1일차 명령은 이 폴더에서 실행한다.

### 2. starter 세 파일 넣기

탐색기의 **New File** 아이콘으로 파일 세 개를 만들고 아래 내용을 그대로 넣는다.
같은 파일이 [examples/rehearsal_starter](examples/rehearsal_starter)에 있다. GitHub 파일 화면의 **Download raw file**로 내려받아도 된다.

`index.html`:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>중간 실기 리허설</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>사진 동아리 소개</h1>
      <nav>
        <a href="#activity">활동</a>
        <a href="#notice">모임</a>
        <a href="#join">신청</a>
      </nav>
    </header>
    <main class="card">
      <h2 id="activity">활동</h2>
      <!-- 문제 1-1: 여기에 ul 하나와 li 세 줄을 넣는다 -->
      <!-- 문제 1-2: 여기에 2열 3행 table을 넣는다. 첫 줄은 th 두 개 -->
      <h2 id="notice">모임</h2>
      <p id="notice-text">아직 누르지 않았습니다.</p>
      <button id="notice-button" type="button">이번 주 모임 보기</button>
      <button id="dark-button" type="button">다크 모드</button>
      <h2 id="join">신청</h2>
      <form id="join-form">
        <p><label for="name">이름</label> <input id="name" type="text"></p>
        <p><label for="reason">신청 이유</label> <input id="reason" type="text"></p>
        <button type="submit">신청하기</button>
      </form>
      <p id="result"></p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`styles.css`:

```css
/* 중간 실기 리허설 — styles.css */
/* 문제 2를 이 파일에 쓴다. */

body {
  margin: 0;
  padding: 16px;
  font-family: system-ui, sans-serif;
  color: #17213a;
  background: #f4f6fb;
}

h1 {
  font-size: 24px;
}

nav a {
  color: #3157d5;
}

/* 문제 2-1: .card 규칙을 만든다. 배경 white, padding 16px, border 한 줄 */

/* 문제 2-2: nav를 display: flex로 가로로 놓고 gap을 준다 */

/* 문제 2-3: @media (max-width: 600px)에서 nav를 세로로 바꾼다 */

body.dark {
  color: #eeeeee;
  background: #222222;
}

body.dark .card {
  background: #333333;
}
```

`app.js`:

```js
// 중간 실기 리허설 — app.js
// 문제 3과 문제 4를 이 파일에 쓴다.

const noticeButton = document.querySelector('#notice-button');
const noticeText = document.querySelector('#notice-text');
const darkButton = document.querySelector('#dark-button');

// 문제 3-1: noticeButton을 누르면 noticeText의 글을
//           '이번 주 모임: 금요일 오후 5시'로 바꾼다.

// 문제 3-2: darkButton을 누르면 document.body에 dark class가 붙었다 떨어지게 한다.

const joinForm = document.querySelector('#join-form');
const nameInput = document.querySelector('#name');
const reasonInput = document.querySelector('#reason');
const result = document.querySelector('#result');

// 문제 4-1: 신청하기를 누르면 result에 '이름: 신청 이유'가 보이게 한다.
//           페이지가 새로고침되면 안 된다.

// 문제 4-2: 이름 칸이 비어 있으면 result에 '이름을 입력하세요'를 보이고
//           이름 칸에 커서를 둔다.

console.log('리허설 starter 준비 완료');
```

**예상 결과** — `index.html`을 더블클릭해 열면 꾸미지 않은 화면에 제목·메뉴 세 개·`활동`·`모임`·버튼 두 개·입력 칸 두 개가 차례로 보인다.
F12 **Console**에 `리허설 starter 준비 완료` 한 줄만 있고 빨간 줄은 없다.

- 메뉴 세 개(`활동`·`모임`·`신청`)는 같은 문서 안의 `id`로 가는 링크다. 눌러도 페이지가 바뀌지 않고 그 자리로 내려간다. 채점 대상이 아니다.
- `활동` 아래가 비어 있는 것이 맞다. 그 자리가 문제 1이다.
- 버튼을 눌러도 아무 일도 일어나지 않는다. 그 동작이 문제 3이다.
- 세 파일은 **같은 폴더에 나란히** 둔다. 폴더를 더 만들지 않는다.

### 3. 문제 1 목록과 표 넣기

`index.html`에서 아래 주석 두 줄을 지우고 그 자리에 목록과 표를 넣는다.

```html
      <!-- 문제 1-1: 여기에 ul 하나와 li 세 줄을 넣는다 -->
      <!-- 문제 1-2: 여기에 2열 3행 table을 넣는다. 첫 줄은 th 두 개 -->
```

```html
      <ul>
        <li>매주 금요일 사진 찍으러 나가기</li>
        <li>찍은 사진 함께 고르기</li>
        <li>학기말 전시 준비</li>
      </ul>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>모이는 곳</td>
          <td>학생회관 2층</td>
        </tr>
        <tr>
          <td>모이는 때</td>
          <td>금요일 오후 5시</td>
        </tr>
      </table>
```

**예상 결과** — `활동` 아래에 점(•) 세 줄이 생기고, 그 아래에 `항목`·`내용`이 굵게 가운데로 놓인 표가 두 줄을 더 데리고 나타난다.

- 점이 붙지 않으면 `li`가 `ul` 밖에 있는 것이다.
- 표에 선이 없는 것이 정상이다. 선은 문제 2에서 `.card`의 `border`로 한 번만 그린다.
- 줄(`tr`)이 세 개, 첫 줄만 `th` 두 개다. 3주차 `about.html`과 같은 모양이다.

### 4. 문제 2 카드 색과 nav 가로 배치

`styles.css`에서 주석 세 줄을 지우고 그 자리에 규칙 세 개를 쓴다.

```css
/* 문제 2-1: .card 규칙을 만든다. 배경 white, padding 16px, border 한 줄 */

/* 문제 2-2: nav를 display: flex로 가로로 놓고 gap을 준다 */

/* 문제 2-3: @media (max-width: 600px)에서 nav를 세로로 바꾼다 */
```

```css
.card {
  padding: 16px;
  border: 1px solid #c7d0e8;
  background: white;
}

nav {
  display: flex;
  gap: 16px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}
```

**예상 결과** — 본문 전체가 흰 상자 안에 들어가고 옅은 테두리가 생긴다. 메뉴 세 개가 가로로 나란히 서고 사이가 벌어진다.
F12 → 기기 모드에서 폭을 **375px**로 줄이면 메뉴가 세로로 선다. 1280px로 되돌리면 다시 가로다.

- `.card`의 점(`.`)을 빠뜨려 `card { … }`로 쓰면 아무 일도 일어나지 않는다. `card`라는 태그는 없다.
- `.card`는 `index.html`의 `<main class="card">`에 이미 붙어 있다. HTML을 고칠 필요가 없다.
- `@media` 블록은 중괄호가 두 겹이다. 닫는 `}`를 하나 빠뜨리면 그 뒤 규칙이 전부 무시된다.

### 5. 문제 3 버튼으로 글자와 색 바꾸기

`app.js`에서 주석 두 덩어리를 지우고 그 자리에 쓴다. 변수 세 개는 파일 맨 위에 이미 만들어져 있다.

```js
noticeButton.addEventListener('click', function () {
  noticeText.textContent = '이번 주 모임: 금요일 오후 5시';
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});
```

**예상 결과** — **이번 주 모임 보기**를 누르면 `아직 누르지 않았습니다.`가 `이번 주 모임: 금요일 오후 5시`로 바뀐다.
**다크 모드**를 누르면 배경이 어두워지고 글자가 밝아진다. 한 번 더 누르면 돌아온다.

- `body.dark` 규칙은 `styles.css`에 이미 있다. JavaScript는 class를 붙였다 떼기만 한다.
- `classList`의 가운데 `L`은 대문자다. `classlist`로 쓰면 빨간 줄이 난다.
- 빨간 줄에 `null`이 보이면 `#notice-text`처럼 선택자 철자를 `index.html`의 `id`와 대소문자까지 비교한다.

### 6. 문제 4 폼 입력 표시와 빈값 안내

`app.js`의 남은 주석 두 덩어리를 지우고 그 자리에 쓴다.

```js
joinForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const reason = reasonInput.value.trim();

  if (name === '') {
    result.textContent = '이름을 입력하세요';
    nameInput.focus();
    return;
  }

  result.textContent = `${name}: ${reason}`;
  joinForm.reset();
  nameInput.focus();
});
```

**예상 결과** — 이름과 신청 이유를 적고 **신청하기**를 누르면 버튼 아래에 `student01: 사진이 좋아서`가 나타나고 입력 칸이 비워진다.
이름을 비우고 누르면 `이름을 입력하세요`가 나타나고 이름 칸에 커서가 들어간다. 주소창은 그대로다.

- 화면이 처음으로 돌아가고 주소 끝에 `?`가 붙으면 `event.preventDefault()`가 빠진 것이다.
- `return`이 없으면 안내를 띄운 뒤에도 아래로 내려가 빈 이름이 그대로 표시된다.
- 빈칸만 넣고 눌러도 안내가 떠야 한다. 그 일을 `trim()`이 한다.

### 7. 해답과 맞춰 보기

네 문제를 모두 해 본 뒤에 연다. 세 파일 전체는 아래와 같고, 같은 파일이 [examples/rehearsal_solution](examples/rehearsal_solution)에 있다.

`index.html`:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>중간 실기 리허설</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>사진 동아리 소개</h1>
      <nav>
        <a href="#activity">활동</a>
        <a href="#notice">모임</a>
        <a href="#join">신청</a>
      </nav>
    </header>
    <main class="card">
      <h2 id="activity">활동</h2>
      <ul>
        <li>매주 금요일 사진 찍으러 나가기</li>
        <li>찍은 사진 함께 고르기</li>
        <li>학기말 전시 준비</li>
      </ul>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>모이는 곳</td>
          <td>학생회관 2층</td>
        </tr>
        <tr>
          <td>모이는 때</td>
          <td>금요일 오후 5시</td>
        </tr>
      </table>
      <h2 id="notice">모임</h2>
      <p id="notice-text">아직 누르지 않았습니다.</p>
      <button id="notice-button" type="button">이번 주 모임 보기</button>
      <button id="dark-button" type="button">다크 모드</button>
      <h2 id="join">신청</h2>
      <form id="join-form">
        <p><label for="name">이름</label> <input id="name" type="text"></p>
        <p><label for="reason">신청 이유</label> <input id="reason" type="text"></p>
        <button type="submit">신청하기</button>
      </form>
      <p id="result"></p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`styles.css`:

```css
/* 중간 실기 리허설 — styles.css */

body {
  margin: 0;
  padding: 16px;
  font-family: system-ui, sans-serif;
  color: #17213a;
  background: #f4f6fb;
}

h1 {
  font-size: 24px;
}

nav a {
  color: #3157d5;
}

.card {
  padding: 16px;
  border: 1px solid #c7d0e8;
  background: white;
}

nav {
  display: flex;
  gap: 16px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}

body.dark {
  color: #eeeeee;
  background: #222222;
}

body.dark .card {
  background: #333333;
}
```

`app.js`:

```js
// 중간 실기 리허설 — app.js

const noticeButton = document.querySelector('#notice-button');
const noticeText = document.querySelector('#notice-text');
const darkButton = document.querySelector('#dark-button');

noticeButton.addEventListener('click', function () {
  noticeText.textContent = '이번 주 모임: 금요일 오후 5시';
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});

const joinForm = document.querySelector('#join-form');
const nameInput = document.querySelector('#name');
const reasonInput = document.querySelector('#reason');
const result = document.querySelector('#result');

joinForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const reason = reasonInput.value.trim();

  if (name === '') {
    result.textContent = '이름을 입력하세요';
    nameInput.focus();
    return;
  }

  result.textContent = `${name}: ${reason}`;
  joinForm.reset();
  nameInput.focus();
});

console.log('리허설 해답 준비 완료');
```

**예상 결과** — 내 파일과 다른 줄이 있어도 화면과 동작이 같으면 맞은 것이다. 문구·색·항목 내용은 달라도 된다.
Console에는 `리허설 해답 준비 완료` 한 줄만 있고 빨간 줄이 없다.

### 8. 리허설 저장소 만들고 Pages 켜기

여기서부터가 **시험 전에 끝내 두는 절차**다. 2주차에 한 것과 같은 순서다. 현재 폴더: `midterm-practice`

```bash
git init
git branch -M main
git config user.name "student01"
git config user.email "본인 이메일"
git add .
git commit -m "리허설 완성"
```

1. 브라우저에서 GitHub **+ › New repository**를 눌러 이름 `midterm-practice`, **Public**, **Add a README file**은 체크하지 않고 만든다.
2. 만든 화면의 HTTPS 주소를 복사한다. 현재 폴더: `midterm-practice`

```bash
git remote add origin https://github.com/student01/midterm-practice.git
git push -u origin main
```

**예상 결과**

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

3. **Settings › Pages › Build and deployment**에서 Source `Deploy from a branch`, Branch `main` · `/(root)` · **Save**.
4. 1분쯤 뒤 새로고침해 "Your site is live at …"가 보이면 **Visit site**를 누른다.

**예상 결과** — `https://student01.github.io/midterm-practice/`에서 리허설 화면이 열리고 버튼 두 개가 동작한다.

- 처음 push에서 **Connect to GitHub** 창이 뜨면 **Sign in with your browser**를 누른다. 시험 당일에는 이 창이 뜨지 않게 오늘 끝내 두는 것이다.
- 공용 PC라면 나가기 전에 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지운다.

## 2일차

### 9. my-web에 exam 폴더 만들기

본시험은 새 저장소를 만들지 않는다. 쓰던 `my-web` 안에 폴더 하나를 더 만든다. 현재 폴더: `my-web`

```bash
git pull
mkdir exam
git status
```

**예상 결과** — `git pull`은 새 commit이 없으면 `Already up to date.`이고, `git status`는 아래와 같다.

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

- git은 빈 폴더를 기억하지 않는다. 파일을 넣어야 `exam/`이 보인다. 그 확인은 10단계에서 한다.
- `my-web` 폴더가 없으면 `git clone https://github.com/student01/my-web.git`을 먼저 한다.

### 10. starter 세 파일 넣고 첫 commit 하기

배포된 시험용 starter 세 파일(`index.html`·`styles.css`·`app.js`)을 `exam/` 안에 넣는다. 구조는 리허설과 같다.

1. 탐색기에서 `my-web/exam/index.html`을 더블클릭한다.
2. 주소창이 `file:///…/my-web/exam/index.html`로 시작한다.
3. F12 **Console**에 빨간 줄이 없는지 본다.

**예상 결과** — 꾸미지 않은 시험 화면이 열리고 Console이 깨끗하다.

- 화면이 전혀 안 열리면 문제지가 아니라 **파일 위치**다. 세 파일이 `exam/` 안에 나란히 있어야 한다.
- 이 단계는 문제를 푸는 시간이 아니다. 실행만 확인하고 저장해 둔다.

파일이 들어갔으면 문제를 풀기 전에 한 번 저장해 올린다. 현재 폴더: `my-web`

```bash
git status
git add .
git commit -m "중간 실기 시작"
git push
```

**예상 결과** — `git status`는 이제 `exam/`을 알아본다.

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	exam/

nothing added to commit but untracked files present (use "git add" to track)
```

`git commit`은 아래와 같다.

```text
[main 09f0ac1] 중간 실기 시작
 3 files changed, 96 insertions(+)
 create mode 100644 exam/app.js
 create mode 100644 exam/index.html
 create mode 100644 exam/styles.css
```

- `96`은 손대지 않은 starter 세 파일의 줄 수 합이다(`index.html` 39 · `styles.css` 33 · `app.js` 24). 문제를 푼 뒤에는 이 숫자가 커진다.
- `git push`는 `main -> main`이 있는 줄이 나오면 된 것이다. 앞뒤 일곱 글자는 PC마다 다르다.
- 이것이 **첫 번째 commit**이다. 여기까지 하고 시험을 시작한다.

### 11. 저장하고 push 하기

문제를 다 풀면 저장하고 올린다. 현재 폴더: `my-web`

```bash
git add .
git commit -m "중간 실기"
git push
```

**예상 결과**

```text
[main 1ea3c2e] 중간 실기
 3 files changed, 54 insertions(+), 15 deletions(-)
```

```text
To https://github.com/student01/my-web.git
   09f0ac1..1ea3c2e  main -> main
```

- 앞의 일곱 글자(`1ea3c2e`)는 PC마다 다르다. 이것이 제출할 commit SHA다.
- 바뀐 줄 수는 사람마다 다르다. `54`·`15`는 리허설 starter를 해답까지 고쳤을 때의 값이다.
- `nothing to commit, working tree clean`이 나오면 파일을 저장하지 않은 것이다. VS Code 탭 제목의 ● 표시를 본다.
- `! [rejected]        main -> main (fetch first)`가 나오면 `git pull` 뒤에 다시 `git push` 한다.
- 10단계의 첫 commit(`중간 실기 시작`)과 이 마지막 commit으로 **두 번 이상**이 된다. 중간에 한 번 더 해도 좋다.

### 12. 제출하기

현재 폴더: `my-web`

```bash
git log -1 --oneline
```

**예상 결과**

```text
1ea3c2e 중간 실기
```

1. 1~3분쯤 뒤 `https://student01.github.io/my-web/exam/`을 새로고침한다.
2. 완성 화면과 **주소창**이 함께 보이게 캡처한다.
3. 아래 네 가지를 제출한다.

```text
① https://student01.github.io/my-web/exam/
② https://github.com/student01/my-web
③ 1ea3c2e
④ 캡처 1장
```

- 공개 주소가 5분이 지나도 옛 화면이면 로컬 화면 캡처와 `git log -1 --oneline` 출력으로 대신 제출한다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 오류가 나면

브라우저에서는 F12 **Console**의 **첫 빨간 줄**을 읽는다. 줄 끝의 `app.js:7`이 파일 이름과 줄 번호다.
터미널에서는 첫 `error:` 또는 `fatal:` 줄을 읽는다. 자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 확인하고, 10분 넘게 같은 자리에 있으면 손을 들어 도움을 요청한다.
