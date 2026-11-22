const button = document.querySelector('#run-button');
const clickButton = document.querySelector('#click-button');
const clickCount = document.querySelector('#click-count');
const output = document.querySelector('#output');
let count = 0;

function wait(ms) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve();
    }, ms);
  });
}

clickButton.addEventListener('click', function () {
  count = count + 1;
  clickCount.textContent = `클릭 ${count}회`;
});

button.addEventListener('click', async function () {
  button.disabled = true;
  output.textContent = '1. 시작\n';

  await wait(1000);
  output.textContent += '2. 1초 지남\n';

  await wait(1000);
  output.textContent += '3. 2초 지남\n';

  button.disabled = false;
});
