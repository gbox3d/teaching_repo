document.querySelector('#send').addEventListener('click', async function () {
  const id = document.querySelector('#id').value;
  const key = document.querySelector('#key').value;
  const message = document.querySelector('#message').value.trim();
  document.querySelector('#key').value = '';
  if (id === '' || key === '' || message === '') return;
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?id=eq.${id}&book_id=eq.${encodeURIComponent(BOOK_ID)}`, {
      method: 'PATCH',
      headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': key, 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: JSON.stringify({ message: message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const changed = await response.json();
    document.querySelector('#result').textContent = JSON.stringify(changed, null, 2);
    document.querySelector('#notice').textContent = changed.length === 1 ? '수정 응답 수신. GET으로 다시 확인하세요.' : '변경한 글 없음. 편집 키와 ID를 확인하세요.';
  } catch (error) {
    document.querySelector('#notice').textContent = `요청 실패: ${error.message}`;
  }
});
