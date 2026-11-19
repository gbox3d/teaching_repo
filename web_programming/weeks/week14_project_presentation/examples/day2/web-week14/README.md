# 온라인 방명록 수정·삭제 참고본

13주 GET·POST를 이어 받아 guestbook.js 하나에 GET·POST·DELETE·PATCH를 구분했다. [따라하기](../../../walkthrough.md)와 [실습지](../../../lab.md)를 사용한다. 레포트 템플릿이 아니다.

1일차 학생 수정은 DELETE 대상 URL·method·헤더 3곳, 2일차는 PATCH 대상 URL·JSON 본문·같은 ID 재조회 3곳이다. 폼 선택·키 처리·설정·초기화·경쟁 응답 보호·오류 복구는 제공 코드다. 모든 함수와 이벤트를 준비한 뒤 파일 끝에서 setupApiSettings와 최초 loadMessages를 실행한다.

키 적용은 메모리로 값을 옮기고 입력 칸을 비운다. 키 지우기는 메모리 값도 지운다. API 설정을 적용하면 새 글 폼·편집 폼·선택 ID·편집 키가 지워진다. 이전 설정의 진행 중 요청은 서버에서 완료될 수 있지만 새 화면의 폼·안내를 덮지 않는다. 이전 결과는 이전 설정으로 돌아가 GET으로 확인한다.

## 기본 배포 파일

index.html, about.html, guestbook.html, app.js, guestbook.js, api-settings.js, styles.css, shared/examples.css, images/profile.png, README.md, requests.http, .env.example, .gitignore를 복사한다. 독립 폴더 실행을 위해 shared 폴더도 포함한다.

config.example.js·submit.js·actions.js·delete.js·edit.js는 이동 안내만 남겼고 HTML에서 읽지 않는다. projects.html·projects.js·about.js, data/projects.json, images/project1.png~project3.png, images/site-map.svg, screenshots의 이전 자료는 기본 배포에서 제외한다. 프로젝트 옛 주소는 짧은 안내로 남긴다. 홈·내 정보는 기존 HTML·CSS·홈 JS를 유지한다.

## 실행과 설정

폴더째 복사해 정적 서버로 연다. [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)은 CDN에서 읽고 추가 스타일은 shared/examples.css에 둔다. api-settings.js는 제공 파일이며 재구현하지 않는다.

화면의 API 설정에서 API 주소·공개 키·방명록 번호를 입력하고 설정 적용을 누른다. 기본값은 로컬 API http://127.0.0.1:8787, 가상 공개 키 classroom-local, student01이다. 공용 HTTPS 값은 실행 중 메모리에서만 사용하므로 새로고침 뒤 다시 입력한다. 서버 비밀 키를 입력하지 않는다. 편집 키는 별도 실행 입력이며 소스·저장소·URL·캡처에 넣지 않는다. 설정을 바꾸면 대상 ID와 입력도 다시 지정한다.

## VS Code REST Client

REST Client 확장 humao.rest-client를 설치한다. .env.example을 같은 폴더의 .env로 복사해 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. .env는 .gitignore 대상이며 배포 ZIP에 넣지 않는다. 브라우저 설정 패널과 .env는 별개이므로 각각 설정한다.

[requests.http](requests.http)를 열고 각 요청 위 **Send Request**를 눌러 about → help → 목록 → 대상 GET → 변경 요청 → 같은 ID 재조회 순서로 진행한다. 목록에서 자기 글 ID를 읽어 .env의 MESSAGE_ID를 바꾼다. 편집 키는 예약 이름 password의 마스킹 프롬프트로 입력한다. 모든 요청의 apikey, PATCH·DELETE의 X-Edit-Key 헤더를 확인한다. PATCH에는 Content-Type과 Prefer도 필요하다.

about·help·GET은 200과 JSON 배열, PATCH는 200과 변경 배열, DELETE는 204와 빈 본문을 확인한다. PATCH 200 []와 DELETE 204만으로 실제 변경을 판단하지 않는다. 동일 ID의 GET에서 메시지 또는 부재를 확인한다. 틀린 편집 키는 변경이 없는 결과여야 한다. 통신 오류 뒤에는 다시 쓰기 전에 GET으로 상태를 확인한다.
