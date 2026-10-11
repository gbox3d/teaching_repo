// ex01 HTML 파일과 DOM: 브라우저는 HTML 파일을 읽어 요소 상자(DOM)를 만든다
// 화면, F12 › Elements 탭, 페이지 소스 보기(Ctrl+U, macOS ⌘+Option+U)를 차례로 비교한다.

const message = document.querySelector('#message');   // DOM 에서 id="message" 요소를 찾는다

console.log('1. document :', document);   // 브라우저가 만든 문서 전체
console.log('2. message :', message);     // 그 안의 요소 하나

// 3. DOM 의 글자를 바꾼다. 화면과 Elements 탭은 바뀌고, HTML 파일(페이지 소스)은 그대로다
message.textContent = '3. JavaScript 가 바꾼 글자';
