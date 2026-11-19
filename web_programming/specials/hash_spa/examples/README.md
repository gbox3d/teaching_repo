# Hash SPA 예제 목록

각 폴더는 HTML·동작 JS·README·`shared/examples.css`를 포함한다. 아래 순서로 실행하며 이 폴더 자체에는 실행용 HTML을 두지 않는다.

| 폴더 | 시작 화면 | 차이 |
|---|---|---|
| [01_mpa](01_mpa/README.md) | [index.html](01_mpa/index.html) | index.html·about.html·guestbook.html 실제 파일 이동 |
| [02_two_screens](02_two_screens/README.md) | [index.html](02_two_screens/index.html) | 주소 변경 없는 두 section 전환 |
| [03_hash_routes](03_hash_routes/README.md) | [index.html](03_hash_routes/index.html) | 세 hash 경로·입력 미리 보기 |
| [04_rest_guestbook](04_rest_guestbook/README.md) | [index.html](04_rest_guestbook/index.html) | 14주 서버 CRUD와 API 설정 제공본 통합 |

01~03의 방명록 미리 보기는 저장 기능이 아니다. 04부터 서버 요청이 발생하며 [requests.http](04_rest_guestbook/requests.http)의 about·help·GET을 먼저 확인한다.

W3.CSS 주소는 `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`로 고정했다. 폴더를 단독 배부할 때 해당 폴더 전체를 복사한다. 04의 `.env.example`과 `.gitignore`를 포함하되 실제 `.env`·키는 배포하지 않는다.
