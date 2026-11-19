const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const list = document.querySelector('#list');

let latestRequest = 0;

async function readMessages() {
  const requestId = ++latestRequest;
  button.disabled = true;
  output.textContent = '불러오는 중';
  try {
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    if (requestId !== latestRequest) return false;
    list.replaceChildren();
    for (let i = 0; i < items.length; i++) {
      const li = document.createElement('li');
      li.textContent = `${items[i].name}: ${items[i].message}`;
      list.append(li);
    }
    output.textContent = `GET ${response.status} · 최근 글 ${items.length}개`;
  } catch (error) {
    if (requestId !== latestRequest) return false;
    list.replaceChildren();
    output.textContent = `조회 실패: ${error.message}. 연결을 확인하고 다시 요청하세요.`;
  } finally {
    if (requestId === latestRequest) button.disabled = false;
  }
}

button.addEventListener('click', readMessages);
setupApiSettings(readMessages);
readMessages();
