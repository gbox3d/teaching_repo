const yearForm = document.querySelector('#year-form');
const yearInput = document.querySelector('#year');
const yearResult = document.querySelector('#year-result');

yearForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const text = yearInput.value.trim();
  const year = Number(text);
  if (text === '' || isNaN(year)) {
    yearResult.textContent = '입학 연도를 숫자로 적어 주세요.';
    yearInput.focus();
    return;
  }
  const thisYear = new Date().getFullYear();
  const years = thisYear - year + 1;
  yearResult.textContent = `${year}년에 입학했으니 올해 ${years}년차입니다.`;
  yearInput.focus();
});
