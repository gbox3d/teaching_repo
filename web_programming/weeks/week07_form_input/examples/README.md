[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

# 7주차 예제 — 비교 예제 8개와 조립 하나

예제는 쓰는 날짜별 폴더에 있다. 번호는 한 주 안에서 이어 센다.

```text
examples/
  day1/   ex01/ ~ ex03/   폼 제출과 preventDefault, 입력 칸의 value, trim
  day2/   ex04/ ~ ex08/   reset 과 focus, 빈값 검사와 return, input 이벤트, 함수 이름만 맡기기, 바꾸기 vs 붙이기
          web-week07/     2일차 끝의 web-week07 — 비교 예제에서 본 줄을 모은 조립
  (예제마다 폴더 하나: index.html + app.js)
```

예제 하나는 **개념 하나**다(폴더 `exNN/` 하나). 같은 일을 다르게 한 **형제**(1·2·3번)를 나란히 놓는다.
결과는 화면과 **주소창**, **F12 › Console** 에서 본다. 이번 주에는 Console 설정 ⚙ › **Preserve log** 를 켜 둔다. 폼이 페이지를 다시 열어도 Console 줄이 남는다. 값이나 줄을 바꾸고 저장 → 새로고침으로 무엇이 달라지는지 본다.
**다른 예제의 개념은 섞지 않는다.** 칸을 비우는 `form.reset()` 은 ex04 의 주제라서 1일차 예제에는 없다. 함수 이름만 맡기는 모양은 ex07 의 주제라서 ex06 은 두 칸 모두 `function () { }` 를 그 자리에 쓴다. 줄을 만들어 붙이는 것은 ex08 의 주제라서 ex05 는 결과 자리의 글자를 바꾼다. 앞 예제의 줄을 빌려 쓸 때는 줄 끝에 `// ex01` 처럼 출처를 적었다.
만들기는 마지막 하나, [`day2/web-week07/`](day2/web-week07/) 뿐이다.

예제 폴더마다 내 사이트와 같은 이름의 두 파일을 둔다. `index.html` 은 화면(그 예제가 쓰는 폼·칸·결과 자리만), `app.js` 는 동작이다. 이번 주의 원리는 모두 `app.js` 에 있다. 브라우저로 여는 것은 `index.html` 이고, `app.js` 는 `index.html` 이 불러온다(`<head>` 의 `<script src="app.js" defer>`. 내 사이트 `guestbook.html` 의 `<script src="guestbook.js" defer>` 와 같은 모양이다). 그래서 두 파일이 같은 폴더에 있어야 한다. 이번 주 예제에는 모양 파일(`styles.css`)이 없다.
2일차 ex04~ex07 은 방명록과 같은 모양의 칸을 쓴다. ex04 는 폼만, ex05 는 폼과 안내 자리 `#notice`·결과 자리 `#last`, ex06·ex07 은 두 칸과 안내 자리만 둔다(폼을 보내지 않는 예제라 폼과 버튼이 없다). ex08 은 글 칸 하나와 버튼 둘, 1번 자리와 빈 목록 `<ul id="list">` 를 쓴다.
내려받아 이번 주 저장소 `web-week07` 의 `ex/` 폴더 안에 같은 이름의 폴더(`ex01` … `ex08`)를 만들고 파일 이름 그대로 저장한다(교재 저장소에서 **Raw** → 저장). 날짜 폴더(`day1`·`day2`)는 만들지 않는다. 가져오는 방법은 [따라하기 1일차](../walkthrough.md#1일차)에 있다.

## 비교 예제

| 예제 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [day1/ex01/index.html](day1/ex01/index.html) + [app.js](day1/ex01/app.js) | 폼 두 개(칸 하나와 보내기 버튼). 2번을 보내면 주소 그대로, 칸 글자 그대로, 결과 `2. 제출을 받았다`, Console 2번. 1번을 보내면 주소 끝에 `?`, 칸이 비고 두 결과 자리가 처음 글자로 돌아간다 | 폼을 보내면 브라우저는 페이지를 **다시 연다**. 리스너는 실행되지만 바꾼 화면이 함께 사라진다. 리스너 첫 줄 `event.preventDefault()` 가 다시 열기를 막는다. 버튼을 눌러도 칸에서 Enter 를 쳐도 같은 `submit` 이다 | Preserve log 를 켜고 1번 보내기 → Console 1번이 남는다. `app.js` 17행 앞에 `//` → 2번도 다시 열린다. 17행 `event.` 지우기 → `preventDefault is not defined` |
| [day1/ex02/index.html](day1/ex02/index.html) + [app.js](day1/ex02/app.js) | 이름·메시지 칸과 남기기. 처음 열고 누르면 1번 `1. 열 때 읽은 이름 : `(빈 글자), 2번 지금 적힌 이름, 3번 지금 적힌 메시지 | `value` 는 칸에 **지금** 적힌 글자다. `app.js` 11행은 열 때 한 번, 15·16행은 누를 때마다 읽는다(6주차 ex02 와 같은 원리). textarea 도 `value` 로 읽는다 | 이름을 바꿔 다시 누르기 → 2번만 바뀐다. `app.js` 16행 `value` 를 `textContent` 로 → 3번이 빈다. 15행 `velue` → 2번 `undefined` |
| [day1/ex03/index.html](day1/ex03/index.html) + [app.js](day1/ex03/app.js) | 이름 칸 하나. 앞뒤에 빈칸을 넣고 누르면 Console 1번 `[  student01  ]`, 2번 `[student01]` | `trim()` 은 앞뒤 빈칸만 뗀 값을 돌려준다. 빈칸만 친 칸은 빈 글자 `''` 가 되고, 가운데 빈칸은 남는다 | 빈칸만 넣기 → 2번 `[]`. `student 01`. `app.js` 10행 `trm()` → 빨간 줄, `.trim` (괄호 빠짐) → 함수 글자 |
| [day2/ex04/index.html](day2/ex04/index.html) + [app.js](day2/ex04/app.js) | 이름·메시지 칸과 남기기. 두 칸을 채우고 누르면 Console 1번 `[student01] [안녕하세요]`, 2번 `[] []`. 칸이 비고 커서가 이름 칸에서 깜박인다(3번) | 다음 입력 준비다. `form.reset()` 은 폼 안의 칸을 모두 비운다. 그래서 값은 비우기 **전에** 읽는다. `focus()` 는 커서를 그 칸으로 옮긴다 | `app.js` 14행 `form.reset();` 을 2번 `console.log` 줄 아래로 → 2번에도 글자. 19행 `nameInput` → `messageInput`. 14행 `rest` → 빨간 줄 |
| [day2/ex05/index.html](day2/ex05/index.html) + [app.js](day2/ex05/app.js) | 폼 아래에 빈 안내 자리와 `아직 남긴 글이 없습니다.`. 이름이 비면 안내 `이름을 입력하세요.`·Console 1번, 메시지가 비면 `메시지를 입력하세요.`·2번, 둘 다 차면 안내가 지워지고 결과 `student01: 안녕하세요`·3번 | `if` 안의 `return` 은 함수를 그 자리에서 끝낸다. 검사는 위에서부터라 둘 다 비면 1번만 나온다. `trim()` 덕분에 빈칸만 친 칸도 1번이다 | `app.js` 19행 `return;` 앞에 `//` → 1번 다음 3번, 결과 `: 안녕하세요`. 16행 `===` 를 `=` 로 → 빨간 줄 |
| [day2/ex06/index.html](day2/ex06/index.html) + [app.js](day2/ex06/app.js) | 두 칸 아래에 안내 `안내 문구 — 칸에 글자를 치면 사라진다`. 이름 칸에 칠 때마다 Console 1번, 메시지 칸에 칠 때마다 2번이 한 줄씩. 첫 글자에서 안내가 사라진다 | `'input'` 은 칸의 글자가 바뀔 때마다 일어난다. 한 글자 칠 때도, Backspace 로 지울 때도. 한 줄 칸(`input`)과 여러 줄 칸(`textarea`)이 같다 | `app.js` 11행 `'input'` 을 `'inptu'` 로 → 이름 칸에 쳐도 1번이 없고 안내가 남는다. 빨간 줄은 없다 |
| [day2/ex07/index.html](day2/ex07/index.html) + [app.js](day2/ex07/app.js) | 두 칸 아래에 안내 `안내 문구 — 칸에 글자를 치면 사라진다`. 이름 칸(1번)이나 메시지 칸(2번)에 한 글자를 치면 안내가 사라진다. Console 은 쓰지 않는다 | 미리 만든 함수 `clearNotice` 는 **이름만** 맡기면 칠 때마다 브라우저가 대신 부른다(2번). `function () { }` 안에서 직접 부를 때는 괄호를 붙인다(1번). 두 모양은 하는 일이 같다 | `app.js` 18행 `clearNotice` 를 `clearNotice()` 로 → 메시지 칸에 쳐도 안내가 남는다. 14행 `clearNotice();` 를 `clearNotice;` 로 → 이름 칸에 쳐도 안내가 남는다. 빨간 줄은 둘 다 없다 |
| [day2/ex08/index.html](day2/ex08/index.html) + [app.js](day2/ex08/app.js) | 글 칸(`student01: 안녕하세요`)과 **1. 바꾸기**·**2. 붙이기**, `1번 자리`, 빈 목록. 칸의 글을 바꿔 가며 번갈아 누르면 1번 자리는 마지막 글 한 줄뿐이고, 목록은 2번을 누를 때마다 `•` 한 줄씩 는다. Console 1번·2번이 누를 때마다 한 줄 | 1번은 같은 자리의 `textContent` 를 바꾼다. 앞 글이 지워져 늘 한 줄이다. 2번은 누를 때마다 `createElement('li')` 로 줄을 **새로 만들고** `textContent` 로 글자를 넣고 `append` 로 목록 맨 뒤에 **붙인다**. 앞 줄은 그대로 남는다. 만들기만 하고 붙이지 않은 줄은 화면에도 Elements 에도 없다 | `app.js` 20행 `list.append(li);` 앞에 `//` → 2번을 눌러도 목록이 비고 빨간 줄도 없다(Console 2번은 찍힌다). 18행 `const li = …` 를 리스너 밖(8행 아래)으로 옮기기 → 목록이 늘 한 줄이고 글자만 바뀐다 |

### 파일 안의 모양

형제 번호가 주석 첫머리와 화면·Console 글자 앞에 있다. [ex02/app.js](day1/ex02/app.js) 에서 인용:

```js
const atOpen = nameInput.value;              // 1. 열 때 한 번 읽는다 — 그때 칸에 있던 글자(보통 빈 글자)

form.addEventListener('submit', function (event) {
    event.preventDefault();                  // ex01: 다시 열리지 않게 막는다
    const atSubmit = nameInput.value;        // 2. 누를 때마다 다시 읽는다 — 지금 적힌 글자
    const message = messageInput.value;      // 3. textarea 도 value 로 읽는다
```

1번과 2번은 같은 `nameInput.value` 다. 다른 것은 그 줄이 리스너 **밖**에 있느냐 **안**에 있느냐 하나다. `event.preventDefault();` 는 ex01 에서 본 줄을 빌려 쓴 것이라 줄 끝에 출처를 적었다.

## `day2/web-week07/` — 2일차 끝의 web-week07

[`day2/web-week07/`](day2/web-week07/) 는 2일차 끝의 `web-week07` 저장소 맨 위(`index.html` 등이 있는 자리) **전체**다. 9주차의 시작점이다. 비교 예제를 저장한 `ex/` 폴더와 서버 `server.mjs` 는 여기 넣지 않는다.

| `day2/web-week07/` 파일 | 내 `web-week07` 의 위치 | 따라하기 단계 |
|---|---|---|
| [guestbook.html](day2/web-week07/guestbook.html) | `guestbook.html` | [2일차 8단계](../walkthrough.md#2일차) — `<head>` 에 `<script src="guestbook.js" defer></script>`, `<form id="guestbook-form">`, 3주차 문장 대신 `#notice` 자리·제목 `남긴 글`·빈 목록 `<ul class="card" id="list">` |
| [guestbook.js](day2/web-week07/guestbook.js) | `guestbook.js` | [2일차 9단계](../walkthrough.md#2일차) — 새로 만든다. 조립표 순서로 쓰면 이 파일과 글자 단위로 같아진다 |
| [index.html](day2/web-week07/index.html) | `index.html` | 6주차 그대로. 이번 주에 열지 않는다 |
| [app.js](day2/web-week07/app.js) | `app.js` | 6주차 그대로. `index.html` 만 이 파일을 부른다(페이지마다 자기 js 하나) |
| [styles.css](day2/web-week07/styles.css) | `styles.css` | 6주차 그대로. 목록 `#list` 도 `.card` 모양을 쓴다 |
| [about.html](day2/web-week07/about.html) | `about.html` | 6주차 그대로 |
| [images/profile.png](day2/web-week07/images/profile.png) | `images/profile.png` | 3주차와 같은 파일. 바꾸지 않는다 |
