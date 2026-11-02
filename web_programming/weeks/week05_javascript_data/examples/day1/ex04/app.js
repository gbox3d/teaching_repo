// ex04 + 는 두 가지 일을 한다: 더하기와 잇기
// F12 › Console 에 1~5번이 찍힌다. 결과와 종류(typeof)를 본다. 6·7번은 버튼을 누른다.

console.log('1. 1 + 2 →', 1 + 2, typeof (1 + 2));                              // 숫자 + 숫자 → 더한다
console.log("2. '1' + '2' →", '1' + '2', typeof ('1' + '2'));                   // 문자열 + 문자열 → 잇는다
console.log("3. '1' + 2 →", '1' + 2, typeof ('1' + 2));                        // 한쪽만 문자열이어도 잇는다
console.log("4. Number('1') + 2 →", Number('1') + 2, typeof (Number('1') + 2)); // 숫자로 바꾼 뒤 더한다
console.log("5. parseInt('12px') + 1 →", parseInt('12px') + 1, typeof (parseInt('12px') + 1));   // 앞의 숫자만 읽는다(작년 day03)
const num1 = document.getElementById('num1');   // 입력 칸(찾는 법은 ex09)
const num2 = document.getElementById('num2');
document.getElementById('btn-plain').addEventListener('click', function () {
    console.log('6. 그냥 더하기 →', num1.value + num2.value);                    // 입력 칸의 value 는 늘 문자열
});
document.getElementById('btn-number').addEventListener('click', function () {
    console.log('7. Number 로 바꿔 더하기 →', Number(num1.value) + Number(num2.value));   // 숫자로 바꿔서 더한다
});
