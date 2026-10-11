// ex05 JSON: 배열·객체를 글자 한 줄로 바꿨다가(JSON.stringify) 다시 되살린다(JSON.parse)
// Console 1~3번과 Application 탭의 두 키(ex05-raw · ex05-json)를 비교한다.

const items = [];
items.push({ name: '하늘', message: '안녕하세요' });
items.push({ name: '바다', message: '잘 봤습니다' });

// 1. 배열을 그대로 저장 칸에 넣으면 — 저장 칸은 글자만 받는다. 내용이 사라진다
localStorage.setItem('ex05-raw', items);                         // setItem 은 ex04
console.log('1. 그대로 넣은 값 :', localStorage.getItem('ex05-raw'));

// 2. JSON.stringify 로 글자 한 줄로 바꿔 넣으면 — 내용이 그대로 남는다
const text = JSON.stringify(items);
localStorage.setItem('ex05-json', text);
console.log('2. JSON.stringify 한 값 :', localStorage.getItem('ex05-json'));

// 3. JSON.parse 로 꺼낸 글자를 다시 배열로 되살린다
const back = JSON.parse(localStorage.getItem('ex05-json'));      // getItem 은 ex04
console.log('3. 되살린 back[0].name :', back[0].name, '/ 개수 :', back.length);

// 4. 주석을 풀면: 1번 글자는 JSON 모양이 아니라서 되살리지 못한다(빨간 줄)
// console.log('4. 1번 값을 되살리면 :', JSON.parse(localStorage.getItem('ex05-raw')));
