# 03 세 hash 경로

[화면](index.html)의 링크는 `#home`, `#about`, `#guestbook`이다. 페이지 시작과 `hashchange`에서 같은 `showRoute()`를 호출한다. 방명록 미리 보기는 DOM 입력 보존을 관찰하는 기능이며 서버·localStorage에 저장하지 않는다.

## 학생 수정과 관찰

`location.hash.slice(1) || 'home'`으로 경로를 읽는 부분, section의 `hidden` 조건, `hashchange` 등록을 순서대로 확인한다. 강의자가 미등록 경로 처리와 현재 메뉴·제목·포커스 코드를 시연한다. 미등록 문자열은 DOM 선택자나 HTML 문자열에 직접 넣지 않고 정해진 `not-found` 화면으로 보낸다.

| 주소·조작 | 예상 결과 |
|---|---|
| index.html, 빈 hash | 홈·현재 메뉴 1개·홈 제목 포커스 |
| index.html#about | 내 정보 직접 표시 |
| index.html#guestbook, 새로고침 | 방명록 직접 표시·입력 초기화 |
| index.html#missing | 안내·홈 링크·현재 메뉴 없음 |
| 뒤로·앞으로 | 주소에 해당하는 section 표시 |
| Tab으로 메뉴 선택, Enter | 선택 화면의 제목에 포커스 |

이름과 메시지를 입력한 뒤 홈·내 정보·방명록을 10회 오간다. 입력은 그대로 남고 홈 횟수 증가 한 번은 1만 더한다. 전환 때 Document 요청이 없어야 한다. `innerHTML`로 section을 재생성하지 않으며 이벤트 등록은 표시 함수 밖에 둔다.

## 주소와 파일

`index.html#guestbook`을 루트와 `/내프로젝트/index.html#guestbook` 아래에서 각각 연다. 파일 경로는 서버가, hash는 브라우저 코드가 처리한다. 선택 연구는 입력과 홈 횟수가 새로고침에서 사라지는 이유를 11주 폼 저장과 비교하는 것이다.

`index.html`, `app.js`, `shared/examples.css`를 함께 복사한다. CDN은 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`다. 로컬 실행 명령은 [특강 README](../../README.md)에 있다.
