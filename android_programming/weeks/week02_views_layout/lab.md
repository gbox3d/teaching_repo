# 2주차 실습 — 내 정보 화면과 카운터 만들기

이번 주에는 처음으로 Android Studio에서 앱을 만든다. 처음에는 예제를 그대로 옮기고,
실행에 성공하면 학번·이름·전공을 본인 것으로 바꾼다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — LinearLayout으로 내 정보 화면 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–15분 | 새 프로젝트 `StudentCard`를 만들고 `Hello World!`를 실행한다 |
| 15–30분 | `activity_main.xml`을 LinearLayout으로 바꾸고 제목 `내 정보`를 띄운다 |
| 30–45분 | 학번·이름·전공 TextView 세 개를 추가한다 |
| 45–55분 | 속성을 하나씩 바꿔 보고 결과를 적는다 |
| 55–60분 | 실행 화면을 캡처하고 프로젝트를 저장한다 |

### 1. 새 프로젝트 만들고 실행하기

Android Studio에서 **New Project → Empty Views Activity**를 고른다.

| 항목 | 입력 |
|---|---|
| Name | `StudentCard` |
| Package name | `com.example.studentcard` (자동으로 채워진 값) |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |

**Finish**를 누르고 아래쪽 진행 표시가 끝날 때까지 기다린 뒤 `Run ▶`을 누른다.
에뮬레이터에 `Hello World!`가 보이면 성공이다.

### 2. 화면을 LinearLayout으로 바꾸기

