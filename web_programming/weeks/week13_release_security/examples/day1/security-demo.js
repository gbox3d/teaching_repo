const input = document.querySelector('#input');
const output = document.querySelector('#output');
const textButton = document.querySelector('#text-button');
const htmlButton = document.querySelector('#html-button');

input.value = '<b>안녕</b>';

textButton.addEventListener('click', function () {
  output.textContent = input.value;
});

htmlButton.addEventListener('click', function () {
  output.innerHTML = input.value;
});
