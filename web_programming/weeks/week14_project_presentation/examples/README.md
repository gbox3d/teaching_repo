# 14주차 예제 안내

1일차 DELETE, 2일차 PATCH를 다룬다. 양일 강의·시연 60분+학생 실습 30분이다. 비교 예제는 폴더째 배부하며 전체 재입력은 필수가 아니다.

| 예제 | 구분 | 확인·학생 수정 |
|---|---|---|
| [day1/ex01](day1/ex01/index.html) | 강의자 시연 | 배열 순서를 바꿔 인덱스와 서버 ID 비교 |
| [day1/ex02](day1/ex02/index.html) | DELETE 비교·필수 수정 참고 | 대상 URL·method·헤더 3곳 |
| [day2/ex03](day2/ex03/index.html) | PATCH 비교·필수 수정 참고 | 대상 URL·JSON 본문·같은 ID 재조회 3곳 |
| [day2/ex04](day2/ex04/index.html) | 시연·선택 | 같은 ID의 변경 전·후 GET |
| [web-week14](day2/web-week14/guestbook.html) | 제공 조립본·실습 결과 | guestbook.js에서 양일 지정한 3곳씩 수정 |

각 REST 폴더에는 `README.md`, `requests.http`, `.env.example`이 있다. 예제만 새 Git 저장소에 복사했다면 그 저장소 최상위의 `.gitignore`에 `.env` 한 줄을 추가한다. REST Client humao.rest-client에서 .env를 준비하고 **Send Request**로 about → help → GET → 변경 → 같은 ID GET을 진행한다. 실제 편집 키는 password 프롬프트로 입력한다. 브라우저가 읽는 config.example.js와 .env는 별개다. 공개 키는 예제를 여는 주소마다 처음 한 번 묻는 창에 넣으며 새로고침해도 남는다. 잘못 넣었으면 제목 아래 [공개 키 지우기]를 누르고 다시 넣는다.

## 제공 코드와 배포

config.example.js는 API 주소·방명록 번호를 정하고, 공개 키를 처음 한 번 물어 localStorage에 저장하며 [공개 키 지우기] 버튼 동작을 붙이는 설정 파일, guestbook.js는 GET·POST·PATCH·DELETE 전체 동작이다. 키·초기화·실패 복구·늦은 응답 보호는 제공 코드이며 평가 대상이 아니다. REST 예제는 [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 CDN에서 읽는다. 홈·내 정보는 styles.css를 쓴다.

완성본 기본 배포 파일은 [완성본 README](day2/web-week14/README.md#기본-배포-파일)에 명시했다. 옛 다중 동작 JS는 이동 안내만 남겼고 HTML에서 읽지 않는다. 이전 projects.html·projects.js·about.js와 프로젝트 데이터·그림·옛 캡처는 배포하지 않는다. day1/ex03 저장 예제는 11주 이동 안내로 남겼으며 현재 14주 실습이 아니다. day1/ex02/message.json도 이전 부속 파일로 배포에서 제외한다.
