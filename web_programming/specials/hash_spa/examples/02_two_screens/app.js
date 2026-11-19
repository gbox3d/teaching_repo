const homeCountBox = document.querySelector('#home-count');
const homeCountButton = document.querySelector('#home-count-button');
let homeCount = 0;
homeCountButton.addEventListener('click', function () {
  homeCount++;
  homeCountBox.textContent = `클릭 ${homeCount}회`;
});

const screenButtons = document.querySelectorAll('[data-screen]');
function showScreen(name) {
  const sections = document.querySelectorAll('main > section');
  for (let i = 0; i < sections.length; i++) sections[i].hidden = sections[i].id !== name;
  for (let i = 0; i < screenButtons.length; i++) {
    if (screenButtons[i].dataset.screen === name) screenButtons[i].setAttribute('aria-current', 'page');
    else screenButtons[i].removeAttribute('aria-current');
  }
  const heading = document.querySelector(`#${name} h2`);
  document.title = `${heading.textContent} · 두 화면`;
  heading.focus();
}
for (let i = 0; i < screenButtons.length; i++) {
  screenButtons[i].addEventListener('click', function () { showScreen(screenButtons[i].dataset.screen); });
}
showScreen('home');
