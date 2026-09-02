# 3주차 예제 — CSS 없는 캠퍼스 활동

## 파일

| 파일 | 관찰 개념 |
|---|---|
| [index.html](index.html) | landmark, heading, section/article, 명확한 link |
| [detail.html](detail.html) | 사진 산책 상세: 정의 목록, table caption/header |
| [detail-algorithm.html](detail-algorithm.html) | 알고리즘 모임 상세와 정확한 link 목적지 |
| [detail-board-game.html](detail-board-game.html) | 보드게임 모임 상세와 정확한 link 목적지 |
| [write.html](write.html) | label, input type, fieldset, native constraints |
| [confirmation.html](confirmation.html) | form action 목적지와 query 관찰 |

## 실행

모두 정적 HTML이므로 `index.html`을 직접 열어도 link와 native validation을 관찰할 수 있다. GitHub Pages 또는 로컬 HTTP로 열면 URL과 query를 더 일관되게 확인할 수 있다.

## 관찰 순서

1. CSS 없이 heading만으로 문서 목차를 말한다.
2. Tab과 Shift+Tab으로 이동 순서를 기록한다.
3. 각 활동의 “자세히 보기” link가 이름과 일치하는 상세로 가는지 확인한다.
4. 일정 표의 caption, column header, row header를 코드에서 찾는다.
5. 작성 form을 빈 채 제출하고 첫 invalid control을 확인한다.
6. 경계·정상 값을 넣어 confirmation URL의 query를 관찰한다.

## 주의

예제의 이름과 이메일은 가상 데이터다. form이 GET을 사용하는 것은 제출 key/value를 주소에서 관찰하려는 학습 목적이며 실제 개인정보 수집 양식의 권장 설계가 아니다.
