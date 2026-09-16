# 11주차 따라하기 — 항목을 객체로 바꾸고 브라우저에 저장하기

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주에 고치는 파일은 `guestbook.html`과 `guestbook.js` 둘뿐이다.
`index.html`·`about.html`·`app.js`·`styles.css`·`README.md`는 10주차 그대로 둔다. 전체 내용은 [이번 주에 고치지 않는 파일](#이번-주에-고치지-않는-파일)에 있다.
예제 파일은 빈 줄 없이 이어 두었다. 내 파일에 빈 줄이 더 있어도 동작은 같다.

**이번 주부터 확인과 캡처는 공개 주소에서만 한다.** 브라우저의 저장 칸은 주소마다 따로 있어서,
내 PC에서 파일을 직접 연 화면(`file://`)에 남긴 글은 공개 주소에서 보이지 않는다.
1일차 중간 화면은 내 PC에서 미리 봐도 되지만, 저장이 들어가는 2일차부터는 공개 주소에서 확인한다.

## 1일차

### 1. 저장소 받아오기

지난 시간과 같은 PC면 `git pull`로 받아 온다. 현재 폴더: `my-web`

```bash
git pull
git status
```

다른 PC에서 처음 여는 경우에는 clone부터 한다. 현재 폴더: 저장소를 둘 위치

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

**예상 결과** — `git pull`은 새 commit이 없으면 `Already up to date.`, 있으면 `Updating …`과 `Fast-forward`가 보인다.
`git status`는 `On branch main`과 `nothing to commit, working tree clean`이다. VS Code **File › Open Folder**로 `my-web`을 연다.

- 10주차와 같이 브랜치를 만들지 않고 `main`에서 바로 작업한다.
- `guestbook.html`을 열었을 때 `<p id="empty">`와 `<p id="count">0개</p>` 두 줄이 보이면 10주차 끝 상태가 맞다.
- clone이 로그인 문제로 막히면 조교에게 10주차 `examples/day2` 폴더를 받아 그 폴더에서 작업하고, 7단계에서 remote를 연결한다.

### 2. 남긴 글을 객체로 바꾸기

`guestbook.js`의 submit 리스너 안에서 아래 한 줄을 찾는다.

```js
  items.push(`${name}: ${message}`);
```

이 한 줄을 지우고 두 줄을 넣는다.

```js
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
```

**예상 결과** — 이름 `하늘`, 메시지 `안녕하세요`를 넣고 **[남기기]**를 누르면 목록에 `[object Object]` 한 줄이 생기고 숫자가 `1개`가 된다.
Console에는 빨간 줄이 없다. 3단계에서 고친다.

- `{ }` 안에 `이름: 값` 쌍 세 개를 쉼표로 이어 적는다. 왼쪽이 이름표, 오른쪽이 넣을 값이다.
- `name: name`의 왼쪽은 객체의 이름표, 오른쪽은 바로 위에서 만든 변수다. 글자가 같아도 다른 것이다.
- `new Date().toLocaleDateString()`은 오늘 날짜를 `2026. 9. 16.` 모양으로 만드는 **복붙 틀**이다. 안을 뜯어보지 않는다.
- `[object Object]`는 오류가 아니다. 객체를 통째로 글자 자리에 넣었다는 표시다.

### 3. 목록 한 줄을 점 표기로 고치기

`showList()` 안의 `li.textContent = items[i];` 한 줄을 아래 한 줄로 바꾼다.

```js
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
```

**예상 결과** — 목록 한 줄이 `하늘: 안녕하세요 (2026. 9. 16.)`처럼 보인다. 줄마다 붙는 **[삭제]** 버튼은 그대로다.

- `items[i]`는 `i`번째 **객체**이고, `items[i].name`은 그 객체 안의 값 하나다. 점 앞뒤에 빈칸을 넣지 않는다.
- 백틱과 `${ }`는 5주차 템플릿 문자열이다. 날짜만 괄호로 감쌌다.
- 이름표 철자를 틀리면 오류 없이 `undefined`가 보인다. 2단계에서 적은 `name`·`message`·`date`와 같게 쓴다.
- 오늘 `showList()`에서 바꾸는 줄은 이 한 줄뿐이다. 삭제 버튼 틀은 10주차 그대로 둔다.

### 4. 안내 문구를 한 줄로 합치기

세 곳을 고친다. 먼저 `guestbook.js` 위쪽의 `clearNotice()` 함수 세 줄을 지운다.

```js
function clearNotice() {
  notice.textContent = '';
}
```

다음으로 파일 맨 아래 `showList();` 위의 두 줄을 지운다.

```js
nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

마지막으로 submit 리스너 안의 아래 열한 줄을 지우고

```js
  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }
  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }
  clearNotice();
