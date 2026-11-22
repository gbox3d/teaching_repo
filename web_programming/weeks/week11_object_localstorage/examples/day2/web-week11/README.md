# 11주차 방명록 완성본

강의자 시연과 12주차 시작 자료다. 11주차 실습 30분의 필수 구현 대상은 ex04~ex06이며, 이 폴더 전체를 수업 중 다시 작성하지 않는다.

## 확인할 기능

- 이름·메시지·날짜를 객체 배열로 보관한다.
- `week11-guestbook-items` 키에 JSON 문자열을 저장하고 페이지를 열 때 복원한다.
- 글 하나 삭제와 전체 지우기 후 새로고침해도 결과가 유지된다.

`guestbook.html`을 열어 글을 두 개 남기고 새로고침한다. 한 줄을 삭제한 뒤 다시 새로고침하고, 마지막으로 전체 지우기를 확인한다. [강의자용 따라하기](../../../walkthrough.md)에 시연 순서와 전체 코드가 있다.

저장 값의 JSON 문법이나 필드가 손상되면 안내가 나오며, 전체 지우기는 `week11-guestbook-items` 키만 삭제한다. 이 복구 코드는 제공 기능이며, 기본 예제의 키와 이전 `guestbook` 키는 그대로 남긴다.

브라우저 권한이나 용량 부족으로 저장이 실패하면 안내를 표시하고 입력·기존 목록을 유지한다. 삭제 저장이 실패할 때도 기존 글을 남긴다. 저장 실패 처리 역시 제공 코드다.

강의자 확인: Application에서 이 키만 `broken-json`으로 바꾸고 새로고침한다. 안내 확인 → 전체 지우기 → 이름·메시지 재입력 → 저장 → 새로고침 순서로 복구를 확인한다.

## 파일

| 파일 | 용도 |
|---|---|
| [guestbook.html](guestbook.html) · [guestbook.js](guestbook.js) | 브라우저에 저장하는 방명록 |
| [index.html](index.html) · [app.js](app.js) | 이전 주차의 홈 화면과 버튼 동작 |
| [about.html](about.html) | 예시 자기소개 |
| [styles.css](styles.css) | 홈·내 정보의 스타일 |

방명록은 [W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용하므로 스타일을 읽을 때 인터넷 연결이 필요하다. `styles.css`는 홈·내 정보에서 사용한다. `screenshots/`는 이전 주차 화면 자료다.

## 다음 주 준비

12주 선택 방명록 `web-week12`는 이 시연본에서 출발한다. 로컬 버전은 `guestbook.local.html`·`guestbook.local.js`로 보관하고 HTML의 script 경로도 바꾼다. 서버 목록은 `guestbook.html`·`guestbook.js`로 분리한다. 로컬 데이터를 서버로 옮기거나 지우지 않는다.

저장 값은 같은 브라우저 프로필의 같은 origin(프로토콜·호스트·포트)에서만 보인다. localhost에서 공개 HTTPS 사이트로 옮기면 이름·메시지를 새로 입력해야 한다. 다음 주 API 실행 설정은 별도 제공 패널에서 입력하며 새로고침 후 다시 입력한다.
