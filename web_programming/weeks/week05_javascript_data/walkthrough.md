# 5주차 따라하기 — 인사말을 만드는 app.js

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면이나 Console에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주 확인 도구는 **Console**이다. 브라우저에서 **F12**(또는 우클릭 › 검사)를 누르고 **Console** 탭을 연다.
1일차에는 화면이 4주차와 똑같다. 값이 Console에만 찍히기 때문이며 정상이다.

## 1일차

### 1. 저장소 받아오기

지난주에 쓰던 PC라면 폴더를 열고 새 commit만 받아 온다. 현재 폴더: `my-web`

```bash
git pull
```

**예상 결과** — 집에서 push한 것이 없으면 `Already up to date.` 한 줄이다.

처음 쓰는 PC라면 저장소를 통째로 내려받는다. 현재 폴더: 저장소를 둘 위치(문서 폴더 등)

```bash
git clone https://github.com/student01/my-web.git
cd my-web
```

**예상 결과** — `Cloning into 'my-web'...`로 시작하고 `my-web` 폴더가 생긴다. **File › Open Folder**로 그 폴더를 연다.

- `fatal: destination path 'my-web' already exists and is not an empty directory.`가 나오면 이미 받아 둔 것이다. 그 폴더를 열고 `git pull`을 한다.
- 로그인이 막혀 clone이 안 되면 조교에게 4주차 `examples/day2` 파일을 받아 새 폴더에서 작업하고, 끝 루틴에서 `git remote add origin <URL>` 뒤에 push한다.

### 2. index.html에 script 줄 되살리기

`index.html`의 `<head>`를 연다. 4주차에 되살린 `<link rel="stylesheet" href="styles.css">` **바로 아래**에 한 줄을 넣는다.

```html
    <script src="app.js" defer></script>
```

여기까지 하면 `index.html` 전체가 아래와 같다. 같은 파일이 [examples/day1/index.html](examples/day1/index.html)에 있다.

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

**예상 결과** — 화면은 4주차와 똑같다. 다만 **F12 › Console**을 열면 빨간 줄이 하나 있다.

```text
Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')      app.js:6
```

아직 지우지 않은 2주차 카운터 코드가 3주차에 사라진 버튼(`#count-button`)을 찾고 있기 때문이다.
다음 단계에서 그 코드를 통째로 지우면 없어진다. 빨간 줄을 읽는 법은 7단계에서 배운다.

- 3주차에 이 줄을 뺐다가 오늘 되살린 것이다. `link` 줄과 순서가 바뀌어도 동작은 같다.
- `defer`는 "HTML을 다 읽은 뒤에 `app.js`를 실행하라"는 뜻이다. 빼면 2일차에 오류가 난다.
- `about.html`과 `guestbook.html`에는 넣지 않는다. 이번 주에 쓰는 JavaScript는 `index.html`만의 것이다.

### 3. app.js 비우고 첫 줄 쓰기

`app.js`를 열면 2주차에 받은 카운터 코드가 들어 있다. **전체를 지우고** 아래 한 줄만 쓴다.

```js
console.log('app.js가 실행되었습니다');
```

저장하고 브라우저에서 `index.html`을 새로고침한 뒤 **F12 › Console** 탭을 본다.

**예상 결과** — Console에 `app.js가 실행되었습니다` 한 줄이 보인다. 오른쪽에 `app.js:1`이 함께 보인다.

- 아무것도 안 보이면 ① `script` 줄의 파일 이름 철자 ② `app.js`를 저장했는지 ③ 새로고침했는지를 차례로 본다.
- 2주차 코드(`() =>`·`#count-button`)는 남기지 않는다. 그 버튼은 3주차에 이미 사라졌다.

### 4. const와 let으로 값 만들기

첫 줄 아래에 값 두 개를 만들고 Console에 찍는다.

```js
const name = 'student01';
let hour = 9;

console.log(name);
console.log(hour);
```

**예상 결과** — Console에 `student01`과 `9`가 차례로 찍힌다. 숫자 `9`에는 따옴표가 없다.

- `const`는 다시 넣지 않을 값, `let`은 다시 넣을 값이다. 먼저 `const`로 쓰고 필요할 때만 `let`으로 바꾼다.
- 문자열은 따옴표 안에, 숫자는 따옴표 없이 쓴다. `'9'`와 `9`는 다른 값이다.
- 줄 끝의 세미콜론(`;`)은 한 문장이 끝났다는 표시다. 빠뜨려도 대개 동작하지만 이 수업에서는 붙여 쓴다.

