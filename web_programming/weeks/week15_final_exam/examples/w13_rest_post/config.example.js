// 수업용 방명록 API 설정. BOOK_ID는 배정받은 방명록 번호로 바꾼다.
// 공개 키는 파일에 적지 않는다. 처음 한 번 입력받아 이 브라우저의 localStorage에 저장한다.
if (localStorage.getItem('API_PUBLIC_KEY') === null) {
  const key = (prompt('배부받은 공개 키를 입력하세요.') || '').trim();
  if (key !== '') localStorage.setItem('API_PUBLIC_KEY', key);
}
const API_BASE_URL = 'https://esoqbcwgzjtwcqszwvin.supabase.co';
const API_PUBLIC_KEY = localStorage.getItem('API_PUBLIC_KEY') || '';
const BOOK_ID = 'student01';

// [공개 키 지우기]: 저장한 키를 지우고 새로고침해 다시 입력받는다.
const keyClearButton = document.querySelector('#key-clear-button');
if (keyClearButton !== null) {
  keyClearButton.addEventListener('click', function () {
    localStorage.removeItem('API_PUBLIC_KEY');
    location.reload();
  });
}
