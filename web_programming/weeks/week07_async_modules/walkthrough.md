# 7주차 따라하기 — 폼을 제출하면 화면에 한 줄 남기기

처음에는 그대로 따라 하고, 결과가 나오면 본인 아이디와 문구로 바꾼다.
각 단계의 예상 결과가 화면에 보이면 다음 단계로 넘어간다.

`student01`은 연습용 아이디다. 명령과 주소에 있는 `student01`은 본인 GitHub 아이디로 바꾼다.
명령은 VS Code의 터미널(**Terminal › New Terminal**, Windows는 PowerShell)에서 실행한다. macOS 터미널도 같은 명령이다.
명령 앞에 **현재 폴더**를 적어 두었다. 다른 폴더에서 실행하면 결과가 다르다.

이번 주에 고치는 파일은 `guestbook.html`·`guestbook.js` 둘, 그리고 2일차에 GitHub 웹에서 만드는 `README.md` 하나다.
`index.html`·`about.html`·`app.js`·`styles.css`는 6주차 그대로 둔다. 전체 내용은 [이번 주에 고치지 않는 파일](#이번-주에-고치지-않는-파일)에 있다.

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

- 6주차 작업이 main에 merge되어 있어야 한다. `git branch`에 `* main`만 있으면 된다.
- clone이 로그인 문제로 막히면 조교에게 6주차 `examples/day2` 폴더를 받아 그 폴더에서 작업하고, 10단계에서 remote를 연결한다.

### 2. guestbook.html에 결과 자리 만들기

`guestbook.html`을 열고 세 곳을 고친다. 3주차에 만든 폼은 그대로 두고 **자리만** 만드는 단계다.

1. `<head>` 안 `<link>` 줄 **아래**에 `<script src="guestbook.js" defer></script>`를 넣는다.
2. `<form>`을 `<form id="guestbook-form">`으로 바꾼다.
3. `</form>` 아래의 `<p>지금은 눌러도 주소창만 바뀐다. 화면에 띄우는 일은 7주에 한다.</p>` 한 줄을 지우고, 그 자리에 세 줄을 넣는다.

```html
      <p id="notice"></p>
      <h3>마지막으로 남긴 글</h3>
      <p class="card" id="last">아직 남긴 글이 없습니다.</p>
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
      <h3>마지막으로 남긴 글</h3>
      <p class="card" id="last">아직 남긴 글이 없습니다.</p>
    </main>
    <footer>
      <p>수업용 연습 페이지 · student01</p>
    </footer>
  </body>
</html>
```

**예상 결과** — 폴더에서 `guestbook.html`을 더블클릭해 열면 폼 아래에 **마지막으로 남긴 글**과 `아직 남긴 글이 없습니다.` 카드가 보인다.
아직 **[남기기]**를 누르면 화면이 처음으로 돌아가고 주소 끝에 `?`가 붙는다. F12 **Console**에 빨간 줄이 하나 보이는 것도 정상이다. `guestbook.js`를 아직 만들지 않았기 때문이다.

- `id`는 `guestbook-form`·`notice`·`last` 세 개다. `name`·`email`·`message`는 3주차에 붙여 둔 것을 그대로 쓴다.
- `<p id="notice"></p>`는 **비어 있는 문단**이다. 안내할 일이 있을 때만 글자가 들어간다.
- `index.html`은 `app.js`를, `guestbook.html`은 `guestbook.js`를 부른다. **페이지마다 자기 js 하나**다.

### 3. guestbook.js 만들고 요소 찾아 두기

VS Code 탐색기의 **New File**로 `my-web` 폴더에 `guestbook.js`를 새로 만들고 다섯 줄을 쓴다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');
```

**예상 결과** — `guestbook.html`을 새로고침하면 Console의 빨간 줄이 사라진다. 화면은 아직 그대로다.

- 6주차 `app.js` 맨 위와 같은 모양이다. 찾아 둔 것을 `const`에 담아 두고 아래에서 이름으로 쓴다.
- `이메일` 칸은 이번 주에 읽지 않는다. 그래서 찾아 두지 않는다.
- Console에 `form`을 쳐 보면 `<form id="guestbook-form">…</form>`이 보인다. `null`이면 철자가 틀린 것이다.

### 4. 제출을 받아 새로고침 막기

`guestbook.js` 아래에 빈 줄 하나를 두고 이어 쓴다.

```js
form.addEventListener('submit', function (event) {
  event.preventDefault();
});
```

**예상 결과** — 새로고침한 뒤 이름·메시지를 아무렇게나 넣고 **[남기기]**를 누르면 이제 **아무 일도 일어나지 않는다.**
화면이 처음으로 돌아가지 않고 주소 끝에 `?`도 붙지 않는다. 입력한 글자도 그대로 남아 있다.

- 6주차 `'click'` 자리에 `'submit'`이 들어갔다. 맡겨 두는 방법은 같다.
- 괄호 안의 `event`는 **방금 일어난 일**이 담겨 오는 이름이다. `event.preventDefault()`는 "브라우저가 원래 하려던 일을 하지 마라"는 뜻이다.
- `event`를 빠뜨리고 `preventDefault()`라고만 쓰면 `Uncaught ReferenceError: preventDefault is not defined`가 뜬다.

### 5. 입력 칸의 값 읽기

`event.preventDefault();` 아래에 빈 줄을 두고 세 줄을 더한다. 마지막 `console.log`는 값을 확인하는 줄이며 6단계에서 지운다.

```js
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  console.log(name, message);
```

**예상 결과** — 이름에 `student01`, 메시지에 `안녕하세요`를 넣고 누르면 Console에 `student01 안녕하세요`가 찍힌다.
이름 칸에 공백만 넣고 누르면 Console에 빈 값이 찍힌다.

- `.value`는 입력 칸에 **지금 적혀 있는 글자**다. `textarea`도 같다.
- `.trim()`은 앞뒤 공백을 떼어 낸 값을 돌려준다. 공백만 친 칸을 빈칸으로 보기 위해서다.
- `const name`은 리스너 **안**에 둔다. 누를 때마다 그때의 값을 새로 읽어야 하기 때문이다.

### 6. 마지막 글 한 줄로 표시하기

`console.log(name, message);` 줄을 지우고 그 자리에 한 줄을 쓴다.

```js
  last.textContent = `${name}: ${message}`;
```

**예상 결과** — 이름 `student01`, 메시지 `안녕하세요`를 넣고 누르면 카드가 `student01: 안녕하세요`로 바뀐다.
입력 칸의 글자는 아직 그대로 남아 있다.

- 6주차의 `textContent`와 같다. 바뀌는 것은 화면이지 HTML 파일이 아니다. 새로고침하면 `아직 남긴 글이 없습니다.`로 돌아간다.
- 이름과 메시지 사이는 **콜론과 공백**(`: `)이다. 5주차 템플릿 문자열 안에 그대로 적는다.

### 7. 이름이 비면 안내하고 커서 옮기기

`const message = …` 줄 아래, `last.textContent = …` 줄 **위**에 다섯 줄과 한 줄을 넣는다.

```js
  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  notice.textContent = '';
```

**예상 결과** — 이름을 비우고 누르면 폼 아래에 `이름을 입력하세요.`가 나타나고 커서가 이름 칸으로 간다.
카드는 `아직 남긴 글이 없습니다.` 그대로다. 이름을 채워 누르면 안내 문구가 사라지고 카드에 글이 보인다.

- `return`은 "여기서 이 함수를 끝내라"는 뜻이다. `return`이 없으면 안내를 띄운 **뒤에도** 아랫줄이 실행되어 `: 안녕하세요`가 표시된다.
- `=== ''`는 "값이 빈 글자와 같은가"다. 5주차의 `===`와 같다.
- `notice.textContent = '';`는 지난번 안내 문구를 지우는 줄이다. 이 줄이 없으면 안내가 계속 남는다.

### 8. 폼 비우고 다음 입력 준비하기

`last.textContent = …` 줄 아래에 두 줄을 더하면 1일차 `guestbook.js`가 끝난다.

```js
  form.reset();
  nameInput.focus();
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day1/guestbook.js](examples/day1/guestbook.js)에 있다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  notice.textContent = '';
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
});
```

**예상 결과** — 이름 `student01`, 메시지 `안녕하세요`를 넣고 누르면 카드에 `student01: 안녕하세요`가 보이고,
**입력 칸 세 개가 모두 비워지며** 커서가 이름 칸에 있다. 그대로 다음 글을 바로 칠 수 있다.

- `form.reset()`은 폼 전체를 비운다. 이메일 칸도 함께 비워진다.
- 순서가 중요하다. `form.reset()`을 **먼저** 하면 값이 지워지므로, 값을 읽어 표시한 **뒤에** 비운다.
- Console에 빨간 줄이 없는지 확인한다. 여기까지가 1일차 목표다.

### 9. 8주차 리허설 starter 열어 보기

8주차 중간 실기의 리허설 파일을 오늘 받아 둔다. [../week08_midterm/examples/rehearsal_starter](../week08_midterm/examples/rehearsal_starter)의 세 파일을
새 폴더 `midterm-practice`에 넣고 `index.html`을 더블클릭해 연다.

**예상 결과** — 기본 색과 글꼴만 적용된 페이지가 열리고 Console에 `리허설 starter 준비 완료`가 보인다. 버튼을 눌러도 아직 아무 일도 일어나지 않는다.
카드 박스와 nav 가로 배치는 아직 비어 있다(8주차 문제 2에서 채운다).

- 이 폴더는 `my-web` **밖**에 둔다. 저장소에 넣지 않는다.
- 오늘은 열어 보기만 한다. 푸는 것은 2일차 15단계와 8주차 1일차다.
- [채점표](../week08_midterm/rubric.md)의 `폼 입력·빈값 안내 3` 줄이 오늘 만든 것이다.

### 10. 오늘 작업 commit하고 push 하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "방명록 폼 제출 받기"
git push
```