```

아래 여섯 줄을 넣는다.

```js
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
```

**예상 결과** — 이름 칸만 비우고 눌러도, 메시지 칸만 비우고 눌러도 `이름과 메시지를 모두 입력하세요.`가 보인다.
두 칸을 채우고 누르면 안내 문구가 사라지고 목록에 한 줄이 늘어난다.

- `||`는 **또는**이다. 왼쪽이 비었거나 오른쪽이 비면 안내를 보여 주고 `return`으로 멈춘다.
- 안내를 지우는 일은 제출이 성공한 자리 한 곳에서만 한다. 그래서 `clearNotice()` 함수와 `input` 두 줄이 필요 없다.
- 지우는 순서를 바꿔도 된다. 다만 `clearNotice`라는 이름이 **한 군데도 남지 않아야** 한다.
- 이 정리를 해 두어야 내일 넣을 저장 코드까지 `guestbook.js`가 60줄 안에 들어간다.

### 5. 빈 목록 안내를 개수 자리로 옮기기

먼저 `guestbook.html`에서 아래 한 줄을 지운다.

```html
      <p id="empty">아직 남긴 글이 없습니다.</p>
```

그리고 바로 아래 줄의 처음 글자를 바꾼다.

```html
      <p id="count">아직 남긴 글이 없습니다.</p>
```

1일차 `guestbook.html` 전체는 아래와 같다. 같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
    <script src="guestbook.js" defer></script>
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <h3>쓰는 순서</h3>
      <ol>
        <li>이름을 적는다.</li>
        <li>메시지를 적는다.</li>
        <li>남기기 버튼을 누른다.</li>
      </ol>
      <form id="guestbook-form">
        <p>
          <label for="name">이름</label>
          <input id="name" type="text">
        </p>
        <p>
          <label for="email">이메일</label>
          <input id="email" type="email">
        </p>
        <p>
          <label for="message">메시지</label>
          <textarea id="message" rows="4"></textarea>
        </p>
        <button type="submit">남기기</button>
      </form>
      <p id="notice"></p>
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <p id="count">아직 남긴 글이 없습니다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

이어서 `guestbook.js` 위쪽의 `const empty = document.querySelector('#empty');` 한 줄을 지운다.
그다음 `showList()` 끝의 아래 여섯 줄을 지우고

```js
  count.textContent = `${items.length}개`;
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
```

아래 다섯 줄을 넣으면 1일차 `guestbook.js`가 끝난다.

```js
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/guestbook.js](examples/day1/guestbook.js)에 있다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
let items = [];

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  showList();
  form.reset();
  nameInput.focus();
});

showList();
```

**예상 결과** — 페이지를 열면 `아직 남긴 글이 없습니다.` 한 줄만 보인다. 글을 남기면 그 자리가 `1개`로 바뀌고,
남긴 글을 모두 지우면 안내 문장이 다시 돌아온다. 안내 문장이 두 줄로 겹쳐 보이지 않는다.

- 한 자리(`#count`)가 두 가지 일을 한다. 목록이 비었으면 안내 문장, 아니면 개수다.
- 처음 화면의 글자는 HTML이 정하고, 그다음부터는 `showList()`가 정한다.
- `#empty`는 오늘부터 없다. `guestbook.js`에 `empty`라는 이름이 남아 있으면 Console에 빨간 줄이 뜬다.
- 여기까지가 1일차 목표다. Console에 빨간 줄이 없는지 확인한다.

