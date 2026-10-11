// ex03 클릭 횟수 세기: 횟수를 담는 변수는 함수 밖에 둔다
// 버튼을 여러 번 누르고 화면의 "클릭 N회"와 Console 의 1·2번을 비교한다.

const btn = document.querySelector('#btn');
const countBox = document.querySelector('#count');

let count = 0;                     // 1. 함수 밖: 열 때 한 번만 0 이 된다

btn.addEventListener('click', function () {
    count = count + 1;             // 누를 때마다 1 씩 는다
    countBox.textContent = `클릭 ${count}회`;
    console.log('1. 밖에 둔 count :', count);

    let inside = 0;                // 2. 함수 안: 누를 때마다 다시 0 이 된다
    inside = inside + 1;
    console.log('2. 안에 둔 inside :', inside);
});
