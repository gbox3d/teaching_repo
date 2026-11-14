# 13주차 따라하기 · REST API로 방명록 저장하기

## 목차

- [1. 작업 폴더 준비](#1-작업-폴더-준비)
- [2. API 설정](#2-api-설정)
- [3. 비교 예제 실행](#3-비교-예제-실행)
- [4. 만들기 파일 작성](#4-만들기-파일-작성)
- [5. 실행과 확인](#5-실행과-확인)
- [6. 저장소에 올리기](#6-저장소에-올리기)

## 1. 작업 폴더 준비

새 `web-week13` 폴더를 VS Code에서 연다. 지난주 완성본은 [여기](../week12_fetch_json/examples/day2/web-week12/)에서 확인한다.
`index.html`·`about.html`·`app.js`·`styles.css`·`images/profile.png`를 이어 쓴다.
[server.mjs](../../tools/static-server/server.mjs)를 작업 폴더에 추가한다.

예상 결과: 홈·내 정보·방명록으로 이동하는 세 페이지가 준비된다.

## 2. API 설정

강의자가 배부한 API URL·공개 키·방명록 번호를 `config.example.js`에 적는다.
이 파일은 예제 이름 그대로 사용한다. 공개 값만 있으며 서버 비밀 키·학생별 편집 키를 넣지 않는다.

로컬 연습에서는 [API 안내](../../tools/guestbook-api/README.md)에 따라 별도 터미널에서 API를 먼저 실행한다.
현재 폴더: 교재 저장소 최상위.

```powershell
node web_programming/tools/guestbook-api/server.mjs
```

학생 페이지의 정적 서버는 다른 터미널에서 실행한다. 현재 폴더: `web-week13`.

```powershell
node server.mjs
```

예상 결과: API는 `http://127.0.0.1:8787`, 학생 페이지는 `http://localhost:8000`으로 열린다.
기본 API 값은 로컬 연습용이다. 공용 클라우드 API는 강의자가 별도로 만들고 주소를 안내해야 한다.

## 3. 비교 예제 실행

`examples/day1/ex01/`부터 각 예제 폴더의 파일 전체를 작업 폴더 `ex/ex01/`처럼 복사한다.
각 폴더의 `config.example.js`도 같은 안내값으로 바꾼다. `ex01`에는 설정 파일이 없다.
브라우저에서 `http://localhost:8000/ex/ex01/`을 연다. 나머지도 마지막 폴더 번호만 바꾼다.
파일을 더블클릭하는 `file://` 실행은 사용하지 않는다.

F12에서 Network를 열고 페이지를 새로고침한다. Fetch/XHR로 요청을 좁히고 요청 한 줄의 Headers·Payload·Response를 확인한다.
GET에는 JSON 요청 본문이 없으며 POST의 본문은 Payload에서 확인한다.

## 4. 만들기 파일 작성

guestbook.html에 폼을 추가하고 submit.js를 새로 연결한다. guestbook.js는 12주와 같다.
스크립트는 설정 → 목록 → 폼 순서로 연결한다. `defer`가 있으므로 HTML을 읽은 뒤 순서대로 실행한다.
아래 코드는 이번 주 완성 예제와 같다.

### config.example.js

```js
// 강의자가 안내한 공용 API 주소·공개 키·방명록 번호로 바꾼다.
// 아래 값은 내 PC의 로컬 연습 서버용이다. 편집 키는 여기에 넣지 않는다.
const API_BASE_URL = 'http://127.0.0.1:8787';
const API_PUBLIC_KEY = 'classroom-local';
const BOOK_ID = 'student01';
```

### guestbook.html

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>온라인 방명록</title>
    <link rel="stylesheet" href="styles.css">
    <script src="config.example.js" defer></script>
    <script src="guestbook.js" defer></script>
    <script src="submit.js" defer></script>
  </head>
  <body>
    <header>
      <h1>온라인 방명록</h1>
      <nav><a href="index.html">홈</a> <a href="about.html">내 정보</a>
        <a href="guestbook.html">방명록</a></nav>
    </header>
    <main>
      <h2>한 줄 남기기</h2>
      <form id="guestbook-form">
        <p><label for="name">이름(별칭)</label>
          <input id="name" maxlength="30" required></p>
        <p><label for="message">메시지</label>
          <textarea id="message" rows="3" maxlength="500" required></textarea></p>
        <button id="submit-button" type="submit">남기기</button>
      </form>
      <div id="notice" role="status"></div>
      <h2>남긴 글</h2>
      <button id="reload-button" type="button">새로 불러오기</button>
      <div id="load-notice" role="status"></div>
      <ul class="card" id="list"></ul>
      <div id="count">최근 글 0개</div>
    </main>
    <footer><p>수업용 연습 페이지 · 별칭만 사용하세요.</p></footer>
  </body>
</html>
```

### guestbook.js

```js
const list = document.querySelector('#list');
const countBox = document.querySelector('#count');
const loadNotice = document.querySelector('#load-notice');
const reloadButton = document.querySelector('#reload-button');

function showList(items) {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
  countBox.textContent = `최근 글 ${items.length}개`;
}

async function loadMessages() {
  loadNotice.textContent = '불러오는 중';
  reloadButton.disabled = true;
  try {
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const items = await response.json();
    showList(items);
    loadNotice.textContent = '불러오기 완료';
    return true;
  } catch (error) {
    loadNotice.textContent = '목록을 불러오지 못했습니다. API 주소와 연결을 확인하세요.';
    console.log(error.message);
    return false;
  } finally {
    reloadButton.disabled = false;
  }
}

reloadButton.addEventListener('click', loadMessages);
loadMessages();
```

### submit.js

```js
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const submitButton = document.querySelector('#submit-button');
const notice = document.querySelector('#notice');

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 입력하세요.';
    return;
  }
  submitButton.disabled = true;
  notice.textContent = '저장 중';
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const saved = await response.json();
    notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
    form.reset();
    nameInput.focus();
    await loadMessages();
  } catch (error) {
    notice.textContent = '저장 결과를 확인하지 못했습니다. 목록을 다시 불러와 확인하세요.';
    console.log(error.message);
  } finally {
    submitButton.disabled = false;
  }
});
```

## 5. 실행과 확인

`http://localhost:8000/guestbook.html`을 연다.
별칭과 메시지를 적어 남기기를 누른다. POST 201 뒤 GET 200이 보이고 서버 id가 안내된다. 새로고침해도 글이 남는다.
Network를 Offline으로 바꿔 요청하면 화면에 실패 안내가 나온다. No throttling으로 되돌린 뒤 다시 요청한다.
저장 응답을 못 받은 경우에도 서버에 글이 생겼을 수 있다. 다시 보내기 전에 새로 불러오기로 목록을 확인한다.

## 6. 저장소에 올리기

GitHub에서 `web-week13` 저장소를 만든다(Public, README 추가 안 함).
현재 폴더: `web-week13`. `<아이디>`를 자신의 GitHub 아이디로 바꾼다.

```bash
git init
git add .
git commit -m "13주차 1일차"
git branch -M main
git remote add origin https://github.com/<아이디>/web-week13.git
git push -u origin main
```

Settings › Pages에서 main·/(root)를 선택한다. 2일차에는 add·commit·push만 반복한다.
공개 페이지에서는 강의자가 배부한 HTTPS API를 사용한다. localhost 설정을 그대로 두고 공유 완료로 판단하지 않는다.
공용 PC에서는 수업 종료 후 GitHub 브라우저 로그인과 저장된 Git 자격 증명을 정리한다.
