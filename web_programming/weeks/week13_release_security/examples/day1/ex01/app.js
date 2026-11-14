const output = document.querySelector('#output');
const item = { book_id: 'student01', name: 'student01', message: '첫 인사입니다.' };
const body = JSON.stringify(item);
output.textContent = body;
console.log('자바스크립트 객체:', item);
console.log('HTTP 본문에 넣을 JSON 글자:', body);
// message를 바꾸고 새로고침한다. 이 예제는 서버에 저장하지 않는다.
