const KEY = 'week11-ex07-memo';
const memo = document.querySelector('#memo');
const status = document.querySelector('#status');
const eventResult = document.querySelector('#event-result');

document.querySelector('#save').addEventListener('click', () => {
  try {
    localStorage.setItem(KEY, memo.value);
    status.textContent = '이 탭에서 저장 완료';
  } catch (error) {
    status.textContent = `저장 실패: ${error.name}`;
  }
});

function loadMemo() {
  try {
    const saved = localStorage.getItem(KEY);
    memo.value = saved ?? '';
    status.textContent = saved === null ? '저장된 메모 없음' : '불러오기 완료';
  } catch (error) {
    status.textContent = `불러오기 실패: ${error.name}`;
  }
}

document.querySelector('#load').addEventListener('click', loadMemo);
document.querySelector('#remove').addEventListener('click', () => {
  try {
    localStorage.removeItem(KEY);
    memo.value = '';
    status.textContent = '이 탭에서 삭제 완료';
  } catch (error) {
    status.textContent = `삭제 실패: ${error.name}`;
  }
});

// storage 이벤트는 값을 변경한 탭이 아닌 다른 탭에서 받는다.
window.addEventListener('storage', (event) => {
  if (event.storageArea !== localStorage) return;
  if (event.key !== KEY && event.key !== null) return;
  memo.value = event.newValue ?? '';
  eventResult.textContent = JSON.stringify({
    key: event.key,
    oldValue: event.oldValue,
    newValue: event.newValue
  }, null, 2);
  status.textContent = '다른 탭 변경 반영 완료';
});

loadMemo();
