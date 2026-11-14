const notice = document.querySelector('#notice');
const result = document.querySelector('#result');

async function readState() {
  notice.textContent = '상태 조회 중';
  try {
    const response = await fetch('/api/state');
    if (!response.ok) throw new Error('상태를 읽지 못했습니다.');
    const state = await response.json();
    result.textContent = JSON.stringify(state, null, 2);
    notice.textContent = '조회 완료 · 온도 ' + state.environment.temperature + ' °C';
  } catch (error) { notice.textContent = error.message; }
}

document.querySelector('#read').addEventListener('click', readState);
