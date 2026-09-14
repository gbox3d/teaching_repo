# 2주차 예제 — LinearLayout과 findViewById

Android Studio에서 **Empty Views Activity**로 만든 `StudentCard` 프로젝트를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.
학번 `20260001`, 이름 `홍길동`, 전공 `컴퓨터공학과`는 연습용 값이다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 |
|---|---|
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.studentcard › MainActivity.kt` — 템플릿이 만든 그대로이며 1일차에는 고치지 않는다 |
| [day2/activity_main.xml](day2/activity_main.xml) | `app › res › layout › activity_main.xml` |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `app › kotlin+java › com.example.studentcard › MainActivity.kt` |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.

## 1. LinearLayout — 차례로 쌓기

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <!-- 이 안에 넣은 순서대로 위에서 아래로 놓인다 -->

</LinearLayout>
```

| 속성 | 뜻 |
|---|---|
| `android:orientation="vertical"` | 위에서 아래로 쌓는다. `horizontal`이면 왼쪽에서 오른쪽으로 쌓는다 |
| `android:gravity="center"` | 안의 내용을 가운데로 모은다 |
| `match_parent` | 부모만큼 크게. 가장 바깥 레이아웃에서는 화면 전체다 |
| `android:id="@+id/main"` | 템플릿의 `MainActivity.kt`가 사용하는 이름이다. 지우지 않는다 |

## 2. TextView — 글자 한 줄

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_marginTop="8dp"
    android:text="학번: 20260001"
    android:textSize="20sp" />
```

- `wrap_content`: 글자에 딱 맞는 크기다.
- `android:text`: 화면에 보일 글자다.
- `android:textSize`: 글자 크기다. 글자에는 `sp`를 쓴다.
- `android:layout_marginTop`: 위쪽 간격이다. 간격에는 `dp`를 쓴다.
- 마지막은 `/>`로 닫는다. 따옴표 `" "` 짝이 맞는지 확인한다.

## 3. 1일차 완성 — 내 정보 화면

[day1/activity_main.xml](day1/activity_main.xml)을 넣고 실행하면 화면 가운데에 네 줄이 보인다.

```text
내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과
```

## 4. `android:id`와 `findViewById`

```xml
<TextView
    android:id="@+id/nameText"
    android:text="이름: ?"
    ... />
```

```kotlin
val name = "홍길동"
val nameText = findViewById<TextView>(R.id.nameText)
nameText.text = "이름: $name"
```

- XML의 `@+id/nameText`가 이름표이고, Kotlin에서는 `R.id.nameText`로 같은 View를 부른다.
- `findViewById<TextView>`는 그 id를 가진 TextView를 찾아 준다.
- `.text`에 글자를 넣으면 화면의 글자가 바뀐다. XML에 적은 `이름: ?`는 코드가 바꾸기 전의 처음 글자다.

## 5. `setOnClickListener` — 누를 때마다 실행

```kotlin
var count = 0
val countText = findViewById<TextView>(R.id.countText)
val plusButton = findViewById<Button>(R.id.plusButton)

plusButton.setOnClickListener {
    count = count + 1
    countText.text = "$count"
}
```

- 중괄호 `{ }` 안의 코드는 앱이 켜질 때가 아니라 **버튼을 누를 때마다** 실행된다.
- `count`는 바뀌는 값이므로 `var`다. `count = count + 1`은 `count++`로 줄여 쓸 수도 있다.
- 화면에는 글자를 넣는다. 숫자 `count`를 그대로 넣는 코드는 [실습지의 막혔을 때](../lab.md#막혔을-때)를 본다.

## 6. 2일차 완성 — 버튼 카운터

[day2/activity_main.xml](day2/activity_main.xml)과 [day2/MainActivity.kt](day2/MainActivity.kt)를 넣고 실행한 결과:

```text
내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과

3
[-1] [초기화] [+1]
```

| 누른 순서 | 화면 숫자 |
|---|---|
| 처음 실행 | `0` |
| `+1` 세 번 | `3` |
| 이어서 `-1` 한 번 | `2` |
| 이어서 `초기화` | `0` |

화면을 돌리면 숫자가 `0`으로 돌아간다. 이번 주에는 관찰만 하고, 3주차에 이유와 해결 방법을 배운다.

## 공식 참고 자료

- [LinearLayout — Android Developers](https://developer.android.com/develop/ui/views/layout/linear)
- [버튼 — Android Developers](https://developer.android.com/develop/ui/views/components/button)
