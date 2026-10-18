[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

# 7주차 실습 — 값을 바꿔 보고 마지막에 조립하기

이번 주 실습도 코드를 새로 쓰는 것이 아니라 **값을 바꿔 보는 것**이다.
비교 예제 7개를 이번 주 새 저장소 `web-week07` 의 `ex/` 폴더에 저장하고(1일차는 `.html`·`.js` 세 쌍, 2일차는 고르기 페이지 `index.html` 하나와 `.js` 네 개), 값이나 줄 하나를 바꾼 뒤 결과가 어떻게 달라지는지 본다.
결과는 화면, **주소창**, **F12 › Console** 에서 본다. DevTools 는 실습 내내 열어 둔다.
2일차 끝에 그 부품으로 `web-week07` 맨 위의 `guestbook.html` 을 고치고 `guestbook.js` 를 새로 만든다. 나머지 파일은 지난주 완성본 그대로다. 채점 대상은 2일차 캡처 1장이다.
`student01` 은 예시 아이디이므로 본인 아이디로 바꾼다.

파일을 받는 법과 Console 의 **Preserve log** 켜는 법은 [따라하기 1일차](walkthrough.md#1일차)에 있다.
"바꿔 보기"는 **무엇이 달라질지 먼저 말해 보고** 저장 → 새로고침으로 확인한다. 확인했으면 원래대로 되돌리고 다음으로 간다.

## 1일차 — 폼 제출과 입력 값 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 새 폴더 `web-week07` 을 만들어 VS Code 로 연다(**File › Open Folder**). 지난주 완성본을 넣는다: 내 `web-week06` 저장소 GitHub 화면 › **Code › Download ZIP** → 압축을 풀어 맨 위 파일과 `images/` 를 넣는다. 못 받으면 교재 [6주차 `examples/day2/web-week06/`](../week06_dom_crud/examples/day2/web-week06/) 파일을 **Raw** 로 받는다. `ex` 폴더를 만들고 교재 [`examples/day1/`](examples/day1/) 의 여섯 파일(ex01~ex03 의 `.html`·`.js`)을 **Raw** 로 저장한다 |
| 5–20분 | ex01 폼 제출과 preventDefault |
| 20–34분 | ex02 입력 칸의 value |
| 34–47분 | ex03 trim |
| 47–50분 | 확인: 여섯 파일이 `ex/` 에 있고, 각 예제에서 값 하나 이상을 바꿨는지. 일부러 낸 오류와 옮긴 줄은 되돌려 두었는지 |
| 50–60분 | 이번 주 저장소 만들어 올리기: GitHub 에 새 저장소 `web-week07` → [올리기 명령](#이번-주-저장소-만들어-올리기) → **Settings › Pages** → 공개 주소 `https://student01.github.io/web-week07/ex/ex01_submit.html` 확인 → 공용 PC면 자격 증명 삭제 |

1일차 예제는 `.html` 과 `.js` 가 한 쌍이다. 두 파일을 같은 `ex/` 폴더에 저장하고 `.html` 을 연다. 코드는 `.js` 에서 고치고, 저장 → `.html` 새로고침으로 본다.
시작하기 전에 지난주 완성본의 `guestbook.html` 을 열어 이름·메시지를 넣고 **남기기**를 눌러 본다. 주소창 끝에 `?` 가 붙고 칸이 빈다. 이번 주에 이 폼을 동작하게 한다.

### 1. ex01 폼 제출과 preventDefault (`submit` · `event.preventDefault()`)

[examples/day1/ex01_submit.html](examples/day1/ex01_submit.html) 과 [ex01_submit.js](examples/day1/ex01_submit.js) 를 `ex/` 에 저장하고 `ex01_submit.html` 을 연다.

- 바꿔 보기: 2번 칸에 글자를 넣고 **2. 보내기**를 누른다. 주소창, 2번 칸의 글자, 2번 결과 자리, Console 은? 이어서 1번 칸에 글자를 넣고 **1. 보내기**를 누른다. 주소창 끝에 무엇이 붙었나? 두 칸의 글자와 **2번** 결과 자리는 왜 처음으로 돌아갔나?
- 바꿔 보기: Console 위쪽 ⚙(**Console settings**) › **Preserve log** 를 끈 채로 1번을 보내고, 켠 뒤 한 번 더 보낸다. 두 번의 Console 은 어떻게 다른가? `1. form1 에서 submit` 이 남아 보이면 1번 리스너는 실행된 것이다. (확인한 뒤 Preserve log 는 이번 주 내내 켜 둔다. 줄이 쌓이면 Console 에서 오른쪽 클릭 › **Clear console**.)
- 바꿔 보기: 2번 칸에 글자를 넣고 **Enter** 를 친다. 버튼을 누른 것과 같은가? 1번 칸에서 Enter 를 치면?
- 바꿔 보기: `.js` 17행 `event.preventDefault();` 앞에 `//` 를 붙이고 2번을 보낸다. 2번도 1번처럼 되나? 확인했으면 되돌린다.
- 흔한 실수: `event.preventDefault()` 를 `preventDefault()` 로 쓴다(`event.` 빠짐). 빨간 줄 `Uncaught ReferenceError: preventDefault is not defined` 가 나고, 막지 못해 페이지가 다시 열린다. Preserve log 를 켜야 그 빨간 줄이 남아 보인다.

### 2. ex02 입력 칸의 value (`input.value` · `textarea.value`)

[examples/day1/ex02_value.html](examples/day1/ex02_value.html) 과 [ex02_value.js](examples/day1/ex02_value.js) 를 `ex/` 에 저장하고 `ex02_value.html` 을 연다.

- 바꿔 보기: 이름 `student01`, 메시지 `안녕하세요` 를 넣고 **남기기**를 누른다. 1·2·3번 자리에 무엇이 나오나? 1번은 왜 비어 있나?
- 바꿔 보기: 이름을 `student02` 로 바꿔 다시 누른다. 1번과 2번 중 무엇이 바뀌나? 11행과 15행은 같은 `nameInput.value` 인데 왜 결과가 다른가? (6주차 ex02 의 "열 때"와 "클릭할 때"를 떠올린다.)
- 바꿔 보기: 16행 `messageInput.value` 를 `messageInput.textContent` 로 바꾸고 누른다. 3번은? 칸에 친 글자는 어디에 들어 있나? 확인했으면 되돌린다.
- 바꿔 보기: 15행 `value` 를 `velue` 로 바꾸고 누른다. 2번에 무엇이 나오나? 빨간 줄이 뜨나? 확인했으면 되돌린다.
- 흔한 실수: 값을 읽는 줄을 리스너 밖(파일 위쪽)에 둔다. 1번처럼 열 때 한 번만 읽으므로 언제 눌러도 그때의 빈 글자다.

### 3. ex03 trim (`trim()`)

[examples/day1/ex03_trim.html](examples/day1/ex03_trim.html) 과 [ex03_trim.js](examples/day1/ex03_trim.js) 를 `ex/` 에 저장하고 `ex03_trim.html` 을 연다.

- 바꿔 보기: 이름 칸에 스페이스 두 번, `student01`, 스페이스 두 번을 넣고 누른다. Console 1·2번의 `[ ]` 안은?
- 바꿔 보기: 스페이스만 세 번 넣고 누른다. 2번은 무엇인가? 빈칸만 친 칸을 "비었다"고 보려면 1·2번 중 어느 값을 써야 하나? (2일차 ex05 에서 쓴다.)
- 바꿔 보기: `student 01` 처럼 가운데에 빈칸을 넣고 누른다. 2번에서 가운데 빈칸은 남나?
- 바꿔 보기: 10행 `trim()` 을 `trm()` 으로 바꾸고 누른다. 빨간 줄 문구와 `파일:줄` 은? 페이지가 다시 열리나? (8행에서 이미 막았다.) 확인했으면 되돌린다.
- 흔한 실수: `trim` 뒤의 괄호를 빠뜨린다(`.trim;`). 빨간 줄은 없지만 2번 `[ ]` 안에 앞뒤 빈칸을 뗀 이름이 아니라 함수의 글자(`function trim() …`)가 들어간다. 6주차 ex06 처럼 **부를 때는 괄호**다.

### 이번 주 저장소 만들어 올리기

GitHub 에서 **New repository** → 이름 `web-week07`, **Public**, README 는 추가하지 않는다. VS Code 터미널(현재 폴더 `web-week07`)에서 2주차에 배운 순서 그대로 친다.

```bash
git init
git add .
git commit -m "7주차 1일차"
git branch -M main
git remote add origin https://github.com/student01/web-week07.git
git push -u origin main
```

저장소 **Settings › Pages › Branch: main, /(root) › Save** → 1~3분 뒤 `https://student01.github.io/web-week07/ex/ex01_submit.html` 을 연다. 두 폼이 보이고 **2. 보내기**가 주소를 바꾸지 않으면 된 것이다. 공용 PC면 자격 증명을 지우고 나간다.
오늘 올린 것은 확인용이다. 제출은 2일차에 캡처 한 장만 한다.

## 2일차 — 빈값 안내와 다음 입력, 그리고 조립 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 같은 PC에 `web-week07` 폴더가 남아 있으면 그대로 연다. 없으면 `git clone https://github.com/student01/web-week07.git` 뒤 **File › Open Folder**. 교재 [`examples/day2/`](examples/day2/) 의 다섯 파일(고르기 페이지 `index.html` 과 ex04~ex07 의 `.js`)을 **Raw** 로 `ex/` 에 저장한다 |
| 5–11분 | ex04 reset 과 focus |
| 11–17분 | ex05 빈값 검사와 return |
| 17–23분 | ex06 input 이벤트 |
| 23–29분 | ex07 함수 이름만 맡기기 |
| 29–48분 | 조립: `guestbook.html` 네 곳 고치기, `guestbook.js` 를 조립표 순서로 새로 쓰기 |
| 48–55분 | 확인: 375·1280 폭, `node server.mjs` → `http://localhost:8000/guestbook.html`. Node 가 없으면 `guestbook.html` 을 두 번 눌러 연다 |
| 55–60분 | 끝 루틴: `git add .` → `git commit -m "7주차 2일차"` → `git push` → 공개 주소 `https://student01.github.io/web-week07/guestbook.html` 에서 결과 카드가 보이는 **캡처 1장** → 공용 PC면 자격 증명 삭제 |

2일차 예제는 모두 `ex/index.html` 하나로 연다. 그 파일 맨 아래 `<script src="exNN_….js">` 네 줄 중 **지금 문항의 줄 하나만** 주석 밖에 둔다(줄에서 **Ctrl+/**, macOS **⌘+/**). 코드는 각 `.js` 파일에서 고치고, 저장 → `ex/index.html` 새로고침으로 본다. 화면은 네 예제가 같다(방명록 모양 폼, 안내 자리 `#notice`, 결과 자리 `#last`).
파일마다 **바꿔 보기를 하나 이상** 하고 넘어간다. 29분이 되면 남은 것은 두고 조립을 시작한다. 남은 바꿔 보기는 캡처까지 끝낸 뒤 한다.

### 4. ex04 reset 과 focus (`form.reset()` · `focus()`)

[examples/day2/index.html](examples/day2/index.html) 과 [ex04_reset_focus.js](examples/day2/ex04_reset_focus.js) 를 `ex/` 에 저장하고 `ex/index.html` 을 연다. 맨 아래에서 ex04 줄만 켜져 있다(처음 받은 상태).

- 바꿔 보기: 두 칸을 채우고 **남기기**를 누른다. Console 1·2번의 `[ ]` 안은? 두 칸은 어떻게 됐나? 커서는 어느 칸에서 깜박이나(3번)?
- 바꿔 보기: 14행 `form.reset();` 을 잘라 2번 `console.log` 줄(`2. 비운 뒤 …` 를 찍는 줄) 바로 아래에 붙인다. 2번은 어떻게 바뀌나? 칸은 결국 비나? 읽는 일과 비우는 일 중 무엇을 먼저 해야 하나? 확인했으면 되돌린다.
- 바꿔 보기: 19행 `nameInput.focus();` 의 `nameInput` 을 `messageInput` 으로 바꾼다. 3번 커서는 어디로 가나? 확인했으면 되돌린다.
- 바꿔 보기: 14행 `reset` 을 `rest` 로 바꾸고 누른다. 빨간 줄과 `파일:줄` 은? 1번은 찍혔나? 칸은 비나? 확인했으면 되돌린다.
- 흔한 실수: `form.reset()` 을 값을 읽기 **전**에 둔다. 읽을 때 칸이 이미 비어 빈 글자를 읽는다. 읽고 → 쓰고 → 비운다.

### 5. ex05 빈값 검사와 return (`if` · `=== ''` · `return`)

[examples/day2/ex05_empty.js](examples/day2/ex05_empty.js) 를 `ex/` 에 저장한다. `ex/index.html` 맨 아래에서 ex04 줄을 끄고 `ex05_empty.js` 줄만 켠다. 이 예제는 칸을 비우지 않으므로 칸은 직접 지우며 해 본다.

- 바꿔 보기: 이름만 비우고, 메시지만 비우고, 둘 다 비우고, 둘 다 채워서 각각 누른다. Console 의 번호와 안내 자리·결과 자리는? 둘 다 비었을 때 어느 안내가 나오나? 왜 그런가?
- 바꿔 보기: 메시지 칸은 `안녕하세요` 로 채운 채 이름 칸에 스페이스만 넣고 누른다. 1번이 나오나? 12행의 `.trim()` 을 지우고 새로고침한 뒤 같은 값(이름 스페이스만, 메시지 `안녕하세요`)으로 다시 누르면? 확인했으면 되돌린다.
- 바꿔 보기: 19행 `return;` 앞에 `//` 를 붙인다. 이름은 비우고 메시지는 `안녕하세요` 로 누른다. Console 의 번호는? 결과 자리는? 1번이 쓴 안내는 왜 사라졌나? 확인했으면 되돌린다.
- 바꿔 보기: 16행 `===` 를 `=` 로 바꾸고 누른다. 빨간 줄과 `파일:줄` 은? 확인했으면 되돌린다.
- 흔한 실수: `return` 을 빠뜨린다. 안내를 쓴 뒤에도 아랫줄이 실행되어 결과 자리에 `: 안녕하세요` 처럼 이름 없는 줄이 남고, 안내는 3번에서 지워진다.

### 6. ex06 input 이벤트 (`'input'`)

[examples/day2/ex06_input.js](examples/day2/ex06_input.js) 를 `ex/` 에 저장한다. `ex/index.html` 맨 아래에서 `ex06_input.js` 줄만 켠다.

- 바꿔 보기: 열자마자 안내 자리에 무엇이 보이나? 이름 칸에 `abc` 를 한 글자씩 친다. Console 1번은 몇 줄인가? 안내는 언제 사라지나? Backspace 로 한 글자 지워도 1번이 찍히나?
- 바꿔 보기: 새로고침하고 메시지 칸에 친다. 2번이 찍히나? 한 줄 칸(`input`)과 여러 줄 칸(`textarea`)에서 같은 `'input'` 이 일어나나?
- 바꿔 보기: 11행 `'input'` 을 `'inptu'` 로(철자를 틀리게) 바꾸고 새로고침한다. 이름 칸에 치면 1번이 찍히나? 안내는 사라지나? 빨간 줄은? 메시지 칸에 치면? 확인했으면 되돌린다.
- 바꿔 보기: 이 예제에서 **남기기**를 누르면? (submit 을 막는 줄이 없다. ex01 의 1번과 같다.)
- 흔한 실수: 이벤트 이름의 철자를 틀린다(`'inptu'`). 브라우저는 그런 이름의 일이 생기기를 기다리기만 해서, 빨간 줄도 없이 아무 일도 일어나지 않는다. 이벤트 이름은 따옴표 안에 소문자 그대로 쓴다.

### 7. ex07 함수 이름만 맡기기 (`addEventListener('input', clearNotice)`)

[examples/day2/ex07_pass_name.js](examples/day2/ex07_pass_name.js) 를 `ex/` 에 저장한다. `ex/index.html` 맨 아래에서 `ex07_pass_name.js` 줄만 켠다. 이 예제는 Console 에 찍지 않는다. 안내 자리를 본다.

- 바꿔 보기: 열자마자 안내가 보인다. 이름 칸에 한 글자를 치면 안내는? 새로고침하고 이번에는 메시지 칸에 한 글자를 친다. 1번과 2번은 맡기는 모양이 다른데 하는 일은 같은가?
- 바꿔 보기: 18행 `clearNotice` 를 `clearNotice()` 로(괄호를 붙여) 바꾸고 새로고침한다. 메시지 칸에 쳐도 안내가 사라지나? 이름 칸에 치면? 빨간 줄은? 확인했으면 되돌린다.
- 바꿔 보기: 14행 `clearNotice();` 를 `clearNotice;` 로(괄호를 빼고) 바꾸고 새로고침한다. 이름 칸에 쳐도 안내가 사라지나? 6주차 ex06 의 `countUp;` 과 무엇이 같은가? 확인했으면 되돌린다.
- 흔한 실수: 함수를 맡길 때 괄호를 붙인다(`clearNotice()`). 괄호를 붙이면 그 줄이 실행될 때 함수가 한 번 불리고 끝난다. 칠 때 부를 함수는 맡겨지지 않아서, 쳐도 아무 일이 없고 빨간 줄도 없다. **맡길 때는 이름만, 부를 때는 괄호**다(6주차 ex06 의 `countUp();`).

### 8. 조립 — `guestbook.html` 네 곳, `guestbook.js` 새로 쓰기 (`submit` · `value` · `trim` · `return` · `reset` · `input`)

이제 `ex/` 가 아니라 `web-week07` 맨 위의 `guestbook.html` 을 연다. `guestbook.js` 는 그 옆(맨 위)에 새로 만든다. `ex/index.html` 은 2일차 예제 고르기 페이지라서 조립에 쓰지 않는다. 전문과 단계는 [따라하기 2일차](walkthrough.md#2일차)에 있다.

- `guestbook.html`: `<link>` 줄 아래에 `<script src="guestbook.js" defer></script>` 를 넣고, `<form>` 에 `id="guestbook-form"` 을 붙인다. 3주차 문장 `<p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>` 를 지우고 그 자리에 안내 자리·제목·결과 카드 세 줄을 넣는다.
- `guestbook.js`: 아래 조립표 순서로 쓴다. `index.html`·`app.js`·`styles.css`·`about.html` 은 6주차 그대로 두고 열지 않는다.

| 조립할 줄 | 어느 ex 에서 본 것 |
|---|---|
| `guestbook.html` 의 `<script src="guestbook.js" defer></script>` | 6주차 완성본 `index.html` 의 `<script src="app.js" defer></script>`. 파일 이름만 바꾼다(페이지마다 자기 js 하나) |
| `<form id="guestbook-form">` | ex01·ex02 (폼에 `id` 를 붙여 찾는다) |
| `<div id="notice"></div>` · `<div class="card" id="last">아직 남긴 글이 없습니다.</div>` | 2일차 고르기 페이지의 `#notice`·`#last`(ex05), 6주차 `#count` 카드의 `.card` |
| `<h3>마지막으로 남긴 글</h3>` | 6주차 완성본 `guestbook.html` 의 `<h3>쓰는 순서</h3>` 와 같은 모양의 제목 |
| `const form = …('#guestbook-form');` · `nameInput` · `messageInput` · `notice` · `last` | ex02·ex05 (찾아서 `const` 에 담기) |
| `function clearNotice() { notice.textContent = ''; }` | ex07 (안내를 지우는 함수. 본문까지 같다) |
| `form.addEventListener('submit', function (event) { event.preventDefault(); …` | ex01 2번 |
| `const name = nameInput.value.trim();` · `const message = messageInput.value.trim();` | ex02 2·3번 (누를 때 읽기) + ex03 2번 (`trim()`) |
| `if (name === '') { notice.textContent = '이름을 입력하세요.'; nameInput.focus(); return; }` | ex05 1번 + ex04 (`focus()`) |
| `if (message === '') { notice.textContent = '메시지를 입력하세요.'; messageInput.focus(); return; }` | ex05 2번 + ex04 |
| `clearNotice();` · `` last.textContent = `${name}: ${message}`; `` | ex07 1번 (함수 안에서 괄호를 붙여 부르기) · ex05 3번 |
| `form.reset();` · `nameInput.focus();` | ex04 |
| `nameInput.addEventListener('input', clearNotice);` · `messageInput.addEventListener('input', clearNotice);` | ex06 (`'input'` 이벤트) + ex07 2번 (이름만 맡기기). 한 함수를 여러 곳에서 쓰는 것은 6주차 ex06 |

- 확인: 저장하고 `guestbook.html` 을 새로고침한다. 이름 `student01`, 메시지 `안녕하세요` 로 **남기기**를 누르면 주소가 그대로이고, 카드가 `student01: 안녕하세요` 로 바뀌고, 칸이 비고, 커서가 이름 칸에 있으면 된 것이다.
- 바꿔 보기: 이름을 비우고 누른 뒤 이름 칸에 한 글자를 친다. 안내는 언제 나타나고 언제 사라지나? 이번에는 메시지만 비우고 해 본다.
- 바꿔 보기: 다른 이름·메시지로 한 번 더 남긴다. 앞 글은 어떻게 되나? (카드가 한 줄이라 마지막 글 하나만 남는다. 글을 쌓는 목록은 10주차에 배운다.)
- 흔한 실수: `<script src="guestbook.js" defer>` 의 `defer` 를 빠뜨린다. 열자마자 `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')`(`guestbook.js:11`)가 뜨고 그 아래가 실행되지 않아, **남기기**를 누르면 페이지가 다시 열린다. 폼 `id` 철자가 틀려도 같은 문구다.

### 9. 375·1280 폭과 서버로 확인

- DevTools 의 기기 툴바(**Ctrl+Shift+M**, macOS **⌘+Shift+M**)로 폭 375 와 1280 에서 `guestbook.html` 을 연다. 두 폭 모두 폼과 카드가 화면 안에 들어오고 **남기기**가 같게 동작하면 된 것이다.
- 1일차에 넣어 둔 `server.mjs` 가 없으면 [server.mjs](../../tools/static-server/server.mjs) 를 **Raw** 로 받아 `web-week07` 맨 위에 둔다. 터미널(현재 폴더 `web-week07`)에서 `node server.mjs` → `http://localhost:8000/guestbook.html` 을 연다. 쓰는 법은 [서버 사용 안내](../../tools/static-server/README.md)에 있다.
- 확인이 끝나면 터미널에서 **Ctrl+C** 로 서버를 멈추고 끝 루틴으로 간다.

## 막혔을 때

| 증상 | 확인할 것 |
|---|---|
| 공개 주소에 방금 push한 내용이 안 보인다 | Pages 반영은 보통 1~3분 걸린다. 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다 |
| push 가 거부되거나 로그인 창이 안 뜬다 | [2주차 막혔을 때](../week02_github_pages/lab.md#막혔을-때) 표를 본다 |
| 화면이 생각과 다른데 이유를 모르겠다 | **Console 을 먼저 연다.** 빨간 줄 오른쪽 `파일:줄` 로 간다. 오류 난 줄 아래는 실행되지 않으므로 그 줄부터 본다 |
| **남기기**를 누르면 주소 끝에 `?` 가 붙고 칸이 빈다. Console 에 새 빨간 줄이 없다 | 페이지가 다시 열린 것이다(오류가 아니라 폼의 원래 동작). ① `guestbook.html` 에 `<script src="guestbook.js" defer></script>` 줄이 있는지 ② 리스너 첫 줄에 `event.preventDefault();` 가 있는지 ③ `event.` 를 빠뜨리지 않았는지 본다. Console ⚙ › **Preserve log** 를 켜고 다시 누르면 빨간 줄이 있었는지 보인다 |
| 열자마자 `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` (`guestbook.js:11`) | 폼을 못 찾았다. `'#guestbook-form'` 과 `<form id="guestbook-form">` 의 글자를 비교하고, `script` 줄에 `defer` 가 있는지 본다 |
| `Uncaught ReferenceError: preventDefault is not defined` | `event.` 를 빠뜨렸다. `event.preventDefault();` 로 쓴다(ex01 흔한 실수) |
| `Uncaught TypeError: Cannot read properties of undefined (reading 'trim')` (`guestbook.js:14`) | `.value` 철자가 틀렸다(`velue`). 없는 이름이라 `undefined` 이고, 그 뒤 `.trim()` 에서 멈췄다(ex02 넷째 바꿔 보기) |
| `Uncaught TypeError: nameInput.value.trm is not a function` | `trim` 철자가 틀렸다(ex03 넷째 바꿔 보기) |
| `Uncaught TypeError: form.rest is not a function` | `reset` 철자가 틀렸다. 결과 카드는 이미 바뀌고 칸만 안 비워진다(ex04 넷째 바꿔 보기) |
| `Uncaught TypeError: Assignment to constant variable.` | `if (name === '')` 를 `if (name = '')` 로 썼다. 비교는 `=` 세 개다(ex05 넷째 바꿔 보기) |
| 이름을 비웠는데 결과 카드에 `: 안녕하세요` 가 나온다 | 이름 검사 안의 `return;` 이 없다(ex05 셋째 바꿔 보기) |
| 이름 칸에 스페이스만 넣었는데 통과한다 | `.trim()` 이 빠졌다. `nameInput.value.trim()` 으로 읽는다(ex03) |
| 채워서 눌러도 늘 `이름을 입력하세요.` 가 나온다 | `const name = …` 줄이 리스너 **밖**에 있거나(ex02 1번), `form.reset();` 이 값을 읽는 줄보다 **위**에 있다(ex04) |
| 안내 문구가 다시 쳐도 사라지지 않는다 | 맨 끝 두 줄의 `'input'` 철자를 보고(ex06 셋째 바꿔 보기), `clearNotice` 에 괄호를 붙이지 않았는지 본다(ex07 둘째 바꿔 보기) |
| **남기기**를 누르면 이메일 칸 옆에 메일 주소를 고치라는 말풍선이 뜨고(문구는 친 글자에 따라 다르다), 커서가 이메일 칸에 남고, 결과·안내는 그대로다. Console 에 새 줄도 없다 | 이메일 칸에 메일 주소 모양이 아닌 글자가 있다. `type="email"` 칸이라 브라우저가 보내기 전에 막았다(제출 리스너까지 가지 않는다). 이메일 칸은 비워 두거나 `student01@example.com` 모양으로 쓴다 |
| 2일차 예제에서 `Uncaught SyntaxError: Identifier '…' has already been declared` | 고르기 페이지에서 `script` 줄을 둘 이상 켰다. 두 파일이 같은 이름의 `const` 를 만들어 둘째 파일이 실행되지 않는다. 한 줄만 켠다 |
| 2일차 예제를 열었는데 아무 일도 없다. ex04·ex05 는 **남기기**를 누르면 `?` 가 붙고 Console 에 찍히는 줄이 없다. ex06·ex07 은 안내 문구가 나오지 않는다 | `ex/index.html` 맨 아래에서 켠 줄이 없다. 그 문항의 `script` 줄 하나를 주석 밖에 둔다 |
| 두 번째 글을 남기면 앞 글이 사라진다 | 정상이다. 카드가 한 줄이다. 글을 쌓는 목록은 10주차에 배운다 |
| 새로고침하면 남긴 글이 사라진다 | 정상이다. 새로고침하면 파일을 다시 읽어 화면을 새로 만든다. 남기는 법은 11주차에 배운다 |
| 공개 주소 `…/web-week07/ex/` 가 404 다 | 1일차에는 `ex/` 에 `index.html` 이 없다. 파일 이름까지 연다(`…/ex/ex01_submit.html`). 그래도 404 면 폴더 이름이 `ex` 인지, 저장소 이름이 `web-week07` 이고 **Settings › Pages** 가 켜져 있는지 본다 |

한 번에 한 곳만 고치고 새로고침한다. 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 한 장

공개 주소 `https://student01.github.io/web-week07/guestbook.html` (본인 아이디) 을 열고 이름과 메시지를 넣어 **남기기**를 누른 화면을 캡처한다.

- **마지막으로 남긴 글** 아래 카드에 `이름: 메시지` 가 한 줄로 보인다(예: `student01: 안녕하세요`).
- **주소창이 함께 보이게** 찍는다.
- 빈값 안내(`이름을 입력하세요.`)는 실습 중에 확인하는 것이고 캡처에는 없어도 된다.

1일차 push 와 `ex/` 실험 파일은 확인용이며 따로 제출하지 않는다.
캡처에 실명·학번·실제 이메일이 보이지 않게 한다(이메일 칸은 비워 둔다). 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 이메일 칸도 검사한다: 비어 있으면 `이메일을 입력하세요.` 를 쓰고 커서를 이메일 칸으로 옮긴다. ex05 2번과 같은 모양의 `if` 를 메시지 검사 아래에 하나 더 둔다. 이메일 칸을 찾아 두는 줄과 읽는 줄은 어디에 더하나? 다시 치면 안내가 사라지게 하려면 맨 끝에 무엇을 한 줄 더하나?
- 안내 문구 색: `styles.css` 맨 아래에 `#notice { color: #b3261e; }` 규칙을 더한다(4주차 `#` 선택자). JavaScript 는 고치지 않는다.
- 남긴 글 수 세기: 결과 카드 아래에 `<div id="total">남긴 글 0개</div>` 를 두고, 글을 남길 때마다 `남긴 글 N개` 로 바꾼다. 횟수 변수는 함수 안과 밖 중 어디에 두나(6주차 ex03)? 두 칸이 비어 막혔을 때는 늘지 않아야 한다.
- 서버로 ex01 열기: 터미널(현재 폴더 `web-week07`)에서 `node server.mjs` → `http://localhost:8000/ex/ex01_submit.html` 을 연다. 열 때 터미널에 어떤 줄들이 찍히나? 1번을 보낼 때는 어떤 줄들이 더 찍히나? 2번을 보낼 때는? "페이지를 다시 연다"는 것이 서버 쪽에서는 어떻게 보이나(1주차 요청과 응답)? 줄 읽는 법은 [서버 사용 안내](../../tools/static-server/README.md#터미널에-찍히는-줄-읽기)에 있다. 확인이 끝나면 **Ctrl+C**.
- 8주차 문제 은행의 [w07_form_line](../week08_midterm/examples/w07_form_line/README.md) 을 풀어 본다. 이번 주와 같은 일을 다른 값으로 한다. 해답은 공개하지 않는다. 문제의 "확인할 것"이 모두 맞으면 된 것이다.

추가 과제는 선택 사항이며 채점하지 않는다.
