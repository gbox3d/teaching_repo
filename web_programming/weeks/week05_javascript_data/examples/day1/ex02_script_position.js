// 3. head 에 defer 로 연결한 파일: HTML 을 다 읽은 뒤 실행된다 → document.body 가 있다
console.log('3. defer 로 연결한 파일 :', document.body);

// ex02_script_position.html 의 script 줄에서 defer 를 지우면 1번처럼 null 이 찍히고 순서가 1 → 3 → 2 가 된다.
// web-week05 의 <script src="app.js" defer></script> 도 이 방식이다.
