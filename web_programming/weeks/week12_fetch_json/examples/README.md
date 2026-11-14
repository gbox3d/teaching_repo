# 12주차 예제 · REST API로 방명록 읽기

## 목차

- [실행](#실행)
- [비교 예제](#비교-예제)
- [조립표](#조립표)

## 실행

[따라하기](../walkthrough.md)의 설정·서버 실행부터 진행한다.
`config.example.js`는 공개 설정 파일이며 HTML이 직접 읽는다. 이름을 바꾸지 않는다.
예제 폴더를 작업 저장소의 `ex/ex01/`처럼 복사해 `http://localhost:8000/ex/ex01/`로 연다.
`ex01`은 API가 필요 없고, 나머지는 강의자 API 또는 로컬 연습 API가 필요하다.

## 비교 예제

| 파일 | 열면 보이는 것 | 보여 주는 원리 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01/index.html](day1/ex01/index.html) · [app.js](day1/ex01/app.js) | JSON.parse 뒤 배열의 첫 메시지를 본다 | JSON 글자와 배열 | 메시지와 큰따옴표 |
| [ex02/index.html](day1/ex02/index.html) · [app.js](day1/ex02/app.js) · [설정](day1/ex02/config.example.js) | 응답 객체와 JSON 배열을 Console에서 구분한다 | GET 응답과 JSON 본문 | 본문의 message와 response.status 비교 |
| [ex03/index.html](day1/ex03/index.html) · [app.js](day1/ex03/app.js) · [설정](day1/ex03/config.example.js) | limit 이하의 최신 글을 읽는다 | 쿼리 문자열 | limit 1·2·5 |
| [ex04/index.html](day2/ex04/index.html) · [app.js](day2/ex04/app.js) · [설정](day2/ex04/config.example.js) | 서버 응답 항목마다 li를 붙인다 | 배열을 화면 목록으로 | name과 message 표시 순서 |
| [ex05/index.html](day2/ex05/index.html) · [app.js](day2/ex05/app.js) · [설정](day2/ex05/config.example.js) | 잘못된 끝점의 status와 ok를 비교한다 | HTTP 실패 | guestbook → missing_table |
| [ex06/index.html](day2/ex06/index.html) · [app.js](day2/ex06/app.js) · [설정](day2/ex06/config.example.js) | Offline 실패 뒤 다시 요청한다 | 연결 실패와 재시도 | Offline → No throttling |

## 조립표

최종 [web-week12/guestbook.html](day2/web-week12/guestbook.html)은 지난주 홈·내 정보 페이지와 같은 CSS를 쓴다.

| 만들기 파일 | 가져오는 개념 |
|---|---|
| [config.example.js](day2/web-week12/config.example.js) | 강의자 공개 설정 세 값 |
| [guestbook.js](day2/web-week12/guestbook.js) | ex02 GET, ex03 쿼리, ex04 목록, ex05·ex06 오류·버튼 상태 |
| [guestbook.html](day2/web-week12/guestbook.html) | 목록·새로 불러오기·상태 자리 |

이름은 30자, 메시지는 500자 이내다. 화면에 넣을 때는 `textContent`를 쓴다.
서버 목록과 11주 localStorage 목록은 자동으로 합쳐지지 않는다.
