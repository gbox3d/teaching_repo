# 1주차 실습 — 내 학번과 이름 출력하기

이번 실습은 짧은 코드를 직접 바꿔 실행하는 연습이다. 처음에는 예제를 그대로 옮기고,
실행에 성공하면 학번과 이름을 본인 것으로 바꾼다.
1일차는 브라우저의 Kotlin Playground에서, 2일차는 Android Studio에서 실행한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 글자 두 줄 출력하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | Playground를 열고 첫 예제를 실행한다 |
| 10–25분 | 이름을 본인 이름으로 바꾸고 다시 실행한다 |
| 25–40분 | 학번과 이름을 각각 한 줄에 출력한다 |
| 40–50분 | 친구 또는 강의자에게 바꾼 부분과 결과를 보여 준다 |
| 50–60분 | 오타를 확인하고 코드를 `Hello.kt`로 저장한다 |

### 1. 먼저 실행해 보기

[Kotlin Playground](https://play.kotlinlang.org/)를 열고 편집 영역의 코드를 아래 코드로 바꾼다.
그다음 `Run ▶` 버튼을 누른다.

```kotlin
fun main() {
    println("안녕하세요")
}
```

결과에 `안녕하세요`가 보이면 첫 실행 성공이다.

### 2. 내 정보로 바꾸기

[1일차 예제](examples/Hello.kt)를 참고해 아래 결과를 만든다. 학번과 이름은 본인 것으로 바꾼다.

```text
학번: 20260001
이름: 홍길동
```

- 글자는 큰따옴표 `" "` 안에 쓴다.
- 한 줄을 출력할 때마다 `println()`을 하나씩 쓴다.
- `fun main() {`와 마지막 `}`는 그대로 두고 그 사이를 수정한다.

### 3. 오늘 확인할 것

- [ ] 내 학번과 이름이 두 줄로 보인다.
- [ ] 글자를 고친 뒤 `Run ▶`을 다시 눌러 결과를 확인했다.
- [ ] 코드를 `Hello.kt`로 저장했다. 일반 텍스트 편집기에 복사해서 저장해도 된다.

1일차 코드는 다음 시간 복습용으로 보관한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 변수와 if, fun으로 자기소개 완성하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–15분 | `StudentCard` 프로젝트를 만들고 `StudentCard.kt`에서 `main()`을 실행한다 |
| 15–25분 | `val`에 학번과 이름을 담고 `$변수이름`으로 두 줄을 출력한다 |
| 25–35분 | `var` 값 바꾸기와 문자열·숫자 예제를 따라 해 본다 |
| 35–45분 | [Intro.kt](examples/Intro.kt)의 코드를 넣고 실행해 `if/else`와 `fun`을 연습한다 |
| 45–55분 | 내 코드에 `if` 한 줄과 `fun` 하나를 넣어 세 줄을 출력한다 |
| 55–60분 | 최종 코드와 Run 창 캡처를 정리해 제출한다 |

오늘 만드는 `StudentCard` 프로젝트는 2주차에 그대로 다시 연다. 실습이 끝나도 지우지 않는다.
개인 노트북에 Android Studio를 설치할 학생은 45–60분 사이에 조교에게 설치 상태를 확인받는다.
실습실 PC를 쓰는 학생은 해당 없다.

### 1. 프로젝트를 만들고 main() 실행하기

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
[따라하기 5~7단계](walkthrough.md#5-새-프로젝트-만들기)에 있다.

1. **Project** 창에서 `app` → `kotlin+java` → `com.example.studentcard`를 고르고
   **File › New › Kotlin Class/File**로 이름 `StudentCard`, 종류 **File**을 만든다.
2. 만들어진 `StudentCard.kt`에 아래 코드를 쓰고, `fun main()` 줄 **왼쪽 여백의 ▶**을 눌러
   **Run 'StudentCardKt'**를 고른다.

```kotlin
fun main() {
    println("안녕하세요")
}
```

아래쪽 **Run** 창에 `안녕하세요`가 나오면 오늘의 첫 실행 성공이다.
위쪽 도구 막대의 `Run ▶`은 앱을 실행하는 버튼이라 에뮬레이터가 뜨고 `println` 결과는 Run 창에 보이지 않는다.
오늘은 항상 왼쪽 여백의 ▶을 쓴다. 처음 실행할 때는 빌드에 시간이 걸린다.

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
막히면 [기초 문법 예제](examples/README.md)나 [따라하기](walkthrough.md#8-학번과-이름을-변수에-담기)를 펼쳐도 된다.

### 4. 짧은 문법 연습

[기초 문법 예제](examples/README.md)의 `var`와 문자열·숫자 예제를 **하나씩 따로** 실행한다.
`fun main() {`와 마지막 `}`는 그대로 두고 중괄호 안의 내용만 바꾼다.

- `var`에 담긴 인사말을 바꾸고 바꾸기 전후의 출력을 본다.
- `println(1 + 2)`와 `println("1 + 2")`의 결과를 비교한다.

예제를 두 개 붙여 `fun main()`이 두 개가 되면 `Conflicting overloads:` 오류가 난다. 한 번에 하나만 넣는다.
이 연습은 별도 보고서 없이 Run 창에서 확인한다. 시간이 부족하면 5번부터 한다.
확인이 끝나면 3번에서 만든 코드로 되돌린다.

### 5. if/else와 fun 연습하기

`package` 줄 아래를 모두 지우고 [Intro.kt](examples/Intro.kt)의 코드를 넣어 실행한다.
Run 창에 아래 세 줄이 나와야 한다.

```text
결과: 합격
이름: 홍길동
이름: 김철수
```

- `val score = 85`를 `50`으로 바꾸고 실행하면 첫 줄이 어떻게 되는지 본다. 본 뒤 `85`로 되돌린다.
- `intro("김철수")` 아래에 `intro(...)`를 한 줄 더 넣어 이름을 하나 더 출력해 본다.

### 6. 내 코드에 if 한 줄과 fun 하나 넣기

3번에서 만든 코드(학번·이름 두 줄)로 되돌린 뒤 아래 세 가지를 추가한다. 결과는 세 줄이다.

```text
학번: 20260001
이름: 홍길동
결과: 합격
```

- `fun main() {` **위**에 `fun intro(name: String) { ... }`를 정의한다. 5번의 `Intro.kt`에 있는 그대로다.
- `println("이름: $name")` 줄을 `intro(name)`으로 바꾼다. 괄호 안에는 큰따옴표 없이 변수 이름을 쓴다.
- `val score = 85`를 추가하고, `if (score >= 60) "합격" else "불합격"`으로 `result`를 만들어 `println("결과: $result")`로 출력한다.

힌트: `if` 줄과 `println("결과: ...")` 줄은 `Intro.kt`의 `main` 안에 있는 두 줄과 같다.
막히면 [따라하기 12단계](walkthrough.md#12-내-코드에-if-한-줄과-fun-하나-넣기)의 완성 코드와 한 줄씩 비교한다.

## 막혔을 때

오류가 보이는 곳이 도구마다 다르다. 1일차 Playground는 출력 영역에 `2:20: error: ...`처럼
**줄:칸** 번호로 시작하는 오류가 나오고, 2일차 Android Studio는 편집기의 틀린 곳에 빨간 줄이 그어지고
실행하면 **Build** 창에 같은 문장이 나온다. Build 창에서는 문장 앞에 `e: file:///…/StudentCard.kt:5:5`처럼
파일과 줄:칸이 붙는다. 두 도구가 모두 Kotlin 컴파일러를 쓰므로 문장은 거의 같지만,
버전에 따라 첫 글자의 대소문자와 자료형 표기(`Int` / `kotlin.Int`)가 다를 수 있다.
아래 문구는 실제로 실행해 확인한 것이다.

| 상황·오류 문구 | 확인할 것 |
|---|---|
| `Expecting '"'.` | 닫는 큰따옴표가 빠졌다. `println("안녕하세요")`처럼 `"` 두 개가 짝을 이루는지 본다 |
| `Expecting ')'.` | 닫는 소괄호가 빠졌다. `println(` 뒤에 `)`가 있는지 본다 |
| `Expecting '}'.` | 마지막 `}`가 빠졌다. `fun main() {`의 짝인 `}`를 마지막 줄에 넣는다 |
| `unresolved reference '학번'.` | 큰따옴표 없이 글자를 적었다. `println("학번: 20260001")`처럼 감싼다 |
| `Unresolved reference 'nmae'.` | 변수 이름 철자가 다르다. 만들 때와 쓸 때를 대조한다. `studentId`의 대문자 `I`도 같아야 한다 |
| `unresolved reference 'Intro'.` | 함수 이름 철자가 다르다. 정의한 `intro`와 호출하는 `intro`가 같아야 한다 |
| `'val' cannot be reassigned.` | `val`로 만든 변수에 다시 값을 넣었다. 다시 넣어야 하면 `var`로 바꾼다 |
| `'if' must have both main and 'else' branches when used as an expression.` | `else "불합격"`이 빠졌다. `if (조건) 값1 else 값2` 두 갈래를 모두 적는다. `else`가 이미 있으면 `if (score >= 60)`처럼 조건에 소괄호가 있는지 본다. 괄호가 없을 때도 이 문구가 먼저 나온다 |
| `Expecting a condition in parentheses '(...)'.` | `if score >= 60`처럼 괄호가 없다. `if (score >= 60)`으로 감싼다 |
| `no value passed for parameter 'name'.` | `intro()`처럼 괄호가 비었다. `intro(name)` 또는 `intro("홍길동")`으로 값을 넣는다 |
| `Argument type mismatch: actual type is 'kotlin.Int', but 'kotlin.String' was expected.` | `val score = "85"`처럼 비교할 점수를 글자로 만들었다. `val score = 85`로 둔다. `intro(20260001)`처럼 함수에 숫자를 넣어도 자료형이 맞지 않는다는 같은 종류의 오류가 난다 |
| `Expecting a top level declaration.` | 함수 정의에서 `fun`이 빠졌다. `fun intro(name: String) {`로 시작한다 |
| `Conflicting overloads:` | 한 파일에 `fun main()`이 두 개다. 아래 두 줄이 그 두 위치를 가리킨다. 예제를 넣을 때 앞의 코드를 지운다 |
| `name`이라는 글자가 그대로 나온다 | 오류는 아니다. `"$name"`처럼 `$`를 붙였는지 본다 |
| 이름을 고쳤는데 결과가 같다 | 1일차는 `Run ▶`, 2일차는 왼쪽 여백의 ▶을 다시 누른다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 현재 코드를 그대로 보여 주고 도움을 받는다.

## 제출 — 두 가지만

1. **`StudentCard.kt`**: 프로젝트의 `app` → `kotlin+java` → `com.example.studentcard` 안에 있는 최종 코드.
   본인 학번과 이름을 `val`에 담고, `intro` 함수와 `if/else` 한 줄로 세 줄을 출력한다
2. **Run 창 캡처 1장**: 학번·이름·결과 세 줄이 보이는 **Run** 창 화면

`println()`으로 학번과 이름이 나오면 기본 출력 성공이다. `if`와 `fun`은 예제와 도움을 받아 마무리해도 된다.
`StudentCard` 프로젝트는 2주차에 다시 여니 제출한 뒤에도 지우지 않는다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 인사말을 `var greeting = "안녕하세요"`에 담아 첫 줄에 출력하고, `main` 끝에서 `greeting = "다음 주에 만나요"`로 바꿔 한 번 더 출력해 본다.
- 자기소개 아래에 `좋아하는 것: 음악`처럼 한 줄을 더 출력해 본다.
- `intro`처럼 `fun showId(studentId: String)` 함수를 만들어 학번 줄도 함수로 출력해 본다.

추가 과제는 선택 사항이다.
