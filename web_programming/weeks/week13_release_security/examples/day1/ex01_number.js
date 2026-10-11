// ex01 Number() 와 isNaN(): 글자를 숫자로 바꾼다. 숫자로 못 바꾸면 NaN(숫자가 아님)이 된다
// 칸에 2023 · 이천이십삼 · 2023년 · (빈칸) 을 차례로 적고 눌러 보기를 누른다. Console 의 1·2·3번을 비교한다.

const yearInput = document.querySelector('#year');
const result = document.querySelector('#result');
const btn = document.querySelector('#btn');

btn.addEventListener('click', function () {
    const text = yearInput.value;                          // 입력 칸의 값은 숫자를 적어도 글자다(5주차 ex04)
    console.log('1. 글자 + 1 :', text + 1);                 // 1. 글자 뒤에 1 이 이어 붙는다

    const year = Number(text);                             // 2. 글자를 숫자로 바꾼다
    console.log('2. Number(글자) + 1 :', year + 1);

    console.log('3. isNaN(바꾼 값) :', isNaN(year));         // 3. 숫자로 못 바꿨으면(NaN 이면) true
    result.textContent = `숫자로 바꾼 값: ${year}`;
});
