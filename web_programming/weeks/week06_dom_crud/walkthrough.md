# 6주차 따라하기 — 클릭 카운터와 다크 모드

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면이나 Console에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주 확인 도구는 **Elements**와 **Console** 두 탭이다. 브라우저에서 **F12**(또는 우클릭 › 검사)를 누른다.
이번 주 작업은 `dark-mode` 브랜치에 쌓인다. 공개 페이지는 2일차 마지막에 한 번만 바뀐다.

## 1일차

### 1. 저장소 받아오기

지난주에 쓰던 PC라면 폴더를 열고 새 commit만 받아 온다. 현재 폴더: `my-web`

```bash
git pull
```

**예상 결과** — 집에서 push한 것이 없으면 `Already up to date.` 한 줄이다.

처음 쓰는 PC라면 저장소를 통째로 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

**예상 결과** — `Cloning into 'my-web'...`로 시작하고 `my-web` 폴더가 생긴다. **File › Open Folder**로 그 폴더를 연다.

- `fatal: destination path 'my-web' already exists and is not an empty directory.`가 나오면 이미 받아 둔 것이다. 그 폴더를 열고 `git pull`을 한다.
- 로그인이 막혀 clone이 안 되면 조교에게 5주차 `examples/day2` 파일을 받아 새 폴더에서 작업하고, 끝 루틴에서 `git remote add origin <URL>` 뒤에 push한다.

### 2. dark-mode 브랜치 만들기

오늘 작업할 브랜치를 만들면서 그 브랜치로 옮겨 간다. 현재 폴더: `my-web`

```bash
git status
git switch -c dark-mode
git branch
```

**예상 결과**

```text
Switched to a new branch 'dark-mode'
* dark-mode
  main
```

- 시작 전 `git status`가 `nothing to commit, working tree clean`이어야 한다. 아니면 먼저 commit한다.
- `-c`는 "만들면서 옮겨 가라"는 뜻이다. 3주차 `guestbook` 브랜치를 만들 때와 같은 명령이다.
- 폴더의 파일은 그대로 보인다. 지금부터의 commit이 `dark-mode`에 쌓인다.
- `*`가 지금 있는 브랜치다. main은 그대로 남아 있고 공개 페이지도 그대로다.

### 3. 버튼과 카운터 자리 만들기

`index.html`을 열고 `#greeting` 카드 **바로 아래**에 두 문단을 넣는다.

```html
      <p>
        <button id="hello-button" type="button">인사 바꾸기</button>
      </p>
      <p class="card" id="count">클릭 0회</p>
```

여기까지 하면 `index.html` 전체가 아래와 같다. 5주차 파일에서 이 네 줄만 늘었다.
같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

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
      </nav>
    </header>
    <main>
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
      <p>
        <button id="hello-button" type="button">인사 바꾸기</button>
      </p>
      <p class="card" id="count">클릭 0회</p>
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

**예상 결과** — 새로고침하면 인사말 카드 아래에 `인사 바꾸기` 버튼과 `클릭 0회` 카드가 보인다. 눌러도 아직 아무 일도 없다.

- `type="button"`을 꼭 붙인다. 지금은 폼 밖이라 붙이지 않아도 새로고침되지 않지만, 7주차 폼 안의 버튼과 습관을 맞추려고 지금부터 붙인다.
- `id`는 한 페이지에 하나씩만 쓴다. 지금 `index.html`에는 `greeting`·`count`·`hello-button` 세 개가 있다.
- 버튼은 꾸미지 않는다. 브라우저 기본 모양 그대로 둔다.

### 4. 요소를 찾아 두기

`app.js`를 연다. 5주차에 쓴 코드가 그대로 있다. **맨 위 두 줄 아래**에 찾아 두는 줄 세 개를 넣는다.

```js
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');

console.log(greeting);
```

**예상 결과** — Console에 요소가 통째로 한 줄 찍힌다. 삼각형을 누르면 펼쳐진다.

```text
<p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

- `document`는 **페이지 전체**다. 브라우저가 미리 만들어 둔다.
- `querySelector('#greeting')`은 `id`가 `greeting`인 요소 **하나**를 찾아 돌려준다. `#`은 `id`를 찾으라는 표시다.
- 찾은 것을 `const`에 담아 두면 그다음부터는 `greeting`이라는 짧은 이름으로 쓴다.
- `null`이 찍히면 못 찾은 것이다. `index.html`의 `id` 철자와 비교한다.
- 확인했으면 `console.log(greeting);` 줄은 지운다.

### 5. 5주차 두 줄을 한 줄로 합치기

`app.js` 아래쪽에 5주차에 쓴 네 줄이 있다. 이 네 줄을 지운다.

