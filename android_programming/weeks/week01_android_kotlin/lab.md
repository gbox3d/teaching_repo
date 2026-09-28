# 1주차 실습 — 내 학번과 이름 출력하기

이번 실습은 짧은 코드를 직접 바꿔 실행하는 연습이다. 처음에는 예제를 그대로 옮기고,
실행에 성공하면 학번과 이름을 본인 것으로 바꾼다.
두 날 모두 실습실 PC의 **Android Studio**에서 실행한다. 에뮬레이터는 쓰지 않는다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 글자 두 줄 출력하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–15분 | `StudentCard` 프로젝트를 만들고 `StudentCard.kt`에서 첫 출력을 실행한다 |
| 15–30분 | 학번과 이름을 각각 한 줄에 출력한다 |
| 30–45분 | 큰따옴표 안을 내 학번·이름으로 바꾸고 다시 실행한다 |
| 45–55분 | 오류를 일부러 만들어 Build 창의 문구를 읽어 본다 |
| 55–60분 | 오타를 확인하고 프로젝트를 그대로 둔다 |

오늘 만드는 `StudentCard` 프로젝트는 2일차와 2주차에 그대로 다시 연다. 실습이 끝나도 지우지 않는다.

### 1. 프로젝트를 만들고 첫 출력 실행하기

Android Studio에서 **New Project**를 누르고 **Phone and Tablet**의 **Empty Views Activity**를 고른다.
이름이 비슷한 **Empty Activity**는 고르지 않는다. 그다음 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Name | `StudentCard` |
| Package name | `com.example.studentcard` (Name을 쓰면 자동으로 채워진다) |
| Save location | 기본값 또는 강의자가 안내한 폴더 |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |
| Build configuration language | 기본값 |

