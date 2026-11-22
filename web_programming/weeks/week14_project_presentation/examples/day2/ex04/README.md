# ID별 GET 확인

강의자 시연·선택 확인 예제다. ID 입력 뒤 다시 읽기를 누르면 해당 객체 배열 또는 빈 배열이 나온다.

수정 전·후 같은 ID의 결과를 비교한다. 14주 30분 필수 수정량에는 이 파일 전체 작성을 포함하지 않는다.

이 폴더의 requests.http에는 about → help → 목록 → 대상 GET만 있다. 변경은 ex02·ex03 또는 완성본에서 실행하고 이 예제로 같은 ID를 다시 조회한다.

## 실행과 설정

폴더를 정적 서버로 연다. 화면은 CDN의 [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다.

config.example.js의 `const BOOK_ID = 'student01';`에서 student01을 배정받은 방명록 번호로 바꾼다. 바꾸지 않으면 student01 방명록에 요청한다. 주소는 수업용 서버다. 공개 키는 파일에 적지 않는다. 예제를 처음 열면 '배부받은 공개 키를 입력하세요.' 창이 뜬다. 이 창에는 편집 키가 아니라 강의자가 배부한 공개 키를 넣는다. 키는 이 브라우저의 localStorage에 저장되고 같은 주소에서 연 다른 예제도 함께 쓴다. 창을 취소하거나 빈 칸으로 두면 키가 저장되지 않아 서버가 HTTP 401을 돌려주고 화면에 확인 실패가 보인다. 새로고침하면 다시 묻는다. 키를 잘못 넣었거나 강의자가 키를 바꾸면 제목 아래 [공개 키 지우기]를 누른다. 버튼이 저장한 키를 지우고 새로고침하면 다시 묻는 창에 새 키를 넣는다. localStorage는 주소(출처)마다 따로이므로 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소, 휴대폰에서는 처음 한 번 묻는다.

localStorage에는 배부받은 공개 키만 저장하고 서버 비밀 키는 넣지 않는다. 편집 키는 별도 실행 입력이며 소스·저장소·URL·localStorage·캡처에 넣지 않는다. 강의자가 로컬 API로 리허설할 때는 config.example.js의 주소를 `http://127.0.0.1:8787`로 바꾸고 [공개 키 지우기]를 누른 뒤 다시 묻는 창에 `classroom-local`을 넣는다. 리허설이 끝나면 주소를 수업용 서버로 되돌리고 [공개 키 지우기]를 누른 뒤 배부받은 공개 키를 다시 넣는다.

## VS Code REST Client

REST Client 확장 humao.rest-client를 설치한다. 별도 Git 저장소를 쓴다면 최상위 `.gitignore`에 `.env`를 추가한다. `.env.example`을 같은 폴더의 `.env`로 복사해 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 배포 ZIP에서는 실제 `.env`를 제외한다. 브라우저가 읽는 config.example.js·localStorage와 .env는 별개이므로 각각 설정한다.

[requests.http](requests.http)를 열고 각 요청 위 **Send Request**를 눌러 about → help → 목록 → 대상 GET → 변경 요청 → 같은 ID 재조회 순서로 진행한다. 목록에서 자기 글 ID를 읽어 .env의 MESSAGE_ID를 바꾼다. 편집 키는 예약 이름 password의 마스킹 프롬프트로 입력한다. 모든 요청의 apikey, PATCH·DELETE의 X-Edit-Key 헤더를 확인한다. PATCH에는 Content-Type과 Prefer도 필요하다.

about·help·GET은 200과 JSON 배열, PATCH는 200과 변경 배열, DELETE는 204와 빈 본문을 확인한다. PATCH 200 []와 DELETE 204만으로 실제 변경을 판단하지 않는다. 동일 ID의 GET에서 메시지 또는 부재를 확인한다. 틀린 편집 키는 변경이 없는 결과여야 한다. 통신 오류 뒤에는 다시 쓰기 전에 GET으로 상태를 확인한다.
