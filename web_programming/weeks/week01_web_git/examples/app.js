const countButton = document.querySelector('#count-button');
const status = document.querySelector('#status');

let clickCount = 0;

countButton.addEventListener('click', () => {
  clickCount += 1;
  status.textContent = `클릭 횟수: ${clickCount}`;
});

console.info('Web role demo ready');
