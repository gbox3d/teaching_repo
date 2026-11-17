const key = 'week11-ex06-entry';
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const storedJson = document.querySelector('#stored-json');
const status = document.querySelector('#status');

document.querySelector('#entry-form').addEventListener('submit', function (event) {
    event.preventDefault();
    try {
        const entry = { name: nameInput.value, message: messageInput.value };
        const text = JSON.stringify(entry);
        localStorage.setItem(key, text);
        storedJson.textContent = text;
        status.textContent = '저장 완료';
    } catch {
        status.textContent = '저장 실패';
    }
});

document.querySelector('#load-button').addEventListener('click', function () {
    try {
        const text = localStorage.getItem(key);
        if (text === null) {
            storedJson.textContent = 'null';
            status.textContent = '저장된 값 없음';
            return;
        }
        storedJson.textContent = text === '' ? '"" (빈 문자열)' : text;
        const entry = JSON.parse(text);
        if (entry === null || Array.isArray(entry) || typeof entry.name !== 'string' || typeof entry.message !== 'string') {
            status.textContent = '이름·메시지 형식 확인 필요';
            return;
        }
        nameInput.value = entry.name;
        messageInput.value = entry.message;
        status.textContent = '폼 복원 완료';
    } catch {
        status.textContent = 'JSON 불러오기 실패';
    }
});

document.querySelector('#remove-button').addEventListener('click', function () {
    try {
        localStorage.removeItem(key);
        nameInput.value = '';
        messageInput.value = '';
        storedJson.textContent = 'null';
        status.textContent = '지우기 완료';
    } catch {
        status.textContent = '지우기 실패';
    }
});
