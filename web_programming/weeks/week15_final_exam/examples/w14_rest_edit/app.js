async function changeMessage(method) {
  const id = document.querySelector('#id').value;
  const input = document.querySelector('#key');
  const editKey = input.value;
  const message = document.querySelector('#message').value.trim();
  input.value = '';
  // 할 일: id와 book_id로 대상을 지정하고 X-Edit-Key 헤더로 요청한다.
  // PATCH: message를 JSON으로 보내고 변경한 행을 확인한다.
  // DELETE: 204에 response.json()을 호출하지 않는다.
  // 두 요청 모두 GET으로 같은 ID를 다시 읽어 실제 변경을 확인한다.
  // 키는 여기의 메모리 변수만 사용하고 저장소나 URL에 넣지 않는다.
  notice.textContent = `${method} 코드를 작성하세요.`;
}
document.querySelector('#patch').addEventListener('click', function () {
  changeMessage('PATCH');
});
document.querySelector('#delete').addEventListener('click', function () {
  changeMessage('DELETE');
});
document.querySelector('#reload').addEventListener('click', loadMessages);
loadMessages();
