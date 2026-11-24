# 3. Update · 글 수정 (PATCH)

[조회 단계](../../day1/ex02_read/README.md)에서 확인한 글 번호를 선택한다. 새 메시지를 입력하고 **수정**을 누른다. 선택 목록을 다시 열면 같은 번호에 바뀐 메시지가 표시된다. [실습 화면](index.html)

브라우저는 같은 폴더의 `config.json`에서 수업 주소(`API_BASE_URL`), 공개 키(`API_PUBLIC_KEY`), 방명록 태그(`BOOK_ID`)를 읽는다. 앞 단계에서 사용한 파일을 복사한다.

## REST Client

VS Code REST Client(`humao.rest-client`)에서는 앞 단계의 `.env`를 이 폴더에 복사한다. [requests.http](requests.http)에서 **Send Request**를 누르고 앞에서 기록한 글 번호를 입력한다.

1. PATCH는 `book_id`와 `id`로 한 글을 지정하고 JSON 본문에는 새 `message`를 보낸다. 헤더에는 공개 키(`apikey`), `Content-Type: application/json`, `Prefer: return=representation`을 넣는다.
2. 응답이 `200`이면 수정된 행 한 개가 배열로 돌아오는지 본다. `[]`이면 수정된 행이 없다. 요청 주소의 태그와 글 번호를 확인한다.
3. 아래 GET에 같은 글 번호를 넣어 메시지가 바뀌었는지 확인한다. 다음 단계에서 [이 글을 삭제한다](../ex04_delete/README.md).
