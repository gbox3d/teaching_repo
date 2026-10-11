// ex06 함수 다시 쓰기: 두 버튼이 같은 일을 하면 그 일을 함수 하나로 묶고 둘 다 부른다

const countBox = document.querySelector('#count');
let count = 0;

function countUp() {                // 같은 일은 한 곳에만 적는다
    count = count + 1;
    countBox.textContent = `클릭 ${count}회`;
}

// 1. A 버튼: 누르면 countUp() 을 부른다
document.querySelector('#btn-a').addEventListener('click', function () {
    console.log('1. A 를 눌렀다');
    countUp();
});

// 2. B 버튼: 같은 함수를 부른다. 셈은 하나로 이어진다
document.querySelector('#btn-b').addEventListener('click', function () {
    console.log('2. B 를 눌렀다');
    countUp();
});
