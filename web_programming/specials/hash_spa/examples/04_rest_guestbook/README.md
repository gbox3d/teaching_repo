# 04 14주 CRUD를 Hash SPA에 합친다

[완성 화면](index.html)은 홈·내 정보·방명록을 한 문서에 둔다. 방명록 폼·목록·편집 영역과 GET·POST·PATCH·DELETE는 [14주 완성본](../../../../weeks/week14_project_presentation/examples/day2/web-week14/README.md)을 재사용한다. 설정은 제공 `api-settings.js`, 동작은 `app.js` 하나다. 03의 미리 보기 코드는 제거하고 서버 방명록으로 교체했다.

## 로컬 실행

저장소 루트의 두 터미널에서 실행한다. 이미 같은 서버가 실행 중이면 새로 시작하지 않는다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

```bash
node web_programming/tools/guestbook-api/server.mjs
```

주소는 `http://localhost:8111/specials/hash_spa/examples/04_rest_guestbook/index.html#guestbook`이다. API 기본값은 `http://127.0.0.1:8787`, 가상 공개 키 `classroom-local`, 방명록 번호 `student01`이다. 로컬 편집 키는 강의자가 별도로 배부한다. 브라우저 API 설정 패널은 실행 중 값만 보관한다. 공용 환경은 강의자가 배부한 HTTPS 주소·공개 키·방명록 번호를 입력하고 설정 적용을 누른다. 새로고침 뒤에는 다시 입력한다.

## REST Client 준비

VS Code 확장 `humao.rest-client`를 설치한다. `.env.example`을 같은 폴더의 `.env`로 복사하고 `API_BASE_URL`, `API_PUBLIC_KEY`, `BOOK_ID`를 배부값으로 설정한다. `.gitignore`도 함께 복사하여 실제 `.env`가 추적되지 않게 한다. 브라우저 설정과 REST Client 설정은 별개다.

[requests.http](requests.http)를 열고 각 요청 위 **Send Request**를 누른다. 접속 확인→도움말→GET을 먼저 보낸다. POST가 반환한 ID를 `.env`의 `MESSAGE_ID`에 적은 뒤 해당 ID 조회·수정·재조회·삭제·재조회 순으로 진행한다.

| 요청 | 필요한 헤더 | 예상 응답 |
|---|---|---|
| about·help·GET | apikey | 200과 JSON 배열 |
| POST | apikey, Content-Type: application/json, Prefer: return=representation | 201과 생성 ID 포함 배열 |
| PATCH | 위 헤더와 X-Edit-Key | 200과 변경 행 1개, []이면 변경 없음 |
| DELETE | apikey, X-Edit-Key | 204와 빈 본문, 이후 GET 200 [] |

편집 키는 `# @prompt password`의 마스킹 입력창에 넣는다. 이름 `password`는 REST Client의 마스킹 예약 이름이며 `editKey`로 바꾸지 않는다. 실제 편집 키·서버 비밀 키를 요청 파일이나 소스에 적지 않는다. 공개 키도 추적 파일에는 로컬 가상 값만 둔다.

응답 401·403이면 공개 키와 배부 설정을 확인한다. PATCH `200 []`는 수정 완료가 아니며 편집 키·서버 ID를 확인한다. DELETE 204는 본문이 없으므로 JSON을 읽지 않고 같은 ID GET으로 삭제를 확인한다. POST 통신 오류는 저장 여부가 불명확할 수 있어 목록부터 확인한다. REST Client 성공은 브라우저 CORS 성공과 별도로 기록한다.

## 조립과 조회 정책

학생 수정은 세 section 조립·hash 연결·ID 구별이다. 홈은 `home-count`·`home-count-button`·`homeCount`·`homeCountBox`, 방명록은 기존 `count`·`countBox`를 쓴다. 제공 REST 오류 처리·설정 패널의 재작성은 요구하지 않는다.

초기화는 모든 DOM·함수·이벤트 준비 뒤 `showRoute()`, `setupApiSettings(...)`, `loadMessages()` 순서다. 화면을 10회 오가도 이벤트가 중복 등록되지 않는다. 최초 실행, 설정 적용, 새로 불러오기, 쓰기 뒤 확인에서 GET하며 단순 화면 전환은 GET하지 않는다.

화면 전환 시 초안·편집 입력·홈 횟수가 남는다. 새로고침 시 메모리 상태는 초기화된다. 서버 글은 남지만 공용 설정과 편집 키는 다시 입력해야 한다. 설정 적용은 작업 대상을 바꾸므로 초안·편집 폼·편집 키를 초기화한다. 방명록 밖에 있는 동안 완료된 요청도 같은 DOM의 목록을 갱신한다.

## 확인 절차

빈 hash·등록 hash·없는 hash, 직접 주소·새로고침·뒤로/앞으로를 확인한다. Tab과 Enter로 메뉴를 조작하고 현재 메뉴 `aria-current`, title, 제목 포커스를 확인한다. 초안을 쓴 뒤 10회 전환하고 POST 한 번으로 글 하나만 생기는지 확인한다.

세 글 중 가운데 ID를 수정·삭제하고 나머지 글을 확인한다. 틀린 편집 키·Offline·복구 재조회를 시험한다. 375px과 1280px에서 가로 넘침을 확인한다. 예제 폴더를 서버 루트로 연 `/index.html#guestbook`과 프로젝트 하위 경로에서 같은 시험을 한다. 공용 API·GitHub Pages·다른 기기는 로컬 리허설과 구분하여 따로 검증한다.

## 파일 배포

`index.html`, `app.js`, `api-settings.js`, `shared/examples.css`, `README.md`, `requests.http`, `.env.example`, `.gitignore`가 한 묶음이다. 실제 `.env`와 편집 키는 제외한다. CSS는 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`와 로컬 `shared/examples.css`다.
