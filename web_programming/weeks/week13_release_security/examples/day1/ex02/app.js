const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
button.addEventListener('click', async function () {
  button.disabled = true;
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: 'student01', message: 'POST 연습입니다.' })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const saved = await response.json();
    output.textContent = `Status ${response.status} · 글 번호 ${saved[0].id}`;
  } catch (error) {
    output.textContent = '저장 결과를 확인하지 못했습니다. 목록에서 확인하세요.';
    console.log(error.message);
  } finally {
    button.disabled = false;
  }
});
