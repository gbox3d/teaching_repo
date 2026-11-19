const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const empty = document.querySelector('#empty');
const count = document.querySelector('#count');
let items = [];

function clearNotice() {
  notice.textContent = '';
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    const button = document.createElement('button');
    button.className = 'w3-button w3-white w3-border';
    button.textContent = '삭제';
    button.addEventListener('click', function () {
      // TODO DELETE: i 위치의 값 한 개를 삭제한다.
      showList();
    });
    li.append(button);
    list.append(li);
  }
  count.textContent = items.length + '개';
  empty.hidden = items.length > 0;
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
  // TODO ADD: 이름: 메시지 문자열을 배열 뒤에 추가한다.
  showList();
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
showList();
