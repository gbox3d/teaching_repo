// ex09 화면에 쓰기: 먼저 찾고, 그다음 바꾼다
// index.html 의 "ex09 가 쓰는 자리" 를 찾아 바꾼다. 바꾸기 버튼을 누른다.

const out1 = document.getElementById('out1');   // 작년 예제 방식: id 로 찾는다('#' 없이)
const out2 = document.querySelector('#out2');   // CSS 선택자로 찾는다('#' 은 id — 4주차 ex01)
const out3 = document.querySelector('#out3');
const inp = document.querySelector('#inp');

console.log(out1, out2);                      // 찾은 요소가 찍힌다
console.log(document.querySelector('#out9')); // 없는 id → null. null 에 .textContent 를 쓰면 오류

document.querySelector('#btn').addEventListener('click', function () {
    out1.innerText = '1. innerText 로 바꿨다';
    out2.textContent = '2. textContent 로 바꿨다';  // 글자만 바꿀 때는 innerText 와 결과가 같다
    out3.textContent = '<b>3. 굵게 될까?</b>';      // 태그가 아니라 글자 그대로 보인다
    inp.value = '4. value 로 바꿨다';               // 입력 칸 안의 글자는 value
});
