const button = document.querySelector('#run-button');
const output = document.querySelector('#output');

function wait(ms) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve();
    }, ms);
  });
}

button.addEventListener('click', function () {
  button.disabled = true;
  output.textContent = '1. 시작\n';

  wait(1000)
    .then(function () {
      output.textContent += '2. 1초 지남\n';
      return wait(1000);
    })
    .then(function () {
      output.textContent += '3. 2초 지남\n';
      button.disabled = false;
    });
});
