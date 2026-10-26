const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');

function clearNotice() {
  notice.textContent = '';
}

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }

  clearNotice();
  last.textContent = `${name}: ${message}`;
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
