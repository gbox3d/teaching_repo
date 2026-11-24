const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
let latestRead = 0;
function apiTarget(id = '') {
  const filter = id ? '&id=eq.' + encodeURIComponent(id) : '&order=id.desc&limit=50';
  return API_BASE_URL + '/rest/v1/guestbook?book_id=eq.' + encodeURIComponent(BOOK_ID) + filter;
}
function showList(items) {
  list.innerHTML = '';
  for (const item of items) {
    const li = document.createElement('li');
    li.textContent = item.id + ' | ' + item.name + ': ' + item.message;
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'w3-button w3-small w3-border w3-margin-left';
    remove.textContent = '삭제';
    remove.addEventListener('click', function () {
      if (confirm('글 ' + item.id + '번을 삭제하시겠습니까?')) changeMessage('DELETE', String(item.id));
    });
    li.append(remove);
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

async function requestPatch(url, message) {
  // TODO PATCH: url에 message를 JSON 본문으로 보낸다.
  // apikey·Content-Type·Prefer 헤더를 넣고 Response를 반환한다.
  throw new Error('PATCH 코드를 작성하세요.');
}
// 제공 코드: DELETE는 이번 공개 연습 문항의 구현 대상이 아니다.
async function requestDelete(url) {
  return fetch(url, { method: 'DELETE', headers: { apikey: API_PUBLIC_KEY } });
}
let changing = false;
async function changeMessage(method, id) {
  if (changing) return;
  const message = document.querySelector('#message').value.trim();
  if (!/^[1-9][0-9]*$/.test(id) || (method === 'PATCH' && !message)) {
    notice.textContent = '글 번호와 수정 메시지를 확인하세요.';
    return;
  }
  const url = apiTarget(id);
  const patch = document.querySelector('#patch');
  changing = true;
  patch.disabled = true;
  try {
    const before = await readItems(url);
    if (before.length !== 1) throw new Error('대상 글 없음');
    const response = method === 'PATCH'
      ? await requestPatch(url, message)
      : await requestDelete(url);
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
    notice.textContent = '변경 미확인 · 태그·글 번호·목록 확인';
  } finally {
    changing = false;
    patch.disabled = false;
  }
}
document.querySelector('#patch').addEventListener('click', function () { changeMessage('PATCH', document.querySelector('#id').value); });
document.querySelector('#reload').addEventListener('click', loadMessages);
loadMessages();
