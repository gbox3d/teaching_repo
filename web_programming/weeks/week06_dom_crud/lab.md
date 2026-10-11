[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud)

# 6주차 실습 — 값을 바꿔 보고 마지막에 조립하기

이번 주 실습도 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 예제 6개를 이번 주 새 저장소 `web-week06` 의 `ex/` 폴더에 저장하고(1일차는 고르기 페이지 `index.html` 하나와 `.js` 세 개, 2일차는 `.html`·`.js` 세 쌍), 값이나 줄 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
결과는 화면, **F12 › Console**, **F12 › Elements** 에서 본다. DevTools 는 실습 내내 열어 둔다.
2일차 끝에 그 부품으로 `web-week06` 맨 위의 `index.html`·`styles.css`·`app.js` 를 조립한다. 세 파일은 지난주 완성본에서 가져온다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법, 고르기 페이지 쓰는 법, Elements 탭 여는 법은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다. 확인했으면 원래대로 되돌리고 다음으로 간다.

## 1일차 — DOM 과 클릭 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week06` 을 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week05` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일과 `images/` 를 넣는다. 못 받으면 교재 [5주차 `examples/day2/web-week05/`](../week05_javascript_data/examples/day2/web-week05/) 파일을 **Raw** 로 받는다. `ex` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 네 파일(고르기 페이지 `index.html` 과 ex01~ex03 의 `.js`)을 **Raw** 로 저장한다 |
| 5–20분 | ex01 HTML 파일과 DOM |
| 20–33분 | ex02 클릭할 때 바꾸기 |
| 33–47분 | ex03 클릭 횟수 |
| 47–50분 | 확인: 네 파일이 `ex/` 에 있고, 각 예제에서 값 하나 이상을 바꿨는지. 일부러 낸 오류와 옮긴 줄은 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week06` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week06/ex/` 확인 → 공용 PC면 자격 증명 삭제 |

1일차 예제는 모두 `ex/index.html` 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 세 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → `ex/index.html` 새로고침으로 본다.

### 1. ex01 HTML 파일과 DOM (`document` · `querySelector` · Elements 탭)

[examples/day1/ex01_dom.js](examples/day1/ex01_dom.js) 를 `ex/ex01_dom.js` 로 저장한다. `ex/index.html` 맨 아래에서 `ex01_dom.js` 줄만 켠다(처음 받은 상태가 이렇다).

- 바꿔 보기: 화면의 첫 글자 줄은 무엇인가? **F12 › Elements** 탭에서 `<div id="message">` 줄을 찾아 글자를 읽는다. 이어서 페이지 소스 보기(**Ctrl+U**, macOS **⌘+Option+U**)에서 같은 줄을 찾는다. 두 곳의 글자가 왜 다른가?
- 바꿔 보기: Elements 탭에서 `<div id="message">` 안의 글자를 두 번 눌러 아무 글자로 고치고 Enter 한다. 화면이 바뀌나? 새로고침하면 어떻게 되나? Elements 에서 고친 것은 어디에 저장되나?
- 바꿔 보기: 4행 `'#message'` 를 `'#msg'` 로 바꾼다. Console 2번에 무엇이 찍히나? 빨간 줄은 무엇이라고 하고 `파일:줄` 은 몇 행인가? 화면 글자는 왜 원래 글자인가? 확인했으면 되돌린다.
- 흔한 실수: Elements 탭에서 고친 것이 파일에 저장된다고 본다. Elements 는 **지금 화면의 DOM** 이다. 파일을 바꾸려면 VS Code 에서 고치고 저장한다.

### 2. ex02 클릭할 때 바꾸기 (`addEventListener` · `textContent`)

[examples/day1/ex02_click_write.js](examples/day1/ex02_click_write.js) 를 `ex/ex02_click_write.js` 로 저장한다. `ex/index.html` 맨 아래에서 ex01 줄을 끄고 `ex02_click_write.js` 줄만 켠다.

