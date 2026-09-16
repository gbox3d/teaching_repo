# 6주차 예제 — 클릭 카운터와 다크 모드

5주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [3단계](../walkthrough.md#3-버튼과-카운터-자리-만들기) — `#greeting` 아래에 두 문단이 늘어난다 | `index.html` |
| [day1/app.js](day1/app.js) | [4~7단계](../walkthrough.md#4-요소를-찾아-두기) — 5주차 코드를 이어받아 위와 아래를 더한다 | `app.js` |
| [day1/styles.css](day1/styles.css) · [day1/about.html](day1/about.html) · [day1/guestbook.html](day1/guestbook.html) | [9단계](../walkthrough.md#9-나머지-파일은-그대로-둔다) — 열지 않는다. 5주차와 같다 | `styles.css` · `about.html` · `guestbook.html` |
| [day2/index.html](day2/index.html) | [11단계](../walkthrough.md#11-다크-모드-버튼-넣기) — 같은 문단 안에 버튼 한 줄이 늘어난다 | `index.html` |
| [day2/styles.css](day2/styles.css) | [12단계](../walkthrough.md#12-어두운-색-규칙-더하기) — 맨 아래에 규칙 하나가 늘어난다 | `styles.css` |
| [day2/app.js](day2/app.js) | [13~14단계](../walkthrough.md#13-classlisttoggle로-다크-모드-켜고-끄기) — 다크 버튼과 `countUp()`이 늘어난다 | `app.js` |
| `day2/`의 `about.html`·`guestbook.html` | day1과 같다. 이번 주에 고치지 않는다 | `about.html` · `guestbook.html` |

`day1/images/profile.png`와 `day2/images/profile.png`는 3주차에 넣은 그림 그대로다.
`guestbook.html`은 6주차에 손대지 않는다. 그 폼이 동작하는 것은 7주차다.

## 1. 1일차 완성 — 인사 바꾸기 버튼과 클릭 횟수

`day1/index.html`을 브라우저로 열면 5주차 화면에 버튼 하나와 카드 하나가 늘어 있다.

```text
안녕하세요, student01님! 좋은 아침입니다.   ← app.js가 바꾼 글자
[인사 바꾸기]
클릭 0회                                     ← 아직 누르지 않았다
```

버튼을 두 번 누르면 이렇게 바뀐다.

```text
반갑습니다. 오늘도 좋은 하루 되세요.
[인사 바꾸기]
클릭 2회
```

- `index.html`에서 늘어난 곳은 `#greeting` 카드 **바로 아래** 두 문단뿐이다.
- 새로고침하면 `클릭 0회`로 돌아간다. 브라우저가 파일을 다시 읽어 화면을 새로 만들기 때문이다.
- `about.html`·`guestbook.html`에는 `script` 줄이 없다. 이번 주 JavaScript는 `index.html`만의 것이다.

### 개념별 최소 코드

요소를 찾아 두고 글자를 바꾸기:

```js
const greeting = document.querySelector('#greeting');

greeting.textContent = '반갑습니다.';
```

`querySelector`가 못 찾으면 `null`이 되고, 그다음 줄에서 `Uncaught TypeError: Cannot set properties of null (setting 'textContent')`이 뜬다.

클릭했을 때 실행되는 코드:

```js
let count = 0;

helloButton.addEventListener('click', function () {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
});
```

`let count = 0;`을 중괄호 **안**에 두면 누를 때마다 0에서 다시 시작해 `클릭 1회`만 나온다.

## 2. 2일차 완성 — 다크 모드와 함수 재사용

`day2/`는 day1에 세 곳이 늘어난 것이다.

```html
<button id="dark-button" type="button">다크 모드</button>
```

```css
body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

```js
darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
  countUp();
});
```

`day2/index.html`을 열고 `[인사 바꾸기]` 2번, `[다크 모드]` 1번을 누르면 아래처럼 된다.

```text
<body class="dark">      ← DevTools Elements에서 보이는 모습
배경·카드: 어두운 색 (#222222)
카드: 반갑습니다. 오늘도 좋은 하루 되세요.
카드: 클릭 3회            ← 두 버튼의 클릭 합계
```

- JavaScript가 하는 일은 class `dark`를 붙였다 떼는 것뿐이다. 색을 정하는 것은 `styles.css`다.
- 그래서 `body.dark` 규칙을 지우면 class는 붙지만 화면은 그대로다.
- 클릭 합계가 `클릭 3회`인 것이 `countUp()`을 두 버튼이 함께 쓴다는 증거다.

## 3. 두 날의 app.js 비교

| | 1일차 | 2일차 |
|---|---|---|
| 찾아 두는 요소 | `#greeting` · `#count` · `#hello-button` | 위 셋 + `#dark-button` |
| 새로 쓰는 것 | `querySelector` · `textContent` · `addEventListener('click')` | `classList.toggle` · `countUp()` 함수 |
| 클릭 횟수 | 리스너 안에서 직접 2줄 | `countUp()` 한 함수를 두 리스너가 부른다 |
| 5주차에서 이어받은 것 | `name` · `hour` · `greet(name)` · `hello(hour)` | 같다 |
| 줄 수 | 26줄 | 36줄 |

`#greeting`·`greet(name)`·`hello(hour)`는 5주차 이름 그대로다. 이름을 바꾸지 않는다.

## 공식 참고 자료

- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [EventTarget.addEventListener() — MDN](https://developer.mozilla.org/ko/docs/Web/API/EventTarget/addEventListener)
- [Element.classList — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/classList)
