# ex02 강의자 시연

[index.html](index.html)을 열고 버튼을 누른다. [app.js](app.js)에서 값을 수정한 뒤 저장·새로고침한다. Console은 코드 실행과 오류를 확인하는 보조 도구다.

## 원리와 기대 결과

head의 일반 script는 body를 읽기 전에 실행된다. defer는 HTML을 모두 읽은 뒤 실행한다.

결과 출력은 1: null → 2: body → 3: body다.

## 수정과 비교

head의 app.js 연결에서 defer를 지우면 1: null → 3: null → 2: body다. 확인 뒤 defer를 복원한다. 출력 버튼 연결은 제공 DOMContentLoaded 코드다.

화면 출력과 버튼 연결은 제공 코드다. 학생이 새로 구현하지 않는다. 전체 필수 수정량은 [실습지](../../../lab.md)에 따른다.
