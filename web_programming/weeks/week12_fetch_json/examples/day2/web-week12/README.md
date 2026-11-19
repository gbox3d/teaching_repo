# 12주차 온라인 방명록

`guestbook.html`은 서버 목록을 읽는다. `guestbook.local.html`·`guestbook.local.js`는 11주 제공 로컬 저장본을 보존한다. 11주 필수 실습 결과는 ex06의 폼 한 객체 저장·복원이며, 객체 배열 방명록 전체는 강의자가 제공한 시연본이다. 서버 목록을 읽어도 로컬 저장 값은 옮기거나 지우지 않는다.

홈·내 정보·홈 JS·기존 CSS·프로필 그림은 11주 파일을 이어 쓴다. 12주 데이터 동작은 `guestbook.js` 하나에 있고, 제공 `api-settings.js`를 먼저 읽는다. 로컬 보관 화면은 별도 JS로 독립 실행한다.

새로 불러오기는 GET을 보낸다. 성공 시 최근 글 수와 목록이 같고, 빈 응답은 0개 안내가 보인다. 실패하면 오래된 목록을 지우고 실패 안내를 표시한다. 연결 복구 뒤 다시 불러오기를 누른다. 목록은 최대 50개이며 서버 전체 개수가 아니다.

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

## 자료 자산

`images/profile.png`는 홈에서 사용한다. `images/project1.png`~`project3.png`와 `site-map.svg`는 이전 주 인계 자료다. `screenshots/home.png`는 홈 예시이며 `screenshots/guestbook.png`는 이번 로컬 서버 목록 화면으로 갱신했다. 제공 화면 그림은 개인 제출 증거가 아니므로 제출 캡처는 현재 서버 목록과 GET 200으로 새로 만든다. 기본 실행 파일은 세 페이지·동작 JS·설정 JS·styles.css·프로필이며 로컬 보관본도 함께 배부한다.

## 설정 변경 중 이전 응답

latestRequest/requestId 비교는 제공 코드다. 설정 적용으로 새 요청이 시작되면 이전 요청은 목록·오류 안내·버튼 상태를 갱신하지 않는다. 학생의 직접 구현 범위에 포함하지 않는다.
