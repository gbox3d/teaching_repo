# 1주차 — Kotlin 첫걸음: 학번과 이름 출력하기

## 이번 주 질문

> 코드를 조금 바꿔서 내 학번과 이름을 출력할 수 있을까?

프로그래밍을 처음 배우는 학생을 기준으로 시작한다. 짧은 코드를 실행하고,
글자를 바꾸고, 다시 실행하는 경험이 이번 주의 중심이다. 두 날 모두 실습실 PC의
**Android Studio**에서 진행하고, 결과는 아래쪽 **Run** 창에서 본다. 1일차 첫 5분에는 이 과목이
15주 동안 무엇을 만드는지 훑어본다.

## 학습 목표

1. Android Studio에서 `StudentCard` 프로젝트를 만들고 `StudentCard.kt` 파일을 만든다.
2. 제공된 `fun main() { }` 틀 안에 코드를 쓰고, 왼쪽 여백의 ▶으로 실행한다.
3. `println()`으로 학번과 이름을 두 줄에 출력한다.
4. `val`에 학번과 이름을 담고 `$변수이름`으로 출력한다.
5. 예제 파일을 하나씩 만들어 `val`과 `var`, 문자열과 숫자의 차이를 확인한다.
6. `if (score >= 60) "합격" else "불합격"`으로 조건에 따라 다른 글자를 고른다.
7. `fun intro(name: String) { }`처럼 함수를 하나 정의하고 호출한다.

## 이번 주 결과물

```text
학번: 20260001
이름: 홍길동
결과: 합격
```

예제의 학번과 이름을 본인 정보로 바꾸면 된다.
마지막에는 프로젝트 안의 코드 `StudentCard.kt`와 위 세 줄이 보이는 **Run 창 캡처**를 제출한다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 과목 소개(15주 흐름·만들 앱·평가), `StudentCard` 프로젝트 만들기, `StudentCard.kt` 만들고 왼쪽 여백의 ▶으로 실행, `main`, `println`, 큰따옴표 | 프로젝트를 만들고 첫 출력 → 학번·이름 두 줄 → 내 정보로 바꾸기 → 오류를 일부러 만들어 Build 창 문구 읽어 보기 | Run 창에 학번·이름 두 줄 |
| 2일차 | `val`, 문자열·숫자, `$변수이름`, `var`, `if/else`, `fun` | 지난 코드 다시 실행 → 학번·이름을 변수에 담기 → 예제 파일 네 개를 만들어 실행 → 내 코드에 `if` 한 줄과 `fun` 하나 추가 → 제출 | Run 창에 자기소개 세 줄 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은
인사말을 `var`로 바꿔 보고, 시간이 필요한 학생은 기본 두 줄을 반복해서 연습한다.
1일차에 만드는 `StudentCard` 프로젝트는 2일차에 이어 쓰고, 2주차에도 그대로 다시 연다.
**1일차에는 제출물이 없다.** 제출은 2일차 마지막에 한 번만 한다.

## 준비

- **실습실 PC의 Android Studio.** 실습실 PC에는 이미 설치되어 있다. 학생이 따로 설치하지 않는다
- 두 날 모두 본인의 학번과 이름
- 에뮬레이터와 실물 폰은 이번 주에 쓰지 않는다

첫 프로젝트를 만들 때는 창 아래쪽 진행 표시가 끝날 때까지 몇 분 걸린다. 끝날 때까지 기다린다.
첫 실행도 빌드에 시간이 걸린다. 진행 표시가 끝나기 전에는 코드에 빨간 줄이 남아 있을 수 있다.
개인 노트북에 Android Studio를 설치하려는 학생은 2일차 실습 마지막 15분에 조교가 현장에서 확인한다.
설치 방법은 [설치 안내](../../ta_setup_guide.md)를 따른다. 실습실 PC를 쓰는 학생은 설치가 필요 없다.

## 기초 문법 범위

