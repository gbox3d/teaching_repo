const notice = document.querySelector('#notice');
const connection = document.querySelector('#connection');
const brightness = document.querySelector('#brightness');
const temperature = document.querySelector('#temperature');
let reading = false;

function showState(state) {
  document.querySelector('#room-temperature').textContent = state.environment.temperature.toFixed(1) + ' °C';
  document.querySelector('#light-status').textContent = state.light.on ? '켜짐' : '꺼짐';
  document.querySelector('#brightness-status').textContent = state.light.brightness + '%';
  document.querySelector('#fan-status').textContent = state.fan.on ? '작동 중' : '정지';
  if (document.activeElement !== brightness) {
    brightness.value = state.light.brightness;
    document.querySelector('#brightness-value').textContent = state.light.brightness + '%';
  }
  if (document.activeElement !== temperature) {
    temperature.value = state.environment.temperature;
    document.querySelector('#temperature-value').textContent = state.environment.temperature.toFixed(1) + ' °C';
  }
  document.querySelector('#light-beam').style.opacity = state.light.on ? state.light.brightness / 100 : 0;
  document.querySelector('#shade').classList.toggle('lit', state.light.on && state.light.brightness > 0);
  document.querySelector('#fan-blades').classList.toggle('running', state.fan.on);
  document.querySelector('#room').setAttribute('aria-label', '가상 거실: 전등 ' + (state.light.on ? '켜짐' : '꺼짐') + ', 선풍기 ' + (state.fan.on ? '작동 중' : '정지'));
  const log = document.querySelector('#request-log');
  log.replaceChildren();
  if (state.log.length === 0) {
    const li = document.createElement('li');
    li.textContent = '제어 요청 없음';
    log.append(li);
  }
  for (const entry of state.log) {
    const li = document.createElement('li');
    const time = new Date(entry.time).toLocaleTimeString('ko-KR', { hour12: false });
    li.textContent = time + '  ' + entry.status + '  ' + entry.method + ' ' + entry.path + '  ' + (entry.body ? JSON.stringify(entry.body) : '요청 실패');
    log.append(li);
  }
}

async function readState() {
  if (reading) return;
  reading = true;
  try {
    const response = await fetch('/api/state');
    if (!response.ok) throw new Error('상태 조회에 실패했습니다.');
    showState(await response.json());
    connection.textContent = '연결됨';
    document.querySelector('#connection-dot').classList.add('connected');
    if (notice.textContent === '상태 조회 중') notice.textContent = '제어 준비 완료';
  } catch {
    connection.textContent = '연결 끊김';
    document.querySelector('#connection-dot').classList.remove('connected');
    notice.textContent = 'Node 서버가 실행 중인지 확인하세요.';
  } finally { reading = false; }
}

async function change(path, values) {
  const buttons = document.querySelectorAll('button');
  for (const button of buttons) button.disabled = true;
  notice.textContent = '제어 요청 중';
  try {
    const response = await fetch(path, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(values) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error);
    showState(result);
    notice.textContent = '제어 완료 · HTTP ' + response.status;
  } catch (error) { notice.textContent = error.message; }
  finally { for (const button of buttons) button.disabled = false; }
}

document.querySelector('#light-on').addEventListener('click', function () { change('/api/devices/light', { on: true }); });
document.querySelector('#light-off').addEventListener('click', function () { change('/api/devices/light', { on: false }); });
document.querySelector('#fan-on').addEventListener('click', function () { change('/api/devices/fan', { on: true }); });
document.querySelector('#fan-off').addEventListener('click', function () { change('/api/devices/fan', { on: false }); });
brightness.addEventListener('input', function () { document.querySelector('#brightness-value').textContent = brightness.value + '%'; });
temperature.addEventListener('input', function () { document.querySelector('#temperature-value').textContent = Number(temperature.value).toFixed(1) + ' °C'; });
document.querySelector('#brightness-apply').addEventListener('click', function () { change('/api/devices/light', { brightness: Number(brightness.value) }); });
document.querySelector('#temperature-apply').addEventListener('click', function () { change('/api/environment', { temperature: Number(temperature.value) }); });
readState();
setInterval(readState, 1000);
