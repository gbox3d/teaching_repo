# 01 MPA의 실제 HTML 이동

[홈](index.html), [내 정보](about.html), [방명록](guestbook.html)은 서로 다른 문서다. 14주의 기존 세 파일 구조를 축소한 비교본이며 원래 정규 수업 파일은 수정하지 않는다. 홈 카운터와 방명록 미리 보기만 사용한다. 서버 저장은 04에서 연결한다.

## 실행과 관찰

[특강 준비](../../README.md)의 서버에서 `http://localhost:8111/specials/hash_spa/examples/01_mpa/index.html`을 연다. 홈 횟수를 2로 바꾸고 내 정보로 이동한다. Network의 Document 요청이 새로 생기는지 확인한다. 각 HTML 주소를 직접 입력하고 새로고침한다. 뒤로·앞으로로 방문했던 문서가 표시되는지 확인한다.

방명록의 이름·메시지를 입력하고 미리 보기를 누르면 텍스트가 표시된다. `<b>연습</b>`도 HTML 태그로 실행되지 않는다. 별도 저장을 하지 않으며 새로고침 후 입력은 보장되지 않는다. 브라우저 뒤로 가기는 이전 문서를 캐시로 복원할 수 있으므로 뒤로 가기만으로 저장 기능이 있다고 판단하지 않는다.

학생은 세 링크의 파일명과 현재 메뉴 `aria-current`를 확인한다. 강의자는 14주 `index.html`, `about.html`, `guestbook.html`과 대조한다. 선택 연습은 소개 글을 바꾸고 세 파일 직접 주소를 다시 확인하는 것이다.

## 파일

`index.html`은 `home.js`, `guestbook.html`은 `guestbook.js`를 읽는다. 소개에는 동작 JS가 없다. 각 페이지는 동작 파일 하나 이하를 쓴다. 세 HTML은 고정 CDN `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`를 읽는다.
