[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_release_security)

# 13주차 실습 · POST와 저장 후 조회

강의자가 배부한 수업용 공개 키와 내 방명록 번호를 준비한다. 각 차시는 강의·시연 60분 뒤 학생 실습 30분이다. 설정 파일(`config.example.js`)과 요청 대기·실패 처리는 제공 코드다.

## 1일차 실습

| 시간 | 필수 활동 |
|---|---|
| 0–10분 | [ex02 요청](examples/day1/ex02/requests.http)의 `message`를 내 문장으로 바꾸고 첫 POST 위의 **Send Request**를 한 번 누른다 |
| 10–20분 | 201 응답의 id를 읽고 이어지는 GET 200에서 같은 글 확인 |
| 20–30분 | [ex03 요청](examples/day1/ex03/requests.http)에서 빈 메시지의 400 응답과 정상 문장의 201 응답 비교 |

ex02에서 `.env.example`을 `.env`로 복사해 `API_PUBLIC_KEY`와 `BOOK_ID`를 채운다. 수업 API 주소는 미리 들어 있다. 다른 예제의 `requests.http`를 열 때도 그 파일 옆에 같은 `.env`를 둔다. POST에 실린 `Content-Type: application/json`은 보내는 본문의 형식을 알리고, `Prefer: return=representation`은 저장한 행을 응답으로 요청한다.

## 2일차 실습

| 시간 | 필수 활동 |
|---|---|
| 0–15분 | 제공 `guestbook.js`에서 학생 수정 1(폼 값), 2(JSON 본문), 3(loadMessages) 세 구역을 확인·변경 |
| 15–22분 | 별칭과 메시지 저장, 느린 연결 중복 클릭·Offline 실패 입력 보존 확인 |
| 22–30분 | 두 번째 브라우저에서 공개 키 입력, GET 확인, POST 201 → GET 200 캡처 |

완성 방명록은 `config.example.js`의 `const BOOK_ID = 'student01';`에서 `student01`을 내 방명록 번호로 바꾼다. 수업 API 주소는 미리 들어 있다. 방명록을 처음 열면 공개 키를 묻는 창에 배부받은 키를 넣는다. 이 키는 브라우저의 localStorage에 남아 새로고침해도 다시 묻지 않는다.

`method: 'POST'`, 공개 키와 JSON 헤더를 읽고 본문의 `name`·`message`가 폼 입력과 일치하는지 확인한다. ex04~ex06을 전부 타이핑하지 않는다. GET·POST는 `guestbook.js` 안에 있고 `submit.js`를 별도로 연결하지 않는다.

## 확인 순서

1. 공백만 입력했을 때 안내가 나오고 POST가 없는지 확인한다.
2. 별칭과 `<b>연습</b>`를 저장하고 화면이 글자 그대로 표시하는지 본다.
3. Network의 속도를 낮춘 뒤 저장 중 버튼 비활성화를 확인한다. Offline에서는 입력이 남고 버튼이 다시 활성화되어야 한다.
4. No throttling으로 복구한다. 저장 응답을 못 받았다면 GET으로 먼저 확인한다. 저장이 확인된 글을 다시 POST하지 않는다.
5. 두 번째 브라우저에서 같은 방명록 페이지를 열고 묻는 창에 공개 키를 넣는다. 목록에서 방금 저장한 글을 찾는다.

## 막혔을 때

| 증상 | 확인·조치 |
|---|---|
| 조회·저장 통신 실패 | 수업 API 주소와 Offline 상태를 확인한 뒤 [접속 확인·도움말 요청](../week12_fetch_json/examples/day2/web-week12/requests.http)으로 연결 점검 |
| REST Client 401·403 | `.env`의 `API_PUBLIC_KEY` 확인. REST Client는 브라우저에 넣은 키를 쓰지 않음. 편집 키·서버 비밀 키로 바꾸지 않음 |
| 화면에 HTTP 401 조회·저장 실패 | 묻는 창을 취소했거나 빈 칸으로 두었거나 틀린 키를 넣음. 제목 아래 **공개 키 지우기**를 누르고 배부받은 공개 키를 다시 입력. **새로 불러오기**는 페이지를 열 때 읽은 키를 그대로 쓰므로 눌러도 401이 반복됨 |
| POST 400 | book_id·이름·메시지·JSON 형식 확인 |
| POST 성공인데 조회 실패 | 저장 안내를 유지하고 새로 불러오기로 GET만 다시 실행 |
| 저장 응답 불명확 | 입력을 보존하고 GET·서버 목록으로 먼저 확인. 재POST를 자동 반복하지 않음 |
| 글이 `student01` 방명록에 저장됨 | `config.example.js`의 `BOOK_ID`가 `student01` 그대로임. 내 방명록 번호로 바꾸고 새로고침 |
| 새로고침 뒤 글이 없음 | 서버 글과 localStorage의 키는 새로고침해도 남음. 조회 안내의 HTTP 상태 번호와 `BOOK_ID` 확인 |
| 다른 브라우저에서 글이 보이지 않음 | 그 브라우저의 묻는 창에 공개 키를 넣었는지 확인. 취소했다면 새로고침해 다시 입력. 두 브라우저가 같은 주소의 페이지와 같은 `BOOK_ID`를 쓰는지 비교 |

## 제출과 선택 연습

POST 201·GET 200과 저장한 글이 보이는 캡처를 제출한다. Network의 Request Headers를 접은 뒤 캡처한다. 저장소 commit·push·Pages 확인은 수업 뒤에 한다.

선택 연습은 POST 성공 뒤 GET만 실패시키기, Application › Local Storage에서 이 주소에 저장된 `API_PUBLIC_KEY` 확인하기다. 공개 API에서는 실패를 만들려고 반복 POST하지 않는다.
