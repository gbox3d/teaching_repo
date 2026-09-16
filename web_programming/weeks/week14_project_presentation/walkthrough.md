# 14주차 따라하기 — 마지막 손질과 3분 시연

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 주소와 글자의 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

**이번 주에도 확인과 캡처는 공개 주소에서 한다.** 방명록에 남긴 글은 브라우저마다 따로 저장되고,
프로젝트 카드는 파일을 더블클릭해 연 화면에서는 그려지지 않는다. 고칠 때마다 push하고 공개 주소를 새로고침한다.

이번 주에 고치는 파일은 `index.html`·`about.html`·`README.md` 셋뿐이다. CSS와 JavaScript는 한 글자도 고치지 않는다.

## 1일차

### 1. 저장소 열고 시작 루틴

VS Code **File › Open Folder**로 `my-web`을 열고 **Terminal › New Terminal**을 연다. 현재 폴더: `my-web`

```bash
git pull
git log --oneline
```

다른 PC에서 처음 시작한다면 `git pull` 대신 아래를 먼저 한다. 현재 폴더: 저장소를 둘 위치

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

**예상 결과** — `Already up to date.`가 나오거나 13주차에 push한 commit을 받아 온다.
`git log --oneline`에 13주차까지의 commit이 한 줄씩 보인다. 맨 위가 `방명록 글자 확인하고 alt·label 고치기`다.

- 집에서 고친 것이 있는데 `git pull`이 `error: Your local changes to the following files would be overwritten by merge:`로 멈추면
  먼저 `git add .` → `git commit`을 하고 다시 `git pull`을 한다. 자세한 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
- 탐색기에 네 개의 `.html`과 `app.js`·`about.js`·`guestbook.js`·`projects.js`·`styles.css`, `data/`·`images/`·`screenshots/` 폴더가 보인다.

### 2. 네 페이지가 모두 열리는지 확인하기

브라우저에서 공개 주소를 **새 시크릿 창**으로 연다. 채점자가 보는 화면과 같은 화면이다.

```text
https://student01.github.io/my-web/
```

| 확인할 것 | 어디서 |
|---|---|
| nav 링크 네 개가 서로 오간다 | 네 페이지 모두 |
| 버튼을 누르면 문장·배경색이 바뀌고 `클릭 N회`가 오른다 | `index.html` |
| 입학 연도를 넣고 누르면 `n년차`가 나온다 | `about.html` |
| 이름을 비우고 누르면 안내가 보이고, 넣고 누르면 목록에 쌓인다 | `guestbook.html` |
| 새로고침해도 목록이 남아 있다 | `guestbook.html` |
| 카드 세 장이 그려진다 | `projects.html` |

**예상 결과** — 여섯 가지가 모두 공개 주소에서 동작한다. F12 **Console**에 빨간 줄이 없다.

