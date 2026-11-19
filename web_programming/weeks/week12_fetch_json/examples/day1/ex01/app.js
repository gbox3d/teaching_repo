const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const responseBody = document.querySelector('#response-body');

let latestRequest = 0;

async function readMessages() {
  const requestId = ++latestRequest;
  button.disabled = true;
  output.textContent = '불러오는 중';
  try {
    const url = `${API_BASE_URL}/rest/v1/about`;
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
