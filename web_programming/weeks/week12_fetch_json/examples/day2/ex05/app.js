const output = document.querySelector('#output');
async function readStatus() {
  try {
    const path = '/rest/v1/guestbook';
    // path를 '/rest/v1/missing_table'로 바꿔 실패 응답을 비교한다.
    const response = await fetch(API_BASE_URL + path, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    output.textContent = `Status ${response.status} · ok ${response.ok}`;
    if (!response.ok) return;
    const items = await response.json();
    console.log(items);
  } catch (error) {
    output.textContent = '서버에 연결하지 못했습니다.';
    console.log(error.message);
  }
}
readStatus();
