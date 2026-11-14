const bookInput = document.querySelector('#book');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const editPanel = document.querySelector('#edit-panel');
const editName = document.querySelector('#edit-name');
const editMessage = document.querySelector('#edit-message');
const editKeyInput = document.querySelector('#edit-key');
const notice = document.querySelector('#notice');
const list = document.querySelector('#messages');
const listSummary = document.querySelector('#list-summary');
let selected = null;
let busy = false;
bookInput.value = BOOK_ID;

function setBusy(value) {
  busy = value;
  for (const element of document.querySelectorAll('button, input, textarea')) {
    element.disabled = value;
  }
}

function clearSelection() {
  selected = null;
  editPanel.hidden = true;
  editName.value = '';
  editMessage.value = '';
  editKeyInput.value = '';
  document.querySelector('#selection').textContent = '';
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
  listSummary.textContent = `${book} · ${rows.length}개의 글`;
  for (const row of rows) {
    const item = document.createElement('li');
    const heading = document.createElement('strong');
    heading.textContent = `${row.name} · #${row.id}`;
    const message = document.createElement('p');
    message.textContent = row.message;
    message.style.whiteSpace = 'pre-wrap';
    const selectButton = document.createElement('button');
    selectButton.type = 'button';
    selectButton.textContent = '글 수정·삭제';
    selectButton.disabled = busy;
    selectButton.addEventListener('click', function () {
      if (busy) return;
      selected = { book, id: String(row.id) };
      editName.value = row.name;
      editMessage.value = row.message;
      editKeyInput.value = '';
      editPanel.hidden = false;
      document.querySelector('#selection').textContent = `${book} · 글 #${row.id}`;
      notice.textContent = '편집할 글을 선택했습니다.';
      editName.focus();
    });
    item.append(heading, message, selectButton);
    list.append(item);
  }
  if (rows.length === 0) {
    const item = document.createElement('li');
    item.textContent = '아직 글이 없습니다. 첫 글을 남겨 보세요.';
    list.append(item);
  }
}

async function readOne(book, id) {
  const url = new URL('/rest/v1/guestbook', API_BASE_URL);
  url.searchParams.set('book_id', `eq.${book}`);
  url.searchParams.set('id', `eq.${id}`);
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error(`결과 조회 HTTP ${response.status}`);
  return response.json();
}

async function refresh() {
  if (busy || !bookInput.reportValidity()) return;
  const book = bookInput.value;
  clearSelection();
  list.replaceChildren();
  listSummary.textContent = '목록 조회 중';
  setBusy(true);
  notice.textContent = '목록 조회 중';
  try {
    await loadMessages(book);
    notice.textContent = '목록 조회 완료';
  } catch (error) {
    listSummary.textContent = '목록 조회 실패';
    notice.textContent = `목록을 불러오지 못했습니다: ${error.message}`;
  } finally {
    setBusy(false);
  }
}

document.querySelector('#book-form').addEventListener('submit', function (event) {
  event.preventDefault();
  refresh();
});

bookInput.addEventListener('input', function () {
  clearSelection();
  list.replaceChildren();
  listSummary.textContent = '태그 변경 후 조회 대기';
  notice.textContent = '변경한 태그의 목록을 새로고침하세요.';
});

document.querySelector('#write-form').addEventListener('submit', async function (event) {
  event.preventDefault();
  if (busy || !bookInput.reportValidity()) return;
  const book = bookInput.value;
  const name = nameInput.value;
  const message = messageInput.value;
  if (!name.trim() || !message.trim() || [...name].length > 30 || [...message].length > 500) {
    notice.textContent = '별칭은 1~30자, 메시지는 1~500자로 입력하세요. 공백만 입력할 수 없습니다.';
    return;
  }
  clearSelection();
  setBusy(true);
  notice.textContent = '글 등록 중';
  let verified = false;
  try {
    const response = await fetch(`${API_BASE_URL}/rest/v1/guestbook`, {
      method: 'POST',
      headers: {
        apikey: API_PUBLIC_KEY,
        'Content-Type': 'application/json',
        Prefer: 'return=representation'
      },
      body: JSON.stringify({ book_id: book, name, message })
    });
    if (!response.ok) throw new Error(`등록 HTTP ${response.status}`);
    const saved = await response.json();
    if (saved.length !== 1) throw new Error('저장된 글 번호를 확인하지 못했습니다.');
    const rows = await readOne(book, saved[0].id);
    if (rows.length !== 1 || rows[0].name !== name || rows[0].message !== message) {
      throw new Error('등록 후 조회 결과가 일치하지 않습니다.');
    }
    verified = true;
    messageInput.value = '';
    await loadMessages(book);
    notice.textContent = '글 등록 완료';
  } catch (error) {
    notice.textContent = verified
      ? `글은 등록되었지만 목록을 갱신하지 못했습니다: ${error.message}. 목록을 새로고침하세요.`
      : `등록 결과를 확인하지 못했습니다: ${error.message}. 다시 등록하기 전에 목록을 조회하세요.`;
  } finally {
    setBusy(false);
  }
});

async function changeSelected(method) {
  if (busy || !selected) return;
  const { book, id } = selected;
  const name = editName.value;
  const message = editMessage.value;
  if (method === 'PATCH' && (!name.trim() || !message.trim() || [...name].length > 30 || [...message].length > 500)) {
    notice.textContent = '별칭은 1~30자, 메시지는 1~500자로 입력하세요. 공백만 입력할 수 없습니다.';
    return;
  }
  const editKey = editKeyInput.value;
  editKeyInput.value = '';
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
  setBusy(true);
  notice.textContent = method === 'PATCH' ? '글 수정 중' : '글 삭제 중';
  let verified = false;
  try {
    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`변경 HTTP ${response.status}`);
    // DELETE 204에는 JSON 본문이 없다.
    const changed = method === 'PATCH' ? await response.json() : null;
    const rows = await readOne(book, id);
    if (method === 'PATCH') {
      verified = changed.length === 1 && rows.length === 1 && rows[0].name === name && rows[0].message === message;
      if (!verified) throw new Error('수정되지 않았습니다. 글과 해당 방명록의 편집 키를 확인하세요.');
    } else {
      verified = rows.length === 0;
      if (!verified) throw new Error('글이 남아 있습니다. 해당 방명록의 편집 키를 확인하세요.');
    }
    clearSelection();
    await loadMessages(book);
    notice.textContent = method === 'PATCH' ? '글 수정 완료' : '삭제 후 해당 글이 없는 것을 확인했습니다.';
  } catch (error) {
    notice.textContent = verified
      ? `변경은 확인했지만 목록을 갱신하지 못했습니다: ${error.message}. 목록을 새로고침하세요.`
      : `변경 결과 확인 실패: ${error.message}. 재시도 전에 목록을 조회하세요.`;
  } finally {
    setBusy(false);
  }
}

document.querySelector('#edit-form').addEventListener('submit', function (event) {
  event.preventDefault();
  changeSelected('PATCH');
});
document.querySelector('#delete').addEventListener('click', () => changeSelected('DELETE'));
document.querySelector('#cancel-edit').addEventListener('click', function () {
  if (busy) return;
  clearSelection();
  notice.textContent = '편집 취소';
});

refresh();
