const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
button.addEventListener('click', async function () {
  button.disabled = true;
  let saved = false;
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: 'student01', message: '저장 후 조회입니다.' })
    });
    if (!response.ok) throw new Error(`POST ${response.status}`);
    saved = true;
    const read = await fetch(`${API_BASE_URL}/rest/v1/guestbook?book_id=eq.${encodeURIComponent(BOOK_ID)}&select=id,name,message,created_at&order=id.desc&limit=50`, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!read.ok) throw new Error(`GET ${read.status}`);
    const items = await read.json();
    output.textContent = JSON.stringify(items, null, 2);
  } catch (error) {
    if (saved) {
      output.textContent = '저장은 완료됐습니다. 목록을 다시 불러오세요.';
    } else {
      output.textContent = '저장 결과를 목록에서 확인하세요.';
    }
    console.log(error.message);
  } finally {
    button.disabled = false;
  }
});
