[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week05_javascript_data)

# 5주차 JavaScript 데이터와 함수

4주차의 세 페이지와 CSS를 이어 쓰고 홈에 인사말을 표시한다. 각 차시는 강의·시연 60분과 학생 실습 30분이다. 비교 예제 10개는 보존하되, 학생 필수 수정은 1일차 값 4곳과 오류 1건, 2일차 조건·함수·출력 각 1곳이다.

## 학습 목표

- `defer`가 HTML을 모두 읽은 뒤 스크립트를 실행한다는 것을 확인한다.
- `let`·`const`, 숫자·문자열, 템플릿 문자열을 구별한다.
- `if` 조건과 함수의 `return`으로 오전·오후 인사말을 만든다.
- `querySelector`로 찾은 요소의 `textContent`를 바꾼다.

버튼과 화면 출력은 예제에 제공한다. Console은 실행 순서·값·오류를 확인하는 보조 도구다. 학생은 출력용 코드와 이벤트 연결을 아직 직접 작성하지 않는다. `var`·`==`·`parseInt`·다른 DOM 접근법은 강의자 비교 시연 또는 선택 연습이며 필수 구현·평가에서 제외한다.

## 차시별 운영

| 차시 | 강의·시연 60분 | 학생 실습 30분 | 결과 |
|---|---|---|---|
| 1일차 | 준비 5, defer·실행 순서 10, let/const 15, 숫자·문자열 15, 템플릿 10, 안내 5 | ex03·ex05 값 4곳 15, 제공 출력 버튼·오류 1건 수정 10, 확인 5 | 바꾼 이름·숫자가 보이는 화면 |
| 2일차 | 준비 5, 비교·if 15, 함수·return 20, querySelector·textContent 10, 서버 5, 안내 5 | 조건 1곳·인사 함수 1곳·출력 1곳 18, 9시/15시 비교 7, 캡처 5 | 함수가 만든 인사말 |

## 수업 전 준비

1. 강의자는 4주 완성 파일을 새 `web-week05` 작업 폴더에 제공한다. 2주에 배운 저장소·Pages 준비는 수업 전에 끝낸다. 5주에 Git 새 개념이나 명령을 설명하지 않는다.
2. 비교 예제 ex01~ex10을 `web-week05/ex/`에 폴더째 배부한다. 수업 시간에 Raw 파일을 하나씩 받지 않는다.
3. 2일차에는 홈의 script 연결과 `#greeting` 자리를 미리 넣고 [시작 app.js](examples/day2/start/app.js)를 맨 위에 배치한다. [시작 파일 안내](examples/day2/start/README.md)를 따른다.
4. Node.js 24 이상과 [server.mjs](../../tools/static-server/server.mjs)를 사전에 준비한다. `node -v`와 `node server.mjs`로 확인한다. 첫 5분은 준비 상태 확인과 누락 복구에 쓴다.

`about.html`·`guestbook.html`·`styles.css`·프로필 그림은 4주 파일을 그대로 유지한다. CSS는 자체 CSS이며 W3.CSS 도입은 7주다. 방명록은 HTML 입력 연습용이다. 잘못된 이메일은 브라우저가 거절하며 유효한 제출은 같은 페이지를 GET으로 다시 탐색한다. 입력에는 name 속성이 없고 저장 기능도 없어 메시지가 저장되지 않는다.

## 자료와 예제 범위

- [실습지](lab.md) · [따라하기](walkthrough.md)
- [한국어 슬라이드](slides.md) · [영어 슬라이드](slides_en.md)
- [전체 예제와 파일 인계표](examples/README.md)
- [1일차 필수 ex03](examples/day1/ex03/README.md) · [ex05](examples/day1/ex05/README.md)
- [2일차 시작 파일](examples/day2/start/README.md) · [완성 홈](examples/day2/web-week05/index.html) · [완성 app.js](examples/day2/web-week05/app.js)
- [정적 서버 사용 안내](../../tools/static-server/README.md)

## 완료와 제출

1일차는 ex03의 a·b, ex05의 name·hour를 바꾸고 제공 버튼으로 확인한다. ex03의 const 재대입 오류를 `let`으로 수정한 결과까지 확인한다. 2일차는 제공 app.js의 세 곳을 고친다. `hour`를 9와 15로 임시 설정해 각각 아침·오후 인사를 확인하고 `new Date().getHours()`로 되돌린다.

수업 안에서는 localhost에서 주소창·인사말 카드·Console 두 줄이 보이는 캡처 1장을 만든다. Console의 두 줄은 시각 숫자와 인사말이며 오류가 없어야 한다. 2일차를 마치지 못한 학생은 ex01 버튼을 누른 A·C·B 화면을 임시 증거로 제출하고 다음 수업 시작 확인 시간에 보완한다.

공개 업로드는 수업 뒤 10분 이내 정리로 수행한다. `https://student01.github.io/web-week05/`에서 다시 확인한다. 업로드·계정 문제는 다음 차시 첫 확인 시간에 처리한다. 예시 별칭만 사용하고 실명·학번·전화번호·실제 이메일을 공개 파일과 캡처에 넣지 않는다.

## 다음 주 인계

6주는 이 완성본을 새 폴더에 미리 준비한다. `#greeting`, `greet(name)`, `hello(hour)`를 유지하고 클릭 이벤트·횟수·다크 모드를 추가한다. 정적 방명록은 보존한다. `server.mjs`도 같은 파일을 이어 쓴다.
