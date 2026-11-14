const notice = document.querySelector('#notice');
const result = document.querySelector('#result');

async function changeLight(on) {
  notice.textContent = '전등 제어 중';
  try {
    const response = await fetch('/api/devices/light', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ on: on, brightness: 65 })
    });
    const state = await response.json();
    if (!response.ok) throw new Error(state.error);
    result.textContent = JSON.stringify(state.light, null, 2);
    notice.textContent = '제어 완료 · HTTP ' + response.status;
  } catch (error) { notice.textContent = error.message; }
}

document.querySelector('#on').addEventListener('click', function () { changeLight(true); });
document.querySelector('#off').addEventListener('click', function () { changeLight(false); });
