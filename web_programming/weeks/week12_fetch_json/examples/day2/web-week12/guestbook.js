const list = document.querySelector('#list');
const countBox = document.querySelector('#count');
const loadNotice = document.querySelector('#load-notice');
const reloadButton = document.querySelector('#reload-button');

function showList(items) {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
  countBox.textContent = `최근 글 ${items.length}개`;
}

async function loadMessages() {
  loadNotice.textContent = '불러오는 중';
  reloadButton.disabled = true;
  try {
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const items = await response.json();
    showList(items);
    loadNotice.textContent = '불러오기 완료';
    return true;
  } catch (error) {
    loadNotice.textContent = '목록을 불러오지 못했습니다. API 주소와 연결을 확인하세요.';
    console.log(error.message);
    return false;
  } finally {
    reloadButton.disabled = false;
  }
}

reloadButton.addEventListener('click', loadMessages);
loadMessages();
