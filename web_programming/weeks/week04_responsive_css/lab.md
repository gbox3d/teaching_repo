# 4주차 실습 — CSS 값과 화면 변화

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week04_responsive_css

각 차시는 강의·시연 60분 뒤 학생 실습 30분이다. 비교 예제 13개와 선택 ex14를 모두 제공하지만 필수 수정은 아래 표의 항목뿐이다. 전체 예제의 비교 원리와 추가 실험은 [예제 안내](examples/README.md)에 있다.

## 사전 준비

수업 전에 `web-week04` 폴더·새 저장소와 제공 파일을 준비한다. 3주차 `.git`은 복사하지 않는다. 자신의 소개·취미는 유지하고 [제공 HTML·CSS](examples/day2/web-week04/)의 연결·카드 클래스를 미리 반영한다. 비교 폴더는 `ex/`에 배부된 상태로 시작한다. 수업 중 Raw 다운로드와 Git 신규 설명은 없다. `app.js`는 연결하지 않는다.

## 1일차 — 선택자와 박스 (30분)

| 실습 시간 | 필수 수정 | 확인 결과 |
|---|---|---|
| 0–10분 | ex01 CSS의 `.red` 색 `red` → `orange`, ex03 CSS의 `.pad` 값 `16px` → `32px` | ex01의 2·3번만 주황, ex03의 2·5번 안쪽 여백 증가 |
| 10–25분 | 사이트 `styles.css`의 `h1 color` → `#365314`, `.card padding` → `20px`, `body max-width` → `600px` | 제목 색·카드 안쪽 여백·넓은 화면의 본문 폭 변화 |
| 25–30분 | 저장·새로고침, 세 페이지 CSS 연결 확인 | 변경한 파일과 화면 확인 |

고치는 파일은 `ex/ex01/styles.css`, `ex/ex03/styles.css`, 사이트 맨 위의 `styles.css`다. 예제 폴더와 사이트에 같은 파일명이 있으므로 VS Code 경로를 확인한다. 색은 읽기 쉬운 다른 값으로 바꿔도 된다.

ex02·ex04·ex05·ex06은 강의자 시연이다. ex04의 고정 `width: 640px` 상자가 375px에서 넘치는 것은 비교 목적이다. 완성 사이트에는 이 고정 폭을 사용하지 않는다.

## 2일차 — flex와 조립 (30분)

| 실습 시간 | 필수 수정 | 확인 결과 |
|---|---|---|
| 0–10분 | ex07 CSS의 `.column` 방향 `column` → `row`, ex08 CSS의 `.center` 정렬 `center` → `flex-end` | ex07 4번 가로 배치, ex08 2번 오른쪽 정렬 |
| 10–22분 | 사이트 `nav gap` → `24px`, media 경계 `600px` → `700px`, media 안 `column` → `row`로 비교한 뒤 `column` 복원 | 기존 세 줄의 값만 변경, 375px에서 세로 메뉴 |
| 22–30분 | 1280px·375px에서 홈·내 정보·방명록 확인, 375px 홈 캡처 | 넓은 화면 가로·좁은 화면 세로 메뉴, 가로 넘침 없음 |

nav·media 수정은 기존 3줄(5줄 이내)이다. 완성본의 경계 600px과 실습값 700px은 모두 375/1280px에서 같은 최종 메뉴 방향을 보인다. ex09~ex13의 추가 값 변경과 전체 CSS 조립은 시연·선택 활동이다.

## 방명록 확인

이름·이메일·메시지 label을 클릭하면 입력에 포커스가 간다. 이메일에 `abc`를 넣고 남기기를 누르면 브라우저가 제출을 막는다. 이메일을 비우거나 `student01@example.com`으로 바꾸고 제출하면 현재 문서가 다시 열리고 입력은 초기화된다. 이름·메시지를 목록에 추가하거나 저장하는 JavaScript는 아직 연결하지 않는다.

## 제출 — 캡처 한 장

파일 또는 localhost에서 홈을 열고 Chrome 기기 모드(**Ctrl+Shift+M**, macOS **⌘+⇧+M**)의 폭을 `375`로 설정한다. 주소창과 폭 표시, 세로 메뉴, 테두리 있는 소개·취미 카드가 함께 보이는 화면 한 장을 제출한다. 1280px 화면과 비교 예제 파일은 확인용이다. 제출 위치·마감은 수업 공지를 따른다.

## 수업 뒤 업로드

2주차에 배운 저장·commit·push 순서로 준비된 `web-week04` 저장소에 올린다. Pages 주소 `https://student01.github.io/web-week04/`를 확인한다. 새 저장소 생성·Pages 설정은 사전 준비이며 수업 시간에는 새로 설명하지 않는다. 반영 지연·계정 문제는 로컬 캡처와 commit 기록을 남기고 다음 차시 첫 확인 시간에 처리한다.

## 막혔을 때

| 증상 | 확인 |
|---|---|
| CSS 변화 없음 | 저장·새로고침, 편집 중인 폴더, `link`의 `styles.css` 철자, 선택자 대소문자 확인 |
| 규칙 일부 무시 | DevTools Elements·Styles에서 취소선, 세미콜론·중괄호·속성값 확인 |
| 375px 메뉴가 가로 | `nav`의 `display: flex`, media 조건의 콜론, 안쪽 `flex-direction: column` 확인 |
| 사이트 가로 넘침 | `body`의 고정 width 사용 여부와 `max-width`, 입력의 `box-sizing` 확인 |
| 공개 주소·push 문제 | [2주차 문제 해결](../week02_github_pages/lab.md#막혔을-때), 사전 준비된 저장소 이름·Pages 설정 확인 |

## 먼저 끝났다면

[예제 안내](examples/README.md)의 다른 비교값을 바꾼다. ex08의 `space-evenly`, ex12의 `flex: 2`, 선택 부록 ex14의 `relative`·`absolute`는 추가 연습이다. `relative`는 원래 자리를 유지하고 `absolute`는 문서 흐름에서 빠진다. 선택 활동은 필수 캡처의 조건에 넣지 않는다.
