# 5주차 예제와 제공 코드

각 exNN 폴더는 index.html·app.js·README.md로 구성한다. 화면에는 제목·버튼·입력·결과만 두고 개념과 조작 순서는 각 README에 둔다. 화면 출력과 버튼 연결은 제공 코드이며 Console은 비교·오류 확인에 함께 쓴다.

## 예제 범위

| 예제 | 수업 범위 | 확인 결과 |
|---|---|---|
| [ex01](day1/ex01/README.md) | 실행 순서 시연 | 처음 A·C, 클릭마다 B |
| [ex02](day1/ex02/README.md) | defer 시연 | 기본 1→2→3, defer 제거 시 1→3→2 |
| [ex03](day1/ex03/README.md) | 1일차 필수 a·b 2값, 오류 1건 수정 | 10→11, const 오류 후 let으로 20→21. var는 선택 |
| [ex04](day1/ex04/README.md) | 숫자/문자열 시연 | 1·2는 연결 12와 합 3. parseInt는 선택 |
| [ex05](day1/ex05/README.md) | 1일차 필수 name·hour 2값 | student02·15시 출력 |
| [ex06](day2/ex06/README.md) | 비교 시연 | true/false 결과. ==는 선택 |
| [ex07](day2/ex07/README.md) | if 시연 | 9시와 15시, 조건 순서 차이 |
| [ex08](day2/ex08/README.md) | 함수 시연 | return 없는 결과 undefined와 인사 문자열 |
| [ex09](day2/ex09/README.md) | DOM 시연 | 글자 변경, 태그는 문자로 표시. 다른 DOM 접근법은 선택 |
| [ex10](day2/ex10/README.md) | 날짜 시연·선택 | 페이지를 읽은 순간의 날짜·시각 |
| [시작 app.js](day2/start/README.md) | 2일차 학생 작업 | 함수·조건·출력 각 1곳 수정 |
| [완성 홈](day2/web-week05/index.html) | 강의자 조립본·비교본 | greet·hello가 만든 인사말 |

필수 수정은 [실습지](../lab.md)의 30분 상한에 따른다. 10개 예제를 모두 수정하는 과제는 없다. 이벤트와 출력 지원 코드는 제공하므로 학생이 새로 작성하지 않는다.

## 4주에서 5주로 넘기는 파일

수업 전에 4주 완성본을 새 `web-week05` 폴더에 제공하고 비교 예제를 `ex/` 아래에 복사한다. Node.js 24 이상과 [공용 server.mjs](../../../tools/static-server/server.mjs)도 미리 준비한다. server.mjs는 공용 원본을 배부하며 이 폴더에 중복 보관하지 않는다.

| 파일 | 제공 준비 | 학생 작업 |
|---|---|---|
| [index.html](day2/web-week05/index.html) | 4주 홈에 defer script와 greeting 카드 각 1줄 추가 | 연결과 id 확인 |
| [시작 app.js](day2/start/app.js) | 기존 카운터 JS를 시작 파일로 교체 | 표시한 세 곳 수정 |
| [완성 app.js](day2/web-week05/app.js) | 완성 비교본 | 9·15시 검증 후 현재 시각 식 복원 |
| [about.html](day2/web-week05/about.html) | 4주 그대로 | 메뉴 이동 확인 |
| [guestbook.html](day2/web-week05/guestbook.html) | 4주 정적 폼 그대로 | 미저장 상태 확인 |
| [styles.css](day2/web-week05/styles.css) | 4주 자체 CSS 그대로 | 375/1280px 확인 |
| [profile.png](day2/web-week05/images/profile.png) | 기존 프로필 그림 | 표시 확인 |

방명록은 유효하지 않은 이메일을 브라우저가 거절한다. 유효한 폼은 같은 URL을 GET으로 다시 탐색하며 메시지를 저장하지 않는다. 입력 name 속성이 없으므로 입력값도 전송되지 않는다. 이 주에는 JS 방명록을 구현하지 않는다.

## 6주 인계

완성 폴더의 세 페이지·CSS·그림과 공용 server.mjs를 넘긴다. `#greeting`, `greet(name)`, `hello(hour)`를 바꾸지 않는다. 6주는 이 이름에 이벤트와 카운터를 연결한다. 5주의 시작 app.js를 다음 주 완성본 대신 넘기지 않는다.
