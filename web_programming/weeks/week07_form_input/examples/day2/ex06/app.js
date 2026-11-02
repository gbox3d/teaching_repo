// ex06 input 이벤트: 칸의 글자가 바뀔 때마다 일어난다. 다시 입력하면 안내 문구를 지우는 데 쓴다
// 열면 안내 문구가 보인다. 두 칸에 한 글자씩 쳐 본다. Backspace 로 지울 때도 Console 을 본다.

const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');

notice.textContent = '안내 문구 — 칸에 글자를 치면 사라진다';   // 열 때 한 번 쓴다(6주 ex02)

// 1. 이름 칸(input): 글자가 바뀔 때마다 안내를 지우고 지금 글자를 찍는다
nameInput.addEventListener('input', function () {
    notice.textContent = '';
    console.log('1. 이름 칸 input :', nameInput.value);
});

// 2. 메시지 칸(textarea): 여러 줄 칸도 같은 'input' 이 일어난다. 하는 일은 1번과 같다
messageInput.addEventListener('input', function () {
    notice.textContent = '';
    console.log('2. 메시지 칸 input :', messageInput.value);
});
