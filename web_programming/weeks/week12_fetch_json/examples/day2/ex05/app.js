const output = document.querySelector('#output');
const drawButton = document.querySelector('#draw-button');
const missingButton = document.querySelector('#missing-button');
const card = document.querySelector('#card');
const cardName = document.querySelector('#card-name');
const cardMeaning = document.querySelector('#card-meaning');

async function readCard(path) {
  const url = `https://tarotapi.dev/api/v1/cards/${path}`;
  drawButton.disabled = true;
  missingButton.disabled = true;
  card.hidden = true;
  output.textContent = '조회 중';
  try {
    const response = await fetch(url, { cache: 'no-store' });
    output.textContent = `HTTP ${response.status} · ok ${response.ok}`;
    if (!response.ok) return;
    const data = await response.json();
    cardName.textContent = data.cards[0].name;
    cardMeaning.textContent = data.cards[0].meaning_up;
    card.hidden = false;
  } catch (error) {
    output.textContent = `요청 실패 · ${error.message}`;
  } finally {
    drawButton.disabled = false;
    missingButton.disabled = false;
  }
}

drawButton.addEventListener('click', function () {
  readCard('random?n=1');
});

missingButton.addEventListener('click', function () {
  readCard('zzmissing');
});
