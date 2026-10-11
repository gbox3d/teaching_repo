// ex02 입력 칸의 value: 칸에 "지금" 적혀 있는 글자다. 누를 때 읽어야 그때 적힌 글자가 나온다
// 두 칸에 글자를 넣고 남기기를 누른다. 이름을 바꿔 한 번 더 누른다. 1번과 2번은 같은 칸을 읽는다.

const form = document.querySelector('#form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const out1 = document.querySelector('#out1');
const out2 = document.querySelector('#out2');
const out3 = document.querySelector('#out3');

const atOpen = nameInput.value;              // 1. 열 때 한 번 읽는다 — 그때 칸에 있던 글자(보통 빈 글자)

form.addEventListener('submit', function (event) {
    event.preventDefault();                  // ex01: 다시 열리지 않게 막는다
    const atSubmit = nameInput.value;        // 2. 누를 때마다 다시 읽는다 — 지금 적힌 글자
    const message = messageInput.value;      // 3. textarea 도 value 로 읽는다

    out1.textContent = `1. 열 때 읽은 이름 : ${atOpen}`;
    out2.textContent = `2. 누를 때 읽은 이름 : ${atSubmit}`;
    out3.textContent = `3. 누를 때 읽은 메시지 : ${message}`;
});
