# w12_rest_get · GET 목록

관련 수업: [12주 비동기 GET](../../../week12_fetch_json/lab.md) · [13주 방명록 조회와 저장](../../../week13_release_security/lab.md) · 권장 8분 · E REST 3점.

## 할 일

app.js의 requestList() 안의 TODO와 임시 throw를 교체한다. apiTarget()이 반환한 자기 태그 URL에 apikey 헤더를 넣어 GET한다. response.ok를 확인하고 JSON 배열을 반환한다. 화면 그리기·실패 안내·재시도는 제공 코드다.

## 확인할 것

- 첫 시작본은 아직 GET이 구현되지 않아 목록 확인 실패를 표시한다.
- 구현 뒤 about/help 200을 확인하고 목록 불러오기를 누르면 자기 글 ID·별칭·메시지가 나온다.
- 목록이 없으면 등록된 글 없음이 보인다.
- [공개 키 지우기]를 누른 뒤 틀린 키를 입력하면 목록 확인 실패가 나오고, 다시 [공개 키 지우기]를 누른 뒤 올바른 키를 입력하면 복구된다.
- Offline에서는 실패 안내가 나오고 Offline을 끈 뒤 다시 누르면 복구된다.
- 200만 확인하지 않고 JSON 배열의 값과 화면을 비교한다.

## 제공 파일과 설정

화면과 W3.CSS는 제공 코드다. 화면 스타일은 W3.CSS 4.1.0 CDN에서 읽는다. 동작 코드는 app.js 하나이고 config.example.js는 별도 제공 설정이다. 폴더를 통째로 복사하고 Node.js 24 정적 서버로 연다.

config.example.js가 수업용 서버 주소 API_BASE_URL과 방명록 번호 BOOK_ID를 정하고, 공개 키 API_PUBLIC_KEY는 이 브라우저의 localStorage에서 읽는다. `const BOOK_ID = 'student01';`의 student01을 배정받은 자기 방명록 번호로 바꾼다. 바꾸지 않으면 student01 방명록을 읽는다. 처음 열면 공개 키를 묻는 창이 뜬다. 강의자가 배부한 공개 키를 입력하면 이 브라우저의 localStorage에 저장되고, 같은 주소에서 연 다른 문항도 그 키를 함께 쓴다.

localStorage는 주소(출처)마다 따로다. 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소에서는 처음 열 때 다시 묻는다. 창을 취소하거나 빈 칸으로 두면 키가 저장되지 않는다. 키가 없거나 틀리면 서버가 HTTP 401을 돌려주고 목록 확인 실패가 보인다. 키 없이 새로고침하면 다시 묻는다. 잘못 넣었거나 학기마다 키가 바뀌면 화면 제목 아래의 [공개 키 지우기]를 누르고 새 키를 입력한다. 로컬 모의 API 리허설은 [공용 설정 안내](../../../../shared/README.md)를 따른다. 실제 키를 파일에 넣지 않는다.

## REST Client

VS Code REST Client(humao.rest-client)를 설치한다. 같은 폴더의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 브라우저는 .env를 읽지 않는다. [requests.http](requests.http)의 **Send Request**를 위에서부터 실행하여 about·help의 200을 먼저 확인한다. GET의 apikey, 쓰기의 Content-Type과 Prefer 헤더를 비교한다. 요청 위 주석의 상태와 응답을 확인한다. 편집 키는 password prompt에만 입력하고 실행 뒤 Clear Request History로 이력을 지운다.

## 실행과 제출

수업 전에 폴더·서버를 준비한다. 연습 주소는 http://localhost:8000/폴더이름/ 이다. 1일차 업로드는 수업 뒤 수행한다. 시험에서는 배부받은 exam/ 목차·개인별 태그·초기 글을 사용한다. 서버 구성과 장애 처리는 [실습지](../../lab.md)를 따른다.