**예상 결과**

```text
[main a69bc37] 방명록 폼 제출 받기
 2 files changed, 28 insertions(+), 2 deletions(-)
 create mode 100644 guestbook.js
```

`git push` 뒤 1분쯤 기다렸다가 `https://student01.github.io/my-web/guestbook.html`을 새로고침하면 공개 페이지에서도 같은 동작이 된다.
이 화면을 **확인용**으로 한 장 찍어 둔다. 제출 캡처는 2일차에 찍는다.

- 앞의 일곱 글자(`a69bc37`)는 PC마다 다르다.
- 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지우고 자리를 뜬다.

## 2일차

### 11. GitHub 웹에서 README 만들고 받아오기

저장소를 설명하는 `README.md`를 **GitHub 화면에서** 만들고 내 PC로 받아 온다.

1. `https://github.com/student01/my-web`을 연다.
2. **Add file › Create new file**을 누른다.
3. 파일 이름에 `README.md`를 적는다.
4. 아래 내용을 넣는다. 공개 주소의 아이디는 본인 것으로 바꾼다.
5. 오른쪽 위 **Commit changes…** → **Commit changes**를 누른다.

```markdown
# my-web

웹프로그래밍 수업에서 한 주씩 늘려 가는 연습 사이트입니다.

- 공개 주소: https://student01.github.io/my-web/
- 페이지: `index.html`(홈) · `about.html`(내 정보) · `guestbook.html`(방명록)

이 파일은 GitHub 웹에서 만들고 `git pull`로 내 컴퓨터에 받았습니다.
```

