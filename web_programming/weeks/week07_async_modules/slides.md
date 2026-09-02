---
marp: true
theme: default
paginate: true
header: 웹프로그래밍
footer: 7주차 · ES Module과 비동기 처리
---

# ES Module과 비동기 처리

## 1일차: 파일을 책임으로 나누기

질문: **코드를 여러 파일로 나누면 무엇이 더 분명해져야 하는가?**

---

## 30분 학습 지도

```text
main.js
 ├─ api.js   : 외부 데이터
 ├─ view.js  : DOM 표현
 └─ stats.js : 순수 계산
```

- 파일 수보다 책임과 의존 방향이 중요하다.
- 브라우저는 import를 따라 module graph를 만든다.

---

## ES Module의 입구

```html
<script type="module" src="./js/main.js"></script>
```

```js
import { fetchCards } from "./api.js";
```

- module은 기본적으로 strict mode
- 자체 scope를 가진다.
- 상대 경로의 확장자를 명시한다.
- 한 번 평가된 module은 재사용된다.

---

## named export

```js
export function normalizeCard(card) {
  return {
    id: String(card.id),
    title: String(card.title).trim()
  };
}
```

```js
import { normalizeCard } from "./data.js";
```

이름이 import 지점에 드러나 리팩터링과 검색이 쉽다.

---

## 의존 방향을 작게 유지

나쁜 신호:

- `api.js`가 DOM selector를 안다.
- `view.js`가 URL과 fetch를 안다.
- 두 module이 서로 import한다.
- 모든 것을 담은 `utils.js`가 생긴다.

좋은 질문: “이 함수는 입력과 출력을 한 문장으로 말할 수 있는가?”

---

## 순수 계산을 분리

```js
export function countByCategory(cards) {
  return cards.reduce((counts, card) => {
    counts[card.category] = (counts[card.category] ?? 0) + 1;
    return counts;
  }, {});
}
```

DOM과 fetch 없이 Console에서도 검증할 수 있다.

입력 배열을 바꾸는지, 새 값을 반환하는지도 확인한다.

---

## module 경로 오류 읽기

```js
import { renderCards } from "./views.js";
```

실제 파일이 `view.js`라면:

1. Console 오류의 요청 URL 확인
2. Network의 404 확인
3. 파일명·상대 위치·대소문자 비교

GitHub Pages는 로컬 Windows보다 대소문자에 엄격할 수 있다.

---

## 왜 로컬 서버인가?

`file://`은 module과 `fetch`의 origin/CORS 동작을 웹 배포와 다르게 만든다.

```bash
python -m http.server 8000
```

브라우저가 실제 HTTP 요청을 보내는 조건에서 연습한다.

---

## 1일차 결론

```text
main: 흐름 조정
api: 요청하고 데이터 반환
view: 상태를 DOM으로 표현
stats: 데이터만 계산
```

**실습:** module graph를 먼저 그리고, import 한 줄마다 Network에서 확인한다.

---

# 2일차: 기다림과 실패를 UI로 표현하기

비동기는 “나중에 끝나는 작업”과 “그동안의 화면”을 함께 설계하는 일이다.

---

## Promise의 세 상태

```text
pending ──성공──▶ fulfilled
        └─실패──▶ rejected
```

settled 뒤에는 다른 상태로 바뀌지 않는다.

```js
const promise = fetch("./data/cards.json");
console.log("A");
promise.then(() => console.log("C"));
console.log("B");
```

예상 순서: A → B → C

---

## async/await는 순서를 읽기 쉽게 한다

```js
async function load() {
  const response = await fetch("./data/cards.json");
  const cards = await response.json();
  return cards;
}
```

`await`는 브라우저 전체를 멈추지 않는다. 현재 async 함수의 다음 줄을 나중에 이어 간다.

---

## fetch의 중요한 경계

```js
const response = await fetch(url);

if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}
```

- 404/500: Promise가 보통 fulfilled, `ok === false`
- 연결 끊김/CORS: Promise rejected
- JSON 오류: `response.json()`이 rejected

한 종류의 “실패”가 아니다.

---

## 응답 데이터도 검사한다

```js
const value = await response.json();

if (!Array.isArray(value)) {
  throw new TypeError("배열 응답이 아닙니다.");
}
```

HTTP 200은 앱에 올바른 데이터라는 뜻이 아니다.

신뢰 경계: network → parsing → shape validation → render

---

## UI 상태 모델

```js
{ kind: "loading" }
{ kind: "empty" }
{ kind: "success", data: cards }
{ kind: "error", message: "..." }
```

각 상태가 동시에 두 개 보이지 않게 한 곳에서 렌더링한다.

---

## try/catch/finally

```js
try {
  showLoading();
  const cards = await fetchCards(url);
  showCards(cards);
} catch (error) {
  showError(error);
} finally {
  loadButton.disabled = false;
}
```

`finally`에는 성공·실패와 무관한 정리만 둔다.

---

## 빠른 요청의 경쟁

```text
요청 A 시작 ──────────────▶ A 응답
   요청 B 시작 ───▶ B 응답
```

B가 최신 선택인데 늦게 온 A가 화면을 덮을 수 있다.

해결 후보:

- request id 비교
- 이전 `AbortController` 취소
- 요청 중 버튼 잠금

---

## 네 가지를 직접 재현하라

| 선택 | 기대 UI |
|---|---|
| `cards.json` | 카드 목록 |
| `empty.json` | empty 안내 |
| `wrong-shape.json` | 데이터 형식 오류 |
| 없는 경로 | HTTP 오류와 재시도 |

**실습 완료는 성공 화면 하나가 아니라 네 상태의 증거다.**
