# ID별 GET 확인

강의자 시연·선택 확인 예제다. ID 입력 뒤 다시 읽기를 누르면 해당 객체 배열 또는 빈 배열이 나온다.

수정 전·후 같은 ID의 결과를 비교한다. 14주 30분 필수 수정량에는 이 파일 전체 작성을 포함하지 않는다.

이 폴더의 requests.http에는 about → help → 목록 → 대상 GET만 있다. 변경은 ex02·ex03 또는 완성본에서 실행하고 이 예제로 같은 ID를 다시 조회한다.

## 실행과 설정

폴더를 정적 서버로 연다. 화면은 CDN의 [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다.

화면의 API 설정에서 API 주소·공개 키·방명록 번호를 입력하고 설정 적용을 누른다. 기본값은 로컬 API http://127.0.0.1:8787, 가상 공개 키 classroom-local, student01이다. 공용 HTTPS 값은 실행 중 메모리에서만 사용하므로 새로고침 뒤 다시 입력한다. 서버 비밀 키를 입력하지 않는다. 편집 키는 별도 실행 입력이며 소스·저장소·URL·캡처에 넣지 않는다. 설정을 바꾸면 대상 ID와 입력도 다시 지정한다.

## VS Code REST Client

REST Client 확장 humao.rest-client를 설치한다. 별도 Git 저장소를 쓴다면 최상위 `.gitignore`에 `.env`를 추가한다. `.env.example`을 같은 폴더의 `.env`로 복사해 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 배포 ZIP에서는 실제 `.env`를 제외한다. 브라우저 설정 패널과 .env는 별개이므로 각각 설정한다.

[requests.http](requests.http)를 열고 각 요청 위 **Send Request**를 눌러 about → help → 목록 → 대상 GET → 변경 요청 → 같은 ID 재조회 순서로 진행한다. 목록에서 자기 글 ID를 읽어 .env의 MESSAGE_ID를 바꾼다. 편집 키는 예약 이름 password의 마스킹 프롬프트로 입력한다. 모든 요청의 apikey, PATCH·DELETE의 X-Edit-Key 헤더를 확인한다. PATCH에는 Content-Type과 Prefer도 필요하다.

about·help·GET은 200과 JSON 배열, PATCH는 200과 변경 배열, DELETE는 204와 빈 본문을 확인한다. PATCH 200 []와 DELETE 204만으로 실제 변경을 판단하지 않는다. 동일 ID의 GET에서 메시지 또는 부재를 확인한다. 틀린 편집 키는 변경이 없는 결과여야 한다. 통신 오류 뒤에는 다시 쓰기 전에 GET으로 상태를 확인한다.
