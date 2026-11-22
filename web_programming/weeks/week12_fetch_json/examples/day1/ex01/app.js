const button = document.querySelector('#run-button');
const output = document.querySelector('#output');

button.addEventListener('click', function () {
  button.disabled = true;
  output.textContent = '1. 타이머 시작\n';

  const timer = new Promise(function (resolve) {
    setTimeout(function () {
      resolve('3. 타이머 완료');
    }, 1000);
  });

  timer.then(function (message) {
    output.textContent += message;
    button.disabled = false;
  });
  output.textContent += '2. 다음 줄 실행\n';
});
