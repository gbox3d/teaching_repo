// ex03 textContent 와 innerHTML: 같은 글을 같은 자리에 넣는다. 다른 것은 단어 하나다
// 입력한 글은 textContent 로 넣는다. innerHTML 은 비울 때(innerHTML = '')만 쓴다.

const input = document.querySelector('#input');
const output = document.querySelector('#output');
const textButton = document.querySelector('#btn-text');
const htmlButton = document.querySelector('#btn-html');
const clearButton = document.querySelector('#btn-clear');

// 1. textContent: 받은 글을 글자 그대로 넣는다. 태그도 글자로 보인다
textButton.addEventListener('click', function () {
    output.textContent = input.value;
    console.log('1. 결과 자리의 글자 :', output.textContent);
});

// 2. innerHTML: 받은 글을 HTML 로 읽어 넣는다. 태그가 진짜 요소가 된다
htmlButton.addEventListener('click', function () {
    output.innerHTML = input.value;
    console.log('2. 결과 자리의 글자 :', output.textContent);
});

// 3. innerHTML = '': 비우기. 입력한 글이 들어가지 않으니 이 자리에는 쓴다(10주차 목록 비우기)
clearButton.addEventListener('click', function () {
    output.innerHTML = '';
    console.log('3. 비운 뒤 글자 수 :', output.textContent.length);
});
