# 14주차 따라하기: 서버의 글 수정·삭제

## 수업 전 파일 준비

새 web-week14 저장소와 [13주 완성본](../week13_release_security/examples/day2/web-week13/)을 준비한다. [이번 주 제공본](examples/day2/web-week14/README.md)의 기본 배포 파일을 복사한다. settings·폼·키·초기화·오류 복구는 제공하고 학생은 각 차시 3곳만 수정한다. 강의·시연 60분 뒤 학생 실습 30분이며 업로드는 수업 뒤 정리한다.

학생 폴더에서 [정적 서버](../../tools/static-server/README.md)를 실행한다. API는 [별도 로컬 API](../../tools/guestbook-api/README.md)를 실행하거나 강의자가 준비한 HTTPS API를 쓴다. 화면 서버와 데이터 서버는 서로 다르다.

## 설정과 요청 확인

브라우저 API 설정 패널에 주소·공개 키·방명록 번호를 입력하고 적용한다. 제공 api-settings.js는 로컬 기본값으로 시작한다. 공용 설정은 메모리에만 있으므로 새로고침 뒤 다시 입력한다. 설정 적용은 선택 ID·새 글 폼·편집 폼·편집 키를 지운다.

REST Client의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. .env는 Git과 배포 ZIP에서 제외한다. 브라우저 설정과 .env는 별개다. requests.http의 **Send Request**로 about → help → 목록 → 대상 GET을 실행한다. 자기 글 ID를 MESSAGE_ID에 넣고 PATCH·DELETE 뒤 같은 ID를 다시 조회한다. 편집 키는 마스킹되는 password 프롬프트로 입력한다.

## 1일차 DELETE 수정

ex01에서 인덱스와 ID를 비교한 뒤 ex02 시연을 본다. 제공 guestbook.js의 deleteMessage에서 ① messageUrl(id) 대상, ② DELETE method, ③ apikey·X-Edit-Key 헤더를 확인·수정한다. readMessage와 204 이후 재조회는 제공한다. 자기 연습 글을 세 개 만들고 가운데 ID만 삭제한다. 틀린 키로 남은 글을 삭제하려 해도 GET에서 원본이 남아야 한다.

## 2일차 PATCH 수정

ex03에서 JSON 본문을 보고 ex04에서 같은 ID를 다시 읽는다. guestbook.js의 updateMessage에서 ① 대상 URL, ② JSON.stringify({ message: message }) 본문, ③ readMessage(url, publicKey) 재조회를 확인·수정한다. 응답 배열 검증과 메시지 비교는 제공한다. PATCH 200 []는 성공으로 표시하지 않는다.

## 완성본 전문

아래 세 파일은 실행 파일과 같다. 제공 HTML은 W3.CSS를 CDN에서 불러오고 설정 파일과 동작 파일을 defer로 읽는다. guestbook.js 끝에서 DOM·함수·이벤트를 준비한 뒤 설정 등록과 최초 GET을 실행한다.

