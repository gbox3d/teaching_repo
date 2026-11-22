const form = document.querySelector('#request-form');
const idInput = document.querySelector('#id');
const button = document.querySelector('#send');
const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
let pending = false;

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  if (pending) return;
  const id = idInput.value;


  if (!/^[1-9][0-9]*$/.test(id)) {
    notice.textContent = '글 ID를 확인하세요.';
    return;
  }
  // 학생 수정: 배열 위치가 아닌 서버 ID와 자기 방명록 번호를 지정한다.
  const url = `${API_BASE_URL}/rest/v1/guestbook?id=eq.${encodeURIComponent(id)}&book_id=eq.${encodeURIComponent(BOOK_ID)}`;
  pending = true;
  button.disabled = true;
  result.textContent = '';
  notice.textContent = '요청 중';
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const items = await response.json();
    if (!Array.isArray(items)) throw new Error('JSON 배열이 아닙니다');
    result.textContent = JSON.stringify(items, null, 2);
    notice.textContent = items.length === 0 ? '해당 글 없음' : `서버 메시지: ${items[0].message}`;
  } catch (error) {
    notice.textContent = `확인 실패: ${error.message}. 다시 요청하기 전에 조회하세요.`;
  } finally {
    pending = false;
    button.disabled = false;
  }
});
