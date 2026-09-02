const checkButton = document.querySelector('#asset-check');
const result = document.querySelector('#result');

checkButton.addEventListener('click', () => {
  result.textContent = '배포 자산 연결: 정상';
});
