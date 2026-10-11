// ex02 new Date().getFullYear(): 오늘 날짜에서 연도만 꺼낸다. 올해 - 입학 연도 + 1 이 몇 년차다
// 칸에 입학 연도를 적고 눌러 보기를 누른다. Console 의 1·2·3번과 화면의 문장을 비교한다.

const yearInput = document.querySelector('#year');
const result = document.querySelector('#result');
const btn = document.querySelector('#btn');

btn.addEventListener('click', function () {
    const year = Number(yearInput.value);                  // 글자를 숫자로 — ex01

    const thisYear = new Date().getFullYear();             // 1. 올해. 2026년에 누르면 2026 (5주차 ex10 3번)
    console.log('1. 올해 :', thisYear);

    console.log('2. 올해 - 입학 연도 :', thisYear - year);    // 2. 입학한 뒤 지난 햇수

    const years = thisYear - year + 1;                     // 3. 입학한 해를 1년차로 센다
    console.log('3. 올해 - 입학 연도 + 1 :', years);
    result.textContent = `${year}년에 입학했으니 올해 ${years}년차입니다.`;
});