현재 폴더: `my-web`

```bash
git pull
```

**예상 결과** — 저장소 첫 화면 아래쪽에 README 내용이 보인다. `git pull` 출력은 아래와 같고 VS Code 탐색기에 `README.md`가 나타난다.

```text
Updating a69bc37..3d51f0c
Fast-forward
 README.md | 8 ++++++++
 1 file changed, 8 insertions(+)
 create mode 100644 README.md
```

- GitHub 화면에서 만든 파일은 **GitHub에만** 있다. `git pull`을 해야 내 PC에 생긴다.
- pull을 건너뛰고 작업하면 나중에 push가 거부된다. 2주차 부록에서 본 `clone`·`pull`의 복습이다.
- README는 9주차 1차 과제에서 레포트로 쓴다. 오늘은 다섯 줄이면 된다.

### 12. 메시지 칸도 검사하기

`guestbook.js`의 이름 검사 블록 **아래**, `notice.textContent = '';` 줄 **위**에 다섯 줄과 빈 줄을 넣는다.

```js
  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }
```

**예상 결과** — 이름만 넣고 누르면 `메시지를 입력하세요.`가 보이고 커서가 메시지 칸으로 간다. 카드는 바뀌지 않는다.
이름을 비우고 누르면 어제처럼 `이름을 입력하세요.`가 먼저 나온다.

- 두 검사는 **위에서부터 차례로** 본다. 이름이 비면 거기서 `return`으로 끝나므로 메시지 검사까지 가지 않는다.
- 안내 문구는 각각 다르게 쓴다. 학생이 어느 칸을 고쳐야 하는지 문구만 보고 알 수 있어야 한다.

### 13. 다시 입력하면 안내 문구 지우기

