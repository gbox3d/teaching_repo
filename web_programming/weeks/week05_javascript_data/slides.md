---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 5주차"
footer: "JavaScript 데이터와 함수"
---

# 5주차
## JavaScript 데이터와 함수

DOM 전에 데이터 변환을 독립적으로 설계하고 검증한다.

---

## 이번 주 파이프라인

```text
activities
  → search(query)
  → filter(category)
  → sort(direction)
  → map(card view model)
  → summarize
```

각 화살표를 작은 함수로 만들면 입력과 출력을 직접 시험할 수 있다.

---

<!-- _class: lead -->

# 1일차 · 설명 30분
## 값, 참조, 함수, collection

---

## 0–4분 · const와 let

```js
const course = 'web';
let visibleCount = 0;

visibleCount += 1;
```

- 기본 binding은 `const`
- 다른 값을 다시 할당해야 할 때 `let`
- `const`는 object 내부까지 immutable하게 만들지 않음

---

## 4–9분 · primitive와 reference

```js
let a = 3;
let b = a;
b += 1;        // a는 3

const first = { joined: 4 };
const second = first;
second.joined += 1; // 같은 object를 관찰
```

변수에 object 자체가 복제된다고 가정하지 않는다.

---

## 9–14분 · object와 array

```js
const activity = {
  id: 'photo-walk',
  title: '사진 산책',
  category: 'hobby',
};

const activities = [activity];
```

- Object: 한 record의 이름 있는 field
- Array: 순서 있는 여러 값
- 같은 의미 field의 이름과 type을 일관되게 유지

---

## 14–19분 · 작은 함수의 계약

```js
function availableSeats({ capacity, joined }) {
  return Math.max(capacity - joined, 0);
}
```

- parameter: 필요한 입력
- return: 호출자가 사용할 출력
- 함수 이름: 변환 의도
- Console 출력만 하고 return하지 않는 함수와 구분

---

## 19–23분 · scope

```js
const category = 'all';

function filterByCategory(items, selectedCategory) {
  const isAll = selectedCategory === 'all';
  return isAll ? [...items] : items.filter(...);
}
```

함수는 숨은 global보다 parameter를 사용하면 사례별 검증이 쉽다.

---

## 23–27분 · collection 선택

| 구조 | 질문 |
|---|---|
| Array | 순서대로 순회·변환할 목록인가? |
| Object | 고정된 이름의 field를 가진 record인가? |
| Map | 임의 key로 자주 조회·집계하는가? |
| Set | 중복 없는 값 자체가 중요한가? |

자료구조를 많이 쓰는 것이 목표가 아니라 목적이 드러나는 것이 목표다.

---

## 27–30분 · 경계 입력을 먼저 정하기

검색 함수의 계약 예:

| 입력 | 기대 |
|---|---|
| `"산책"` | 제목/소개에 포함된 항목 |
| `"  산책  "` | 공백 정규화 후 같은 결과 |
| `""` | 전체 복사본 |
| `[]` | 빈 배열 |

구현 전에 이 표가 테스트가 된다.

---

<!-- _class: lead -->

# 2일차 · 설명 30분
## 배열을 변환하고 원본을 지키기

---

## 0–4분 · destructuring

```js
const { title, category } = activity;
const [first, second] = activities;
```

필요한 field와 순서의 의도를 짧게 표현한다. 존재하지 않는 field는 `undefined`다.

---

## 4–8분 · spread는 얕은 복사

```js
const copy = [...activities];
const updated = { ...activity, joined: activity.joined + 1 };
```

바깥 array/object는 새 값이지만 안쪽 nested object까지 깊게 복제되는 것은 아니다.

---

## 8–12분 · map: 같은 개수의 새 형태

```js
const cards = activities.map(({ id, title, category }) => ({
  id,
  title,
  meta: category,
}));
```

입력 object를 화면용 view model로 바꾼다.

---

## 12–16분 · filter와 find

```js
const studies = activities.filter((item) => item.category === 'study');
const target = activities.find((item) => item.id === 'photo-walk');
```

- filter: 0개 이상인 Array
- find: 첫 값 하나 또는 `undefined`

반환 형태가 다음 코드의 분기를 결정한다.

---

## 16–21분 · sort는 원본을 바꾼다

```js
const sorted = [...activities].sort((a, b) =>
  a.startsAt.localeCompare(b.startsAt)
);
```

- 원본 array의 `sort()`는 in-place mutation
- 먼저 복사해 입력 순서를 보존
- comparator는 음수/0/양수 의미를 가져야 함

---

## 21–26분 · reduce는 누적 결과가 필요할 때

```js
const totalSeats = activities.reduce(
  (sum, item) => sum + item.capacity,
  0,
);
```

빈 배열에서도 결과 type이 정해지도록 initial value를 준다.

단순 map/filter를 억지로 reduce 하나에 합치지 않는다.

---

## 26–28분 · Map과 Set으로 집계·중복 제거

```js
const counts = new Map();
const tags = new Set(activities.flatMap((item) => item.tags));
```

Map은 key별 count, Set은 unique tag라는 목적을 코드에 드러낸다.

---

## 28–30분 · 조합과 테스트

```js
const result = toCardModels(
  sortByStartsAt(
    filterByCategory(searchActivities(data, query), category),
    'asc',
  ),
);
```

확인:

- 각 함수 단독 사례
- 조합 결과
- 원본 배열 순서 유지
- 빈 결과와 잘못된 옵션

---

## 정리

```text
명확한 data contract
  + 작은 pure transformation
  + 원본 보존
  + 정상/경계/실패 test
= DOM과 분리된 신뢰 가능한 로직
```
