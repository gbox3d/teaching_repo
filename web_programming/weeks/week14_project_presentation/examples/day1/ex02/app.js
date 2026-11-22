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
  const keyInput = document.querySelector('#key');
  const key = keyInput.value.trim();
  keyInput.value = '';

  if (!/^[1-9][0-9]*$/.test(id) || key === '') {
    notice.textContent = '글 ID, 편집 키를 확인하세요.';
    return;
  }
  // 학생 수정 1: 배열 위치가 아닌 서버 ID와 자기 방명록 번호를 지정한다.
  const url = `${API_BASE_URL}/rest/v1/guestbook?id=eq.${encodeURIComponent(id)}&book_id=eq.${encodeURIComponent(BOOK_ID)}`;
  pending = true;
  button.disabled = true;
  result.textContent = '';
  notice.textContent = '요청 중';
  try {
    const response = await fetch(url, {
      // 학생 수정 2: 삭제 메서드를 지정한다.
      method: 'DELETE',
      // 학생 수정 3: 공개 키와 편집 키를 헤더에 넣는다.
      headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': key }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // DELETE 204에는 JSON 본문이 없다.
    // 제공 코드: 같은 URL로 다시 조회해 실제 변경을 확인한다.
    const checked = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
    if (!checked.ok) throw new Error(`재조회 HTTP ${checked.status}`);
    const items = await checked.json();
    if (!Array.isArray(items)) throw new Error('JSON 배열이 아닙니다');
    result.textContent = JSON.stringify(items, null, 2);
    if (items.length !== 0) {
      throw new Error('편집 키와 글 번호를 확인하세요.');
    }
    notice.textContent = '삭제 확인 완료';
  } catch (error) {
    notice.textContent = `확인 실패: ${error.message}. 다시 요청하기 전에 조회하세요.`;
  } finally {
    pending = false;
    button.disabled = false;
  }
});
