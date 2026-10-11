[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud)

# 6주차 따라하기 — 비교 예제로 원리를 보고 마지막에 조립

이번 주는 새 저장소 `web-week06`을 만든다. 지난주 완성본을 넣고, 비교 예제는 그 안의 `ex/` 폴더에 저장한다. 값·줄을 바꾼 뒤 결과를 화면과 **F12 › Console**, **F12 › Elements**에서 본다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

비교 예제 6개는 교재 저장소의 [examples/day1](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud/examples/day1)(1일차 ex01~ex03과 고르기 페이지)과 [examples/day2](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud/examples/day2)(2일차 ex04~ex06) 폴더에 있다.
각 파일이 무엇을 비교하는지는 [예제 설명](examples/README.md)에, 바꿔 볼 값은 [실습지](lab.md)에 있다.

## 1일차

### 1. web-week06 폴더 만들고 지난주 완성본 넣기

저장소를 둘 위치(문서 폴더 등)에 새 폴더 `web-week06`을 만들고 VS Code **File › Open Folder**로 연다.

지난주 완성본을 넣는다. 내 `web-week05` 저장소 GitHub 화면에서 **Code › Download ZIP**을 누르고, 압축을 푼 폴더에서 맨 위 파일(`index.html`·`about.html`·`guestbook.html`·`styles.css`·`app.js`·`server.mjs`)과 `images/`를 `web-week06`으로 옮긴다. 지난주 `ex/` 폴더는 옮기지 않는다.
ZIP을 못 받았으면 교재 [5주차 `examples/day2/web-week05/`](../week05_javascript_data/examples/day2/web-week05/)의 파일을 2단계와 같은 **Raw** 방법으로 받고, [server.mjs](../../tools/static-server/server.mjs)도 같은 방법으로 받는다.

이어서 `web-week06` 안에 `ex` 폴더를 만든다. 현재 폴더: `web-week06`

```bash
mkdir ex
```

**예상 결과** — VS Code 탐색기가 아래 모양이다.

```text
web-week06/
  ex/            ← 아직 비어 있다
  images/
  about.html
  app.js
  guestbook.html
  index.html
  server.mjs
  styles.css
```

- `index.html`을 두 번 눌러 열면 5주차 완성 화면(인사말 카드)이 보인다. 이번 주는 여기서 시작한다.
- `index.html`·`styles.css`·`app.js`는 오늘 건드리지 않는다. 2일차 끝에 조립한다.

### 2. 비교 예제 가져오기

오늘 파일은 네 개다. 고르기 페이지 `index.html` 하나와 예제 코드 `.js` 세 개다. 세 예제가 같은 화면(글자 자리 하나, 버튼 하나, 횟수 자리 하나)을 쓰기 때문에 화면은 `index.html` 하나에 두고 코드만 따로 뗐다.

| 파일 | 비교하는 것 |
|---|---|
| [index.html](examples/day1/index.html) | 고르기 페이지. 맨 아래 `<script src>` 세 줄 중 하나만 켠다. 예제가 쓰는 자리(`#message`·`#btn`·`#count`)가 여기 있다 |
| [ex01_dom.js](examples/day1/ex01_dom.js) | `document` / 찾은 요소 / JS 가 바꾼 글자 — 화면·Elements·페이지 소스에서 비교 |
| [ex02_click_write.js](examples/day1/ex02_click_write.js) | 열 때 바꾸기 / 클릭할 때 바꾸기 |
| [ex03_counter.js](examples/day1/ex03_counter.js) | 함수 밖의 `let count` / 함수 안의 `let inside` |

[교재 저장소 examples/day1 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud/examples/day1)에서 파일을 누르고 오른쪽 위 **Raw**를 누른다. 코드만 보이는 화면에서 **Ctrl+S**(macOS는 ⌘+S)로 `web-week06/ex/`에 저장한다. 파일 이름은 교재와 **같게** 둔다. Raw가 열리지 않을 때만 주석 줄까지 그대로 친다.

**예상 결과** — `ex/` 안에 파일 네 개가 있다.

```text
ex/
  ex01_dom.js
  ex02_click_write.js
  ex03_counter.js
  index.html
```

