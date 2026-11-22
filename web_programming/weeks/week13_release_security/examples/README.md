# 13주차 예제 · 방명록에 글 쓰기

12주에 익힌 GET에 이어, 강의자가 준비한 수업용 방명록에 글을 쓴다. 1차시는 REST Client로, 2차시는 웹 폼으로 같은 API에 JSON 본문을 보낸다.

| 예제 | 구분 | 확인할 내용 |
|---|---|---|
| [ex01](day1/ex01/README.md) | 선택 복습 | 입력한 문장이 `JSON.stringify` 결과에 들어가는 자리 |
| [ex02](day1/ex02/README.md) | 1차시 필수 | 첫 POST의 `201` 응답에서 받은 `id`를 목록에서 찾기 |
| [ex03](day1/ex03/README.md) | 1차시 필수 | 빈 메시지의 `400`과 정상 메시지의 `201` 비교 |
| [ex04](day2/ex04/README.md) | 시연 | 폼에 입력한 문장과 POST 본문 비교 |
| [ex05](day2/ex05/README.md) | 시연 | 저장 버튼이 잠기는 시점과 통신 실패 뒤 남은 입력 확인 |
| [ex06](day2/ex06/README.md) | 시연 | 저장 성공 뒤 제공된 조회 함수 호출 |
| [완성 방명록](day2/web-week13/README.md) | 2차시 필수 | 별칭·메시지 입력부터 저장과 목록 갱신까지 연결 |

## 수업 API 설정

VS Code에 REST Client(`humao.rest-client`)를 설치하고 실행할 예제 폴더의 `.env.example`을 `.env`로 복사한다. `API_BASE_URL`에는 기본 수업 주소를 두고 `API_PUBLIC_KEY`와 `BOOK_ID`에 배부받은 공개 키와 방명록 번호를 넣는다. 12주 선택 방명록에서 같은 API를 썼다면 그 `.env`를 복사해도 된다. `.env`는 개인 설정이므로 Git에 올리지 않는다.

각 폴더의 `requests.http`에서 해당 요청 위 **Send Request**를 누른다. 모든 요청의 `apikey` 헤더는 공개 키다. POST의 `Content-Type: application/json`은 JSON 본문을 지정하고 `Prefer: return=representation`은 저장된 행을 응답으로 요청한다. 접속 확인이 필요할 때는 [수업 API의 접속 확인·도움말 요청](../../week12_fetch_json/examples/day2/web-week12/requests.http)을 연다.

브라우저 예제는 폴더마다 있는 `config.example.js`에서 수업 주소와 방명록 번호를 읽는다. 폴더마다 `const BOOK_ID = 'student01';`에서 `student01`을 배정받은 방명록 번호로 바꾼다. 공개 키는 파일에 적지 않는다. 예제를 처음 열면 공개 키를 묻는 창이 뜨고, 배부받은 키를 넣으면 localStorage에 저장된다. localStorage는 주소(출처)마다 따로라서 같은 주소로 연 예제끼리는 이 키를 함께 쓰고 다음부터 묻지 않는다. 다른 브라우저, 포트가 다른 localhost, Pages 주소, 휴대폰에서는 처음 열 때 한 번 묻는다. 새로고침해도 키와 서버에 저장한 글은 남는다. 창을 취소하거나 빈 칸으로 두면 요청이 HTTP 401로 거절되고, 새로고침하면 다시 묻는다. 키를 잘못 넣었거나 키가 바뀌면 화면 제목 아래 **공개 키 지우기**를 누르고 새 키를 넣는다. 강의자가 로컬 모의 API로 리허설할 때는 `config.example.js`의 주소를 `http://127.0.0.1:8787`로 바꾸고, 같은 버튼으로 키를 지운 뒤 묻는 창에 `classroom-local`을 넣는다. 리허설이 끝나면 주소를 되돌리고 같은 방법으로 수업용 공개 키를 다시 넣는다.

## 실습 시간과 조립 순서

1차시 실습은 메시지 변경과 POST 10분, 응답 id와 GET 확인 10분, 빈값 거절 비교 10분이다. 2차시는 폼 값·JSON 본문·재조회 호출 연결 15분, 대기·실패 확인 7분, 다른 브라우저에서 확인하고 캡처하기 8분이다. 각 차시 강의와 시연은 60분이다.

| 제공된 방명록에서 이어 쓸 부분 | 13주에 추가할 부분 |
|---|---|
| `config.example.js`의 수업 API 주소·방명록 번호와 localStorage의 공개 키 | 폼을 제출할 때 보낼 별칭과 메시지 |
| `loadMessages()`와 목록 화면 | POST 성공 뒤 `loadMessages()`를 호출하는 한 줄 |

[완성본 guestbook.js](day2/web-week13/guestbook.js)에 폼과 요청을 연결한다. 방명록 화면은 W3.CSS 4.1.0을 쓴다. [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)
