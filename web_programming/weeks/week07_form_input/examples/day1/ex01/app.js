const button = document.querySelector('#button');
const result = document.querySelector('#result');
let count = 0;

button.addEventListener('click', function () {
  count += 1;
  result.textContent = `클릭 횟수: ${count}`;
});
