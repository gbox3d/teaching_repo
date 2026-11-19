const fixed = document.querySelector('#fixed');
const list = document.querySelector('#list');
const count = document.querySelector('#count');
let items = ['student01', 'student02', 'student03'];
items.push('student04');

function showLists() {
  fixed.innerHTML = '';
  list.innerHTML = '';
  // 비교 시연: 숫자 3을 쓰면 배열 길이가 달라도 세 번 실행한다.
  for (let i = 0; i < 3; i++) {
    const li = document.createElement('li');
    li.textContent = String(items[i]);
    fixed.append(li);
  }
  // 필수: 배열 길이에 맞춰 다섯 줄로 목록을 만든다.
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
  }
  count.textContent = '배열 ' + items.length + '개 · 목록 ' + list.children.length + '개';
}
document.querySelector('#run').addEventListener('click', showLists);
showLists();
