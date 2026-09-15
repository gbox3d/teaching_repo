---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 2주차
footer: 첫 Android 앱 · LinearLayout과 findViewById
---

# 첫 Android 앱: 내 정보 화면과 카운터

1주차에는 학번과 이름을 **콘솔**에 출력했습니다.
이번 주에는 **앱 화면**에 띄우고, 버튼으로 숫자를 바꿉니다.

```text
내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과

3
[-1] [초기화] [+1]
```

---

# 1일차 — 앱 화면에 내 정보 띄우기

`30분 설명·시연 → 60분 실습`

1. Android Studio에서 새 프로젝트 만들기
2. LinearLayout으로 글자를 위에서 아래로 쌓기
3. TextView로 학번·이름·전공 표시하기

---

## 1일차 · 0–5분 — 새 프로젝트 만들기

1. **New Project** → **Empty Views Activity** 선택
2. Name: `StudentCard` · Language: **Kotlin**
3. **Finish** → 아래쪽 진행 표시가 끝날 때까지 기다리기
4. 기기를 고르고 **Run ▶** → `Hello World!` 확인

이름이 비슷한 **Empty Activity**가 아니라 **Empty Views Activity**를 고릅니다.

---

## 1일차 · 5–15분 ① — Project 창의 세 폴더

왼쪽 **Project** 창(위쪽이 `Android` 보기)에서 `app`을 펼치면 폴더 세 개가 보입니다.

| 폴더 | 들어 있는 것 |
|---|---|
| `manifests` | 앱 정보 파일 `AndroidManifest.xml` — 이번 주에는 열지 않습니다 |
| `kotlin+java` | Kotlin 코드. `MainActivity.kt`가 여기 있습니다 |
| `res` | 화면·그림 같은 자원. `layout › activity_main.xml`이 여기 있습니다 |

이번 주에 여는 파일은 `kotlin+java`와 `res`에 하나씩, **둘뿐**입니다.
나머지 폴더와 파일은 이름만 보고 지나갑니다.

---

## 1일차 · 5–15분 ② — 화면을 만드는 두 파일

| 파일 | 하는 일 |
|---|---|
| `res/layout/activity_main.xml` | 화면에 **무엇을 어떻게** 놓을지 적는다 |
| `MainActivity.kt` | 앱이 시작될 때 **할 일**을 적는다 |

```kotlin
setContentView(R.layout.activity_main)
```

“`activity_main.xml`을 이 화면으로 쓴다”는 뜻입니다. 1일차에는 XML만 고칩니다.

---

## 1일차 · 5–15분 ③ — LinearLayout은 차례로 쌓는다

```text
vertical (세로)            horizontal (가로)

내 정보                    [-1] [초기화] [+1]
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과
```

- 안에 넣은 **순서대로** 한 줄씩 놓습니다.
- `android:orientation`: `vertical`은 위에서 아래로, `horizontal`은 옆으로
- `android:gravity="center"`: 안의 내용을 가운데로 모읍니다.

---

## 1일차 · 15–25분 ① — TextView 하나 읽기

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_marginTop="8dp"
    android:text="학번: 20260001"
    android:textSize="20sp" />
```

- `wrap_content`: 글자에 딱 맞는 크기 (`match_parent`는 부모만큼)
- `android:text`: 화면에 보일 글자
- 글자 크기는 `sp`, 간격은 `dp`를 씁니다.

---

## 1일차 · 15–25분 ② — 내 정보 화면 완성하기

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <!-- TextView 네 개: 내 정보 · 학번 · 이름 · 전공 -->

</LinearLayout>
```

