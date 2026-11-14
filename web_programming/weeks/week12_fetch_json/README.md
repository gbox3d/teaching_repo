[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week12_fetch_json)

# 12주차 · REST API로 방명록 읽기

## 목차

- [학습 목표](#학습-목표)
- [이번 주 결과물](#이번-주-결과물)
- [2일 수업 흐름](#2일-수업-흐름)
- [준비](#준비)
- [이번 주 용어](#이번-주-용어)
- [비교 예제](#비교-예제)
- [수업 자료](#수업-자료)
- [완료 기준](#완료-기준)
- [다음 수업 연결](#다음-수업-연결)

11주에는 내 브라우저의 localStorage에 글을 저장했다. 이번 주에는 강의자가 준비한 서버에 GET 요청을 보내 같은 방명록을 읽는다. 서버 계정 만들기와 데이터베이스 설정은 강의자가 준비한다.

## 학습 목표

1. URL·GET·헤더·응답 본문을 Network 탭에서 구분한다.
2. async 함수 안에서 fetch와 response.json을 await로 기다린다.
3. 서버가 보낸 JSON 배열을 for·createElement·textContent로 목록에 표시한다.
4. response.ok로 HTTP 실패를 확인하고 try/catch로 연결 실패를 화면에 알린다.
5. 공용 HTTPS API를 설정한 두 기기에서 같은 목록을 확인한다.

## 이번 주 결과물

서버 방명록 목록과 Network의 GET 200이 함께 보이는 화면을 캡처 한 장으로 제출한다.
새 저장소 `web-week12`의 홈·내 정보·방명록 세 페이지를 이어 쓴다.
이번 주에는 프로젝트 카드나 레포트를 만들지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 실습 60분 |
|---|---|---|
| 1일차 | JSON 복습 → GET → Network → 쿼리 문자열 | ex01~ex03에서 응답과 목록 개수 비교 |
| 2일차 | 배열을 목록으로 → HTTP 실패 → 연결 실패 → 조립 | ex04~ex06 비교 후 온라인 guestbook.html 완성 |

## 준비

- 지난주 완성본: [web-week11](../week11_object_localstorage/examples/day2/web-week11/)
- VS Code·Git·Chrome과 Node.js. [정적 서버](../../tools/static-server/README.md)를 작업 폴더에 둔다.
- 강의자가 제공한 HTTPS API 주소·공개 키·방명록 번호. 학생은 Supabase 계정을 만들지 않는다.
- [강의자 API 준비·로컬 연습 안내](../../tools/guestbook-api/README.md). 설정 예제의 `127.0.0.1:8787`은 로컬 연습 주소이며 이미 배포된 공용 주소가 아니다.

`config.example.js`의 세 값을 수정하며 파일 이름은 그대로 쓴다. 공개 키는 학생별 편집 키나 서버 비밀 키와 다르다.
로컬 연습은 정적 서버 `http://localhost:8000`과 API `http://127.0.0.1:8787`을 함께 실행한다.
GitHub Pages에서는 강의자가 제공한 HTTPS API를 사용한다. 공용 API가 준비되기 전에는 로컬 화면·Network 캡처로 실습을 확인하고, 다른 기기 공유는 공용 API 설정 후 확인한다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 요청 | request | 请求 |
| 응답 | response | 响应 |
| 끝점 주소 | endpoint | 端点 |
| 헤더 | header | 请求头 |
| 쿼리 문자열 | query string | 查询字符串 |
| 기다리기 | await | 等待 |
| 상태 코드 | status code | 状态码 |

## 비교 예제

각 예제는 `index.html`·`app.js`와 필요한 `config.example.js`로 구성된다.
원리를 하나씩 확인하고 마지막에 [이번 주 완성본](examples/day2/web-week12/guestbook.html)을 조립한다.

| 예제 | 주제 | 확인할 것 | 바꿔 볼 값 |
|---|---|---|---|
| [ex01](examples/day1/ex01/index.html) | JSON 글자와 배열 | JSON.parse 뒤 배열의 첫 메시지를 본다 | 메시지와 큰따옴표 |
| [ex02](examples/day1/ex02/index.html) | GET 응답과 JSON 본문 | 응답 객체와 JSON 배열을 Console에서 구분한다 | 본문의 message와 response.status 비교 |
| [ex03](examples/day1/ex03/index.html) | 쿼리 문자열 | limit 이하의 최신 글을 읽는다 | limit 1·2·5 |
| [ex04](examples/day2/ex04/index.html) | 배열을 화면 목록으로 | 서버 응답 항목마다 li를 붙인다 | name과 message 표시 순서 |
| [ex05](examples/day2/ex05/index.html) | HTTP 실패 | 잘못된 끝점의 status와 ok를 비교한다 | guestbook → missing_table |
| [ex06](examples/day2/ex06/index.html) | 연결 실패와 재시도 | Offline 실패 뒤 다시 요청한다 | Offline → No throttling |

## 수업 자료

- [슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- 교재 사이트: https://gbox3d.github.io/teaching_repo/webprg/decks/week12_fetch_json/index.html
- [따라하기](walkthrough.md) · [실습지](lab.md) · [예제 설명](examples/README.md)
- 강의 대본과 실습 해답은 강의자 별도 관리(비공개)다.

## 완료 기준

- [ ] 강의자가 배부한 API 주소·공개 키·BOOK_ID를 config.example.js에 적었다.
- [ ] 서버의 글이 목록에 보이고 새로 불러오기 버튼이 GET을 보낸다.
- [ ] Network에서 GET의 URL·상태 200·Response 배열을 확인했다.
- [ ] Offline에서는 안내가 보이며, 연결을 되돌린 뒤 다시 불러오면 성공한다.
- [ ] 캡처 한 장에 페이지 주소·목록·GET 200이 보인다.

API에 처음 준비된 글 수는 환경에 따라 다르다. 특정 개수보다 요청·응답과 화면이 일치하는지 확인한다.
실명·학번·실제 이메일을 사용하지 않고 수업용 별칭으로 실습한다.

## 다음 수업 연결

13주에는 기존 입력 폼을 POST에 연결해 서버에 새 글을 저장한다.

## 공식 참고 자료

- [MDN · Fetch API 사용](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [MDN · HTTP 요청 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods)
- [Supabase · Data REST API](https://supabase.com/docs/guides/api)
