# 배열 심화 예제

삽입·삭제, 순회, filter, map, reduce를 다섯 폴더에서 비교한다. 각 폴더에 `index.html`, `app.js`, `README.md`가 있다. 화면에서 입력·버튼·결과를 확인하고 코드에서 사용한 메서드를 찾는다. 정규 11주차 과제에 포함하지 않는 보강수업 자료다.

## 실행 순서

저장소 루트에서 다음 명령을 실행하고 예제 주소를 연다.

```bash
node web_programming/tools/static-server/server.mjs web_programming 8111
```

각 예제에는 `index.html`과 `app.js`가 있다. 두 파일을 같은 폴더에 두고 HTML을 연다. [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css) 연결에는 인터넷이 필요하다.

| 순서 | 폴더와 설명 | 실행 주소 | 확인할 결과 |
|---|---|---|---|
| 1 | [01_insert_delete](01_insert_delete/README.md) | [삽입·삭제](http://localhost:8111/specials/array_advanced/examples/01_insert_delete/) | 앞·뒤·지정 위치의 배열 변화와 메서드 반환값 |
| 2 | [02_iteration](02_iteration/README.md) | [순회](http://localhost:8111/specials/array_advanced/examples/02_iteration/) | `for...of`와 `forEach`의 같은 출력, `forEach` 반환값 |
| 3 | [03_filter](03_filter/README.md) | [필터](http://localhost:8111/specials/array_advanced/examples/03_filter/) | 70점 이상인 하늘·노을, 원본 3명 유지 |
| 4 | [04_map](04_map/README.md) | [변환](http://localhost:8111/specials/array_advanced/examples/04_map/) | 가산점 5점 적용 결과 85·65·95점, 원본 유지 |
| 5 | [05_reduce](05_reduce/README.md) | [누적](http://localhost:8111/specials/array_advanced/examples/05_reduce/) | 합계 230과 누적 과정, 빈 배열의 결과 0 |

브라우저에서 조작한 배열은 메모리에만 있다. 새로고침하면 처음 상태로 돌아간다. 이 특강에서는 저장 기능이나 외부 API를 사용하지 않는다.

## 메서드별 원본과 반환값

| 동작 | 호출 | 원본 배열 변경 | 반환값 |
|---|---|---|---|
| 뒤·앞 삽입 | `push(value)`, `unshift(value)` | 변경 | 변경 후 길이 |
| 뒤·앞 삭제 | `pop()`, `shift()` | 변경 | 삭제한 값, 비어 있으면 `undefined` |
| 지정 위치 삽입 | `splice(index, 0, value)` | 변경 | 삭제한 값이 없으므로 `[]` |
| 지정 위치 삭제 | `splice(index, 1)` | 변경 | 삭제한 값을 담은 배열 |
| 순회 | `forEach(callback)` | 메서드 자체는 변경하지 않음 | `undefined` |
| 조건 선택 | `filter(callback)` | 메서드 자체는 변경하지 않음 | 조건을 통과한 요소의 새 배열 |
| 값 변환 | `map(callback)` | 메서드 자체는 변경하지 않음 | 각 반환값을 모은 새 배열 |
| 값 누적 | `reduce(callback, initialValue)` | 메서드 자체는 변경하지 않음 | 마지막 누적값 |

콜백 안에서 객체의 속성을 직접 고치면 원본도 바뀔 수 있다. `filter`는 새 배열을 만들지만 그 안의 객체 참조는 원본과 같다. 이 예제의 `map`은 새 객체를 반환해 원본 점수를 보존한다. [MDN filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter), [MDN map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)

## 콜백 함수 읽기

콜백은 메서드에 전달하는 함수다. 예를 들어 `filter`는 배열의 각 요소를 인수로 넣어 다음 함수를 실행한다.

```js
const selected = students.filter(function (student) {
  return student.score >= 70;
});
```

`student`에는 이번에 검사할 객체 하나가 들어온다. 반환한 조건이 참인 요소를 결과 배열에 남긴다. `map`의 콜백은 새 배열에 넣을 값을 반환하고, `reduce`의 콜백은 다음 호출에 넘길 누적값을 반환한다.

```js
const total = students.reduce(function (sum, student) {
  return sum + student.score;
}, 0);
```

여기서 `sum`의 첫 값은 마지막 인수 `0`이다. 다음 호출부터는 직전 콜백의 반환값이 들어온다. 빈 배열이면 콜백을 실행하지 않고 초깃값 `0`을 반환한다. 초깃값 없이 빈 배열에 `reduce`를 호출하면 예외가 발생한다. [MDN reduce](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)

`forEach`는 각 요소로 작업을 실행할 때 사용한다. 콜백에서 값을 반환해도 그것을 모아 새 배열로 만들어 주지는 않는다. 새 배열이 필요하면 `map`을 사용한다. [MDN forEach](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)

## 실습 확인

- 삽입 위치 0과 마지막 위치를 비교하고, 빈 배열에서 삭제한 결과를 확인한다.
- 순회 버튼을 여러 번 눌러도 화면의 항목이 중복되지 않는지 확인한다.
- 필터 기준을 바꿔 전체 선택·일부 선택·0명 선택을 확인한다.
- `map`을 두 번 실행해도 가산점이 중복 적용되지 않고 원본 점수가 남는지 확인한다.
- `reduce`의 누적값 0 → 80 → 140 → 230을 따라가고 빈 배열과 비교한다.

지정 위치 삽입·삭제의 인수 순서는 [MDN splice](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/splice)에서 확인할 수 있다.
