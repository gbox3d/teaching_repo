let fruits = ['사과', '바나나', '포도'];
const valueInput = document.querySelector('#value');
const positionInput = document.querySelector('#position');
const arrayOutput = document.querySelector('#array-output');
const lengthOutput = document.querySelector('#length-output');
const returnOutput = document.querySelector('#return-output');
const status = document.querySelector('#status');

function showArray() {
    arrayOutput.textContent = JSON.stringify(fruits, null, 2);
    lengthOutput.textContent = fruits.length;
}

function showResult(result, method) {
    showArray();
    returnOutput.textContent = result === undefined ? 'undefined' : JSON.stringify(result);
    status.textContent = `${method} 실행 완료`;
}

document.querySelector('#push').addEventListener('click', function () {
    const value = valueInput.value.trim();
    if (value === '') {
        returnOutput.textContent = '실행 안 함';
        status.textContent = '추가할 값을 입력하세요.';
        return;
    }
    const result = fruits.push(value);
    showResult(result, 'push');
});

document.querySelector('#unshift').addEventListener('click', function () {
    const value = valueInput.value.trim();
    if (value === '') {
        returnOutput.textContent = '실행 안 함';
        status.textContent = '추가할 값을 입력하세요.';
        return;
    }
    const result = fruits.unshift(value);
    showResult(result, 'unshift');
});

document.querySelector('#pop').addEventListener('click', function () {
    const result = fruits.pop();
    showResult(result, 'pop');
});

document.querySelector('#shift').addEventListener('click', function () {
    const result = fruits.shift();
    showResult(result, 'shift');
});

document.querySelector('#insert').addEventListener('click', function () {
    const value = valueInput.value.trim();
    const position = Number(positionInput.value);
    if (value === '') {
        returnOutput.textContent = '실행 안 함';
        status.textContent = '추가할 값을 입력하세요.';
        return;
    }
    if (positionInput.value === '' || !Number.isInteger(position) || position < 0 || position > fruits.length) {
        returnOutput.textContent = '실행 안 함';
        status.textContent = `삽입 위치는 0~${fruits.length}의 정수로 입력하세요.`;
        return;
    }
    const result = fruits.splice(position, 0, value);
    showResult(result, 'splice 삽입');
});

document.querySelector('#delete').addEventListener('click', function () {
    const position = Number(positionInput.value);
    if (fruits.length === 0) {
        returnOutput.textContent = '실행 안 함';
        status.textContent = '삭제할 항목 없음';
        return;
    }
    if (positionInput.value === '' || !Number.isInteger(position) || position < 0 || position >= fruits.length) {
        returnOutput.textContent = '실행 안 함';
        status.textContent = `삭제 위치는 0~${fruits.length - 1}의 정수로 입력하세요.`;
        return;
    }
    const result = fruits.splice(position, 1);
    showResult(result, 'splice 삭제');
});

document.querySelector('#reset').addEventListener('click', function () {
    fruits = ['사과', '바나나', '포도'];
    valueInput.value = '';
    positionInput.value = '0';
    showArray();
    returnOutput.textContent = '실행 전';
    status.textContent = '초기화 완료';
});

showArray();
