const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const buttons = document.querySelectorAll('button');
async function readInfo(path) {
  for (const button of buttons) button.disabled = true;
  notice.textContent = '조회 중';
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    result.textContent = JSON.stringify(await response.json(), null, 2);
    notice.textContent = 'GET ' + response.status;
  } catch (error) {
    notice.textContent = '조회 실패: ' + error.message;
  } finally {
    for (const button of buttons) button.disabled = false;
  }
}
document.querySelector('#about').addEventListener('click', function () { readInfo('/api/about'); });
document.querySelector('#help').addEventListener('click', function () { readInfo('/api/help'); });
