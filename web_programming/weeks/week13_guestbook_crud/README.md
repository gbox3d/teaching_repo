[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week13_guestbook_crud)

# 13주차 · REST 방명록 CRUD

방명록에 ‘토요일 모임’이라는 글 하나를 만들고 글 번호(`id`)를 적어 둔다. 그 번호로 글을 찾아 ‘일요일 모임’으로 고친 뒤 지운다. 수업에서는 강의자가 준비한 Supabase API를 사용한다.

| 순서 | 예제 | HTTP | 확인할 결과 |
|---|---|---|---|
| 1. Create · 생성 | [글 저장](examples/day1/ex01_create/README.md) | POST | 새 글 번호가 생긴다 |
| 2. Read · 조회 | [목록 보기](examples/day1/ex02_read/README.md) | GET | 내 방명록에서 그 번호와 원래 문장을 찾는다 |
| 3. Update · 수정 | [메시지 수정](examples/day2/ex03_update/README.md) | PATCH | 글 번호는 그대로이고 문장이 바뀐다 |
| 4. Delete · 삭제 | [글 삭제](examples/day2/ex04_delete/README.md) | DELETE | 같은 번호로 조회하면 빈 배열 `[]`이 돌아온다 |

## 두 차시 수업

| 차시 | 강의·시연 60분 | 실습 30분 |
|---|---|---|
| 1차시 | 접속 준비, 폼에서 글 생성, 응답의 번호 읽기, 태그별 목록 조회 | 접속 확인 5분, 글 생성 10분, 목록에서 번호와 문장 대조 15분 |
| 2차시 | 태그와 글 번호로 한 건 수정, 수정 결과 재조회, 한 건 삭제와 결과 확인 | 메시지 수정 10분, 같은 번호로 수정 확인 5분, 삭제와 재조회 15분 |

브라우저는 HTML 옆의 `config.json`을, VS Code REST Client는 요청 파일 옆의 `.env`를 읽는다. 두 파일에 같은 수업 주소·공개 키·방명록 태그(`BOOK_ID`)를 설정한다. [설정과 실행](walkthrough.md#2-rest-client와-브라우저-설정)

방명록은 수업 기간에 공개한다. `book_id`로 각자 실습한 글을 구분한다. 같은 공용 API를 쓰는 학생은 다른 태그의 글도 수정·삭제할 수 있다.

[완성 방명록](examples/day2/web-week13/guestbook.html)에서는 네 동작을 한 화면에서 실행한다. 14주에는 요청에 넣은 태그와 글 번호를 바꿔 보고 어떤 행이 수정·삭제됐는지 재조회한다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 글 번호 (`id`) | Entry ID | 留言编号 |
| 방명록 태그 (`book_id`) | Guestbook tag | 留言簿标签 |
| 공개 키 (`apikey` 헤더) | Publishable key | 可公开密钥 |
| 조회 조건 (`eq.`) | Equality filter | 等值过滤条件 |
| 요청 본문 | Request body | 请求体 |

[강의 슬라이드](https://gbox3d.github.io/teaching_repo/webprg/decks/week13_guestbook_crud/index.html) · [영문 원고](slides_en.md) · [실습지](lab.md) · [예제 색인](examples/README.md)
