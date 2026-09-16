# 11주차 예제 — 객체로 바꾸고 브라우저에 저장하기

10주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/guestbook.js](day1/guestbook.js) | [2~5단계](../walkthrough.md#2-남긴-글을-객체로-바꾸기) — 항목이 객체가 되고, 안내 문구와 빈 목록 안내가 한 자리로 모인다 | `guestbook.js` |
| [day1/guestbook.html](day1/guestbook.html) | [5단계](../walkthrough.md#5-빈-목록-안내를-개수-자리로-옮기기) — `<p id="empty">` 한 줄이 사라지고 `<p id="count">`의 처음 글자가 바뀐다 | `guestbook.html` |
| [day1/index.html](day1/index.html) · [day1/about.html](day1/about.html) · [day1/app.js](day1/app.js) · [day1/styles.css](day1/styles.css) · [day1/README.md](day1/README.md) | [이번 주에 고치지 않는 파일](../walkthrough.md#이번-주에-고치지-않는-파일) — 열지 않는다. 10주차와 같다 | `index.html` · `about.html` · `app.js` · `styles.css` · `README.md` |
| [day2/guestbook.js](day2/guestbook.js) | [8~11단계](../walkthrough.md#8-저장하는-함수-savelist-만들기) — `saveList()`·복원 한 줄·전체 지우기가 들어온다 | `guestbook.js` |
| [day2/guestbook.html](day2/guestbook.html) | [11단계](../walkthrough.md#11-전체-지우기-버튼-붙이기) — **[전체 지우기]** 버튼 한 줄이 늘어난다 | `guestbook.html` |
| `day2/`의 나머지 파일 | day1과 같다. 2일차에 고치지 않는다 | `index.html` · `about.html` · `app.js` · `styles.css` · `README.md` · `images/` · `screenshots/` |

`images/profile.png`는 3주차에 넣은 그림, `README.md`와 `screenshots/` 두 장은 9주차 1차 과제에서 만든 것 그대로다.
`guestbook.html`의 이메일 칸도 3주차 것을 그대로 두고 이번 주에도 읽지 않는다.

**이번 주부터 확인은 공개 주소에서 한다.** 예제 파일을 내 PC에서 직접 열어도 동작하지만,
그때 남긴 글은 공개 주소의 저장 칸이 아니라 내 PC 파일 주소의 저장 칸에 들어간다.

## 1. 1일차 완성 — 한 줄에 이름·메시지·날짜

`day1/guestbook.html`을 열고 이름과 메시지를 넣어 두 번 남기면 이렇게 된다.

```text
남긴 글
· 하늘: 안녕하세요 (2026. 9. 16.)   [삭제]
· 바다: 잘 봤습니다 (2026. 9. 16.)   [삭제]
2개
```

- 10주차에는 `하늘: 안녕하세요` 문자열 하나가 배열에 들어갔다. 이제 값 세 개가 이름표와 함께 들어간다.
- 날짜는 남긴 그날의 날짜다. `2026. 9. 16.`처럼 보이는 것은 브라우저가 한국어 설정이기 때문이다.
- 새로고침하면 목록이 사라진다. 1일차 목록은 아직 화면에만 있다.
- 이름이나 메시지 중 하나라도 비우고 누르면 `이름과 메시지를 모두 입력하세요.`가 보이고 아무것도 쌓이지 않는다.

### 개념별 최소 코드

객체 만들고 꺼내기:

```js
const item = { name: '하늘', message: '안녕하세요', date: '2026. 9. 16.' };

console.log(item.name);      // 하늘
console.log(item.date);      // 2026. 9. 16.
```

`{ }` 안에 `이름: 값` 쌍을 쉼표로 잇는다. 꺼낼 때는 점 표기 `item.name`을 쓴다. 이름표에 따옴표를 붙이지 않는다.

배열 안의 객체 읽기:

```js
li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

`items[i]`가 `i`번째 **객체**이고, 그 뒤의 `.name`이 그 객체 안의 값 하나다.
점 표기를 빼고 `items[i]`만 쓰면 화면에 `[object Object]`가 보인다. 오류는 나지 않는다.

## 2. 2일차 완성 — 새로고침해도 남는다

`day2/guestbook.js`는 day1과 네 곳이 다르다. 첫째, 저장하는 함수가 생겼다.

```js
function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}
```

둘째, 추가한 뒤와 삭제한 뒤 두 곳에서 그 함수를 부른다.

```js
  items.push({ name: name, message: message, date: today });
  saveList();
```

셋째, 페이지를 열 때 저장 칸에서 되살린다. 이 한 줄은 그대로 옮겨 쓰는 **틀**이다.

```js
let items = JSON.parse(localStorage.getItem('guestbook')) || [];
```

넷째, **[전체 지우기]** 버튼이 화면 쪽 배열과 저장 칸을 함께 비운다.

```js
clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});
```

`day2/guestbook.html`을 열고 글 세 개를 남긴 뒤 새로고침하면 목록이 그대로 남아 있다.
F12 **Application › Local Storage**에서 값을 보면 이렇게 들어 있다.

```text
Key     guestbook
Value   [{"name":"하늘","message":"안녕하세요","date":"2026. 9. 16."}]
```

- 저장 칸에는 **문자열만** 들어간다. 그래서 넣기 전에 `JSON.stringify`, 꺼낸 뒤에 `JSON.parse`를 쓴다.
- `JSON.stringify` 없이 배열을 그대로 넣으면 값이 `[object Object]`로 적히고, 다음에 열 때 `JSON.parse`가 오류를 낸다.
- `|| []`가 없으면 처음 여는 사람은 `null`을 받아 `Cannot read properties of null (reading 'length')`로 멈춘다.
- 키 이름 `guestbook`은 12주차·15주차와 이어지는 이름이다. 바꾸지 않는다(15주차 기말 starter만 다른 키를 쓴다).

## 3. 두 날의 guestbook.js 비교

| | 1일차 | 2일차 |
|---|---|---|
| 찾아 두는 요소 | `#guestbook-form` · `#name` · `#message` · `#notice` · `#list` · `#count` | 위 여섯 개 + `#clear-button` |
| 배열 | `let items = [];` | `let items = JSON.parse(localStorage.getItem('guestbook')) \|\| [];` |
| 저장 | 없다 | `saveList()` — `setItem('guestbook', JSON.stringify(items))` |
| 저장을 부르는 곳 | 없다 | 제출 뒤 한 곳, 삭제 버튼 안 한 곳 |
| 전체 지우기 | 없다 | `items = []` + `removeItem('guestbook')` + `showList()` |
| 새로고침 | 목록이 사라진다 | 목록이 그대로 남는다 |
| 줄 수 | 47줄 | 60줄 |

`#list`·`#count`·`#clear-button`과 `items`·`showList()`·`saveList()`는 이름을 바꾸지 않는다.
12주차에 `projects.html`·`projects.js`를 더할 때 이 파일은 그대로 두고 nav에 네 번째 링크만 붙인다.

## 공식 참고 자료

- [객체로 작업하기 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Working_with_objects)
- [속성 접근자 — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/Property_accessors)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [JSON.stringify() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)
- [JSON.parse() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
- [Date.prototype.toLocaleDateString() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString)
