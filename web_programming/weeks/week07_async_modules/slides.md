---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 7주차"
footer: "폼 입력 읽기와 결과 표시 · 비교 예제로 원리를 보고 마지막에 조립"
---

# 폼 입력 읽기와 결과 표시

6주차에는 버튼을 누르면 **정해 둔 글자**를 띄웠습니다. 이번 주는 방명록 폼에 **사용자가 입력한 글자**를 읽어 띄웁니다.

이번 주 방식도 같습니다: **비교 예제 7개**를 하나씩 보고, 마지막에 새 저장소 `web-week07` 의 `guestbook.html`·`guestbook.js` 를 **조립**합니다(지난주 완성본에서 시작).

- 폼을 보내면 브라우저는 페이지를 **다시 엽니다**. 그것을 막아야 결과가 남습니다.
- 결과는 화면, **주소창**, **Console** 에서 봅니다.
- 파일 하나 = 개념 하나. 실습은 **값을 바꿔 보는 것**입니다.

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

[examples/day1/ex01_submit.html](examples/day1/ex01_submit.html) · [ex01_submit.js](examples/day1/ex01_submit.js)

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

[examples/day1/ex02_value.html](examples/day1/ex02_value.html) · [ex02_value.js](examples/day1/ex02_value.js)

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

[examples/day1/ex03_trim.html](examples/day1/ex03_trim.html) · [ex03_trim.js](examples/day1/ex03_trim.js)

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

[1일차 실습](lab.md#1일차--폼-제출과-입력-값-60분) · [따라하기](walkthrough.md#1일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

1. 새 폴더 `web-week07` 에 지난주 완성본, `ex/` 에 오늘 여섯 파일(`.html`·`.js` 세 쌍).
2. ex01~ex03 — 값 바꿔 보기. 무엇이 달라질지 먼저 말해 봅니다. Preserve log 를 켭니다.
3. 새 저장소 `web-week07` 만들어 올리기 · Pages 켜기.

**설명 합계: 5+8+8+7+2 = 30분**

---

# 2일차 — 빈값 안내와 다음 입력, 그리고 조립

`30분 설명·시연 → 60분 실습`

1. 고르기 페이지 — 네 예제가 같은 폼을 쓴다
2. ex04 — `form.reset()` 과 `focus()`: 다음 입력 준비
3. ex05 — 빈값 검사와 `return`
4. ex06 — `'input'` 이벤트: 글자가 바뀔 때마다
5. ex07 — 함수 이름만 맡기기
6. 조립 — `web-week07` 의 `guestbook.html`·`guestbook.js`

---

## 2일차 · 0–3분 — 고르기 페이지: 네 예제가 같은 폼을 쓴다

[examples/day2/index.html](examples/day2/index.html) — 방명록 모양 폼, 안내 자리 `#notice`, 결과 자리 `#last`.

```html
<script src="ex04_reset_focus.js"></script>
<!-- <script src="ex05_empty.js"></script> -->
<!-- <script src="ex06_input.js"></script> -->
<!-- <script src="ex07_pass_name.js"></script> -->
```

- 5·6주차와 같은 방법입니다. **Ctrl+/**(macOS ⌘+/)로 **한 줄만** 켭니다.
- 두 줄을 켜면 같은 이름의 `const` 가 겹쳐 둘째 파일이 빨간 줄을 내고 멈춥니다.

**어느 코드를 불러올지는 `script` 줄 하나가 정한다.**

---

## 2일차 · 3–9분 — ex04 reset 과 focus: 다음 입력 준비

[examples/day2/ex04_reset_focus.js](examples/day2/ex04_reset_focus.js)

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

## 2일차 · 9–15분 — ex05 빈값 검사와 return

[examples/day2/ex05_empty.js](examples/day2/ex05_empty.js)

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

## 2일차 · 15–19분 — ex06 input 이벤트: 글자가 바뀔 때마다

[examples/day2/ex06_input.js](examples/day2/ex06_input.js)

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

## 2일차 · 19–23분 — ex07 함수 이름만 맡기기

[examples/day2/ex07_pass_name.js](examples/day2/ex07_pass_name.js)

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

## 2일차 · 23–26분 — 조립 ① guestbook.html

```text
<head>  <script src="guestbook.js" defer>   ← 6주 app.js 줄
<form id="guestbook-form">                  ← ex01 · ex02
<p>지금은 눌러도 …</p> 를 지우고 그 자리에
  <div id="notice"></div>                   ← ex05 자리
  <h3>마지막으로 남긴 글</h3>
  <div class="card" id="last">…</div>       ← ex05 · .card
```

- 페이지마다 자기 js 하나: `index.html` 은 `app.js`, `guestbook.html` 은 `guestbook.js`.
- `index.html`·`app.js`·`styles.css`·`about.html` 은 6주차 그대로입니다.

**HTML 에는 찾을 `id` 와 결과를 쓸 자리만 만든다.**

---

## 2일차 · 26–30분 — 조립 ② guestbook.js, 그리고 실습 인계

```text
const form·nameInput·messageInput·notice·last     ← ex02 · ex05
function clearNotice() { … }                      ← ex07
submit 리스너 + event.preventDefault()            ← ex01 2번
const name·message = … .value.trim()              ← ex02 · ex03
if 이름 · if 메시지 { 안내 · focus() · return }   ← ex05 · ex04
clearNotice() · 결과 한 줄 · reset() · focus()    ← ex07 · ex05 · ex04
input 리스너 두 줄(clearNotice 이름만)            ← ex06 · ex07 2번
```

[2일차 실습](lab.md#2일차--빈값-안내와-다음-입력-그리고-조립-60분) · [따라하기](walkthrough.md#2일차) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week07_async_modules)

1. ex04~ex07 값 바꾸기(29분까지) → 조립 → 375·1280 과 서버로 확인 → push → 캡처.
2. 8주차는 1~7주 [문제 은행](../week08_midterm/examples/README.md)에서 값을 바꿔 냅니다. 오늘 폼도 들어 있습니다.

**설명 합계: 3+6+6+4+4+3+4 = 30분**

---

## 제출하기

2일차가 끝나면 캡처 **한 장**을 제출합니다.

```text
https://student01.github.io/web-week07/guestbook.html
이름 student01 · 메시지 안녕하세요 를 넣고 [남기기]
마지막으로 남긴 글
카드: student01: 안녕하세요
주소창이 함께 보이게 찍습니다
```

빈값 안내(`이름을 입력하세요.`)는 실습 중에 확인하는 것이고 캡처에는 없어도 됩니다.
캡처에 실명·학번·실제 이메일이 보이지 않게 합니다.

---

## 다음 주 미리 보기

8주차는 **중간 개인 실기**입니다. 1일차에 문제 은행으로 연습하고, 2일차에 실기를 봅니다. 저장소는 `web-week08` 입니다.

[문제 은행](../week08_midterm/examples/README.md)은 공개되어 있습니다. 해답 대신 문제마다 있는 "확인할 것"으로 맞춰 보고 옵니다.

지금은 두 번째 글을 남기면 앞 글이 사라집니다. 글을 쌓는 목록은 10주차, 새로고침해도 남기기는 11주차입니다.
이 주차 폴더 이름의 비동기(async)는 12주차 `fetch` 에서 다루고, 모듈(`import`/`export`)은 이 과목 범위 밖입니다.
