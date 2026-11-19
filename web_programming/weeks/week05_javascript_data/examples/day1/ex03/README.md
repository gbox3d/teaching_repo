# ex03 1일차 필수

[index.html](index.html)을 열고 버튼을 누른다. [app.js](app.js)에서 값을 수정한 뒤 저장·새로고침한다. Console은 코드 실행과 오류를 확인하는 보조 도구다.

## 원리와 기대 결과

let은 재대입할 수 있고 const는 재대입할 수 없다. var는 선택 비교다.

기본 0에서 let 버튼 2회는 2다. const 버튼은 값이 0으로 남고 Console에 Assignment to constant variable.이 나온다.

## 수정과 비교

a를 10, b를 20으로 바꾼다. let 버튼 1회는 11이다. const 버튼에서 오류를 보고 const b를 let b로 수정한 뒤 새로고침하면 버튼 1회는 21이다. var는 수정하지 않는다.

화면 출력과 버튼 연결은 제공 코드다. 학생이 새로 구현하지 않는다. 전체 필수 수정량은 [실습지](../../../lab.md)에 따른다.
