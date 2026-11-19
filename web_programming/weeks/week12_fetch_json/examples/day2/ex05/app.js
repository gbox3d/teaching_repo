const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const responseBody = document.querySelector('#response-body');

let latestRequest = 0;

async function readMessages() {
  const requestId = ++latestRequest;
  button.disabled = true;
  output.textContent = '불러오는 중';
  try {
    const fields = document.querySelector('#request-fields').value;
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=${fields}`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    const items = await response.json();
    if (requestId !== latestRequest) return false;
    responseBody.textContent = JSON.stringify(items, null, 2);
    output.textContent = `Status ${response.status} · ok ${response.ok}`;
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
