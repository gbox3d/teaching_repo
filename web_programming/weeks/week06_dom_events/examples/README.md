# 6주차 예제 파일 안내

각 예제의 index.html·styles.css·app.js는 같은 폴더에서 연다. 1~6주에는 자체 CSS를 사용하며 CDN이 필요 없다. 파일은 수업 전에 배부한다. [주차 실습지](../lab.md)의 필수 변경만 30분 안에 작성하고, 비교 예제의 추가 수정은 선택이다.

| 폴더 | HTML·CSS·JS | README와 수업 범위 |
|---|---|---|
| day1/ex01 | [HTML](day1/ex01/index.html), [CSS](day1/ex01/styles.css), [JS](day1/ex01/app.js) | [DOM·소스 비교](day1/ex01/README.md), 시연 |
| day1/ex02 | [HTML](day1/ex02/index.html), [CSS](day1/ex02/styles.css), [JS](day1/ex02/app.js) | [열 때·클릭할 때](day1/ex02/README.md), 시연 |
| day1/ex03 | [HTML](day1/ex03/index.html), [CSS](day1/ex03/styles.css), [JS](day1/ex03/app.js), [시작 틀](day1/ex03/app.start.js) | [카운터](day1/ex03/README.md), 여섯 줄 필수·inside 비교 시연 |
| day2/ex04 | [HTML](day2/ex04/index.html), [CSS](day2/ex04/styles.css), [JS](day2/ex04/app.js) | [classList](day2/ex04/README.md), 시연 |
| day2/ex05 | [HTML](day2/ex05/index.html), [CSS](day2/ex05/styles.css), [JS](day2/ex05/app.js) | [다크 모드](day2/ex05/README.md), 시연 |
| day2/ex06 | [HTML](day2/ex06/index.html), [CSS](day2/ex06/styles.css), [JS](day2/ex06/app.js) | [함수 재사용](day2/ex06/README.md), 시연 |

ex01은 원래 HTML과 바뀐 DOM, ex02는 실행 시점, ex03은 count 1·2·3과 inside 1·1·1을 비교한다. ex04는 add·remove를 반복해도 상태가 유지되는 것과 toggle 전환을 비교한다. ex05는 body와 카드 배경, ex06은 두 버튼의 공유 함수를 확인한다. 설명과 실습 순서는 각 README에 두고 HTML에는 제목·버튼·결과만 둔다.

## 5주에서 6주로 이어 쓰는 파일

완성 [web-week06](day2/web-week06/README.md)은 7주차 시작점이다. 학생은 개인 본문과 이미지를 유지한다. 강의자가 HTML·CSS와 JS 시작 틀을 사전에 준비하고, 학생은 CSS 색 두 곳과 JS 세 줄만 완성한다.

| 파일 | 5주 대비 변경 | 제공·직접 수정 구분 |
|---|---|---|
| [index.html](day2/web-week06/index.html) | #greeting 뒤 #hello-button·#dark-button·#count 추가 | 제공 HTML, 개인 본문 유지 |
| [styles.css](day2/web-week06/styles.css) | body.dark의 배경·카드·제목·메뉴·푸터 규칙 추가 | 규칙 제공, 배경·글자 두 값 변경 |
| [app.start.js](day2/web-week06/app.start.js) | 요소 선택·count·countUp·리스너 틀 | 개인 app.js로 복사, TODO 세 줄 직접 작성 |
| [app.js](day2/web-week06/app.js) | 두 버튼이 countUp 공유, 다크 버튼 toggle | 비교용 완성본, 추가 script로 로드하지 않음 |
| [about.html](day2/web-week06/about.html) | 5주 그대로 | 왕복 링크 확인 |
| [guestbook.html](day2/web-week06/guestbook.html) | 5주 정적 폼 그대로 | 7주에 W3.CSS 변환과 제공 폼 코드 연결 |
| [images/profile.png](day2/web-week06/images/profile.png) | 3주부터 이어 쓰는 이미지 | 개인 이미지 유지 |

## 시작 틀 사용

개인 ex03 폴더에서는 app.start.js를 app.js로 복사하고 여섯 줄을 작성한다. 완성 app.js의 inside와 로그는 강의자 비교용이다. 개인 홈에서는 별도의 app.start.js를 app.js로 복사하고 두 리스너 안의 TODO만 채운다. 각 페이지는 동작 파일 app.js 하나만 읽는다.

## 정적 방명록 설명

이름·이메일·메시지를 입력하고 남기기를 누르는 순서다. 이메일 형식이 잘못되면 브라우저가 제출을 막는다. 유효하거나 빈 입력은 같은 문서로 기본 GET 탐색을 하며 저장되지 않는다. input과 textarea에 name 속성이 없으므로 입력 값도 URL에 포함되지 않는다. 7주에서 제공 JS가 입력 검사와 DOM 추가를 담당한다. 이메일은 HTML 입력 종류 비교용이며 이후 서버 필드가 아니다.
