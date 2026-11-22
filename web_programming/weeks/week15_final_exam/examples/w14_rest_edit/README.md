# w14_rest_edit · PATCH 한 요청

출처: [14주](../../../week14_project_presentation/lab.md) · 권장 8분 · E REST 3점.

## 할 일

공개 연습본에서는 requestPatch(url, editKey, message)의 TODO와 임시 throw만 교체한다. url은 id와 book_id 필터가 포함된 제공 값이고 apikey 값은 config.example.js의 API_PUBLIC_KEY다. PATCH로 message JSON을 보내며 apikey·X-Edit-Key·Content-Type: application/json·Prefer: return=representation을 넣고 fetch의 Response를 반환한다.

DELETE·응답 검사·같은 ID 재조회·입력 검증·키 지우기·버튼 복구는 제공 코드다. PATCH와 DELETE를 모두 작성하는 문항이 아니다. 실제 시험이 DELETE 변형이면 강의자는 PATCH 완성부와 DELETE 빈칸을 바꾼 시작본을 배부하며 학생 구현은 여전히 한 요청뿐이다.

## 확인할 것

- 자기 태그에서 연습 글 세 개의 실제 서버 ID를 확인한다. 배열 위치를 ID로 쓰지 않는다.
- 가운데 글에 PATCH를 구현하고 메시지를 수정한다. 반환 행 한 개와 같은 ID의 GET 결과가 일치해야 한다.
- 별도 연습 글의 삭제 확인은 제공 DELETE로 수행한다. 다른 글이 남고 204에 JSON 파싱 오류가 없다.
- 틀린 키로는 글이 바뀌지 않고 변경 미확인 안내가 나온다. DELETE는 204이어도 같은 ID가 남아 있으면 실패다.
- 편집 키 입력은 요청할 때마다 비워지며 소스·URL·localStorage에 남지 않는다.
- 시험 ID·태그·편집 키는 별도 배부한다. 다른 학생 데이터로 실습하지 않는다.

## 제공 파일과 설정

화면과 W3.CSS는 제공 코드다. 화면 스타일은 W3.CSS 4.1.0 CDN에서 읽는다. 동작 코드는 app.js 하나이고 config.example.js는 별도 제공 설정이다. 폴더를 통째로 복사하고 Node.js 24 정적 서버로 연다.

config.example.js가 수업용 서버 주소 API_BASE_URL과 방명록 번호 BOOK_ID를 정하고, 공개 키 API_PUBLIC_KEY는 이 브라우저의 localStorage에서 읽는다. `const BOOK_ID = 'student01';`의 student01을 배정받은 자기 방명록 번호로 바꾼다. 바꾸지 않으면 student01 방명록에서 글을 찾는다. 처음 열면 공개 키를 묻는 창이 뜬다. 강의자가 배부한 공개 키를 입력하면 이 브라우저의 localStorage에 저장되고, 같은 주소에서 연 다른 문항도 그 키를 함께 쓴다.

localStorage는 주소(출처)마다 따로다. 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소에서는 처음 열 때 다시 묻는다. 창을 취소하거나 빈 칸으로 두면 키가 저장되지 않는다. 공개 키가 없거나 틀리면 서버가 HTTP 401을 돌려주고 목록 확인 실패나 변경 미확인이 보인다. 키 없이 새로고침하면 다시 묻는다. 잘못 넣었거나 학기마다 키가 바뀌면 화면 제목 아래의 [공개 키 지우기]를 누르고 새 키를 입력한다. 편집 키는 이 창에 넣지 않는다. 로컬 모의 API 리허설은 [공용 설정 안내](../../../../shared/README.md)를 따른다. 실제 키를 파일에 넣지 않는다.

## REST Client

VS Code REST Client(humao.rest-client)를 설치한다. 같은 폴더의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 브라우저는 .env를 읽지 않는다. [requests.http](requests.http)의 **Send Request**를 위에서부터 실행하여 about·help의 200을 먼저 확인한다. GET의 apikey, 쓰기의 Content-Type과 Prefer 헤더를 비교한다. 요청 위 주석의 상태와 응답을 확인한다. 편집 키는 password prompt에만 입력하고 실행 뒤 Clear Request History로 이력을 지운다.

## 실행과 제출

수업 전에 폴더·서버를 준비한다. 연습 주소는 http://localhost:8000/폴더이름/ 이다. 1일차 업로드는 수업 뒤 수행한다. 시험에서는 배부받은 exam/ 목차·개인별 태그·초기 글을 사용한다. 서버 구성과 장애 처리는 [실습지](../../lab.md)를 따른다.
