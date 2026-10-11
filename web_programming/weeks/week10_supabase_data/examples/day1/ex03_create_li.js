// ex03 목록 한 줄 만들기: 만들고(createElement) → 글자를 넣고(textContent) → 붙인다(append)
// 화면의 목록과 Console 1~3번을 비교한다. 붙인 줄만 화면에 보인다.

const list = document.querySelector('#list');    // 빈 <ul id="list"> 를 찾아 둔다(6주 ex01)

// 1. 만들기만 했다 — 어디에도 붙이지 않아 화면에 없다
const li1 = document.createElement('li');
li1.textContent = '1. 만들기만 한 줄';
console.log('1. 만든 li :', li1);

// 2. 만들고 목록에 붙였다 — 화면에 보인다
const li2 = document.createElement('li');
li2.textContent = '2. 만들고 붙인 줄';
list.append(li2);
console.log('2. 붙인 li :', li2);

// 3. 하나 더 붙였다 — append 는 늘 맨 뒤에 붙인다
const li3 = document.createElement('li');
li3.textContent = '3. 나중에 붙인 줄';
list.append(li3);
console.log('3. 목록 :', list);
