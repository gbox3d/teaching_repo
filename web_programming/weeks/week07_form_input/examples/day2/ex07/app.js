// ex07 함수 이름만 맡기기: 미리 만든 함수는 이름만 맡긴다. 괄호는 부를 때만 붙인다
// 열면 안내 문구가 보인다. 이름 칸에 한 글자를 치고 안내 자리를 본다. 새로고침하고 이번에는 메시지 칸에 쳐 본다.

const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');

function clearNotice() {                      // 안내를 지우는 일을 함수 하나로 만들어 둔다(6주 ex06)
    notice.textContent = '';
}

// 1. 이름 칸: function () { } 를 맡기고, 그 안에서 괄호를 붙여 부른다(6주 ex06 과 같은 모양)
nameInput.addEventListener('input', function () {
    clearNotice();
});

// 2. 메시지 칸: 함수 이름만 맡긴다. 괄호가 없다 — 칠 때마다 브라우저가 대신 부른다
messageInput.addEventListener('input', clearNotice);

notice.textContent = '안내 문구 — 칸에 글자를 치면 사라진다';   // 열 때 한 번 쓴다(ex06)
