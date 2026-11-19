// 제공 코드: 입력한 설정은 현재 페이지의 메모리에서만 사용한다.
let API_BASE_URL = 'http://127.0.0.1:8787';
let API_PUBLIC_KEY = 'classroom-local';
let BOOK_ID = 'student01';

function setupApiSettings(onApply) {
  const form = document.querySelector('#api-settings-form');
  const baseInput = document.querySelector('#api-base-url');
  const keyInput = document.querySelector('#api-public-key');
  const bookInput = document.querySelector('#api-book-id');
  const notice = document.querySelector('#api-settings-notice');
  baseInput.value = API_BASE_URL;
  keyInput.value = API_PUBLIC_KEY;
  bookInput.value = BOOK_ID;

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const baseUrl = baseInput.value.trim().replace(/\/+$/, '');
    const publicKey = keyInput.value.trim();
    const bookId = bookInput.value.trim();
    if (!/^https?:\/\//.test(baseUrl) || publicKey === '' || !/^[a-z0-9_-]{1,40}$/.test(bookId)) {
      notice.textContent = 'API 주소, 공개 키, 방명록 번호를 확인하세요.';
      return;
    }
    API_BASE_URL = baseUrl;
    API_PUBLIC_KEY = publicKey;
    BOOK_ID = bookId;
    notice.textContent = '설정 적용 완료 · 새로고침 후 재입력';
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      await onApply();
    } finally {
      button.disabled = false;
    }
  });
}
