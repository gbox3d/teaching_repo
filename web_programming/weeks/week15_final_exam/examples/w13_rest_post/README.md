# w13_rest_post · POST 한 요청

출처: [13주](../../../week13_release_security/lab.md) · 권장 8분 · C 폼·목록 4점 또는 E REST 3점. C와 E에 중복 출제하지 않는다.

## 할 일

app.js의 requestPost(name, message) 안의 TODO와 임시 throw를 교체한다. /rest/v1/guestbook에 POST하며 apikey·Content-Type: application/json·Prefer: return=representation을 넣는다. 본문은 자기 book_id와 name·message의 JSON 객체다. response.ok를 확인하고 JSON 배열을 반환한다.

빈값 검사·중복 클릭 방지·GET 재조회·입력 보존·설정 변경 처리는 제공 코드다. POST 구현을 제외한 페이지 전체를 새로 작성하지 않는다.

## 확인할 것

- 시작본은 목록 조회는 되지만 등록은 저장 미확인으로 표시한다.
- 공백만 입력하면 요청하지 않는다.
- 연습별칭·REST 연습 중입니다.를 등록하면 POST 201, 반환 ID, 같은 ID의 GET 저장값이 일치한다.
- 새로고침 후 API 설정을 다시 입력해도 서버 글이 남는다.
- 실패하면 입력이 유지된다. 응답만 유실됐을 수 있으므로 목록부터 확인하고 재등록한다.

## 제공 파일과 설정

화면·W3.CSS·설정 패널은 제공 코드다. 화면 스타일은 W3.CSS 4.1.0 CDN에서 읽는다. 동작 코드는 app.js 하나이고 api-settings.js는 별도 제공 설정이다. 폴더를 통째로 복사하고 Node.js 24 정적 서버로 연다.

API 설정을 펼쳐 주소·공개 키·자기 방명록 번호를 입력한다. 기본값은 로컬 127.0.0.1:8787·classroom-local·student01이다. 설정은 메모리에만 있으므로 새로고침 후 다시 입력한다. 공용 실습과 Pages는 강의자가 준비한 HTTPS API를 사용한다. 실제 키를 파일에 넣지 않는다.

## REST Client

VS Code REST Client(humao.rest-client)를 설치한다. 같은 폴더의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 브라우저는 .env를 읽지 않는다. [requests.http](requests.http)의 **Send Request**를 위에서부터 실행하여 about·help의 200을 먼저 확인한다. GET의 apikey, 쓰기의 Content-Type과 Prefer 헤더를 비교한다. 요청 위 주석의 상태와 응답을 확인한다. 편집 키는 password prompt에만 입력하고 실행 뒤 Clear Request History로 이력을 지운다.

## 실행과 제출

수업 전에 폴더·서버를 준비한다. 연습 주소는 http://localhost:8000/폴더이름/ 이다. 1일차 업로드는 수업 뒤 수행한다. 시험에서는 배부받은 exam/ 목차·개인별 태그·초기 글을 사용한다. 서버 구성과 장애 처리는 [실습지](../../lab.md)를 따른다.