- 시크릿 창에서 404가 나면 저장소가 Private이거나 `main`에 `index.html`이 없는 것이다.
- 목록이 비어 있는 것은 정상이다. 시크릿 창은 저장된 글을 함께 쓰지 않는다. 그 자리에서 두세 줄 남겨 둔다.
- 하나라도 동작하지 않으면 [이번 주에 고치지 않는 파일](#이번-주에-고치지-않는-파일)에서 내 파일과 한 줄씩 비교한다.

### 3. 홈에 할 수 있는 것 목록 넣기

`index.html`의 `<p class="card" id="count">클릭 0회</p>` 줄 **아래**에 여덟 줄을 넣는다.
다섯 줄의 순서가 곧 발표 순서다.

```html
<h2>이 사이트에서 할 수 있는 것</h2>
<ol class="card">
  <li>위 메뉴로 네 페이지를 오갑니다.</li>
  <li>버튼으로 인사말과 배경색을 바꿉니다.</li>
  <li>방명록에 글을 남기고 지웁니다.</li>
  <li>남긴 글은 새로고침해도 그대로 있습니다.</li>
  <li>프로젝트 카드는 JSON 파일에서 읽어 옵니다.</li>
</ol>
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
      <p>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </p>
      <p class="card" id="count">클릭 0회</p>
      <h2>이 사이트에서 할 수 있는 것</h2>
      <ol class="card">
        <li>위 메뉴로 네 페이지를 오갑니다.</li>
        <li>버튼으로 인사말과 배경색을 바꿉니다.</li>
        <li>방명록에 글을 남기고 지웁니다.</li>
        <li>남긴 글은 새로고침해도 그대로 있습니다.</li>
        <li>프로젝트 카드는 JSON 파일에서 읽어 옵니다.</li>
      </ol>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul class="card">
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```
**예상 결과** — 저장하고 공개 주소를 새로고침하면(6단계의 push 뒤) `클릭 0회` 아래에
`이 사이트에서 할 수 있는 것`이라는 제목과 번호가 붙은 다섯 줄이 카드 안에 보인다.

- `<ol>`은 번호가 붙는 목록이다. 취미에 쓴 `<ul>`은 점이 붙는다. 3주차에 둘 다 배웠다.
- `class="card"`를 붙였으므로 흰 상자 안에 들어간다. 4주차에 만든 규칙이다.
- 다섯 줄을 본인 사이트에 맞게 고쳐도 된다. 다만 **줄 수와 발표 순서는 같게** 둔다.
- 여기까지 하면 발표 중에 다음에 할 일을 화면에서 볼 수 있다. 종이를 들고 읽지 않아도 된다.

### 4. 내 정보 표에 공개 주소 한 줄 넣기

`about.html`의 표에서 `관심 분야` 행 **아래**에 네 줄을 넣는다.

```html
<tr>
  <td>공개 주소</td>
  <td>https://student01.github.io/my-web/</td>
</tr>
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
    <script src="about.js" defer></script>
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <h2>한눈에 보기</h2>
      <p>수업용 가상 정보입니다.</p>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>아이디</td>
          <td>student01</td>
        </tr>
        <tr>
          <td>이메일</td>
          <td>student01@example.com</td>
        </tr>
        <tr>
          <td>관심 분야</td>
          <td>웹 페이지 만들기</td>
        </tr>
        <tr>
          <td>공개 주소</td>
          <td>https://student01.github.io/my-web/</td>
        </tr>
      </table>
      <h2>몇 년차일까요?</h2>
      <form id="year-form">
        <p>
          <label for="year">입학 연도</label>
          <input id="year" type="text">
          <button type="submit">계산하기</button>
        </p>
      </form>
      <p class="card" id="year-result">입학 연도를 적고 계산하기를 누르세요.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```
**예상 결과** — 내 정보 표가 다섯 행(항목·아이디·이메일·관심 분야·공개 주소)이 된다.

- 표의 한 행은 `<tr>`이고 그 안의 칸이 `<td>` 두 개다. 3주차에 만든 표에 행 하나를 더하는 것뿐이다.
- 주소는 글자로 적는다. 링크로 만들 필요는 없다. 지금 보고 있는 페이지가 그 주소이기 때문이다.
- 본인 아이디로 바꾼다. `student01`이 남아 있으면 채점에서 예시를 베낀 것으로 본다.

### 5. README 최종판 마무리하기

13주차에 쓴 `README.md`에서 **두 곳만** 고친다. 새로 쓰지 않는다.

1. `## 페이지`의 첫 줄(홈) 설명에 `할 수 있는 것 목록`을 넣는다.
   13주차에는 `인사말, 소개, 취미 목록`이었고, 이번 주에는 `인사말, 할 수 있는 것 목록, 소개, 취미 목록`이 된다.
   줄 앞의 링크 부분은 그대로 둔다. 전체 줄은 [examples/day1/README.md](examples/day1/README.md) 11번째 줄에 있다.

2. `## 만든 과정 (git log --oneline)`의 **맨 위**에 이번 주 commit 한 줄을 더한다. 6단계에서 commit한 뒤 그 값을 적는다.

```markdown
- 9b2f7c1 홈에 할 수 있는 것 목록 넣고 내 정보에 공개 주소 적기
```

3. 홈 화면이 바뀌었으므로 `screenshots/home.png`를 **다시 찍어 덮어쓴다.** 공개 주소에서 **[인사 바꾸기]**를 한 번 누른 뒤 찍는다.
   `guestbook.png`와 `projects.png`는 13주차 것을 그대로 둔다.

전체 파일은 [examples/day1/README.md](examples/day1/README.md)에 있다(52줄).

**예상 결과** — VS Code에서 `README.md`를 열고 오른쪽 위 **Open Preview**를 누르면 제목·목록·링크·그림이 들어간 문서로 보인다.
그림 세 장이 모두 나오고, `## 만든 과정`이 여섯 줄이 된다.

- 앞의 일곱 글자(`9b2f7c1`)는 PC마다 다르다. `git log --oneline`에서 **본인 값**을 옮겨 적는다.
- 그림이 깨져 보이면 `screenshots/` 안 파일 이름과 README에 적은 이름의 **대소문자**를 맞춘다.
- 이 파일이 레포트 8점이다. 별도 보고서 파일은 내지 않는다.

### 6. push하고 공개 주소에서 확인하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "홈에 할 수 있는 것 목록 넣고 내 정보에 공개 주소 적기"
git push
git log --oneline
```

**예상 결과**

```text
[main 9b2f7c1] 홈에 할 수 있는 것 목록 넣고 내 정보에 공개 주소 적기
 4 files changed, 14 insertions(+), 1 deletion(-)
```

1. 1~3분 뒤 공개 주소를 **시크릿 창**에서 새로고침한다.
2. 홈에 다섯 줄 목록이, 내 정보에 공개 주소 행이 보인다.
3. `git log --oneline` 맨 위 줄의 일곱 글자를 5단계의 README에 옮겨 적고 다시 `add → commit → push` 한다.

- 줄 수는 본인 캡처 크기에 따라 다르다. 파일이 네 개(`index.html`·`about.html`·`README.md`·`screenshots/home.png`)면 맞다.
- 5분이 지나도 옛 화면이면 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다. 그래도 그대로면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
- 공용 PC라면 오늘 작업이 끝난 뒤 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지운다.

### 7. 3분 리허설 해 보기

[3분 시연 흐름 표](examples/demo_outline.md)를 옆에 두고 짝과 번갈아 한 번씩 3분을 재며 해 본다.

```text
0:00  공개 주소를 열고 한 줄 소개        1:15  이름·메시지를 넣고 [남기기], 한 줄 [삭제]
0:20  nav로 네 페이지                    1:45  새로고침 — 목록이 남아 있다
0:40  홈에서 [다크 모드] 클릭            2:05  프로젝트 카드 세 장
0:55  칸을 비우고 [남기기] → 안내        2:35  Commits 탭과 README
```

**예상 결과** — 3분 안에 여덟 줄이 모두 끝난다. 넘치면 어디를 줄일지 정한다. 대개 첫 소개와 카드 설명이 길다.

- 말하면서 누른다. 누르고 나서 설명하면 시간이 두 배가 된다.
- 듣는 짝은 점수를 매기지 않는다. 넘긴 시간과 빠뜨린 줄만 적어 준다.
- 조교 1:1 확인에서는 공개 주소와 README 두 가지만 본다.

## 2일차

### 8. 발표 전 탭 세 개 준비하기

자기 차례 두 사람 앞에서 브라우저 탭 세 개를 연다.

```text
탭 1  https://student01.github.io/my-web/            ← 시크릿 창
탭 2  https://github.com/student01/my-web
탭 3  https://github.com/student01/my-web/commits
```

**예상 결과** — 세 탭이 모두 열려 있고, 탭 1은 홈 화면이 밝은 배경에 `클릭 0회`인 처음 상태다.

- 방명록에는 글 두세 줄을 미리 남겨 둔다. 발표 중에 한 줄 더 남기고 하나를 지우는 것이 목록 점수다.
- 시크릿 창은 저장된 글을 함께 쓰지 않는다. 시크릿 창으로 발표한다면 **그 창에서** 미리 두세 줄을 남겨 둔다.
- 다크 모드는 꺼 두고 시작한다. 0:40에 눌러서 바뀌는 것을 보여 준다.
- 다른 사이트나 로그인 화면이 보이는 탭은 닫는다.

### 9. 3분 시연 순서대로 해 보기

7단계에서 연습한 여덟 줄을 그대로 한다. 말하면서 누른다.

1. 탭 1을 보이며 "`student01`의 웹 연습장입니다. 네 페이지가 있고, 남긴 글이 새로고침해도 남습니다."
2. nav로 홈 → 내 정보 → 방명록 → 프로젝트 → 홈. 내 정보 표의 **공개 주소** 행을 한 번 짚는다.
3. 홈에서 **[다크 모드]**를 누르며 "배경색이 바뀌고 클릭 횟수가 오릅니다."
4. 방명록에서 칸을 비운 채 **[남기기]** → 안내 문장.
5. 이름·메시지를 넣고 **[남기기]**, 한 줄을 **[삭제]**.
6. 같은 페이지를 **새로고침**한다. 목록이 그대로다.
7. 프로젝트 페이지에서 "카드 세 장은 제가 쓴 `data/projects.json`에서 읽어 온 것입니다."
8. 탭 3의 **Commits** 탭과 탭 2의 README를 보이며 마무리.

**예상 결과** — 3분 안에 끝나고, 채점자가 여덟 가지를 모두 화면에서 확인한다.

- 코드 파일은 띄우지 않는다. 구술 질문("이 버튼을 누르면 어느 함수가 실행됩니까?")을 받으면 그때 연다.
- 잘 안 되는 기능이 있으면 그 줄을 지우고 되는 것부터 보여 준다. 남은 시간에 원인을 말하면 시간 점수는 유지된다.
- 공개 주소가 열리지 않으면 손을 들어 알린다. 시크릿 창 → 로컬 시연 순서로 같은 배점을 받는다.

### 10. 발표가 끝나면

1. 남의 발표를 들으며 채점표를 본다. 자기 코드는 고치지 않는다.
2. 마지막 10분에 README를 고칠 것이 있으면 고쳐 올린다. 현재 폴더: `my-web`

```bash
git add .
git commit -m "README 다듬기"
git push
```

3. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

**예상 결과** — `git status`가 `nothing to commit, working tree clean`이고, 저장소 첫 화면에 최종 README가 보인다.

- 고칠 것이 없으면 `nothing to commit, working tree clean`이 나온다. 그것도 정상이다.
- 제출은 발표 3분과 캡처 1장(저장소 첫 화면)이다. 제출 위치와 마감은 수업 공지를 따른다.

## 이번 주에 고치지 않는 파일

아래 여덟 파일은 13주차와 같다. 내 파일이 예제와 다르면 여기서 한 줄씩 비교한다.
1단계에서 파일이 없거나 동작하지 않는 학생만 그대로 넣어 오늘 발표를 준비한다.

`styles.css` (같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다):

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

h1 {
  color: #1f3a93;
  font-size: 28px;
}

h2 {
  color: #3157d5;
}

nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

nav a {
  color: #3157d5;
}

.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}

input,
textarea {
  width: 280px;
  max-width: 100%;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}

body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```
`app.js` — 홈의 인사말·클릭 횟수·다크 모드 (같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다):

```js
const name = 'student01';
const hour = new Date().getHours();
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');
const darkButton = document.querySelector('#dark-button');
let count = 0;

function greet(name) {
  return `안녕하세요, ${name}님!`;
}

function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}

greeting.textContent = `${greet(name)} ${hello(hour)}`;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  countUp();
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
  countUp();
});
```
`about.js` — 입학 연도로 몇 년차인지 계산 (같은 파일이 [examples/day1/about.js](examples/day1/about.js)에 있다):

```js
const yearForm = document.querySelector('#year-form');
const yearInput = document.querySelector('#year');
const yearResult = document.querySelector('#year-result');

yearForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const text = yearInput.value.trim();
  const year = Number(text);
  if (text === '' || isNaN(year)) {
    yearResult.textContent = '입학 연도를 숫자로 적어 주세요.';
    yearInput.focus();
    return;
  }
  const thisYear = new Date().getFullYear();
  const years = thisYear - year + 1;
  yearResult.textContent = `${year}년에 입학했으니 올해 ${years}년차입니다.`;
  yearInput.focus();
});
```
`guestbook.html` (같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다):

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
    <script src="guestbook.js" defer></script>
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <h3>쓰는 순서</h3>
      <ol>
        <li>이름을 적는다.</li>
        <li>메시지를 적는다.</li>
        <li>남기기 버튼을 누른다.</li>
      </ol>
      <form id="guestbook-form">
        <p>
          <label for="name">이름</label>
          <input id="name" type="text">
        </p>
        <p>
          <label for="email">이메일</label>
          <input id="email" type="email">
        </p>
        <p>
          <label for="message">메시지</label>
          <textarea id="message" rows="4"></textarea>
        </p>
        <button type="submit">남기기</button>
      </form>
      <p id="notice"></p>
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <p id="count">아직 남긴 글이 없습니다.</p>
      <p><button id="clear-button" type="button">전체 지우기</button></p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```
`guestbook.js` — 목록 추가·삭제와 브라우저 저장 (같은 파일이 [examples/day1/guestbook.js](examples/day1/guestbook.js)에 있다):

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
let items = JSON.parse(localStorage.getItem('guestbook')) || [];

function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      saveList();
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  saveList();
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});

showList();
```
`projects.html` (같은 파일이 [examples/day1/projects.html](examples/day1/projects.html)에 있다):

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 프로젝트</title>
    <link rel="stylesheet" href="styles.css">
    <script src="projects.js" defer></script>
  </head>
  <body>
    <header>
      <h1>프로젝트</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
        <a href="projects.html">프로젝트</a>
      </nav>
    </header>
    <main>
      <h2>지금까지 만든 것</h2>
      <p>아래 카드는 data/projects.json 파일에서 읽어 옵니다.</p>
      <p id="notice"></p>
      <div id="project-list"></div>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```
`projects.js` — JSON 파일을 불러와 카드 세 장 (같은 파일이 [examples/day1/projects.js](examples/day1/projects.js)에 있다):

```js
const projectList = document.querySelector('#project-list');
const notice = document.querySelector('#notice');

function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const image = document.createElement('img');
    image.src = projects[i].image;
    image.alt = `${projects[i].title} 화면 그림`;
    image.width = 240;
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    const description = document.createElement('p');
    description.textContent = projects[i].description;
    const link = document.createElement('a');
    link.href = projects[i].link;
    link.textContent = `${projects[i].title} 열기`;
    article.append(image, title, description, link);
    projectList.append(article);
  }
}

