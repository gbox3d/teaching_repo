// ex02 클릭할 때 바꾸기: 바꾸는 줄을 addEventListener 안에 넣는다
// 열자마자 1번이 한 번 실행된다. 버튼을 누를 때마다 2번이 실행된다.

const message = document.querySelector('#message');
const btn = document.querySelector('#btn');

// 1. 열 때 바꾸기 — 5주차 ex09 처럼 페이지를 열 때 한 번
message.textContent = '1. 열자마자 바꾼 글자';
console.log('1. 열 때 실행');

// 2. 클릭할 때 바꾸기 — 버튼을 누를 때마다
btn.addEventListener('click', function () {
    message.textContent = '2. 버튼을 눌러 바꾼 글자';
    console.log('2. 클릭할 때 실행');
});
