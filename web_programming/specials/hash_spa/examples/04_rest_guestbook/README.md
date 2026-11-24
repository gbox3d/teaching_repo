# 04 14주 CRUD를 Hash SPA에 합친다

[완성 화면](index.html)은 홈·내 정보·방명록을 한 문서에 둔다. 방명록 폼·목록·편집 영역과 GET·POST·PATCH·DELETE는 [14주 완성본](../../../../weeks/week14_project_presentation/examples/day2/web-week14/README.md)을 재사용한다. 설정은 `config.example.js`, 동작은 `app.js` 하나다. 03의 미리 보기 코드는 제거하고 서버 방명록으로 교체했다.

## 로컬 실행

저장소 루트의 터미널에서 정적 서버를 실행한다. 이미 같은 서버가 실행 중이면 새로 시작하지 않는다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

강의자가 로컬 모의 API로 리허설할 때는 다른 터미널에서 아래 서버도 실행한다.

```bash
node web_programming/tools/guestbook-api/server.mjs
```

주소는 `http://localhost:8111/specials/hash_spa/examples/04_rest_guestbook/index.html#guestbook`이다. API 주소와 방명록 번호는 `config.example.js`가 정한다. `API_BASE_URL`은 수업용 서버 주소다. 학생은 `BOOK_ID`를 배정받은 방명록 번호로 바꾼다.

```js
const BOOK_ID = 'student01';
```

공개 키는 파일에 적지 않는다. 예제를 처음 열면 첫 화면이 홈이어도 `config.example.js`가 공개 키를 묻는 창을 띄운다. 강의자가 배부한 공개 키를 넣으면 이 브라우저의 localStorage에 저장되고 다음부터는 묻지 않는다. 취소하거나 빈 칸으로 넘기면 저장하지 않으며 목록 조회가 HTTP 401로 실패한다. 페이지를 새로고침하면 다시 묻는다. 화면의 새로 불러오기 버튼은 공개 키를 묻지 않는다.

키를 잘못 넣었거나 강의자가 새 키를 배부하면 방명록 화면 제목 아래의 [공개 키 지우기]를 누른다. 저장한 키를 지우고 새로고침하므로 다시 묻는 창에 새 키를 넣는다. localStorage는 주소(출처)마다 따로다. 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소, 휴대폰에서는 처음 한 번 다시 묻는다.

화면에 조회 실패나 저장 거절과 함께 HTTP 401이 보이면 공개 키를 저장하지 않았거나 저장한 값이 틀렸다. 저장하지 않았으면 새로고침하고, 틀린 값을 저장했으면 [공개 키 지우기]를 누른다. `BOOK_ID`를 바꾸지 않으면 글이 `student01` 방명록에 저장된다. 저장 전에 배정받은 번호로 바꾸고 새로고침한다.

모의 API 리허설에서는 `config.example.js`의 주소를 `http://127.0.0.1:8787`로 바꾸고 공개 키를 묻는 창에 `classroom-local`을 넣는다. 이 브라우저에 다른 키가 저장되어 있으면 먼저 [공개 키 지우기]를 누른다.

## REST Client 준비

VS Code 확장 `humao.rest-client`를 설치한다. 별도 Git 저장소에서 실습할 때는 먼저 저장소 최상위의 `.gitignore`에 `.env` 한 줄을 추가한다. `.env.example`을 같은 폴더의 `.env`로 복사하고 `API_BASE_URL`, `API_PUBLIC_KEY`, `BOOK_ID`를 배부값으로 설정한다. REST Client는 브라우저에 저장한 공개 키를 쓰지 않고 이 `.env`를 따로 읽는다.

[requests.http](requests.http)를 열고 각 요청 위 **Send Request**를 누른다. 접속 확인→도움말→GET을 먼저 보낸다. POST가 반환한 ID를 `.env`의 `MESSAGE_ID`에 적은 뒤 해당 ID 조회·수정·재조회·삭제·재조회 순으로 진행한다.

| 요청 | 필요한 헤더 | 예상 응답 |
|---|---|---|
| about·help·GET | apikey | 200과 JSON 배열 |
| POST | apikey, Content-Type: application/json, Prefer: return=representation | 201과 생성 ID 포함 배열 |
| PATCH | apikey, Content-Type, Prefer | 200과 변경 행 1개, []이면 변경 없음 |
| DELETE | apikey | 204와 빈 본문, 이후 GET 200 [] |

공용 API 키는 요청 파일 옆의 `.env`에서 읽는다.

응답 401·403이면 공개 키와 배부 설정을 확인한다. PATCH `200 []`는 수정 완료가 아니며 방명록 태그·서버 ID를 확인한다. DELETE 204는 본문이 없으므로 JSON을 읽지 않고 같은 ID GET으로 삭제를 확인한다. POST 통신 오류는 저장 여부가 불명확할 수 있어 목록부터 확인한다. REST Client 성공은 브라우저 CORS 성공과 별도로 기록한다.

## 조립과 조회 정책

학생 수정은 세 section 조립·hash 연결·ID 구별이다. 홈은 `home-count`·`home-count-button`·`homeCount`·`homeCountBox`, 방명록은 기존 `count`·`countBox`를 쓴다. 제공 REST 오류 처리의 재작성은 요구하지 않는다. `config.example.js`에서는 `BOOK_ID`만 바꾼다.

초기화는 모든 DOM·함수·이벤트 준비 뒤 `showRoute()`, `loadMessages()` 순서다. 화면을 10회 오가도 이벤트가 중복 등록되지 않는다. 최초 실행, 새로 불러오기, 쓰기 뒤 확인에서 GET하며 단순 화면 전환은 GET하지 않는다.

화면 전환 시 초안·편집 입력·홈 횟수가 남는다. 새로고침 시 메모리 상태는 초기화된다. 서버에 저장한 글과 localStorage의 공개 키는 새로고침해도 남는다. 방명록 밖에 있는 동안 완료된 요청도 같은 DOM의 목록을 갱신한다.

## 확인 절차

빈 hash·등록 hash·없는 hash, 직접 주소·새로고침·뒤로/앞으로를 확인한다. Tab과 Enter로 메뉴를 조작하고 현재 메뉴 `aria-current`, title, 제목 포커스를 확인한다. 초안을 쓴 뒤 10회 전환하고 POST 한 번으로 글 하나만 생기는지 확인한다.

세 글 중 가운데 ID를 수정·삭제하고 나머지 글을 확인한다. 없는 글 번호·Offline·복구 재조회를 시험한다. 375px과 1280px에서 가로 넘침을 확인한다. 예제 폴더를 서버 루트로 연 `/index.html#guestbook`과 프로젝트 하위 경로에서 같은 시험을 한다. 주소(출처)가 바뀌면 처음 열 때 묻는 창에 공개 키를 다시 넣는다. 공용 API·GitHub Pages·다른 기기는 로컬 리허설과 구분하여 따로 검증한다.

## 파일 배포

`index.html`, `app.js`, `config.example.js`, `README.md`, `requests.http`, `.env.example`을 배포한다. 실제 `.env`는 제외한다. CSS는 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`에서 읽는다.
