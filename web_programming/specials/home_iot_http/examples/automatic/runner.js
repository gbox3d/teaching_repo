// 제공 실행기: 정책(policy.js), HTTP 요청, 다음 검사 예약을 구분한다.
const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const history = document.querySelector('#history');
const fields = ['mode', 'threshold', 'low', 'high', 'interval'];
let active = false;
let generation = 0;
let timer = null;
let controller = null;
let settings = null;
let failures = 0;
let reads = 0;
let changes = 0;
let sequence = 0;
const observations = [];

function record(status, detail) {
  sequence += 1;
  const entry = { sequence, time: new Date().toISOString(), status, ...detail };
  observations.push(entry);
  if (observations.length > 500) observations.shift();
  const li = document.createElement('li');
  li.textContent = entry.sequence + ' · ' + new Date(entry.time).toLocaleTimeString('ko-KR', { hour12: false }) + ' · ' + status + ' · ' + JSON.stringify(detail);
  history.prepend(li);
  while (history.children.length > 30) history.lastElementChild.remove();
  document.querySelector('#counts').textContent = '조회 ' + reads + '회 · 제어 ' + changes + '회 · 연속 실패 ' + failures + '회';
}

function setActive(value) {
  active = value;
  document.querySelector('#start').disabled = value;
  document.querySelector('#stop').disabled = !value;
  for (const id of fields) document.querySelector('#' + id).disabled = value;
}

function startControl() {
  if (active) return;
  settings = {
    mode: document.querySelector('#mode').value,
    threshold: Number(document.querySelector('#threshold').value),
    low: Number(document.querySelector('#low').value),
    high: Number(document.querySelector('#high').value),
    interval: Number(document.querySelector('#interval').value)
  };
  const temperatures = [settings.threshold, settings.low, settings.high];
  if (temperatures.some(value => !Number.isFinite(value) || value < 10 || value > 40) || settings.low >= settings.high || !Number.isFinite(settings.interval) || settings.interval < 500 || settings.interval > 10000) {
    notice.textContent = '온도는 10~40, 하한은 상한 미만, 조회 간격은 500~10000ms로 입력하세요.';
    return;
  }
  failures = 0;
  generation += 1;
  setActive(true);
  record('시작', settings);
  runCycle(generation);
}

function stopControl() {
  generation += 1;
  clearTimeout(timer);
  timer = null;
  if (controller) controller.abort();
  controller = null;
  setActive(false);
  notice.textContent = '중지됨 · 새 요청 없음';
  record('중지', {});
}

async function runCycle(run) {
  if (!active || run !== generation) return;
  const current = new AbortController();
  controller = current;
  const timeout = setTimeout(function () { current.abort(); }, 3000);
  let delay = settings.interval;
  try {
    notice.textContent = '상태 조회 중';
    const response = await fetch('/api/state', { signal: current.signal });
    if (!response.ok) throw new Error('조회 실패 · HTTP ' + response.status);
    const state = await response.json();
    if (!active || run !== generation) return;
    reads += 1;
    const desired = decideFan(state.environment.temperature, state.fan.on, settings);
    if (typeof desired !== 'boolean') {
      record('정책 미완성', { temperature: state.environment.temperature });
      stopControl();
      notice.textContent = 'policy.js의 TODO를 완성하세요. 반환값은 true 또는 false여야 합니다.';
      return;
    }
    const changed = desired !== state.fan.on;
    if (changed) {
      notice.textContent = '선풍기 제어 중';
      const response = await fetch('/api/devices/fan', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ on: desired }),
        signal: current.signal
      });
      const updated = await response.json();
      if (!response.ok) throw new Error(updated.error || '제어 요청에 실패했습니다.');
      if (!active || run !== generation) return;
      changes += 1;
    }
    failures = 0;
    result.textContent = JSON.stringify({ temperature: state.environment.temperature, before: state.fan.on, after: desired, changed }, null, 2);
    record(changed ? '제어 완료' : '상태 유지', { temperature: state.environment.temperature, fan: desired });
    notice.textContent = '다음 조회 대기 · ' + delay + 'ms';
  } catch (error) {
    if (!active || run !== generation) return;
    failures += 1;
    delay = Math.min(settings.interval * 2 ** Math.min(failures, 4), 10000);
    const reason = current.signal.aborted ? '응답 제한 시간 3초 초과' : error.message;
    record('통신 실패', { reason, retryAfterMs: delay });
    notice.textContent = '재시도 대기 · ' + delay + 'ms';
  } finally {
    clearTimeout(timeout);
    if (controller === current) controller = null;
    if (active && run === generation) timer = setTimeout(function () { runCycle(run); }, delay);
  }
}

document.querySelector('#start').addEventListener('click', startControl);
document.querySelector('#stop').addEventListener('click', stopControl);
document.querySelector('#download').addEventListener('click', function () {
  const url = URL.createObjectURL(new Blob([JSON.stringify(observations, null, 2)], { type: 'application/json' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'iot-observations.json';
  link.click();
  setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
});
window.addEventListener('pagehide', function () {
  generation += 1;
  active = false;
  clearTimeout(timer);
  if (controller) controller.abort();
});