### 6. Console에서 items 펼쳐 보기

글을 두세 개 남긴 뒤 F12 **Console**에 아래를 한 줄씩 쳐 본다.

```js
items
items[0]
items[0].name
items[0].date
```

**예상 결과** — `items`는 `▶ (2) [{…}, {…}]`처럼 보이고, 왼쪽 삼각형을 누르면 `name`·`message`·`date` 세 줄이 펼쳐진다.
`items[0].name`은 `'하늘'`, `items[0].date`는 `'2026. 9. 16.'`이다.

- 배열은 대괄호 `[ ]`, 객체는 중괄호 `{ }`로 보인다. 눈으로 구분해 둔다.
- 없는 이름표를 물으면 `undefined`가 나온다. 오류는 아니다.
- 화면의 한 줄과 `items[0]`의 세 값이 같은지 대조한다.

### 7. commit하고 push 하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "방명록 항목을 객체로 바꾸기"
git push
```

**예상 결과**

```text
[main 7b2e4d1] 방명록 항목을 객체로 바꾸기
 2 files changed, 9 insertions(+), 22 deletions(-)
```

`git push` 뒤 1분쯤 기다렸다가 `https://student01.github.io/my-web/guestbook.html`을 새로고침하면 공개 페이지에서도 날짜가 함께 보인다.
이 화면을 **확인용**으로 한 장 찍어 둔다. 제출 캡처는 2일차에 찍는다.

- 앞의 일곱 글자(`7b2e4d1`)는 PC마다 다르다.
- 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 자리를 뜬다.

## 2일차

### 8. 저장하는 함수 saveList 만들기

`guestbook.js`의 `function showList() {` **위**에 함수 하나를 만든다.

```js
function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}
```

**예상 결과** — 화면은 어제와 같다. 이 함수를 부르는 곳이 아직 없기 때문이다. Console에 빨간 줄이 없으면 된다.

- `JSON.stringify(items)`는 배열을 한 줄 문자열로 바꾼다. 저장 칸에는 **문자열만** 들어간다.
- `'guestbook'`은 저장 칸의 **키**다. 따옴표를 빼먹거나 철자를 바꾸면 다른 칸에 저장된다.
- 함수 이름은 `saveList`로 통일한다. `showList`와 한 글자 차이이므로 천천히 읽는다.

### 9. 추가한 뒤와 삭제한 뒤에 저장하기

`saveList();` 한 줄을 두 곳에 넣는다. 먼저 submit 리스너 안, `items.push({ … });` 바로 아래다.

```js
  saveList();
```

다음은 삭제 버튼 틀 안, `items.splice(i, 1);` 바로 아래다. 들여쓰기가 더 깊다.

```js
      saveList();
```

**예상 결과** — 글을 하나 남기고 F12 **Application › Storage › Local Storage**에서 지금 주소를 고르면
`guestbook` 키에 `[{"name":"하늘","message":"안녕하세요","date":"2026. 9. 16."}]`가 보인다.
다만 새로고침하면 목록은 아직 사라진다. 10단계에서 되살린다.

- 저장은 **바뀐 뒤에** 한다. `push` 다음, `splice` 다음이다.
- 저장 칸에 값이 보이는데 화면이 비어 있는 것은 지금 정상이다. 읽어 오는 줄이 아직 없다.
- 삭제 버튼 안에 넣는 `saveList();`를 빠뜨리면 지운 항목이 새로고침할 때 되살아난다.

### 10. 페이지를 열 때 되살리기

`guestbook.js` 위쪽의 `let items = [];` 한 줄을 아래 한 줄로 바꾼다.

```js
let items = JSON.parse(localStorage.getItem('guestbook')) || [];
```

