# 1주차 예제 — Kotlin 기초 문법

[Kotlin Playground](https://play.kotlinlang.org/)의 편집 영역에 코드를 넣고 `Run ▶`을 누른다.
아래 예제는 **한 번에 하나씩** 실행한다. 새 예제를 넣을 때는 이전 코드를 지운다.
학번 `20260001`과 이름 `홍길동`은 연습용 값이다.

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

[StudentCard.kt](StudentCard.kt)의 전체 코드다. **2일차 최종 실습은 여기까지다.**

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

## 이번 주에 사용할 파일

| 파일 | 용도 |
|---|---|
| [Hello.kt](Hello.kt) | 1일차: 큰따옴표 안의 학번과 이름 바꾸기 |
| [StudentCard.kt](StudentCard.kt) | 2일차: 변수에 담은 학번과 이름 출력하기 |

두 파일은 각각 독립된 예제다. Playground에는 한 파일의 코드만 넣는다.
코드를 보관할 때는 텍스트 편집기에 복사해 해당 이름으로 저장한다.

## 공식 참고 자료

- [Kotlin 기본 문법](https://kotlinlang.org/docs/basic-syntax.html)
- [Kotlin Playground 사용 안내](https://kotlinlang.org/docs/run-code-snippets.html#browser-kotlin-playground)