### guestbook.html

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>온라인 방명록</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css">
    <script src="api-settings.js" defer></script>
    <script src="guestbook.js" defer></script>
  </head>
  <body class="w3-light-grey">
    <header class="w3-container w3-teal w3-padding-16">
      <h1>온라인 방명록</h1>
    </header>
    <nav class="w3-bar w3-white w3-card" aria-label="주 메뉴">
      <a class="w3-bar-item w3-button w3-mobile" href="index.html">홈</a>
      <a class="w3-bar-item w3-button w3-mobile" href="about.html">내 정보</a>
      <a class="w3-bar-item w3-button w3-mobile w3-teal" href="guestbook.html" aria-current="page">방명록</a>
    </nav>
    <main class="w3-content w3-padding">
      <details class="w3-margin-bottom">
        <summary>API 설정</summary>
        <form id="api-settings-form" autocomplete="off">
          <p><label for="api-base-url">API 주소</label> <input id="api-base-url" type="url" required></p>
          <p><label for="api-public-key">공개 키</label> <input id="api-public-key" type="password" autocomplete="off" required></p>
          <p><label for="api-book-id">방명록 번호</label> <input id="api-book-id" pattern="[a-z0-9_-]{1,40}" required></p>
          <button class="w3-button w3-teal" type="submit">설정 적용</button>
          <p id="api-settings-notice" role="status">로컬 연습 설정</p>
        </form>
      </details>
      <section class="w3-container w3-card w3-white w3-margin-top">
        <h2>한 줄 남기기</h2>
        <form id="guestbook-form">
          <p><label for="name">이름(별칭)</label>
            <input class="w3-input w3-border" id="name" maxlength="30" required></p>
          <p><label for="message">메시지</label>
            <textarea class="w3-input w3-border" id="message" rows="3" maxlength="500" required></textarea></p>
          <p><button class="w3-button w3-teal" id="submit-button" type="submit">남기기</button></p>
        </form>
        <div class="w3-text-red" id="notice" role="status"></div>
      </section>
      <section class="w3-container w3-card w3-white w3-margin-top">
        <h2>글 수정·삭제</h2>
        <form id="key-form" autocomplete="off">
          <label for="edit-key">편집 키</label>
          <input class="w3-input w3-border" id="edit-key" type="password" autocomplete="off">
          <button class="w3-button w3-teal" id="key-button" type="submit">키 적용</button>
          <button class="w3-button w3-light-grey" id="clear-key" type="button">키 지우기</button>
        </form>
        <div id="edit-notice" role="status"></div>
        <form id="edit-form">
          <label for="edit-id">수정할 글 ID</label><input class="w3-input w3-border" id="edit-id" readonly>
          <label for="edit-message">수정 메시지</label>
          <textarea class="w3-input w3-border" id="edit-message" maxlength="500" required></textarea>
          <button class="w3-button w3-teal" id="save-edit" type="submit">수정 저장</button>
        </form>
      </section>
      <section class="w3-container w3-card w3-white w3-margin-top">
        <h2>남긴 글</h2>
        <p><button class="w3-button w3-teal" id="reload-button" type="button">새로 불러오기</button></p>
        <div class="w3-text-grey" id="load-notice" role="status"></div>
        <p id="empty" hidden>아직 남긴 글이 없습니다.</p>
        <ul id="list" class="w3-ul w3-responsive" aria-live="polite"></ul>
        <div id="count">최근 글 0개</div>
      </section>
    </main>
    <footer class="w3-container w3-center w3-text-grey w3-padding-16"><p>수업용 연습 페이지 · 별칭만 사용하세요.</p></footer>
  </body>
</html>
```

### api-settings.js

```js
// 제공 코드: 입력한 설정은 현재 페이지의 메모리에서만 사용한다.
let API_BASE_URL = 'http://127.0.0.1:8787';
let API_PUBLIC_KEY = 'classroom-local';
let BOOK_ID = 'student01';

