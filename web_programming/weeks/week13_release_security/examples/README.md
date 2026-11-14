# 13주차 예제 · REST API로 방명록 저장하기

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
| [ex01/index.html](day1/ex01/index.html) · [app.js](day1/ex01/app.js) | 객체와 전송할 JSON 글자를 비교한다 | JSON 본문 만들기 | message 값 |
| [ex02/index.html](day1/ex02/index.html) · [app.js](day1/ex02/app.js) · [설정](day1/ex02/config.example.js) | 버튼을 누를 때만 글 한 줄을 저장한다 | 고정값 POST | 보내는 메시지 |
| [ex03/index.html](day1/ex03/index.html) · [app.js](day1/ex03/app.js) · [설정](day1/ex03/config.example.js) | 빈 메시지는 서버가 거절한다 | 서버 입력 검사 | 빈 문자열 → 문장 |
| [ex04/index.html](day2/ex04/index.html) · [app.js](day2/ex04/app.js) · [설정](day2/ex04/config.example.js) | 입력한 문장을 JSON 본문에 넣는다 | 폼 입력 POST | 입력 내용과 앞뒤 공백 |
| [ex05/index.html](day2/ex05/index.html) · [app.js](day2/ex05/app.js) · [설정](day2/ex05/config.example.js) | 응답을 기다리는 동안 다시 누를 수 없다 | 저장 중 버튼 | Slow 3G → No throttling |
| [ex06/index.html](day2/ex06/index.html) · [app.js](day2/ex06/app.js) · [설정](day2/ex06/config.example.js) | POST 성공 뒤 GET 결과를 표시한다 | 저장 후 재조회 | Network의 POST·GET 순서 |

## 조립표

최종 [web-week13/guestbook.html](day2/web-week13/guestbook.html)은 지난주 홈·내 정보 페이지와 같은 CSS를 쓴다.

| 만들기 파일 | 가져오는 개념 |
|---|---|
| [config.example.js](day2/web-week13/config.example.js) | 강의자 공개 설정 세 값 |
| [guestbook.js](day2/web-week13/guestbook.js) | 12주 GET·목록 함수를 그대로 사용 |
| [submit.js](day2/web-week13/submit.js) | ex01 JSON 본문, ex02 POST, ex04 폼, ex05 버튼, ex06 재조회 |
| [guestbook.html](day2/web-week13/guestbook.html) | 7주 폼에 이름·메시지·저장 버튼을 연결 |

이름은 30자, 메시지는 500자 이내다. 화면에 넣을 때는 `textContent`를 쓴다.
서버 목록과 11주 localStorage 목록은 자동으로 합쳐지지 않는다.
