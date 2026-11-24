# PATCH와 대상 재조회

직접 쓴 글 번호와 새 메시지를 입력하고 **수정 요청**을 누른다. 같은 번호를 다시 조회해 바뀐 메시지를 확인한다.

학생 수정은 대상 URL·JSON 본문·같은 ID 재조회 3곳이다. 설정·초기화·응답 검증은 제공 코드다.

## 실행과 설정

폴더를 정적 서버로 연다. 화면은 CDN의 [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다.

config.example.js의 `const BOOK_ID = 'student01';`에서 student01을 배정받은 방명록 번호로 바꾼다. 바꾸지 않으면 student01 방명록에 요청한다. 주소는 수업용 서버다. 공개 키는 파일에 적지 않는다. 예제를 처음 열면 '배부받은 공개 키를 입력하세요.' 창이 뜬다. 키는 이 브라우저의 localStorage에 저장되고 같은 주소에서 연 다른 예제도 함께 쓴다. 창을 취소하거나 빈 칸으로 두면 키가 저장되지 않아 서버가 HTTP 401을 돌려주고 화면에 확인 실패가 보인다. 새로고침하면 다시 묻는다. 키를 잘못 넣었거나 강의자가 키를 바꾸면 제목 아래 [공개 키 지우기]를 누른다. 버튼이 저장한 키를 지우고 새로고침하면 다시 묻는 창에 새 키를 넣는다. localStorage는 주소(출처)마다 따로이므로 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소, 휴대폰에서는 처음 한 번 묻는다.

localStorage에는 배부받은 공개 키만 저장하고 서버 비밀 키는 넣지 않는다. 강의자가 로컬 API로 리허설할 때는 config.example.js의 주소를 `http://127.0.0.1:8787`로 바꾸고 [공개 키 지우기]를 누른 뒤 다시 묻는 창에 `classroom-local`을 넣는다. 리허설이 끝나면 주소를 수업용 서버로 되돌리고 [공개 키 지우기]를 누른 뒤 배부받은 공개 키를 다시 넣는다.

## VS Code REST Client

REST Client 확장 humao.rest-client를 설치한다. 별도 Git 저장소를 쓴다면 최상위 `.gitignore`에 `.env`를 추가한다. `.env.example`을 같은 폴더의 `.env`로 복사해 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 배포 ZIP에서는 실제 `.env`를 제외한다. 브라우저가 읽는 config.example.js·localStorage와 .env는 별개이므로 각각 설정한다.

[requests.http](requests.http)에서 각 요청 위의 **Send Request**를 위에서부터 누른다. 모든 요청은 `apikey` 헤더에 배부받은 공개 키를 넣는다.

1. `GET /rest/v1/about`에서 서버 소개 배열과 HTTP 200을 확인한다.
2. `GET /rest/v1/help`에서 사용 순서가 담긴 배열과 HTTP 200을 확인한다.
3. `GET /rest/v1/guestbook`의 목록에서 내가 쓴 글을 찾는다. 해당 글의 `id`를 같은 폴더의 `.env`에서 `MESSAGE_ID`에 적고 저장한다.
4. 대상 GET에서 해당 태그의 글 한 건을 읽고 원래 메시지를 확인한다.
5. `PATCH`에서 보낼 `message`를 적고 요청을 보낸다. `Content-Type: application/json`과 `Prefer: return=representation` 헤더를 사용하면 HTTP 200과 수정된 글의 배열이 돌아온다. 응답이 `[]`이면 태그와 ID에 맞는 글이 없어 변경된 행이 없다는 뜻이다.
6. 같은 태그와 ID로 마지막 GET을 보낸다. HTTP 200 응답에서 글의 `message`가 방금 보낸 값과 일치하는지 확인한다.
