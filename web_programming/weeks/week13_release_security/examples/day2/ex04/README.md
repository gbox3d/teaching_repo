# ex04 · 폼 입력 POST

수업 구분: 2차시 폼 값 연결 시연.

폼의 `messageInput.value.trim()` 값을 JSON 본문에 넣는다. 공백만 입력하면 POST를 보내지 않는다. 성공한 입력만 비우며 실패한 입력은 남긴다.

## 실행과 설정

폴더 전체를 정적 서버로 열고 [index.html](index.html)로 이동한다. `file://`로 열지 않는다. 로컬 연습에서는 별도 터미널에서 교재의 `tools/guestbook-api/server.mjs`를 실행한다. 기본 API는 `http://127.0.0.1:8787`, 가상 공개 키는 `classroom-local`, 방명록 번호는 `student01`이다.

공용 API를 쓰면 화면의 **API 설정**을 열어 강의자가 안내한 HTTPS 주소·공개 키·방명록 번호를 입력하고 **설정 적용**을 누른다. 적용 즉시 새 목록을 조회한다. 설정은 메모리에만 있으므로 새로고침 후에는 다시 입력한다. 서버 비밀 키와 편집 키를 이 패널에 입력하지 않는다. `config.example.js`는 이전 파일의 이동 안내이며 HTML에서 읽지 않는다.

## REST Client

VS Code REST Client 확장(`humao.rest-client`)을 설치한다. 같은 폴더의 `.env.example`을 `.env`로 복사해 `API_BASE_URL`·`API_PUBLIC_KEY`·`BOOK_ID`를 적는다. 브라우저 설정과 `.env`는 별개다. `.gitignore`의 `.env` 제외 규칙도 학생 저장소에 함께 복사한다. 실제 키를 `requests.http`나 추적 파일에 넣지 않는다.

[requests.http](requests.http)의 각 요청 위 **Send Request**를 about → help → POST → GET 순서로 누른다. about·help는 200과 정보 배열, POST는 201과 생성된 id를 포함한 배열, GET은 200과 목록 배열을 기대한다. 모든 요청은 `apikey`, POST는 `Content-Type: application/json`과 `Prefer: return=representation` 헤더를 쓴다. 마지막 빈 메시지 요청은 400을 기대하며 정상 문장으로 바꾸면 글이 실제로 저장된다.

POST 응답을 받지 못했다면 저장됐을 수도 있다. 같은 요청을 바로 반복하지 말고 **새로 불러오기** 또는 `.http`의 GET으로 먼저 확인한다. POST 성공과 뒤따르는 GET 실패를 구분한다. 다른 브라우저에서 같은 로컬 API·방명록 번호를 조회하는 검사는 같은 PC의 서버 공유 확인이다. 다른 기기의 공유 확인에는 강의자가 제공한 공용 HTTPS API가 필요하다.

## 제공 코드와 스타일

설정 패널·중복 요청 방지·실패 안내·이전 설정의 늦은 응답 무시는 제공 코드다. 설정이 바뀌면 이전 요청 결과를 새 목록이나 저장 안내에 섞지 않는다. 실패한 입력을 보존하며 요청이 끝나면 저장 버튼을 다시 활성화한다. 버튼 잠금은 화면의 중복 클릭을 줄이며 서버의 중복 저장 자체를 보장하지 않는다.

[W3.CSS CDN 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)과 폴더 안 `shared/examples.css`를 사용한다. CDN 스타일을 읽을 때 인터넷 연결이 필요하다. HTML·동작 JS·`api-settings.js`·`shared/`를 함께 복사해야 독립 실행된다.