창 아래쪽 진행 표시가 끝나면 아래 두 가지를 한다. 자세한 순서는
[따라하기 1~3단계](walkthrough.md#1-새-프로젝트-만들기)에 있다.

1. **Project** 창에서 `app` → `kotlin+java` → `com.example.studentcard`를 고르고
   **File › New › Kotlin Class/File**로 이름 `StudentCard`, 종류 **File**을 만든다.
2. 만들어진 `StudentCard.kt`에 아래 코드를 쓰고, `fun main()` 줄 **왼쪽 여백의 ▶**을 눌러
   **Run 'StudentCardKt'**를 고른다.

```kotlin
fun main() {
    println("안녕하세요")
}
```

아래쪽 **Run** 창에 `안녕하세요`가 나오면 첫 실행 성공이다.
위쪽 도구 막대의 `Run ▶`은 앱을 실행하는 버튼이라 에뮬레이터가 뜨고 `println` 결과는 Run 창에 보이지 않는다.
이번 주에는 항상 왼쪽 여백의 ▶을 쓴다. 처음 실행할 때는 빌드에 시간이 걸린다.

### 2. 학번과 이름 두 줄 출력하기

`fun main() {`와 마지막 `}`는 그대로 두고 그 사이를 고쳐 아래 결과를 만든다.

```text
학번: 20260001
이름: 홍길동
```

- 글자는 큰따옴표 `" "` 안에 쓴다.
- 한 줄을 출력할 때마다 `println()`을 하나씩 쓴다.
- 코드를 고친 뒤에는 왼쪽 여백의 ▶을 다시 누른다.

막히면 [따라하기 4단계](walkthrough.md#4-학번과-이름-쓰기)의 코드와 한 줄씩 비교한다.

### 3. 내 학번과 이름으로 바꾸기

큰따옴표 안의 `20260001`과 `홍길동`을 본인 것으로 바꾸고 다시 실행한다.
`학번: `, `이름: ` 부분은 그대로 둔다. 처음에는 **큰따옴표 안의 글자만** 바꾼다.

### 4. 오류 문구 읽어 보기

오류 문구를 읽는 연습을 한 번 한다. 고친 코드는 곧 되돌린다.

1. `println("이름: 홍길동")`에서 **닫는 큰따옴표 하나를 지운다.** 그 줄에 빨간 줄이 그어진다.
2. 왼쪽 여백의 ▶으로 실행한다. 아래쪽 **Build** 창에 `Syntax error: Expecting '"'.`가 나온다.
   같은 자리에 `Syntax error: Expecting ')'.`와 `Syntax error: Incorrect template entry: .`도 함께 나온다.
3. 문구 앞의 `e: file:///…/StudentCard.kt:5:22`이 파일 이름과 줄:칸 번호다. 그 번호로 고칠 자리를 찾는다.
4. 지운 큰따옴표를 다시 넣고 ▶으로 실행한다. 두 줄이 다시 나오면 된다.

한 곳을 틀려도 이렇게 여러 줄이 나온다. **첫 번째 줄**만 보고 한 곳을 고친 뒤 다시 실행한다.
자주 나오는 문구는 [막혔을 때](#막혔을-때)에 정리해 두었다.

### 5. 오늘 확인할 것

- [ ] `StudentCard` 프로젝트를 만들고 `StudentCard.kt`의 `main()`을 실행했다.
- [ ] 내 학번과 이름이 Run 창에 두 줄로 보인다.
- [ ] 글자를 고친 뒤 왼쪽 여백의 ▶을 다시 눌러 결과를 확인했다.
- [ ] 오류를 일부러 만들어 Build 창의 문구를 한 번 읽고 되돌렸다.

**1일차에는 제출물이 없다.** 위 네 가지를 확인하면 오늘 할 일은 끝이다.
1일차 코드는 프로젝트에 그대로 둔다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 변수와 if, fun으로 자기소개 완성하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 지난 시간의 `StudentCard.kt`를 열고 다시 실행한다 |
| 10–22분 | `val`에 학번과 이름을 담고 `$변수이름`으로 두 줄을 출력한다 |
| 22–34분 | 예제 `Vars.kt`·`Types.kt`를 만들어 `var`와 글자·정수를 확인한다 |
| 34–46분 | 예제 `Branch.kt`·`Functions.kt`를 만들어 `if/else`와 `fun`을 확인한다 |
| 46–56분 | 내 코드에 `if` 한 줄과 `fun` 하나를 넣어 세 줄을 출력한다 |
| 56–60분 | 최종 코드와 Run 창 캡처를 정리해 제출한다 |

`StudentCard` 프로젝트는 2주차에 그대로 다시 연다. 실습이 끝나도 지우지 않는다.
개인 노트북에 Android Studio를 설치할 학생은 실습 **마지막 15분**에 조교에게 설치 상태를 확인받는다.
실습실 PC를 쓰는 학생은 해당 없다.

### 1. 지난 시간 코드 다시 실행하기

Android Studio를 열면 지난 시간의 `StudentCard` 프로젝트가 그대로 열린다.
열리지 않으면 **File › Open**으로 프로젝트 폴더를 고른다.
`StudentCard.kt`를 열고 왼쪽 여백의 ▶ → **Run 'StudentCardKt'**로 학번·이름 두 줄이 나오는지 확인한다.

프로젝트를 잃어버린 학생은 [따라하기 1~3단계](walkthrough.md#1-새-프로젝트-만들기)대로 다시 만든다.

### 2. 값을 담을 자리 만들기

`StudentCard.kt`의 코드를 아래처럼 바꾸고, 큰따옴표 안을 본인 정보로 바꾼다.

```kotlin
fun main() {
    val studentId = "20260001"
    val name = "홍길동"

    // 이 아래에 학번과 이름을 출력하는 코드를 적는다.
}
```

학번은 계산할 숫자가 아니라 표시할 글자로 다룬다. 큰따옴표를 유지한다.

### 3. 변수의 값 출력하기

이름 출력의 힌트는 다음과 같다.

```kotlin
println("이름: $name")
```

같은 방법으로 학번 출력도 작성한다. 결과는 1일차처럼 학번과 이름 두 줄이면 된다.
막히면 [기초 문법 예제](examples/README.md)나 [따라하기 5단계](walkthrough.md#5-학번과-이름을-변수에-담기)를 펼쳐도 된다.

### 4. 예제 파일로 문법 확인하기

`StudentCard.kt`는 그대로 두고, 예제를 **파일 하나씩** 만들어 실행한다.
**File › New › Kotlin Class/File**로 이름을 쓰고 종류는 **File**을 고른다.

| 만들 파일 | 볼 것 | Run 창 결과 |
|---|---|---|
| [Vars.kt](examples/Vars.kt) | `val`과 `var`, `$변수이름` | `안녕하세요, 홍길동 님` / `반갑습니다, 홍길동 님` |
| [Types.kt](examples/Types.kt) | 글자(`String`)와 정수(`Int`), 주석 | `학번: 20260001` / `점수: 85` / `3` / `1 + 2` |

- `var`에 담긴 인사말을 바꾸고 바꾸기 전후의 출력을 비교한다.
- `println(1 + 2)`와 `println("1 + 2")`의 결과를 비교한다.
- 예제 파일과 `StudentCard.kt`를 한 프로젝트에 함께 두어도 된다. 파일마다 `fun main()`이 하나씩 있는 것은 문제가 되지 않는다.
- 다만 **한 파일 안에** `fun main()`을 두 개 쓰면 `Conflicting overloads:` 오류가 난다. 예제를 이어 붙이지 않고 파일을 따로 만든다.

이 연습은 별도 보고서 없이 Run 창에서 확인한다. 시간이 부족하면 5번부터 한다.

### 5. if/else와 fun 예제 실행하기

같은 방법으로 파일 두 개를 더 만들어 실행한다.

| 만들 파일 | 볼 것 | Run 창 결과 |
|---|---|---|
| [Branch.kt](examples/Branch.kt) | `if/else`의 결과를 `val`에 담기 | `점수: 85` / `결과: 합격` |
| [Functions.kt](examples/Functions.kt) | `fun greet(name: String)` 정의와 호출 | `안녕하세요, 홍길동 님` / `안녕하세요, 김철수 님` |

- `Branch.kt`의 `val score = 85`를 `50`으로 바꾸고 실행하면 결과 줄이 어떻게 되는지 본다. 본 뒤 `85`로 되돌린다.
- `Functions.kt`에 `greet(...)`를 한 줄 더 넣어 이름을 하나 더 출력해 본다.

### 6. 내 코드에 if 한 줄과 fun 하나 넣기

먼저 `Intro`라는 파일을 만들어 [Intro.kt](examples/Intro.kt)의 코드를 넣고 실행한다.
`if/else`와 `fun`이 한 파일에 같이 있는 모양이다. Run 창에 아래 세 줄이 나온다.

```text
결과: 합격
이름: 홍길동
이름: 김철수
```

확인이 끝나면 **`Intro.kt`를 지운다.** `Intro.kt`와 아래에서 고칠 `StudentCard.kt`는
둘 다 `intro` 함수를 정의하므로 함께 둘 수 없다. 함께 두면 빌드가 멈춘다.
지우기 전에 한 번 함께 두고 실행해 `Conflicting overloads:` 문구를 읽어 보는 것도 오늘의 연습이다.

그다음 `StudentCard.kt`(학번·이름 두 줄)에 아래 세 가지를 추가한다. 결과는 세 줄이다.

```text
학번: 20260001
이름: 홍길동
결과: 합격
```

- `fun main() {` **위**에 `fun intro(name: String) { ... }`를 정의한다. `Intro.kt`에 있던 그대로다.
- `println("이름: $name")` 줄을 `intro(name)`으로 바꾼다. 괄호 안에는 큰따옴표 없이 변수 이름을 쓴다.
- `val score = 85`를 추가하고, `if (score >= 60) "합격" else "불합격"`으로 `result`를 만들어 `println("결과: $result")`로 출력한다.

힌트: `if` 줄과 `println("결과: ...")` 줄은 `Intro.kt`의 `main` 안에 있는 두 줄과 같다.
막히면 [따라하기 10단계](walkthrough.md#10-내-코드에-if-한-줄과-fun-하나-넣기)의 완성 코드와 한 줄씩 비교한다.

## 막혔을 때

틀린 곳에는 편집기에서 **빨간 줄**이 그어진다. 그 위에 마우스를 올리면 문장이 보인다.
실행하면 **Build** 창에 같은 문장이 나오고, 문장 앞에 `e: file:///…/StudentCard.kt:5:5`처럼
파일 이름과 줄:칸 번호가 붙는다.

짝이 맞지 않는 따옴표·괄호처럼 문장을 읽을 수 없는 실수는 문구 앞에 `Syntax error:`가 붙고,
한 곳을 틀려도 여러 줄이 함께 나온다. **첫 번째 줄**만 보고 한 곳을 고친 뒤 다시 실행한다.
아래 문구는 이 프로젝트에서 실제로 실행해 확인한 것이다.

| 상황·오류 문구 | 확인할 것 |
|---|---|
| `Syntax error: Expecting '"'.` | 닫는 큰따옴표가 빠졌다. `println("안녕하세요")`처럼 `"` 두 개가 짝을 이루는지 본다. 같은 자리에 `Syntax error: Expecting ')'.`와 `Syntax error: Incorrect template entry: .`도 함께 나온다 |
| `Syntax error: Expecting ')'.` | 닫는 소괄호가 빠졌다. `println(` 뒤에 `)`가 있는지 본다 |
| `Syntax error: Expecting '}'.` | 마지막 `}`가 빠졌다. `fun main() {`의 짝인 `}`를 마지막 줄에 넣는다 |
| `Unresolved reference '학번'.` | 큰따옴표 없이 글자를 적었다. `println("학번: 20260001")`처럼 감싼다. `Syntax error: Expecting ')'.`와 `Syntax error: Unexpected tokens (use ';' to separate expressions on the same line).`도 함께 나온다 |
| `Unresolved reference 'nmae'.` | 변수 이름 철자가 다르다. 만들 때와 쓸 때를 대조한다. `studentId`의 대문자 `I`도 같아야 한다 |
| `'val' cannot be reassigned.` | `val`로 만든 변수에 다시 값을 넣었다. 다시 넣어야 하면 `var`로 바꾼다 |
| `'if' must have both main and 'else' branches when used as an expression.` | `else "불합격"`이 빠졌다. `if (조건) 값1 else 값2` 두 갈래를 모두 적는다. **`if score >= 60`처럼 조건에 괄호가 없을 때도 첫 줄이 이 문구다.** 뒤에 `Syntax error: Expecting a condition in parentheses '(...)'.`와 `Syntax error: Unexpected tokens (use ';' to separate expressions on the same line).`가 함께 나오면 `else`가 아니라 괄호가 빠진 것이다 |
| `No value passed for parameter 'name'.` | `intro()`처럼 괄호를 비웠다. `intro(name)` 또는 `intro("홍길동")`으로 값을 넣는다 |
| `Syntax error: Expecting a top level declaration.` | 함수 정의에서 `fun`이 빠졌다. `fun intro(name: String) {`로 시작한다. 같은 줄을 가리키며 여러 번 나온다 |
| `Argument type mismatch: actual type is 'kotlin.Int', but 'kotlin.String' was expected.` | `val score = "85"`처럼 비교할 점수를 글자로 만들었다. `val score = 85`로 둔다 |
| `Conflicting overloads:` | 한 파일에 `fun main()`이 두 개이거나, 두 파일에 같은 이름의 함수가 있다 |
| `Overload resolution ambiguity between candidates:` | 위와 같은 원인이다. `Intro.kt`와 `StudentCard.kt`를 함께 두었는지 본다. `Intro.kt`를 지운다 |
| `name`이라는 글자가 그대로 나온다 | 오류는 아니다. `"$name"`처럼 `$`를 붙였는지 본다 |
| 고쳤는데 결과가 같다 | 왼쪽 여백의 ▶을 다시 눌렀는지, 실행 이름이 지금 고친 파일의 이름인지 본다 |
| Run 창 대신 에뮬레이터가 뜬다 | 위쪽 도구 막대의 `Run ▶`을 눌렀다. `fun main()` 줄 **왼쪽 여백의 ▶**을 쓴다 |

문구는 버전에 따라 조금 다를 수 있다. 빨간 줄이 그어진 자리를 함께 본다.

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 현재 코드를 그대로 보여 주고 도움을 받는다.

## 제출 — 두 가지만

1. **`StudentCard.kt`**: 프로젝트의 `app` → `kotlin+java` → `com.example.studentcard` 안에 있는 최종 코드.
   본인 학번과 이름을 `val`에 담고, `intro` 함수와 `if/else` 한 줄로 세 줄을 출력한다
2. **Run 창 캡처 1장**: 학번·이름·결과 세 줄이 보이는 **Run** 창 화면

`println()`으로 학번과 이름이 나오면 기본 출력 성공이다. `if`와 `fun`은 예제와 도움을 받아 마무리해도 된다.
`Vars.kt`·`Types.kt`·`Branch.kt`·`Functions.kt`는 연습용이므로 제출하지 않는다. 지우지 않아도 된다.
`StudentCard` 프로젝트는 2주차에 다시 여니 제출한 뒤에도 지우지 않는다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 인사말을 `var greeting = "안녕하세요"`에 담아 첫 줄에 출력하고, `main` 끝에서 `greeting = "다음 주에 만나요"`로 바꿔 한 번 더 출력해 본다.
- 자기소개 아래에 `좋아하는 것: 음악`처럼 한 줄을 더 출력해 본다.
- `intro`처럼 `fun showId(studentId: String)` 함수를 만들어 학번 줄도 함수로 출력해 본다.

추가 과제는 선택 사항이다.