- 바꿔 보기: 열자마자 화면 글자와 Console 은? **눌러 보기**를 세 번 누른다. Console 의 2번은 몇 줄인가? 1번은 늘어나나? 새로고침하면 화면은 어떻게 되나?
- 바꿔 보기: 13행 `message.textContent = '2. 버튼을 눌러 바꾼 글자';` 를 잘라 15행 `});` **아래**에 붙인다. 열자마자 화면 글자는 무엇인가? 버튼을 누르면 화면이 바뀌나? 확인했으면 되돌린다.
- 바꿔 보기: 8행 앞에 `//` 를 붙여 주석으로 만든다. 열자마자 화면 글자는 어디서 온 글자인가? 확인했으면 되돌린다.
- 흔한 실수: 바꾸는 줄을 `addEventListener( … function () { … });` 의 `{ }` 밖에 쓴다. 그 줄은 열자마자 한 번 실행되고 버튼과 관계가 없다(5주차 ex01 의 A·C 와 B).

### 3. ex03 클릭 횟수 (`let count` · `count = count + 1`)

[examples/day1/ex03_counter.js](examples/day1/ex03_counter.js) 를 `ex/ex03_counter.js` 로 저장한다. `ex/index.html` 에서 `ex03_counter.js` 줄만 켠다.

- 바꿔 보기: 버튼을 다섯 번 누른다. 화면의 `클릭 N회` 와 Console 1번·2번 숫자는? 두 숫자가 왜 다른가? `+ 1` 하는 줄은 똑같다.
- 바꿔 보기: 7행 `let count = 0;` 을 잘라 9행 `btn.addEventListener('click', function () {` 바로 아래(함수 안 첫 줄)에 붙인다. 다섯 번 누르면 화면은? 2번과 같아졌나? 확인했으면 되돌린다.
- 바꿔 보기: 7행 `let` 을 `const` 로 바꾸고 누른다. 빨간 줄과 `파일:줄` 은? 5주차 ex03 의 어느 버튼과 같은가? 확인했으면 되돌린다.
- 바꿔 보기: 세 번 누른 뒤 새로고침한다. 화면은 몇 회인가? 왜 0 으로 돌아가나? (새로고침하면 브라우저가 파일을 다시 읽어 DOM 과 변수를 새로 만든다. 새로고침해도 남기는 법은 11주차에 배운다.)
- 흔한 실수: 횟수 변수를 함수 안에서 `let count = 0;` 으로 만든다. 누를 때마다 다시 0 에서 시작해 늘 `클릭 1회` 다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week06`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week06`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "6주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week06.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week06/ex/` 를 연다. `ex/index.html` 의 화면(제목과 "예제가 쓰는 자리")이 보이면 된 것이다. 공용 PC면 자격 증명을 지우고 나간다.
오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — class 와 함수, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week06` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week06.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 여섯 파일(ex04~ex06 의 `.html`·`.js`)을 **Raw** 로 `ex/` 에 저장한다 |
| 5–13분 | ex04 classList |
| 13–21분 | ex05 다크 모드 |
| 21–29분 | ex06 함수 하나를 두 버튼에 |
| 29–48분 | 조립: `index.html` 에 다섯 줄, `styles.css` 에 규칙 하나, `app.js` 를 조립표 순서로 다시 쓰기 |
| 48–55분 | 확인: 375·1280 폭에서 다크 모드, `node server.mjs` → `http://localhost:8000/`. Node 가 없으면 `index.html` 을 두 번 눌러 연다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit -m "6주차 2일차"` → `git push` → 공개 주소 `https://student01.github.io/web-week06/` 에서 다크 모드를 켠 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

2일차 예제는 `.html` 과 `.js` 가 한 쌍이다. 두 파일을 같은 `ex/` 폴더에 저장하고 `.html` 을 연다. 코드는 `.js`, 모양 규칙은 `.html` 의 `<style>` 에 있다.
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 29분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.

### 4. ex04 classList (`classList.add` · `remove` · `toggle`)

[examples/day2/ex04_classlist.html](examples/day2/ex04_classlist.html) 과 [ex04_classlist.js](examples/day2/ex04_classlist.js) 를 `ex/` 에 저장하고 `ex04_classlist.html` 을 연다.

