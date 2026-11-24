const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const url = 'https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW';

async function readRate() {
  try {
    output.textContent = '조회 중';
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    output.textContent = `1 USD = ${data.rates.KRW} KRW · 기준일 ${data.date}`;
  } catch (error) {
    output.textContent = `조회 실패 · ${error.message}`;
  }
}

button.addEventListener('click', readRate);
