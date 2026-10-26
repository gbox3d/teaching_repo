// ex04 저장 칸 localStorage: setItem 으로 적은 글자는 새로고침해도 남는다
// 저장하기를 누르기 전·후에 새로고침하며 Console 1·2번을 비교한다. Application 탭의 ex04-memo 도 본다.

const saveButton = document.querySelector('#save-button');   // index.html 의 "ex04 가 쓰는 자리" 에 있는 버튼

let memo = '(처음 값)';                                   // 1. 변수: 페이지를 열 때마다 이 줄부터 다시 시작한다
console.log('1. 변수 memo :', memo);
console.log('2. 저장 칸 ex04-memo :', localStorage.getItem('ex04-memo'));   // 2. 저장 칸에서 꺼낸다. 적은 적이 없으면 null

saveButton.addEventListener('click', function () {
    memo = '안녕하세요';                                   // 1. 변수에 담는다
    localStorage.setItem('ex04-memo', '안녕하세요');        // 2. 저장 칸에 적는다(키, 값)
    console.log('눌렀다 — 1. 변수 :', memo, '/ 2. 저장 칸 :', localStorage.getItem('ex04-memo'));
});
