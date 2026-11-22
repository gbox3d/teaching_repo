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
async function loadMessages() {
  const request = ++latestRead;
  try {
    const items = await requestList();
    if (request !== latestRead) return false;
    showList(items);
    notice.textContent = items.length ? '목록 확인 완료' : '등록된 글 없음';
    return true;
  } catch {
    if (request === latestRead) notice.textContent = '목록 확인 실패 · 연결과 설정 확인';
    return false;
  }
}

async function requestList() {
  // TODO GET: apiTarget()에 apikey 헤더로 GET한다.
  // response.ok 확인 뒤 JSON 배열을 반환한다.
  throw new Error('GET 코드를 작성하세요.');
}
document.querySelector('#reload').addEventListener('click', loadMessages);
loadMessages();
