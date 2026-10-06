const cardBox = document.querySelector('#doc-list');
const notice = document.querySelector('#notice');

function showCards(items) {
  cardBox.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const title = document.createElement('h3');
    title.textContent = items[i].title;
    const description = document.createElement('p');
    description.textContent = items[i].description;
    const link = document.createElement('a');
    link.href = items[i].link;
    link.textContent = '문서 열기';
    article.append(title, description, link);
    cardBox.append(article);
  }
}

async function loadCards() {
  // 할 일 1~4 를 여기에 쓴다.
}

loadCards();
