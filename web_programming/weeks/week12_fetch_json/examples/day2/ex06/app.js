const output = document.querySelector('#output');
const button = document.querySelector('#run-button');
const countrySelect = document.querySelector('#country');
const list = document.querySelector('#holidays');

async function readHolidays() {
  const year = new Date().getFullYear();
  const country = countrySelect.value;
  const url = `https://nagerholidays.com/api/v4/Holidays/${country}/${year}`;
  button.disabled = true;
  countrySelect.disabled = true;
  output.textContent = '조회 중';
  list.replaceChildren();

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const holidays = await response.json();
    let count = 0;
    for (let i = 0; i < holidays.length; i++) {
      const holiday = holidays[i];
      if (holiday.nationalHoliday && holiday.holidayTypes.includes('Public')) {
        const item = document.createElement('li');
        item.textContent = `${holiday.date} · ${holiday.name}`;
        list.append(item);
        count++;
      }
    }
    output.textContent = `${year}년 공휴일 ${count}개`;
  } catch (error) {
    output.textContent = `조회 실패 · ${error.message}. 다시 조회하세요.`;
  } finally {
    button.disabled = false;
    countrySelect.disabled = false;
  }
}

button.addEventListener('click', readHolidays);
