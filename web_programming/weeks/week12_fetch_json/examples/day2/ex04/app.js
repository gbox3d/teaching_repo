const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const url = 'https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m';

async function readWeather() {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const weather = await response.json();
    output.textContent = `서울 ${weather.current.temperature_2m}${weather.current_units.temperature_2m}`;
  } catch (error) {
    output.textContent = `조회 실패 · ${error.message}`;
  }
}

button.addEventListener('click', readWeather);
