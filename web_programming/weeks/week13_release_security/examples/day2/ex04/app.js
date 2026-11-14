const form = document.querySelector('#example-form');
const output = document.querySelector('#output');
const button = document.querySelector('#send-button');
form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const message = document.querySelector('#message').value.trim();
  if (message === '') {
    output.textContent = '메시지를 입력하세요.';
    return;
  }
  button.disabled = true;
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
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const saved = await response.json();
    output.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
    form.reset();
  } catch (error) {
    output.textContent = '저장 결과를 확인하지 못했습니다. 목록에서 확인하세요.';
    console.log(error.message);
  } finally {
    button.disabled = false;
  }
});
