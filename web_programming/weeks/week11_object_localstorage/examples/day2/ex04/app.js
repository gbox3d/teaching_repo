const key = 'week11-ex04-text';
const memoInput = document.querySelector('#memo');
const result = document.querySelector('#result');
const status = document.querySelector('#status');

document.querySelector('#save-button').addEventListener('click', function () {
    try {
        localStorage.setItem(key, memoInput.value);
        result.textContent = memoInput.value === '' ? '"" (빈 문자열)' : memoInput.value;
        status.textContent = '저장 완료';
    } catch {
        status.textContent = '저장 실패';
    }
});

document.querySelector('#load-button').addEventListener('click', function () {
    try {
        const saved = localStorage.getItem(key);
        if (saved === null) {
            result.textContent = 'null';
            status.textContent = '저장된 값 없음';
        } else {
            memoInput.value = saved;
            result.textContent = saved === '' ? '"" (빈 문자열)' : saved;
            status.textContent = '불러오기 완료';
        }
    } catch {
        status.textContent = '불러오기 실패';
    }
});

document.querySelector('#remove-button').addEventListener('click', function () {
    try {
        localStorage.removeItem(key);
        memoInput.value = '';
        result.textContent = 'null';
        status.textContent = '지우기 완료';
    } catch {
        status.textContent = '지우기 실패';
    }
});
