[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week14_project_presentation)

# 14주차 방명록 수정·삭제

13주 서버 방명록에 DELETE·PATCH를 연결한다. 각 차시는 강의·시연 60분과 학생 실습 30분이다. 레포트 검사와 발표 평가는 포함하지 않는다. 기존 폴더·덱 주소를 유지하며 별도 과제의 내용·배점·마감은 강의자 공지를 따른다.

## 학습 목표와 결과

배열 인덱스와 서버 ID를 구분하고 자기 방명록의 지정 ID만 변경한다. DELETE 204에 JSON 본문이 없음을 확인하고 PATCH 응답 배열과 같은 ID의 GET으로 실제 변경을 판단한다. 세 글을 만든 뒤 가운데 글을 삭제하고 남은 글을 수정한 결과를 캡처한다.

## 양일 운영

| 차시 | 강의·시연 60분 | 학생 실습 30분 | 필수 수정 |
|---|---|---|---|
| 1일차 | 준비 5, 인덱스와 ID 15, 편집 키 10, DELETE·204 15, 대상 재조회 10, 안내 5 | 자기 ID·.http 확인 5, 삭제 틀 12, 정답 키·틀린 키 재조회 13 | 대상 URL·method·헤더 3곳 |
| 2일차 | 준비 5, PATCH 15, 기존 글→폼 10, 응답 배열·재조회 15, 전체 동작 10, 안내 5 | PATCH 틀 12, 세 글 수정·가운데 삭제·실패 복구 13, 키 지우고 캡처 5 | 대상 URL·JSON 본문·같은 ID 재조회 3곳 |

ex01·ex04와 완성본 전체 조립은 강의자 시연이다. 학생은 제공된 guestbook.js에서 지정한 요청 부분을 수정한다. 설정·키 처리·DOM 연결·최초 초기화·중복 요청·늦은 응답 보호는 제공 코드이며 작성 과제가 아니다. 나머지 예제 재작성은 선택이다.

## 사전 준비와 수업 뒤 정리

수업 전 [13주 완성본](../week13_release_security/examples/day2/web-week13/)과 이번 주 제공 파일을 새 web-week14 폴더·저장소에 준비한다. 공개 업로드는 30분 실습 뒤 정리 단계에서 한다. 수업 첫 5분에는 서버와 파일 준비 상태를 확인한다.

브라우저의 API 설정 패널에 API 주소·공개 키·BOOK_ID를 입력한다. 기본값은 로컬 http://127.0.0.1:8787, classroom-local, student01이다. 공용 HTTPS 설정은 메모리에만 두며 새로고침 뒤 재입력한다. 편집 키는 별도 입력으로 적용하고 키 지우기로 메모리에서도 지운다. 실제 키를 소스·URL·localStorage·캡처에 넣지 않는다. 공개 키와 방명록 번호만으로 편집 권한이 생기지 않는다.

로컬 API는 [강의자 안내](../../tools/guestbook-api/README.md), 화면 서버는 [정적 서버 안내](../../tools/static-server/README.md)를 따른다. REST Client의 .env와 브라우저 설정은 서로 별개다. [예제 안내](examples/README.md)의 폴더별 README와 requests.http를 사용한다.

## 결과 확인

틀린 키의 PATCH 200 []나 DELETE 204도 변경이 없을 수 있다. 같은 ID를 GET으로 확인한다. 통신 오류 뒤에는 같은 쓰기를 반복하기 전에 조회한다. 설정 변경은 선택 ID·폼·편집 키를 지우며, 이전 설정의 늦은 응답은 현재 화면에 표시하지 않는다.

수업 내 확인과 캡처는 localhost에서 수행할 수 있다. 공용 HTTPS API가 준비된 경우 수업 뒤 Pages와 다른 브라우저에서 같은 데이터인지 확인한다. 로컬 리허설을 다른 기기·공용 서버 검증 완료로 표시하지 않는다.

## 자료와 다음 수업

- [한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md) · [따라하기](walkthrough.md) · [실습지](lab.md)
- [덱](https://gbox3d.github.io/teaching_repo/webprg/decks/week14_project_presentation/index.html)
- [별도 과제 안내](project_brief.md) · [기존 평가 안내](rubric.md) · [기존 발표 안내](demo_outline.md)

15주 기말 REST 기본 문제는 PATCH 또는 DELETE 한 요청이다. 나머지 요청 틀과 재조회는 제공한다. SPA 직접 전환은 별도 선택 특강이며 14주 정규 실습에 포함하지 않는다.
