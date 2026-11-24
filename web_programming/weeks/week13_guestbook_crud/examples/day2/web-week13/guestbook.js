const actions = document.querySelector('#actions');
const form = document.querySelector('#guestbook-form');
const list = document.querySelector('#list');
const notice = document.querySelector('#notice');
const loadNotice = document.querySelector('#load-notice');
const editInput = document.querySelector('#edit-message');
let endpoint;
let bookUrl;

async function runAction(action, value) {
  if (actions.disabled) return;
  actions.disabled = true;
  try {
    await action(value);
  } finally {
    actions.disabled = false;
  }
}

async function getRows(url) {
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store' });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

// Create
async function submitMessage() {
  const name = document.querySelector('#name').value.trim();
  const message = document.querySelector('#message').value.trim();
  if (!name || !message) {
    notice.textContent = '별칭과 내용을 입력하세요.';
    return;
  }
  notice.textContent = '저장 중';
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { apikey: API_PUBLIC_KEY, 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: JSON.stringify({ book_id: BOOK_ID, name, message })
    });
    if (!response.ok) {
      notice.textContent = `글을 저장하지 못했습니다 (HTTP ${response.status}).`;
      return;
    }
    const saved = await response.json();
    form.reset();
    list.replaceChildren();
    loadNotice.textContent = '목록 보기를 누르세요.';
    notice.textContent = `저장 완료 · 글 번호 ${saved[0].id}`;
  } catch {
    notice.textContent = '저장 결과를 확인할 수 없습니다. 목록 보기로 글을 확인하세요.';
  }
}

function rowButton(label, id, action) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'w3-button w3-border w3-small w3-margin-left';
  button.textContent = label;
  button.setAttribute('aria-label', `글 ${id} ${label}`);
  button.addEventListener('click', function () {
    runAction(action, id);
  });
  return button;
}

// Read
async function loadMessages() {
  loadNotice.textContent = '목록 조회 중';
  try {
    const items = await getRows(bookUrl + '&select=id,name,message&order=id.desc&limit=50');
    list.replaceChildren();
    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      const row = document.createElement('li');
      row.append(`#${item.id} ${item.name} · ${item.message}`);
      row.append(rowButton('수정', item.id, updateMessage), rowButton('삭제', item.id, deleteMessage));
      list.append(row);
    }
    loadNotice.textContent = items.length ? `최근 글 ${items.length}개` : '아직 남긴 글이 없습니다.';
  } catch (error) {
    list.replaceChildren();
    loadNotice.textContent = `목록을 불러오지 못했습니다 (${error.message}). 목록 보기를 다시 누르세요.`;
  }
}

// Update
async function updateMessage(id) {
  const message = editInput.value.trim();
  if (!message) {
    notice.textContent = '수정할 내용을 입력하세요.';
    return;
  }
  const rowUrl = bookUrl + '&id=eq.' + id;
  notice.textContent = '수정 중';
  try {
    const response = await fetch(rowUrl, {
      method: 'PATCH',
      headers: { apikey: API_PUBLIC_KEY, 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: JSON.stringify({ message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const changed = await response.json();
    if (!changed.length) {
      notice.textContent = '수정된 글이 없습니다. 방명록 태그와 글 번호를 확인하세요.';
      return;
    }
    const rows = await getRows(rowUrl);
    if (rows.length === 1 && rows[0].id === id && rows[0].message === message) {
      notice.textContent = `수정 확인 · 글 번호 ${id}`;
      editInput.value = '';
    } else {
      notice.textContent = '같은 글 번호에서 수정한 내용을 확인할 수 없습니다.';
    }
    await loadMessages();
  } catch (error) {
    notice.textContent = `수정 결과를 확인할 수 없습니다 (${error.message}). 목록 보기를 누르세요.`;
  }
}

// Delete
async function deleteMessage(id) {
  if (!window.confirm(`글 ${id}번을 삭제하시겠습니까?`)) return;
  const rowUrl = bookUrl + '&id=eq.' + id;
  notice.textContent = '삭제 중';
  try {
    const response = await fetch(rowUrl, {
      method: 'DELETE', headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const remaining = await getRows(rowUrl);
    notice.textContent = remaining.length
      ? '글이 남아 있습니다. 방명록 태그와 글 번호를 확인하세요.'
      : `삭제 확인 · 글 번호 ${id}`;
    await loadMessages();
  } catch (error) {
    notice.textContent = `삭제 결과를 확인할 수 없습니다 (${error.message}). 목록 보기를 누르세요.`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  runAction(submitMessage);
});
document.querySelector('#reload-button').addEventListener('click', function () {
  runAction(loadMessages);
});

loadConfig().then(function (ready) {
  if (!ready) return;
  endpoint = API_BASE_URL + '/rest/v1/guestbook';
  bookUrl = endpoint + '?book_id=eq.' + encodeURIComponent(BOOK_ID);
  actions.disabled = false;
});
