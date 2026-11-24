# 4. Delete · 글 삭제 (DELETE)

앞 단계에서 사용한 `config.json`을 이 폴더에 복사한다. 브라우저는 여기서 수업 주소(`API_BASE_URL`), 공개 키(`API_PUBLIC_KEY`), 방명록 태그(`BOOK_ID`)를 읽는다.

정적 서버에서 [실습 화면](index.html)을 연다. [수정 단계](../ex03_update/README.md)에서 고친 글을 목록에서 찾는다. 그 글 옆의 **삭제**를 누른 뒤 확인창에 표시된 글 번호를 확인한다. 삭제를 승인하면 해당 글만 목록에서 사라진다.

## REST Client

VS Code REST Client(`humao.rest-client`)에서는 앞 단계의 `.env`를 이 폴더에 복사한다. [requests.http](requests.http)에서 **Send Request**를 누른다.

1. DELETE 요청의 입력창에 앞에서 수정한 글 번호를 넣는다. URL에는 `book_id`와 `id`를 모두 지정한다. `apikey` 헤더에는 수업용 공개 키를 넣는다.
2. DELETE 응답은 `204 No Content`이고 본문은 비어 있다. 아래 GET에 같은 글 번호를 넣는다. `200`과 `[]`이면 이 글이 사라졌다. 글이 남아 있으면 요청에 넣은 태그와 글 번호를 확인한다.
