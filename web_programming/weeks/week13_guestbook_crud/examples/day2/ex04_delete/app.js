const entries = document.querySelector('#entries');
const statusLine = document.querySelector('#status');
let bookUrl;

async function loadEntries() {
  if (!await loadConfig()) return;
  bookUrl = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}`;
  try {
    const response = await fetch(bookUrl + '&select=id,name,message&order=id.desc', {
      headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store'
    });
    if (!response.ok) {
      statusLine.textContent = `목록 조회 실패 · HTTP ${response.status}`;
      return;
    }
    const rows = await response.json();
    for (const row of rows) {
      const item = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'w3-button w3-red w3-small w3-margin-left';
      button.textContent = '삭제';
      button.setAttribute('aria-label', `글 ${row.id} 삭제`);
      button.addEventListener('click', function () {
        deleteEntry(row.id, item, button);
      });
      item.append(`#${row.id} ${row.name} · ${row.message}`, button);
      entries.append(item);
    }
    if (!rows.length) statusLine.textContent = '삭제할 글 없음';
  } catch {
    statusLine.textContent = '목록을 불러올 수 없습니다. 페이지를 새로고침하세요.';
  }
}

async function deleteEntry(id, item, button) {
  if (!window.confirm(`글 ${id}번을 삭제하시겠습니까?`)) return;
  const url = bookUrl + '&id=eq.' + id;
  button.disabled = true;
  statusLine.textContent = '삭제 중';
  try {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) {
      statusLine.textContent = `삭제 요청 실패 · HTTP ${response.status}`;
      return;
    }
    const check = await fetch(url, { headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store' });
    if (!check.ok) {
      statusLine.textContent = `삭제 결과 조회 실패 · HTTP ${check.status}`;
      return;
    }
    const rows = await check.json();
    if (rows.length) {
      statusLine.textContent = '글이 남아 있습니다. 방명록 태그와 글 번호를 확인하세요.';
      return;
    }
    item.remove();
    statusLine.textContent = `삭제 완료 · 글 번호 ${id}`;
  } catch {
    statusLine.textContent = '삭제 결과를 확인할 수 없습니다. 페이지를 새로고침하세요.';
  } finally {
    button.disabled = false;
  }
}

loadEntries();
