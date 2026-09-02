---
marp: true
theme: default
paginate: true
header: 웹프로그래밍
footer: 6주차 · DOM·event·브라우저 CRUD
---

# DOM·event·브라우저 CRUD

## 1일차: 상태를 화면으로 연결하기

오늘의 질문: **사용자가 입력한 한 줄은 어떤 경로로 화면에 나타나는가?**

---

## 오늘의 30분 지도

1. HTML 문서와 DOM 객체
2. 요소 찾기와 event 관찰
3. form 제출의 기본 동작
4. 상태 → `render()` → 화면

```text
사용자 행동 → event handler → state 변경 → render()
```

---

## HTML과 DOM은 같은가?

```html
<ul id="todo-list"></ul>
```

```js
const list = document.querySelector("#todo-list");
console.log(list instanceof HTMLElement);
```

- HTML: 브라우저가 읽는 원본 문자열
- DOM: 브라우저가 만든 객체 트리
- DevTools의 Elements: 현재 DOM을 관찰하는 창

---

## 요소를 찾았다고 가정하지 않는다

```js
const form = document.querySelector("#todo-form");

if (!form) {
  throw new Error("#todo-form을 찾을 수 없습니다.");
}
```

- selector 오타는 `null`을 만든다.
- script 실행 시점이 너무 빠를 수도 있다.
- `defer` 또는 문서 끝의 script가 순서를 보장한다.

**예상 질문:** 없는 요소에 `addEventListener`를 호출하면?

---

## event는 “발생한 일”의 기록

```js
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  console.log(formData.get("title"));
});
```

- `submit`: Enter와 버튼 클릭을 함께 처리
- `event.target`: event가 시작된 요소
- `event.currentTarget`: handler가 등록된 요소

---

## form의 기본 동작을 먼저 안다

`submit` 뒤 페이지가 새로고침되는 이유는 브라우저의 기본 전송 동작이다.

```js
event.preventDefault();
```

기본 동작을 막는 것은 목적이 아니라, JavaScript가 제출 과정을 책임지겠다는 선택이다.

접근성 원칙: 클릭 전용 `div` 대신 form과 button의 의미를 유지한다.

---

## 화면보다 상태가 먼저

```js
let todos = [
  { id: crypto.randomUUID(), title: "DOM 관찰", done: false }
];

function render() {
  // todos를 읽어 DOM을 만든다.
}
```

- 상태: 앱이 기억해야 하는 값
- DOM: 그 값을 지금 보여 주는 표현
- handler마다 DOM을 제각각 고치면 상태와 화면이 어긋난다.

---

## 한 방향 흐름

```text
입력
  ↓
검증
  ↓
todos 변경
  ↓
render(todos)
```

`render()`는 같은 상태를 받으면 같은 목록을 보여야 한다.

**1일차 실습:** Create → Read → Delete 순으로 한 기능씩 검증한다.

---

# 2일차: id·수정·영속화

배열의 몇 번째가 아니라 **어떤 항목인가**를 다룬다.

---

## index보다 id

```js
const nextTodos = todos.filter((todo) => todo.id !== targetId);
```

정렬하거나 삭제하면 index는 바뀐다. 고유 `id`는 항목의 정체성을 유지한다.

```html
<li data-id="고유-id">...</li>
```

DOM과 상태 사이에는 문자열 id를 명시적으로 전달한다.

---

## CRUD를 배열 연산으로 번역

| 동작 | 배열 표현 |
|---|---|
| Create | 새 객체를 추가 |
| Read | `render(todos)` |
| Update | `map`으로 대상만 새 객체 |
| Delete | `filter`로 대상 제외 |

```js
todos = todos.map((todo) =>
  todo.id === targetId ? { ...todo, done: !todo.done } : todo
);
```

---

## event delegation

```js
list.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const item = button.closest("[data-id]");
  if (!item) return;
});
```

- 목록 하나에 handler 하나
- 동적으로 추가된 버튼에도 동작
- `closest` 결과가 없을 수 있음을 처리

---

## 수정은 별도 상태다

```js
let editingId = null;
```

수정 시작, 저장, 취소는 서로 다른 상태 전이이다.

```text
보기 ──수정──▶ 편집
편집 ──저장──▶ 보기
편집 ──취소──▶ 보기
```

빈 수정값, 삭제된 항목의 저장 요청도 생각한다.

---

## localStorage 경계

```js
localStorage.setItem("todos:v1", JSON.stringify(todos));
```

- 값은 문자열만 저장된다.
- 브라우저·origin별 로컬 저장소다.
- 다른 기기와 공유되지 않는다.
- 사용자가 DevTools에서 언제든 값을 바꿀 수 있다.

저장값은 신뢰하지 말고 읽을 때 검사한다.

---

## 안전하게 복원하기

```js
function loadTodos() {
  try {
    const value = JSON.parse(localStorage.getItem("todos:v1") ?? "[]");
    return Array.isArray(value) ? value : [];
  } catch {
    return [];
  }
}
```

복구 정책도 제품 결정이다.

- 빈 배열로 시작
- 오류 메시지 표시
- 손상 값을 별도 보관

---

## UI 상태는 최소 네 가지

| 상태 | 사용자에게 보여 줄 것 |
|---|---|
| 정상 | 항목 목록 |
| empty | 첫 항목 작성 안내 |
| validation | 무엇을 고쳐야 하는지 |
| storage error | 복구 사실과 재시도 방법 |

`console.error`만으로는 사용자가 문제를 해결할 수 없다.

---

## 오늘의 검증 질문

1. 공백만 제출하면 배열 길이가 그대로인가?
2. 같은 제목 두 개를 각각 삭제할 수 있는가?
3. 수정 후 새로고침해도 유지되는가?
4. 저장값을 `{broken`으로 바꾸면 앱이 살아 있는가?
5. 키보드만으로 추가·수정·삭제 가능한가?

**2일차 실습:** Update + persistence + failure path를 증거로 남긴다.