async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    if (!response.ok) {
      notice.textContent = '프로젝트를 불러오지 못했습니다.';
      return;
    }
    const projects = await response.json();
    notice.textContent = '';
    showProjects(projects);
  } catch (error) {
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
  }
}

loadProjects();
```
`data/projects.json` (같은 파일이 [examples/day1/data/projects.json](examples/day1/data/projects.json)에 있다):

```json
[
  {
    "title": "자기소개 페이지",
    "description": "홈 화면입니다. 이름과 소개, 취미 목록을 적었습니다.",
    "image": "images/project1.png",
    "link": "index.html"
  },
  {
    "title": "내 정보 표",
    "description": "아이디와 이메일, 관심 분야를 표로 정리했습니다.",
    "image": "images/project2.png",
    "link": "about.html"
  },
  {
    "title": "방명록",
    "description": "이름과 메시지를 남기면 목록에 저장되는 페이지입니다.",
    "image": "images/project3.png",
    "link": "guestbook.html"
  }
]
```
**예상 결과** — 여덟 파일을 그대로 두고 공개 주소를 열면 2단계의 여섯 가지가 모두 동작한다.

- `guestbook.js`의 저장 이름은 `guestbook`이다. 15주차 기말 starter는 다른 이름(`final-items`)을 쓴다.
- `projects.js`는 `data/projects.json`을 상대 경로로 부른다. 앞에 `/`를 붙이면 공개 주소에서 404가 난다.
- 함수 이름·id 이름을 바꾸지 않는다. 구술 질문이 이 이름으로 나온다.

## 오류가 나면

터미널에서는 첫 `error:` 또는 `fatal:` 줄을 읽는다. `hint:` 줄은 git이 알려 주는 해결 방법이다.
브라우저에서는 F12 **Console**의 첫 빨간 줄을 읽는다. 줄 끝의 `guestbook.js:14`가 파일 이름과 줄 번호다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 화면을 그대로 보여 주고 도움을 요청한다.
