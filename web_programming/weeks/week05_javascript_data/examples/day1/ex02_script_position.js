// 3. head 에 defer 로 연결한 파일: HTML 을 다 읽은 뒤 실행된다 → 찾는다
console.log('3. defer 로 연결한 파일 :', document.getElementById('msg'));
document.getElementById('msg').innerText = '3번(defer 파일)이 p#msg 를 찾아 글자를 바꿨다';

// ex02_script_position.html 의 script 줄에서 defer 를 지우면 1번처럼 null → 빨간 오류가 뜬다.
// my-web 의 <script src="app.js" defer></script> 도 이 방식이다.
