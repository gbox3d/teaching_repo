// ex04 누를 때마다 쌓기: 배열에 넣고(push), 화면에 한 줄 붙이고(append), 개수를 쓴다(length)
// 칸의 글을 바꿔 가며 [더하기]를 세 번 누른다. 화면의 줄, "N개", Console 1~3번을 비교한다.

const textInput = document.querySelector('#text');
const addButton = document.querySelector('#add');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
let items = [];

addButton.addEventListener('click', function () {
    const text = textInput.value;               // 칸에 쓴 글(7주차 value)
    items.push(text);                           // 1. 배열에 넣는다(ex01)
    console.log('1. 배열 :', items);
    const li = document.createElement('li');    // 2. 화면에 한 줄 만들어 붙인다(ex03)
    li.textContent = text;
    list.append(li);
    console.log('2. 붙인 줄 :', li);
    count.textContent = `${items.length}개`;    // 3. 개수는 화면의 줄을 세지 않고 배열의 length 로 쓴다
    console.log('3. 개수 :', items.length);
});
