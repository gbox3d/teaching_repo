# 1주차 예제 — Kotlin 기초 문법

모든 예제는 실습실 PC의 **Android Studio**에서 실행한다.
1일차에 만든 `StudentCard` 프로젝트를 열고, 2일차 예제는 파일을 하나씩 만든다.

1. **Project** 창에서 `app` → `kotlin+java` → `com.example.studentcard`를 고른다.
2. **File › New › Kotlin Class/File**을 누르고 이름을 쓴 뒤 종류에서 **File**을 고른다.
3. 만들어진 파일에 코드를 넣고, `fun main()` 줄 **왼쪽 여백의 ▶**을 눌러 실행한다.
4. 아래쪽 **Run** 창에서 결과를 본다.

왼쪽 여백 ▶의 이름은 **파일 이름 + `Kt`**다. `Vars.kt`는 `Run 'VarsKt'`가 된다.
위쪽 도구 막대의 `Run ▶`은 앱을 실행하는 버튼이라 에뮬레이터가 뜨고 `println` 결과는 Run 창에 보이지 않는다.
맨 위에 `package com.example.studentcard` 줄이 들어 있으면 지우지 않고 그대로 둔다.

학번 `20260001`, 이름 `홍길동`, 점수 `85`는 연습용 값이다.
짝이 맞지 않는 따옴표·괄호처럼 문장을 읽을 수 없는 실수는 Build 창의 문구 앞에 `Syntax error:`가 붙는다.
실측한 오류 문구는 [실습지의 막혔을 때](../lab.md#막혔을-때)에 정리해 두었다.

## 이번 주에 사용할 파일

| 파일 | 다루는 문법 | Run 창 결과 |
|---|---|---|
| [Hello.kt](Hello.kt) | `fun main`·`println`·큰따옴표. **1일차 완성 예시(참고용)** | `학번: 20260001` / `이름: 홍길동` |
| [Vars.kt](Vars.kt) | `val`·`var`·`$변수이름` | `안녕하세요, 홍길동 님` / `반갑습니다, 홍길동 님` |
| [Types.kt](Types.kt) | `String`·`Int`·주석·`1 + 2`와 `"1 + 2"` | `학번: 20260001` / `점수: 85` / `3` / `1 + 2` |
| [Branch.kt](Branch.kt) | `if/else`를 `val`에 담기 | `점수: 85` / `결과: 합격` |
| [Functions.kt](Functions.kt) | `fun greet(name: String)` 정의와 두 번 호출 | `안녕하세요, 홍길동 님` / `안녕하세요, 김철수 님` |
| [Intro.kt](Intro.kt) | `if/else` + `fun intro`를 한 파일에 | `결과: 합격` / `이름: 홍길동` / `이름: 김철수` |
| [StudentCard.kt](StudentCard.kt) | 완성본: 변수·`if`·`fun`. **제출 형태** | `학번: 20260001` / `이름: 홍길동` / `결과: 합격` |

`Hello.kt`는 1일차에 `StudentCard.kt`가 어떤 모양이 되는지 보여 주는 참고용 파일이다. 따로 만들지 않는다.
2일차의 `Vars.kt`·`Types.kt`·`Branch.kt`·`Functions.kt`·`Intro.kt`는 파일을 만들어 실행한다.
`StudentCard.kt`는 프로젝트에 이미 있으므로 고쳐 쓴다.

### 파일을 함께 두어도 되는 경우

- 예제 파일 여러 개를 한 프로젝트에 **함께 두어도 된다.** 파일마다 `fun main()`이 하나씩 있어도 서로 방해하지 않는다.
- 다만 **한 파일 안에** `fun main()`을 두 개 쓰면 `Conflicting overloads:` 오류가 난다. 예제를 이어 붙이지 말고 파일을 따로 만든다.
- **같은 이름의 함수를 두 파일에 정의하면 빌드가 실패한다.** `Intro.kt`와 `StudentCard.kt`는 둘 다 `intro`를 정의하므로 **함께 둘 수 없다.**
  `Conflicting overloads:`와 `Overload resolution ambiguity between candidates:`가 나오고 두 파일의 위치를 가리킨다.
  순서는 **`Intro.kt`를 만들어 실행 → `Intro.kt` 삭제 → `StudentCard.kt` 고치기**다.
  지우기 전에 한 번 함께 두고 그 오류를 읽어 보는 것도 이번 주 내용이다.

## 1. 시작하는 틀과 `println`

1일차의 첫 실행이다. `StudentCard.kt`에 아래 코드를 쓰고 왼쪽 여백의 ▶으로 실행한다.

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

[Hello.kt](Hello.kt)의 전체 코드다. 1일차에는 `StudentCard.kt`를 이 모양으로 고친다.
`Hello.kt`라는 파일을 따로 만들지는 않는다.

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

큰따옴표 안의 학번과 이름을 본인 것으로 바꾸고 다시 실행해 본다.

## 3. `val` — 값에 이름 붙이기

여기부터 2일차다.

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
`val`과 `var`를 한 번에 보려면 [Vars.kt](Vars.kt)를 만들어 실행한다.

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
철자가 다르면 `Unresolved reference 'nmae'.`처럼 그 이름을 찾을 수 없다는 오류가 난다.
2일차에 `StudentCard.kt`를 고치는 앞부분은 여기까지다.

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

실습에서는 [Vars.kt](Vars.kt)를 만들어 실행한다. 위 문법에 `$변수이름`이 함께 들어 있다.

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
실습에서는 [Types.kt](Types.kt)를 만들어 실행한다.

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
[Types.kt](Types.kt)에도 `// String`, `// Int`처럼 주석이 붙어 있다.

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

실습에서는 [Branch.kt](Branch.kt)를 만들어 실행한다. 점수 줄이 함께 출력된다.

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
- `main`도 함수다. 왼쪽 여백의 ▶을 누르면 `main`이 먼저 불린다.
- `intro()`처럼 괄호를 비우면 `No value passed for parameter 'name'.` 오류가 난다.

실습에서는 [Functions.kt](Functions.kt)를 만들어 실행한다. 함수 이름이 `greet`이고 인사말을 출력한다.
위 코드를 그대로 파일로 만들 때는 이름을 `Intro`로 하지 않는다. 10번과 11번의 제약을 먼저 읽는다.

## 10. 2일차 연습 — if와 fun 한 번에

[Intro.kt](Intro.kt)의 전체 코드다. 8번과 9번을 한 파일에 모았다.
`Intro`라는 파일을 만들어 넣고 `Run 'IntroKt'`로 실행한다.

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

확인이 끝나면 **`Intro.kt`를 지운다.** 11번의 `StudentCard.kt`도 `intro`를 정의하므로 두 파일을 함께 둘 수 없다.
지우기 전에 한 번 함께 두고 `Conflicting overloads:` 문구를 읽어 본다.

## 11. 2일차 완성 — 자기소개 세 줄

[StudentCard.kt](StudentCard.kt)의 전체 코드다. **2일차 최종 실습과 제출 형태는 여기까지다.**
프로젝트의 `StudentCard.kt`를 이 모양으로 고친다.
제출물은 이 코드가 담긴 `StudentCard.kt`와 세 줄이 보이는 Run 창 캡처 1장이다.

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
- `Intro.kt`를 지우지 않고 실행하면 `Conflicting overloads:`가 나온다. 먼저 `Intro.kt`를 지운다.

## 공식 참고 자료

- [Android Studio 소개](https://developer.android.com/studio/intro)
- [Kotlin 기본 문법](https://kotlinlang.org/docs/basic-syntax.html)
- [Kotlin if 표현식](https://kotlinlang.org/docs/control-flow.html#if-expression)
- [Kotlin 함수](https://kotlinlang.org/docs/functions.html)
