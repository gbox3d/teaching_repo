# 2. Read · 목록 조회 (GET)

[생성 단계](../ex01_create/README.md)에서 쓴 `config.json`을 이 폴더에 복사한다. 수업 주소(`API_BASE_URL`), 공개 키(`API_PUBLIC_KEY`), 방명록 태그(`BOOK_ID`)가 같아야 같은 글을 볼 수 있다.

정적 서버에서 [실습 화면](index.html)을 열고 **목록 보기**를 누른다. 방금 기록한 글 번호를 찾아 별칭과 메시지를 확인한다. 다음 [수정 단계](../../day2/ex03_update/README.md)에서도 같은 글을 고른다.

## REST Client

VS Code REST Client(`humao.rest-client`)에서는 앞 단계의 `.env`를 이 폴더에 복사한다. [requests.http](requests.http)의 **Send Request**를 누른다.

`GET /rest/v1/guestbook`은 `apikey` 헤더에 공개 키를 보낸다. `book_id=eq.…`는 내 태그의 글을 고르고 `order=id.desc`는 최신 글을 먼저 보여 준다. 응답은 `200 OK`와 글 배열이다. 글이 없으면 `[]`다.
