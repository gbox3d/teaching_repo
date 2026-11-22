# 배열 05: reduce로 점수 합계 구하기

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/specials/array_advanced/examples/05_reduce/)

이 예제는 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용하므로 인터넷 연결이 필요하다.

저장소나 서버 없이 메모리의 학생 배열로 계산한다.

## 조작과 예상 결과

빈 배열 선택을 해제하고 합계 계산을 누르면 합계는 230, 콜백 호출은 3회다.

| 단계 | accumulator | current.score | next |
|---|---|---|---|
| 1 | 0 | 80 | 80 |
| 2 | 80 | 60 | 140 |
| 3 | 140 | 90 | 230 |

빈 배열을 선택하고 다시 계산하면 합계는 0, 콜백 호출은 0회이며 표의 행도 없다. 선택을 해제하고 다시 계산하면 230으로 돌아온다. 원본 배열은 어느 경우에도 세 학생을 유지한다.

## 콜백 인수와 초깃값

```js
const total = input.reduce(function (accumulator, current, index) {
    const next = accumulator + current.score;
    steps.push({ step: index + 1, accumulator: accumulator, current: current.score, next: next });
    return next;
}, 0);
```

- `accumulator`: 첫 호출에서는 초깃값 0, 이후에는 직전 콜백의 반환값이다.
- `current`: 현재 학생 객체다. 점수는 `current.score`로 읽는다.
- `index`: 현재 학생의 배열 인덱스다. 표에서는 1을 더해 단계 번호로 표시한다.
- `next`: 콜백 안에서 계산한 지역 변수이며 반환하면 다음 누적값이 된다.

표는 미리 만든 정답이 아니다. 실제 콜백 안에서 `steps.push()`로 기록하고 계산 후 화면에 표시한다. `reduce`의 네 번째 콜백 인수로 입력 배열을 받을 수도 있지만 이 예제에서는 쓰지 않는다. [MDN: reduce()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)

## 빈 배열과 원본 보존

빈 배열에 초깃값 0을 주면 콜백을 호출하지 않고 0을 반환한다. 초깃값을 생략한 빈 배열 계산은 오류가 되므로 마지막 `, 0`을 구분해서 읽는다. [MDN: reduce()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)

이 코드는 학생 객체의 점수를 읽기만 하고 누적값은 숫자로 계산한다. `reduce`가 원본 객체를 복사해 보호하는 것은 아니다. 콜백에서 `current.score`를 직접 바꾸면 원본도 바뀐다. 배열 안 객체를 다른 값으로 변환할 때는 앞의 map 예제처럼 새 객체를 만드는 방식을 사용한다.
