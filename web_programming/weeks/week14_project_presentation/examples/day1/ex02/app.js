document.querySelector('#send').addEventListener('click', async function () {
  const id = document.querySelector('#id').value;
  const key = document.querySelector('#key').value;
  document.querySelector('#key').value = '';
  if (id === '' || key === '') return;
  const notice = document.querySelector('#notice');
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?id=eq.${id}&book_id=eq.${encodeURIComponent(BOOK_ID)}`, {
      method: 'DELETE', headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': key }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    notice.textContent = `HTTP ${response.status}. 삭제 여부는 GET으로 확인하세요.`;
    // 204에는 본문이 없다. response.json()을 호출하지 않는다.
  } catch (error) {
    notice.textContent = `요청 실패: ${error.message}`;
  }
});
