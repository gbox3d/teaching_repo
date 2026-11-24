const form = document.querySelector('#entry-form');
const saveButton = document.querySelector('#save');
const statusLine = document.querySelector('#status');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  if (saveButton.disabled) return;
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (!name || !message) {
    statusLine.textContent = '별칭과 메시지를 입력하세요.';
    return;
  }

  saveButton.disabled = true;
  nameInput.readOnly = true;
  messageInput.readOnly = true;
  statusLine.textContent = '저장 중';
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name, message })
    });
    if (!response.ok) {
      statusLine.textContent = `저장 실패 · HTTP ${response.status}`;
      return;
    }

    const rows = await response.json();
    statusLine.textContent = `저장 완료 · 글 번호 ${rows[0].id} · HTTP ${response.status}`;
    form.reset();
  } catch {
    statusLine.textContent = '저장 결과를 확인할 수 없습니다. 목록에서 글을 확인하세요.';
  } finally {
    nameInput.readOnly = false;
    messageInput.readOnly = false;
    saveButton.disabled = false;
  }
});

loadConfig().then(function (ready) {
  saveButton.disabled = !ready;
});
