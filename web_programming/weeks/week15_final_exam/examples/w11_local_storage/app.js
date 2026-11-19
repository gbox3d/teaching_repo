const form = document.querySelector('#memo-form');
const titleInput = document.querySelector('#title-input');
const memoInput = document.querySelector('#memo-input');
const notice = document.querySelector('#notice');
const storedJson = document.querySelector('#stored-json');
const key = 'week15-memo-form';

form.addEventListener('submit', function (event) {
  event.preventDefault();
  try {
    const entry = { title: titleInput.value, memo: memoInput.value };
    // TODO SAVE: entry를 JSON 문자열로 바꾸어 key에 저장한다.
    storedJson.textContent = localStorage.getItem(key) ?? 'null';
    notice.textContent = '저장 요청 처리';
  } catch {
    notice.textContent = '저장 실패';
  }
});

document.querySelector('#load-memo').addEventListener('click', function () {
  try {
    const text = localStorage.getItem(key);
    if (text === null) {
      notice.textContent = '저장된 값 없음';
      storedJson.textContent = 'null';
      return;
    }
    // TODO LOAD: text를 객체로 파싱하고 두 입력 칸의 value에 복원한다.
    storedJson.textContent = text;
    notice.textContent = '불러오기 요청 처리';
  } catch {
    notice.textContent = 'JSON 불러오기 실패 · 지우기로 복구';
  }
});

document.querySelector('#clear-memos').addEventListener('click', function () {
  try {
    // TODO REMOVE: key 한 개만 삭제한다.
    form.reset();
    storedJson.textContent = localStorage.getItem(key) ?? 'null';
    notice.textContent = '지우기 요청 처리';
  } catch {
    notice.textContent = '지우기 실패';
  }
});
