# 1주차 따라하기 — 내 학번과 이름 출력하기

처음에는 그대로 따라 쓰고, 결과가 나오면 본인 정보로 바꾼다.
각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
두 날 모두 실습실 PC의 **Android Studio**에서 실행한다. 에뮬레이터는 쓰지 않는다.

코드의 학번 `20260001`, 이름 `홍길동`, 점수 `85`는 연습용 값이다.

## 1일차

### 1. 새 프로젝트 만들기

실습실 PC에는 Android Studio가 설치되어 있다. 따로 설치하지 않는다.
오늘 만드는 프로젝트는 2주차에 그대로 다시 연다.

1. Android Studio를 실행하고 **New Project**를 누른다. 이미 열린 프로젝트가 있으면 **File › New › New Project**를 누른다.
2. **Phone and Tablet**에서 **Empty Views Activity**를 고르고 **Next**를 누른다.
   이름이 비슷한 **Empty Activity**는 고르지 않는다. 2주차에 사용할 `activity_main.xml`이 만들어지지 않는다.
3. 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Name | `StudentCard` |
| Package name | `com.example.studentcard` (Name을 쓰면 자동으로 채워진다) |
| Save location | 기본값 또는 강의자가 안내한 폴더 |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |
| Build configuration language | 기본값 |

4. 창 아래쪽 진행 표시가 모두 끝날 때까지 기다린다. 처음 만들 때는 몇 분 걸릴 수 있다.

진행 표시가 끝나기 전에는 코드를 써도 빨간 줄이 남아 있을 수 있다. 끝날 때까지 기다린다.

### 2. StudentCard.kt 파일 만들기

1. 왼쪽 **Project** 창에서 `app` → `kotlin+java` → `com.example.studentcard`를 고른다.
2. **File › New › Kotlin Class/File**을 누른다.
3. 이름에 `StudentCard`를 쓰고 종류에서 **File**을 고른다.

`com.example.studentcard` 안에 `StudentCard.kt`가 만들어지고 편집기에 열린다.
맨 위에 `package com.example.studentcard` 줄이 들어 있으면 지우지 않고 그대로 둔다.
오늘 코드는 모두 그 줄 아래에 쓴다.

같은 폴더에 `MainActivity.kt`도 있다. 이 파일은 2주차에 열고 오늘은 고치지 않는다.

### 3. main()을 쓰고 실행하기

`StudentCard.kt`에 아래 코드를 쓴다.

```kotlin
fun main() {
    println("안녕하세요")
}
```

`fun main()` 줄의 **왼쪽 여백에 ▶ 표시**가 나타난다. 그 ▶을 누르고 **Run 'StudentCardKt'**를 고른다.
아래쪽 **Run** 창에 `안녕하세요`가 나오면 성공이다.

- `fun main() {`와 마지막 `}`는 프로그램을 실행하는 틀이다. 먼저 그 안의 `println()`을 바꾸는 것부터 시작한다.
- 실행 이름의 `StudentCardKt`는 파일 이름 `StudentCard.kt`에서 온다. 파일 이름 뒤에 `Kt`가 붙는다.
- 위쪽 도구 막대의 `Run ▶`은 **앱을 실행하는 버튼**이다. 그것을 누르면 에뮬레이터로 앱이 뜨고 `println` 결과는 Run 창에 보이지 않는다. 이번 주에는 항상 왼쪽 여백의 ▶을 쓴다.
- 처음 실행할 때는 빌드에 시간이 걸린다. 창 아래쪽 진행 표시가 끝날 때까지 기다린다.
- 코드를 고친 뒤에는 ▶을 다시 눌러야 결과가 바뀐다.

### 4. 학번과 이름 쓰기

코드를 다음처럼 바꾸고 다시 실행한다. 학번과 이름은 본인 것으로 쓴다.
같은 코드가 [examples/Hello.kt](examples/Hello.kt)에 있다.

```kotlin
fun main() {
    println("학번: 20260001")
    println("이름: 홍길동")
}
```

Run 창에 아래처럼 두 줄이 나온다.

```text
학번: 20260001
이름: 홍길동
```

- `println()` 하나가 한 줄을 출력한다. 출력할 글자는 큰따옴표 `" "`로 감싼다.
- 글자를 바꾼 후에는 왼쪽 여백의 ▶을 다시 눌러야 결과가 바뀐다.

두 줄이 나오면 마지막으로 **오류 문구를 한 번 읽어 본다.** 고친 코드는 곧 되돌린다.

1. `println("이름: 홍길동")`에서 닫는 큰따옴표 하나를 지운다. 그 줄에 빨간 줄이 그어진다.
2. 왼쪽 여백의 ▶으로 실행한다. 아래쪽 **Build** 창에 `Syntax error: Expecting '"'.`가 나온다.
   같은 자리에 `Syntax error: Expecting ')'.`와 `Syntax error: Incorrect template entry: .`도 함께 나온다.