- 저장한 파일 이름이 `.txt`로 끝나면 이름을 고친다. 이름은 VS Code 탐색기에서 확인한다.
- `ex/index.html`은 예제를 고르는 페이지다. 맨 위 `index.html`(내 사이트)과 이름이 같지만 다른 파일이다. 탭 이름 옆 폴더 경로로 구분한다.

### 3. 고르기 페이지와 Elements 탭

`ex/index.html`을 Chrome으로 연다(VS Code 탐색기에서 오른쪽 클릭 › **Reveal in File Explorer**, macOS는 **Reveal in Finder** → 두 번 누르기). `.js` 파일은 두 번 누르지 않는다. `.js`는 `index.html`이 불러온다.

VS Code에서 `ex/index.html`도 열어 맨 아래를 본다.

```html
<script src="ex01_dom.js"></script>
<!-- <script src="ex02_click_write.js"></script> -->
<!-- <script src="ex03_counter.js"></script> -->
```

지금은 ex01 줄만 켜져 있다. 다른 예제로 바꿀 때는 켜 둔 줄에 커서를 두고 **Ctrl+/**(macOS **⌘+/**)로 주석으로 만들고, 볼 줄에서 다시 **Ctrl+/** 로 주석을 푼다. 저장 → 새로고침한다. 한 번에 한 줄만 켠다.

**예상 결과** — 화면의 "예제가 쓰는 자리" 첫 줄이 `3. JavaScript 가 바꾼 글자`다. F12 › **Console**에 두 줄이 찍혀 있다.

```text
1. document : #document          ex01_dom.js:6
2. message : <div id="message">…  ex01_dom.js:7
```

이번 주에는 **Elements** 탭도 쓴다. DevTools 위쪽 탭에서 **Elements**를 누른다. 브라우저가 지금 보여 주는 요소 상자(DOM)가 들여쓰기로 보인다. `<body>` 앞의 ▶를 눌러 펼치고 `<div id="message">` 줄을 찾는다.

**예상 결과** — Elements의 그 줄 글자는 `3. JavaScript 가 바꾼 글자`다. 페이지 소스 보기(**Ctrl+U**, macOS **⌘+Option+U**)의 같은 줄은 `원래 글자 — HTML 파일에 적힌 글자`다.

- 페이지 소스는 **파일**이고, Elements는 브라우저가 그 파일을 읽어 만든 뒤 JavaScript가 바꾼 **DOM**이다. 화면은 DOM을 보여 준다.
- Elements에서 줄 위에 마우스를 올리면 화면의 그 요소가 파랗게 표시된다. 화면과 줄을 맞춰 볼 때 쓴다.
- Elements에서 고친 것은 파일에 저장되지 않는다. 새로고침하면 사라진다.

### 4. 값 바꾸는 요령

실험은 늘 같은 순서다. **VS Code에서 고치고 저장**(Ctrl+S, macOS는 ⌘+S) → **브라우저에서 새로고침**(F5, macOS는 ⌘+R) → **화면·Console·Elements**를 본다.
바꾸기 전에 무엇이 달라질지 먼저 말해 보고 확인한다.

**클릭해 보기** — `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex03_counter.js` 줄을 켠 뒤 저장 → 새로고침한다. **눌러 보기**를 세 번 누른다.

**예상 결과** — 화면의 횟수가 `클릭 3회`가 되고, Console에 두 줄씩 세 번 찍힌다.

```text
1. 밖에 둔 count : 1     ex03_counter.js:12
2. 안에 둔 inside : 1    ex03_counter.js:16
1. 밖에 둔 count : 2     ex03_counter.js:12
2. 안에 둔 inside : 1    ex03_counter.js:16
1. 밖에 둔 count : 3     ex03_counter.js:12
2. 안에 둔 inside : 1    ex03_counter.js:16
```

`+ 1` 하는 줄은 똑같은데 1번만 는다. `let count = 0;`은 함수 밖이라 열 때 한 번만 실행되고, `let inside = 0;`은 함수 안이라 누를 때마다 다시 실행된다.

- 새로고침하면 `클릭 0회`로 돌아간다. 브라우저가 파일을 다시 읽어 DOM과 변수를 새로 만들기 때문이다.
- 값을 원래대로 못 돌리겠으면 교재에서 그 파일을 다시 **Raw**로 받아 덮어쓴다.
- 파일마다 무엇을 바꿔 볼지는 [1일차 실습](lab.md#1일차--dom-과-클릭-60분)에 있다.

### 5. 이번 주 저장소 만들어 올리기

1일차 50–60분에 한다. 세 예제에서 각각 값 하나 이상을 바꿔 봤으면 올린다.

GitHub에서 **New repository**를 누르고 이름 `web-week06`, **Public**으로 만든다. README는 추가하지 않는다.
터미널에서 2주차에 배운 순서 그대로 친다. 현재 폴더: `web-week06`

```bash
git init
git add .
git commit -m "6주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week06.git
git push -u origin main
```

저장소 화면에서 **Settings › Pages › Branch: main, /(root) › Save**를 누른다.

**예상 결과** — GitHub 저장소 화면을 새로고침하면 `ex/`·`images/`와 맨 위 파일들이 보인다.
1~3분 뒤 `https://student01.github.io/web-week06/ex/`를 연다. 고르기 페이지의 제목과 "예제가 쓰는 자리"가 보인다. 이 화면은 **확인용**이다.
공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 404가 나면 주소의 `web-week06/ex/`가 저장소·폴더 이름과 글자 단위로 같은지, Pages를 켰는지 본다.
- push가 거부되거나 로그인 창이 안 뜨면 [2주차 실습지의 막혔을 때](../week02_github_pages/lab.md#막혔을-때)를 본다.

## 2일차

### 6. 폴더 열고 비교 예제 여섯 파일 가져오기

같은 PC에 `web-week06` 폴더가 남아 있으면 VS Code로 그대로 연다. 없으면 받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/web-week06.git
```

내려받은 `web-week06`을 **File › Open Folder**로 연다.

오늘 예제는 세 개이고, 예제마다 `.html`과 `.js`가 한 쌍이라 파일은 여섯 개다. 오늘 예제는 화면이 서로 달라서 `.html`을 따로 둔다. [교재 저장소 examples/day2 폴더](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud/examples/day2)에서 1일차와 같은 **Raw** → 저장으로 `web-week06/ex/`에 넣는다.

| 파일 | 비교하는 것 |
|---|---|
| [ex04_classlist.html](examples/day2/ex04_classlist.html) + [ex04_classlist.js](examples/day2/ex04_classlist.js) | `classList.add` / `remove` / `toggle` 세 버튼과 상자 하나 |
| [ex05_dark.html](examples/day2/ex05_dark.html) + [ex05_dark.js](examples/day2/ex05_dark.js) | `body.dark` 규칙 / `body.dark .card` 규칙, 다크 모드 버튼 하나 |
| [ex06_reuse.html](examples/day2/ex06_reuse.html) + [ex06_reuse.js](examples/day2/ex06_reuse.js) | A 버튼 / B 버튼이 같은 함수 `countUp()`을 부른다 |

**예상 결과** — `ex/`에 파일이 열 개 있다(1일차 네 개 + 오늘 여섯 개).
`ex/ex04_classlist.html`을 열고 **1. add**를 누르면 상자가 노랗게 된다. F12 › **Elements**의 `<div id="box">` 줄에 `class="on"`이 생긴다.

- 오늘은 `.html`을 연다. `.js`는 같은 폴더에서 `.html`이 불러온다. 둘 중 하나를 빠뜨리면 버튼이 동작하지 않는다.
- `ex05`는 버튼을 누를 때 `<body>` 줄에 `class="dark"`가 붙었다 떨어진다. 색을 바꾸는 JS 줄은 없다. 색은 `.html`의 `<style>` 규칙이 정한다.
- `ex06`은 A·B를 섞어 눌러도 횟수가 하나로 이어진다.
- 파일마다 무엇을 바꿔 볼지는 [2일차 실습](lab.md#2일차--class-와-함수-그리고-조립-60분)에 있다.

### 7. 조립표

29분부터 조립한다. 이제 `ex/`가 아니라 `web-week06` 맨 위의 `index.html`·`styles.css`·`app.js`를 연다.
조립하는 줄은 모두 비교 예제와 5주차 완성본에서 본 것이다.

| 조립할 줄 | 출처 |
|---|---|
| `index.html`에 버튼 두 개(`#hello-button`·`#dark-button`)와 `#count` 카드 | [ex02](examples/day1/ex02_click_write.js) 누를 버튼, [ex03](examples/day1/ex03_counter.js) 횟수 자리 |
| `styles.css` 맨 아래 `body.dark, body.dark .card { … }` | [ex05](examples/day2/ex05_dark.html) 1·2번 규칙을 쉼표로 묶은 것 |
| `app.js`의 `name`·`hour`·`greet`·`hello` | 5주차 완성본 그대로 |
| `const greeting`·`countBox`·`helloButton`·`darkButton` | [ex01](examples/day1/ex01_dom.js) 찾아서 `const`에 담기 |
| `let count = 0;` | [ex03](examples/day1/ex03_counter.js) 1번, 함수 밖 |
| `function countUp() { … }` | [ex06](examples/day2/ex06_reuse.js) |
| `` greeting.textContent = `${greet(name)} ${hello(hour)}`; `` | [ex02](examples/day1/ex02_click_write.js) 1번, 열 때 바꾸기 |
| `helloButton.addEventListener('click', function () { … countUp(); });` | [ex02](examples/day1/ex02_click_write.js) 2번 + [ex06](examples/day2/ex06_reuse.js) |
| `darkButton.addEventListener('click', function () { document.body.classList.toggle('dark'); countUp(); });` | [ex05](examples/day2/ex05_dark.js) + [ex06](examples/day2/ex06_reuse.js) |

옮겨 적을 때 출처 ex 파일을 옆에 열어 두고, 같은 줄이 거기서 무엇을 했는지 떠올린다.

### 8. index.html에 다섯 줄 넣기

`web-week06/index.html`을 연다. `<main>` 첫 줄 `<div class="card" id="greeting">인사말을 준비 중입니다.</div>` **바로 아래**에 다섯 줄을 넣는다.

```html
      <div>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </div>
      <div class="card" id="count">클릭 0회</div>
```

- 버튼 두 개를 한 줄에 두려고 `<div>`로 감쌌다. 두 번째 줄은 횟수를 쓸 카드다. 4주차 `.card` 모양을 그대로 쓴다.
- `id`는 `app.js`가 찾을 이름이다. `hello-button`·`dark-button`·`count`를 글자 단위로 같게 쓴다.
- `type="button"`은 보통 버튼이라는 뜻이다. 폼 안에 두어도 폼을 보내지 않는다(폼은 7주차).

### 9. styles.css 맨 아래에 규칙 하나 넣기

`web-week06/styles.css`를 열고 맨 아래(`@media` 덩어리 다음)에 규칙 하나를 넣는다.

```css
body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

- ex05의 두 규칙(`body.dark`·`body.dark .card`)을 쉼표로 묶어 하나로 썼다. 쉼표로 묶으면 두 선택자에 같은 선언이 붙는다(4주차 `input, textarea`와 같다).
- 이 규칙은 `<body>`에 `class="dark"`가 붙었을 때만 맞는다. 붙이는 일은 `app.js`가 한다.

### 10. app.js 다시 쓰기

`web-week06/app.js`를 열어 **전부 지운다**. 5주차 코드를 지우는 이유: 마지막 줄 구조가 바뀌고, 찾은 요소를 `const`에 담아 두 번 이상 쓰기 때문이다. 5주차의 `name`·`hour`·`greet`·`hello` 네 덩어리는 그대로 다시 쓴다.

조립표 순서로 쓴다.

1. 값 두 개 — `name`(본인 아이디), `hour`. 5주차와 같다.
2. 찾아 두기 네 줄 — `#greeting`·`#count`·`#hello-button`·`#dark-button`을 `querySelector`로 찾아 `const`에 담는다(ex01).
3. `let count = 0;` — 함수 밖에 둔다(ex03 1번).
4. 함수 `greet`·`hello` — 5주차와 같다.
5. 함수 `countUp` — 횟수를 1 늘리고 `#count`에 쓴다(ex06).
6. 열 때 한 번 — 인사말 카드에 5주차 인사를 쓴다(ex02 1번).
7. 인사 바꾸기 버튼 — 누르면 문장을 바꾸고 `countUp()`을 부른다(ex02 2번 + ex06).
8. 다크 모드 버튼 — 누르면 `body`의 `dark`를 뒤집고 `countUp()`을 부른다(ex05 + ex06).

**예상 결과** — 저장하고 `index.html`을 새로고침한다. 첫 카드에 5주차 인사가 보이고, **인사 바꾸기**를 누르면 `반갑습니다. 오늘도 좋은 하루 되세요.`로 바뀐다. 두 버튼 어느 쪽을 눌러도 `클릭 N회`가 하나씩 늘고, **다크 모드**는 누를 때마다 배경과 카드가 어둡게 ↔ 원래대로 바뀐다. Console에 빨간 줄이 없다.

### 11. index.html 전문

10단계까지 마친 `index.html` 전체다. 내 파일과 한 줄씩 비교한다. 5주차 파일에서 늘어난 것은 8단계의 다섯 줄뿐이다.

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
      <div class="card" id="greeting">인사말을 준비 중입니다.</div>
      <div>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </div>
      <div class="card" id="count">클릭 0회</div>
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

같은 파일이 [examples/day2/web-week06/index.html](examples/day2/web-week06/index.html)에 있다.

### 12. styles.css 전문

5주차 파일에서 늘어난 것은 맨 아래 규칙 하나뿐이다.

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

같은 파일이 [examples/day2/web-week06/styles.css](examples/day2/web-week06/styles.css)에 있다.

### 13. app.js 전문

1행의 `student01`만 본인 아이디로 다르고 나머지는 글자 단위로 같아야 한다.

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

같은 파일이 [examples/day2/web-week06/app.js](examples/day2/web-week06/app.js)에 있다.

- 3~6행은 찾은 요소를 `const`에 담아 둔다. 두 번 이상 쓰는 요소를 매번 다시 찾지 않는다(ex01).
- 7행 `let count = 0;`은 함수 밖이다. 함수 안에 두면 늘 `클릭 1회`다(ex03).
- 21~24행 `countUp`은 두 버튼이 같이 쓰는 일이다. 고칠 일이 생기면 여기 한 곳만 고친다(ex06).
- 26행은 열 때 한 번 실행된다. 28~36행의 안쪽은 누를 때마다 실행된다(ex02).
- 34행 `document.body`는 `<body>` 요소다. 찾지 않고 바로 쓴다(ex05).

### 14. 375·1280 폭과 서버로 확인

DevTools의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)를 켜고 폭을 375와 1280으로 바꿔 가며 **다크 모드**를 켜 본다.

**예상 결과** — 두 폭 모두 배경과 카드가 어두워진다. 375에서는 메뉴가 세로로 선다(4주차 `@media`).

이어서 서버로 연다. 현재 폴더: `web-week06`

```bash
node server.mjs
```

주소창에 `http://localhost:8000/`을 친다. 두 번 눌러 연 것과 결과가 같으면 된 것이다. 확인이 끝나면 터미널에서 **Ctrl+C**로 서버를 멈춘다.
쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다. Node가 없는 PC는 `index.html`을 두 번 눌러 연 것으로 대신한다.

### 15. push와 캡처

현재 폴더: `web-week06`

```bash
git add .
git commit -m "6주차 2일차"
git push
```

1~3분 뒤 `https://student01.github.io/web-week06/`을 연다. **인사 바꾸기**를 한 번 누르고 **다크 모드**를 켠다.

**예상 결과** — 어두운 화면에 `반갑습니다. 오늘도 좋은 하루 되세요.`와 `클릭 2회`가 보인다. 주소창이 함께 보이게 캡처한다. 이 캡처 한 장이 제출이다.
공용 PC라면 자격 증명을 지우고 나간다.

- 옛 화면이 그대로면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 막히면 [실습지의 막혔을 때](lab.md#막혔을-때)를 본다.
