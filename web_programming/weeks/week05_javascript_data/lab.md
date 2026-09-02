# 5주차 실습 — 데이터 파이프라인을 함수로 증명하라

## 프로젝트 시나리오

캠퍼스 활동 카드 8개를 다음 주 DOM에 렌더링할 예정이다. 이번 주에는 UI 없이 데이터 계약과 변환 규칙을 구현한다. input/output과 원본 불변성을 Console과 test로 증명한다.

## 공통 규칙

- 외부 package를 설치하지 않는다.
- 변환 함수 안에서 DOM을 읽거나 수정하지 않는다.
- 변환 함수는 `console.log` 대신 값을 return한다.
- 샘플 객체는 동일한 field shape와 type을 유지한다.
- 실제 개인정보와 외부 API data를 사용하지 않는다.

## 1일차 실습 — 데이터 계약과 기본 조회

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 계약 설계 | 0–10분 | field·type·경계 표 |
| 데이터 8개 | 10–22분 | 일관된 object와 array 작성 |
| 함수 1–2 | 22–36분 | search, category filter |
| 함수 3–4 | 36–47분 | find by id, unique tags |
| 사례 검증 | 47–55분 | 정상·빈·없는 값 |
| 정리 | 55–60분 | export, commit, 회고 |

### 문제 1 · 데이터 계약

`activities.mjs`에서 최소 8개 object를 export한다. 다음 field를 기본으로 하고 프로젝트 주제에 맞게 이름을 바꿀 수 있다.

| field | type | 규칙 예시 |
|---|---|---|
| `id` | string | unique, URL-friendly |
| `title` | string | 1자 이상 |
| `description` | string | 검색 대상 |
| `category` | string | `study`, `hobby`, `volunteer` 중 하나 |
| `capacity` | number | 1 이상 정수 |
| `joined` | number | 0 이상, capacity 이하 |
| `startsAt` | string | 정렬 가능한 동일 ISO 형식 |
| `tags` | Array<string> | 중복 없는 소문자 token 권장 |

데이터 작성 뒤 다음 자체 검사를 생각해 본다.

- id가 모두 unique인가?
- category 철자가 일관적인가?
- joined가 capacity를 넘는 항목이 있는가?
- tags가 Array가 아닌 항목이 있는가?

### 문제 2 · 검색 함수

함수 계약:

```text
searchActivities(items, query) → Array
```

요구:

1. query의 앞뒤 공백을 제거한다.
2. 대소문자 차이를 무시한다.
3. title, description, tags 중 하나에 포함되면 남긴다.
4. 정규화한 query가 빈 문자열이면 입력과 같은 항목을 가진 **새 Array**를 반환한다.
5. 입력 object를 수정하지 않는다.

구현 전에 아래 예상표를 채운다.

| query | 예상 length | 예상 id |
|---|---:|---|
| `산책` |  |  |
| `  산책  ` |  |  |
| `WEB` |  |  |
| `` | 8 | 전체 |
| 존재하지 않는 말 | 0 | 없음 |

### 문제 3 · 범주와 id 조회

```text
filterByCategory(items, category) → Array
findActivityById(items, id) → Object | undefined
```

- category가 `all`이면 새 Array로 전체를 반환한다.
- 없는 category는 빈 Array다.
- find는 첫 일치 object 또는 undefined다.
- 함수가 global selected value를 직접 읽지 않는다.

### 문제 4 · unique tag

```text
uniqueTags(items) → Array<string>
```

모든 `tags`를 펼치고 Set으로 중복을 제거한 뒤 일관된 순서로 반환한다. 원본 tags 배열은 바꾸지 않는다.

### 단계별 힌트

<details>
<summary>힌트 1 — 검색어 대소문자와 공백</summary>

query와 검색 대상 문자열에 같은 정규화 함수를 적용한다. `trim()`과 `toLocaleLowerCase('ko-KR')`를 한 곳에서 처리하면 규칙이 어긋나지 않는다.
</details>

<details>
<summary>힌트 2 — tags 검색</summary>

`tags.some((tag) => normalizedTag.includes(normalizedQuery))`처럼 “하나라도” 조건을 표현할 수 있다.
</details>

<details>
<summary>힌트 3 — Set을 Array로 반환</summary>

Set은 unique를 만드는 중간 구조로 쓰고 `[...set]` 또는 `Array.from(set)`으로 다음 단계가 다루기 쉬운 Array를 반환한다.
</details>

### 검증

Node의 `node:assert/strict` 또는 `node:test`를 사용해 최소 다음을 확인한다.

- 공백 query와 빈 query
- 대소문자 query
- 없는 category와 `all`
- 존재/부재 id의 find 결과
- tag 중복 제거
- 반환 Array가 입력과 같은 reference가 아님

### 확장

1. `buildActivityIndex(items) → Map<id, activity>`를 만들고 없는 id lookup을 비교한다.
2. 데이터 계약을 검사해 모든 오류를 문자열 배열로 반환하는 `validateActivities`를 설계한다.
3. 한국어 검색에서 단순 lowercase/includes가 해결하지 못하는 초성·띄어쓰기·정규화 문제를 조사한다.

