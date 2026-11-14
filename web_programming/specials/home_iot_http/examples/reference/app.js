const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const threshold = 28;

async function readState() {
  try {
    const response = await fetch('/api/state');
    if (!response.ok) throw new Error('상태를 읽지 못했습니다.');
    const state = await response.json();
    result.textContent = JSON.stringify(state, null, 2);
    notice.textContent = '조회 완료 · HTTP ' + response.status;
  } catch (error) { notice.textContent = error.message; }
}

async function changeLight() {
  try {
    const response = await fetch('/api/devices/light', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: true, brightness: 65 })
    });
    const state = await response.json();
    if (!response.ok) throw new Error(state.error);
    result.textContent = JSON.stringify(state.light, null, 2);
    notice.textContent = '전등 제어 완료';
  } catch (error) { notice.textContent = error.message; }
}

async function controlFan() {
  try {
    const response = await fetch('/api/state');
    if (!response.ok) throw new Error('온도를 읽지 못했습니다.');
    const state = await response.json();
    const changed = await fetch('/api/devices/fan', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: state.environment.temperature >= threshold })
    });
    const updated = await changed.json();
    if (!changed.ok) throw new Error(updated.error);
    result.textContent = JSON.stringify(updated.fan, null, 2);
    notice.textContent = '제어 완료 · 기준 ' + threshold + ' °C';
  } catch (error) { notice.textContent = error.message; }
}

document.querySelector('#read').addEventListener('click', readState);
document.querySelector('#light').addEventListener('click', changeLight);
document.querySelector('#control').addEventListener('click', controlFan);
