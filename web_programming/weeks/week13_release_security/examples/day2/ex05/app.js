const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
button.addEventListener('click', async function () {
  button.disabled = true;
  output.textContent = '저장 중';
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: BOOK_ID, name: 'student01', message: '버튼 상태 연습입니다.' })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    output.textContent = '저장 완료';
  } catch (error) {
    output.textContent = '저장 결과를 확인하지 못했습니다. 목록에서 확인하세요.';
    console.log(error.message);
  } finally {
    button.disabled = false;
  }
});
// Network의 Slow 3G에서 저장 중 버튼이 비활성화되는지 확인한다.
// 확인 후 No throttling으로 되돌린다.
