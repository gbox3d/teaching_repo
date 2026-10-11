// ex03 새로고침해도 남는 것: 변수는 새로고침하면 처음으로 돌아가고, localStorage 에 저장한 값은 남는다
// 누르고 새로고침한 뒤, 같은 파일을 다른 주소와 시크릿 창으로 열어 2번을 비교한다.

const varBox = document.querySelector('#count-var');
const savedBox = document.querySelector('#count-saved');
const btn = document.querySelector('#btn');

let countVar = 0;                                                       // 1. 변수: 열 때마다 0 에서 시작한다
let countSaved = JSON.parse(localStorage.getItem('ex03-count')) || 0;   // 2. 저장 칸에서 꺼낸다. 처음 여는 주소는 null 이라 || 0 (11주 ex06)
savedBox.textContent = `2. 저장한 수: ${countSaved}`;

btn.addEventListener('click', function () {
    countVar = countVar + 1;
    varBox.textContent = `1. 변수에 담은 수: ${countVar}`;
    console.log('1. 변수 :', countVar);

    countSaved = countSaved + 1;
    localStorage.setItem('ex03-count', JSON.stringify(countSaved));   // 11주 방명록 saveList 와 같은 모양
    savedBox.textContent = `2. 저장한 수: ${countSaved}`;
    console.log('2. 저장 :', countSaved);
});
