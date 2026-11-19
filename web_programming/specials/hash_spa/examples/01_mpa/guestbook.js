const draftForm = document.querySelector('#guestbook-form');
draftForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = document.querySelector('#name').value.trim();
  const message = document.querySelector('#message').value.trim();
  document.querySelector('#notice').textContent = name && message ? `${name}: ${message}` : '이름과 메시지를 입력하세요.';
});
