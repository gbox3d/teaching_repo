# ex08 강의자 시연

[index.html](index.html)을 열고 버튼을 누른다. [app.js](app.js)에서 값을 수정한 뒤 저장·새로고침한다. Console은 코드 실행과 오류를 확인하는 보조 도구다.

## 원리와 기대 결과

정의만 한 함수는 실행되지 않는다. 호출 결과는 return 값이며 return이 없으면 undefined다.

화면의 1번은 undefined, 2번은 student01 인사, 3번은 student02와 student03 인사다.

## 수정과 비교

greetLog의 console.log를 return으로 바꾸면 1번도 인사말이 된다. neverCalled()를 부르면 해당 로그가 추가된다. 인사 함수 1곳의 필수 수정은 시작 app.js에서 한다.

화면 출력과 버튼 연결은 제공 코드다. 학생이 새로 구현하지 않는다. 전체 필수 수정량은 [실습지](../../../lab.md)에 따른다.
