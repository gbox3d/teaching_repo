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

// GET 응답 표시: 12주 목록 함수
function showList(items) {
  list.replaceChildren();
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
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
  // 학생 수정 1: 폼의 값을 읽고 앞뒤 공백을 제거한다.
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
      // 학생 수정 2: 폼 값을 JSON 요청 본문에 넣는다.
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
    // 학생 수정 3: POST 성공 뒤 서버 목록을 다시 읽는다.
    await loadMessages();
  } catch (error) {
    notice.textContent = '저장 결과를 확인하지 못했습니다. 다시 저장하기 전에 새로 불러오기로 확인하세요.';
  } finally {
    saving = false;
    submitButton.disabled = false;
  }
}

// 이벤트를 연결한 뒤 첫 목록을 읽는다.
reloadButton.addEventListener('click', loadMessages);
form.addEventListener('submit', submitMessage);
loadMessages();
