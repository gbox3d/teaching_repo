// 같은 폴더의 JSON 설정을 읽은 뒤 실습을 시작한다.
let API_BASE_URL;
let API_PUBLIC_KEY;
let BOOK_ID;

async function loadConfig() {
  const status = document.querySelector('#config-status');

  try {
    const response = await fetch('./config.json', { cache: 'no-store' });
    if (response.status === 404) {
      status.textContent = '같은 폴더의 config.example.json을 config.json으로 복사하고 설정값을 입력하세요.';
      return false;
    }
    if (!response.ok) throw new Error();

    const config = await response.json();
    const url = new URL(config.API_BASE_URL);
    const key = config.API_PUBLIC_KEY.trim();
    const bookId = config.BOOK_ID.trim();
    if ((url.protocol !== 'https:' && url.protocol !== 'http:') || !key || !bookId) {
      throw new Error();
    }

    API_BASE_URL = url.href.replace(/\/+$/, '');
    API_PUBLIC_KEY = key;
    BOOK_ID = bookId;
    status.textContent = `내 방명록 · ${BOOK_ID}`;
    return true;
  } catch {
    status.textContent = 'config.json의 JSON 문법, API 주소, 공개 키와 방명록 번호를 확인하세요.';
    return false;
  }
}
