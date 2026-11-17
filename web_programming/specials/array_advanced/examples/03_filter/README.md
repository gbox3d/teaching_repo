# 배열 03: filter로 조건에 맞는 항목 선택

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/specials/array_advanced/examples/03_filter/)

이 예제는 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용하므로 인터넷 연결이 필요하다.
[공용 추가 스타일](../../../../shared/README.md)인 `web_programming/shared/examples.css`를 함께 준비하고 예제와의 상대 위치를 유지한다.

이 예제는 배열만 다루며 저장소를 읽거나 쓰지 않는다.

## 조작과 예상 결과

| 조작 | 결과 |
|---|---|
| 최소 점수 70 → filter 실행 | 하늘 80, 노을 90의 새 배열, 2명 |
| 최소 점수 60 → 실행 | 세 학생 모두 포함, 3명 |
| 최소 점수 100 → 실행 | 빈 배열 `[]`, 0명 |
| 입력 칸 비우기 → 실행 | 숫자 입력 안내, 새 계산 없음 |

각 실행 후 원본 배열에는 하늘 80, 바다 60, 노을 90이 그대로 남는다.

## 콜백과 반환값

```js
const selected = students.filter(function (student) {
    return student.score >= minimum;
});
```

`filter`는 배열의 학생을 하나씩 콜백에 전달한다. 이 예제의 `student`는 현재 학생 객체이며 비교 결과가 `true`이면 결과 배열에 포함한다. 콜백은 필요할 때 현재 인덱스와 원본 배열을 두 번째·세 번째 인수로 받을 수도 있다. 조건을 만족하는 항목이 없으면 새 빈 배열을 반환한다. [MDN: filter()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)

## 원본 보존과 얕은 복사

`filter`가 만드는 것은 새 배열이며 학생 객체 자체의 복사본은 아니다. 선택된 객체는 원본과 같은 객체를 가리킨다. 이 예제는 점수를 읽기만 하므로 원본이 유지된다. 결과 객체의 `score`를 직접 바꾸면 원본에서도 바뀐다. 점수를 바꾼 별도 결과가 필요하면 다음 map 예제처럼 새 객체를 만들어 반환한다. [MDN: filter()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)
