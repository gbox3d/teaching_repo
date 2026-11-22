const output = document.querySelector('#output');
const button = document.querySelector('#send-button');
const form = document.querySelector('#example-form');
const messageInput = document.querySelector('#message');

setupApiSettings(function () {
  button.disabled = false;
  output.textContent = '';
});

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  if (button.disabled) return;
  const message = messageInput.value.trim();
  if (message === '') {
    output.textContent = '메시지를 입력하세요.';
    return;
  }
  const entry = { book_id: BOOK_ID, name: 'student01', message: message };
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
    if (!response.ok) {
      output.textContent = `저장 거절 · HTTP ${response.status}`;
      return;
    }
    const rows = await response.json();
    output.textContent = `저장 완료 · HTTP ${response.status} · 글 번호 ${rows[0].id}`;
  } catch {
    output.textContent = '저장 결과를 확인할 수 없습니다. GET으로 목록을 조회하세요.';
  }
});
