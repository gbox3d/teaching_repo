# 온라인 방명록 완성본

[방명록](guestbook.html)에서 글 하나를 저장하고, 목록에서 그 번호를 찾아 내용을 수정한 뒤 삭제한다. 기능별 예제도 같은 순서로 연다. [생성](../../day1/ex01_create/README.md) · [조회](../../day1/ex02_read/README.md) · [수정](../ex03_update/README.md) · [삭제](../ex04_delete/README.md)

## 브라우저 실습

[config.example.json](config.example.json)을 같은 폴더에 `config.json`으로 복사한다. `API_BASE_URL`에는 수업 API 주소, `API_PUBLIC_KEY`에는 배부받은 공개 키, `BOOK_ID`에는 내 방명록 태그를 넣는다. 정적 서버에서 [방명록](guestbook.html)을 연다.

| 순서 | 조작 | 확인할 결과 |
|---|---|---|
| 1. 생성 (Create) | 별칭과 내용을 입력하고 **저장**을 누른다 | 새 글 번호가 표시된다 |
| 2. 조회 (Read) | **목록 보기**를 누른다 | 내 태그의 목록에서 방금 저장한 번호와 내용을 찾을 수 있다 |
| 3. 수정 (Update) | 수정할 내용을 입력하고 그 글 옆의 **수정**을 누른다 | 같은 글 번호에 새 내용이 보인다 |
| 4. 삭제 (Delete) | 같은 글 옆의 **삭제**를 누른 뒤 번호를 확인한다 | 대상 글만 목록에서 사라진다 |

페이지를 새로고침한 뒤에도 **목록 보기**로 결과를 확인할 수 있다.

## VS Code REST Client

`humao.rest-client`를 설치하고 [.env.example](.env.example)을 같은 폴더에 `.env`로 복사한다. 수업 주소·공개 키·태그는 브라우저와 같은 값으로 채운다. [requests.http](requests.http)를 열고 소개·도움말 위의 **Send Request**로 접속을 확인한다. 이어 C → R → U → D 순서로 각 요청을 보낸다.

POST는 JSON 본문과 `Prefer: return=representation`을 보내고 `201` 응답에서 글 번호를 받는다. 목록 GET은 `200`과 글 배열을 반환한다. 이후 요청은 방금 생성한 글 번호를 재사용한다.

PATCH는 `200`과 수정한 행을 반환한다. 빈 배열이면 방명록 태그와 글 번호를 확인한다. 같은 번호를 GET해 내용이 바뀌었는지 확인한다. DELETE는 `204`와 빈 본문을 반환한다. 같은 번호를 GET해 `200 []`이면 삭제된 것이다. 모든 요청에 같은 `apikey` 헤더를 사용한다.
