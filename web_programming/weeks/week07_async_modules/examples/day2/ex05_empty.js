// ex05 빈값 검사: 칸이 비었으면 안내하고 return 으로 그 자리에서 멈춘다
// 칸을 비우거나 채워서 남기기를 누른다. Console 의 번호로 어디까지 실행됐는지 보고, 안내 자리와 결과 자리를 본다.

const form = document.querySelector('#form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const last = document.querySelector('#last');

form.addEventListener('submit', function (event) {
    event.preventDefault();                       // ex01
    const name = nameInput.value.trim();          // ex02·ex03: 빈칸만 넣어도 '' 가 된다
    const message = messageInput.value.trim();

    // 1. 이름이 비었으면 안내하고 멈춘다
    if (name === '') {
        notice.textContent = '이름을 입력하세요.';
        console.log('1. 이름이 비었다 → return');
        return;
    }

    // 2. 메시지가 비었으면 안내하고 멈춘다. 1번에서 멈추면 여기까지 오지 않는다
    if (message === '') {
        notice.textContent = '메시지를 입력하세요.';
        console.log('2. 메시지가 비었다 → return');
        return;
    }

    // 3. 두 칸이 다 차 있을 때만 여기까지 온다. 지난 안내를 지우고 결과를 쓴다
    notice.textContent = '';
    last.textContent = `${name}: ${message}`;
    console.log('3. 끝까지 왔다');
});
