# 10주차 예제 — 배열에 쌓아 목록으로 그리기

9주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/guestbook.html](day1/guestbook.html) | [2단계](../walkthrough.md#2-목록-자리-만들기) — 마지막 글 두 줄이 `<ul id="list">`·`<p id="count">` 세 줄로 바뀐다 | `guestbook.html` |
| [day1/guestbook.js](day1/guestbook.js) | [3~6단계](../walkthrough.md#3-배열과-목록-상자-찾아-두기) — `let items = []`와 목록에 붙이는 다섯 줄, 항목 수 한 줄이 늘어난다 | `guestbook.js` |
| [day1/index.html](day1/index.html) · [day1/about.html](day1/about.html) · [day1/app.js](day1/app.js) · [day1/styles.css](day1/styles.css) · [day1/README.md](day1/README.md) | [이번 주에 고치지 않는 파일](../walkthrough.md#이번-주에-고치지-않는-파일) — 열지 않는다. 9주차와 같다 | `index.html` · `about.html` · `app.js` · `styles.css` · `README.md` |
| [day2/guestbook.html](day2/guestbook.html) | [12단계](../walkthrough.md#12-빈-목록-안내-넣기) — `<p id="empty">` 한 줄이 늘어난다 | `guestbook.html` |
| [day2/guestbook.js](day2/guestbook.js) | [9~13단계](../walkthrough.md#9-다시-그리는-함수-showlist-만들기) — `showList()`와 삭제 버튼 틀이 들어온다 | `guestbook.js` |
| `day2/`의 나머지 파일 | day1과 같다. 2일차에 고치지 않는다 | `index.html` · `about.html` · `app.js` · `styles.css` · `README.md` · `images/` · `screenshots/` |

`images/profile.png`는 3주차에 넣은 그림, `README.md`와 `screenshots/` 두 장은 9주차 1차 과제에서 만든 것 그대로다.
`guestbook.html`의 이메일 칸도 3주차 것을 그대로 두고 이번 주에도 읽지 않는다.

## 1. 1일차 완성 — 남긴 글이 쌓인다

`day1/guestbook.html`을 브라우저로 열면 폼 아래가 이렇게 바뀌어 있다.

```text
[이름 ______]  [이메일 ______]  [메시지 ______]
[남기기]

남긴 글
(빈 카드)
0개                       ← 아직 아무것도 남기지 않았다
```

이름과 메시지를 넣고 **[남기기]**를 세 번 누르면 이렇게 된다.

```text
남긴 글
· student01: 안녕하세요
· student02: 고맙습니다
· student03: 반갑습니다
3개                       ← 누를 때마다 숫자가 오른다
```

- 7주차에는 새 글이 앞 글을 덮어썼다. 이제 `items` 배열에 쌓고 `<li>`를 하나씩 붙이므로 앞 글이 남는다.
- 화면의 줄을 세지 않고 `items.length`를 그대로 보여 준다. 배열이 원본이고 화면은 그 배열을 비춘 것이다.
- 새로고침하면 목록이 사라진다. 오늘 글은 화면에만 있다. 남게 하는 것은 11주차다.
- 이름이나 메시지를 비우고 누르면 7주차처럼 안내만 나오고 배열에도 화면에도 들어가지 않는다.

### 개념별 최소 코드

배열에 쌓기:

```js
let items = [];

items.push(text);
console.log(items.length);
```

`push`는 배열 **뒤에** 하나를 더한다. `length`는 개수이며 `0개`·`1개`처럼 그대로 화면에 쓴다.

목록 한 줄 만들어 붙이기:

```js
const li = document.createElement('li');
li.textContent = text;
list.append(li);
```

만들기 → 글자 넣기 → 붙이기 세 줄이 한 묶음이다. `append`하지 않으면 만들어만 두고 화면에는 보이지 않는다.

## 2. 2일차 완성 — 다시 그리기와 삭제 버튼

`day2/guestbook.js`는 day1과 세 곳이 다르다. 첫째, 목록을 그리는 일이 `showList()` 함수로 모였다.

```js
function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
```

둘째, submit 안에서 화면을 직접 만들지 않고 배열에 넣은 뒤 `showList()`를 부른다.

```js
  items.push(`${name}: ${message}`);
  showList();
```

셋째, 줄마다 **[삭제]** 버튼이 붙는다. 이 일곱 줄은 그대로 옮겨 쓰는 **틀**이다.

```js
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
```

`day2/guestbook.html`을 열고 글 세 개를 남긴 뒤 **가운데** 줄의 **[삭제]**를 누르면 이렇게 된다.

```text
누르기 전                            누른 뒤
· student01: 안녕하세요  [삭제]      · student01: 안녕하세요  [삭제]
· student02: 고맙습니다  [삭제]      · student03: 반갑습니다  [삭제]
· student03: 반갑습니다  [삭제]      2개
3개
```

- 가운데를 지워도 남은 줄의 버튼이 밀리지 않는다. `showList()`가 다시 그릴 때 버튼마다 번호를 새로 붙이기 때문이다.
- 항목 수는 `items.length`를 다시 읽으므로 따로 빼지 않아도 함께 줄어든다.
- 모두 지우면 `아직 남긴 글이 없습니다.`가 다시 보인다. 페이지를 처음 열었을 때도 같은 화면이다.
- `list.innerHTML = ''`는 **비우기에만** 쓴다. 입력한 글을 넣을 때는 쓰지 않는다(13주차에 이유를 본다).

## 3. 두 날의 guestbook.js 비교

| | 1일차 | 2일차 |
|---|---|---|
| 찾아 두는 요소 | `#guestbook-form` · `#name` · `#message` · `#notice` · `#list` · `#count` | 위 여섯 개 + `#empty` |
| 배열 | `let items = []` | 같다 |
| 목록 그리는 곳 | submit 안 (다섯 줄) | `showList()` 함수 하나 |
| submit 안 | `items.push(text)` + `<li>` 세 줄 + 항목 수 | `items.push(…)` + `showList()` 두 줄 |
| 삭제 | 없다 | 줄마다 **[삭제]** 버튼(`splice(i, 1)` → `showList()`) |
| 빈 목록 안내 | 없다 | `items.length === 0`이면 문장을 보인다 |
| 줄 수 | 39줄 | 59줄 |

`#list`·`#count`·`#empty`와 `items`·`showList()`는 이름을 바꾸지 않는다. 11주차에 `items`를 객체 배열로 바꾸고 `localStorage`에 저장할 때 그대로 이어 쓴다.

## 공식 참고 자료

- [Array.prototype.push() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/push)
- [Array.prototype.splice() — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/splice)
- [for — MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/for)
- [Document.createElement() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/createElement)
- [Element.append() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/append)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
