[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 · REST API로 방명록 저장하기

12주 GET 목록에 POST를 연결한다. 11주 필수 실습은 폼 저장·복원이며 전체 저장 방명록은 제공 시연본이었다. 이번 주에는 그 방명록 화면과 12주 서버 조회 함수를 이어 쓴다.

## 학습 목표와 결과물

`method`·`headers`·`body`의 역할을 읽고 폼 값을 `JSON.stringify`로 전송한다. POST 201의 서버 id와 뒤따르는 GET 200을 확인한다. 저장 중 중복 클릭, 실패한 입력 보존, 저장 성공과 목록 조회 실패를 구분한다. 결과물은 홈·내 정보·방명록 세 페이지와 POST 201 → GET 200 캡처다.

## 2일 수업 흐름

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 1차시 | 준비 5, POST 15, headers·body 15, 201·id 10, 입력 거절 10, 안내 5 | `.http` message 변경·POST 10, id 확인·GET 10, 빈값 거절 비교 10 |
| 2차시 | 준비 5, 기존 submit 복습 10, POST 연결 15, 대기·실패 15, 재조회 10, 안내 5 | 폼 값·JSON·loadMessages 세 구역 15, 중복 클릭·실패 입력 보존 7, 다른 브라우저·캡처 8 |

예제 전체를 학생이 다시 작성하지 않는다. ex01·ex04~ex06은 강의자 시연, ex02·ex03은 1차시 `.http` 실습의 비교본이다. 설정 패널과 방어 코드는 제공한다. 선택 연습은 저장 응답 손실·GET 지연 비교이며 정규 30분에 포함하지 않는다.

## 사전 준비와 수업 뒤 정리

수업 전에 [web-week12](../week12_fetch_json/examples/day2/web-week12/)와 이번 주 제공 폴더, Node.js·VS Code REST Client(`humao.rest-client`), 새 `web-week13` 저장소를 준비한다. 로컬 연습은 [정적 서버](../../tools/static-server/README.md)와 [API 서버](../../tools/guestbook-api/README.md)를 함께 실행한다. 첫 5분에는 파일과 서버만 확인한다.

화면의 API 설정에서 강의자 URL·공개 키·방명록 번호를 입력한다. 메모리 설정이므로 새로고침 뒤 다시 입력한다. 기본값은 로컬 연습용이며 배포된 공용 주소가 아니다. 각 REST 폴더의 `.env.example`을 `.env`로 복사해 REST Client도 별도로 설정한다. 실제 키를 추적 파일에 적지 않는다. 자세한 절차는 [따라하기](walkthrough.md)에 있다.

실습 시간에는 localhost 동작과 캡처를 마친다. commit·push·Pages 확인은 수업 뒤 정리다. 공용 HTTPS API가 준비되면 별도 브라우저·기기의 공유를 확인한다. 같은 PC의 로컬 API 검증을 다른 기기·공용 서버 검증으로 기록하지 않는다.

## 예제 구분

| 예제 | 구분 | 관찰 결과 |
|---|---|---|
| [ex01](examples/day1/ex01/README.md) | 시연 | 객체를 JSON 문자열로 변환, 서버 요청 없음 |
| [ex02](examples/day1/ex02/README.md) | 필수 요청의 비교본 | 고정값 POST·201·id |
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
- 같은 API·방명록 번호를 설정한 두 브라우저에서 글을 확인한다. 공용 API·다른 기기 검증 여부는 별도로 적는다.

## 자료와 다음 수업

[슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [실습지](lab.md) · [따라하기](walkthrough.md) · [예제 설명](examples/README.md)

교재 사이트: https://gbox3d.github.io/teaching_repo/webprg/decks/week13_release_security/index.html

14주는 같은 `guestbook.js`에 서버 id를 이용한 PATCH·DELETE 구역을 추가한다. 방명록 화면은 W3.CSS CDN 4.1.0과 폴더별 `shared/examples.css`를 함께 쓴다. 홈·내 정보의 기존 CSS는 이어 쓴다.

## 용어와 공식 자료

| 용어 | 뜻 |
|---|---|
| method | 요청할 동작(GET·POST) |
| headers | 공개 키·본문 형식·응답 방식 |
| body | JSON 문자열로 전송하는 글 |
| id | 서버가 생성한 글 식별 번호 |
| disabled | 요청을 기다리는 동안 버튼 비활성화 |

[MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) · [HTTP 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods) · [Supabase Data REST API](https://supabase.com/docs/guides/api)
