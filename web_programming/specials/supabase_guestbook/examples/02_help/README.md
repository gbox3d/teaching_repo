# API 사용법 조회

사용법 조회를 누르면 GET 200과 단계 1~6의 안내 배열이 나온다. 화면 목록도 여섯 항목이다.

## 설정과 실행

브라우저는 이 폴더의 config.example.js에서 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 읽는다. 새 프로젝트를 구축했다면 세 값을 자신의 서버로 바꾼다. 공개 publishable key만 사용하고 DB 비밀번호·service_role·편집 키를 이 파일에 넣지 않는다. 정규 12~14주의 실행 중 설정 패널과는 다른 방식이다.

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/supabase_guestbook/examples 8000
```

화면: http://localhost:8000/02_help/

## REST Client

VS Code REST Client (humao.rest-client)를 설치한다. 같은 폴더의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 브라우저는 .env를 읽지 않는다. [requests.http](requests.http)의 **Send Request**를 누르고 주석의 상태 번호·응답을 확인한다. 처음에는 [01 접속](../01_about/README.md)과 [02 도움말](../02_help/README.md)을 먼저 수행한다.

모든 요청의 apikey 헤더, POST·PATCH의 Content-Type: application/json을 구분한다. 편집 요청은 password prompt에 편집 키를 넣으며 요청마다 다시 입력한다. 실제 키를 요청 파일에 적지 않는다. 실행 후 REST Client의 Clear Request History로 키가 담긴 이력을 정리한다.

## 화면과 배포

7주에서 배운 W3.CSS를 cdnjs 4.1.0 고정 CDN으로 읽고 이 폴더의 shared/examples.css를 추가한다. CDN에는 인터넷 연결이 필요하다. 이 폴더 전체의 상대 위치를 유지하면 독립적으로 배포할 수 있다. styles.css는 이전 배부 경로의 호환 파일이다. 긴 설명은 이 문서에서 읽고 화면에서 입력·응답을 확인한다.

[전체 설정·HTTPS·배포 안내](../README.md) · [연구 실습](../../lab.md)