3. 문구 앞의 `e: file:///…/StudentCard.kt:5:22`이 파일 이름과 줄:칸 번호다. 그 번호로 고칠 자리를 찾는다.
4. 지운 큰따옴표를 다시 넣고 ▶으로 실행한다. 두 줄이 다시 나오면 된다.

한 곳을 틀려도 이렇게 여러 줄이 나온다. **첫 번째 줄**만 보고 한 곳을 고친 뒤 다시 실행한다.

`StudentCard.kt`의 이 두 줄은 지우지 않는다. 2일차에 이 코드에서 이어 쓴다.
**1일차에는 제출물이 없다.** Run 창에서 두 줄을 확인하면 오늘 할 일은 끝이다.

## 2일차

### 5. 학번과 이름을 변수에 담기

같은 프로젝트를 열고 `StudentCard.kt`의 코드를 아래처럼 바꾼 뒤 다시 실행한다.

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "홍길동"

    println("학번: $studentId")
    println("이름: $name")
}
```

1일차와 같은 두 줄이 Run 창에 나온다. 학번과 이름은 본인 것으로 바꾼다.

- `val studentId = ...`: 학번을 `studentId`라는 변수에 담는다.
- `val name = ...`: 이름을 `name`이라는 변수에 담는다.
- `$studentId`, `$name`: 문자열 안에서 변수의 값을 꺼내 쓴다.

### 6. 값을 바꿔 확인하기

코드의 `val name = "홍길동"`에서 큰따옴표 안의 글자를 바꾸고 왼쪽 여백의 ▶으로 다시 실행한다.
이름 줄만 바뀌는지 본다. 확인한 뒤 본인 이름으로 되돌린다.

`val`은 실행 중 다른 값을 다시 대입하지 않는 변수다.
지금처럼 소스 코드의 처음 값을 고치고 새로 실행하는 것은 가능하다.
실행 중 다시 대입하면 그 줄에 빨간 줄이 그어지고 `'val' cannot be reassigned.`가 나온다.

### 7. 예제 파일 만들어 실행하기

문법은 예제 파일을 하나씩 만들어 실행해 확인한다. `StudentCard.kt`는 고치지 않고 그대로 둔다.

1. **Project** 창에서 `com.example.studentcard`를 고르고 **File › New › Kotlin Class/File**을 누른다.
2. 이름에 `Vars`를 쓰고 종류에서 **File**을 고른다.
3. 만들어진 `Vars.kt`에 아래 코드를 넣고, `fun main()` 줄 **왼쪽 여백의 ▶** → **Run 'VarsKt'**를 누른다.

같은 코드가 [examples/Vars.kt](examples/Vars.kt)에 있다.

```kotlin
// val은 값을 한 번만 담는다. var는 나중에 다른 값을 담을 수 있다.
fun main() {
    val name = "홍길동"
    var greeting = "안녕하세요"

    println("$greeting, $name 님")

    greeting = "반갑습니다"
    println("$greeting, $name 님")
}
```

```text
안녕하세요, 홍길동 님
반갑습니다, 홍길동 님
```

- `var greeting`은 나중에 `greeting = "반갑습니다"`처럼 다른 값을 다시 넣을 수 있다.
- 같은 변수의 값을 바꿀 때는 `var`를 다시 쓰지 않는다. `greeting = ...`처럼 이름만 쓴다.
- 왼쪽 여백 ▶의 이름은 **파일 이름 + `Kt`**다. `Vars.kt`는 `Run 'VarsKt'`가 된다.

같은 방법으로 `Types`라는 파일을 만들고 아래 코드를 넣어 **Run 'TypesKt'**로 실행한다.
같은 코드가 [examples/Types.kt](examples/Types.kt)에 있다.

```kotlin
// 큰따옴표로 감싼 값은 글자(String), 큰따옴표가 없는 숫자는 정수(Int)다.
fun main() {
    val studentId = "20260001"  // String
    val score = 85              // Int

    println("학번: $studentId")
    println("점수: $score")

    println(1 + 2)
    println("1 + 2")
}
```

```text
학번: 20260001
점수: 85
3
1 + 2
```

- `"20260001"`은 큰따옴표 안에 있으므로 글자(`String`)다. 학번은 계산하지 않으므로 글자로 둔다.
- `85`는 큰따옴표가 없으므로 정수(`Int`)다.
- `println(1 + 2)`는 계산한 `3`을, `println("1 + 2")`는 글자 `1 + 2`를 그대로 출력한다.
- 같은 줄에서 `//` 뒤의 내용은 주석이라 실행되지 않는다.

