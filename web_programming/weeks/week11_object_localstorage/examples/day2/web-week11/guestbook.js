const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
const clearButton = document.querySelector('#clear-button');
const storageKey = 'week11-guestbook-items';
let items = [];

// 제공 코드: 저장 값이 손상되어도 화면과 초기화 버튼은 사용할 수 있다.
function loadList() {
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === null) return;
    const restored = JSON.parse(saved);
    if (!Array.isArray(restored)) throw new Error('배열 형식 오류');
    for (let i = 0; i < restored.length; i++) {
      const item = restored[i];
      if (item === null || typeof item.name !== 'string' || typeof item.message !== 'string' || typeof item.date !== 'string') {
        throw new Error('필드 형식 오류');
      }
    }
    items = restored;
  } catch {
    notice.textContent = '저장 값을 불러올 수 없습니다. 전체 지우기를 눌러 이 방명록만 초기화하세요.';
  }
}

function saveList() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(items));
    notice.textContent = '';
    return true;
  } catch {
    notice.textContent = '저장하지 못했습니다. 브라우저 저장 권한이나 여유 공간을 확인하세요.';
    return false;
  }
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      const removed = items.splice(i, 1)[0];
      if (!saveList()) {
        items.splice(i, 0, removed);
        return;
      }
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
  if (!saveList()) {
    items.pop();
    return;
  }
  showList();
  form.reset();
  nameInput.focus();
});

clearButton.addEventListener('click', function () {
  try {
    localStorage.removeItem(storageKey);
    items = [];
    showList();
    notice.textContent = '이 방명록의 저장 값 삭제 완료';
  } catch {
    notice.textContent = '저장 값을 지울 수 없습니다. 브라우저 저장 권한을 확인하세요.';
  }
});

loadList();
showList();
