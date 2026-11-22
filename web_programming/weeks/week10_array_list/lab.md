# 10주차 실습 — 배열 목록과 삭제

강의·시연 60분 뒤 아래 필수 실습을 30분씩 수행한다. 파일 배부·저장소 준비는 수업 전, 업로드는 수업 뒤다. `student01` 같은 가상 이름을 사용한다.

## 1일차

| 시간 | 필수 활동 | 기대 결과 |
|---|---|---|
| 0~5분 | ex01 app.js의 push 문자열 두 값을 바꾸고 새로고침 | 개수 3, 첫 값과 셋째 값 표시 변경 |
| 5~20분 | ex02 app.start.js의 TODO 다섯 줄 작성, start.html 실행 | 배열 개수와 아래 목록 개수 일치 |
| 20~30분 | 배열을 0개·1개·3개로 바꾸어 실행 | 아래 목록도 0·1·3개 |

[ex01](examples/day1/ex01/README.md), [ex02 시작 틀](examples/day1/ex02/start.html)을 연다. ex02는 먼저 `items.push('student04');`를 주석 처리하고 배열 리터럴만 `[]`, `['하나']`, `['하나', '둘', '셋']`으로 바꾼다. 숫자 3으로 반복한 위 목록은 항상 세 줄이고 없는 값은 `undefined`다. 아래 목록이 배열 길이와 같아야 한다. 비교 뒤 원본 배열을 복원한다.

다섯 줄은 `for` 시작, `li` 생성, `textContent`, `list.append`, 닫는 중괄호다. 버튼 처리·비우기·개수 표시는 제공되어 있다. [따라하기](walkthrough.md#1일차)의 코드와 비교한다.

## 2일차

[10주 시작 화면](examples/day2/web-week10/guestbook.start.html)을 열고 같은 폴더의 `guestbook.start.js`를 수정한다. 9주의 최신순 타임라인에서 등록순 문자열 목록으로 넘어간다. 아래 표의 `append` 세 줄은 10주 시작 파일의 `submit` 안에 있다. `guestbook.html`에서 완성 결과를 비교한다.

| 시간 | 필수 활동 | 기대 결과 |
|---|---|---|
| 0~10분 | submit의 직접 append 세 줄을 push·showList 두 줄로 교체 | 글 등록 때 배열·목록·개수 일치 |
| 10~18분 | 삭제 버튼 TODO에 splice·showList 두 줄 작성 | 가운데 값 하나만 삭제 |
| 18~25분 | 세 글 등록, 가운데 삭제, 남은 둘도 삭제 | 3→2→0개, 마지막 빈 안내 |
| 25~30분 | 다시 세 글 등록·가운데 삭제 후 localhost 캡처 | 두 글·각 삭제 버튼·2개 |

완료한 `guestbook.start.js` 내용을 `guestbook.js`에 복사하고 `guestbook.html`에서도 같은 결과인지 확인한다. HTML·폼 검증·showList·삭제 버튼 생성·시작 시 호출은 제공 코드라 다시 작성하지 않는다.

## 확인 항목

- 첫 글과 셋째 글이 남고 가운데 글만 삭제된다.
- 빈 이름, 공백뿐인 메시지는 등록되지 않는다. 입력을 고치면 안내가 지워진다.
- 이메일이 비어 있으면 제출할 수 있고, `abc`처럼 형식이 틀리면 브라우저 기본 검사가 막는다. 이메일은 목록 문자열에 넣지 않는다.
- `<b>인사</b>`는 굵은 글자가 아니라 입력한 문자열로 보인다.
- 375px와 1280px에서 긴 글·버튼이 화면 밖으로 넘치지 않는다.
- 새로고침과 다른 페이지로 이동 후 돌아오기는 새 페이지를 만들므로 글이 사라진다. 뒤로 가기의 메모리 복원은 브라우저 캐시에 따라 다를 수 있다.

## 막혔을 때

| 증상 | 확인 |
|---|---|
| 배열만 늘고 화면은 그대로 | push 뒤 showList 호출 |
| 다시 그릴 때마다 중복 줄 | showList 첫 줄의 `list.innerHTML = ''` |
| 삭제 후 개수만 또는 목록만 그대로 | splice와 showList 두 줄 |
| 마지막에 undefined 또는 빈 줄 | `<`를 `<=`로 쓰지 않았는지 |
| TypeError: Assignment to constant variable | 반복 변수 i는 let |
| Identifier 'list' has already been declared | 제공 DOM 선택 줄을 중복 추가했는지 |
| 스타일이 없다 | W3.CSS CDN 연결 상태 |
| 시작 화면만 고쳤는데 완성 페이지는 그대로 | guestbook.start.js와 guestbook.js 구분 |

## 선택 연습

필수 캡처 뒤 ex03 요소 붙이기, ex04 push 또는 append 한 줄 생략, ex05 비우기 생략, ex06 showList 호출 생략, ex07 splice의 삭제 개수 1→2를 비교한다. 각 폴더 README에 순서와 결과가 있다. 확인 뒤 원래 코드로 돌린다.

배열의 map·filter·reduce는 [배열 심화 특강](../../specials/array_advanced/README.md)에서 다루며 이번 정규 실습과 시험의 필수 범위가 아니다.

## 제출

주소창·두 글·삭제 버튼·`2개`가 보이는 캡처 한 장을 제출한다. localhost 결과를 인정한다. 수업 뒤 GitHub에 올리고 Pages 배포가 완료되면 다시 확인한다. 공개 자료에 실제 개인정보를 적지 않는다.
