const textInput = document.querySelector('#text');
const result = document.querySelector('#result');
let items = [];
items.push('student01: 안녕하세요');
items.push('student02: 고맙습니다');
items.push('student03: 반갑습니다');

// 이 출력 함수는 제공 코드다. 배열·push·length·인덱스를 비교한다.
function showValues() {
  result.textContent = '배열: ' + JSON.stringify(items) + '\n'
    + 'length: ' + items.length + '\n'
    + 'items[0]: ' + items[0] + '\n'
    + 'items[2]: ' + items[2] + '\n'
    + 'items[3]: ' + items[3];
  console.log(items);
}
document.querySelector('#add').addEventListener('click', function () {
  items.push(textInput.value);
  showValues();
});
document.querySelector('#reset').addEventListener('click', function () {
  items = [];
  showValues();
});
showValues();
