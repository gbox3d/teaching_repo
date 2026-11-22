# 방명록 예제의 API 설정

정본은 `web_programming/shared/api-settings.js`다. 방명록의 설정 패널을 쓰는 폴더에 같은 파일을 `api-settings.js`로 복사한다. HTML은 이 파일 다음에 `app.js` 또는 `guestbook.js`를 `defer`로 읽는다. 독립 배포 시 두 파일과 HTML을 함께 복사한다.

## 변수와 함수

| 이름 | 기본값·역할 |
|---|---|
| `API_BASE_URL` | 12주 선택 방명록과 13주 방명록은 주소 입력란의 수업용 HTTPS 기본값, 주소가 지정되지 않은 예제는 리허설용 `http://127.0.0.1:8787` |
| `API_PUBLIC_KEY` | 12주 선택 방명록과 13주 방명록은 배부받은 공개 키 입력, 리허설 기본값은 `classroom-local`. 요청의 `apikey` 헤더에 사용 |
| `BOOK_ID` | `student01`, 요청의 `book_id` 필터·POST 본문 |
| `setupApiSettings(onApply)` | 폼 기본값과 submit 리스너 등록. 적용 후 콜백 실행 |

12주 선택 방명록은 `setupApiSettings(loadMessages);`로 폼을 준비한 뒤 학생이 설정을 적용하면 첫 GET을 보낸다. 13주 REST 예제는 설정 적용 뒤에 저장 버튼이나 폼을 쓴다. 리허설 기본값을 쓰는 14주 완성본은 초기화 뒤 바로 목록을 조회한다. 설정을 바꾸면 적용 콜백에서 다시 조회한다.

## HTML 계약

| 요소 | ID·조건 |
|---|---|
| 제공 폼 | `api-settings-form`, `autocomplete="off"` |
| API 주소 | `api-base-url`, `type="url"`, `required` |
| 공개 키 | `api-public-key`, `type="password"`, `required` |
| 방명록 번호 | `api-book-id`, `required`, `pattern="[a-z0-9_-]{1,40}"` |
| 적용 버튼 | 폼 안의 `button[type="submit"]`, ‘설정 적용’ |
| 설정 안내 | `api-settings-notice`, `role="status"` |

목록 계약은 `list`, `count`, `load-notice`, `reload-button`, `showList(items)`, `loadMessages()`다. `loadMessages()`는 성공 시 true, 실패 시 false를 반환한다. 13주 입력 폼은 `guestbook-form`, `name`, `message`, `notice`를 이어 쓴다. `email`을 서버 본문에 넣지 않는다.

## 저장과 배포

12주 선택 방명록과 13주 방명록 HTML의 주소 입력란과 `.env.example`에 수업용 기본 주소를 제공한다. 실행 중 입력한 공개 키와 방명록 번호는 브라우저 메모리에만 두며 새로고침하면 해당 예제의 초기값으로 돌아간다. 편집 키는 별도로 14주 입력에서 메모리만 사용한다.

기존 `config.example.js`는 이동 안내 주석만 유지하고 HTML에서 읽지 않는다. 학생은 설정 패널을 재구현하지 않으며 요청 URL·헤더·본문·응답 처리만 수정한다.

## REST Client 계약

각 폴더의 `.env.example`을 `.env`로 복사한다. `API_BASE_URL`, `API_PUBLIC_KEY`, `BOOK_ID`를 `{{$dotenv API_BASE_URL}}` 형식으로 요청에서 읽는다. 교재 루트 `.gitignore`에서 `.env`를 제외하고 ZIP에는 `.env.example`만 담는다. 별도 학생 저장소도 그 저장소 루트에 같은 환경 파일 제외 규칙을 둔다. 편집 키는 `.http`의 `# @prompt password`로 입력하고 `{{password}}`로 참조한다. REST Client에서 마스킹되는 예약 프롬프트 이름을 사용하며 설명에 편집 키라고 표시한다. 브라우저 패널과 REST Client의 `.env`는 서로 별개이며 둘 다 설정해야 한다. 12주 선택 방명록은 about → help → 목록 GET, 13주는 POST → 저장 결과 확인 순서로 해당 요청 위 **Send Request**를 누른다.

## 요청 순서 보호

조회 동작 JS는 `let latestRequest = 0`을 두고 `loadMessages()` 첫 줄에서 `const requestId = ++latestRequest`를 기록한다. JSON 수신 뒤와 catch에서 현재 번호가 다르면 false를 반환한다. finally는 번호가 같은 요청만 조회 버튼을 활성화한다. 설정 적용 중 늦게 끝난 이전 요청이 새 목록이나 안내를 덮지 않게 하는 제공 코드이며 학생 구현 과제에 넣지 않는다. 요청 URL과 헤더는 첫 await 전에 현재 설정으로 구성한다.
