const form = document.querySelector('#request-form');
const methodInput = document.querySelector('#method');
const bookInput = document.querySelector('#book');
const idInput = document.querySelector('#id');
const bodyInput = document.querySelector('#body');
const keyInput = document.querySelector('#edit-key');
const sendButton = document.querySelector('#send');
const notice = document.querySelector('#notice');
bookInput.value = BOOK_ID;
document.querySelector('#api-address').textContent = `API 주소: ${API_BASE_URL}`;

document.querySelector('#sample').addEventListener('click', function () {
  if (methodInput.value === 'POST') {
    bodyInput.value = JSON.stringify({ book_id: bookInput.value, name: '연구별칭', message: 'REST 연구 중입니다.' }, null, 2);
  } else if (methodInput.value === 'PATCH') {
    bodyInput.value = JSON.stringify({ message: '수정 내용을 다시 확인합니다.' }, null, 2);
  } else {
    bodyInput.value = '';
    notice.textContent = 'GET·DELETE 요청에는 본문을 보내지 않습니다.';
  }
});

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const method = methodInput.value;
  const editKey = keyInput.value;
  keyInput.value = '';
  sendButton.disabled = true;
  notice.textContent = '요청 중';
  document.querySelector('#request-summary').textContent = '아직 요청을 보내지 않았습니다.';
  document.querySelector('#response-status').textContent = '응답 대기';
  document.querySelector('#response-body').textContent = '';
  document.querySelector('#observation').textContent = '응답을 받은 뒤 결과를 확인하세요.';
  try {
    const request = buildRequest(method, bookInput.value, idInput.value, bodyInput.value, editKey);
    document.querySelector('#request-summary').textContent = `${method} ${request.url}\n헤더 이름: ${Object.keys(request.options.headers).join(', ')}`;
    const response = await fetch(request.url, request.options);
    const text = await response.text();
    document.querySelector('#response-status').textContent = `HTTP ${response.status} ${response.statusText}`;
    document.querySelector('#response-body').textContent = text === '' ? '(본문 없음)' : text;
    document.querySelector('#observation').textContent = describeObservation(method, response.status, text);
    notice.textContent = response.ok ? '응답 수신. 실제 변경은 GET으로 확인하세요.' : '오류 응답 수신. 상태와 본문을 확인하세요.';
  } catch (error) {
    document.querySelector('#response-status').textContent = '응답 확인 실패';
    notice.textContent = `요청 실패: ${error.message}`;
  } finally {
    sendButton.disabled = false;
  }
});