function setupApiSettings(onApply) {
  const form = document.querySelector('#api-settings-form');
  const baseInput = document.querySelector('#api-base-url');
  const keyInput = document.querySelector('#api-public-key');
  const bookInput = document.querySelector('#api-book-id');
  const notice = document.querySelector('#api-settings-notice');
  baseInput.value = API_BASE_URL;
  keyInput.value = API_PUBLIC_KEY;
  bookInput.value = BOOK_ID;

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const baseUrl = baseInput.value.trim().replace(/\/+$/, '');
    const publicKey = keyInput.value.trim();
    const bookId = bookInput.value.trim();
    if (!/^https?:\/\//.test(baseUrl) || publicKey === '' || !/^[a-z0-9_-]{1,40}$/.test(bookId)) {
      notice.textContent = 'API 주소, 공개 키, 방명록 번호를 확인하세요.';
      return;
    }
    API_BASE_URL = baseUrl;
    API_PUBLIC_KEY = publicKey;
    BOOK_ID = bookId;
    notice.textContent = '설정 적용 완료 · 새로고침 후 재입력';
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      await onApply();
    } finally {
      button.disabled = false;
    }
  });
}
```

### guestbook.js

```js
const list = document.querySelector('#list');
const countBox = document.querySelector('#count');
const empty = document.querySelector('#empty');
const loadNotice = document.querySelector('#load-notice');
const reloadButton = document.querySelector('#reload-button');
const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const submitButton = document.querySelector('#submit-button');
const notice = document.querySelector('#notice');
// 제공 코드: 설정 변경과 겹친 이전 응답을 현재 목록에 표시하지 않는다.
let settingsVersion = 0;
let latestRequest = 0;
let saving = false;
let editing = false;
let editKey = '';
const editNotice = document.querySelector('#edit-notice');
const editForm = document.querySelector('#edit-form');
const editId = document.querySelector('#edit-id');
const editMessage = document.querySelector('#edit-message');
const keyInput = document.querySelector('#edit-key');
const saveEditButton = document.querySelector('#save-edit');

// GET 응답 표시: 12주 목록 함수
function showList(items) {
  list.replaceChildren();
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
    li.append(createEditButtons(items[i]));
    list.append(li);
  }
  countBox.textContent = `최근 글 ${items.length}개`;
  empty.hidden = items.length !== 0;
}

