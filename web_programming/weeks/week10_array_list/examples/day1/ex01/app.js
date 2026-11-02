// ex01 배열: 값 여러 개를 순서대로 담는 상자. 번호는 0 부터 센다
// Console 의 1~6번을 본다. 개수(length)와 마지막 번호는 하나 차이 난다.

let items = [];                             // 1. 빈 배열 — 대괄호 두 개
console.log('1. 빈 배열의 개수 :', items.length);

items.push('student01: 안녕하세요');         // 2. push — 맨 뒤에 하나를 더한다
items.push('student02: 고맙습니다');
items.push('student03: 반갑습니다');
console.log('2. push 세 번 뒤의 개수 :', items.length, items);

console.log('3. 첫 번째 items[0] :', items[0]);     // 번호는 0 부터 센다
console.log('4. 마지막 items[2] :', items[2]);      // 마지막 번호 = 개수 - 1
console.log('5. 없는 번호 items[3] :', items[3]);   // 없는 번호는 undefined. 빨간 줄은 뜨지 않는다

let names = ['student01', 'student02'];     // 6. 처음부터 값을 넣어 만든다 — 대괄호 안에 쉼표로 나눈다
console.log('6. 처음 값을 넣어 만든 배열의 개수 :', names.length, names);
