# 14주차 예제 — REST 수정·삭제

각 비교 예제를 폴더째 복사한다. `config.example.js`는 세 공개 설정값만 담으며 HTML에서 직접 읽는다. 편집 키를 이 파일에 적지 않는다.

| 예제 | 보여 주는 것 | 바꿔 볼 것 |
|---|---|---|
| [day1/ex01](day1/ex01/index.html) | 배열 위치와 서버 ID | 배열 두 객체 순서 |
| [day1/ex02](day1/ex02/index.html) | DELETE와 204 | 자기 글 ID, 자기 키 한 글자 |
| [day2/ex03](day2/ex03/index.html) | PATCH와 JSON 본문 | 자기 글 메시지 |
| [day2/ex04](day2/ex04/index.html) | ID별 GET 재조회 | 삭제 전·후 같은 ID |

## 만들기 파일

[day2/web-week14](day2/web-week14/guestbook.html)은 13주 폼에 수정·삭제를 연결한 실행 참고본이다. 학습 순서는 비교 예제 → [실습지](../lab.md) → [따라하기](../walkthrough.md)다.

| 파일 | 역할 | 연결되는 예제 |
|---|---|---|
| `config.example.js` | API 주소·공개 키·방명록 ID | 모든 REST 예제 |
| `guestbook.js` | GET·목록 표시 | 12주, ex04 |
| `submit.js` | POST로 새 글 저장 | 13주 |
| `actions.js` | 서버 ID·편집키·수정폼·재조회 | ex01, ex04 |
| `delete.js` | DELETE·204·재조회 | ex02 |
| `edit.js` | PATCH·JSON·재조회 | ex03, ex04 |

이전 발표 수업의 부속 자료는 보존되어 있으나 이번 실습에 사용하지 않는다. 현재 사용할 파일은 위 표와 `guestbook.html`·`index.html`·`about.html`·`app.js`·`styles.css`·`images/profile.png`다.
