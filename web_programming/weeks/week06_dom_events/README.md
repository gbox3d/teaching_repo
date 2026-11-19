[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

# 6주차 DOM과 클릭 이벤트

5주차의 `greet`·`hello`·`#greeting`을 이어 쓴다. 이번 주에는 click 리스너가 화면을 바꾸고, 함수 밖 변수가 클릭 횟수를 기억하며, classList가 다크 모드를 전환한다. 1~6주에는 직접 작성한 CSS를 사용한다.

## 학습 목표

- 페이지 소스의 HTML과 Elements의 현재 DOM을 구분한다.
- querySelector로 찾은 요소의 textContent를 click 리스너 안에서 바꾼다.
- 함수 밖 count를 유지하고 새로고침하면 0으로 돌아오는 이유를 설명한다.
- classList의 add·remove·toggle을 비교하고 두 버튼에서 countUp을 호출한다.
- 다크 모드에서 배경뿐 아니라 제목·메뉴·카드·푸터의 글자도 확인한다.

## 두 차시 운영

각 차시는 강의·시연 60분과 학생 실습 30분이다. 파일 배부와 저장소 준비는 수업 전, GitHub 업로드는 수업 뒤에 한다. 첫 5분은 준비 상태 확인이다.

| 차시 | 강의·시연 60분 | 학생 실습 30분 | 완료 증거 |
|---|---|---|---|
| 1차시 | 준비 5, DOM·소스 비교 15, click 15, 함수 밖 변수 15, 오류 시연 5, 안내 5 | 버튼 ID 대조 5, ex03 시작 틀의 count·textContent 여섯 줄 작성 15, 3회 클릭·새로고침 10 | 클릭 3회와 초기화 0회 |
| 2차시 | 준비 5, classList 15, 다크 모드 15, 함수 재사용 15, 시험 범위 5, 안내 5 | 제공 CSS 색 두 곳 5, toggle·countUp 세 줄 연결 10, 두 버튼·375/1280px 확인 10, 캡처 5 | 다크 모드·인사말·클릭 횟수 |

ex01·ex02·ex04~ex06은 강의자 시연이며 학생의 추가 수정은 선택이다. ex03의 inside 비교·console 로그도 제공 시연이다. 최종 HTML, 요소 선택, greet·hello, countUp, 두 리스너 틀은 제공한다. 완성 app.js 전체를 다시 쓰는 활동은 필수가 아니다.

## 사전 준비

지난주 개인 파일을 `web-week06`에 복사하고 개인 본문·이미지를 유지한다. 강의자는 홈 버튼·횟수 카드와 다크 CSS를 조립한 [제공본](examples/day2/web-week06/)을 배부한다. [예제 안내](examples/README.md)의 변경표로 지난주 파일과 비교한다. 학생 개인 사본의 ex03과 web-week06에서 각각 `app.start.js`를 `app.js`로 복사해 실습을 시작한다. 배부된 완성 `app.js`는 비교 답안이다.

VS Code·Chrome·Git을 확인한다. localhost를 쓰면 [server.mjs](../../tools/static-server/server.mjs)를 미리 준비한다. Node가 없는 PC는 index.html을 파일로 열어도 이번 주 동작을 확인할 수 있다. 공개 파일에는 별칭 `student01`과 가상 이메일만 쓴다.

## 예제와 자료

| 예제 | 개념 | 운영 |
|---|---|---|
| [ex01](examples/day1/ex01/README.md) | HTML 소스와 DOM | 강의자 시연 |
| [ex02](examples/day1/ex02/README.md) | 열 때 실행과 click | 강의자 시연 |
| [ex03](examples/day1/ex03/README.md) | 함수 밖 count | 여섯 줄 필수, inside 비교 시연 |
| [ex04](examples/day2/ex04/README.md) | add·remove·toggle | 강의자 시연 |
| [ex05](examples/day2/ex05/README.md) | body.dark와 카드 | 강의자 시연 |
| [ex06](examples/day2/ex06/README.md) | 함수 재사용 | 강의자 시연 |
| [web-week06](examples/day2/web-week06/README.md) | 기존 홈에 두 버튼 연결 | 세 줄 연결과 색 두 곳 필수 |

[실습지](lab.md), [따라하기와 완성 코드](walkthrough.md), [예제 파일 안내](examples/README.md), [한국어 슬라이드](slides.md), [영어 슬라이드](slides_en.md)를 함께 사용한다. 기존 덱 주소는 https://gbox3d.github.io/teaching_repo/webprg/decks/week06_dom_events/index.html 이다.

## 제출과 완료 기준

수업 안에서는 localhost 또는 파일 주소가 보이는 캡처 한 장을 제출한다. 인사 문장이 바뀌고 다크 모드에서 클릭 횟수가 1 이상이어야 한다. 375px에서 메뉴는 세로, 1280px에서는 가로이며 가로 넘침이 없어야 한다. 새로고침하면 횟수와 다크 모드가 초기화된다. Console에 예상하지 않은 오류가 없어야 한다.

수업 뒤 10분 이내에 commit·push하고 `https://student01.github.io/web-week06/`에서 확인한다. Pages 반영이 늦으면 로컬 캡처와 Commits 기록으로 확인한다. 공개 주소 확인이 30분 실습을 지연시키지 않는다.

## 다음 수업 연결

7주차는 오늘의 `web-week06` 파일에서 시작해 방명록 화면을 W3.CSS로 바꾼다. CDN을 연결하고 입력창·버튼·카드·메뉴 클래스를 적용한다. 시작 파일은 [`examples/day2/web-week06/`](examples/day2/web-week06/)에 있다.
폼 동작은 7주차 제공 코드로 확인한다. `class`로 모양을 바꾸면서 JavaScript가 사용하는 `id`는 유지한다. 결과는 `web-week07/guestbook.html`에서 확인한다.
8주차는 중간 개인 실기다. 1~7주 실습 제출로 만든 문제 은행에서 값을 바꿔 출제한다. 문제 은행은 [8주차 예제](../week08_midterm/examples/README.md)에 있다.

## 공식 참고 자료

- [DOM 소개 (MDN)](https://developer.mozilla.org/ko/docs/Web/API/Document_Object_Model/Introduction)
- [Document.querySelector() — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/querySelector)
- [Node.textContent — MDN](https://developer.mozilla.org/ko/docs/Web/API/Node/textContent)
- [EventTarget.addEventListener() — MDN](https://developer.mozilla.org/ko/docs/Web/API/EventTarget/addEventListener)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Element.classList — MDN](https://developer.mozilla.org/ko/docs/Web/API/Element/classList)
- [Document.body — MDN](https://developer.mozilla.org/ko/docs/Web/API/Document/body)
- [함수와 코드 재사용 (MDN)](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Functions)
- [DOM 보기와 바꾸기(Elements 패널) — Chrome DevTools](https://developer.chrome.com/docs/devtools/dom?hl=ko)
