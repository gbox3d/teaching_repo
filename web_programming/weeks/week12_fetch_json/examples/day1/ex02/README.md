# ex02 · API 도움말

help 요청을 실행한다. step 1~6에서 GET·POST·PATCH·DELETE의 경로를 읽는다. 이번 주에는 GET만 사용한다.

## 실행과 설정

이 폴더 전체를 정적 서버로 연다. HTML은 `api-settings.js` 다음에 동작 JS를 `defer`로 실행한다. 제공 설정 패널은 구현 과제가 아니다.
기본값은 `http://127.0.0.1:8787`·`classroom-local`·`student01`이다. 강의자가 로컬 API와 정적 서버를 먼저 실행한다. 로컬 주소는 다른 기기의 API를 뜻하지 않는다.
공용 API를 쓰면 화면의 **API 설정**을 열고 배부받은 HTTPS 주소·공개 키·방명록 번호를 입력한 뒤 **설정 적용**을 누른다. 입력은 메모리에만 있으며 새로고침 후 다시 입력한다. 실제 값을 JS에 기록하지 않는다. 서버 비밀 키·편집 키를 이 패널에 입력하지 않는다.

## VS Code REST Client

1. `humao.rest-client` 확장을 설치한다. `.env.example`을 같은 폴더의 `.env`로 복사한다.
2. `.env`의 `API_BASE_URL`·`API_PUBLIC_KEY`·`BOOK_ID`를 확인한다. 기본 로컬 값은 그대로 실행할 수 있다. 공용 값은 이 무시되는 로컬 파일에만 적는다.
3. `requests.http`를 열고 요청 위 **Send Request**를 about → help → GET 순서로 누른다. `{{$dotenv ...}}`는 같은 폴더 `.env`에서 읽으며 모든 요청에 `apikey` 헤더가 있다. GET에는 JSON 본문·Content-Type이 필요 없다.
4. about는 200과 API 정보 배열, help는 200과 사용법 배열, GET은 200과 글 배열을 반환한다. `[]`는 글이 없는 정상 결과다. 401이면 공개 키, 404이면 URL, 연결 실패면 서버 실행 여부를 확인한다.

브라우저 패널과 REST Client `.env`는 별개다. 한쪽 설정은 다른 쪽에 전달되지 않는다. `.env`와 실제 키는 Git·ZIP에 포함하지 않는다. 폴더의 `.gitignore`도 복사한다. REST Client 성공만으로 브라우저 CORS나 두 기기 공유가 검증되지는 않는다.

## 스타일과 파일

W3.CSS는 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`에서 읽는다. 인터넷 연결이 필요하다. 추가 스타일은 이 폴더의 `shared/examples.css`다. 교재 `web_programming/shared/examples.css`의 배포 사본이므로 이 하위 폴더까지 복사하면 단독 배포가 가능하다. `api-settings.js`는 교재 `web_programming/shared/api-settings.js`의 제공 사본이다. 기존 `config.example.js`가 있으면 이동 안내만 담으며 실행하지 않는다.
