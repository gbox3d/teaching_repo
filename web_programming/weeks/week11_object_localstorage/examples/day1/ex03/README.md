# ex03 객체를 목록에 표시

`index.html`의 두 목록을 비교한다. 첫 목록은 객체를 문자 자리에 넣어 `[object Object]`로 표시한다. 둘째 목록은 이름·메시지·날짜를 꺼내 표시한다.

필수 수정은 둘째 목록의 `items[i].name`을 `items[i].message`로 바꾸고 새로고침하는 것이다. 표시 필드가 달라지는지 확인한 뒤 되돌린다. 속성 이름을 `nmae`로 잘못 쓰면 `undefined`가 보인다. 목록을 만들고 붙이는 코드는 10주 제공 틀을 이어 쓴다.

스타일은 [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)과 `../../../../../shared/examples.css`다. 교재 폴더 구조를 유지하고 [주차 실행 안내](../../../README.md#준비와-실행)를 따른다.