`Vars.kt`, `Types.kt`, `StudentCard.kt`를 한 프로젝트에 함께 두어도 된다.
파일마다 `fun main()`이 하나씩 있는 것은 문제가 되지 않는다.
다만 **한 파일 안에** `fun main()`을 두 개 쓰면 `Conflicting overloads:` 오류가 난다.
예제를 이어 붙이지 않고 파일을 따로 만든다.

### 8. if/else로 합격·불합격 고르기

`Branch`라는 파일을 만들고 아래 코드를 넣어 **Run 'BranchKt'**로 실행한다.
같은 코드가 [examples/Branch.kt](examples/Branch.kt)에 있다.

```kotlin
// if/else는 조건이 맞을 때와 아닐 때 고를 값을 정한다.
fun main() {
    val score = 85
    val result = if (score >= 60) "합격" else "불합격"

    println("점수: $score")
    println("결과: $result")
}
```

```text
점수: 85
결과: 합격
```

- `if (조건) 값1 else 값2`: 조건이 맞으면 `값1`, 아니면 `값2`가 `result`에 들어간다.
- `score >= 60`은 "score가 60 이상인가"라는 조건이다. `>`, `<`, `<=`, `==`(같은가)도 쓸 수 있다.
- `85`를 `50`으로 바꾸고 실행하면 `결과: 불합격`이 나온다. 확인한 뒤 `85`로 되돌린다.
- `else`를 빼면 `'if' must have both main and 'else' branches when used as an expression.` 오류가 난다.

### 9. fun으로 이름 붙여 부르기

`Functions`라는 파일을 만들고 아래 코드를 넣어 **Run 'FunctionsKt'**로 실행한다.
같은 코드가 [examples/Functions.kt](examples/Functions.kt)에 있다.

```kotlin
// 함수는 하는 일에 이름을 붙인 것이다. main 바깥에 정의하고 이름으로 부른다.
fun greet(name: String) {
    println("안녕하세요, $name 님")
}

fun main() {
    greet("홍길동")
    greet("김철수")
}
```

```text
안녕하세요, 홍길동 님
안녕하세요, 김철수 님
```

- `fun greet(name: String) { ... }`: `greet`라는 함수를 만든다. `fun main()` **바깥**, 그 위에 적는다.
- `name: String`: 글자 하나를 받아서 함수 안에서 `name`이라고 부른다.
- `greet("홍길동")`: 함수를 호출한다. 괄호 안의 값이 `name`으로 들어가고 `{ }` 안의 코드가 실행된다.
- 함수를 한 번 만들면 이름으로 여러 번 부를 수 있다. 위에서는 두 번 불렀다.
- `greet()`처럼 괄호를 비우면 `No value passed for parameter 'name'.` 오류가 난다.

### 10. 내 코드에 if 한 줄과 fun 하나 넣기

먼저 `Intro`라는 파일을 만들어 `if/else`와 `fun`을 한 번에 본다.
아래 코드를 넣고 **Run 'IntroKt'**로 실행한다.
같은 코드가 [examples/Intro.kt](examples/Intro.kt)에 있다.

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

- `intro("김철수")` 아래에 `intro(...)`를 한 줄 더 넣어 이름을 하나 더 출력해 본다.
- `intro`는 `main` 바깥의 함수이므로 이 파일의 `fun main()`은 여전히 하나뿐이다.

확인이 끝나면 **`Intro.kt`를 지운다.** Project 창에서 파일을 고르고 **Delete**를 누른다.
`Intro.kt`와 아래의 `StudentCard.kt`는 둘 다 `intro` 함수를 정의하므로 함께 둘 수 없다.
함께 두고 실행하면 `Conflicting overloads:`와
`Overload resolution ambiguity between candidates:`가 나오고 두 파일의 위치를 가리킨다.
그 문구를 한 번 읽어 보는 것도 오늘의 연습이다. 읽은 뒤 `Intro.kt`를 지우고 다음으로 넘어간다.

이제 `StudentCard.kt`를 5단계의 코드(학번·이름 두 줄)에서 세 곳 고친다.

1. `fun main() {` **위**에 `intro` 함수를 정의한다(`Intro.kt`에 있던 `fun intro(name: String) {`부터 닫는 `}`까지 세 줄. 주석 줄은 넣지 않아도 된다).
2. `println("이름: $name")` 줄을 `intro(name)`으로 바꾼다.
3. `val score = 85`를 추가하고, 마지막에 `if/else` 한 줄과 `println("결과: $result")`를 넣는다.

완성한 코드 전체는 아래와 같다. 같은 코드가 [examples/StudentCard.kt](examples/StudentCard.kt)에 있다.

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

왼쪽 여백의 ▶으로 **Run 'StudentCardKt'**를 실행하면 Run 창에 세 줄이 나온다. 학번·이름은 본인 것이어야 한다.

