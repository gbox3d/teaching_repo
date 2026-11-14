const loadButton = document.querySelector('#load');
const notice = document.querySelector('#notice');
const responseStatus = document.querySelector('#response-status');
const responseBody = document.querySelector('#response-body');
const url = `${API_BASE_URL}/rest/v1/about`;
document.querySelector('#api-address').textContent = url;

loadButton.addEventListener('click', async function () {
  loadButton.disabled = true;
  notice.textContent = '접속 확인 중';
  responseStatus.textContent = '응답 대기';
  responseBody.textContent = '응답 없음';
  try {
    const response = await fetch(url, {
      headers: { apikey: API_PUBLIC_KEY }
    });
    responseStatus.textContent = `HTTP ${response.status}`;
    if (!response.ok) {
      if (response.status === 404) throw new Error('강의자에게 about/help API 설치 여부를 확인하세요.');
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    responseBody.textContent = JSON.stringify(data, null, 2);
    notice.textContent = '접속 확인 완료';
  } catch (error) {
    notice.textContent = `접속 확인 실패: ${error.message}`;
  } finally {
    loadButton.disabled = false;
  }
});
