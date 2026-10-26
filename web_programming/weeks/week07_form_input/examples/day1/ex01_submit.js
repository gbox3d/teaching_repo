// ex01 폼 제출: 폼을 보내면 브라우저는 페이지를 다시 연다. event.preventDefault() 가 그것을 막는다
// 2번 → 1번 순서로 보내기를 누른다. 주소창 끝의 ?, 입력 칸, 결과 자리, Console 을 비교한다.

const form1 = document.querySelector('#form1');
const out1 = document.querySelector('#out1');
const form2 = document.querySelector('#form2');
const out2 = document.querySelector('#out2');

// 1. 막지 않는다 — 두 줄은 실행되지만 곧바로 페이지가 다시 열려 처음 화면으로 돌아간다
form1.addEventListener('submit', function (event) {
    out1.textContent = '1. 제출을 받았다';
    console.log('1. form1 에서 submit');
});

// 2. 막는다 — 첫 줄이 브라우저가 원래 하려던 일(페이지 다시 열기)을 멈춘다
form2.addEventListener('submit', function (event) {
    event.preventDefault();         // event: 방금 일어난 제출의 정보가 담겨 오는 이름
    out2.textContent = '2. 제출을 받았다';
    console.log('2. form2 에서 submit');
});
