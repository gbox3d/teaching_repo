# DELETE와 대상 재조회

강의자 시연 뒤 필요한 요청 부분만 수정한다. 자기 연습 글 ID와 편집 키를 입력한다. 빈 키는 전송하지 않는다. 키 입력 칸은 요청 직전에 비운다. 성공은 같은 ID의 GET까지 확인한 결과다.

학생 수정은 대상 URL·DELETE 메서드·헤더 3곳이다. 재조회·초기화·중복 클릭·설정 변경 방어는 제공 코드다.

## 실행과 설정

폴더째 복사해 정적 서버로 연다. [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)은 CDN에서 읽고 추가 스타일은 shared/examples.css에 둔다. api-settings.js는 제공 파일이며 재구현하지 않는다.

화면의 API 설정에서 API 주소·공개 키·방명록 번호를 입력하고 설정 적용을 누른다. 기본값은 로컬 API http://127.0.0.1:8787, 가상 공개 키 classroom-local, student01이다. 공용 HTTPS 값은 실행 중 메모리에서만 사용하므로 새로고침 뒤 다시 입력한다. 서버 비밀 키를 입력하지 않는다. 편집 키는 별도 실행 입력이며 소스·저장소·URL·캡처에 넣지 않는다. 설정을 바꾸면 대상 ID와 입력도 다시 지정한다.

## VS Code REST Client

REST Client 확장 humao.rest-client를 설치한다. .env.example을 같은 폴더의 .env로 복사해 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. .env는 .gitignore 대상이며 배포 ZIP에 넣지 않는다. 브라우저 설정 패널과 .env는 별개이므로 각각 설정한다.

[requests.http](requests.http)를 열고 각 요청 위 **Send Request**를 눌러 about → help → 목록 → 대상 GET → 변경 요청 → 같은 ID 재조회 순서로 진행한다. 목록에서 자기 글 ID를 읽어 .env의 MESSAGE_ID를 바꾼다. 편집 키는 예약 이름 password의 마스킹 프롬프트로 입력한다. 모든 요청의 apikey, PATCH·DELETE의 X-Edit-Key 헤더를 확인한다. PATCH에는 Content-Type과 Prefer도 필요하다.

about·help·GET은 200과 JSON 배열, PATCH는 200과 변경 배열, DELETE는 204와 빈 본문을 확인한다. PATCH 200 []와 DELETE 204만으로 실제 변경을 판단하지 않는다. 동일 ID의 GET에서 메시지 또는 부재를 확인한다. 틀린 편집 키는 변경이 없는 결과여야 한다. 통신 오류 뒤에는 다시 쓰기 전에 GET으로 상태를 확인한다.
