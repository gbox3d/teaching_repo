# 8주차 따라하기 — 문제 은행 연습과 시험 날

1일차는 은행 문제 하나를 읽고 풀어 확인하는 순서, 2일차는 시험 날 순서다. 문제 문장은 [문제 은행](examples/README.md)에 있고, 시간 배분은 [실습지](lab.md)에 있다.
이번 주에는 받을 예제 코드가 없다. 수업에서 쓴 `StudentCard` 프로젝트에서 직접 쓴다.

## 1일차

### 1. 프로젝트 열고 실행하기

1. Android Studio 를 열고 **Open** 으로 `StudentCard` 프로젝트를 연다. 없으면 **New Project › Empty Views Activity**, Name `StudentCard`([1주차 따라하기](../week01_android_kotlin/walkthrough.md#1-새-프로젝트-만들기)).
2. 아래쪽 진행 표시(Sync)가 끝나면 에뮬레이터를 고르고 Run ▶ 을 누른다. 화면이 뜨면 시작할 수 있다.
3. 아래쪽 **Logcat** 탭을 한 번 열어 둔다.

### 2. 문제 하나 읽는 법: a03_name_button

[a03_name_button](examples/a03_name_button/README.md) 을 연다. 모든 문제가 같은 순서다.

```text
첫 줄         무엇을 다시 만드는지 한 문장 (2주차 2일차의 글자 바꾸기와 버튼)
할 일         XML 에서 할 것(View·id·글자)과 Kotlin 에서 할 것(findViewById·리스너·변수). 적힌 순서대로
확인할 것      화면·Logcat 으로 스스로 맞춰 보는 목록. 해답 대신이다
힌트          막혔을 때 읽는다. 시험의 설명 물음이 이 내용이다
이 문제의 값    시험에서 바뀌는 값. a03 은 nameText · 홍길동 · countText · 0 · plusButton · +1 · 3 …
설명 물음      시험에서 1~2문장으로 답할 것
```

값(id·글자·숫자)은 문제 문장에서 **복사해 붙인다.** `id` 한 글자가 다르면 `Unresolved reference` 가 난다.

### 3. XML 쓰기

1. `app › res › layout › activity_main.xml` 을 열고 오른쪽 위 **Code** 를 눌러 글자로 본다.
2. 할 일의 XML 부분을 쓴다. a03 은 이름 TextView 에 `android:id="@+id/nameText"`, 숫자 TextView(`countText`, `0`, `40sp`), Button(`plusButton`, `+1`).
3. 저장한다. 오른쪽 위 **Split** 으로 미리보기를 보면 배치가 맞는지 바로 보인다(실행 화면은 아니다).

### 4. Kotlin 쓰기

1. `app › kotlin+java › com.example.studentcard › MainActivity.kt` 를 연다.
2. `onCreate` 안, `setContentView(R.layout.activity_main)` 과 insets 블록 **아래**에 할 일의 Kotlin 부분을 쓴다. a03 은 `findViewById` 두 줄, `var count = 0`, 리스너 하나.
3. 빨간 글자가 있으면 커서를 두고 Alt+Enter(맥 ⌥+Enter)로 import 한다. `R.id.` 뒤가 빨갛면 XML 의 id 철자를 본다.

### 5. 실행하고 확인할 것 맞추기

1. 저장(Ctrl+S, 맥 ⌘+S) → Run ▶. 빌드 오류가 나면 **Build** 창의 첫 빨간 줄을 읽고 [막혔을 때](lab.md#막혔을-때)를 본다.
2. "확인할 것"을 위에서부터 하나씩 한다. a03 은 처음 글자 `이름: 홍길동`·숫자 `0`, `+1` 세 번 → `3`, 다섯 번 → `5`.
3. 맞지 않는 항목이 있으면 그 항목이 가리키는 할 일로 돌아간다. 막히면 힌트를 읽는다.
4. 요구한 상태를 캡처한다. 에뮬레이터 창 옆 도구 막대의 카메라 버튼, 또는 운영체제 캡처.

같은 순서로 a04 → a05 … 를 푼다. 문제마다 10분을 넘기면 남은 항목을 적어 두고 다음 문제로 간다.

### 6. 회전과 Logcat 필터 (a05)

1. 에뮬레이터 창 옆 도구 막대의 회전 버튼을 누르면 가로 화면이 된다. 숫자가 남는지 본다.
2. **Logcat** 탭의 필터 칸에 `Life` 를 친다. `Log.d("Life", …)` 로 남긴 줄만 보인다. 회전할 때 `onDestroy` 다음 `onCreate` 가 찍히는지 본다.
3. 가로 화면과 Logcat 을 각각 캡처한다.

## 2일차

### 7. 시험 전 점검

- 분반 공지를 다시 읽는다. 시작·끝 시각, 문제 수, 볼 수 있는 것, AI 도구 허용 여부, 내는 곳.
- 1교시에 Android Studio 로 `StudentCard` 를 열고 에뮬레이터를 켜 Run ▶ 까지 해 둔다. 안 되는 PC 는 시험 전에 손을 든다.
- 캡처 방법과 LMS 답안 칸(코드 붙이기·이미지 넣기)이 열리는지 본다.

### 8. 문제 읽기와 값 표시

시험이 시작되면 문제를 끝까지 읽는다. 문제마다 "이 문제의 값"이 은행 문제와 어디가 다른지 표시한다(id·글자·숫자·키 이름). 아직 코드를 쓰지 않는다. 3분 안에 끝낸다.

### 9. 풀기와 캡처

1. XML → Kotlin → 저장·실행 순서로 1일차와 같이 한다.
2. "확인할 것"을 하나씩 맞추고, 맞춘 상태를 캡처한다. 회전·Logcat 을 요구하면 그 화면까지.
3. 오래 막히면 다음 문제로 간다. 빌드가 안 되는 줄은 앞에 `//` 를 붙여 실행되는 상태를 만들고, 원래 쓰려던 코드는 답안에 적는다.

### 10. 설명 쓰기

문제의 설명 물음에 자기 말로 1~2문장을 쓴다. 힌트에 있는 내용 수준이면 된다. 예: "회전하면 Activity 가 없어지고 새로 만들어져서 `onCreate` 안의 `count = 0` 이 다시 실행된다."

### 11. 제출

- Android Studio 에서 `activity_main.xml` 과 `MainActivity.kt` 를 각각 전체 선택(Ctrl+A) → 복사 → LMS 답안 칸에 붙인다.
- 캡처를 답안 칸에 넣는다(이미지 붙이기 또는 첨부). 설명을 그 아래에 쓴다.
- 끝나기 5분 전에 문제마다 코드·캡처·설명이 있는지 본다. 제출 버튼을 누른 뒤 제출됐다는 화면을 확인한다.

## 오류가 나면

| 증상 | 확인할 것 |
|---|---|
| `Unresolved reference 'nameText'.` | XML 의 `@+id/` 뒤 이름과 글자까지 같은지 본다 |
| 빨간 글자 `TextView`·`Button`·`Log`·`Toast` | Alt+Enter(맥 ⌥+Enter) → Import |
| `Unresolved reference 'name님'.` | `"${name}님"` 처럼 중괄호를 쓴다 |
| 회전하면 `0` 으로 돌아간다 | `putInt`·`getInt` 의 키가 같은지, `count` 가 class 바로 안에 있는지 본다 |
| 앱이 켜지자마자 꺼진다 | Logcat 의 빨간 줄에서 `NullPointerException` 과 줄 번호를 읽는다. `findViewById` 의 id 를 본다 |

더 많은 증상은 [실습지 막혔을 때](lab.md#막혔을-때)에 있다.
