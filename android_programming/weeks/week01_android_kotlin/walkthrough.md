# 1주차 따라하기 — 내 학번과 이름 출력하기

처음에는 그대로 따라 쓰고, 결과가 나오면 본인 정보로 바꾼다.
각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
1일차는 브라우저의 Kotlin Playground에서, 2일차는 Android Studio에서 실행한다.

코드의 학번 `20260001`, 이름 `홍길동`, 점수 `85`는 연습용 값이다.

## 1일차

### 1. 실행할 곳 열기

웹 브라우저에서 [Kotlin Playground](https://play.kotlinlang.org/)를 연다.
화면에서 코드를 입력하는 편집 영역과 `Run ▶` 버튼을 찾는다.
편집 영역에는 처음부터 짧은 코드가 들어 있다. 이 코드는 지우고 시작한다.

### 2. 첫 문장 출력하기

기존 코드를 지우고 아래 코드를 넣는다.

```kotlin
fun main() {
    println("안녕하세요")
}
```

`Run ▶`을 누른다. 실행 결과에 `안녕하세요`가 나오면 성공이다.

`fun main() {`와 마지막 `}`는 프로그램을 실행하는 틀이다.
이번에는 그 안의 `println()`을 바꾸는 것부터 시작한다.

### 3. 학번과 이름 쓰기

코드를 다음처럼 바꾼다. 학번과 이름은 본인 것으로 쓴다.
같은 코드가 [examples/Hello.kt](examples/Hello.kt)에 있다.

```kotlin
fun main() {
    println("학번: 20260001")
    println("이름: 홍길동")
}
```

다시 실행하면 아래처럼 두 줄이 나온다.

```text
학번: 20260001
이름: 홍길동
```

`println()` 하나가 한 줄을 출력한다. 글자를 바꾼 후에는 실행 버튼을 다시 눌러야 한다.

### 4. 코드 보관하기

편집 영역의 코드를 복사해 텍스트 편집기(메모장 등)에 붙여 넣고 `Hello.kt`로 저장한다.
파일 이름이 `Hello.kt.txt`가 되지 않았는지 확인한다.
2일차에는 이 두 줄을 Android Studio에 다시 적는다. 그때 열어 볼 파일이다.

## 2일차

### 5. 새 프로젝트 만들기

2일차부터는 브라우저 대신 **Android Studio**를 쓴다.
오늘 만드는 프로젝트를 2주차에 그대로 다시 연다.

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

### 6. StudentCard.kt 파일 만들기

1. 왼쪽 **Project** 창에서 `app` → `kotlin+java` → `com.example.studentcard`를 고른다.
2. **File › New › Kotlin Class/File**을 누른다.
3. 이름에 `StudentCard`를 쓰고 종류에서 **File**을 고른다.

`com.example.studentcard` 안에 `StudentCard.kt`가 만들어지고 편집기에 열린다.
맨 위에 `package com.example.studentcard` 줄이 들어 있으면 지우지 않고 그대로 둔다.
오늘 코드는 모두 그 줄 아래에 쓴다.

같은 폴더에 `MainActivity.kt`도 있다. 이 파일은 2주차에 열고 오늘은 고치지 않는다.

### 7. main()을 쓰고 실행하기

`StudentCard.kt`에 아래 코드를 쓴다.

```kotlin
fun main() {
    println("안녕하세요")
}
```

`fun main()` 줄의 **왼쪽 여백에 ▶ 표시**가 나타난다. 그 ▶을 누르고 **Run 'StudentCardKt'**를 고른다.
아래쪽 **Run** 창에 `안녕하세요`가 나오면 성공이다.

- 실행 이름의 `StudentCardKt`는 파일 이름 `StudentCard.kt`에서 온다. 파일 이름 뒤에 `Kt`가 붙는다.
- 위쪽 도구 막대의 `Run ▶`은 **앱을 실행하는 버튼**이다. 그것을 누르면 에뮬레이터로 앱이 뜨고 `println` 결과는 Run 창에 보이지 않는다. 오늘은 항상 왼쪽 여백의 ▶을 쓴다.
- 처음 실행할 때는 빌드에 시간이 걸린다. 창 아래쪽 진행 표시가 끝날 때까지 기다린다.
- 코드를 고친 뒤에는 ▶을 다시 눌러야 결과가 바뀐다.

### 8. 학번과 이름을 변수에 담기

1일차에 저장한 `Hello.kt`를 열어 두고, `StudentCard.kt`의 코드를 아래처럼 바꾼 뒤 다시 실행한다.

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

### 9. 값을 바꿔 확인하기

코드의 `val name = "홍길동"`에서 큰따옴표 안의 글자를 바꾸고 왼쪽 여백의 ▶으로 다시 실행한다.
이름 줄만 바뀌는지 본다. 확인한 뒤 본인 이름으로 되돌린다.

`val`은 실행 중 다른 값을 다시 대입하지 않는 변수다.
지금처럼 소스 코드의 처음 값을 고치고 새로 실행하는 것은 가능하다.
실행 중 다시 대입하면 그 줄에 빨간 줄이 그어지고 `'val' cannot be reassigned.`가 나온다.

### 10. 짧은 문법 예제 따라 하기

[기초 문법 예제](examples/README.md)의 **5. `var`**, **6. 문자열과 숫자**, **7. 주석**을 하나씩 실행한다.
`fun main() {`와 마지막 `}`는 그대로 두고 **중괄호 안의 내용만** 예제 코드로 바꾼다.
각 예제의 예상 결과와 Run 창의 결과를 비교한다.

예제를 두 개 붙여 `fun main()`이 두 개가 되면 `Conflicting overloads:` 오류가 난다.
한 번에 하나만 넣고, 다음 예제를 넣기 전에 앞의 예제를 지운다.
확인이 끝나면 8단계의 코드로 되돌린다. 이 예제들은 문법을 확인하는 연습이며 별도 제출물은 없다.

### 11. if/else와 fun 연습하기

`package` 줄 아래의 내용을 모두 지우고 아래 코드를 넣은 뒤 실행한다.
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

- `if (score >= 60) "합격" else "불합격"`: `score`가 60 이상이면 `"합격"`, 아니면 `"불합격"`이 `result`에 들어간다.
  `85`를 `50`으로 바꾸고 실행하면 `결과: 불합격`이 나온다. 확인한 뒤 `85`로 되돌린다.
- `fun intro(name: String) { ... }`: `intro`라는 함수를 만든다. `fun main()` **바깥**, 그 위에 적는다.
- `intro("홍길동")`: 함수를 호출한다. 괄호 안의 `"홍길동"`이 `name`으로 들어가 `이름: 홍길동`이 출력된다.
- `intro`는 `main` 바깥의 함수이므로 `fun main()`은 여전히 파일에 하나뿐이다.
- `//`로 시작하는 줄은 주석이라 넣지 않아도 결과는 같다.

### 12. 내 코드에 if 한 줄과 fun 하나 넣기

`package` 줄 아래를 8단계의 코드(학번·이름 두 줄)로 되돌리고, 세 곳을 고친다.

1. `fun main() {` **위**에 `intro` 함수를 정의한다(11단계 코드에서 `fun intro(name: String) {`부터 닫는 `}`까지 세 줄. 주석 줄은 넣지 않아도 된다).
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

왼쪽 여백의 ▶으로 실행하면 Run 창에 세 줄이 나온다. 학번·이름은 본인 것이어야 한다.

```text
학번: 20260001
이름: 홍길동
결과: 합격
```

- `intro(name)`: 괄호 안에 큰따옴표 없이 변수 `name`을 넣는다. 변수에 담긴 값이 함수로 들어간다.
- `intro` 정의를 `main` 안에 넣어도 실행은 되지만, 이번 주에는 **`main` 바깥, 위쪽**에 두는 것으로 통일한다.
- `else`를 빼면 `'if' must have both main and 'else' branches when used as an expression.` 오류가 난다.

### 13. 최종 결과 제출하기

완성한 코드는 프로젝트의 `app` → `kotlin+java` → `com.example.studentcard` → `StudentCard.kt`에 있다.
본인 학번과 이름, `결과:` 줄까지 세 줄이 Run 창에 나오면 그 **Run 창 화면을 캡처**한다.

제출물은 **`StudentCard.kt`와 Run 창 캡처 1장**이다.
`StudentCard` 프로젝트는 2주차에 다시 여니 제출한 뒤에도 지우지 않는다.

## 오류가 나면

1일차 Playground에서는 출력 영역의 **첫 번째 오류 줄**을 읽는다. `2:20`처럼 앞의 숫자는 줄 번호와 칸 번호다.
2일차 Android Studio에서는 틀린 곳에 **빨간 줄**이 그어지고, 실행하면 **Build** 창에 같은 문장이 나온다.
Build 창에서는 문장 앞에 `e: file:///…/StudentCard.kt:5:5`처럼 파일과 줄:칸이 붙는다.

아래는 2일차 프로젝트에서 실제로 확인한 문구다.

| 오류 문구 | 확인할 것 |
|---|---|
| `'val' cannot be reassigned.` | `val`로 만든 변수에 값을 다시 넣었다. 다시 넣어야 하면 `var`로 바꾼다 |
| `Unresolved reference 'nmae'.` | 변수 이름 철자가 다르다. 만들 때와 쓸 때를 대조한다. `studentId`의 대문자 `I`도 같아야 한다 |
| `'if' must have both main and 'else' branches when used as an expression.` | `val`에 담는 `if`에 `else`가 없다. `if (조건) 값1 else 값2`로 두 갈래를 적는다 |
| `Argument type mismatch: actual type is 'kotlin.Int', but 'kotlin.String' was expected.` | `val score = "85"`처럼 비교할 점수를 글자로 만들었다. `val score = 85`로 둔다 |
| `Conflicting overloads:` | 한 파일에 `fun main()`이 두 개다. 아래 두 줄이 그 두 위치를 가리킨다. 앞의 예제를 지운다 |

큰따옴표 `" "`, 소괄호 `( )`, 중괄호 `{ }`의 짝을 확인한다.
변수와 함수의 철자를 비교하고, 한 곳을 고친 다음 다시 실행한다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
혼자 해결하기 어려우면 코드가 보이는 화면에서 도움을 요청한다.

수업 시간 배분과 제출 기준은 [실습지](lab.md)에 있다.
