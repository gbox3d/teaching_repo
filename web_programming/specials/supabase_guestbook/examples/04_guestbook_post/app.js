const form = document.querySelector('#write-form');
const fields = document.querySelector('#entry-fields');
const bookInput = document.querySelector('#book');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const loadButton = document.querySelector('#load');
const notice = document.querySelector('#notice');
const responseStatus = document.querySelector('#response-status');
const responseBody = document.querySelector('#response-body');
const messages = document.querySelector('#messages');
const endpoint = `${API_BASE_URL}/rest/v1/guestbook`;
bookInput.value = BOOK_ID;
document.querySelector('#api-address').textContent = endpoint;

async function readMessages(book) {
  if (!/^[a-z0-9_-]{1,40}$/.test(book)) throw new Error('방명록 태그를 확인하세요.');
  const url = new URL(endpoint);
  url.searchParams.set('book_id', `eq.${book}`);
  url.searchParams.set('order', 'id.desc');
  url.searchParams.set('limit', '50');
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error(`GET HTTP ${response.status}`);
  const data = await response.json();
  messages.replaceChildren();
  for (const row of data) {
    const item = document.createElement('li');
    item.textContent = `#${row.id} ${row.name}: ${row.message}`;
    messages.append(item);
  }
  return data;
}

loadButton.addEventListener('click', async function () {
  loadButton.disabled = true;
  fields.disabled = true;
  notice.textContent = '목록 조회 중';
  responseStatus.textContent = '응답 대기';
  responseBody.textContent = '응답 없음';
  try {
    const data = await readMessages(bookInput.value);
    responseStatus.textContent = 'GET HTTP 200';
    responseBody.textContent = JSON.stringify(data, null, 2);
    notice.textContent = `조회 완료: ${data.length}개`;
  } catch (error) {
    notice.textContent = `목록 조회 실패: ${error.message}`;
  } finally {
    loadButton.disabled = false;
    fields.disabled = false;
  }
});

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const book = bookInput.value;
  loadButton.disabled = true;
  fields.disabled = true;
  notice.textContent = '저장 요청 중';
  responseStatus.textContent = '응답 대기';
  responseBody.textContent = '응답 없음';
  try {
    if (!/^[a-z0-9_-]{1,40}$/.test(book)) throw new Error('방명록 태그를 확인하세요.');
    if (!nameInput.value.trim() || !messageInput.value.trim()) throw new Error('별칭과 메시지를 입력하세요.');
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: book, name: nameInput.value, message: messageInput.value })
    });
    responseStatus.textContent = `POST HTTP ${response.status}`;
    if (!response.ok) throw new Error(`POST HTTP ${response.status}`);
    const saved = await response.json();
    responseBody.textContent = JSON.stringify(saved, null, 2);
    notice.textContent = '저장 응답 수신. GET으로 확인 중입니다.';
    const data = await readMessages(book);
    const found = data.some(row => row.id === saved[0]?.id);
    notice.textContent = found ? `저장 확인 완료: 글 #${saved[0].id}` : '현재 목록에서 새 글을 확인하지 못했습니다. 목록을 다시 조회하세요.';
    responseStatus.textContent += ' → GET HTTP 200';
    if (found) messageInput.value = '';
  } catch (error) {
    notice.textContent = `저장 결과 확인 실패: ${error.message} 다시 저장하기 전에 목록을 조회하세요.`;
  } finally {
    loadButton.disabled = false;
    fields.disabled = false;
  }
});
