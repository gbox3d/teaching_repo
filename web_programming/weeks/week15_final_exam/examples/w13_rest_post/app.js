const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
let settingsVersion = 0;
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
async function readItems(url = apiTarget(), publicKey = API_PUBLIC_KEY) {
  const response = await fetch(url, { headers: { apikey: publicKey } });
  if (!response.ok) throw new Error('HTTP ' + response.status);
  return response.json();
}
async function loadMessages() {
  const version = settingsVersion;
  const request = ++latestRead;
  try {
    const items = await readItems();
    if (version !== settingsVersion || request !== latestRead) return false;
    showList(items);
    notice.textContent = items.length ? '목록 확인 완료' : '등록된 글 없음';
    return true;
  } catch {
    if (version === settingsVersion && request === latestRead) notice.textContent = '목록 확인 실패 · 연결과 설정 확인';
    return false;
  }
}

async function requestPost(name, message) {
  // TODO POST: /rest/v1/guestbook에 JSON 본문을 보낸다.
  // apikey·Content-Type·Prefer 헤더, book_id·name·message를 사용한다.
  // response.ok 확인 뒤 JSON 배열을 반환한다.
  throw new Error('POST 코드를 작성하세요.');
}
let saving = false;
document.querySelector('#guestbook-form').addEventListener('submit', async function (event) {
  event.preventDefault();
  if (saving) return;
  const form = event.currentTarget;
  const name = document.querySelector('#name').value.trim();
  const message = document.querySelector('#message').value.trim();
  if (!name || !message) { notice.textContent = '이름과 메시지를 모두 입력하세요.'; return; }
  const version = settingsVersion;
  const button = form.querySelector('button');
  saving = true;
  button.disabled = true;
  try {
    const rows = await requestPost(name, message);
    if (version !== settingsVersion) return;
    if (rows.length !== 1 || !rows[0].id) throw new Error('생성 결과 확인 실패');
    const saved = await readItems(apiTarget(rows[0].id));
    if (version !== settingsVersion) return;
    if (saved.length !== 1 || saved[0].name !== name || saved[0].message !== message) throw new Error('저장값 확인 실패');
    form.reset();
    await loadMessages();
  } catch {
    if (version === settingsVersion) notice.textContent = '저장 미확인 · 입력 유지 · 목록 먼저 확인';
  } finally {
    saving = false;
    button.disabled = false;
  }
});
document.querySelector('#reload').addEventListener('click', loadMessages);
setupApiSettings(async function () {
  settingsVersion += 1;
  list.innerHTML = '';
  await loadMessages();
});
loadMessages();
