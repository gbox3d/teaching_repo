[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a01_kotlin_card — Android Studio 학생 카드

출처: [1주차 실습 제출](../../../week01_android_kotlin/lab.md#제출--두-가지만) · 권장 8분 · 범위 1주

1주차에 한 것처럼 Android Studio 의 `StudentCard` 프로젝트(또는 새 Empty Views Activity)에서 `fun main()` 을 실행해 학번·이름과 통과 여부를 세 줄로 출력한다. 결과는 아래쪽 **Run** 창에서 본다.

## 할 일

1. `fun main()` **위**에 함수 `intro(name: String) { ... }` 을 정의한다. 중괄호 안에서 `println("이름: $name")` 으로 한 줄을 출력한다.
2. `fun main()` 안에 `val` 세 개를 만든다. 학번 `"20260001"`, 이름 `"홍길동"`, 점수 `72`.
3. `println` 으로 첫 줄을 출력한다. `학번: 20260001`. 글자 안에 변수 값을 `$변수` 로 넣는다.
4. `intro(name)` 으로 둘째 줄을 출력한다. 괄호 안에는 큰따옴표 없이 변수 이름을 쓴다.
5. `if/else` 한 줄로 `val result` 를 만든다. 점수가 `70` 이상이면 `"통과"`, 아니면 `"재시험"` 이다. `println("결과: $result")` 로 셋째 줄을 출력한다.
6. 실행해서 세 줄이 보이는 **Run** 창을 캡처한다.

## 확인할 것

- [ ] 출력이 정확히 세 줄이다. `학번: 20260001` / `이름: 홍길동` / `결과: 통과`.
- [ ] 둘째 줄은 `main` 의 `println` 이 아니라 `intro` 함수가 출력한다.
- [ ] 점수를 `65` 로 바꾸고 다시 실행하면 셋째 줄이 `결과: 재시험` 이 된다.
- [ ] 코드에 `val`, `$`, `if`, `else`, `fun` 이 모두 보인다. 빨간 줄이 없다.

## 힌트

- 글자 안에 값 넣기: `println("학번: $studentId")`. `$` 바로 뒤에 변수 이름을 붙인다.
- `if` 한 줄: `val result = if (score >= 70) "통과" else "재시험"`. 조건이 맞으면 앞의 글자, 아니면 뒤의 글자가 `result` 에 담긴다. `else` 를 빼면 `'if' must have both main and 'else' branches when used as an expression.` 오류가 난다.
- 함수는 `main` 바깥, 위쪽에 정의하고 `main` 안에서 이름으로 부른다. `intro(name)` 의 괄호 안 값이 함수의 `name` 으로 들어가고 중괄호 안의 코드가 실행된다. `intro()` 처럼 괄호를 비우면 `No value passed for parameter 'name'.` 오류가 난다.
- `val` 은 다시 넣을 수 없는 이름, `var` 는 다시 넣을 수 있는 이름이다. 여기서는 바뀌는 값이 없으니 모두 `val` 이다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 학번 | `20260001` |
| 이름 | `홍길동` |
| 점수 | `72` |
| 기준 점수(이상) | `70` |
| 기준 이상일 때 글자 | `통과` |
| 그 밖 | `재시험` |
| 함수 이름 | `intro` |
| 다시 넣어 볼 점수 | `65` |

## 설명 물음(시험에서 1~2문장)

- `val` 과 `var` 의 차이는 무엇인가?
- `"학번: $studentId"` 에서 `$` 는 무슨 일을 하나?
- `intro(name)` 의 괄호 안 값은 함수 안에서 어떤 이름으로 쓰이나?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
