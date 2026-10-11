// ex04 classList: 요소에 class 를 붙이고(add) 떼고(remove) 뒤집는다(toggle)
// 모양은 CSS 의 .on 규칙이 정한다. JS 는 class 이름만 붙였다 뗀다.

const box = document.querySelector('#box');

document.querySelector('#btn-add').addEventListener('click', function () {
    box.classList.add('on');        // 1. 붙인다. 이미 있으면 그대로
});

document.querySelector('#btn-remove').addEventListener('click', function () {
    box.classList.remove('on');     // 2. 뗀다. 없으면 그대로
});

document.querySelector('#btn-toggle').addEventListener('click', function () {
    box.classList.toggle('on');     // 3. 있으면 떼고, 없으면 붙인다
});
