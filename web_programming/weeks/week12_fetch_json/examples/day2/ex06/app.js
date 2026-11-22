const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const citySelect = document.querySelector('#city');
const cities = {
  seoul: { name: '서울', latitude: 37.5665, longitude: 126.9780 },
  busan: { name: '부산', latitude: 35.1796, longitude: 129.0756 }
};

async function readWeather() {
  const city = cities[citySelect.value];
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${city.latitude}&longitude=${city.longitude}&current=temperature_2m`;
  button.disabled = true;
  citySelect.disabled = true;
  output.textContent = '조회 중';
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const weather = await response.json();
    output.textContent = `${city.name} ${weather.current.temperature_2m}${weather.current_units.temperature_2m}`;
  } catch (error) {
    output.textContent = `조회 실패 · ${error.message}. 연결을 확인하고 다시 조회하세요.`;
  } finally {
    button.disabled = false;
    citySelect.disabled = false;
  }
}

button.addEventListener('click', readWeather);
