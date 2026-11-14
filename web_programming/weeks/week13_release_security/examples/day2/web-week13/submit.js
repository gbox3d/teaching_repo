const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const submitButton = document.querySelector('#submit-button');
const notice = document.querySelector('#notice');

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 입력하세요.';
    return;
  }
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
      body: JSON.stringify({ book_id: BOOK_ID, name: name, message: message })
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const saved = await response.json();
    notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
    form.reset();
    nameInput.focus();
    await loadMessages();
  } catch (error) {
    notice.textContent = '저장 결과를 확인하지 못했습니다. 목록을 다시 불러와 확인하세요.';
    console.log(error.message);
  } finally {
    submitButton.disabled = false;
  }
});
