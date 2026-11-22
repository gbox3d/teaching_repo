// 공용 Supabase API: 로컬 미리보기와 GitHub Pages에서 이 HTTPS 주소를 사용합니다.
// localhost:8000은 화면 주소입니다. API_BASE_URL에는 화면 주소를 넣지 않습니다.
// 공개 키는 파일에 적지 않습니다. 처음 한 번 입력받아 이 브라우저의 localStorage에 저장합니다.
if (localStorage.getItem("API_PUBLIC_KEY") === null) {
  const key = (prompt("공개 키(publishable key)를 입력하세요.") || "").trim();
  if (key !== "") localStorage.setItem("API_PUBLIC_KEY", key);
}
const API_BASE_URL = "https://esoqbcwgzjtwcqszwvin.supabase.co";
const API_PUBLIC_KEY = localStorage.getItem("API_PUBLIC_KEY") || "";
const BOOK_ID = "student01";

// [공개 키 지우기]: 저장한 키를 지우고 새로고침해 다시 입력받습니다.
const keyClearButton = document.querySelector("#key-clear-button");
if (keyClearButton !== null) {
  keyClearButton.addEventListener("click", function () {
    localStorage.removeItem("API_PUBLIC_KEY");
    location.reload();
  });
}
