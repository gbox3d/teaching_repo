---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 배열 심화"
footer: "원본 · 반환값 · 콜백 · 객체 참조"
---

# 배열 심화

같은 배열을 삽입·삭제·순회·선택·변환·누적하며 비교한다.

- 원본 배열과 반환값을 따로 읽는다.
- 일반 function 콜백의 인수와 반환값을 확인한다.
- 빈 배열과 객체 참조를 살펴본다.
- 보강수업 자료이며 정규 11주차 과제에는 포함하지 않는다.

[실습지](lab.md) · [따라하기](walkthrough.md)

---

## 실행 준비와 공용 CSS

배열·객체·함수·DOM 이벤트를 알고 시작한다. 화살표 함수는 필요 없다.
저장소 루트에서 실행한다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

주소: http://localhost:8111/specials/array_advanced/examples/01_insert_delete/

[W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css) 로딩에는 인터넷 연결이 필요하다.
예제와 공용 추가 스타일 web_programming/shared/examples.css의 상대 위치를 유지한다.

---

## 다섯 예제와 같은 학생 배열

01은 과일 배열, 02~05는 아래 학생 배열을 사용한다.

```js
const students = [
  { name: '하늘', score: 80 },
  { name: '바다', score: 60 },
  { name: '노을', score: 90 }
];
```

01 삽입·삭제 → 02 순회 → 03 filter → 04 map → 05 reduce
각 실행 전에 결과를 예상하고 원본·반환값·화면을 비교한다.
배열은 메모리에만 있으며 새로고침하면 초기 상태로 돌아간다.

---

## 01: 원본 변화와 반환값

[삽입·삭제 코드](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/01_insert_delete/app.js)

| 메서드 | 원본 변화 | 반환값 |
|---|---|---|
| push(value) | 뒤에 추가 | 새 길이 |
| unshift(value) | 앞에 추가 | 새 길이 |
| pop() | 뒤에서 삭제 | 삭제한 값 |
| shift() | 앞에서 삭제 | 삭제한 값 |

각 실험 전에 초기화를 누른다. 시작 배열은 사과·바나나·포도다.
귤을 push하면 배열은 네 항목이 되고 반환값은 숫자 4다.

---

## 01: splice와 빈 배열

각 줄을 시험하기 전에 초기화한다.

```js
fruits.splice(1, 0, '귤'); // 위치 1에 삽입, 반환값 []
fruits.splice(1, 1);      // 위치 1에서 삭제, 반환값 ['바나나']
```

- splice의 반환값은 삭제한 항목의 배열이다.
- pop·shift로 배열을 비운 뒤 다시 실행하면 undefined다.
- 화면은 삽입 위치 0~길이, 삭제 위치 0~길이-1만 허용한다.
- JavaScript splice 자체의 모든 위치 규칙을 다루는 예제는 아니다.

---

## 02: for...of와 forEach

[순회 코드](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/02_iteration/app.js)

```js
for (const student of students) {
  console.log(student.name);
}
const result = students.forEach(function (student) {
  console.log(student.name);
}); // result는 undefined
```

실제 예제는 Console 대신 li를 만들어 같은 세 항목을 표시한다.
for...of는 반복문이다. forEach는 콜백을 호출하며 새 배열을 반환하지 않는다.

---

## 03: filter는 조건에 맞는 항목 선택

[filter 코드](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/03_filter/app.js)

```js
const selected = students.filter(function (student) {
  return student.score >= minimum;
});
```

- student는 현재 학생 객체다. true인 항목을 새 배열에 포함한다.
- 최소 70점: 하늘·노을, 2명
- 최소 60점: 전체, 3명 / 최소 100점: 빈 배열 [], 0명
- 원본에서 학생을 삭제하지 않는다.

---

## 04: map은 반환값으로 새 배열 구성

[map 코드](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/04_map/app.js)

```js
const adjusted = students.map(function (student) {
  return { name: student.name, score: student.score + bonus };
});
```

가산점 5를 적용하면 결과 점수는 85·65·95다.
두 번 실행해도 매번 원본 80·60·90에서 계산하므로 누적되지 않는다.
콜백은 새 객체를 반환한다. 원본 student.score에는 대입하지 않는다.

---

## 새 배열과 새 객체는 다르다

| 예제 | 새 배열 | 안쪽 객체 |
|---|---|---|
| filter | 생성 | 선택된 원본 객체와 공유 |
| 현재 map 코드 | 생성 | 콜백에서 새 객체 생성 |

filter 결과의 객체 필드를 직접 바꾸면 원본 객체도 바뀐다.
map에서도 원본 객체를 그대로 반환하거나 직접 수정하면 영향을 줄 수 있다.
이번 예제는 객체를 읽기만 하거나 새 객체를 만들어 원본을 보존한다.
새 배열을 받았다는 사실만으로 깊은 복사가 되었다고 판단하지 않는다.

---

## 05: reduce의 누적값

[reduce 코드](https://github.com/gbox3d/teaching_repo/blob/main/web_programming/specials/array_advanced/examples/05_reduce/app.js)

```js
const total = students.reduce(function (accumulator, current) {
  return accumulator + current.score;
}, 0);
```

| 호출 | accumulator | current.score | 반환값 |
|---|---|---|---|
| 1 | 0 | 80 | 80 |
| 2 | 80 | 60 | 140 |
| 3 | 140 | 90 | 230 |

---

## 05: 초깃값과 빈 배열

- 첫 accumulator는 마지막 인수로 전달한 초깃값 0이다.
- 직전 반환값이 다음 호출의 accumulator가 된다.
- 마지막 반환값 230이 reduce의 결과다.
- 빈 배열과 초깃값 0: 결과 0, 콜백 호출 0회

빈 배열을 선택하고 합계 계산을 누른다.
실제 콜백의 steps.push 기록으로 만든 표가 0행인지 확인한다.
초깃값 없이 빈 배열에 reduce를 호출하면 오류가 된다.

---

## 원본과 반환값 비교

| 연산 | 이번 예제의 원본 | 반환값 |
|---|---|---|
| push·unshift·pop·shift·splice | 변경 | 길이·삭제 값·삭제 배열 |
| forEach | 유지 | undefined |
| filter | 유지 | 선택된 새 배열 |
| map | 유지 | 새 객체를 담은 배열 |
| reduce | 유지 | 합계 숫자 |

콜백에서 원본 객체에 직접 대입하면 이 표의 원본 유지 조건이 달라진다.

---

## 입력을 바꾸어 비교하는 실습

1. 삽입·삭제: 실행마다 초기화하고 배열과 반환값을 기록한다.
2. 순회: 두 방식의 목록과 반환값을 비교한다.
3. filter: 최소 점수 70·60·100, 경계 80을 시험한다.
4. map: 가산점 5를 반복 실행한 뒤 10·0·-5를 비교한다.
5. reduce: 일반 배열과 빈 배열의 합계·콜백 수를 비교한다.

운영 예: 설명·시연 60분 + 실습 30분
특강의 전체 시간·차시 수·분량을 고정하는 기준은 아니다.
[실습지](lab.md) · [예제 목록](examples/README.md)

---

## 확인할 설명과 실습 기록

- push의 반환값이 변경 후 배열이 아닌 이유
- splice 삽입의 반환값이 []인 이유
- forEach 결과와 map 결과의 차이
- filter의 객체 참조와 map의 새 객체 생성
- 빈 배열 reduce에서 초깃값이 하는 역할

예제·입력 → 예상 → 실제 결과 → 차이의 이유를 기록한다.
필요한 화면과 코드를 남긴다. 정규 11주차 제출물에는 포함하지 않는다.
