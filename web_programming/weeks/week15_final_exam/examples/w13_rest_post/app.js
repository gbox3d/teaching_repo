document.querySelector('#form').addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = document.querySelector('#name').value.trim();
  const message = document.querySelector('#message').value.trim();
  // 할 일: 빈 값이면 멈춘다. book_id, name, message를 JSON 본문으로 POST한다.
  // 성공 응답 확인 후 제공된 loadMessages()로 다시 읽는다.
  // 실패하면 입력값을 유지하고 안내한다.
  notice.textContent = 'POST 코드를 작성하세요.';
});
document.querySelector('#reload').addEventListener('click', loadMessages);
loadMessages();
