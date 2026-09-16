# 15주차 예제 — 기말 실기 공개 starter와 리허설 완성본

이 폴더에는 **시험과 같은 구조의 연습 파일**만 있다. 실제 시험 문항과 값은 없다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 완성본과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `web-final` 폴더의 파일 |
|---|---|---|
| [rehearsal_starter/index.html](rehearsal_starter/index.html) | [2단계](../walkthrough.md#2-starter-네-파일-넣기) — 그대로 넣고 고치지 않는다 | `index.html` |
| [rehearsal_starter/styles.css](rehearsal_starter/styles.css) | [2단계](../walkthrough.md#2-starter-네-파일-넣기) | `styles.css` |
| [rehearsal_starter/app.js](rehearsal_starter/app.js) | [2단계](../walkthrough.md#2-starter-네-파일-넣기) — TODO 네 자리가 들어 있다 | `app.js` |
| [rehearsal_starter/data/items.json](rehearsal_starter/data/items.json) | [2단계](../walkthrough.md#2-starter-네-파일-넣기) — `data` 폴더를 만들어 넣는다 | `data/items.json` |
| [rehearsal_solution/app.js](rehearsal_solution/app.js) | [7단계](../walkthrough.md#7-todo-4--추천-목록-불러오기) — TODO 네 개를 다 채운 모습 | `app.js` (리허설을 끝낸 뒤) |
| [rehearsal_solution/index.html](rehearsal_solution/index.html) · [styles.css](rehearsal_solution/styles.css) · [data/items.json](rehearsal_solution/data/items.json) | starter와 **같은 파일**이다. 리허설에서 고치지 않는다 | 그대로 |

`app.js` 한 파일만 starter와 완성본이 다르다. 나머지 세 파일은 글자 단위로 같다.

## 1. 공개 starter — 지금 되는 것과 안 되는 것

`rehearsal_starter`를 공개 주소에 올리고 열면 이렇게 보인다.

```text
읽은 책 기록            [다크 모드]     ← header, 버튼은 지금도 동작한다
한 권 남기기
제목 [          ] [추가]               ← 눌러도 아무 일이 없다 (TODO 1)
                                        ← 목록 자리는 비어 있다 (TODO 2)
추천 목록
불러오는 중…                            ← 문구가 그대로 멈춰 있다 (TODO 4)
```

- **되는 것**: `[다크 모드]` 버튼(`classList.toggle`), 화면 꾸미기, 375px에서 폼이 세로로 접히는 `@media`.
- **안 되는 것**: 추가(TODO 1), 지우기(TODO 2), 저장·복원(TODO 3), 추천 목록(TODO 4).
- Console 오류는 **0개**다. 기능이 없을 뿐 깨져 있지 않다. 시험도 이 상태에서 시작한다.

## 2. TODO 네 자리

| TODO | 자리 | 하는 일 | 처음 배운 주 |
|---|---|---|---|
| 1 | `form.addEventListener('submit', …)` 안 | 빈값 안내 → `books.push` → `showList()` | 7주 · 10주 |
| 2 | `showList()`의 `for` 안 | 항목마다 [지우기] 버튼(`splice(i, 1)`) | 10주 |
| 3 | `let books` 윗줄과 `saveList()` 안 | `final-items` 키로 저장·복원 | 11주 |
| 4 | `loadRecommend()` 안 | `data/items.json` 불러오기와 오류 안내 | 12주 |

## 3. 개념별 최소 코드

목록 한 줄 만들기(10주):

```html
<ul id="book-list"></ul>
```

저장과 복원은 두 줄이 짝이다(11주). 키 이름 `final-items`는 문항이 정한 것이며 `my-web`의 `guestbook`과 다르다.

불러오기는 **상대 경로**로 쓴다(12주). `/data/items.json`처럼 `/`로 시작하면 공개 주소에서 404가 난다.

```json
[
  {
    "title": "처음 만나는 웹",
    "comment": "HTML과 CSS를 그림으로 설명한다."
  }
]
```

## 4. 완성본을 보는 방법

`rehearsal_solution/app.js`는 **1일차 리허설에서만** 연다. 막힌 TODO의 그 부분만 보고, 전체를 복사해 붙여 넣지 않는다.
2일차 본시험에서는 이 폴더를 열어 두어도 되지만 문항의 값과 화면 주제가 달라 그대로 쓸 수 없다.

`app.js`만 72줄로 다른 주차 예제보다 길다. 한 페이지에 폼·목록·저장·불러오기 네 기능이 모여 있기 때문이다.
시험에서는 이 파일을 처음부터 타이핑하지 않고 starter의 TODO 자리만 채운다.

## 공식 참고 자료

- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [Fetch API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
