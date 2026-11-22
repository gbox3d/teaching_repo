# 배열 04: map으로 값을 바꾼 새 배열 만들기

## 실행

저장소 루트에서 다음 명령을 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

[실습 화면 열기](http://localhost:8111/specials/array_advanced/examples/04_map/)

이 예제는 [W3.CSS CDN](https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css)을 사용하므로 인터넷 연결이 필요하다.

이 예제는 브라우저 저장소를 사용하지 않는다.

## 조작과 예상 결과

| 조작 | 결과 점수 |
|---|---|
| 가산점 5 → map 실행 | 하늘 85, 바다 65, 노을 95 |
| 같은 값으로 다시 실행 | 85, 65, 95 유지, 가산점 누적 없음 |
| 가산점 10 → 실행 | 90, 70, 100 |
| 가산점 0 → 실행 | 80, 60, 90 |
| 입력 칸 비우기 → 실행 | 숫자 입력 안내, 새 계산 없음 |

원본은 매번 80, 60, 90이다. 이 예제는 단순 덧셈을 비교하므로 결과를 0~100 범위로 제한하지 않는다. 소수나 음수도 입력해 볼 수 있다.

## 콜백과 반환값

```js
const adjusted = students.map(function (student) {
    return { name: student.name, score: student.score + bonus };
});
```

`student`는 현재 학생 객체다. 콜백의 반환값 하나가 결과 배열의 항목 하나가 되므로 여기서는 학생 수와 순서가 유지된다. 필요하면 콜백의 두 번째 인수로 현재 인덱스, 세 번째로 원본 배열을 받을 수 있다. [MDN: map()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)

## 새 배열과 새 객체의 차이

새 배열을 받았다는 사실만으로 안쪽 객체가 깊게 복사되었다고 판단하지 않는다. `return student`처럼 원본 객체를 그대로 반환하면 결과도 같은 객체를 가리킨다. `student.score += bonus`로 원본 객체를 수정하면 원본 점수도 바뀌고 반복 실행 때 가산점이 누적된다.

이 예제는 `{ name: ..., score: ... }`로 매번 새 객체를 만들고 문자열·숫자 값을 넣는다. 원본을 고치지 않고 변환 결과를 얻기 위한 선택이다. 객체 안에 다른 객체가 있는 경우까지 자동으로 깊게 복사하는 코드가 아니다. [MDN: map()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)