- 바꿔 보기: **F12 › Elements** 에서 `<div id="box">` 줄을 펼쳐 둔다. 1 add 를 두 번, 2 remove 를 한 번, 3 toggle 을 세 번 누르며 그 줄의 `class` 를 본다. add 를 두 번 눌렀을 때 `on` 이 두 개 붙나?
- 바꿔 보기: `.html` 의 `<style>` 에서 `.on` 의 `gold` 를 `lightblue` 로 바꾼다. JS 를 고치지 않았는데 무엇이 달라지나? 모양은 어디가 정하나?
- 바꿔 보기: `.js` 15행 `toggle('on')` 의 `'on'` 을 `'On'` 으로 바꾸고 3 toggle 을 누른다. Elements 의 class 는? 상자 색은 왜 안 바뀌나? 확인했으면 되돌린다.
- 흔한 실수: CSS 규칙은 `.on` 인데 JS 에는 `'.on'` 처럼 점을 붙인다. `classList` 에는 **class 이름만** 쓴다. 점은 CSS 선택자와 `querySelector` 에서만 붙인다.

### 5. ex05 다크 모드 (`body.dark` · `document.body.classList.toggle`)

[examples/day2/ex05_dark.html](examples/day2/ex05_dark.html) 과 [ex05_dark.js](examples/day2/ex05_dark.js) 를 `ex/` 에 저장하고 `ex05_dark.html` 을 연다.

- 바꿔 보기: **다크 모드**를 누르며 Elements 의 `<body>` 줄을 본다. 무엇이 붙었다 떨어지나? 배경색을 바꾼 JS 줄이 있나?
- 바꿔 보기: `<style>` 의 2번 규칙 `body.dark .card { … }` 세 줄을 지우고 다크 모드를 켠다. 카드는 어떻게 보이나? 왜 카드만 남나? (4주차 `nav a` 처럼 "어두운 body **안의** 카드"를 고르는 규칙이다.) 확인했으면 되돌린다.
- 바꿔 보기: `.js` 6행의 `toggle` 을 `add` 로 바꾸고 버튼을 여러 번 누른다. 다크 모드를 끌 수 있나? ex04 의 어느 버튼과 같은가? 확인했으면 되돌린다.
- 흔한 실수: CSS 에 `body.dark` 규칙을 넣지 않고 JS 만 쓴다. Elements 의 body 에 `class="dark"` 는 붙는데 화면은 그대로다. 색은 CSS 가 정한다.

### 6. ex06 함수 하나를 두 버튼에 (`function` · 부르기)

[examples/day2/ex06_reuse.html](examples/day2/ex06_reuse.html) 과 [ex06_reuse.js](examples/day2/ex06_reuse.js) 를 `ex/` 에 저장하고 `ex06_reuse.html` 을 연다.

- 바꿔 보기: A, B, A 순서로 누른다. 화면 횟수와 Console 은? A·B 의 셈이 따로인가, 하나로 이어지나? 왜 그런가?
- 바꿔 보기: 8행 `` `클릭 ${count}회` `` 를 `` `누른 횟수 ${count}` `` 로 바꾼다. A·B 두 버튼의 글자가 모두 바뀌나? 몇 곳을 고쳤나?
- 바꿔 보기: 14행 `countUp();` 을 `countUp;` 으로(괄호를 빼고) 바꾸고 A 를 누른다. Console 1번은 찍히나? 횟수는 느나? 빨간 줄이 뜨나? 확인했으면 되돌린다.
- 흔한 실수: 함수를 부를 때 괄호를 빠뜨린다. `countUp;` 은 이름만 적은 것이라 아무 일도 하지 않고 오류도 나지 않는다. 5주차 ex08 처럼 **괄호를 붙여야** 실행된다.

### 7. 조립 — `index.html` 다섯 줄, `styles.css` 규칙 하나, `app.js` (`addEventListener` · `classList.toggle` · `countUp`)

