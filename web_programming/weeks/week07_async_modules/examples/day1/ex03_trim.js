// ex03 trim(): 글자 앞뒤의 빈칸(스페이스)을 떼어 낸 값을 돌려준다. 가운데 빈칸은 그대로 둔다
// 이름 칸 앞뒤에 빈칸을 넣고 남기기를 누른다. Console 1·2번의 [ ] 안을 비교한다. 빈칸만 넣고도 눌러 본다.

const form = document.querySelector('#form');
const nameInput = document.querySelector('#name');

form.addEventListener('submit', function (event) {
    event.preventDefault();                       // ex01
    const raw = nameInput.value;                  // 1. 적힌 그대로(ex02)
    const trimmed = nameInput.value.trim();       // 2. 앞뒤 빈칸을 뗀 값

    console.log(`1. value 그대로 : [${raw}]`);
    console.log(`2. trim() 한 값 : [${trimmed}]`);
});
