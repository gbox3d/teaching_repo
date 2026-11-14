const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const threshold = 28; // 이 값을 바꿔 제어 기준을 비교한다.

async function controlFan() {
  notice.textContent = '온도 확인 중';
  try {
    const response = await fetch('/api/state');
    if (!response.ok) throw new Error('온도를 읽지 못했습니다.');
    const state = await response.json();
    const shouldRun = state.environment.temperature >= threshold;
    const changed = await fetch('/api/devices/fan', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: shouldRun })
    });
    const updated = await changed.json();
    if (!changed.ok) throw new Error(updated.error);
    result.textContent = JSON.stringify(updated.fan, null, 2);
    notice.textContent = '제어 완료 · 온도 ' + state.environment.temperature + ' °C · 기준 ' + threshold + ' °C';
  } catch (error) { notice.textContent = error.message; }
}

document.querySelector('#control').addEventListener('click', controlFan);
