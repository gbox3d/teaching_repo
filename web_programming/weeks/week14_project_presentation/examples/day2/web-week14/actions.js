let editKey = '';
const editNotice = document.querySelector('#edit-notice');
const editForm = document.querySelector('#edit-form');
const editId = document.querySelector('#edit-id');
const editMessage = document.querySelector('#edit-message');

document.querySelector('#key-button').addEventListener('click', function () {
  const input = document.querySelector('#edit-key');
  editKey = input.value.trim();
  input.value = '';
  editNotice.textContent = editKey === '' ? '편집 키를 입력하세요.' : '편집 키 입력 완료';
});

function createEditButtons(item) {
  const box = document.createElement('div');
  const editButton = document.createElement('button');
  editButton.textContent = '수정';
  editButton.addEventListener('click', function () {
    editId.value = item.id;
    editMessage.value = item.message;
    editMessage.focus();
  });
  const deleteButton = document.createElement('button');
  deleteButton.textContent = '삭제';
  deleteButton.addEventListener('click', function () {
    deleteMessage(item.id, deleteButton);
  });
  box.append(editButton, deleteButton);
  return box;
}

function messageUrl(id) {
  return `${API_BASE_URL}/rest/v1/guestbook?id=eq.${id}&book_id=eq.${encodeURIComponent(BOOK_ID)}`;
}

async function readMessage(id) {
  const response = await fetch(messageUrl(id), { headers: { apikey: API_PUBLIC_KEY } });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
}
