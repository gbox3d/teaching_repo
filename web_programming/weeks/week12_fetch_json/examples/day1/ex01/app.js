const output = document.querySelector('#output');
const text = '[{"name":"student01","message":"안녕하세요"}]';
const items = JSON.parse(text);
output.textContent = items[0].message;
console.log('JSON 글자:', text);
console.log('자바스크립트 배열:', items);
// text의 큰따옴표 하나를 작은따옴표로 바꾸고 Console을 확인한다.
