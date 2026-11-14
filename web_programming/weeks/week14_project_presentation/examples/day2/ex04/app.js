document.querySelector('#send').addEventListener('click', async function () {
  const id = document.querySelector('#id').value;
  if (id === '') return;
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?id=eq.${id}&book_id=eq.${encodeURIComponent(BOOK_ID)}`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    document.querySelector('#result').textContent = JSON.stringify(items, null, 2);
    document.querySelector('#notice').textContent = items.length === 0 ? '해당 글 없음' : `서버 메시지: ${items[0].message}`;
  } catch (error) {
    document.querySelector('#notice').textContent = `확인 실패: ${error.message}`;
  }
});
