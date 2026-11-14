const list = document.querySelector('#list');
const output = document.querySelector('#output');
async function readList() {
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    for (let i = 0; i < items.length; i++) {
      const li = document.createElement('li');
      li.textContent = `${items[i].name}: ${items[i].message}`;
      list.append(li);
    }
    output.textContent = `최근 글 ${items.length}개`;
  } catch (error) {
    output.textContent = '목록을 불러오지 못했습니다.';
    console.log(error.message);
  }
}
readList();