| 문법 | 이번 주에 알아둘 뜻 |
|---|---|
| `fun main() { }` | 프로그램을 시작하는 틀. 코드는 중괄호 안에 쓴다 |
| `println("안녕하세요")` | 큰따옴표 안의 글자를 출력하고 줄을 바꾼다 |
| `val name = "홍길동"` | 값에 이름을 붙인다. 실행 중 같은 변수에 다른 값을 다시 넣을 수 없다 |
| `var greeting = "안녕하세요"` | 실행 중 값을 다시 넣을 수 있는 변수다 |
| `"20260001"` / `85` | 큰따옴표가 있으면 문자열(`String`), 예제의 정수 `85`는 숫자(`Int`)다 |
| `println("이름: $name")` | 문자열 안에 변수의 값을 넣어 출력한다 |
| `if (score >= 60) "합격" else "불합격"` | 조건이 맞으면 앞의 값, 아니면 `else` 뒤의 값이 된다 |
| `fun intro(name: String) { }` / `intro("홍길동")` | 함수를 정의한다 / 함수를 호출한다. 괄호 안의 값이 `name`으로 들어간다 |
| `// 메모` | 같은 줄에서 `//` 뒤는 실행하지 않는 설명이다 |

숫자 덧셈은 짧게 맛보기로 확인한다. 반복문(`for`)과 목록(`listOf`)은 이번 주에 다루지 않고 필요한 주에 배운다.

## 수업 자료

- [슬라이드](slides.md) · [English slides](slides_en.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [기초 문법 예제](examples/README.md)
- 1일차 완성 예시(참고용): [Hello.kt](examples/Hello.kt)
- 2일차 문법 예제: [Vars.kt](examples/Vars.kt) · [Types.kt](examples/Types.kt) · [Branch.kt](examples/Branch.kt) · [Functions.kt](examples/Functions.kt) · [Intro.kt](examples/Intro.kt)
- 2일차 완성 코드: [StudentCard.kt](examples/StudentCard.kt)

## 완료 기준

- [ ] Android Studio에서 `StudentCard` 프로젝트를 만들고 `StudentCard.kt`의 `main()`을 실행했다.
- [ ] 본인의 학번과 이름이 Run 창에 각각 한 줄씩 출력된다.
- [ ] 학번과 이름을 `val`에 담아 출력할 수 있다.
- [ ] `if/else` 한 줄로 `결과: 합격` 또는 `결과: 불합격`이 출력된다.
- [ ] `fun intro(name: String)`을 정의하고 `main`에서 호출한다.
- [ ] 코드에서 이름을 바꾸면 어느 출력이 달라지는지 가리킬 수 있다.
- [ ] Build 창의 오류 문구를 한 번 읽고 그 자리를 고쳐 봤다.
- [ ] 최종 코드 `StudentCard.kt`와 세 줄이 보이는 **Run 창 캡처** 1장을 제출한다.

## 다음 수업 연결

다음 주는 [2주차 — 첫 Android 앱: 내 정보 화면과 카운터](../week02_views_layout/README.md)다.
이번 주에는 Android Studio의 Run 창에 글자를 출력했다.
**2주차는 이번 주에 만든 `StudentCard` 프로젝트를 그대로 연다.** 새로 만들지 않는다.
같은 학번과 이름을 Run 창이 아니라 폰 화면에 띄우고, 버튼을 누르면 숫자가 바뀌는 카운터를 만든다.
`println("이름: $name")`이 `nameText.text = "이름: $name"`으로 바뀌는 것이 다음 주의 핵심이다.
이번 주에 배운 `var`는 카운터에서, `if`와 `fun`은 이후 주차의 버튼 코드에서 다시 쓴다.

## 공식 참고 자료

- [Android Studio 소개](https://developer.android.com/studio/intro)
- [Kotlin 기초 문법](https://kotlinlang.org/docs/basic-syntax.html)
- [Kotlin if 표현식](https://kotlinlang.org/docs/control-flow.html#if-expression)
- [Kotlin 함수](https://kotlinlang.org/docs/functions.html)
