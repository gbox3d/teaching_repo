[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

# 14주차 — REST API로 방명록 수정·삭제

13주에 서버에 저장한 글을 ID로 골라 수정하고 삭제한다. 14주는 구현 실습 주차다. 레포트와 발표는 이 주차에서 평가하지 않으며, 별도 과제는 강의자 공지를 따른다. 기존 링크를 유지하기 위해 폴더 이름은 그대로 둔다.

## 학습 목표

1. 배열의 위치와 서버가 부여한 `id`를 구분한다.
2. `DELETE`로 지정한 글 하나를 삭제하고 `204` 응답에는 JSON 본문이 없음을 확인한다.
3. 편집 키를 요청 헤더에 넣고, `BOOK_ID`는 글 구분값일 뿐 권한을 증명하지 않음을 설명한다.
4. 기존 글을 폼에 불러와 `PATCH`의 JSON 본문으로 메시지를 고친다.
5. 요청 후 `GET`으로 다시 읽어 실제 변경 결과를 확인한다.

## 이번 주 결과물

온라인 방명록에 글 세 개를 남긴 뒤 가운데 글을 삭제하고, 남은 글 하나의 메시지를 수정한다. 새로고침 후 두 글과 수정한 메시지가 보인다. Network에서 PATCH 또는 DELETE 뒤 GET 요청을 확인한다. 편집 키 입력 칸은 비운 뒤 캡처한다.

## 2일 수업 흐름

| 일차 | 설명 30분 | 실습 60분 | 결과 |
|---|---|---|---|
| 1일차 | ID, DELETE, 편집 키, 204, 재조회 | ex01·ex02, 내 연습 글 삭제, 서버 결과 확인 | 지정한 ID 한 개 삭제 |
| 2일차 | PATCH, JSON 본문, 폼에 기존 글 넣기, 재조회 | ex03·ex04, 수정·삭제 버튼을 13주 방명록에 연결 | 수정·삭제되는 온라인 방명록 |

## 준비

- [13주 완성본](../week13_release_security/examples/day2/web-week13/)에서 시작한다. 새 저장소는 `web-week14`다.
- 강의자가 제공한 API 주소·공개 키·`BOOK_ID`를 `config.example.js`에 넣는다. 편집 키는 코드에 넣지 않는다.
- 강의자가 배부한 자기 방명록의 편집 키를 실행 중 입력한다. 새로고침하면 다시 입력한다.
- 로컬 리허설: [공용 API 안내](../../tools/guestbook-api/README.md)에 따라 API를 8787번에서 실행하고, 학생 폴더는 [정적 서버](../../tools/static-server/README.md)로 8000번에서 연다.
- 인터넷 실습은 강의자가 준비한 HTTPS API를 쓴다. `127.0.0.1`은 현재 PC이므로 클라우드 주소처럼 사용할 수 없다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 식별자 | identifier | 标识符 |
| 일부 수정 | PATCH | 部分修改 |
| 삭제 | DELETE | 删除 |
| 요청 헤더 | request header | 请求头 |
| 편집 키 | edit key | 编辑密钥 |
| 본문 없음 | No Content | 无内容 |
| 다시 조회 | fetch again | 再次查询 |

## 이번 주 범위

- 기존 `GET`·`POST`는 유지한다. 새 요청은 `PATCH`와 `DELETE`다.
- 서버 ID는 목록 순서가 바뀌어도 같은 글을 가리킨다. 배열 인덱스를 ID로 보내지 않는다.
- 편집 키는 메모리 변수에만 둔다. 저장소·스크린샷·URL·localStorage에 넣지 않는다.
- 서버 정책 때문에 잘못된 키로 `PATCH`하면 `200 []`, `DELETE`하면 `204`라도 글이 바뀌지 않을 수 있다. HTTP 성공과 실제 변경을 나누어 확인한다.
- 회원가입·로그인 화면, DB 설정, 서버 권한 정책 작성은 학생 실습 범위 밖이다.

## 수업 자료

- [슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week14_project_presentation/index.html
- [따라하기](walkthrough.md) · [실습지](lab.md) · [예제 안내](examples/README.md)
- 강의 대본과 해답은 강의자 별도 관리다.

## 완료 기준

- [ ] 새 저장소 `web-week14`와 Pages 주소가 있다.
- [ ] 삭제 대상의 `id`만 사라지고 다른 글은 남는다.
- [ ] 수정한 메시지가 GET 응답과 다른 브라우저에서 확인된다.
- [ ] 자기 공간에서 틀린 편집 키를 넣었을 때 변경되지 않은 사실을 확인한다.
- [ ] 편집 키를 비운 화면과 Network 요청을 캡처 한 장으로 제출한다.
- [ ] 코드·주소·캡처에 편집 키와 개인정보가 없다.

## 다음 수업 연결

15주는 1~14주 문제은행과 기말 개인 실기다. REST 문제는 강의자가 마련한 시험용 방명록에서 실행한다. 수업용 방명록의 글을 시험 중 변경하지 않는다.

## 공식 참고 자료

- [MDN Fetch API](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [Supabase Data REST API](https://supabase.com/docs/guides/api)
