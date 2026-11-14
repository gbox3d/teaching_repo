const loadButton = document.querySelector('#load');
const notice = document.querySelector('#notice');
const responseStatus = document.querySelector('#response-status');
const responseBody = document.querySelector('#response-body');
const helpList = document.querySelector('#help-list');
const url = `${API_BASE_URL}/rest/v1/help?order=step.asc`;
document.querySelector('#api-address').textContent = url;

loadButton.addEventListener('click', async function () {
  loadButton.disabled = true;
  notice.textContent = '사용법 조회 중';
  responseStatus.textContent = '응답 대기';
  responseBody.textContent = '응답 없음';
  helpList.replaceChildren();
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
    for (const endpoint of data) {
      const item = document.createElement('li');
      item.textContent = `${endpoint.method} ${endpoint.path} — ${endpoint.description}`;
      helpList.append(item);
    }
    notice.textContent = '사용법 조회 완료';
  } catch (error) {
    notice.textContent = `사용법 조회 실패: ${error.message}`;
  } finally {
    loadButton.disabled = false;
  }
});
