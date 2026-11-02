---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 7주차"
footer: "폼 입력 읽기와 결과 표시 · 비교 예제로 원리를 보고 마지막에 조립"
---

# 폼 입력 읽기와 결과 표시

6주차에는 버튼을 누르면 **정해 둔 글자**를 띄웠습니다. 이번 주는 방명록 폼에 **사용자가 입력한 글자**를 읽어, 남길 때마다 목록에 **한 줄씩 붙입니다**.

이번 주 방식도 같습니다: **비교 예제 8개**를 하나씩 보고, 마지막에 새 저장소 `web-week07` 의 `guestbook.html`·`guestbook.js` 를 **조립**합니다(지난주 완성본에서 시작).

- 폼을 보내면 브라우저는 페이지를 **다시 엽니다**. 그것을 막아야 결과가 남습니다.
- 결과는 화면, **주소창**, **Console** 에서 봅니다.
- 예제 하나 = 개념 하나. 실습은 **값을 바꿔 보는 것**입니다.

---

# 1일차 — 폼 제출과 입력 값

`30분 설명·시연 → 60분 실습`

1. 3주차 폼 다시 보기 — 남기기를 누르면 주소 끝에 `?`
2. ex01 — 폼 제출과 `event.preventDefault()`
3. ex02 — 입력 칸의 `value`: 열 때 vs 누를 때
4. ex03 — `trim()`: 앞뒤 빈칸 떼기

---

## 1일차 · 0–5분 — 3주차 폼 다시 보기

지난주 완성본의 `guestbook.html` — 3주차에 만든 그 폼입니다.

```text
이름·메시지를 넣고 [남기기]
  → 주소: …/guestbook.html?     ← 끝에 ? 가 붙는다
  → 칸이 비고 화면이 처음으로     Console 빨간 줄 없음
```

- 오류가 아닙니다. 브라우저가 폼을 **보내려고** 같은 파일을 다시 연 것입니다.
- 오늘 할 일: 이 동작을 **멈추고**, 입력한 글자를 **내 코드로 읽는 것**입니다.

**폼을 보내면 브라우저는 페이지를 다시 연다.**

---

## 1일차 · 5–13분 — ex01 폼 제출과 preventDefault

[examples/day1/ex01/index.html](examples/day1/ex01/index.html) · [app.js](examples/day1/ex01/app.js)

```js
form2.addEventListener('submit', function (event) {
    event.preventDefault();          // 2. 다시 열기를 막는다
    out2.textContent = '2. 제출을 받았다';
});
```

- 1번 폼(막지 않음): 주소 끝 `?`, 바꾼 글자가 사라집니다. 2번 폼: 그대로 남습니다.
- 6주차 `'click'` 자리에 `'submit'`. 버튼을 눌러도 **Enter** 를 쳐도 폼의 `submit` 입니다.
- Console ⚙ › **Preserve log** 를 켜면 다시 열려도 Console 줄이 남습니다.

**리스너 첫 줄에서 `event.preventDefault()` 로 막아야 결과가 남는다.**

---

## 1일차 · 13–21분 — ex02 입력 칸의 value

[examples/day1/ex02/index.html](examples/day1/ex02/index.html) · [app.js](examples/day1/ex02/app.js)

```js
const atOpen = nameInput.value;             // 1. 열 때 한 번
form.addEventListener('submit', function (event) {
    event.preventDefault();
    const atSubmit = nameInput.value;       // 2. 누를 때마다
    const message = messageInput.value;     // 3. textarea 도 value
});
```

- 처음 열면 1번은 빈 글자, 2번은 지금 적힌 글자. 6주차 ex02(열 때 vs 클릭할 때)와 같은 원리입니다.
- textarea 에 친 글자도 `textContent` 가 아니라 `value` 에 있습니다.

**칸의 글자는 `value`. 읽는 줄은 리스너 안에 둔다.**

---

## 1일차 · 21–28분 — ex03 trim(): 앞뒤 빈칸 떼기

[examples/day1/ex03/index.html](examples/day1/ex03/index.html) · [app.js](examples/day1/ex03/app.js)

```js
const raw = nameInput.value;              // 1. [  student01  ]
const trimmed = nameInput.value.trim();   // 2. [student01]
```

- 빈칸만 넣으면 1번 `[   ]`, 2번 `[]`. 빈칸만 친 칸을 빈 글자 `''` 로 볼 수 있습니다.
- 가운데 빈칸(`student 01`)은 그대로입니다. 빈칸은 Console 의 `[ ]` 안에서 셉니다.
- `.trim` 처럼 괄호를 빼면 값이 아니라 함수가 들어갑니다. 부를 때는 괄호.

