# w13_rest_post · POST 한 요청

출처: [13주](../../../week13_release_security/lab.md) · 권장 8분 · C 폼·목록 4점 또는 E REST 3점. C와 E에 중복 출제하지 않는다.

## 할 일

app.js의 requestPost(name, message) 안의 TODO와 임시 throw를 교체한다. /rest/v1/guestbook에 POST하며 apikey·Content-Type: application/json·Prefer: return=representation을 넣는다. 본문은 자기 book_id와 name·message의 JSON 객체다. response.ok를 확인하고 JSON 배열을 반환한다.

빈값 검사·중복 클릭 방지·GET 재조회·입력 보존은 제공 코드다. POST 구현을 제외한 페이지 전체를 새로 작성하지 않는다.

## 확인할 것

- 시작본은 목록 조회는 되지만 등록은 저장 미확인으로 표시한다.
- 공백만 입력하면 요청하지 않는다.
- 연습별칭·REST 연습 중입니다.를 등록하면 POST 201, 반환 ID, 같은 ID의 GET 저장값이 일치한다.
- 새로고침해도 서버 글이 남는다.
- 실패하면 입력이 유지된다. 응답만 유실됐을 수 있으므로 목록부터 확인하고 재등록한다.

## 제공 파일과 설정

화면과 W3.CSS는 제공 코드다. 화면 스타일은 W3.CSS 4.1.0 CDN에서 읽는다. 동작 코드는 app.js 하나이고 config.example.js는 별도 제공 설정이다. 폴더를 통째로 복사하고 Node.js 24 정적 서버로 연다.

config.example.js가 수업용 서버 주소 API_BASE_URL과 방명록 번호 BOOK_ID를 정하고, 공개 키 API_PUBLIC_KEY는 이 브라우저의 localStorage에서 읽는다. `const BOOK_ID = 'student01';`의 student01을 배정받은 자기 방명록 번호로 바꾼다. 바꾸지 않으면 글이 student01 방명록에 저장된다. 처음 열면 공개 키를 묻는 창이 뜬다. 강의자가 배부한 공개 키를 입력하면 이 브라우저의 localStorage에 저장되고, 같은 주소에서 연 다른 문항도 그 키를 함께 쓴다.

localStorage는 주소(출처)마다 따로다. 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소에서는 처음 열 때 다시 묻는다. 창을 취소하거나 빈 칸으로 두면 키가 저장되지 않는다. 키가 없거나 틀리면 서버가 HTTP 401을 돌려주고 목록 확인 실패나 저장 미확인이 보인다. 키 없이 새로고침하면 다시 묻는다. 잘못 넣었거나 학기마다 키가 바뀌면 화면 제목 아래의 [공개 키 지우기]를 누르고 새 키를 입력한다. 로컬 모의 API 리허설은 [공용 설정 안내](../../../../shared/README.md)를 따른다. 실제 키를 파일에 넣지 않는다.

## REST Client

VS Code REST Client(humao.rest-client)를 설치한다. 같은 폴더의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 브라우저는 .env를 읽지 않는다. [requests.http](requests.http)의 **Send Request**를 위에서부터 실행하여 about·help의 200을 먼저 확인한다. GET의 apikey, 쓰기의 Content-Type과 Prefer 헤더를 비교한다. 요청 위 주석의 상태와 응답을 확인한다. 편집 키는 password prompt에만 입력하고 실행 뒤 Clear Request History로 이력을 지운다.

## 실행과 제출

수업 전에 폴더·서버를 준비한다. 연습 주소는 http://localhost:8000/폴더이름/ 이다. 1일차 업로드는 수업 뒤 수행한다. 시험에서는 배부받은 exam/ 목차·개인별 태그·초기 글을 사용한다. 서버 구성과 장애 처리는 [실습지](../../lab.md)를 따른다.
