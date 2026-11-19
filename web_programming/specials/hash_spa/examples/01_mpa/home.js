const homeCountBox = document.querySelector('#home-count');
const homeCountButton = document.querySelector('#home-count-button');
let homeCount = 0;
homeCountButton.addEventListener('click', function () {
  homeCount++;
  homeCountBox.textContent = `클릭 ${homeCount}회`;
});
