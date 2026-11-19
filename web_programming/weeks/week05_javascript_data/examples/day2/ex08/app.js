// ex08 function: 정의 · 호출 · return
// Console 에 찍히는 줄과 순서를 본다.

function greetLog(name) {           // 정의: 이름을 붙여 두기만 한다
    console.log('안녕하세요, ' + name + '님!');     // return 이 없다
}
function greet(name) {
    return `안녕하세요, ${name}님!`;               // 만든 문장을 부른 곳으로 돌려준다
}
function neverCalled() {
    console.log('이 줄은 찍히지 않는다');           // 정의만 하고 부르지 않았다
}
const a = greetLog('student01');    // 호출: Console 에 찍히고, a 에는 undefined
const b = greet('student01');       // 호출: Console 에는 없고, b 에 문장이 담긴다
console.log('1. return 없는 함수를 부른 결과 :', a);
console.log('2. return 하는 함수를 부른 결과 :', b);
console.log('3. 같은 함수, 다른 값 :', greet('student02'), '/', greet('student03'));

// 제공 출력 코드: 비교 결과를 화면에서도 확인한다.
document.querySelector('#btn').addEventListener('click', function () {
    document.querySelector('#result').textContent = `1: ${a} / 2: ${b} / 3: ${greet('student02')} / ${greet('student03')}`;
});
