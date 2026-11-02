// ex08 바꾸기와 붙이기: textContent 는 자리의 글자를 바꾸고, createElement → append 는 목록에 한 줄을 더 붙인다
// 칸의 글을 바꿔 가며 1번과 2번을 번갈아 누른다. 1번 자리는 늘 한 줄, 2번 목록은 누를 때마다 한 줄씩 는다.

const textInput = document.querySelector('#text');
const btn1 = document.querySelector('#btn1');
const btn2 = document.querySelector('#btn2');
const out1 = document.querySelector('#out1');
const list = document.querySelector('#list');

// 1. 바꾸기 — 같은 자리의 글자를 바꾼다. 앞 글은 지워지고 늘 한 줄이다(6주 ex02)
btn1.addEventListener('click', function () {
    out1.textContent = textInput.value;               // 칸에 지금 적힌 글(ex02)
    console.log('1. 바꿨다 :', textInput.value);
});

// 2. 붙이기 — 새 줄(li)을 만들고, 글자를 넣고, 목록(ul) 맨 뒤에 붙인다. 앞 줄은 그대로 남는다
btn2.addEventListener('click', function () {
    const li = document.createElement('li');         // 새 <li> 를 만든다. 아직 화면에 없다
    li.textContent = textInput.value;                 // 만든 줄에 글자를 넣는다
    list.append(li);                                  // 목록 맨 뒤에 붙인다. 이제 화면에 보인다
    console.log('2. 붙였다 :', textInput.value);
});