**`trim()` 은 앞뒤 빈칸만 뗀 값을 돌려준다.**

---

## 1일차 · 28–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--폼-제출과-입력-값-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

1. 새 폴더 `web-week07` 에 지난주 완성본, `ex/` 에 예제 폴더 세 개(폴더마다 `index.html`·`app.js`).
2. ex01~ex03 — 폴더마다 `index.html` 을 열고 `app.js` 값 바꿔 보기. 무엇이 달라질지 먼저 말해 봅니다. Preserve log 를 켭니다.
3. 새 저장소 `web-week07` 만들어 올리기 · Pages 켜기.

**설명 합계: 5+8+8+7+2 = 30분**

---

# 2일차 — 빈값 안내와 다음 입력, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. 예제 폴더 — 오늘도 폴더 하나에 `index.html`·`app.js`
2. ex04 — `form.reset()` 과 `focus()`: 다음 입력 준비
3. ex05 — 빈값 검사와 `return`
4. ex06 — `'input'` 이벤트: 글자가 바뀔 때마다
5. ex07 — 함수 이름만 맡기기
6. ex08 — 바꾸기 vs 붙이기: `createElement`·`append`
7. 조립 — `web-week07` 의 `guestbook.html`·`guestbook.js`

---

## 2일차 · 0–3분 — 예제 폴더: 오늘도 폴더 하나에 파일 두 개

1일차와 같습니다. 예제마다 폴더 하나, 내 사이트와 같은 이름의 두 파일입니다.

```text
ex04/
  index.html   화면 — 그 예제가 쓰는 칸과 자리만
  app.js       동작 — 오늘 원리는 여기
```

- ex04 는 폼만, ex05 는 폼·안내 자리·결과 자리, ex06·ex07 은 두 칸과 안내 자리, ex08 은 글 칸·버튼·목록.
- `<head>` 의 `<script src="app.js" defer>` 가 같은 폴더의 `app.js` 를 부릅니다.
- 이름이 같은 파일이 많습니다. 저장 창의 폴더와 편집기 위쪽 경로 줄(`ex › ex04`)을 봅니다.

**화면은 HTML, 동작은 JS — 두 파일을 한 폴더에.**

---

## 2일차 · 3–8분 — ex04 reset 과 focus: 다음 입력 준비

[examples/day2/ex04/index.html](examples/day2/ex04/index.html) · [app.js](examples/day2/ex04/app.js)

```js
// 1. 비우기 전에 읽으면 [student01]
console.log(`1. 비우기 전 : [${nameInput.value}] …`);
form.reset();            // 폼 안의 칸을 모두 비운다
// 2. 비운 뒤에 읽으면 []
console.log(`2. 비운 뒤 : [${nameInput.value}] …`);
nameInput.focus();       // 3. 커서를 이름 칸으로
```

- `reset()` 뒤에 읽으면 빈 글자입니다. 그래서 **읽고 나서 비웁니다**.
- `focus()` 는 커서를 옮깁니다. 바로 다음 글을 칠 수 있습니다.

**`reset()` 은 칸을 비우고 `focus()` 는 커서를 옮긴다. 읽은 다음에 비운다.**

---

## 2일차 · 8–13분 — ex05 빈값 검사와 return

[examples/day2/ex05/index.html](examples/day2/ex05/index.html) · [app.js](examples/day2/ex05/app.js)

```js
if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    return;                                  // 1. 여기서 멈춘다
}
if (message === '') { … return; }            // 2.
last.textContent = `${name}: ${message}`;    // 3. 둘 다 찼을 때만
```

- 검사는 위에서부터입니다. 둘 다 비면 1번 안내만 나옵니다.
- `return` 이 없으면 아랫줄도 실행되어 `: 안녕하세요` 가 남습니다.

**빈 칸이면 안내하고 `return` 으로 거기서 멈춘다.**

---

## 2일차 · 13–16분 — ex06 input 이벤트: 글자가 바뀔 때마다

[examples/day2/ex06/index.html](examples/day2/ex06/index.html) · [app.js](examples/day2/ex06/app.js)

```js
// 1. 이름 칸 — 한 글자 칠 때마다, 지울 때도 (2. 메시지 칸도 같다)
nameInput.addEventListener('input', function () {
    notice.textContent = '';
    console.log('1. 이름 칸 input :', nameInput.value);
});
```

- `abc` 를 한 글자씩 치면 1번이 세 줄입니다. 첫 글자에서 안내가 사라집니다.
- `'inptu'` 처럼 이름이 틀리면 빨간 줄 없이 아무 일도 일어나지 않습니다.

**칸의 글자가 바뀔 때마다 `'input'` 이 일어난다.**

---

## 2일차 · 16–19분 — ex07 함수 이름만 맡기기

