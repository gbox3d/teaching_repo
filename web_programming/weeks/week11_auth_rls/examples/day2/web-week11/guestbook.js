const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
let items = JSON.parse(localStorage.getItem('guestbook')) || [];

function saveList() {
  localStorage.setItem('guestbook', JSON.stringify(items));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      saveList();
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '아직 남긴 글이 없습니다.';
  } else {
    count.textContent = `${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();
  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    nameInput.focus();
    return;
  }
  notice.textContent = '';
  const today = new Date().toLocaleDateString();
  items.push({ name: name, message: message, date: today });
  saveList();
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  items = [];
  localStorage.removeItem('guestbook');
  showList();
});

showList();
