const homeCountBox = document.querySelector('#home-count');
const homeCountButton = document.querySelector('#home-count-button');
let homeCount = 0;
homeCountButton.addEventListener('click', function () {
  homeCount++;
  homeCountBox.textContent = `클릭 ${homeCount}회`;
});
const draftForm = document.querySelector('#guestbook-form');
draftForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = document.querySelector('#name').value.trim();
  const message = document.querySelector('#message').value.trim();
  document.querySelector('#notice').textContent = name && message ? `${name}: ${message}` : '이름과 메시지를 입력하세요.';
});

// 화면을 숨겨도 DOM과 입력은 유지한다. 이벤트 등록은 이 함수 밖에서 한 번만 한다.
function showRoute() {
  const route = location.hash.slice(1) || 'home';
  const known = route === 'home' || route === 'about' || route === 'guestbook';
  const visibleId = known ? route : 'not-found';
  const sections = document.querySelectorAll('main > section');
  for (let i = 0; i < sections.length; i++) sections[i].hidden = sections[i].id !== visibleId;
  const links = document.querySelectorAll('[data-route]');
  for (let i = 0; i < links.length; i++) {
    const current = known && links[i].dataset.route === route;
    links[i].classList.toggle('w3-teal', current);
    if (current) links[i].setAttribute('aria-current', 'page');
    else links[i].removeAttribute('aria-current');
  }
  const heading = document.querySelector(`#${visibleId} h2`);
  document.title = `${heading.textContent} · Hash SPA`;
  heading.focus();
}
window.addEventListener('hashchange', showRoute);
// 직접 hash 진입의 기본 앵커 처리 뒤에도 제목 포커스를 유지한다.
window.addEventListener('load', showRoute, { once: true });
showRoute();
