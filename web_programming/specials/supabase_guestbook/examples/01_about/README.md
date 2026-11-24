# API 접속 확인

접속 확인을 누르면 GET 200과 안내 객체 한 개의 배열이 나온다. name·version·help_path를 확인한다.

## 설정과 실행

브라우저는 이 폴더의 `config.example.js`에서 `API_BASE_URL`과 `BOOK_ID`를 읽는다. 자기 프로젝트를 사용하면 프로젝트 URL과 등록된 태그를 넣는다.

화면을 처음 열면 공개 키를 묻는 창에 배부받은 키를 넣는다. 키를 잘못 넣었거나 새 프로젝트의 publishable key로 바꿀 때는 제목 아래 **공개 키 지우기**를 누르고 새 키를 넣는다. 자세한 내용은 [공개 키 입력과 지우기](../README.md#공개-키-입력과-지우기)에 있다.

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/supabase_guestbook/examples 8000
```

화면: http://localhost:8000/01_about/

## REST Client

VS Code REST Client (humao.rest-client)를 설치한다. 같은 폴더의 .env.example을 .env로 복사하고 API_BASE_URL·API_PUBLIC_KEY·BOOK_ID를 설정한다. 브라우저는 .env를 읽지 않는다. [requests.http](requests.http)의 **Send Request**를 누르고 주석의 상태 번호·응답을 확인한다. 처음에는 [01 접속](../01_about/README.md)과 [02 도움말](../02_help/README.md)을 먼저 수행한다.

공개 키는 `apikey` 헤더로 보낸다. GET 응답의 상태 번호와 JSON 배열을 확인한다.

## 화면과 배포

이 폴더를 그대로 배포한다. 스타일은 [W3.CSS 4.1.0](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 CDN에서 읽는다.

[전체 설정·HTTPS·배포 안내](../README.md) · [연구 실습](../../lab.md)
