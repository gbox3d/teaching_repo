const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const messageInput = document.querySelector('#message');

button.addEventListener('click', async function () {
  const entry = { book_id: BOOK_ID, name: 'student01', message: messageInput.value };
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify(entry)
    });
    const result = await response.json();
    output.textContent = `HTTP ${response.status} · ok ${response.ok}\n${JSON.stringify(result, null, 2)}`;
  } catch {
    output.textContent = '저장 결과를 확인할 수 없습니다. GET으로 목록을 조회하세요.';
  }
});
