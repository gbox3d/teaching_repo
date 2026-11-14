const output = document.querySelector('#output');
async function readRecent() {
  try {
    const limit = 2;
    const url = `${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=${limit}`;
    const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    output.textContent = JSON.stringify(items, null, 2);
  } catch (error) {
    output.textContent = '목록을 불러오지 못했습니다.';
    console.log(error.message);
  }
}
readRecent();
// limit을 1 또는 5로 바꾼다. 글이 적으면 limit보다 적게 나온다.