안내 문구를 지우는 일이 두 곳에서 필요해졌다. 그 한 줄을 함수로 묶고 입력 칸에 맡긴다.

1. `const last = …` 줄 아래에 함수를 만든다.

```js
function clearNotice() {
  notice.textContent = '';
}
```

2. 리스너 안의 `notice.textContent = '';` 줄을 `clearNotice();`로 바꾼다.
3. 파일 **맨 끝**에 두 줄을 더한다.

```js
nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

전체 파일은 아래와 같다. 같은 파일이 [examples/day2/guestbook.js](examples/day2/guestbook.js)에 있다.

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');

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
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
```

**예상 결과** — 이름을 비우고 눌러 `이름을 입력하세요.`가 뜬 뒤, 이름 칸에 **글자를 한 자만 쳐도** 안내 문구가 사라진다.
메시지 칸도 같다. 제출은 어제와 똑같이 된다.

- `'input'`은 입력 칸의 글자가 바뀔 때마다 일어난다. 6주차에 배운 `addEventListener`에서 **이벤트 이름만** 바뀌었다.
- 맡길 때는 `clearNotice`에 괄호를 붙이지 않는다. `clearNotice()`라고 쓰면 맡기는 순간 한 번 실행되고 만다.
- 6주차 `countUp()`처럼 같은 일을 여러 곳에서 쓰면 함수로 묶는다.

### 14. 두 번째 글을 남겨 보기

글을 하나 남긴 뒤 다른 이름·메시지로 한 번 더 남긴다.

**예상 결과** — 카드에는 **마지막 글 하나만** 보인다. 앞에 남긴 글은 사라진다.

- 카드가 한 줄뿐이라 그렇다. 글을 쌓아 목록으로 보여 주는 것은 10주차, 새로고침해도 남게 하는 것은 11주차다.
- 지금 단계에서 정상 동작이므로 고치지 않는다.

### 15. 리허설 문항 하나 풀어 보기

9단계에서 받아 둔 `midterm-practice` 폴더의 `app.js`를 열고 **문제 4-1·4-2** 주석 자리만 채운다.
오늘 만든 `guestbook.js`와 같은 모양이며, 이름만 `joinForm`·`nameInput`·`reasonInput`·`result`로 다르다.

**예상 결과** — 이름과 신청 이유를 넣고 **신청하기**를 누르면 `#result`에 `student01: 사진을 배우고 싶습니다`가 보이고,
이름을 비우고 누르면 `이름을 입력하세요`가 보이며 커서가 이름 칸으로 간다.

- 막히면 오늘 만든 `guestbook.js`를 옆에 두고 이름만 바꿔 읽는다.
- [해답](../week08_midterm/examples/rehearsal_solution)은 다 푼 뒤에 연다.
- 이 폴더는 채점하지 않는다. 8주차 1일차에 나머지 세 문제와 함께 다시 푼다.

### 16. push 하고 공개 페이지 캡처하기

현재 폴더: `my-web`

```bash
git add .
git commit -m "빈값 안내 다듬기"
git push
```

**예상 결과** — push 뒤 1분쯤 기다렸다가 `https://student01.github.io/my-web/guestbook.html`을 새로고침한다.
이름 `student01`, 메시지 `안녕하세요`를 넣고 **[남기기]**를 누르면 카드에 `student01: 안녕하세요`가 보인다. 이 화면이 **제출 캡처**다.

- 주소창이 함께 보이게 찍는다. 실명·학번·실제 이메일이 보이지 않게 한다.
- 공개 페이지가 옛 화면이면 1분 더 기다렸다가 **Ctrl+F5**(macOS는 ⌘+Shift+R)로 새로고침한다.
- 공용 PC면 **자격 증명 관리자 › Windows 자격 증명**에서 `git:https://github.com`을 지운다.

## 이번 주에 고치지 않는 파일

아래 네 파일은 6주차와 글자 하나까지 같다. 열지 않아도 되고, 조교에게 받은 폴더로 시작했거나 화면이 이상할 때만 비교한다.

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

`#notice`에는 따로 CSS 규칙을 주지 않았다. 기본 글자 그대로 보이는 것이 정상이다.

## 오류가 나면

먼저 F12 **Console**의 **첫 빨간 줄**을 읽는다. 줄 끝의 `guestbook.js:7`이 파일 이름과 줄 번호다.
자주 나오는 메시지와 확인할 것은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 새로고침하고, 해결되지 않으면 Console 화면을 그대로 보여 주고 도움을 요청한다.
