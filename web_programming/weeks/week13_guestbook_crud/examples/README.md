# 13주차 방명록 CRUD 예제

| 실습 폴더 | 브라우저 화면 | VS Code REST Client |
|---|---|---|
| [day1/ex01_create](day1/ex01_create/README.md) | [글 생성 · 저장](day1/ex01_create/index.html) | [접속 준비 후 POST](day1/ex01_create/requests.http) |
| [day1/ex02_read](day1/ex02_read/README.md) | [글 조회 · 목록 보기](day1/ex02_read/index.html) | [GET](day1/ex02_read/requests.http) |
| [day2/ex03_update](day2/ex03_update/README.md) | [메시지 수정](day2/ex03_update/index.html) | [PATCH와 수정 확인](day2/ex03_update/requests.http) |
| [day2/ex04_delete](day2/ex04_delete/README.md) | [글 삭제](day2/ex04_delete/index.html) | [DELETE와 삭제 확인](day2/ex04_delete/requests.http) |
| [day2/web-week13](day2/web-week13/README.md) | [완성 방명록](day2/web-week13/guestbook.html) | [한 글의 CRUD 요청](day2/web-week13/requests.http) |

첫 단계에서 받은 글 번호를 나머지 세 단계에서도 사용한다. 브라우저는 각 폴더의 `config.example.json`을 `config.json`으로, REST Client는 `.env.example`을 `.env`로 복사한다. 네 예제에 같은 주소·공개 키·방명록 태그를 넣는다. [설정 및 실행](../walkthrough.md#2-rest-client와-브라우저-설정)

예제 화면은 [W3.CSS 4.1.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용한다.