```text
학번: 20260001
이름: 홍길동
결과: 합격
```

- `intro(name)`: 괄호 안에 큰따옴표 없이 변수 `name`을 넣는다. 변수에 담긴 값이 함수로 들어간다.
- `intro` 정의를 `main` 안에 넣어도 실행은 되지만, 이번 주에는 **`main` 바깥, 위쪽**에 두는 것으로 통일한다.
- `else`를 빼면 `'if' must have both main and 'else' branches when used as an expression.` 오류가 난다.

### 11. 최종 결과 제출하기

완성한 코드는 프로젝트의 `app` → `kotlin+java` → `com.example.studentcard` → `StudentCard.kt`에 있다.
본인 학번과 이름, `결과:` 줄까지 세 줄이 Run 창에 나오면 그 **Run 창 화면을 캡처**한다.

제출물은 **`StudentCard.kt`와 Run 창 캡처 1장**이다.
`StudentCard` 프로젝트는 2주차에 다시 여니 제출한 뒤에도 지우지 않는다.
`Vars.kt`·`Types.kt`·`Branch.kt`·`Functions.kt`는 연습용이므로 그대로 두어도 되고 지워도 된다.

## 오류가 나면

틀린 곳에는 편집기에서 **빨간 줄**이 그어진다. 그 위에 마우스를 올리면 문장이 보인다.
실행하면 **Build** 창에 같은 문장이 나오고, 문장 앞에 `e: file:///…/StudentCard.kt:5:5`처럼
파일 이름과 줄:칸 번호가 붙는다. 여러 줄이 나오면 **첫 번째 줄**부터 읽는다.

짝이 맞지 않는 따옴표·괄호처럼 문장을 읽을 수 없는 실수는 문구 앞에 `Syntax error:`가 붙는다.
아래는 이 프로젝트에서 실제로 확인한 문구다.

| 오류 문구 | 확인할 것 |
|---|---|
| `Syntax error: Expecting '"'.` | 닫는 큰따옴표가 빠졌다. `"` 두 개가 짝을 이루는지 본다. 같은 자리에 `Syntax error: Expecting ')'.`와 `Syntax error: Incorrect template entry: .`도 함께 나온다 |
| `Syntax error: Expecting ')'.` | 닫는 소괄호가 빠졌다. `println(` 뒤에 `)`가 있는지 본다 |
| `Syntax error: Expecting '}'.` | 마지막 `}`가 빠졌다. `fun main() {`의 짝인 `}`를 마지막 줄에 넣는다 |
| `Unresolved reference '학번'.` | 큰따옴표 없이 글자를 적었다. `println("학번: 20260001")`처럼 감싼다 |
| `'val' cannot be reassigned.` | `val`로 만든 변수에 값을 다시 넣었다. 다시 넣어야 하면 `var`로 바꾼다 |
| `Unresolved reference 'nmae'.` | 변수 이름 철자가 다르다. 만들 때와 쓸 때를 대조한다. `studentId`의 대문자 `I`도 같아야 한다 |
| `'if' must have both main and 'else' branches when used as an expression.` | `val`에 담는 `if`에 `else`가 없다. `if (조건) 값1 else 값2`로 두 갈래를 적는다. `if score >= 60`처럼 조건에 괄호가 없을 때도 첫 줄이 이 문구다 |
| `No value passed for parameter 'name'.` | `intro()`처럼 괄호를 비웠다. `intro(name)` 또는 `intro("홍길동")`으로 값을 넣는다 |
| `Syntax error: Expecting a top level declaration.` | 함수 정의에서 `fun`이 빠졌다. `fun intro(name: String) {`로 시작한다 |
| `Argument type mismatch: actual type is 'kotlin.Int', but 'kotlin.String' was expected.` | `val score = "85"`처럼 비교할 점수를 글자로 만들었다. `val score = 85`로 둔다 |
| `Conflicting overloads:` | 한 파일에 `fun main()`이 두 개이거나, 두 파일에 같은 이름의 함수가 있다. 아래 두 줄이 그 위치를 가리킨다. `Intro.kt`와 `StudentCard.kt`를 함께 두었는지 본다 |

큰따옴표 `" "`, 소괄호 `( )`, 중괄호 `{ }`의 짝을 확인한다.
변수와 함수의 철자를 비교하고, 한 곳을 고친 다음 다시 실행한다.
결과가 그대로면 왼쪽 여백의 ▶을 다시 눌렀는지, 그리고 실행 이름이 지금 고친 파일의 이름인지 본다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
혼자 해결하기 어려우면 코드가 보이는 화면에서 도움을 요청한다.

수업 시간 배분과 제출 기준은 [실습지](lab.md)에 있다.
