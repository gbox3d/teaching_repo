# 02 두 section 전환

한 HTML에 홈과 내 정보를 둔다. 버튼이 `showScreen(name)`을 실행하고 각 section의 `hidden`만 바꾼다. 주소와 방문 기록은 바뀌지 않으므로 아직 방명록 직접 주소를 제공하지 않는다.

## 실습

[화면](index.html)을 열고 홈 횟수를 2로 올린다. 내 정보·홈 버튼을 눌러 횟수가 유지되는지 확인한다. Network에서 HTML을 다시 받지 않고 주소도 그대로인지 확인한다. 새로고침하면 홈과 클릭 0회로 돌아간다.

학생은 `sections[i].hidden = sections[i].id !== name`의 좌우를 설명하고 표시 대상을 바꾼다. 강의자가 제공한 현재 메뉴 `aria-current`, `document.title`, `heading.focus()`를 확인한다. 화면 제목은 `tabindex="-1"`로 프로그램 포커스를 받으며 일반 Tab 순서를 늘리지 않는다.

이벤트는 `showScreen` 밖에서 한 번 등록한다. 내 정보·홈을 10회 오간 뒤 횟수 증가를 한 번 누르면 1만 증가해야 한다. 선택 연습은 세 번째 버튼 추가이며 주소 연결은 다음 예제에서 한다.

## 파일과 예상 결과

`index.html`, `app.js`를 함께 준비한다. CDN은 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`다. 표시된 section은 항상 하나다. 키보드로 버튼에 이동하여 Enter를 누르면 해당 제목이 포커스를 받는다.
