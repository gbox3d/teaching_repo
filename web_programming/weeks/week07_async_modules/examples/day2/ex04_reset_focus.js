// ex04 다음 입력 준비: form.reset() 은 폼 안의 칸을 모두 비우고, focus() 는 커서를 그 칸으로 옮긴다
// 두 칸을 채우고 남기기를 누른다. Console 1·2번을 비교하고, 칸이 비었는지와 커서가 어디서 깜박이는지(3번) 본다.

const form = document.querySelector('#form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');

form.addEventListener('submit', function (event) {
    event.preventDefault();                       // ex01

    // 1. 비우기 전에 읽는다 — 아직 칸에 글자가 있다
    console.log(`1. 비우기 전 : [${nameInput.value}] [${messageInput.value}]`);

    form.reset();                                 // 폼 안의 칸을 모두 비운다(메시지 칸도)

    // 2. 비운 뒤에 읽는다 — 두 칸 다 빈 글자다
    console.log(`2. 비운 뒤 : [${nameInput.value}] [${messageInput.value}]`);

    nameInput.focus();                            // 3. 커서를 이름 칸으로 옮긴다. 다음 글을 바로 칠 수 있다
});
