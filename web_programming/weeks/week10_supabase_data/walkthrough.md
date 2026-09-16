# 10주차 따라하기 — 남긴 글을 목록으로 쌓고 지우기

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주에 고치는 파일은 `guestbook.html`과 `guestbook.js` 둘뿐이다.
`index.html`·`about.html`·`app.js`·`styles.css`·`README.md`는 9주차 그대로 둔다. 전체 내용은 [이번 주에 고치지 않는 파일](#이번-주에-고치지-않는-파일)에 있다.
예제 파일은 빈 줄 없이 이어 두었다. 내 파일에 빈 줄이 더 있어도 동작은 같다.

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

- 9주차에 만든 `readme` 브랜치는 이미 지웠다. `git branch`에 `* main`만 있으면 된다.
- 이번 주에는 브랜치를 만들지 않고 `main`에서 바로 작업한다.
- clone이 로그인 문제로 막히면 조교에게 9주차 `examples/day2` 폴더를 받아 그 폴더에서 작업하고, 8단계에서 remote를 연결한다.

### 2. 목록 자리 만들기

`guestbook.html`을 열고 `</form>` 아래 `<p id="notice"></p>` **다음** 두 줄을 찾는다.

```html
      <h3>마지막으로 남긴 글</h3>
      <p class="card" id="last">아직 남긴 글이 없습니다.</p>
```

이 두 줄을 지우고 아래 세 줄을 넣는다.

```html
      <h3>남긴 글</h3>
      <ul class="card" id="list"></ul>
      <p id="count">0개</p>
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다.

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
      <p id="count">0개</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 폴더에서 `guestbook.html`을 더블클릭해 열면 **남긴 글** 제목 아래에 빈 카드와 `0개`가 보인다.
아직 **[남기기]**를 누르면 Console에 빨간 줄이 하나 보인다. `guestbook.js`가 `#last`를 찾지 못하기 때문이며 3단계에서 고친다.

- `<ul>` 안은 **비워 둔다.** 목록 줄은 JavaScript가 만들어 넣는다.
- `id`는 `list`와 `count` 둘이다. `guestbook-form`·`name`·`email`·`message`·`notice`는 그대로 쓴다.
- `<p id="count">0개</p>`의 `0개`는 처음 화면에 보일 글자다. 글을 남기면 JavaScript가 바꾼다.

### 3. 배열과 목록 상자 찾아 두기

`guestbook.js`의 맨 위에서 `const last = document.querySelector('#last');` 한 줄을 지우고 세 줄을 넣는다.

```js
const list = document.querySelector('#list');
const count = document.querySelector('#count');
let items = [];
```

**예상 결과** — 새로고침하면 Console의 빨간 줄이 사라진다. 화면은 아직 그대로다.

- `items`는 남긴 글을 담아 둘 **배열**이다. 값이 늘었다 줄었다 하므로 `const`가 아니라 `let`으로 선언한다.
- `list`는 `<ul>`, `count`는 `<p>`다. 7주차에 `#last`를 찾아 두었던 자리에 두 개가 들어온 것이다.
- Console에 `items`를 쳐 보면 `[]`가 보인다. 아직 비어 있다.

### 4. 제출한 글을 배열에 쌓기

리스너 안에서 `clearNotice();` 아래의 `last.textContent = \`${name}: ${message}\`;` 한 줄을 지우고 두 줄을 넣는다.

```js
  const text = `${name}: ${message}`;
  items.push(text);
```

**예상 결과** — 이름 `student01`, 메시지 `안녕하세요`를 넣고 **[남기기]**를 누르면 화면은 그대로지만 폼이 비워진다.
Console에 `items`를 쳐 보면 `['student01: 안녕하세요']`가 보이고, 한 번 더 남기면 값이 두 개가 된다.

- 같은 문장을 배열과 화면 두 곳에 넣으므로 `const text`로 **한 번만** 만들어 둔다.
- `push`는 배열 **뒤에** 하나를 더한다. 쌓이는 자리는 늘 맨 뒤다.
- 아직 화면에는 아무것도 붙이지 않았다. 5단계에서 붙인다.

### 5. 목록에 한 줄 만들어 붙이기

`items.push(text);` 아래에 세 줄을 더한다.

```js
  const li = document.createElement('li');
  li.textContent = text;
  list.append(li);
```

**예상 결과** — 이름과 메시지를 넣고 누를 때마다 목록에 `student01: 안녕하세요`가 한 줄씩 **쌓인다.**
세 번 남기면 세 줄이 보이고 앞 글이 사라지지 않는다.

- `createElement('li')`는 아직 화면에 없는 새 `<li>`를 만든다. `textContent`로 글자를 넣고 `append`로 `<ul>` 안에 붙인다.
- 세 줄이 한 묶음이다. 순서를 바꾸지 않는다.
- 새로고침하면 목록이 사라진다. 지금 글은 화면에만 있다. 남게 하는 것은 11주차다.

### 6. 항목 수 보여 주기

`list.append(li);` 아래에 한 줄을 더하면 1일차 `guestbook.js`가 끝난다.

```js
  count.textContent = `${items.length}개`;
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

function clearNotice() {
  notice.textContent = '';
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
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
  const text = `${name}: ${message}`;
  items.push(text);
  const li = document.createElement('li');
  li.textContent = text;
  list.append(li);
  count.textContent = `${items.length}개`;
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

**예상 결과** — 글을 남길 때마다 목록 아래 숫자가 `1개`, `2개`, `3개`로 오른다.

- 화면의 줄을 세지 않고 **배열의 개수**(`items.length`)를 그대로 보여 준다.
- `${items.length}개`는 5주차 템플릿 문자열이다. 백틱 안에 `${ }`로 값을 끼워 넣는다.
- Console에 빨간 줄이 없는지 확인한다. 여기까지가 1일차 목표다.

### 7. 빈 이름으로 눌러 보기

이름 칸을 비우고 **[남기기]**를 눌러 본다. 7주차에 만든 빈값 안내가 그대로 동작하는지 보는 단계다.

**예상 결과** — `이름을 입력하세요.`가 보이고 커서가 이름 칸으로 간다. 목록에는 아무것도 늘지 않고 숫자도 그대로다.
메시지 칸만 비우고 누르면 `메시지를 입력하세요.`가 보인다.

- 빈값일 때 `return`으로 멈추므로 `items.push`까지 가지 않는다. 7주차에 만든 순서 그대로다.
- Console에 `items`를 쳐 안내만 뜬 제출이 배열에 들어가지 않았는지 확인한다.
- 이름 칸에 **공백만** 넣고 눌러도 안내가 떠야 한다. 뜨지 않으면 `.trim()`이 빠진 것이다.

### 8. commit하고 push 하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "방명록 글을 목록으로 쌓기"
git push
```

**예상 결과**

```text
[main 4c1f0a2] 방명록 글을 목록으로 쌓기
 2 files changed, 12 insertions(+), 4 deletions(-)
```

`git push` 뒤 1분쯤 기다렸다가 `https://student01.github.io/my-web/guestbook.html`을 새로고침하면 공개 페이지에서도 글이 쌓인다.
이 화면을 **확인용**으로 한 장 찍어 둔다. 제출 캡처는 2일차에 찍는다.

- 앞의 일곱 글자(`4c1f0a2`)는 PC마다 다르다.
- 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 자리를 뜬다.

## 2일차

### 9. 다시 그리는 함수 showList 만들기

`guestbook.js`의 `clearNotice()` 함수 **아래**에 새 함수를 만든다. 아직 리스너는 고치지 않는다.

```js
function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
  }
  count.textContent = `${items.length}개`;
}
```

**예상 결과** — 아직 화면은 어제와 같다. 이 함수를 부르는 곳이 없기 때문이다. Console에 빨간 줄이 없으면 된다.

- `list.innerHTML = ''`는 목록을 **비운다.** 이 수업에서 `innerHTML`은 비우기에만 쓴다.
- `for (let i = 0; i < items.length; i++)`는 `i`를 0부터 하나씩 올리며 배열을 끝까지 훑는다. **몇 번째인지(`i`)가 필요해서** 이 모양을 쓴다.
- 안의 세 줄은 어제 submit에서 쓴 것과 같고, 글자만 `text` 대신 `items[i]`에서 가져온다.

### 10. submit 안을 두 줄로 줄이기

리스너 안 `clearNotice();` 아래의 다섯 줄(`const text`부터 `count.textContent`까지)을 지우고 두 줄을 넣는다.

```js
  items.push(`${name}: ${message}`);
  showList();
```

**예상 결과** — 어제와 똑같이 동작한다. 글을 남기면 목록에 한 줄이 늘고 숫자가 오른다.
달라진 것은 **화면을 만드는 곳이 한 군데로 모였다**는 점이다.

- 배열에 넣은 뒤 `showList()`를 부르면 화면은 배열대로 다시 그려진다.
- `const text`는 이제 필요 없다. 문장을 바로 `push` 안에 넣는다.
- Console에 `items`를 쳐 배열과 화면의 줄 수가 같은지 확인한다.

### 11. 삭제 버튼 붙이기

`showList()` 안 `li.textContent = items[i];` 줄과 `list.append(li);` 줄 **사이**에 아래 일곱 줄을 그대로 옮겨 쓴다.

```js
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
```

**예상 결과** — 목록의 줄마다 **[삭제]** 버튼이 생긴다. 글 세 개를 남기고 **가운데** 줄의 **[삭제]**를 누르면
그 줄만 사라지고 위아래 두 줄이 남으며 숫자가 `2개`가 된다.

- `splice(i, 1)`은 배열에서 `i`번째 값 **하나**를 뺀다. 뺀 뒤 `showList()`를 부르면 화면이 새 배열대로 다시 그려진다.
- `showList()`가 다시 그릴 때 **버튼마다 번호를 새로 붙인다.**
- 이 일곱 줄은 그대로 옮겨 쓰는 **틀**이다. 안을 뜯어보지 않는다.
- `li.append(removeButton)`은 버튼을 그 줄 안에 붙이고, `list.append(li)`는 그 줄을 목록에 붙인다. 두 줄의 상자가 다르다.

### 12. 빈 목록 안내 넣기

먼저 `guestbook.html`의 `<ul class="card" id="list"></ul>` 줄 **아래**에 한 줄을 넣는다.

```html
      <p id="empty">아직 남긴 글이 없습니다.</p>
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day2/guestbook.html](examples/day2/guestbook.html)에 있다.

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
      <p id="empty">아직 남긴 글이 없습니다.</p>
      <p id="count">0개</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

이어서 `guestbook.js` 맨 위 `const count = …` 줄 **위**에 한 줄을 넣는다.

```js
const empty = document.querySelector('#empty');
```

그리고 `showList()`의 `count.textContent = \`${items.length}개\`;` 줄 아래에 다섯 줄을 더한다.

```js
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
```

**예상 결과** — 글을 하나 남기면 `아직 남긴 글이 없습니다.` 문장이 사라지고, 남긴 글을 모두 지우면 다시 나타난다.
다만 페이지를 처음 열었을 때는 아직 문장이 **그대로 보인다.** 13단계에서 마무리한다.

- 안내 문장은 HTML에 한 번, `showList()` 안에 한 번, 모두 두 곳에 적는다. 처음 화면은 HTML이 만들고 그다음부터는 함수가 정한다.
- `items.length === 0`은 "배열이 비었는가"다. 5주차의 `===`와 같다.
- `empty.textContent = '';`는 문장을 지우는 줄이다. 요소를 없애는 것이 아니라 글자만 비운다.

### 13. 페이지를 열 때 한 번 그리기

파일 **맨 끝**에 한 줄을 더하면 2일차 `guestbook.js`가 끝난다.

```js
showList();
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day2/guestbook.js](examples/day2/guestbook.js)에 있다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const empty = document.querySelector('#empty');
const count = document.querySelector('#count');
let items = [];

function clearNotice() {
  notice.textContent = '';
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  count.textContent = `${items.length}개`;
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
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
  items.push(`${name}: ${message}`);
  showList();
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
showList();
```

**예상 결과** — 페이지를 열면 빈 목록과 `아직 남긴 글이 없습니다.`, `0개`가 보인다.
글 세 개를 남기면 세 줄과 `3개`, 가운데 줄의 **[삭제]**를 누르면 두 줄과 `2개`가 된다.

- 맨 끝의 `showList();`는 페이지를 열 때 **한 번** 그리는 줄이다. 배열이 비어 있으니 빈 목록과 안내 문장이 그려진다.
- 이 줄은 리스너 밖, 파일 맨 아래에 둔다. 함수 정의보다 위에 두어도 동작하지만 읽기 쉽게 맨 끝에 둔다.
- Console에 빨간 줄이 없는지 마지막으로 확인한다.

### 14. push 하고 공개 페이지 캡처하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "목록 다시 그리기와 삭제 버튼"
git push
```

**예상 결과** — push 뒤 1분쯤 기다렸다가 `https://student01.github.io/my-web/guestbook.html`을 새로고침한다.
글 세 개를 남기고 가운데 줄의 **[삭제]**를 누르면 두 줄과 `2개`가 보인다. 이 화면이 **제출 캡처**다.

- 주소창이 함께 보이게 찍는다. 실명·학번·실제 이메일이 보이지 않게 한다.
- 공개 페이지가 옛 화면이면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지운다.

## 이번 주에 고치지 않는 파일

아래 네 파일은 9주차와 글자 하나까지 같다. 열지 않아도 되고, 조교에게 받은 폴더로 시작했거나 화면이 이상할 때만 비교한다.

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

`<li>`와 **[삭제]** 버튼에는 따로 CSS 규칙을 주지 않았다. 목록이 카드 안에 들어가고 버튼은 기본 모양으로 보이는 것이 정상이다.

## 오류가 나면

먼저 F12 **Console**의 **첫 빨간 줄**을 읽는다. 줄 끝의 `guestbook.js:31`이 파일 이름과 줄 번호다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