```js
const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
```

대신 한 줄로 쓴다.

```js
greeting.textContent = `${greet(name)} ${hello(hour)}`;
```

**예상 결과** — 화면은 5주차와 똑같다. 인사말 카드에 `안녕하세요, student01님! 좋은 아침입니다.`가 보인다.

- 5주차의 복붙 틀 한 줄이 오늘 둘로 나뉘었다. 4단계에서 **찾아 두고**(`querySelector`), 여기서 **바꾼다**(`textContent`).
- `.textContent`는 요소 안의 글자다. `=` 왼쪽에 두면 바꿔 넣는다는 뜻이다.
- `greet`·`hello` 두 함수는 5주차 그대로 쓴다. 지우지 않는다.

### 6. 클릭하면 인사말 바꾸기

`app.js` 맨 아래에 클릭했을 때 실행될 코드를 맡겨 둔다.

```js
helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
});
```

**예상 결과** — 새로고침한 뒤 `인사 바꾸기`를 누르면 카드 글자가 `반갑습니다. 오늘도 좋은 하루 되세요.`로 바뀐다.

- "이 버튼을 **클릭하면** 이 함수를 실행하라"고 브라우저에 맡겨 두는 줄이다.
- 맡기는 순간에는 실행되지 않는다. 누를 때마다 중괄호 안이 실행된다.
- 리스너는 `function () { }` 모양으로 쓴다. 2주차 `app.js`에 있던 `() =>`는 틀로만 본 것이다.
- 새로고침하면 HTML에 적힌 글자로 돌아간다. 화면만 바뀌었지 파일은 그대로이기 때문이다.

### 7. 클릭 횟수 세기

찾아 두는 줄 아래에 `let count = 0;`을 넣고, 리스너 안에서 1씩 올린다.

```js
let count = 0;
```

```js
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
```

여기까지 하면 `app.js` 전체가 아래와 같다. 같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다.

```js
const name = 'student01';
const hour = new Date().getHours();
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');
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

greeting.textContent = `${greet(name)} ${hello(hour)}`;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
});
```

**예상 결과** — 버튼을 누를 때마다 숫자가 오른다.

```text
1번 누름: 클릭 1회
2번 누름: 클릭 2회
3번 누름: 클릭 3회
```

- `let count = 0;`은 리스너 **밖**에 둔다. 안에 두면 누를 때마다 0에서 다시 시작해 계속 `클릭 1회`만 나온다.
- `count = count + 1;`은 "지금 값에 1을 더해 다시 넣어라"는 뜻이다. 5주차의 `hour = 15;`와 같은 모양이다.
- 숫자를 문장에 넣을 때는 5주차의 템플릿 문자열을 쓴다. 백틱은 영문 입력 상태에서 친다.
- 새로고침하면 `클릭 0회`로 돌아간다. 새로고침해도 남게 하는 것은 11주차에 배운다.

### 8. null 오류 두 가지 만들어 보기

같은 오류가 나는 두 가지 원인을 직접 만들어 본다. 하나씩 만들고, 읽고, **바로 되돌린다.**

먼저 `app.js`의 선택자에 오타를 낸다.

```js
const helloButton = document.querySelector('#hello-buton');
```

**예상 결과** — Console에 빨간 줄이 뜨고 버튼이 동작하지 않는다.

```text
Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')      app.js:22
```

되돌린 뒤, 이번에는 `index.html`의 `script` 줄에서 `defer`만 지운다.

```html
    <script src="app.js"></script>
```

**예상 결과** — 이번에는 인사말조차 표시되지 않고 다른 빨간 줄이 뜬다.

```text
Uncaught TypeError: Cannot set properties of null (setting 'textContent')      app.js:20
```

- 두 줄 모두 원인은 하나다. **찾지 못해서 `null`이 나왔다.** `null`에는 아무것도 붙일 수 없다.
- 첫 번째는 철자가 틀려서 못 찾았다. 두 번째는 `defer`가 없어 HTML을 다 읽기 전에 찾으러 갔기 때문이다.
- `defer`는 "HTML을 다 읽은 뒤에 실행하라"는 뜻이다. 5주차에 예고한 그 단어다.
- 확인했으면 **반드시 원래대로 되돌린다.** 오류가 있는 채로 commit하지 않는다.

### 9. 나머지 파일은 그대로 둔다

`styles.css`·`about.html`·`guestbook.html`은 1일차에 **한 글자도 고치지 않는다.** 폴더에 그대로 있는지만 확인한다.

