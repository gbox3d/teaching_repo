# 10주차 — 배열 데이터를 목록으로 그리기

7·9주 방명록은 작성자·시각·본문을 표시하고 `prepend`로 새 글을 맨 위에 놓았다. 10주 실습용 방명록은 `이름: 메시지` 문자열 하나를 한 줄로 표시한다. `push`로 추가한 순서대로 그리므로 첫 줄은 `items[0]`이다. 가운데 글을 삭제하며 배열 인덱스와 화면의 줄을 비교한다.

## 학습 목표

- `push`, `length`, 0부터 시작하는 인덱스로 문자열 배열을 다룬다.
- 고전 `for`로 배열 길이만큼 `li`를 만들어 붙인다.
- 배열이 바뀐 뒤 목록을 비우고 `showList()`로 다시 그린다.
- `splice(i, 1)`로 가운데 값을 삭제하고 개수·빈 상태를 갱신한다.

## 2일 수업 흐름

각 차시는 강의·시연 60분과 실습 30분이다. 일곱 예제를 모두 수정하는 과제가 아니다.

| 차시 | 강의·시연 60분 | 학생 실습 30분 | 결과 |
|---|---|---|---|
| 1일차 | 준비 5, 배열·push·length 20, 인덱스·for 20, li·textContent·append 10, 안내 5 | 배열 2값 변경 5, 제공 for 틀 5줄 완성 15, 0·1·3개 비교 10 | 배열과 목록 개수 일치 |
| 2일차 | 준비 5, showList 15, 비우고 그리기 15, 삭제 버튼 틀 15, 폼 인계 5, 안내 5 | submit의 세 줄을 push·showList 두 줄로 교체 10, 삭제 2줄 완성 8, 3→2→0개 확인 7, 캡처 5 | 문자열 배열 방명록 |

1일차 필수는 ex01의 두 값과 [ex02 시작 틀](examples/day1/ex02/start.html)이다. ex03·04는 강의자 시연이며 추가 변경은 선택이다. 2일차 ex05~07은 시연과 참고이고, 학생은 [방명록 시작 틀](examples/day2/web-week10/guestbook.start.html)의 네 줄을 작성한다. 폼 검증·showList·삭제 버튼 생성·CSS는 제공 코드다.

## 준비와 실행

수업 전에 [10주 제공 폴더](examples/day2/web-week10/) 전체를 새 `web-week10`으로 복사한다. 9주에 꾸민 홈과 내 정보를 이어 쓰려면 `index.html`, `about.html`, `app.js`, `styles.css`, `images/`를 옮긴다. 방명록은 10주 폴더의 `guestbook.start.html`에서 시작한다. 학생이 바꿀 네 줄은 같은 폴더의 `guestbook.start.js`에 있다.

Node.js 24, Chrome, VS Code를 사용한다. 저장소 루트에서 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

`http://localhost:8000/day1/ex01/`부터 연다. 각 폴더의 `index.html`을 직접 열어도 배열 동작은 같지만 HTTP 주소로 연습한다. W3.CSS cdnjs 4.1.0에는 인터넷 연결이 필요하다. [예제 안내](examples/README.md)에 폴더별 경로가 있다.

## 제공 코드와 학생 작성

| 구분 | 범위 |
|---|---|
| 필수 작성 | ex01 문자열 2값, ex02 for와 본문 5줄, 방명록 등록 2줄·삭제 2줄 |
| 제공 | HTML·W3.CSS·보조 CSS, DOM 선택, 버튼·이벤트 틀, 폼 검증, showList·빈 상태·개수, 시작 시 호출 |
| 시연·선택 | ex03~07의 코드 변형, Console에서 배열 관찰, 전체 지우기 |
| 별도 보강 | [배열 심화](../../specials/array_advanced/README.md)의 삽입·삭제·forEach·filter·map·reduce |

## 제출과 완료 기준

3개 등록 → 가운데 삭제 → 위아래 두 글과 `2개`가 보이는 화면 한 장을 제출한다. localhost 주소창이 보이면 인정한다. 캡처 뒤 나머지 글을 삭제하여 `0개`와 빈 안내도 확인한다. 새로고침하면 배열과 화면이 초기화된다. 공백 이름·메시지는 등록되지 않고, 잘못된 이메일은 브라우저 기본 검사가 막는다. 이메일은 목록에 저장하지 않는다.

수업 뒤 변경을 commit·push하고 Pages에서 다시 확인한다. 배포 완료 시점은 GitHub Actions/Pages 상태로 확인하며 정해진 대기 시간을 가정하지 않는다. 업로드 지연으로 수업 내 캡처를 미루지 않는다.

## 다음 수업 연결

11주에는 객체 필드를 읽고 문자열→JSON→폼 저장·불러오기를 실습한다. 전체 저장 방명록은 제공 시연본이다. 이번 문자열 배열 방명록을 학생이 모두 저장 기능으로 재작성하는 과제로 넘기지 않는다. 12~14주는 강의자가 준비한 공용 API를 호출하고, Supabase 서버 구축과 SPA 전환은 별도 특강이다.

[실습지](lab.md) · [따라하기](walkthrough.md) · [한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md)

## 공식 참고

[Array](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array), [for](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/for), [splice](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/splice), [append](https://developer.mozilla.org/ko/docs/Web/API/Element/append).
