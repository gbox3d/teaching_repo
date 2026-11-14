async function loadMessages() {
  // 할 일: 자기 BOOK_ID의 목록을 GET으로 요청한다.
  // response.ok 확인 → JSON 배열 읽기 → 제공된 showList(items) 호출.
  // 실패하면 notice에 안내하고 다시 누를 수 있게 한다.
  notice.textContent = 'GET 코드를 작성하세요.';
}
document.querySelector('#reload').addEventListener('click', loadMessages);