**예상 결과** — 글을 세 개 남기고 **새로고침**해도 세 줄과 `3개`가 그대로 남아 있다. 브라우저를 껐다 켜도 남는다.

- `getItem('guestbook')`은 적어 둔 문자열을 꺼낸다. 적어 둔 적이 없으면 `null`이다.
- `JSON.parse(…)`가 그 문자열을 다시 배열로 되살린다.
- `|| []`는 "앞이 없으면 빈 배열로"라는 뜻이다. 이 한 줄은 **복붙 틀**이니 그대로 옮겨 쓴다.
- 파일 맨 끝의 `showList();`가 되살린 배열을 그린다. 10주차에 넣어 둔 줄이다.

### 11. 전체 지우기 버튼 붙이기

먼저 `guestbook.html`의 `<p id="count">…</p>` 줄 **아래**에 한 줄을 넣는다.

```html
      <p><button id="clear-button" type="button">전체 지우기</button></p>
```

2일차 `guestbook.html` 전체는 아래와 같다. 같은 파일이 [examples/day2/guestbook.html](examples/day2/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
    <script src="guestbook.js" defer></script>
  </head>
  <body>
    <header>
      <h1>방명록</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <h3>쓰는 순서</h3>
      <ol>
        <li>이름을 적는다.</li>
        <li>메시지를 적는다.</li>
        <li>남기기 버튼을 누른다.</li>
      </ol>
      <form id="guestbook-form">
        <p>
          <label for="name">이름</label>
          <input id="name" type="text">
        </p>
        <p>
          <label for="email">이메일</label>
          <input id="email" type="email">
        </p>
        <p>
          <label for="message">메시지</label>
          <textarea id="message" rows="4"></textarea>
        </p>
        <button type="submit">남기기</button>
      </form>
      <p id="notice"></p>
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <p id="count">아직 남긴 글이 없습니다.</p>
      <p><button id="clear-button" type="button">전체 지우기</button></p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

이어서 `guestbook.js`의 `const count = document.querySelector('#count');` 줄 아래에 한 줄을 넣는다.

```js
const clearButton = document.querySelector('#clear-button');
```

그리고 파일 맨 끝 `showList();` **위**에 다섯 줄을 넣으면 2일차 `guestbook.js`가 끝난다.

```js
clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day2/guestbook.js](examples/day2/guestbook.js)에 있다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
let items = JSON.parse(localStorage.getItem('guestbook')) || [];

function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      saveList();
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  saveList();
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});

showList();
```

**예상 결과** — 목록 아래에 **[전체 지우기]** 버튼이 보인다. 누르면 목록이 비고 `아직 남긴 글이 없습니다.`가 보이며,
새로고침해도 비어 있다. Application 탭에서 `guestbook` 키도 사라진다.

- `items = [];`는 화면 쪽 배열을 비우고, `removeItem('guestbook')`은 저장 칸을 지운다. 둘 다 해야 새로고침 뒤에도 비어 있다.
- `items`를 `let`으로 선언해 둔 이유가 여기서 드러난다. 배열을 통째로 바꾼다.
- 버튼을 HTML에 넣지 않고 JavaScript만 고치면 Console에 빨간 줄이 하나 뜬다. HTML을 먼저 고친다.

### 12. Application 탭에서 확인하고 push 하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "방명록을 브라우저에 저장하고 되살리기"
git push
```

**예상 결과**

```text
[main 9d5a37c] 방명록을 브라우저에 저장하고 되살리기
 2 files changed, 15 insertions(+), 1 deletion(-)
```

push 뒤 1분쯤 기다렸다가 아래 순서로 제출 캡처를 만든다.

1. 공개 주소 `https://student01.github.io/my-web/guestbook.html`을 연다.
2. 앞사람 글이 보이면 **[전체 지우기]**를 먼저 누른다.
3. 글 세 개를 남기고 **새로고침**한다. 세 줄과 `3개`가 그대로여야 한다.
4. F12 **Application › Storage › Local Storage**에서 내 공개 주소를 고르고 `guestbook` 키를 누른다.
5. 목록과 Application 탭이 한 화면에 보이게 캡처한다. 이 화면이 **제출 캡처**다.

- 주소창이 함께 보이게 찍는다. 실명·학번·실제 이메일이 보이지 않게 한다.
- 공개 페이지가 옛 화면이면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 공용 PC면 캡처가 끝난 뒤 **[전체 지우기]**를 한 번 더 누르고, **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지운다.

## 이번 주에 고치지 않는 파일

아래 네 파일은 10주차와 글자 하나까지 같다. 열지 않아도 되고, 조교에게 받은 폴더로 시작했거나 화면이 이상할 때만 비교한다.

`index.html` — 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web</title>
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header>
      <h1>student01의 웹 연습장</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
      <p>
        <button id="hello-button" type="button">인사 바꾸기</button>
        <button id="dark-button" type="button">다크 모드</button>
      </p>
      <p class="card" id="count">클릭 0회</p>
      <h2>소개</h2>
      <img src="images/profile.png" alt="student01의 프로필 그림" width="160">
      <p class="card">웹프로그래밍을 배우는 <strong>student01</strong>입니다.</p>
      <p class="card">이 페이지는 수업 시간에 한 주씩 늘려 갑니다.</p>
      <h2>취미</h2>
      <ul class="card">
        <li>사진 찍기</li>
        <li>보드게임</li>
        <li>저녁 산책</li>
      </ul>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`index.html`의 `id="count"`는 **클릭 횟수**를 보여 주는 자리다. 방명록의 `id="count"`와 이름이 같지만 페이지가 다르므로 서로 영향이 없다.

`about.html` — 같은 파일이 [examples/day1/about.html](examples/day1/about.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 내 정보</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>내 정보</h1>
      <nav>
        <a href="index.html">홈</a>
        <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a>
      </nav>
    </header>
    <main>
      <h2>한눈에 보기</h2>
      <p>수업용 가상 정보입니다.</p>
      <table>
        <tr>
          <th>항목</th>
          <th>내용</th>
        </tr>
        <tr>
          <td>아이디</td>
          <td>student01</td>
        </tr>
        <tr>
          <td>이메일</td>
          <td>student01@example.com</td>
        </tr>
        <tr>
          <td>관심 분야</td>
          <td>웹 페이지 만들기</td>
        </tr>
      </table>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

`app.js` — 같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다.

```js
const name = 'student01';
const hour = new Date().getHours();
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');
const darkButton = document.querySelector('#dark-button');
let count = 0;

function greet(name) {
  return `안녕하세요, ${name}님!`;
}

function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}

greeting.textContent = `${greet(name)} ${hello(hour)}`;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  countUp();
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
  countUp();
});
```

`styles.css` — 같은 파일이 [examples/day1/styles.css](examples/day1/styles.css)에 있다.

```css
body {
  background-color: #eef2ff;
  color: #17213a;
  font-family: system-ui, sans-serif;
  font-size: 16px;
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

h1 {
  color: #1f3a93;
  font-size: 28px;
}

h2 {
  color: #3157d5;
}

nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

nav a {
  color: #3157d5;
}

.card {
  background-color: #ffffff;
  padding: 16px;
  margin: 12px 0;
  border: 1px solid #c3cbe6;
}

input,
textarea {
  width: 280px;
  max-width: 100%;
}

footer {
  color: #5a6478;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 600px) {
  nav {
    flex-direction: column;
  }
}

body.dark,
body.dark .card {
  background-color: #222222;
  color: #eeeeee;
}
```

**[전체 지우기]** 버튼에는 따로 CSS 규칙을 주지 않았다. 기본 모양으로 보이는 것이 정상이다.

## 오류가 나면

먼저 F12 **Console**의 **첫 빨간 줄**을 읽는다. 줄 끝의 `guestbook.js:54`가 파일 이름과 줄 번호다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
