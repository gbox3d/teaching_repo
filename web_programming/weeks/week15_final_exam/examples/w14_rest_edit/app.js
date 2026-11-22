const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
let latestRead = 0;
function apiTarget(id = '') {
  const filter = id ? '&id=eq.' + encodeURIComponent(id) : '&order=id.desc&limit=50';
  return API_BASE_URL + '/rest/v1/guestbook?book_id=eq.' + encodeURIComponent(BOOK_ID) + filter;
}
function showList(items) {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i].id + ' | ' + items[i].name + ': ' + items[i].message;
    list.append(li);
  }
}
async function readItems(url = apiTarget()) {
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error('HTTP ' + response.status);
  return response.json();
}
async function loadMessages() {
  const request = ++latestRead;
  try {
    const items = await readItems();
    if (request !== latestRead) return false;
    showList(items);
    notice.textContent = items.length ? '목록 확인 완료' : '등록된 글 없음';
    return true;
  } catch {
    if (request === latestRead) notice.textContent = '목록 확인 실패 · 연결과 설정 확인';
    return false;
  }
}

async function requestPatch(url, editKey, message) {
  // TODO PATCH: url에 message를 JSON 본문으로 보낸다.
  // apikey·X-Edit-Key·Content-Type·Prefer 헤더를 넣고 Response를 반환한다.
  throw new Error('PATCH 코드를 작성하세요.');
}
// 제공 코드: DELETE는 이번 공개 연습 문항의 구현 대상이 아니다.
async function requestDelete(url, editKey) {
  return fetch(url, { method: 'DELETE', headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey } });
}
let changing = false;
async function changeMessage(method) {
  if (changing) return;
  const id = document.querySelector('#id').value;
  const input = document.querySelector('#key');
  const editKey = input.value.trim();
  const message = document.querySelector('#message').value.trim();
  input.value = '';
  if (!/^[1-9][0-9]*$/.test(id) || !editKey || (method === 'PATCH' && !message)) {
    notice.textContent = 'ID·편집 키·수정 메시지를 확인하세요.';
    return;
  }
  const url = apiTarget(id);
  const patch = document.querySelector('#patch');
  const remove = document.querySelector('#delete');
  changing = true;
  patch.disabled = remove.disabled = true;
  try {
    const before = await readItems(url);
    if (before.length !== 1) throw new Error('대상 글 없음');
    const response = method === 'PATCH'
      ? await requestPatch(url, editKey, message)
      : await requestDelete(url, editKey);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    if (method === 'PATCH') {
      const rows = await response.json();
      if (rows.length !== 1 || rows[0].message !== message) throw new Error('변경된 행 없음');
    }
    const after = await readItems(url);
    const changed = method === 'PATCH' ? after.length === 1 && after[0].message === message : after.length === 0;
    if (!changed) throw new Error('변경 확인 실패');
    await loadMessages();
  } catch {
    notice.textContent = '변경 미확인 · ID·편집 키·목록 확인';
  } finally {
    changing = false;
    patch.disabled = remove.disabled = false;
  }
}
document.querySelector('#patch').addEventListener('click', function () { changeMessage('PATCH'); });
document.querySelector('#delete').addEventListener('click', function () { changeMessage('DELETE'); });
document.querySelector('#reload').addEventListener('click', loadMessages);
loadMessages();
