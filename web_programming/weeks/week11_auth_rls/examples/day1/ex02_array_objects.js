// ex02 배열 안의 객체: [i] 로 몇 번째 묶음인지 고르고, 점으로 그 묶음의 값을 고른다
// Console 의 1~5번을 본다. 1·3번 줄 앞의 ▶ 를 눌러 펼쳐 본다.

// 1·2. 10주차처럼 글자를 쌓은 배열 — 한 칸이 글자 한 덩어리다
const texts = [];
texts.push('하늘: 안녕하세요');
texts.push('바다: 잘 봤습니다');
console.log('1. texts :', texts);
console.log('2. texts[0] :', texts[0]);             // 이름만 따로 꺼낼 수 없다

// 3·4·5. 객체를 쌓은 배열 — 한 칸이 이름표 붙은 한 묶음이다
const today = new Date().toLocaleDateString();      // 오늘 날짜를 글자로. 그대로 옮겨 쓰는 한 줄(틀)
const items = [];
items.push({ name: '하늘', message: '안녕하세요', date: today });
items.push({ name: '바다', message: '잘 봤습니다', date: today });
console.log('3. items :', items);
console.log('4. items[0].name :', items[0].name);   // 대괄호로 0번째 묶음, 점으로 그 이름
console.log('5. items[1].date :', items[1].date);   // 1번째 묶음의 날짜
