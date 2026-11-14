[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

# 14주차 따라하기 — 서버의 글 수정·삭제

## 1. 지난주 완성본 준비

현재 폴더: 새 `web-week14`. [13주 완성본](../week13_release_security/examples/day2/web-week13/)에서 홈·내 정보·방명록·CSS·JavaScript를 가져온다. 이번 주 사용할 파일 목록은 [예제 안내](examples/README.md)에 있다.

`config.example.js`의 API 주소·공개 키·BOOK_ID를 강의자 제공값으로 바꾼다. 파일 이름을 바꾸지 않는다. 편집 키는 넣지 않는다. 로컬 리허설의 주소는 `http://127.0.0.1:8787`이며 공용 HTTPS API 주소가 아니다.

강의자 API 실행은 [서버 안내](../../tools/guestbook-api/README.md)를 따른다. 학생 폴더는 아래처럼 연다. `server.mjs`는 [수업용 정적 서버](../../tools/static-server/server.mjs) 파일이다.

```powershell
node server.mjs
```

예상 결과: `http://localhost:8000/guestbook.html`에서 목록이 보인다. 공개 페이지에서 테스트할 때는 공용 HTTPS API 설정으로 바꾼다.

## 2. 비교 예제 실행

현재 폴더: `web-week14/ex/`. [ex01](examples/day1/ex01/)·[ex02](examples/day1/ex02/)·[ex03](examples/day2/ex03/)·[ex04](examples/day2/ex04/)를 폴더째 받는다. 서버 주소 `/ex/ex02/`처럼 연다. 모든 예제의 `config.example.js`도 같은 설정으로 맞춘다.

1. ex01에서 배열 순서를 바꾸어 ID와 위치를 비교한다.
2. 13주 폼으로 자기 방명록에 연습 글 세 개를 남긴다. GET 응답에서 ID를 읽는다.
3. ex02에 자기 글 ID와 배부받은 키를 입력하고 DELETE한다. 키 칸은 요청 직전 비워진다.
4. ex04로 같은 ID를 읽는다. 배열이 비면 그 글이 없다. 다른 두 글은 남아 있어야 한다.
5. ex03으로 남은 글 하나의 메시지를 PATCH하고 ex04로 다시 확인한다.

## 3. 수정·삭제 화면 연결

현재 폴더: `web-week14`. 아래 파일을 같은 위치에 둔다. 13주 파일 중 `guestbook.js`는 목록마다 `createEditButtons(items[i])`를 붙이는 줄만 추가한다. `submit.js`는 기존 POST를 유지한다.

HTML의 script는 config → GET → POST → actions → delete → edit 순서이며 모두 defer다. 키 적용 버튼은 값을 메모리 변수로 옮기고 입력 칸을 비운다. 새로고침하면 키를 다시 입력한다.

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
    <script src="actions.js" defer></script>
    <script src="delete.js" defer></script>
    <script src="edit.js" defer></script>
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
      <h2>편집 키</h2>
      <label for="edit-key">강의자가 배부한 자기 편집 키</label>
      <input id="edit-key" type="password" autocomplete="off">
      <button id="key-button" type="button">키 적용</button>
      <div id="edit-notice" role="status"></div>
      <form id="edit-form">
        <label for="edit-id">수정할 글 ID</label><input id="edit-id" readonly>
        <label for="edit-message">수정 메시지</label>
        <textarea id="edit-message" maxlength="500" required></textarea>
        <button id="save-edit" type="submit">수정 저장</button>
      </form>
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

### config.example.js

```js
// 강의자가 안내한 공용 API 주소·공개 키·방명록 번호로 바꾼다.
// 아래 값은 내 PC의 로컬 연습 서버용이다. 편집 키는 여기에 넣지 않는다.
const API_BASE_URL = 'http://127.0.0.1:8787';
const API_PUBLIC_KEY = 'classroom-local';
const BOOK_ID = 'student01';
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
    li.append(createEditButtons(items[i]));
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

### actions.js

```js
let editKey = '';
const editNotice = document.querySelector('#edit-notice');
const editForm = document.querySelector('#edit-form');
const editId = document.querySelector('#edit-id');
const editMessage = document.querySelector('#edit-message');

document.querySelector('#key-button').addEventListener('click', function () {
  const input = document.querySelector('#edit-key');
  editKey = input.value.trim();
  input.value = '';
  editNotice.textContent = editKey === '' ? '편집 키를 입력하세요.' : '편집 키 입력 완료';
});

function createEditButtons(item) {
  const box = document.createElement('div');
  const editButton = document.createElement('button');
  editButton.textContent = '수정';
  editButton.addEventListener('click', function () {
    editId.value = item.id;
    editMessage.value = item.message;
    editMessage.focus();
  });
  const deleteButton = document.createElement('button');
  deleteButton.textContent = '삭제';
  deleteButton.addEventListener('click', function () {
    deleteMessage(item.id, deleteButton);
  });
  box.append(editButton, deleteButton);
  return box;
}

function messageUrl(id) {
  return `${API_BASE_URL}/rest/v1/guestbook?id=eq.${id}&book_id=eq.${encodeURIComponent(BOOK_ID)}`;
}

async function readMessage(id) {
  const response = await fetch(messageUrl(id), { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
}
```

### delete.js

```js
async function deleteMessage(id, button) {
  if (editKey === '') {
    editNotice.textContent = '편집 키를 먼저 입력하세요.';
    return;
  }
  if (!confirm(`글 ${id}번을 삭제하시겠습니까?`)) return;
  button.disabled = true;
  editNotice.textContent = '삭제 중';
  try {
    const response = await fetch(messageUrl(id), {
      method: 'DELETE',
      headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // 204 응답에는 본문이 없으므로 response.json()을 호출하지 않는다.
    const remaining = await readMessage(id);
    if (remaining.length !== 0) throw new Error('편집 키와 글 번호를 확인하세요.');
    const loaded = await loadMessages();
    editNotice.textContent = loaded ? '삭제 완료' : '삭제 완료. 목록을 다시 불러오세요.';
  } catch (error) {
    editNotice.textContent = `삭제 확인 실패: ${error.message}`;
  } finally {
    button.disabled = false;
  }
}
```

### edit.js

```js
editForm.addEventListener('submit', async function (event) {
  event.preventDefault();
  const id = editId.value;
  const message = editMessage.value.trim();
  if (editKey === '' || id === '' || message === '') {
    editNotice.textContent = '편집 키, 수정할 글, 메시지를 확인하세요.';
    return;
  }
  const button = document.querySelector('#save-edit');
  button.disabled = true;
  editNotice.textContent = '수정 중';
  try {
    const response = await fetch(messageUrl(id), {
      method: 'PATCH',
      headers: {
        apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey,
        'Content-Type': 'application/json', Prefer: 'return=representation'
      },
      body: JSON.stringify({ message: message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const changed = await response.json();
    if (changed.length !== 1) throw new Error('편집 키와 글 번호를 확인하세요.');
    const saved = await readMessage(id);
    if (saved.length !== 1 || saved[0].message !== message) {
      throw new Error('저장한 글을 다시 확인하지 못했습니다.');
    }
    const loaded = await loadMessages();
    editNotice.textContent = loaded ? '수정 완료' : '수정 완료. 목록을 다시 불러오세요.';
    editForm.reset();
  } catch (error) {
    editNotice.textContent = `수정 확인 실패: ${error.message}`;
  } finally {
    button.disabled = false;
  }
});
```

## 4. 실행 확인과 올리기

1. 글 세 개를 남기고 두 번째 글을 삭제한다. 삭제는 204 뒤 JSON을 읽지 않는다.
2. 남은 글의 수정 버튼을 누르고 메시지를 바꾼다. 새로고침 후에도 수정값이 보여야 한다.
3. 자기 공간에서 편집 키 한 글자를 바꾸고 시도한다. 화면에 성공이라고 나오지 않고 원본이 남아야 한다.
4. 키가 코드나 캡처에 없는지 확인하고 add·commit·push한다.
5. 공용 HTTPS API가 준비되었으면 Pages 주소와 다른 브라우저에서 같은 서버 결과를 확인한다. 로컬 리허설에서는 같은 PC의 다른 브라우저로 확인한다.

제출물과 Pages 지연 처리는 [실습지](lab.md#제출--캡처-한-장)를 따른다. 레포트 검사는 이번 주 수업에 포함하지 않는다.
