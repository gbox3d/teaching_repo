const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const responseBody = document.querySelector('#response-body');

let latestRequest = 0;

async function readMessages() {
  const requestId = ++latestRequest;
  button.disabled = true;
  output.textContent = '불러오는 중';
  try {
    const limit = Number(document.querySelector('#limit').value);
    if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
      output.textContent = '최대 글 수는 1~100 사이로 입력하세요.';
      return;
    }
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=${limit}`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    if (requestId !== latestRequest) return false;
    responseBody.textContent = JSON.stringify(items, null, 2);
    output.textContent = `GET ${response.status} · ${items.length}개`;
  } catch (error) {
    if (requestId !== latestRequest) return false;
    output.textContent = `요청 실패: ${error.message}. 주소와 연결을 확인하세요.`;
  } finally {
    if (requestId === latestRequest) button.disabled = false;
  }
}

button.addEventListener('click', readMessages);
setupApiSettings(readMessages);
readMessages();
