const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
function showList(items) {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].id} | ${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
}

async function loadMessages() {
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&order=id.desc&limit=50`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    showList(await response.json());
    return true;
  } catch (error) {
    notice.textContent = '목록 확인 실패. API 주소와 연결을 확인하세요.';
    return false;
  }
}
