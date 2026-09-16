const form = document.querySelector('#book-form');
const titleInput = document.querySelector('#title');
const notice = document.querySelector('#notice');
const list = document.querySelector('#book-list');
const modeButton = document.querySelector('#mode-button');
const loadStatus = document.querySelector('#load-status');
const recommendList = document.querySelector('#recommend-list');

// TODO 3: 페이지를 열 때 'final-items'에 저장해 둔 목록을 복원한다.
let books = [];

function saveList() {
  // TODO 3: books를 'final-items' 키로 localStorage에 저장한다.
}

function showList() {
  list.innerHTML = '';
  for (let i = 0; i < books.length; i++) {
    const row = document.createElement('li');
    row.textContent = `${books[i].title} (${books[i].date})`;
    // TODO 2: 이 줄을 지우는 [지우기] 버튼을 만들어 row에 붙인다.
    list.append(row);
  }
}

form.addEventListener('submit', function (event) {
  event.preventDefault();
  // TODO 1: 제목이 비었으면 notice에 '제목을 입력하세요'를 쓰고 멈춘다.
  // TODO 1: 비지 않았으면 books에 { title, date }를 넣고 showList()·saveList()를 부른다.
});

modeButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});

async function loadRecommend() {
  // TODO 4: data/items.json을 불러와 recommendList에 li로 그린다.
  // TODO 4: 실패하면 loadStatus에 '불러오지 못했습니다.'를 쓴다.
}

showList();
loadRecommend();