[examples/day2/ex07/index.html](examples/day2/ex07/index.html) · [app.js](examples/day2/ex07/app.js)

```js
function clearNotice() { notice.textContent = ''; }
// 1. function () { } 안에서 괄호를 붙여 부른다
nameInput.addEventListener('input', function () { clearNotice(); });
// 2. 이름만 맡긴다 — 칠 때마다 브라우저가 부른다
messageInput.addEventListener('input', clearNotice);
```

- 1·2번은 하는 일이 같습니다. 이름 칸이든 메시지 칸이든 치면 안내가 사라집니다.
- `clearNotice()` 로 맡기면 그 줄에서 한 번 불리고 끝입니다. 쳐도 안내가 남고 빨간 줄도 없습니다.

**맡길 때는 함수 이름만, 부를 때는 괄호.**

---

## 2일차 · 19–24분 — ex08 바꾸기 vs 붙이기

[examples/day2/ex08/index.html](examples/day2/ex08/index.html) · [app.js](examples/day2/ex08/app.js)

```js
out1.textContent = textInput.value;          // 1. 바꾸기 — 늘 한 줄
const li = document.createElement('li');     // 2. 줄을 새로 만들고
li.textContent = textInput.value;            //    글자를 넣고
list.append(li);                             //    목록 맨 뒤에 붙인다
```

- 글을 바꿔 가며 누르면 1번 자리는 마지막 글 하나, 목록은 2번을 누를 때마다 한 줄씩 늡니다.
- `append` 를 빼면 만든 줄이 화면에도 Elements 에도 없습니다. 빨간 줄도 없습니다.
- 3주차에 `<ul>` 안에 손으로 적던 `<li>` 를 JavaScript 가 만들어 붙입니다.

**쌓으려면 바꾸지 말고, 줄을 만들어 붙인다.**

---

## 2일차 · 24–27분 — 조립 ① guestbook.html

```text
<head>  <script src="guestbook.js" defer>   ← 6주 app.js 줄
<form id="guestbook-form">                  ← ex01 · ex02
<p>지금은 눌러도 …</p> 를 지우고 그 자리에
  <div id="notice"></div>                   ← ex05 자리
  <h3>남긴 글</h3>
  <ul class="card" id="list"></ul>          ← ex08 목록 · .card
```

- 페이지마다 자기 js 하나: `index.html` 은 `app.js`, `guestbook.html` 은 `guestbook.js`.
- `<ul>` 안은 비워 둡니다. 줄은 JavaScript 가 만들어 붙입니다.
- `index.html`·`app.js`·`styles.css`·`about.html` 은 6주차 그대로입니다.

**HTML 에는 찾을 `id` 와 결과를 쓸 자리만 만든다.**

---

## 2일차 · 27–30분 — 조립 ② guestbook.js, 그리고 실습 인계

```text
const form·nameInput·messageInput·notice·list     ← ex02 · ex05 · ex08
function clearNotice() { … }                      ← ex07
submit 리스너 + event.preventDefault()            ← ex01 2번
const name·message = … .value.trim()              ← ex02 · ex03
if 이름 · if 메시지 { 안내 · focus() · return }   ← ex05 · ex04
clearNotice() · li 만들고 붙이기 · reset · focus  ← ex07 · ex08 2번 · ex04
input 리스너 두 줄(clearNotice 이름만)            ← ex06 · ex07 2번
```

[2일차 실습](lab.md#2일차--빈값-안내와-다음-입력-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_form_input)

1. ex04~ex08 값 바꾸기(29분까지) → 조립 → 375·1280 과 서버로 확인 → push → 캡처.
2. 8주차는 1~7주 [문제 은행](../week08_midterm/examples/README.md)에서 값을 바꿔 냅니다. 오늘 폼도 들어 있습니다.

**설명 합계: 3+5+5+3+3+5+3+3 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week07/guestbook.html
글 두 개를 차례로 남긴 화면
남긴 글
· student01: 안녕하세요
· student02: 반갑습니다
주소창이 함께 보이게 찍습니다
```

빈값 안내(`이름을 입력하세요.`)는 실습 중에 확인하는 것이고 캡처에는 없어도 됩니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

8주차는 **중간 개인 실기**입니다. 1일차에 문제 은행으로 연습하고, 2일차에 실기를 봅니다. 저장소는 `web-week08` 입니다.

[문제 은행](../week08_midterm/examples/README.md)은 공개되어 있습니다. 해답 대신 문제마다 있는 "확인할 것"으로 맞춰 보고 옵니다.

오늘 목록은 화면에만 있습니다. 한 줄씩 지우기는 10주차(배열로 다시 그리기), 새로고침해도 남기기는 11주차입니다.
