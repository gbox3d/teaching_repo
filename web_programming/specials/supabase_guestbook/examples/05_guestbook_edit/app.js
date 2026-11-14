const bookInput = document.querySelector('#book');
const idInput = document.querySelector('#id');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const keyInput = document.querySelector('#edit-key');
const notice = document.querySelector('#notice');
const responseBody = document.querySelector('#response-body');
const list = document.querySelector('#messages');
let busy = false;

bookInput.value = BOOK_ID;
document.querySelector('#api-address').textContent = `API 주소: ${API_BASE_URL}`;

function setBusy(value) {
  busy = value;
  for (const element of document.querySelectorAll('button, input, textarea')) {
    element.disabled = value;
  }
}

async function loadMessages(book) {
  const url = new URL('/rest/v1/guestbook', API_BASE_URL);
  url.searchParams.set('book_id', `eq.${book}`);
  url.searchParams.set('order', 'id.desc');
  url.searchParams.set('limit', '50');
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error(`목록 조회 HTTP ${response.status}`);
  const rows = await response.json();
  list.replaceChildren();
  for (const row of rows) {
    const item = document.createElement('li');
    const text = document.createElement('p');
    text.textContent = `#${row.id} · ${row.name}: ${row.message}`;
    const select = document.createElement('button');
    select.type = 'button';
    select.textContent = `글 ${row.id} 선택`;
    select.disabled = busy;
    select.addEventListener('click', function () {
      bookInput.value = book;
      idInput.value = row.id;
      nameInput.value = row.name;
      messageInput.value = row.message;
      keyInput.value = '';
      notice.textContent = `선택한 글 ID: ${row.id}`;
    });
    item.append(text, select);
    list.append(item);
  }
  if (rows.length === 0) {
    const item = document.createElement('li');
    item.textContent = '등록된 글 없음';
    list.append(item);
  }
}

document.querySelector('#load').addEventListener('click', async function () {
  if (!bookInput.reportValidity()) return;
  const book = bookInput.value;
  setBusy(true);
  notice.textContent = '목록 조회 중';
  try {
    await loadMessages(book);
    notice.textContent = '목록 조회 완료';
  } catch (error) {
    notice.textContent = `목록 조회 실패: ${error.message}`;
  } finally {
    setBusy(false);
  }
});

async function changeMessage(method) {
  if (!bookInput.reportValidity()) return;
  const book = bookInput.value;
  const id = idInput.value;
  if (!/^[1-9][0-9]*$/.test(id)) {
    notice.textContent = '변경할 글 ID를 양의 정수로 입력하세요.';
    return;
  }
  const name = nameInput.value;
  const message = messageInput.value;
  if (method === 'PATCH' && (!name.trim() || !message.trim() || [...name].length > 30 || [...message].length > 500)) {
    notice.textContent = '별칭은 1~30자, 메시지는 1~500자로 입력하세요. 공백만 입력할 수 없습니다.';
    return;
  }
  const editKey = keyInput.value;
  keyInput.value = '';
  if (!editKey) {
    notice.textContent = '해당 방명록의 편집 키를 입력하세요.';
    return;
  }

  const url = new URL('/rest/v1/guestbook', API_BASE_URL);
  url.searchParams.set('book_id', `eq.${book}`);
  url.searchParams.set('id', `eq.${id}`);
  const options = { method, headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey } };
  if (method === 'PATCH') {
    options.headers['Content-Type'] = 'application/json';
    options.headers.Prefer = 'return=representation';
    options.body = JSON.stringify({ name, message });
  }

  let responseReceived = false;
  setBusy(true);
  notice.textContent = `${method} 요청 중`;
  responseBody.textContent = '응답 대기';
  try {
    const response = await fetch(url, options);
    const text = await response.text();
    responseBody.textContent = `HTTP ${response.status}\n${text || '(본문 없음)'}`;
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    responseReceived = true;
    const changed = method === 'PATCH' ? JSON.parse(text) : null;

    // 성공 상태 번호만으로 변경 여부를 판단하지 않고 같은 글을 다시 읽는다.
    const check = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
    if (!check.ok) throw new Error(`재조회 HTTP ${check.status}`);
    const remaining = await check.json();
    let result;
    if (method === 'PATCH') {
      result = changed.length === 1 && remaining.length === 1 && remaining[0].name === name && remaining[0].message === message
        ? '수정 후 GET으로 저장된 값을 확인했습니다.'
        : '수정 결과가 일치하지 않습니다. 글 ID와 해당 방명록의 편집 키를 확인하세요.';
    } else {
      result = remaining.length === 0
        ? 'GET 재조회 결과 해당 글이 없습니다.'
        : '글이 남아 있습니다. 해당 방명록의 편집 키를 확인하세요.';
    }
    await loadMessages(book);
    notice.textContent = result;
  } catch (error) {
    notice.textContent = responseReceived
      ? `변경 요청 응답을 받았지만 결과 확인에 실패했습니다: ${error.message}. 목록을 다시 조회하세요.`
      : `변경 요청 결과를 확인하지 못했습니다: ${error.message}. 재시도 전에 목록을 조회하세요.`;
  } finally {
    setBusy(false);
  }
}

document.querySelector('#patch').addEventListener('click', () => changeMessage('PATCH'));
document.querySelector('#delete').addEventListener('click', () => changeMessage('DELETE'));
