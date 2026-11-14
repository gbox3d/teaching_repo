const form = document.querySelector('#read-form');
const bookInput = document.querySelector('#book');
const loadButton = document.querySelector('#load');
const notice = document.querySelector('#notice');
const responseStatus = document.querySelector('#response-status');
const responseBody = document.querySelector('#response-body');
const messages = document.querySelector('#messages');
bookInput.value = BOOK_ID;

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  loadButton.disabled = true;
  notice.textContent = '목록 조회 중';
  responseStatus.textContent = '응답 대기';
  responseBody.textContent = '응답 없음';
  messages.replaceChildren();
  try {
    const book = bookInput.value;
    if (!/^[a-z0-9_-]{1,40}$/.test(book)) throw new Error('방명록 태그를 확인하세요.');
    const url = new URL('/rest/v1/guestbook', API_BASE_URL);
    url.searchParams.set('book_id', `eq.${book}`);
    url.searchParams.set('order', 'id.desc');
    url.searchParams.set('limit', '50');
    document.querySelector('#api-address').textContent = url.href;
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    responseStatus.textContent = `HTTP ${response.status}`;
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    responseBody.textContent = JSON.stringify(data, null, 2);
    for (const row of data) {
      const item = document.createElement('li');
      item.textContent = `#${row.id} ${row.name}: ${row.message}`;
      messages.append(item);
    }
    notice.textContent = data.length === 0 ? '조회된 글 없음' : `조회 완료: ${data.length}개`;
  } catch (error) {
    notice.textContent = `목록 조회 실패: ${error.message}`;
  } finally {
    loadButton.disabled = false;
  }
});
