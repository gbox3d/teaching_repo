const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
async function readAgain() {
  button.disabled = true;
  output.textContent = '불러오는 중';
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    output.textContent = `불러오기 완료 · ${items.length}개`;
  } catch (error) {
    output.textContent = '연결을 확인하고 다시 요청하세요.';
    console.log(error.message);
  } finally {
    button.disabled = false;
  }
}
button.addEventListener('click', readAgain);
// DevTools의 Network를 Offline으로 바꾸고 버튼을 누른다.
// No throttling으로 되돌린 뒤 다시 누른다.
