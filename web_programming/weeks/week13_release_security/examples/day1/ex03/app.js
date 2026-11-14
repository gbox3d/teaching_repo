const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
button.addEventListener('click', async function () {
  button.disabled = true;
  try {
    const message = ''; // 빈 글 → 서버 거절. 문장을 적으면 저장된다.
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: 'student01', message: message })
    });
    const result = await response.json();
    output.textContent = `Status ${response.status} · ok ${response.ok}`;
    console.log(result);
  } catch (error) {
    output.textContent = '요청에 실패했습니다. 연결을 확인하세요.';
    console.log(error.message);
  } finally {
    button.disabled = false;
  }
});
