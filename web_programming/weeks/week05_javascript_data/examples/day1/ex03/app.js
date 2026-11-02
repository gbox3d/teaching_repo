// ex03 let · const · var: 버튼마다 자기 변수에 1 을 더해 다시 담는다
// F12 › Console 을 열고 세 버튼을 차례로 누른다.

let a = 0;      // 다시 담을 수 있다
const b = 0;    // 한 번 담으면 다시 담을 수 없다
var c = 0;      // 옛 방식(작년 예제). 다시 담을 수 있는 것은 let 과 같다
console.log('처음 값 :', a, b, c);
document.getElementById('btn-let').addEventListener('click', function () {
    a = a + 1;
    console.log('1. let a =', a);
});
document.getElementById('btn-const').addEventListener('click', function () {
    b = b + 1;  // 여기서 멈춘다 → Console: Assignment to constant variable.
    console.log('2. const b =', b);     // 이 줄은 실행되지 않는다
});
document.getElementById('btn-var').addEventListener('click', function () {
    c = c + 1;
    console.log('3. var c =', c);
});