`app › res › layout › activity_main.xml`을 열고 오른쪽 위 **Code**를 누른다.
내용을 모두 지우고 [따라하기 4단계](walkthrough.md#4-linearlayout으로-바꾸기)의 코드를 넣어 실행한다.

- 가장 바깥 `LinearLayout`에 `android:orientation="vertical"`과 `android:gravity="center"`가 있다.
- `android:id="@+id/main"`은 지우지 않는다. `MainActivity.kt`가 이 이름을 사용한다.
- 화면 가운데에 `내 정보`가 보이면 다음 단계로 간다.

### 3. 학번·이름·전공 추가하기

아래 결과가 되도록 `내 정보` 아래에 TextView 세 개를 추가한다. 값은 본인 정보로 쓴다.

```text
내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과
```

- 학번 TextView를 먼저 만들고, 복사해서 두 개 더 붙인 뒤 `android:text`만 바꾼다.
- 글자 크기는 `android:textSize="20sp"`, 위 간격은 `android:layout_marginTop="8dp"`로 시작한다.
- 막히면 [1일차 완성 XML](examples/day1/activity_main.xml)을 열어 내 코드와 한 줄씩 비교한다.

### 4. 하나씩 바꿔 보기

한 번에 **한 곳만** 바꾸고 실행한다. 결과를 적은 뒤 원래대로 되돌린다.

| 바꾼 곳 | 예상 | 실제 |
|---|---|---|
| 바깥 LinearLayout의 `orientation`을 `horizontal`로 |  |  |
| 바깥 LinearLayout의 `android:gravity="center"` 줄 삭제 |  |  |
| 학번의 `textSize`를 `40sp`로 |  |  |
| 이름의 `layout_marginTop`을 `48dp`로 |  |  |

### 5. 오늘 확인할 것

- [ ] `Empty Views Activity`로 만든 `StudentCard` 프로젝트가 실행된다.
- [ ] 화면에 본인의 학번·이름·전공이 세 줄로 보인다.
- [ ] 속성을 바꿔 본 결과를 표에 적었다.
- [ ] 실행 화면을 캡처했다.

프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 버튼으로 숫자 세기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 `StudentCard`를 열어 다시 실행한다 |
| 10–25분 | 이름 TextView에 id를 붙이고 코드에서 글자를 바꾼다 |
| 25–40분 | 숫자와 버튼을 배치하고 `+1` 버튼을 동작시킨다 |
| 40–50분 | `-1`과 `초기화` 버튼을 직접 완성한다 |
| 50–55분 | 숫자를 `3`으로 만들고 화면을 돌려 본다 |
| 55–60분 | 최종 파일과 실행 화면을 정리해 제출한다 |

### 1. 코드로 이름 바꾸기

1. `activity_main.xml`의 이름 TextView에 `android:id="@+id/nameText"`를 추가하고, 글자는 `이름: ?`로 바꾼다.
2. 실행해서 `이름: ?`가 보이는지 확인한다.
3. `MainActivity.kt`에서 `onCreate()` 마지막 `}` 바로 위에 아래 코드를 넣는다.

```kotlin
val name = "홍길동"
val nameText = findViewById<TextView>(R.id.nameText)
nameText.text = "이름: $name"
```

`홍길동`을 본인 이름으로 바꾸고 실행한다. `이름: ?`가 본인 이름으로 바뀌면 성공이다.
`TextView`가 빨간색이면 커서를 올리고 **Alt+Enter**(맥은 ⌥+Enter)를 눌러 import한다.

### 2. `+1` 버튼 만들기

[따라하기 9단계](walkthrough.md#9-숫자와-버튼-배치하기)의 XML로 숫자 TextView(`countText`)와 버튼 세 개를 배치한다.
그다음 아래 코드를 1번 코드 아래에 넣는다.

```kotlin
var count = 0
val countText = findViewById<TextView>(R.id.countText)
val plusButton = findViewById<Button>(R.id.plusButton)

plusButton.setOnClickListener {
    count = count + 1
    countText.text = "$count"
}
```

`+1`을 세 번 눌러 숫자가 `3`이 되는지 확인한다.

### 3. `-1`과 `초기화` 버튼 직접 완성하기

`+1` 코드를 보고 두 버튼을 직접 완성한다.

- `-1`: 누를 때마다 숫자가 1씩 줄어든다. 버튼 id는 `minusButton`이다.
- `초기화`: 누르면 숫자가 `0`이 된다. 버튼 id는 `resetButton`이다.
- `+1` 코드와 비교해 **바뀌는 곳**은 버튼 이름과 `count`를 계산하는 줄뿐이다.

| 누른 순서 | 예상 숫자 | 실제 숫자 |
|---|---|---|
| `+1` 세 번 |  |  |
| 이어서 `-1` 한 번 |  |  |
| 이어서 `초기화` |  |  |
| 이어서 `-1` 한 번 |  |  |

### 4. 화면 돌려 보기

숫자를 `3`으로 만든 뒤 에뮬레이터 화면을 돌린다. 숫자와 이름이 어떻게 되는지 한 문장으로 적는다.
이번 주에는 **관찰만** 하고 고치지 않는다. 이유는 3주차에 배운다.

## 막혔을 때

| 상황 | 확인할 것 |
|---|---|
| 프로젝트에 `activity_main.xml`이 없다 | `Empty Activity`로 만들었는지 본다. `Empty Views Activity`로 새로 만든다 |
| `Unresolved reference 'id'` 또는 `Unresolved reference 'main'` 오류 | 가장 바깥 `LinearLayout`에 `android:id="@+id/main"`이 있는지 본다 |
| `Unresolved reference 'nameText'` 오류 | XML의 `@+id/nameText`와 코드의 `R.id.nameText` 철자가 같은지 본다 |
| `TextView`, `Button`이 빨간색이다 | **Alt+Enter**(맥 ⌥+Enter)로 import한다 |
| `Assignment type mismatch` 오류 | `countText.text = count`처럼 숫자를 그대로 넣었는지 본다. `"$count"`로 쓴다 |
| 버튼을 누르면 앱이 꺼진다 | `countText.setText(count)`를 썼는지 본다. `countText.text = "$count"`로 쓴다 |
| 버튼을 눌러도 숫자가 그대로다 | 중괄호 `{ }` 안에서 `countText.text`를 바꾸는지 본다 |
| 노란색 경고 표시가 있다 | 실행에는 문제가 없다. 빨간 오류부터 해결한다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 세 가지

1. **`activity_main.xml`**: 본인 학번·이름·전공과 숫자·버튼이 있는 최종 XML
2. **`MainActivity.kt`**: 이름 바꾸기와 버튼 세 개가 동작하는 최종 코드
3. **실행 화면 1장**: 학번·이름·전공과 숫자 `3`이 보이는 캡처

`+1` 버튼까지 동작하면 기본 성공이다. `-1`과 `초기화`는 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: `좋아하는 것` 한 줄을 더 추가하거나 제목에 `android:textColor="#1E88E5"`를 넣어 색을 바꿔 본다.
- 2일차: 숫자가 `0` 아래로 내려가지 않게 `-1` 버튼 안에 `if (count > 0)`을 넣어 본다.
- 2일차: 세 버튼에 똑같이 있는 `countText.text = "$count"` 줄을 함수 하나로 묶어 본다.

추가 과제는 선택 사항이다.
