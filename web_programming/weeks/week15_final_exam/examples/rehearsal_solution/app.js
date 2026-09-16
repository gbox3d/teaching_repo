const form = document.querySelector('#book-form');
const titleInput = document.querySelector('#title');
const notice = document.querySelector('#notice');
const list = document.querySelector('#book-list');
const modeButton = document.querySelector('#mode-button');
const loadStatus = document.querySelector('#load-status');
const recommendList = document.querySelector('#recommend-list');

let books = JSON.parse(localStorage.getItem('final-items')) || [];

function saveList() {
  localStorage.setItem('final-items', JSON.stringify(books));
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < books.length; i++) {
    const row = document.createElement('li');
    row.textContent = `${books[i].title} (${books[i].date})`;
    const removeButton = document.createElement('button');
    removeButton.textContent = '지우기';
    removeButton.addEventListener('click', function () {
      books.splice(i, 1);
      showList();
      saveList();
    });
    row.append(removeButton);
    list.append(row);
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const title = titleInput.value.trim();
  if (title === '') {
    notice.textContent = '제목을 입력하세요';
    titleInput.focus();
    return;
  }
  notice.textContent = '';
  books.push({ title: title, date: new Date().toLocaleDateString() });
  showList();
  saveList();
  form.reset();
  titleInput.focus();
});

modeButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});

async function loadRecommend() {
  try {
    const response = await fetch('data/items.json');
    if (!response.ok) {
      loadStatus.textContent = '불러오지 못했습니다.';
      return;
    }
    const data = await response.json();
    for (let i = 0; i < data.length; i++) {
      const row = document.createElement('li');
      row.textContent = `${data[i].title} — ${data[i].comment}`;
      recommendList.append(row);
    }
    loadStatus.textContent = `추천 ${data.length}권`;
  } catch (error) {
    loadStatus.textContent = '불러오지 못했습니다.';
  }
}

showList();
loadRecommend();
