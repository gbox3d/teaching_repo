const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const threshold = 27; // 이번 실습에서는 27도 이상일 때 작동한다.

async function readState() {
  // TODO 1: ex01의 GET을 참고해 온도와 전등 상태를 result에 표시한다.
  notice.textContent = 'app.js의 TODO 1을 완성하세요.';
}

async function changeLight() {
  // TODO 2: ex02의 PATCH를 참고해 전등을 켜고 밝기를 40으로 정한다.
  notice.textContent = 'app.js의 TODO 2를 완성하세요.';
}

async function controlFan() {
  // TODO 3: ex03을 참고해 threshold 이상이면 선풍기를 켜고, 미만이면 끈다.
  // 응답이 실패한 경우에는 notice에 안내 문장을 표시한다.
  notice.textContent = 'app.js의 TODO 3을 완성하세요.';
}

document.querySelector('#read').addEventListener('click', readState);
document.querySelector('#light').addEventListener('click', changeLight);
document.querySelector('#control').addEventListener('click', controlFan);