// GET 요청: 요청 번호는 제공 코드다.
async function loadMessages() {
  const requestId = ++latestRequest;
  loadNotice.textContent = '불러오는 중';
  reloadButton.disabled = true;
  try {
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`;
    const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    if (!Array.isArray(items)) throw new Error('JSON 배열이 아닙니다');
    if (requestId !== latestRequest) return false;
    showList(items);
    loadNotice.textContent = '불러오기 완료';
    return true;
  } catch (error) {
    if (requestId !== latestRequest) return false;
    list.replaceChildren();
    empty.hidden = true;
    countBox.textContent = '조회 결과 없음';
    loadNotice.textContent = `조회 실패: ${error.message}. 새로 불러오기를 누르세요.`;
    return false;
  } finally {
    if (requestId === latestRequest) reloadButton.disabled = false;
  }
}

// POST 요청: 학생 수정은 폼 값, JSON 본문, 재조회 호출이다.
async function submitMessage(event) {
  event.preventDefault();
  if (saving) return;
  // 13주 복습: 폼의 값을 읽고 앞뒤 공백을 제거한다.
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 입력하세요.';
    return;
  }
  const requestVersion = settingsVersion;
  saving = true;
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
      // 13주 복습: 폼 값을 JSON 요청 본문에 넣는다.
      body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
    });
    if (requestVersion !== settingsVersion) return;
    if (!response.ok) {
      notice.textContent = `저장 거절: HTTP ${response.status}. 입력값과 설정을 확인하세요.`;
      return;
    }
    // HTTP 성공과 응답 본문 해석, 다음 GET의 실패를 구분한다.
    let saved;
    try { saved = await response.json(); } catch { saved = null; }
    if (requestVersion !== settingsVersion) return;
    if (Array.isArray(saved) && saved[0]?.id) {
      notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
      // 대기 중 사용자가 새로 쓴 입력은 지우지 않는다.
      if (nameInput.value.trim() === name && messageInput.value.trim() === message) form.reset();
      nameInput.focus();
    } else {
      notice.textContent = '저장 응답 수신 · 글 번호를 확인하지 못했습니다. 목록을 확인하고 다시 저장하지 마세요.';
    }
    // 13주 복습: POST 성공 뒤 서버 목록을 다시 읽는다.
    await loadMessages();
  } catch (error) {
    if (requestVersion !== settingsVersion) return;
    notice.textContent = '저장 결과를 확인하지 못했습니다. 다시 저장하기 전에 새로 불러오기로 확인하세요.';
  } finally {
    saving = false;
    submitButton.disabled = false;
  }
}


// 제공 코드: 서버 ID 선택, 편집 키와 폼을 연결한다.
function createEditButtons(item) {
  const box = document.createElement('div');
  const editButton = document.createElement('button');
  editButton.type = 'button';
  editButton.className = 'w3-button w3-light-grey';
  editButton.textContent = '수정';
  editButton.addEventListener('click', function () {
    editId.value = item.id;
    editMessage.value = item.message;
    editMessage.focus();
  });
  const deleteButton = document.createElement('button');
  deleteButton.type = 'button';
  deleteButton.className = 'w3-button w3-light-grey';
  deleteButton.textContent = '삭제';
  deleteButton.addEventListener('click', function () {
    deleteMessage(item.id, deleteButton);
  });
  box.append(editButton, deleteButton);
  return box;
}

function messageUrl(id) {
  return `${API_BASE_URL}/rest/v1/guestbook?id=eq.${encodeURIComponent(id)}&book_id=eq.${encodeURIComponent(BOOK_ID)}`;
}

// 제공 코드: 요청 시작 때 고정한 URL·공개 키로 같은 대상을 확인한다.
async function readMessage(url, publicKey) {
  const response = await fetch(url, { headers: { apikey: publicKey } });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const items = await response.json();
  if (!Array.isArray(items)) throw new Error('JSON 배열이 아닙니다');
  return items;
}

// DELETE 요청: 1일차 학생 수정 3곳(대상 URL, method, 헤더).
async function deleteMessage(id, button) {
  if (editing) return;
  if (editKey === '') {
    editNotice.textContent = '편집 키를 먼저 입력하세요.';
    return;
  }
  if (!confirm(`글 ${id}번을 삭제하시겠습니까?`)) return;
  const requestVersion = settingsVersion;
  const publicKey = API_PUBLIC_KEY;
  // 1일차 수정 1: 배열 위치가 아닌 서버 ID를 URL에 넣는다.
  const url = messageUrl(id);
  editing = true;
  button.disabled = true;
  saveEditButton.disabled = true;
  editNotice.textContent = '삭제 중';
  try {
    const response = await fetch(url, {
      // 1일차 수정 2: 삭제 메서드를 지정한다.
      method: 'DELETE',
      // 1일차 수정 3: 공개 키와 편집 키를 헤더에 넣는다.
      headers: { apikey: publicKey, 'X-Edit-Key': editKey }
    });
    if (requestVersion !== settingsVersion) return;
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // 204에는 본문이 없다. 같은 ID의 GET으로 실제 삭제를 확인한다.
    const remaining = await readMessage(url, publicKey);
    if (requestVersion !== settingsVersion) return;
    if (remaining.length !== 0) throw new Error('편집 키와 글 번호를 확인하세요.');
    if (editId.value === String(id)) editForm.reset();
    const loaded = await loadMessages();
    if (requestVersion !== settingsVersion) return;
    editNotice.textContent = loaded ? '삭제 확인 완료' : '삭제 확인 완료 · 목록을 다시 불러오세요.';
  } catch (error) {
    if (requestVersion !== settingsVersion) return;
    editNotice.textContent = `삭제 확인 실패: ${error.message}. 다시 요청하기 전에 조회하세요.`;
  } finally {
    editing = false;
    button.disabled = false;
    saveEditButton.disabled = false;
  }
}

// PATCH 요청: 2일차 학생 수정 3곳(대상 URL, JSON 본문, 같은 ID 재조회).
async function updateMessage(event) {
  event.preventDefault();
  if (editing) return;
  const id = editId.value;
  const message = editMessage.value.trim();
  if (editKey === '' || id === '' || message === '') {
    editNotice.textContent = '편집 키, 수정할 글, 메시지를 확인하세요.';
    return;
  }
  const requestVersion = settingsVersion;
  const publicKey = API_PUBLIC_KEY;
  // 2일차 수정 1: 선택한 서버 ID와 방명록 번호로 대상을 지정한다.
  const url = messageUrl(id);
  editing = true;
  saveEditButton.disabled = true;
  editNotice.textContent = '수정 중';
  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        apikey: publicKey, 'X-Edit-Key': editKey,
        'Content-Type': 'application/json', Prefer: 'return=representation'
      },
      // 2일차 수정 2: 수정 메시지만 JSON 본문에 넣는다.
      body: JSON.stringify({ message: message })
    });
    if (requestVersion !== settingsVersion) return;
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const changed = await response.json();
    if (requestVersion !== settingsVersion) return;
    if (!Array.isArray(changed) || changed.length !== 1 || String(changed[0].id) !== id) {
      throw new Error('편집 키와 글 번호를 확인하세요.');
    }
    // 2일차 수정 3: 같은 ID를 다시 읽고 메시지를 비교한다.
    const saved = await readMessage(url, publicKey);
    if (requestVersion !== settingsVersion) return;
    if (saved.length !== 1 || String(saved[0].id) !== id || saved[0].message !== message) {
      throw new Error('저장한 글을 다시 확인하지 못했습니다.');
    }
    // 대기 중 선택하거나 새로 입력한 내용은 지우지 않는다.
    if (editId.value === id && editMessage.value.trim() === message) editForm.reset();
    const loaded = await loadMessages();
    if (requestVersion !== settingsVersion) return;
    editNotice.textContent = loaded ? '수정 확인 완료' : '수정 확인 완료 · 목록을 다시 불러오세요.';
  } catch (error) {
    if (requestVersion !== settingsVersion) return;
    editNotice.textContent = `수정 확인 실패: ${error.message}. 다시 요청하기 전에 조회하세요.`;
  } finally {
    editing = false;
    saveEditButton.disabled = false;
  }
}

// 제공 코드: 키는 메모리에서만 사용하고 입력 칸은 바로 비운다.
function clearEditKey() {
  editKey = '';
  keyInput.value = '';
}
document.querySelector('#key-form').addEventListener('submit', function (event) {
  event.preventDefault();
  editKey = keyInput.value.trim();
  keyInput.value = '';
  editNotice.textContent = editKey === '' ? '편집 키를 입력하세요.' : '편집 키 적용 완료';
});
document.querySelector('#clear-key').addEventListener('click', function () {
  clearEditKey();
  editNotice.textContent = '편집 키 삭제 완료';
});
reloadButton.addEventListener('click', loadMessages);
form.addEventListener('submit', submitMessage);
editForm.addEventListener('submit', updateMessage);

// 모든 DOM·함수·이벤트 준비 뒤 설정과 최초 GET을 실행한다.
setupApiSettings(function () {
  settingsVersion++;
  clearEditKey();
  editForm.reset();
  form.reset();
  showList([]);
  notice.textContent = saving ? '설정 변경 완료 · 이전 저장 결과는 이전 설정에서 조회하세요.' : '';
  editNotice.textContent = '설정 변경 완료 · 편집 키를 다시 입력하세요.';
  return loadMessages();
});
loadMessages();
```

## 동작 확인과 수업 뒤 정리

글 세 개의 가운데 삭제, 남은 글 수정, 틀린 키의 변경 없음, 통신 실패 뒤 조회 복구를 확인한다. 키 지우기는 메모리와 입력 칸을 함께 비운다. 설정 변경 중 이전 요청이 완료되더라도 새 폼·안내를 바꾸지 않는다. 진행 중 요청은 서버에서 끝날 수 있으므로 원래 설정으로 돌아가 GET으로 확인한다.

키를 지우고 [실습지](lab.md)의 캡처를 만든다. 수업 뒤 add·commit·push하고 공용 HTTPS API가 준비된 경우 Pages·다른 브라우저에서 확인한다. 로컬 리허설 결과를 공용 API나 다른 기기 검증으로 기록하지 않는다. 레포트 검사는 포함하지 않는다.