이제 `ex/` 가 아니라 `web-week06` 맨 위의 `index.html`·`styles.css`·`app.js` 를 연다. `ex/index.html` 은 1일차 예제 고르기 페이지라서 조립에 쓰지 않는다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `index.html` 의 `<p class="card" id="greeting">…</p>` 바로 아래에 버튼 두 개를 감싼 줄과 `<p class="card" id="count">클릭 0회</p>` 를 넣는다(다섯 줄).
- `styles.css` 맨 아래에 `body.dark, body.dark .card { background-color: #222222; color: #eeeeee; }` 규칙을 넣는다.
- `app.js` 는 **전부 지우고** 아래 조립표 순서로 다시 쓴다. 5주차 줄 중 `name`·`hour`·`greet`·`hello` 는 그대로 옮긴다.

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `index.html` 의 `<button id="hello-button" type="button">인사 바꾸기</button>` · `<button id="dark-button" type="button">다크 모드</button>` | ex02 (누를 버튼에 `id`). `type="button"` 은 폼 안에서 눌러도 폼을 보내지 않는 보통 버튼이라는 뜻이다(폼은 7주차) |
| `index.html` 의 `<p class="card" id="count">클릭 0회</p>` | ex03 (횟수를 쓸 자리), 4주차 `.card` |
| `styles.css` 의 `body.dark, body.dark .card { … }` | ex05 1·2번 (두 선택자를 쉼표로 묶어 규칙 하나로) |
| `const name = 'student01';` · `const hour = new Date().getHours();` | 5주차 그대로 |
| `const greeting = document.querySelector('#greeting');` · `const countBox = document.querySelector('#count');` | ex01 (찾아서 `const` 에 담기), ex03 |
| `const helloButton = …('#hello-button');` · `const darkButton = …('#dark-button');` | ex02 (버튼 찾기), ex05 |
| `let count = 0;` | ex03 1번 (함수 밖) |
| `function greet(name) { … }` · `function hello(hour) { … }` | 5주차 그대로 |
| `function countUp() { count = count + 1; countBox.textContent = `클릭 ${count}회`; }` | ex06 |
| `` greeting.textContent = `${greet(name)} ${hello(hour)}`; `` | ex02 1번 (열 때 바꾸기). 5주차의 `message` 를 따로 만들지 않고 바로 넣었다 |
| `helloButton.addEventListener('click', function () { greeting.textContent = '반갑습니다. …'; countUp(); });` | ex02 2번 (클릭할 때 바꾸기) + ex06 |
| `darkButton.addEventListener('click', function () { document.body.classList.toggle('dark'); countUp(); });` | ex05 + ex06 |

- 확인: 저장하고 `index.html` 을 새로고침한다. 열자마자 첫 카드에 5주차 인사(`안녕하세요, student01님! 좋은 아침입니다.` 또는 `좋은 오후입니다.`)가 보이고, **인사 바꾸기**를 누르면 `반갑습니다. 오늘도 좋은 하루 되세요.` 로 바뀌고, 두 버튼 어느 쪽이든 `클릭 N회` 가 하나씩 늘면 된 것이다.
- 바꿔 보기: **다크 모드**를 켠 채 새로고침한다. 다크 모드와 횟수는 어떻게 되나? 왜 그런가? (ex03 넷째 바꿔 보기와 같다.)
- 흔한 실수: 버튼 `id` 와 `querySelector` 의 글자가 다르다(`hello-button` / `hello_button`). 찾지 못해 `null` 이 되고 `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` 가 뜬다. 그 줄 아래는 실행되지 않는다.

### 8. 375·1280 폭과 서버로 확인

- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 다크 모드를 켜 본다. 두 폭 모두 카드까지 어두워지면 된 것이다.
- 1일차에 넣어 둔 `server.mjs` 가 없으면 [server.mjs](../../tools/static-server/server.mjs) 를 **Raw** 로 받아 `web-week06` 맨 위에 둔다. 터미널(현재 폴더 `web-week06`)에서 `node server.mjs` → `http://localhost:8000/` 을 연다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.
- 확인이 끝나면 터미널에서 **Ctrl+C** 로 서버를 멈추고 끝 루틴으로 간다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 오류 난 줄 아래는 실행되지 않으므로 그 줄부터 본다 |
| 1일차 예제를 열었는데 Console 에 아무것도 없다 | `ex/index.html` 맨 아래에서 그 문항의 `script` 줄을 켰는지(주석 밖인지), `.js` 파일이 같은 `ex/` 폴더에 있는지 본다. `Failed to load resource` 줄이 있으면 파일 이름 철자가 틀린 것이다 |
| `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` | 글자를 바꿀 요소를 못 찾았다. `querySelector('#…')` 의 id 와 HTML 의 `id="…"` 를 글자 단위로 비교한다(ex01 셋째 바꿔 보기). 조립한 `app.js` 26행에서 뜨고 인사말이 `인사말을 준비 중입니다.` 그대로면 `index.html` 의 `<script src="app.js" defer>` 에서 `defer` 가 빠졌다(5주차 ex02) |
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | 버튼을 못 찾았다. 버튼의 `id` 와 `querySelector('#…')` 의 글자를 비교한다(`hello-button` / `hello_button`). 그 줄 아래는 실행되지 않아 다른 버튼도 동작하지 않는다 |
| `Uncaught TypeError: Assignment to constant variable.` | `count` 를 `const` 로 만들었다. 다시 담는 변수는 `let` 이다(ex03 셋째 바꿔 보기) |
| `Uncaught ReferenceError: countUp is not defined` | 함수 이름과 부른 이름이 다르다. `function countUp()` 과 `countUp();` 의 철자를 비교한다 |
| 버튼을 눌러도 횟수가 늘 `클릭 1회` 다 | `let count = 0;` 이 함수 안에 있다. 함수 밖 맨 위로 옮긴다(ex03) |
| 버튼을 눌러도 횟수가 안 는다. 빨간 줄도 없다 | `countUp;` 처럼 괄호를 빠뜨렸다(ex06 셋째 바꿔 보기) |
| 다크 모드를 눌러도 화면이 그대로다 | Elements 의 `<body>` 에 `class="dark"` 가 붙는지 본다. 붙는데 그대로면 `styles.css` 에 `body.dark` 규칙이 없거나, `styles.css` 를 저장하지 않았다. 안 붙으면 Console 의 빨간 줄부터 본다 |
| 다크 모드에서 카드만 흰색이다 | `styles.css` 규칙에 `body.dark .card` 가 빠졌다(ex05 둘째 바꿔 보기) |
| 새로고침하면 횟수와 다크 모드가 처음으로 돌아간다 | 정상이다. 새로고침하면 DOM 과 변수를 새로 만든다. 남기는 법은 11주차에 배운다 |
| 공개 주소 `…/web-week06/ex/` 가 404 다 | ① 폴더 이름이 `ex` 인지 ② 그 안에 `index.html` 이 있는지 ③ 저장소 이름이 `web-week06` 이고 **Settings › Pages** 가 켜져 있는지 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-week06/` (본인 아이디) 을 열고 다음 상태로 한 화면을 캡처한다.

- **인사 바꾸기**를 눌러 첫 카드가 `반갑습니다. 오늘도 좋은 하루 되세요.` 다.
- **다크 모드**가 켜져 배경과 카드가 어둡다.
- 횟수 카드가 `클릭 1회` 이상이다.
- **주소창이 함께 보이게** 찍는다.

1일차 push 와 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 메뉴 접기: `index.html` 의 `<nav>` 위에 **메뉴** 버튼을 하나 더 두고, 누를 때마다 `nav` 에 `hidden` class 를 붙였다 떼게 한다. `styles.css` 에는 `nav.hidden { display: none; }` 을 더한다. ex04 의 어느 버튼을 쓰나? 이 버튼도 횟수를 세게 하려면 무엇을 한 줄 더하나?
- ex03: 횟수가 10 이 되면 `클릭 10회 — 그만 눌러도 됩니다` 로 쓰게 한다. 5주차 ex07 의 `if` 를 함수 안 어디에 넣나?
- ex05: 다크 모드일 때 버튼 글자를 `밝게 보기` 로, 아닐 때 `다크 모드` 로 바꾼다. `toggle` 대신 `if` 로 나누려면 무엇을 알아야 하나? (힌트: `document.body.classList.contains('dark')` 는 class 가 있으면 `true` 다.)

추가 과제는 선택 사항이며 채점하지 않는다.