`styles.css` — 같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다.

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
```

`about.html` — 같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
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
      </table>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`guestbook.html` — 같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
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
      <form>
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
      <p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 세 페이지 모양은 5주차와 같다. `about.html`·`guestbook.html`을 열면 Console이 비어 있다.

- 두 페이지에는 `script` 줄이 없어서 `app.js`가 실행되지 않는다. 방명록 동작은 7주차에 `guestbook.js`로 만든다.
- `styles.css`의 `.card`는 2일차에 어두운 색 규칙이 함께 쓸 class다. 지우지 않는다.

**1일차 끝 루틴** — 현재 폴더: `my-web`

```bash
git add .
git commit -m "버튼을 누르면 인사말과 클릭 횟수가 바뀌게 만들기"
git push -u origin dark-mode
```

**예상 결과**

```text
[dark-mode 69b950c] 버튼을 누르면 인사말과 클릭 횟수가 바뀌게 만들기
 2 files changed, 14 insertions(+), 5 deletions(-)
 * [new branch]      dark-mode -> dark-mode
branch 'dark-mode' set up to track 'origin/dark-mode'.
```

1. GitHub 저장소 화면의 브랜치 드롭다운(`main ▾`)에서 `dark-mode`가 보이는지 확인한다.
2. **공개 페이지는 아직 그대로다.** Pages는 `main`만 배포하기 때문이며 정상이다.
3. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 앞의 일곱 글자(`69b950c`)는 PC마다 다르다.
- 처음 올리는 브랜치이므로 `-u origin dark-mode`가 필요하다. `git push`만 치면 `fatal: The current branch dark-mode has no upstream branch.`가 나온다.

## 2일차

### 10. 저장소 받아와 브랜치로 돌아가기

현재 폴더: `my-web`

```bash
git pull
git switch dark-mode
git branch
```

**예상 결과** — `Switched to branch 'dark-mode'`가 보이고 `*`가 `dark-mode`에 있다.

- 1일차 끝에 `dark-mode`에 있었다면 이미 그 브랜치다. `Already on 'dark-mode'`가 나온다.
- 다른 PC에서 clone한 학생은 `git switch dark-mode` 한 번으로 그 브랜치를 받아 온다.
- `fatal: invalid reference: dark-mode`가 나오면 1일차 push를 안 한 것이다. `git switch -c dark-mode`로 새로 만들고 2단계부터 한다.

### 11. 다크 모드 버튼 넣기

`index.html`에서 3단계에 만든 `<p>` **안에** 버튼을 한 줄 더 넣는다.

```html
        <button id="dark-button" type="button">다크 모드</button>
```

여기까지 하면 `index.html` 전체가 아래와 같다. 1일차 파일에서 이 한 줄만 늘었다.
같은 파일이 [examples/day2/index.html](examples/day2/index.html)에 있다.

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
      </nav>
    </header>
    <main>
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
      <p>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </p>
      <p class="card" id="count">클릭 0회</p>
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

**예상 결과** — 새로고침하면 `인사 바꾸기` 옆에 `다크 모드` 버튼이 나란히 보인다. 눌러도 아직 아무 일도 없다.

- 두 버튼을 같은 `<p>` 안에 두었으므로 한 줄에 나란히 보인다.
- `id`는 `dark-button`이다. 3단계의 `hello-button`과 다른 이름이어야 한다.

### 12. 어두운 색 규칙 더하기

`styles.css`를 열고 **맨 아래**에 규칙 하나를 더한다. 위의 53줄은 그대로 둔다.

```css
body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

여기까지 하면 `styles.css` 전체가 아래와 같다. 같은 파일이 [examples/day2/styles.css](examples/day2/styles.css)에 있다.

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

**예상 결과** — 화면은 아직 그대로다. `<body>`에 class `dark`가 없기 때문이다.

- `body.dark`는 "`<body>`에 class `dark`가 붙었을 때"라는 뜻이다. **사이를 띄우지 않는다.**
- `body.dark .card`는 띄어 썼다. "그 안에 있는 `.card`"라는 뜻이다(4주차 선택자).
- 쉼표로 이어 쓰면 두 대상에 같은 규칙을 준다.
- 규칙을 미리 적어 두고, 다음 단계에서 JavaScript가 class를 붙인다.

### 13. classList.toggle로 다크 모드 켜고 끄기

`app.js`의 찾아 두는 줄에 버튼 하나를 더하고, 맨 아래에 리스너를 하나 더 맡긴다.

```js
const darkButton = document.querySelector('#dark-button');
```

```js
darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});
```

**예상 결과** — `다크 모드`를 누르면 배경과 카드가 어두워지고, 다시 누르면 돌아온다.

