const homeCountBox = document.querySelector('#home-count');
const homeCountButton = document.querySelector('#home-count-button');
let homeCount = 0;
homeCountButton.addEventListener('click', function () {
  homeCount++;
  homeCountBox.textContent = `클릭 ${homeCount}회`;
});

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
// 제공 코드: 먼저 보낸 조회의 늦은 응답은 현재 목록에 표시하지 않는다.
let latestRequest = 0;
let saving = false;
let editing = false;
const editNotice = document.querySelector('#edit-notice');
const editForm = document.querySelector('#edit-form');
const editId = document.querySelector('#edit-id');
const editMessage = document.querySelector('#edit-message');
const saveEditButton = document.querySelector('#save-edit');

// GET 응답 표시: 12주 목록 함수
function showList(items) {
  list.replaceChildren();
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `#${items[i].id} ${items[i].name}: ${items[i].message}`;
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
    if (!response.ok) {
      notice.textContent = `저장 거절: HTTP ${response.status}. 입력값과 설정을 확인하세요.`;
      return;
    }
    // HTTP 성공과 응답 본문 해석, 다음 GET의 실패를 구분한다.
    let saved;
    try { saved = await response.json(); } catch { saved = null; }
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
    notice.textContent = '저장 결과를 확인하지 못했습니다. 다시 저장하기 전에 새로 불러오기로 확인하세요.';
  } finally {
    saving = false;
    submitButton.disabled = false;
  }
}


// 제공 코드: 목록에서 고른 글을 수정 폼에 표시한다.
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

// 제공 코드: 변경 요청과 같은 URL로 대상을 다시 읽는다.
async function readMessage(url) {
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const items = await response.json();
  if (!Array.isArray(items)) throw new Error('JSON 배열이 아닙니다');
  return items;
}

// DELETE 요청: 1일차 학생 수정 3곳(대상 URL, method, 헤더).
async function deleteMessage(id, button) {
  if (editing) return;
  if (!confirm(`글 ${id}번을 삭제하시겠습니까?`)) return;
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
      // 1일차 수정 3: 공개 키를 헤더에 넣는다.
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // 204에는 본문이 없다. 같은 ID의 GET으로 실제 삭제를 확인한다.
    const remaining = await readMessage(url);
    if (remaining.length !== 0) throw new Error('방명록 태그와 글 번호를 확인하세요.');
    if (editId.value === String(id)) editForm.reset();
    const loaded = await loadMessages();
    editNotice.textContent = loaded ? '삭제 확인 완료' : '삭제 확인 완료 · 목록을 다시 불러오세요.';
  } catch (error) {
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
  if (id === '' || message === '') {
    editNotice.textContent = '수정할 글, 메시지를 확인하세요.';
    return;
  }
  // 2일차 수정 1: 선택한 서버 ID와 방명록 번호로 대상을 지정한다.
  const url = messageUrl(id);
  editing = true;
  saveEditButton.disabled = true;
  editNotice.textContent = '수정 중';
  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json', Prefer: 'return=representation'
      },
      // 2일차 수정 2: 수정 메시지만 JSON 본문에 넣는다.
      body: JSON.stringify({ message: message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const changed = await response.json();
    if (!Array.isArray(changed) || changed.length !== 1 || String(changed[0].id) !== id) {
      throw new Error('방명록 태그와 글 번호를 확인하세요.');
    }
    // 2일차 수정 3: 같은 ID를 다시 읽고 메시지를 비교한다.
    const saved = await readMessage(url);
    if (saved.length !== 1 || String(saved[0].id) !== id || saved[0].message !== message) {
      throw new Error('저장한 글을 다시 확인하지 못했습니다.');
    }
    // 대기 중 선택하거나 새로 입력한 내용은 지우지 않는다.
    if (editId.value === id && editMessage.value.trim() === message) editForm.reset();
    const loaded = await loadMessages();
    editNotice.textContent = loaded ? '수정 확인 완료' : '수정 확인 완료 · 목록을 다시 불러오세요.';
  } catch (error) {
    editNotice.textContent = `수정 확인 실패: ${error.message}. 다시 요청하기 전에 조회하세요.`;
  } finally {
    editing = false;
    saveEditButton.disabled = false;
  }
}

reloadButton.addEventListener('click', loadMessages);
form.addEventListener('submit', submitMessage);
editForm.addEventListener('submit', updateMessage);

// 화면을 숨겨도 DOM과 입력은 유지한다. 이벤트 등록은 이 함수 밖에서 한 번만 한다.
function showRoute() {
  const route = location.hash.slice(1) || 'home';
  const known = route === 'home' || route === 'about' || route === 'guestbook';
  const visibleId = known ? route : 'not-found';
  const sections = document.querySelectorAll('main > section');
  for (let i = 0; i < sections.length; i++) sections[i].hidden = sections[i].id !== visibleId;
  const links = document.querySelectorAll('[data-route]');
  for (let i = 0; i < links.length; i++) {
    const current = known && links[i].dataset.route === route;
    links[i].classList.toggle('w3-teal', current);
    if (current) links[i].setAttribute('aria-current', 'page');
    else links[i].removeAttribute('aria-current');
  }
  const heading = document.querySelector(`#${visibleId} h2`);
  document.title = `${heading.textContent} · Hash SPA`;
  heading.focus();
}
window.addEventListener('hashchange', showRoute);
// 직접 hash 진입의 기본 앵커 처리 뒤에도 제목 포커스를 유지한다.
window.addEventListener('load', showRoute, { once: true });
showRoute();

// 모든 DOM·함수·이벤트 준비 뒤 최초 GET을 실행한다.
loadMessages();
