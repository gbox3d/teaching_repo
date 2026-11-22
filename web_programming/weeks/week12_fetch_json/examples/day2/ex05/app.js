const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const latitudeSelect = document.querySelector('#latitude');

async function readWeather() {
  const latitude = latitudeSelect.value;
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=126.9780&current=temperature_2m`;
  try {
    const response = await fetch(url);
    const weather = await response.json();
    const status = `HTTP ${response.status} · ok ${response.ok}`;
    if (response.ok) {
      output.textContent = `${status} · 서울 ${weather.current.temperature_2m}${weather.current_units.temperature_2m}`;
    } else {
      output.textContent = `${status} · ${weather.reason}`;
    }
  } catch (error) {
    output.textContent = `요청 실패 · ${error.message}`;
  }
}

button.addEventListener('click', readWeather);
