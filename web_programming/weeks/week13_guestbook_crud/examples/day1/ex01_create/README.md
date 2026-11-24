# 1. Create · 글 저장 (POST)

이 폴더의 `config.example.json`을 `config.json`으로 복사한다. `API_BASE_URL`에는 수업 주소가 들어 있다. `API_PUBLIC_KEY`에 배부받은 공개 키, `BOOK_ID`에 자기 방명록 태그를 적는다. 정적 서버에서 [실습 화면](index.html)을 연다.

별칭과 메시지를 입력하고 **저장**을 누른다. 서버가 발급한 글 번호(`id`)를 적어 둔다. 다음 [조회 단계](../ex02_read/README.md)에서 같은 번호를 찾는다.

## REST Client

VS Code REST Client(`humao.rest-client`)를 설치한다. 이 폴더의 `.env.example`을 `.env`로 복사하고 브라우저와 같은 세 값을 넣는다. [requests.http](requests.http)에서 요청 위의 **Send Request**를 누른다.

1. 처음 연결할 때 서버 소개(`/rest/v1/about`)와 도움말(`/rest/v1/help`)이 `200`으로 열리는지 확인한다.
2. POST 요청의 JSON 본문에 `book_id`, `name`, `message`를 보낸다. 헤더에는 공개 키(`apikey`), `Content-Type: application/json`, `Prefer: return=representation`을 넣는다.
3. `201 Created` 응답의 첫 항목에서 `id`를 찾는다. POST를 실행할 때마다 새 글 한 건이 생긴다.