## 2일차 실습 — 복사 정렬, view model, 집계

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 결과 계약 | 0–8분 | 정렬/view model/summary 예상 |
| 정렬 | 8–20분 | asc/desc와 invalid direction |
| view model | 20–32분 | map과 available seat 문구 |
| 집계 | 32–43분 | reduce와 Map/total |
| 파이프라인 | 43–50분 | search→filter→sort→map |
| 자동 검증 | 50–58분 | 정상·경계·실패·불변성 tests |
| 회고 | 58–60분 | 함수 분리 근거 |

### 문제 1 · 원본을 보존하는 정렬

```text
sortByStartsAt(items, direction) → Array
direction: "asc" | "desc"
```

요구:

1. 입력 Array를 먼저 복사한다.
2. `startsAt` 오름차순/내림차순을 지원한다.
3. direction이 두 값이 아니면 `RangeError`를 던진다.
4. 같은 날짜 항목의 tie-break 기준을 title 또는 id로 명시한다.

불변성 검증:

```js
const before = activities.map(({ id }) => id);
const sorted = sortByStartsAt(activities, 'desc');
const after = activities.map(({ id }) => id);
```

`before`, `after`, `sorted`의 관계를 assertion으로 작성한다.

### 문제 2 · card view model

```text
toCardModels(items) → Array<CardModel>
```

각 결과는 최소 다음을 가진다.

```js
{
  id,
  title,
  categoryLabel,
  startsAt,
  availability
}
```

- `availability`: 남은 자리 0이면 `마감`, 아니면 `N자리 남음`
- category 내부 code를 보이는 한국어 label로 변환
- 입력 object를 수정하지 않음
- 결과 개수는 입력 개수와 같음

### 문제 3 · 요약 집계

```text
summarizeActivities(items) → {
  totalActivities,
  totalCapacity,
  totalJoined,
  openActivities,
  categoryCounts // Map
}
```

reduce를 사용할 때 빈 배열에서도 위 구조와 number/Map type이 유지되도록 initial value를 제공한다. 한 함수가 너무 복잡해지면 `countByCategory`를 분리한다.

### 문제 4 · 파이프라인

다음 입력 상태를 받아 card model 결과를 만드는 작은 함수 또는 demo를 작성한다.

```js
const state = {
  query: '웹',
  category: 'study',
  direction: 'asc',
};
```

순서:

```text
전체 → 검색 → category filter → 날짜 정렬 → card model
```

각 단계의 length를 별도 log로 관찰하되 변환 함수 내부에는 log를 넣지 않는다.

### 필수 테스트 표

| 함수 | 입력 | 기대 | 종류 |
|---|---|---|---|
| search | 공백 query | 전체의 새 Array | 경계 |
| filter | 없는 category | `[]` | 경계 |
| sort | `asc` | 첫 날짜가 가장 빠름 | 정상 |
| sort | `sideways` | `RangeError` | 실패 |
| sort | 원본 | id 순서 유지 | 불변성 |
| view model | 정원=참여 | `마감` | 경계 |
| summary | `[]` | 모두 0, Map size 0 | 경계 |
| pipeline | 검색+범주+정렬 | 예상 id 순서 | 정상 |

### 단계별 힌트

<details>
<summary>힌트 1 — sort 뒤 원본 test가 실패한다</summary>

`items.sort(...)`는 items 자체를 바꾼다. `[...items].sort(...)`처럼 array container를 복사한 뒤 정렬한다.
</details>

<details>
<summary>힌트 2 — 내림차순 comparator</summary>

오름차순 비교 결과에 방향 계수 `1` 또는 `-1`을 곱할 수 있다. invalid direction을 기본값으로 조용히 처리하지 않는다.
</details>

<details>
<summary>힌트 3 — reduce가 빈 배열에서 실패한다</summary>

누적 결과의 완전한 초기 object를 두 번째 인수로 준다. Map도 `new Map()`으로 초기화한다.
</details>

### 최종 검증

```powershell
node demo.mjs
node --test
```

- [ ] 모든 test가 통과한다.
- [ ] demo 결과의 id 순서를 예상표와 비교했다.
- [ ] 원본 id 순서는 demo 전후 같다.
- [ ] 변환 함수가 DOM/global state/Console에 의존하지 않는다.
- [ ] 최소 4개 named function이 각각 한 가지 변환 의도를 가진다.

### 확장 주제

1. 여러 조건 정렬(comparator composition)을 title tie-break와 함께 구현한다.
2. 평균 참여율을 계산할 때 capacity 0인 비정상 데이터의 정책을 설계한다.
3. `Object.freeze`의 shallow 특성과 개발 중 mutation 탐지 용도를 실험한다.
4. 많은 데이터에서 매번 filter하는 방식과 Map index의 시간·메모리 trade-off를 설명한다.

## 다음 주 handoff 작성

아래 내용을 `handoff.md`에 적는다.

- 카드 하나를 만드는 데 필요한 view model field
- 결과가 빈 배열일 때 보일 문구
- 검색 중 query와 category 상태
- 함수를 호출한 뒤 DOM이 담당할 일과 담당하지 않을 일
