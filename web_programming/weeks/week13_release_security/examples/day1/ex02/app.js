const output = document.querySelector('#output');
const list = document.querySelector('#list');
const loadNotice = document.querySelector('#load-notice');
const reloadButton = document.querySelector('#reload-button');
const button = document.querySelector('#run-button');

// 제공 코드: 대기 중 중복 요청과 설정 변경 후의 오래된 응답을 막는다.
let saving = false;
let settingsVersion = 0;
let requestId = 0;

// 제공된 GET: 저장 결과는 이 목록에서 확인한다.
async function loadMessages() {
  const currentRequest = ++requestId;
  reloadButton.disabled = true;
  loadNotice.textContent = '불러오는 중';
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    if (!Array.isArray(items)) throw new Error('JSON 배열이 아닙니다');
    if (currentRequest !== requestId) return false;
    list.replaceChildren();
    for (let i = 0; i < items.length; i++) {
      const li = document.createElement('li');
      li.textContent = `${items[i].id} · ${items[i].name}: ${items[i].message}`;
      list.append(li);
    }
    loadNotice.textContent = `불러오기 완료 · ${items.length}개`;
    return true;
  } catch (error) {
    if (currentRequest !== requestId) return false;
    list.replaceChildren();
    loadNotice.textContent = `조회 실패: ${error.message}. 새로 불러오기를 누르세요.`;
    return false;
  } finally {
    if (currentRequest === requestId) reloadButton.disabled = false;
  }
}

button.addEventListener('click', async function (event) {
  event.preventDefault();
  if (saving) return;
  const message = 'POST 연습입니다.';

  const requestVersion = settingsVersion;
  saving = true;
  button.disabled = true;
  output.textContent = '저장 중';
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: 'student01', message: message })
    });
    if (requestVersion !== settingsVersion) return;
    if (!response.ok) {
      output.textContent = `저장 거절: HTTP ${response.status} · ok ${response.ok}`;
      return;
    }
    let saved;
    try { saved = await response.json(); } catch { saved = null; }
    if (requestVersion !== settingsVersion) return;
    if (Array.isArray(saved) && saved[0]?.id) {
      output.textContent = `저장 완료 · HTTP ${response.status} · 글 번호 ${saved[0].id}`;

    } else {
      output.textContent = '저장 응답 수신 · 글 번호 확인 실패. 목록을 확인하고 다시 저장하지 마세요.';
    }
    // 목록은 새로 불러오기로 확인한다. 자동 재조회는 ex06에서 연결한다.
  } catch (error) {
    if (requestVersion === settingsVersion) output.textContent = '저장 결과 확인 실패. 다시 저장하기 전에 새로 불러오기로 확인하세요.';
  } finally {
    saving = false;
    button.disabled = false;
  }
});

reloadButton.addEventListener('click', loadMessages);
setupApiSettings(function () {
  settingsVersion++;
  list.replaceChildren();
  output.textContent = saving ? '설정 변경 완료 · 이전 저장 결과는 이전 설정의 목록에서 확인하세요.' : '';
  return loadMessages();
});
loadMessages();