- `android:id="@+id/main"`은 **지우지 않습니다.** `MainActivity.kt`가 씁니다.
- 학번 TextView를 복사해 붙이고 `android:text`만 바꿉니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--linearlayout으로-내-정보-화면-만들기-60분) · [따라하기](walkthrough.md#1일차)

1. `StudentCard` 프로젝트를 만들고 `Hello World!`를 실행합니다.
2. `activity_main.xml`을 LinearLayout으로 바꿉니다.
3. 학번·이름·전공을 본인 정보로 띄우고 캡처합니다.

**설명 합계: 5+10+10+5 = 30분**

막히면 `android:id="@+id/main"`, 따옴표, `/>` 짝부터 확인합니다.

---

# 2일차 — 코드로 화면 바꾸기

`30분 설명·시연 → 60분 실습`

1. `android:id`로 View에 이름표 붙이기
2. `findViewById`로 View를 찾아 글자 바꾸기
3. 버튼을 누를 때마다 숫자 세기

---

## 2일차 · 0–5분 — id는 View의 이름표

```xml
<TextView
    android:id="@+id/nameText"
    android:text="이름: ?"
    ... />
```

```kotlin
R.id.nameText
```

- XML에서 `@+id/nameText`로 이름표를 붙입니다.
- Kotlin에서는 `R.id.nameText`로 같은 View를 가리킵니다.
- 철자가 한 글자라도 다르면 찾지 못합니다.

---

## 2일차 · 5–15분 ① — 지금은 안 봐도 되는 틀

```kotlin
class MainActivity : AppCompatActivity() {                  // 틀
    override fun onCreate(savedInstanceState: Bundle?) {    // 틀: 앱이 켜질 때 실행
        super.onCreate(savedInstanceState)                  // 틀
        enableEdgeToEdge()                                  // 틀
        setContentView(R.layout.activity_main)              // 화면 파일 연결
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            ...                                             // 틀 (insets 블록)
        }
        // ← 오늘 쓰는 코드는 이 자리에 넣습니다
    }
}
```

- 템플릿이 만든 줄은 **지우지도 고치지도 않습니다.** 뜻은 3주차부터 배웁니다.
- 우리 자리는 `onCreate()` 안, `insets` 블록 **아래**입니다.

---

## 2일차 · 5–15분 ② — findViewById로 찾아서 바꾸기

```kotlin
val name = "홍길동"
val nameText = findViewById<TextView>(R.id.nameText)
nameText.text = "이름: $name"
```

| 1주차 (콘솔) | 2주차 (앱 화면) |
|---|---|
| `println("이름: $name")` | `nameText.text = "이름: $name"` |

`findViewById<TextView>`: id가 `nameText`인 **TextView**를 찾아 줘

---

## 2일차 · 5–15분 ③ — 버튼을 누르면 실행할 코드

```kotlin
val plusButton = findViewById<Button>(R.id.plusButton)

plusButton.setOnClickListener {
    // 버튼을 누를 때마다 이 안의 코드가 실행된다
}
```

- `{ }` 안의 코드는 앱이 켜질 때가 아니라 **누를 때마다** 실행됩니다.
- `TextView`, `Button`이 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 import합니다.

---

## 2일차 · 15–25분 ① — 숫자와 버튼 배치하기

```xml
<TextView
    android:id="@+id/countText"
    android:text="0"
    android:textSize="40sp"
    ... />

<LinearLayout android:orientation="horizontal" ...>
    <Button android:id="@+id/minusButton" android:text="-1" ... />
    <Button android:id="@+id/resetButton" android:text="초기화" ... />
    <Button android:id="@+id/plusButton" android:text="+1" ... />
</LinearLayout>
```

- 숫자 TextView 하나와, 버튼 세 개를 감싼 **가로** LinearLayout을 정보 아래에 둡니다.
- 전체 XML은 [따라하기 9단계](walkthrough.md#9-숫자와-버튼-배치하기)에서 붙여 넣습니다.

---

## 2일차 · 15–25분 ② — var로 숫자 세기

```kotlin
var count = 0
val countText = findViewById<TextView>(R.id.countText)

plusButton.setOnClickListener {
    count = count + 1
    countText.text = "$count"
}
```

- 누를 때마다 값이 바뀌므로 `val`이 아니라 `var`입니다.
- 화면에는 글자가 들어가므로 `count`가 아니라 `"$count"`로 넣습니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--버튼으로-숫자-세기-60분) · [따라하기](walkthrough.md#2일차)

1. 이름 TextView에 id를 붙이고 코드로 글자를 바꿉니다.
2. `+1` 버튼을 누르면 숫자가 1씩 늘게 합니다.
3. `-1`과 `초기화` 버튼은 `+1` 코드를 보고 **직접** 완성합니다.

**설명 합계: 5+10+10+5 = 30분**

---

## 제출하기

2일차가 끝나면 세 가지를 한 번 제출합니다.

1. **`activity_main.xml`**
2. **`MainActivity.kt`**
3. **실행 화면 캡처 1장**: 학번·이름·전공과 숫자 `3`이 보이는 화면

---

## 확장 — layout_weight로 버튼 세 개 가로 균등

```xml
<Button
    android:id="@+id/minusButton"
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    android:layout_weight="1"
    android:text="-1" />
```

- 버튼을 감싼 가로 LinearLayout의 `layout_width`를 `match_parent`로 바꿉니다.
- 버튼 세 개 모두 `layout_width="0dp"` + `layout_weight="1"` → 남은 폭을 **1:1:1**로 나눕니다.
- 폭은 weight가 정하므로 `layout_width`는 `0dp`로 비워 둡니다.
- 먼저 끝난 학생의 선택 과제입니다. 실습지 [먼저 끝났다면](lab.md#먼저-끝났다면)을 봅니다.

---

## 다음 주 미리 보기

숫자를 `3`으로 만든 뒤 에뮬레이터 화면을 **돌려** 보세요.

숫자는 어떻게 되었나요? 왜 그럴까요?

3주차에는 화면이 다시 만들어지는 **Activity 생명주기**를 배웁니다.
