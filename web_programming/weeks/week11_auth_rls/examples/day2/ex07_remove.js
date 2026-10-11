// ex07 removeItem: 저장 칸에서 키 하나를 지운다. 배열 변수와 저장 칸은 따로다
// Console 1~3번과 Application 탭(ex07-list · ex07-other)을 본다.

let items = ['하늘', '바다'];
localStorage.setItem('ex07-list', JSON.stringify(items));      // 저장해 둔다(ex04 · ex05)
localStorage.setItem('ex07-other', '다른 키');

// 1. 배열만 비운다 — 저장 칸은 그대로다
items = [];
console.log('1. items = [] 뒤 :', items.length, '개 / 저장 칸 :', localStorage.getItem('ex07-list'));

// 2. 저장 칸의 키를 지운다 — 이제 꺼내면 null 이다
localStorage.removeItem('ex07-list');
console.log('2. removeItem 뒤 :', items.length, '개 / 저장 칸 :', localStorage.getItem('ex07-list'));

// 3. 지운 키는 ex07-list 하나다. 다른 키는 남는다
console.log('3. ex07-other :', localStorage.getItem('ex07-other'));
