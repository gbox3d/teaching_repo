[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 · REST API로 방명록 저장하기

12주에는 공개 API를 호출해 응답을 기다리고 JSON을 읽었다. 이번 주에는 수업용 Supabase API에 `POST /rest/v1/guestbook`을 보내 내 방명록에 새 글을 남긴다. 저장 응답에서 글 번호(`id`)를 읽고 제공된 조회 함수 `loadMessages()`로 목록에서 그 글을 확인한다.

## 학습 목표와 결과물

`method`·`headers`·`body`의 역할을 읽고 폼 값을 `JSON.stringify`로 전송한다. POST 201의 서버 id와 뒤따르는 GET 200을 확인한다. 저장 중 중복 클릭, 실패한 입력 보존, 저장 성공과 목록 조회 실패를 구분한다. 결과물은 홈·내 정보·방명록 세 페이지와 POST 201 → GET 200 캡처다.

## 2일 수업 흐름

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 1차시 | 준비 5, POST 15, headers·body 15, 201·id 10, 입력 거절 10, 안내 5 | `.http` message 변경·POST 10, id 확인·GET 10, 빈값 거절 비교 10 |
| 2차시 | 준비 5, 폼에서 요청 본문 만들기 10, POST 연결 15, 대기·실패 15, 재조회 10, 안내 5 | 폼 값·JSON·loadMessages 세 구역 15, 중복 클릭·실패 입력 보존 7, 다른 브라우저·캡처 8 |

첫 필수 예제는 [ex02의 POST 요청](examples/day1/ex02/requests.http)이다. ex01은 객체를 JSON으로 바꾸는 과정이 낯설 때 펴 보는 선택 복습이다. 2차시에는 ex04~ex06을 시연한 뒤 완성 방명록에서 폼과 저장 요청을 연결한다.

## 사전 준비와 수업 뒤 정리

수업 전에 예제와 `web-week13` 저장소를 준비한다. 별도 저장소에는 [학생용 API 안내](../../tools/guestbook-api/student-guide.md#1-접속-주소와-설정)에 따라 루트 `.gitignore`를 설정한다. 수업 API 주소는 `https://esoqbcwgzjtwcqszwvin.supabase.co`다. VS Code REST Client(`humao.rest-client`)에서는 각 예제의 `.env.example`을 `.env`로 복사한다. 기본 주소는 그대로 두고 `API_PUBLIC_KEY`에 배부받은 공개 키, `BOOK_ID`에 내 방명록 번호를 적는다. 12주 선택 방명록 예제를 해 본 학생은 그 예제의 `.env`를 복사해도 된다. [따라하기](walkthrough.md)

브라우저에서는 예제를 열고 **API 설정**에 배부받은 공개 키와 방명록 번호를 입력한 뒤 **설정 적용**을 누른다. 새로고침하면 키와 번호를 다시 입력한다. `commit`·`push`·Pages 확인은 수업 뒤에 진행한다.

## 예제 구분

| 예제 | 구분 | 관찰 결과 |
|---|---|---|
| [ex01](examples/day1/ex01/README.md) | 선택 복습 | 객체를 JSON 문자열로 변환 |
| [ex02](examples/day1/ex02/README.md) | 첫 필수 요청 | 고정 본문의 POST·201·id |
| [ex03](examples/day1/ex03/README.md) | 필수 거절 비교 | 빈 메시지 400·정상 메시지 201 |
| [ex04](examples/day2/ex04/README.md) | 시연 | trim한 폼 값을 JSON 본문에 연결 |
| [ex05](examples/day2/ex05/README.md) | 시연 | 대기 중 버튼 잠금·실패 입력 보존 |
| [ex06](examples/day2/ex06/README.md) | 시연 | POST 성공 뒤 GET 재조회 |
| [완성 방명록](examples/day2/web-week13/README.md) | 2차시 필수 수정 3곳 | 폼 값·JSON 본문·재조회 |

## 완료 기준

- 별칭과 메시지를 저장하고 POST 201의 id를 GET 200 목록에서 찾는다.
- 공백만 입력하면 요청을 보내지 않고, `<b>글자</b>`는 HTML 효과 없이 글자 그대로 보인다.
- 대기 중 중복 클릭을 막고 실패 입력과 재활성화된 버튼을 확인한다.
- POST 응답이 불명확하면 GET으로 먼저 확인하며, GET 실패를 저장 실패로 판단해 재POST하지 않는다.
- 두 번째 브라우저에 같은 방명록 번호를 입력해 방금 저장한 글을 확인한다.

## 자료와 다음 수업

[슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제 설명](examples/README.md)

교재 사이트: https://gbox3d.github.io/teaching_repo/webprg/decks/week13_release_security/index.html

14주는 같은 `guestbook.js`에 서버 id를 이용한 PATCH·DELETE 구역을 추가한다. 방명록은 W3.CSS CDN 4.1.0을 사용한다.

## 용어와 공식 자료

| 용어 | 뜻 |
|---|---|
| method | 요청할 동작(GET·POST) |
| headers | 공개 키·본문 형식·응답 방식 |
| body | JSON 문자열로 전송하는 글 |
| id | 서버가 생성한 글 식별 번호 |
| disabled | 요청을 기다리는 동안 버튼 비활성화 |

[MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) · [HTTP 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods) · [Supabase Data REST API](https://supabase.com/docs/guides/api)