- `classList`는 그 요소가 달고 있는 **class 이름 목록**이다.
- `toggle('dark')`은 **없으면 붙이고 있으면 뗀다.** 버튼 하나로 켜고 끄기에 맞는다.
- `add('dark')`를 쓰면 한 번 켜진 뒤 꺼지지 않는다. `remove('dark')`는 떼기만 한다.
- DevTools **Elements** 탭에서 `<body>`가 `<body class="dark">`로 바뀌는 것을 눈으로 확인한다.
- class는 붙는데 색이 그대로면 12단계의 CSS 철자를 본다. JavaScript는 class만 붙이고 색은 CSS가 정한다.

### 14. 두 버튼이 한 함수를 쓰게 정리하기

두 버튼이 똑같이 하는 일("횟수를 1 올리고 화면에 쓴다")을 함수로 빼낸다.
`hello`·`greet` 함수 아래에 `countUp`을 만들고, 두 리스너에서 부른다.

```js
function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}
```

```js
  countUp();
```

여기까지 하면 `app.js` 전체가 아래와 같다. 같은 파일이 [examples/day2/app.js](examples/day2/app.js)에 있다.

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

**예상 결과** — `인사 바꾸기` 2번, `다크 모드` 1번을 누르면 두 버튼의 합계가 세어진다.

```text
클릭 3회
```

- 같은 두 줄을 두 곳에 쓰지 않는다. 한 곳에 두고 두 리스너가 **부른다.**
- 부를 때는 괄호를 붙인다. `countUp;`이라고만 쓰면 아무 일도 일어나지 않는다.
- 돌려줄 값이 없으므로 `return`은 쓰지 않는다. 하는 일만 있는 함수다.
- 나중에 `클릭 ${count}번`으로 바꾸고 싶으면 이 함수 한 곳만 고치면 된다.

### 15. 오늘 작업 commit하고 push 하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "다크 모드 버튼과 countUp 함수 추가"
git push
```

**예상 결과**

```text
[dark-mode 9a76325] 다크 모드 버튼과 countUp 함수 추가
 3 files changed, 19 insertions(+), 2 deletions(-)
   69b950c..9a76325  dark-mode -> dark-mode
```

- 1일차에 `-u`로 올려 두었으므로 이번에는 `git push`만 친다.
- **이 push를 건너뛰지 않는다.** 1일차에 push해 둔 브랜치라, 건너뛰면 16단계의 `git branch -d`가 `error: the branch 'dark-mode' is not fully merged`로 거부된다.

### 16. main에 합치고 브랜치 지우기

현재 폴더: `my-web`

```bash
git switch main
git merge dark-mode
git push
git branch -d dark-mode
```

**예상 결과**

```text
Switched to branch 'main'
Updating e1bf03b..9a76325
Fast-forward
 app.js     | 23 +++++++++++++++++++----
 index.html |  5 +++++
 styles.css |  6 ++++++
 3 files changed, 30 insertions(+), 4 deletions(-)
   e1bf03b..9a76325  main -> main
Deleted branch dark-mode (was 9a76325).
```

- `git switch main` 직후 화면이 5주차로 돌아간다. 버튼이 사라져 보이지만 정상이다. merge하면 돌아온다.
- main에 다른 commit이 없으므로 항상 `Fast-forward`다. 합칠 것을 고르라는 창이 뜨지 않는다.
- merge만 하고 push하지 않으면 공개 페이지는 그대로다. **push까지 해야** 바뀐다.
- `git branch`를 치면 `* main` 하나만 남는다. GitHub에 올라간 브랜치도 지우려면 `git push origin --delete dark-mode`를 한다(선택).

### 17. 2일차 끝 루틴과 제출

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침한다.
2. `인사 바꾸기`와 `다크 모드`를 눌러 **다크 모드가 켜진 화면**을 만든다.
3. 주소창이 함께 보이게 한 화면을 캡처한다. 이 한 장이 이번 주 제출물이다.
4. DevTools 기기 모드(**Ctrl+Shift+M**)로 375px과 1280px에서도 확인한다.
5. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 오늘 작업은 15단계에서 이미 commit했다. 끝 루틴에서 `git commit`을 다시 하면 `nothing to commit, working tree clean`이 나오는데 그것도 정상이다.
- `클릭 0회`인 채로 찍지 않는다. 눌러 본 것이 보이도록 **1 이상**으로 만든다.
- 375px에서는 4주차 `@media` 규칙이 살아 있어 nav가 세로로 접힌다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 오류가 나면

먼저 Console의 **첫 빨간 줄**을 읽는다. 오른쪽의 `app.js:22`가 고칠 자리다.
이번 주 오류는 대부분 `null`이다. **찾지 못했다**는 뜻이므로 `id` 철자와 `script` 줄의 `defer`를 차례로 본다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
