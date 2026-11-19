// ex01 객체와 점 표기: 이름표가 붙은 값 여러 개를 { } 한 묶음에 담는다
// Console 의 1~5번을 본다. 1번 줄 앞의 ▶ 를 눌러 펼쳐 본다.

const item = { name: '하늘', message: '안녕하세요', date: '2026. 11. 11.' };   // 이름표: 값 쌍을 쉼표로 잇는다

console.log('1. item :', item);               // 1. 한 묶음 통째로
console.log('2. item.name :', item.name);     // 2. 점 뒤에 이름표 → 그 값 하나
console.log('3. item.date :', item.date);     // 3. 이름표만 바꾸면 다른 값
console.log('4. item.nmae :', item.nmae);     // 4. 없는 이름표(철자 틀림) → undefined. 빨간 줄은 뜨지 않는다

// 5. 값 자리에 변수를 넣는다. 왼쪽 name 은 이름표, 오른쪽 name 은 바로 위의 변수다
const name = '바다';
const message = '잘 봤습니다';
const item5 = { name: name, message: message, date: '2026. 11. 11.' };
console.log('5. item5.name :', item5.name);

// 제공 화면 코드: 실습에서는 위의 객체 값과 속성 이름을 바꾼다.
const nameInput = document.querySelector('#name');
const result = document.querySelector('#result');
nameInput.value = item.name;
function showResult() {
    result.textContent = `item.name: ${item.name}\nitem.date: ${item.date}\nitem.nmae: ${item.nmae}\nitem5.name: ${item5.name}`;
}
document.querySelector('#apply-button').addEventListener('click', function () {
    item.name = nameInput.value;
    showResult();
});
showResult();
