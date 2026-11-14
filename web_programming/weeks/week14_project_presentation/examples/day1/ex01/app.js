const items = [{ id: 41, message: '첫 번째 글' }, { id: 73, message: '두 번째 글' }];
document.querySelector('#show').addEventListener('click', function () {
  document.querySelector('#result').textContent = `배열 위치 0, 서버 ID ${items[0].id}`;
});
// 두 객체의 순서를 바꾸어도 각 객체의 id는 그대로다.
