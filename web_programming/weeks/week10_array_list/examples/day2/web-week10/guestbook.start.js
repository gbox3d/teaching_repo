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
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.className = 'w3-button w3-small w3-border w3-margin-left';
    removeButton.addEventListener('click', function () {
      // TODO 삭제 1: 배열의 i번째 한 개를 뺀다.
      // TODO 삭제 2: 화면을 다시 그린다.
    });
    li.append(removeButton);
    list.append(li);
  }
  count.textContent = `${items.length}개`;
  if (items.length === 0) {
    empty.textContent = '아직 남긴 글이 없습니다.';
  } else {
    empty.textContent = '';
  }
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
  // TODO 등록: 아래 세 줄을 push와 showList 두 줄로 교체한다.
  const li = document.createElement('li');
  li.textContent = `${name}: ${message}`;
  list.append(li);
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
showList();
