const form = document.querySelector('#update-form');
const fields = document.querySelector('#fields');
const entries = document.querySelector('#entry');
const messageInput = document.querySelector('#message');
const statusLine = document.querySelector('#status');
let bookUrl;

async function loadEntries() {
  if (!await loadConfig()) return;
  bookUrl = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}`;
  try {
    const response = await fetch(bookUrl + '&select=id,name,message&order=id.desc', {
      headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store'
    });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const rows = await response.json();
    for (const row of rows) {
      entries.add(new Option(`#${row.id} ${row.name} · ${row.message}`, row.id));
    }
    fields.disabled = rows.length === 0;
    if (!rows.length) statusLine.textContent = '수정할 글 없음';
  } catch (error) {
    statusLine.textContent = `목록 조회 실패 (${error.message}). 페이지를 새로고침하세요.`;
  }
}

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  if (fields.disabled) return;
  const message = messageInput.value.trim();
  if (!message) {
    statusLine.textContent = '새 메시지를 입력하세요.';
    return;
  }
  const option = entries.selectedOptions[0];
  const url = bookUrl + '&id=eq.' + option.value;
  fields.disabled = true;
  statusLine.textContent = '수정 중';
  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json', Prefer: 'return=representation'
      },
      body: JSON.stringify({ message: message })
    });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const changed = await response.json();
    if (!changed.length) {
      statusLine.textContent = '수정된 글이 없습니다. 방명록 태그와 글 번호를 확인하세요.';
      return;
    }

    const check = await fetch(url, { headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store' });
    if (!check.ok) throw new Error('HTTP ' + check.status);
    const rows = await check.json();
    if (!rows.length || rows[0].message !== message) {
      statusLine.textContent = '다시 조회한 결과가 다릅니다. 목록을 확인하세요.';
      return;
    }
    const row = rows[0];
    option.textContent = `#${row.id} ${row.name} · ${row.message}`;
    statusLine.textContent = `수정 완료 · 글 번호 ${row.id}`;
    form.reset();
  } catch (error) {
    statusLine.textContent = `수정 결과를 확인할 수 없습니다 (${error.message}). 목록을 확인하세요.`;
  } finally {
    fields.disabled = false;
  }
});

loadEntries();
