# 5주차 예제 — 인사말을 만드는 app.js

4주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [2단계](../walkthrough.md#2-indexhtml에-script-줄-되살리기) — `script` 한 줄만 늘어난다 | `index.html` |
| [day1/app.js](day1/app.js) | [3~6단계](../walkthrough.md#3-appjs-비우고-첫-줄-쓰기) — 2주차 내용을 지우고 새로 쓴다 | `app.js` |
| [day1/about.html](day1/about.html) · [day1/guestbook.html](day1/guestbook.html) · [day1/styles.css](day1/styles.css) | [8단계](../walkthrough.md#8-나머지-파일은-그대로-둔다) — 열지 않는다. 4주차와 같다 | `about.html` · `guestbook.html` · `styles.css` |
| [day2/index.html](day2/index.html) | [10단계](../walkthrough.md#10-인사말-자리-만들기) — `<main>` 첫 줄에 한 줄이 늘어난다 | `index.html` |
| [day2/app.js](day2/app.js) | [11~14단계](../walkthrough.md#11-지금-시각-가져오기) — day1 내용을 지우고 함수로 다시 쓴다 | `app.js` |
| `day2/`의 나머지 세 파일 | day1과 같다. 이번 주에 고치지 않는다 | `about.html` · `guestbook.html` · `styles.css` |

`day1/images/profile.png`와 `day2/images/profile.png`는 3주차에 넣은 그림 그대로다.

## 1. 1일차 완성 — Console에만 찍는 app.js

`day1/index.html`을 브라우저로 열고 **F12 › Console**을 보면 여섯 줄이 찍혀 있다. 화면은 4주차와 똑같다.

```text
app.js가 실행되었습니다     ← 1행
student01                   ← 6행  console.log(name)
9                           ← 7행  console.log(hour)
15                          ← 10행 hour = 15 뒤에 다시 찍음
안녕하세요, student01님!     ← 14행 템플릿 문자열
지금은 15시입니다.           ← 15행
```

- `index.html`에서 바뀐 곳은 `<script src="app.js" defer></script>` **한 줄뿐**이다. `styles.css` 줄 바로 아래에 둔다.
- 1일차 `app.js`는 화면을 건드리지 않는다. 그래서 새로고침해도 페이지 모양이 그대로다.
- `about.html`·`guestbook.html`에는 `script` 줄이 없다. 방명록 동작은 7주차에 `guestbook.js`로 만든다.

### 개념별 최소 코드

값 담기와 다시 넣기:

```js
const name = 'student01';
let hour = 9;

hour = 15;
```

`const`에 다시 넣으면 Console에 `Uncaught TypeError: Assignment to constant variable.`이 뜬다.

템플릿 문자열:

```js
const greeting = `안녕하세요, ${name}님!`;
```

백틱 대신 작은따옴표로 감싸면 `안녕하세요, ${name}님!`이 글자 그대로 찍힌다.

## 2. 2일차 완성 — if와 함수로 만든 인사말

`day2/`는 day1에 두 곳이 늘거나 바뀐 것이다.

```html
<p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

```js
function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}
```

`day2/index.html`을 열면 카드 한 줄이 아래처럼 바뀐다.

```text
열기 전: 인사말을 준비 중입니다.          ← HTML에 적힌 글자
열고 나서: 안녕하세요, student01님! 좋은 아침입니다.   ← app.js 마지막 줄이 바꾼 글자
Console: 10 / 안녕하세요, student01님! 좋은 아침입니다.
```

- 앞의 `10`은 `new Date().getHours()`가 준 지금 시각이다. 여는 시각에 따라 숫자와 인사가 달라진다.
- 12시가 지나면 `좋은 오후입니다.`가 나온다. 두 갈래 모두 정답이다.
- `인사말을 준비 중입니다.`가 그대로 남아 있으면 마지막 줄까지 가지 못한 것이다. Console의 빨간 줄을 먼저 본다.

## 3. 두 날의 app.js 비교

| | 1일차 | 2일차 |
|---|---|---|
| 목적 | 값을 만들고 Console에서 확인 | 문장을 고르고 화면에 표시 |
| 새로 쓰는 것 | `console.log` · `const`·`let` · 템플릿 문자열 | `if / else` · `function`·`return` · 화면 한 줄 틀 |
| `hour` | `let hour = 9;` 뒤에 `hour = 15;` | `const hour = new Date().getHours();` |
| 화면 | 바뀌지 않는다 | `#greeting` 한 줄이 바뀐다 |
| 줄 수 | 15줄 | 21줄 |

`greet(name)`·`hello(hour)` 두 함수와 `#greeting`은 6주차에 그대로 쓴다. 이름을 바꾸지 않는다.

## 공식 참고 자료

- [변수에 필요한 정보 저장하기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Variables)
- [조건문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Conditionals)
- [나만의 함수 만들기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Build_your_own_function)
