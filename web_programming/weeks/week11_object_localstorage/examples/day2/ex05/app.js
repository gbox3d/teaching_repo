const key = 'week11-ex05-items';
const items = [
    { name: '하늘', message: '안녕하세요' },
    { name: '바다', message: '잘 봤습니다' }
];
const storedJson = document.querySelector('#stored-json');
const restoredItems = document.querySelector('#restored-items');
const status = document.querySelector('#status');
document.querySelector('#source-json').textContent = JSON.stringify(items, null, 2);

document.querySelector('#save-button').addEventListener('click', function () {
    try {
        const text = JSON.stringify(items);
        localStorage.setItem(key, text);
        storedJson.textContent = '조회 전';
        restoredItems.replaceChildren();
        status.textContent = 'JSON 저장 완료';
    } catch {
        status.textContent = '저장 실패';
    }
});

document.querySelector('#read-button').addEventListener('click', function () {
    try {
        const text = localStorage.getItem(key);
        storedJson.textContent = text === null ? 'null' : text === '' ? '"" (빈 문자열)' : text;
        status.textContent = text === null ? '저장된 값 없음' : '원문 조회 완료';
    } catch {
        status.textContent = '원문 조회 실패';
    }
});

document.querySelector('#parse-button').addEventListener('click', function () {
    restoredItems.replaceChildren();
    try {
        const text = localStorage.getItem(key);
        if (text === null) {
            storedJson.textContent = 'null';
            status.textContent = '저장된 값 없음';
            return;
        }
        storedJson.textContent = text === '' ? '"" (빈 문자열)' : text;
        const restored = JSON.parse(text);
        if (!Array.isArray(restored) || restored.some(item => item === null || typeof item.name !== 'string' || typeof item.message !== 'string')) {
            status.textContent = '배열과 필드 형식 확인 필요';
            return;
        }
        for (const item of restored) {
            const row = document.createElement('li');
            row.textContent = `이름: ${item.name} / 메시지: ${item.message}`;
            restoredItems.append(row);
        }
        status.textContent = `복원 완료: ${restored.length}개`;
    } catch {
        status.textContent = 'JSON 복원 실패';
    }
});

document.querySelector('#remove-button').addEventListener('click', function () {
    try {
        localStorage.removeItem(key);
        storedJson.textContent = 'null';
        restoredItems.replaceChildren();
        status.textContent = '지우기 완료';
    } catch {
        status.textContent = '지우기 실패';
    }
});
