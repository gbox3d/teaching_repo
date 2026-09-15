# 1주차 예제 — Kotlin 기초 문법

[Kotlin Playground](https://play.kotlinlang.org/)의 편집 영역에 코드를 넣고 `Run ▶`을 누른다.
아래 예제는 **한 번에 하나씩** 실행한다. 새 예제를 넣을 때는 이전 코드를 지운다.
학번 `20260001`, 이름 `홍길동`, 점수 `85`는 연습용 값이다.

## 이번 주에 사용할 파일

| 파일 | 용도 | 실행 결과 |
|---|---|---|
| [Hello.kt](Hello.kt) | 1일차: 큰따옴표 안의 학번과 이름 바꾸기 | 학번·이름 두 줄 |
| [Intro.kt](Intro.kt) | 2일차: `if/else`와 `fun` 연습 | 결과 한 줄 + 이름 두 줄 |
| [StudentCard.kt](StudentCard.kt) | 2일차 완성본: 변수·`if`·`fun`으로 자기소개 출력. **제출 형태** | 학번·이름·결과 세 줄 |

세 파일은 각각 독립된 예제다. Playground에는 한 파일의 코드만 넣는다.
코드를 보관할 때는 텍스트 편집기에 복사해 해당 이름으로 저장한다.

## 1. 시작하는 틀과 `println`

```kotlin
fun main() {
    println("안녕하세요")
}
```

```text
안녕하세요
```

- `fun main()`은 프로그램이 시작하는 부분이다. 지금은 이 틀을 그대로 사용한다.
- `{ }` 안에 실행할 코드를 쓴다.
- `println()`은 소괄호 안의 내용을 출력하고 줄을 바꾼다.
- 출력할 글자는 큰따옴표 `" "`로 감싼다. 한 줄씩 쓸 때 끝에 세미콜론은 필요 없다.

## 2. 학번과 이름을 두 줄로 출력하기

[Hello.kt](Hello.kt)의 전체 코드를 복사해 실행한다.

```kotlin
fun main() {
    println("학번: 20260001")
    println("이름: 홍길동")
}
```

```text
학번: 20260001
이름: 홍길동
```

큰따옴표 안의 학번과 이름을 바꾸고 다시 실행해 본다.

## 3. `val` — 값에 이름 붙이기

```kotlin
fun main() {
    val name = "홍길동"
    println(name)
}
```

```text
홍길동
```

`name`이라는 변수에 `홍길동`을 담았다. `println(name)`은 변수 안의 값을 출력한다.
`println("name")`처럼 큰따옴표로 감싸면 `name`이라는 글자 자체가 나온다.

`val` 변수에는 실행 중 다른 값을 다시 대입할 수 없다. 코드를 편집할 때
`"홍길동"`을 본인 이름으로 바꾸고 새로 실행하는 것은 가능하다.

## 4. `$변수이름` — 문장 안에 값 넣기

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "홍길동"

    println("학번: $studentId")
    println("이름: $name")
}
```

```text
학번: 20260001
이름: 홍길동
```

`"이름: $name"`에서 `$name` 자리에 변수의 값이 들어간다. 이를 **문자열 템플릿**이라고 한다.
`studentId`의 `I`는 대문자다. 변수를 만들 때와 사용할 때 철자를 같게 쓴다.
2일차 실습의 앞부분(학번·이름 두 줄)은 여기까지다.

## 5. `var` — 실행 중 값 바꾸기

```kotlin
fun main() {
    var greeting = "안녕하세요"
    println(greeting)

    greeting = "반갑습니다"
    println(greeting)
}
```

```text
안녕하세요
반갑습니다
```

변수를 처음 만들 때만 `var`를 쓴다. 같은 변수의 값을 바꿀 때는 `greeting = ...`처럼 쓴다.
이 예제처럼 실행 중 값이 바뀌면 `var`, 학번과 이름처럼 다시 대입하지 않으면 `val`을 사용한다.
`val`로 만든 변수에 다시 대입하면 `'val' cannot be reassigned.` 오류가 난다.

## 6. 문자열과 숫자

```kotlin
fun main() {
    val studentId = "20260001"
    val week = 1

    println(studentId)
    println(week)
    println(1 + 2)
    println("1 + 2")
}
```

```text
20260001
1
3
1 + 2
```

- `"20260001"`은 **문자열(`String`)**이다. 숫자 모양이어도 큰따옴표 안에 있으므로 글자로 다룬다.
- `1`은 **정수(`Int`)**다. `1 + 2`처럼 계산할 수 있다.
- `"1 + 2"`는 계산하지 않고 글자 그대로 출력한다.

이번 예제에서는 Kotlin이 오른쪽 값을 보고 자료형을 알아내므로 `String`이나 `Int`를 직접 적지 않아도 된다.
학번은 앞자리의 `0`도 그대로 표시할 수 있도록 문자열로 둔다.

## 7. `//` — 코드에 설명 남기기

