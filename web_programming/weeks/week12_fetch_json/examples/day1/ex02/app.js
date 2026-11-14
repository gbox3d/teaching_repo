const output = document.querySelector('#output');
async function readMessages() {
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    console.log('응답:', response);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    console.log('본문 배열:', items);
    output.textContent = `GET ${response.status} · ${items.length}개`;
  } catch (error) {
    output.textContent = '요청에 실패했습니다. API 주소와 Network 탭을 확인하세요.';
    console.log(error.message);
  }
}
readMessages();