### 5. 값을 다시 넣어 보기

`hour`에 다른 숫자를 넣고 다시 찍는다.

```js
hour = 15;
console.log(hour);
```

**예상 결과** — Console에 `9` 다음 줄에 `15`가 찍힌다. 같은 이름에 새 값이 들어갔다.

- 다시 넣을 때 `let`을 또 쓰지 않는다. `let hour = 15;`라고 쓰면 같은 이름을 두 번 만드는 것이다.
- `name = 'student02';`를 한 줄 넣어 저장해 보면 Console에 빨간 줄이 뜬다.

```text
Uncaught TypeError: Assignment to constant variable.
```

확인했으면 그 줄은 **지운다.** `const`에는 다시 넣지 않는다는 뜻이다.

### 6. 템플릿 문자열로 인사말 만들기

백틱(`` ` ``)으로 감싼 문장 안에 `${name}`·`${hour}`를 넣는다. 백틱은 키보드 `1` 왼쪽, `Esc` 아래 키다.

```js
const greeting = `안녕하세요, ${name}님!`;

console.log(greeting);
console.log(`지금은 ${hour}시입니다.`);
```

여기까지 하면 `app.js` 전체가 아래와 같다. 같은 파일이 [examples/day1/app.js](examples/day1/app.js)에 있다.

```js
console.log('app.js가 실행되었습니다');

const name = 'student01';
let hour = 9;

console.log(name);
console.log(hour);

hour = 15;
console.log(hour);

const greeting = `안녕하세요, ${name}님!`;

console.log(greeting);
console.log(`지금은 ${hour}시입니다.`);
```

**예상 결과** — Console에 여섯 줄이 보인다.

```text
app.js가 실행되었습니다
student01
9
15
안녕하세요, student01님!
지금은 15시입니다.
```

- `${name}`이 글자 그대로 찍히면 백틱이 아니라 작은따옴표를 쓴 것이다.
- 한글 입력 상태에서 친 백틱은 다른 글자가 된다. 영문 상태에서 친다.

### 7. 일부러 오타를 내고 빨간 줄 읽기

6행의 `console.log(name);`을 `console.log(nmae);`로 바꿔 저장하고 새로고침한다.

**예상 결과** — Console에 빨간 줄이 뜨고, 그 아래 줄들이 찍히지 않는다.

```text
Uncaught ReferenceError: nmae is not defined      app.js:6
```

- 오른쪽의 `app.js:6`이 **파일 이름과 줄 번호**다. 그 줄로 가서 고친다.
- `is not defined`는 "그런 이름이 없다"는 뜻이다. 대개 철자 오타다.
- 오류가 난 줄에서 실행이 멈추므로 **그 아래 `console.log`는 하나도 찍히지 않는다.** 몇 줄이 사라졌는지 세어 본다.
- 고쳐서 다시 여섯 줄이 모두 보이면 이 화면을 **확인용 캡처**로 저장한다.

### 8. 나머지 파일은 그대로 둔다

`about.html`·`guestbook.html`·`styles.css`는 이번 주에 **한 글자도 고치지 않는다.** 폴더에 그대로 있는지만 확인한다.

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

`guestbook.html` — 같은 파일이 [examples/day1/guestbook.html](examples/day1/guestbook.html)에 있다.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>my-web · 방명록</title>
    <link rel="stylesheet" href="styles.css">
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
      <form>
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
      <p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
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
```

**예상 결과** — 세 페이지 모양은 4주차와 같다. `about.html`·`guestbook.html`을 열면 Console이 비어 있다.

- 두 페이지에는 `script` 줄이 없어서 `app.js`가 실행되지 않는다. 방명록 동작은 7주차에 `guestbook.js`로 만든다.
- `styles.css`의 `.card`는 2일차에 인사말 문단이 쓸 class다. 지우지 않는다.

### 9. 1일차 끝 루틴

현재 폴더: `my-web`

```bash
git add .
git commit -m "app.js에 인사말 값 만들기"
git push
```

**예상 결과**

```text
[main 4e02309] app.js에 인사말 값 만들기
 2 files changed, 13 insertions(+), 8 deletions(-)
```

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침하고 **F12 › Console**을 연다. 여섯 줄이 같게 보인다.
2. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 앞의 일곱 글자(`4e02309`)는 PC마다 다르다.
- 4주차 `app.js`를 남겨 둔 학생은 위 출력 그대로다. 4주차에 `app.js`를 **지운** 학생만 숫자가 `2 files changed, 16 insertions(+)`가 되고 그 아래에 `create mode 100644 app.js` 줄이 붙는다.

## 2일차

### 10. 인사말 자리 만들기

현재 폴더: `my-web`

```bash
git pull
```

`index.html`의 `<main>` **첫 줄**에 문단 하나를 넣는다.

```html
      <p class="card" id="greeting">인사말을 준비 중입니다.</p>
```

여기까지 하면 `index.html` 전체가 아래와 같다. 1일차 파일에서 이 한 줄만 늘었다.
같은 파일이 [examples/day2/index.html](examples/day2/index.html)에 있다.

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

**예상 결과** — 새로고침하면 소개 카드 위에 `인사말을 준비 중입니다.`라는 흰 카드가 하나 더 보인다.

- `id="greeting"`은 이 문단에만 붙인다. 한 페이지에 같은 `id`를 두 번 쓰지 않는다.
- 지금 보이는 글자는 HTML에 적힌 글자다. 오늘 마지막 단계에서 `app.js`가 이 글자를 바꾼다.

### 11. 지금 시각 가져오기

`app.js`의 1일차 내용을 **전부 지우고** 두 줄부터 다시 쓴다.

```js
const name = 'student01';
const hour = new Date().getHours();

console.log(hour);
```

**예상 결과** — Console에 지금 시각이 숫자 하나로 찍힌다. 오전 10시에 열면 `10`이다.

- `new Date().getHours()`는 **오늘 복붙 틀 한 줄**이다. 뜻은 "지금 몇 시인지 0~23 숫자로 달라"는 것이며, 모양 그대로 쓴다.
- 이번에는 다시 넣지 않으므로 `hour`도 `const`로 쓴다.

### 12. if로 오전·오후 인사 고르기

시각에 따라 두 문장 중 하나를 고른다.

```js
if (hour >= 12) {
  console.log('좋은 오후입니다.');
} else {
  console.log('좋은 아침입니다.');
}
```

**예상 결과** — 12시 전에 열면 `좋은 아침입니다.`, 12시 이후면 `좋은 오후입니다.` 한 줄만 찍힌다.

- 두 갈래를 다 보려면 두 번째 줄을 잠시 `const hour = 9;`로 바꿔 본다. 확인한 뒤 틀 한 줄로 되돌린다.
- `>=`는 "크거나 같다"다. `=` 하나는 넣는 것이고, 같은지 비교할 때는 `===`를 쓴다.
- 중괄호 `{ }`의 짝이 맞지 않으면 `Uncaught SyntaxError: Unexpected end of input`이 뜬다.

### 13. 함수 두 개로 묶기

방금 만든 `if`를 함수 안으로 옮기고, 인사 문장을 만드는 함수도 하나 만든다. `console.log` 대신 `return`으로 값을 돌려준다.

```js
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

console.log(greet(name));
console.log(hello(hour));
```

**예상 결과** — Console에 `안녕하세요, student01님!`과 `좋은 아침입니다.` 두 줄이 찍힌다.

- 함수는 정의만으로는 실행되지 않는다. `greet(name)`처럼 **괄호를 붙여 호출**해야 그때 실행된다.
- `return`을 빼고 `console.log`만 두면 호출 결과가 `undefined`가 된다.
- 괄호 안의 `name`·`hour`는 함수가 받는 값의 이름이다. 호출할 때 준 값이 그 자리에 들어간다.

### 14. 문장 조립하고 화면에 띄우기

두 함수의 결과를 한 문장으로 잇고, 마지막 줄에서 화면 글자를 바꾼다. 확인이 끝난 `console.log(greet(name));`·`console.log(hello(hour));` 두 줄은 지운다.

```js
const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
```

여기까지 하면 `app.js` 전체가 아래와 같다. 같은 파일이 [examples/day2/app.js](examples/day2/app.js)에 있다.

```js
const name = 'student01';
const hour = new Date().getHours();

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

const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
```

**예상 결과** — 새로고침하면 카드 글자가 바뀐다.

```text
바뀌기 전: 인사말을 준비 중입니다.
바뀐 뒤  : 안녕하세요, student01님! 좋은 아침입니다.
Console  : 10
           안녕하세요, student01님! 좋은 아침입니다.
```

- 마지막 줄은 **복붙 틀**이다. "`#greeting`인 자리의 글자를 `message`로 바꿔라"는 뜻이며, 무엇인지는 6주차에 배운다.
- `인사말을 준비 중입니다.`가 그대로면 마지막 줄까지 가지 못한 것이다. Console의 첫 빨간 줄부터 고친다.
- `Cannot set properties of null`이 뜨면 `#greeting` 철자나 `script` 줄의 `defer`를 본다.

여기까지가 오늘 만든 코드다. 되돌리기를 연습하기 전에 지금 상태를 commit해 둔다. 현재 폴더: `my-web`

```bash
git add .
git commit -m "함수로 인사말 만들어 화면에 표시"
```

**예상 결과**

```text
[main b7a4821] 함수로 인사말 만들어 화면에 표시
 2 files changed, 17 insertions(+), 10 deletions(-)
```

- 아직 push하지 않는다. push는 16단계에서 한 번에 한다.
- 이 commit을 건너뛰고 15단계로 가면 오늘 한 작업이 통째로 되돌아간다. 10단계에서 넣은 `index.html`의 `#greeting` 문단까지 함께 되돌아가, 공개 페이지에서 인사말 카드가 통째로 사라지고 1일차 화면이 되어 제출 캡처를 만들 수 없다.

### 15. 틀린 문장을 commit하고 git revert로 되돌리기

되돌리기를 한 번 연습한다. `greet` 안의 문장을 일부러 다른 문구로 바꾸고 저장한다.

```js
  return `반갑습니다, ${name}님!!!`;
```

현재 폴더: `my-web`

```bash
git add .
git commit -m "인사말 문구 바꾸기"
git revert HEAD
```

**예상 결과** — `git commit`이 먼저 아래 두 줄을 찍는다. 14단계에서 commit해 두었으므로 이번에 바뀐 곳은 `return` 한 줄뿐이다.

```text
[main 4c11521] 인사말 문구 바꾸기
 1 file changed, 1 insertion(+), 1 deletion(-)
```

이어 `git revert HEAD`에서 편집기 창이 열린다. 기본 메시지 `Revert "인사말 문구 바꾸기"`를 그대로 두고 저장한 뒤 닫으면 터미널에 아래가 나온다.

```text
[main a519cac] Revert "인사말 문구 바꾸기"
 Date: Wed Sep 16 10:24:31 2026 +0900
 1 file changed, 1 insertion(+), 1 deletion(-)
```

```bash
git log --oneline
```

```text
a519cac Revert "인사말 문구 바꾸기"
4c11521 인사말 문구 바꾸기
b7a4821 함수로 인사말 만들어 화면에 표시
4e02309 app.js에 인사말 값 만들기
```

- `app.js`를 열어 보면 문장이 `안녕하세요, ${name}님!`로 돌아와 있다.
- 되돌린 기록도 commit으로 남는다. 그래서 함께 쓰는 저장소에서 안전하다.
- `git reset HEAD^`는 기록 자체를 지운다. **push해서 공유한 commit에는 쓰지 않는다.**
- 앞의 일곱 글자와 `Date:` 줄의 시각은 PC마다 다르다. 가운데 `Date:` 줄은 `git revert`가 늘 한 줄 붙이는 것이다.

### 16. 2일차 끝 루틴과 제출

현재 폴더: `my-web`

```bash
git push
```

1. 1분쯤 뒤 `https://student01.github.io/my-web/`을 새로고침한다.
2. **F12 › Console**을 켜 둔 채로, 카드의 인사말과 Console 두 줄이 함께 보이는 화면을 캡처한다. 이 한 장이 이번 주 제출물이다.
3. 공용 PC라면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 나간다.

- 오늘 코드는 14단계에서, 되돌리기는 15단계에서 이미 commit했다. 그래서 끝 루틴은 push만 한다. `git add .` → `git commit`을 다시 해 보면 `nothing to commit, working tree clean`이 나오는데 그것도 정상이다.
- 12시 이후에 열면 `좋은 오후입니다.`가 나온다. 둘 다 정답이다.
- 캡처에 실명·학번·실제 이메일이 보이지 않게 한다. 아이디는 보여도 된다.

## 오류가 나면

먼저 Console의 **첫 빨간 줄**을 읽는다. 오른쪽의 `app.js:6`이 고칠 자리다.
줄 번호로 가서 철자·따옴표·괄호를 차례로 본다. 자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
