const form = document.querySelector('#memo-form');
const titleInput = document.querySelector('#title-input');
const memoInput = document.querySelector('#memo-input');
const notice = document.querySelector('#notice');
const list = document.querySelector('#memos');
const count = document.querySelector('#memo-count');
const clearButton = document.querySelector('#clear-memos');
// 할 일 3: 이 줄을 고쳐 저장된 목록으로 시작한다(저장된 값이 없으면 빈 배열).
let items = [];

function saveList() {
  // 할 일 1: items 전체를 'memo-list' 키에 저장한다.
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].title}: ${items[i].memo}`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '삭제';
    removeButton.addEventListener('click', function () {
      items.splice(i, 1);
      // 할 일 2: 삭제한 뒤 저장한다.
      showList();
    });
    li.append(removeButton);
    list.append(li);
  }
  if (items.length === 0) {
    count.textContent = '저장된 메모가 없습니다.';
  } else {
    count.textContent = `메모 ${items.length}개`;
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const title = titleInput.value.trim();
  const memo = memoInput.value.trim();
  if (title === '' || memo === '') {
    notice.textContent = '제목과 내용을 모두 입력하세요.';
    titleInput.focus();
    return;
  }
  notice.textContent = '';
  items.push({ title: title, memo: memo });
  // 할 일 2: 추가한 뒤 저장한다.
  showList();
  form.reset();
  titleInput.focus();
});

clearButton.addEventListener('click', function () {
  // 할 일 4: 배열을 비우고, 'memo-list' 키 하나만 지우고, 목록을 다시 그린다.
});

showList();
