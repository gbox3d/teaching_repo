# 7주차 예제 — 폼 제출을 받아 한 줄 남기기

6주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/guestbook.html](day1/guestbook.html) | [2단계](../walkthrough.md#2-guestbookhtml에-결과-자리-만들기) — `script` 줄, `<form>`의 `id`, 결과 자리 세 줄이 늘어난다 | `guestbook.html` |
| [day1/guestbook.js](day1/guestbook.js) | [3~8단계](../walkthrough.md#3-guestbookjs-만들고-요소-찾아-두기) — 새로 만드는 파일이다 | `guestbook.js` |
| [day1/index.html](day1/index.html) · [day1/about.html](day1/about.html) · [day1/app.js](day1/app.js) · [day1/styles.css](day1/styles.css) | [이번 주에 고치지 않는 파일](../walkthrough.md#이번-주에-고치지-않는-파일) — 열지 않는다. 6주차와 같다 | `index.html` · `about.html` · `app.js` · `styles.css` |
| [day2/README.md](day2/README.md) | [11단계](../walkthrough.md#11-github-웹에서-readme-만들고-받아오기) — GitHub 웹에서 만들고 `git pull`로 받는다 | `README.md` |
| [day2/guestbook.js](day2/guestbook.js) | [12~13단계](../walkthrough.md#12-메시지-칸도-검사하기) — 메시지 검사와 `clearNotice()`가 늘어난다 | `guestbook.js` |
| `day2/`의 나머지 여섯 파일 | day1과 같다. 2일차에 고치지 않는다 | `guestbook.html` · `index.html` · `about.html` · `app.js` · `styles.css` · `images/profile.png` |

`day1/`에는 `README.md`가 없다. 저장소 설명 파일은 2일차에 GitHub 웹에서 만들기 때문이다.
`images/profile.png`는 3주차에 넣은 그림 그대로다. `guestbook.html`의 이메일 칸은 3주차 것을 그대로 두되 이번 주에 읽지 않는다.

## 1. 1일차 완성 — 제출하면 한 줄이 남는다

`day1/guestbook.html`을 브라우저로 열면 3주차 폼 아래에 결과 자리가 생겨 있다.

```text
[이름 ______]  [이메일 ______]  [메시지 ______]
[남기기]

마지막으로 남긴 글
아직 남긴 글이 없습니다.        ← 아직 누르지 않았다
```

이름에 `student01`, 메시지에 `안녕하세요`를 넣고 **[남기기]**를 누르면 이렇게 바뀐다.

```text
[이름 ______]  [이메일 ______]  [메시지 ______]   ← 세 칸이 비워졌다. 커서는 이름 칸
[남기기]

마지막으로 남긴 글
student01: 안녕하세요
```

- 페이지가 새로고침되지 않고 주소도 그대로다. `event.preventDefault()`가 막고 있다.
- 새로고침하면 `아직 남긴 글이 없습니다.`로 돌아간다. 바뀐 것은 화면이지 HTML 파일이 아니다.
- `guestbook.html`은 `guestbook.js`를, `index.html`은 `app.js`를 부른다. 페이지마다 자기 js 하나다.

### 개념별 최소 코드

제출을 받아 새로고침을 막기:

```js
form.addEventListener('submit', function (event) {
  event.preventDefault();
});
```

`event.preventDefault()`가 없으면 주소 끝에 `?`가 붙으면서 페이지가 처음 상태로 돌아간다.

입력 칸의 값 읽어 표시하기:

```js
const name = nameInput.value.trim();

last.textContent = `${name}: ${message}`;
```

`.value`는 칸에 지금 적혀 있는 글자, `.trim()`은 앞뒤 공백을 떼어 낸 값이다.

비었으면 안내하고 멈추기:

```js
if (name === '') {
  notice.textContent = '이름을 입력하세요.';
  nameInput.focus();
  return;
}
```

`return`을 빠뜨리면 안내를 띄운 **뒤에도** 아랫줄이 실행되어 `: 안녕하세요`가 그대로 표시된다.

## 2. 2일차 완성 — 두 칸 검사와 안내 문구 지우기

`day2/guestbook.js`는 day1에 세 곳이 늘어난 것이다.

```js
function clearNotice() {
  notice.textContent = '';
}
```

```js
  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }
```

```js
nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

`day2/guestbook.html`을 열고 이름을 비운 채 **[남기기]**를 누른 뒤, 이름 칸에 한 글자를 치면 이렇게 된다.

```text
누른 직후          이름을 입력하세요.       ← 커서는 이름 칸
한 글자 친 뒤      (안내 문구가 사라진다)
```

- 검사는 위에서부터 차례로 한다. 이름이 비면 `return`으로 끝나 메시지 검사까지 가지 않는다.
- `'input'`은 칸의 글자가 바뀔 때마다 일어난다. 6주차 `addEventListener`에서 이벤트 이름만 바뀐 것이다.
- 맡길 때는 `clearNotice`에 괄호를 붙이지 않는다. 붙이면 맡기는 순간 한 번 실행되고 만다.

`day2/README.md`는 GitHub 웹에서 만들어 `git pull`로 받은 파일이다. 저장소 첫 화면에 그대로 보인다.

## 3. 두 날의 guestbook.js 비교

| | 1일차 | 2일차 |
|---|---|---|
| 찾아 두는 요소 | `#guestbook-form` · `#name` · `#message` · `#notice` · `#last` | 같다 |
| 검사하는 칸 | 이름 하나 | 이름·메시지 둘 |
| 안내 문구 지우기 | 성공했을 때 한 줄 | `clearNotice()` 함수 + `'input'` 리스너 두 줄 |
| 함수 | 없다 | `clearNotice()` 하나 |
| 리스너 | `submit` 1개 | `submit` 1개 + `input` 2개 |
| 줄 수 | 23줄 | 36줄 |

`#name`·`#message`·`#notice`·`#last`는 이름을 바꾸지 않는다. 10주차에 `#last`를 목록으로 바꿔 이어 쓴다.

## 공식 참고 자료

- [HTMLFormElement: submit 이벤트 — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLFormElement/submit_event)
- [Event.preventDefault() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Event/preventDefault)
- [String.prototype.trim() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/String/trim)
- [HTMLFormElement.reset() — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLFormElement/reset)
- [HTMLElement.focus() — MDN](https://developer.mozilla.org/ko/docs/Web/API/HTMLElement/focus)
