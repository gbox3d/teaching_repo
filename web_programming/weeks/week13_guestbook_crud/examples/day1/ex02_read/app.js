const loadButton = document.querySelector('#load');
const entries = document.querySelector('#entries');
const statusLine = document.querySelector('#status');

loadButton.addEventListener('click', async function () {
  loadButton.disabled = true;
  statusLine.textContent = '조회 중';
  const tag = encodeURIComponent(BOOK_ID);
  const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${tag}&select=id,name,message&order=id.desc`;
  try {
    const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store' });
    if (!response.ok) {
      statusLine.textContent = `목록 조회 실패 · HTTP ${response.status}`;
      return;
    }

    const rows = await response.json();
    entries.replaceChildren();
    for (const row of rows) {
      const item = document.createElement('li');
      item.textContent = `#${row.id} ${row.name} · ${row.message}`;
      entries.append(item);
    }
    statusLine.textContent = rows.length ? `${BOOK_ID} · ${rows.length}개` : '등록된 글 없음';
  } catch {
    statusLine.textContent = '목록을 불러올 수 없습니다. 연결을 확인하세요.';
  } finally {
    loadButton.disabled = false;
  }
});

loadConfig().then(function (ready) {
  loadButton.disabled = !ready;
});