```kotlin
fun main() {
    // 이 줄은 메모이므로 실행되지 않는다.
    println("오늘은 Kotlin 첫 실습입니다")
}
```

```text
오늘은 Kotlin 첫 실습입니다
```

같은 줄에서 `//` 뒤의 내용은 **주석**, 즉 코드를 읽는 사람을 위한 설명이다.

## 8. `if/else` — 조건에 따라 다른 값

```kotlin
fun main() {
    val score = 85
    val result = if (score >= 60) "합격" else "불합격"
    println("결과: $result")
}
```

```text
결과: 합격
```

- `if (조건) 값1 else 값2`: 조건이 맞으면 `값1`, 아니면 `값2`가 된다. 이 값을 `result`에 담는다.
- `score >= 60`은 "score가 60 이상인가"라는 조건이다. `>`, `<`, `<=`, `==`(같은가)도 쓸 수 있다.
- `85`를 `50`으로 바꾸면 `결과: 불합격`이 나온다.
- `else`를 빼면 `'if' must have both main and 'else' branches when used as an expression.` 오류가 난다.

같은 뜻을 중괄호로 나눠 쓸 수도 있다. 2주차의 버튼 코드에서 이 모양을 다시 본다.

```kotlin
if (score >= 60) {
    println("결과: 합격")
} else {
    println("결과: 불합격")
}
```

## 9. `fun` — 함수 정의와 호출

```kotlin
fun intro(name: String) {
    println("이름: $name")
}

fun main() {
    intro("홍길동")
    intro("김철수")
}
```

```text
이름: 홍길동
이름: 김철수
```

- `fun intro(name: String) { ... }`: `intro`라는 **함수**를 정의한다. `main` 바깥, 위쪽에 적는다.
- `name: String`: 글자 하나를 받아서 함수 안에서 `name`이라고 부른다.
- `intro("홍길동")`: 함수를 **호출**한다. 괄호 안의 값이 `name`에 들어가고 `{ }` 안의 코드가 실행된다.
- `main`도 함수다. 실행 버튼을 누르면 `main`이 먼저 불린다.
- `intro()`처럼 괄호를 비우면 `no value passed for parameter 'name'.` 오류가 난다.

## 10. 2일차 연습 — if와 fun 한 번에

[Intro.kt](Intro.kt)의 전체 코드다. 8번과 9번을 한 파일에 모았다.

```kotlin
// 이름을 받아 한 줄을 출력하는 함수. main 바깥에 정의한다.
fun intro(name: String) {
    println("이름: $name")
}

fun main() {
    // if/else: 점수가 60 이상이면 "합격", 아니면 "불합격"
    val score = 85
    val result = if (score >= 60) "합격" else "불합격"
    println("결과: $result")

    // 함수 호출: 괄호 안의 값이 name으로 들어간다
    intro("홍길동")
    intro("김철수")
}
```

```text
결과: 합격
이름: 홍길동
이름: 김철수
```

## 11. 2일차 완성 — 자기소개 세 줄

[StudentCard.kt](StudentCard.kt)의 전체 코드다. **2일차 최종 실습과 제출 형태는 여기까지다.**

```kotlin
// 이름을 받아 "이름: ..." 한 줄을 출력하는 함수
fun intro(name: String) {
    println("이름: $name")
}

fun main() {
    val studentId = "20260001"
    val name = "홍길동"
    val score = 85

    println("학번: $studentId")
    intro(name)

    val result = if (score >= 60) "합격" else "불합격"
    println("결과: $result")
}
```

```text
학번: 20260001
이름: 홍길동
결과: 합격
```

- `intro(name)`: 큰따옴표 없이 변수 `name`을 넣는다. 변수에 담긴 값이 함수로 들어간다.
- 4번 코드에 `intro` 정의, `val score`, `if` 한 줄, `println("결과: ...")`가 더해졌다.

## 공식 참고 자료

- [Kotlin 기본 문법](https://kotlinlang.org/docs/basic-syntax.html)
- [Kotlin Playground 사용 안내](https://kotlinlang.org/docs/run-code-snippets.html#browser-kotlin-playground)
- [Kotlin if 표현식](https://kotlinlang.org/docs/control-flow.html#if-expression)
- [Kotlin 함수](https://kotlinlang.org/docs/functions.html)
