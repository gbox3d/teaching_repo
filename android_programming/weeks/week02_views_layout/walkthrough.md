# 2주차 따라하기 — 내 정보 화면과 카운터

처음에는 그대로 따라 하고, 결과가 나오면 본인 정보로 바꾼다.
각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.

코드의 학번 `20260001`, 이름 `홍길동`, 전공 `컴퓨터공학과`는 연습용 값이다.
Android Studio와 에뮬레이터는 실습실 PC에 설치된 것을 사용하며, 버전은 수업 공지를 따른다.

## 1일차

### 1. 새 프로젝트 만들기

1. Android Studio를 실행하고 **New Project**를 누른다. 이미 열린 프로젝트가 있으면 **File › New › New Project**를 누른다.
2. **Phone and Tablet**에서 **Empty Views Activity**를 고르고 **Next**를 누른다.
   이름이 비슷한 **Empty Activity**는 고르지 않는다. 오늘 사용할 `activity_main.xml`이 만들어지지 않는다.
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

### 2. 처음 실행하기

1. 위쪽 도구 막대의 기기 목록에서 에뮬레이터를 고른다.
2. `Run ▶` 버튼을 누른다.
3. 에뮬레이터에 `Hello World!`가 보이면 성공이다.

기기 목록이 비어 있으면 **Device Manager**에서 강의자가 안내한 에뮬레이터를 실행한다.

### 3. 두 파일 찾기

왼쪽 **Project** 창 위쪽이 `Android` 보기인지 확인하고 `app`을 펼친다. 폴더 세 개가 보인다.

| 폴더 | 들어 있는 것 | 이번 주 |
|---|---|---|
| `manifests` | 앱 정보 파일 `AndroidManifest.xml` | 열지 않는다 |
| `kotlin+java` | Kotlin 코드 | `MainActivity.kt`를 연다 |
| `res` | 화면·그림 같은 자원 | `layout › activity_main.xml`을 연다 |

이번 주에 여는 파일은 아래 두 개뿐이다.

| 파일 | 위치 | 하는 일 |
|---|---|---|
| `activity_main.xml` | `app › res › layout` | 화면에 무엇을 놓을지 적는다 |
| `MainActivity.kt` | `app › kotlin+java › com.example.studentcard` | 앱이 시작될 때 할 일을 적는다 |

`MainActivity.kt`에 있는 아래 줄이 두 파일을 이어 준다. 1일차에는 이 파일을 고치지 않는다.

```kotlin
setContentView(R.layout.activity_main)
```

`activity_main.xml`을 열었을 때 그림 화면만 보이면 오른쪽 위의 **Code** 버튼을 누른다.

### 4. LinearLayout으로 바꾸기

`activity_main.xml`의 내용을 **모두 지우고** 아래 코드를 넣은 뒤 실행한다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="내 정보"
        android:textSize="28sp"
        android:textStyle="bold" />

</LinearLayout>
```

화면 가운데에 `내 정보`가 보이면 성공이다.

- `android:orientation="vertical"`: 안에 넣은 View를 위에서 아래로 쌓는다.
- `android:gravity="center"`: 안의 내용을 화면 가운데로 모은다.
- `android:id="@+id/main"`: **지우지 않는다.** `MainActivity.kt`의 `findViewById(R.id.main)`이 이 이름을 사용한다.
  지우면 `Unresolved reference 'id'` 빌드 오류가 난다.

### 5. 학번·이름·전공 추가하기

`activity_main.xml` 전체를 아래 코드로 바꾼다. 학번·이름·전공은 본인 정보로 쓴다.
같은 코드가 [examples/day1/activity_main.xml](examples/day1/activity_main.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="내 정보"
        android:textSize="28sp"
        android:textStyle="bold" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="학번: 20260001"
        android:textSize="20sp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="이름: 홍길동"
        android:textSize="20sp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="전공: 컴퓨터공학과"
        android:textSize="20sp" />

</LinearLayout>
```

실행하면 화면 가운데에 아래 네 줄이 보인다.

```text
내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과
```

| 속성 | 뜻 |
|---|---|
| `wrap_content` | 글자에 딱 맞는 크기 |
| `match_parent` | 부모(바깥 LinearLayout)만큼의 크기 |
| `android:textSize="20sp"` | 글자 크기. 글자에는 `sp`를 쓴다 |
| `android:layout_marginTop="8dp"` | 위쪽 간격. 간격에는 `dp`를 쓴다 |
| `android:textStyle="bold"` | 굵은 글씨 |

XML 글자 아래에 노란 줄이 생길 수 있다. 경고일 뿐 실행에는 문제가 없다.

### 6. 속성을 바꿔 보기

한 번에 한 곳만 바꾸고 실행한다. 결과를 본 뒤 원래대로 되돌린다.

1. 바깥 LinearLayout의 `vertical`을 `horizontal`로 바꾼다. → 네 TextView가 한 줄에 옆으로 붙는다. 폭이 좁은 폰에서는 마지막 전공 글자가 여러 줄로 접힌다.
2. `android:gravity="center"` 줄을 지운다. → 글자가 화면 왼쪽 위로 붙는다.
3. 학번의 `20sp`를 `40sp`로 바꾼다. → 학번 글자만 커진다.

바꾼 결과는 [실습지](lab.md#4-하나씩-바꿔-보기)의 표에 적는다.

### 7. 캡처하고 보관하기

본인 정보가 보이는 화면을 캡처한다. Android Studio는 파일을 자동으로 저장하므로 프로젝트를 닫아도 된다.
2일차에는 같은 `StudentCard` 프로젝트를 다시 연다.

## 2일차

### 8. 코드로 이름 바꾸기

1. `activity_main.xml`에서 이름 TextView를 찾아 **두 곳**을 바꾼다.
   `android:id="@+id/nameText"` 줄을 추가하고, `android:text`를 `이름: ?`로 바꾼다.

```xml
    <TextView
        android:id="@+id/nameText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="이름: ?"
        android:textSize="20sp" />
```

2. 실행해서 `이름: ?`가 보이는지 확인한다.
3. `MainActivity.kt`를 연다. 템플릿이 만든 아래 코드가 이미 들어 있다(같은 내용이 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다).
   이 줄들은 **지금은 안 봐도 되는 틀**이므로 지우거나 고치지 않는다. 지웠다면 아래 코드를 그대로 다시 넣는다.

```kotlin
package com.example.studentcard

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }
}
```

| 템플릿 코드 | 지금 알아둘 것 |
|---|---|
| `class MainActivity : AppCompatActivity() {` | 이 화면의 코드를 담는 틀 |
| `override fun onCreate(savedInstanceState: Bundle?) {` | 앱이 켜질 때 실행되는 곳. 우리 코드는 이 안에 넣는다 |
| `super.onCreate(...)`, `enableEdgeToEdge()` | 틀. 그대로 둔다 |
| `setContentView(R.layout.activity_main)` | 화면 파일을 연결하는 줄 |
| `ViewCompat.setOnApplyWindowInsetsListener(...) { ... }` | 틀(`insets` 블록). 그대로 둔다 |

   `onCreate()`의 **마지막 `}` 바로 위**, 즉 `insets` 블록의 닫는 `}` 아래에 아래 세 줄을 넣는다.

```kotlin
        val name = "홍길동"
        val nameText = findViewById<TextView>(R.id.nameText)
        nameText.text = "이름: $name"
```

4. `TextView`가 빨간색이면 그 글자에 커서를 두고 **Alt+Enter**(맥은 ⌥+Enter)를 눌러 **Import class**를 고른다.
   위쪽 `import` 줄에 `import android.widget.TextView`가 생긴다.
5. `홍길동`을 본인 이름으로 바꾸고 실행한다. `이름: ?`가 본인 이름으로 바뀌면 성공이다.
   코드를 `onCreate()` 바깥에 넣으면 `Syntax error: Expecting member declaration` 오류가 난다. 위치를 다시 확인한다.

1주차의 `println("이름: $name")`은 콘솔에 출력했다. `nameText.text = "이름: $name"`은 **앱 화면**의 글자를 바꾼다.

### 9. 숫자와 버튼 배치하기

`activity_main.xml` 전체를 아래 코드로 바꾼다. 학번·전공은 다시 본인 정보로 쓴다.
같은 코드가 [examples/day2/activity_main.xml](examples/day2/activity_main.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="내 정보"
        android:textSize="28sp"
        android:textStyle="bold" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="학번: 20260001"
        android:textSize="20sp" />

    <TextView
        android:id="@+id/nameText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="이름: ?"
        android:textSize="20sp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="전공: 컴퓨터공학과"
        android:textSize="20sp" />

    <TextView
        android:id="@+id/countText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="32dp"
        android:text="0"
        android:textSize="40sp" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/minusButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="-1" />

        <Button
            android:id="@+id/resetButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:text="초기화" />

        <Button
            android:id="@+id/plusButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:text="+1" />

    </LinearLayout>

</LinearLayout>
```

실행하면 정보 아래에 `0`과 버튼 세 개가 보인다. 아직 버튼을 눌러도 아무 일도 일어나지 않는다.
버튼 세 개가 옆으로 놓인 것은 버튼을 감싼 LinearLayout이 `horizontal`이기 때문이다.

- `android:layout_marginStart="8dp"`: 왼쪽(시작) 간격. 옆으로 놓을 때 쓴다. 위쪽 간격 `layout_marginTop`과 같은 방식이다.

### 10. `+1` 버튼 동작시키기

8단계에서 넣은 세 줄 **아래**에 이어서 넣는다.

```kotlin
        var count = 0
        val countText = findViewById<TextView>(R.id.countText)
        val plusButton = findViewById<Button>(R.id.plusButton)

        plusButton.setOnClickListener {
            count = count + 1
            countText.text = "$count"
        }
```

`Button`이 빨간색이면 8단계처럼 import한다. 실행하고 `+1`을 세 번 눌러 `3`이 되면 성공이다.

- `var count = 0`: 누를 때마다 바뀌는 값이므로 `var`로 만든다.
- `setOnClickListener { }`: 중괄호 안의 코드는 버튼을 **누를 때마다** 실행된다.
- `"$count"`: 화면에는 글자를 넣어야 하므로 숫자를 문자열로 바꿔 넣는다.

### 11. `-1`과 `초기화` 버튼 완성하기

먼저 [실습지](lab.md#3--1과-초기화-버튼-직접-완성하기)를 보고 직접 만들어 본다. 완성한 `MainActivity.kt` 전체는 아래와 같다.
같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.studentcard

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. id로 TextView를 찾아 글자를 바꾼다.
        val name = "홍길동"
        val nameText = findViewById<TextView>(R.id.nameText)
        nameText.text = "이름: $name"

        // 2. 버튼을 누를 때마다 숫자를 바꾼다.
        var count = 0
        val countText = findViewById<TextView>(R.id.countText)
        val plusButton = findViewById<Button>(R.id.plusButton)
        val minusButton = findViewById<Button>(R.id.minusButton)
        val resetButton = findViewById<Button>(R.id.resetButton)

        plusButton.setOnClickListener {
            count = count + 1
            countText.text = "$count"
        }

        minusButton.setOnClickListener {
            count = count - 1
            countText.text = "$count"
        }

        resetButton.setOnClickListener {
            count = 0
            countText.text = "$count"
        }
    }
}
```

`package com.example.studentcard` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
`//` 뒤의 설명은 1주차에 배운 주석이라 넣지 않아도 된다.

| 누른 순서 | 화면 숫자 |
|---|---|
| `+1` 세 번 | `3` |
| 이어서 `-1` 한 번 | `2` |
| 이어서 `초기화` | `0` |
| 이어서 `-1` 한 번 | `-1` |

### 12. 화면 돌려 보기

숫자를 `3`으로 만든 뒤 에뮬레이터 도구 막대의 **회전** 버튼을 눌러 화면을 돌린다.
화면이 돌지 않으면 에뮬레이터 화면 위쪽을 아래로 끌어 빠른 설정을 열고 **자동 회전**을 켠 뒤 다시 누른다.

숫자가 `0`으로 돌아간다. 이름은 코드가 다시 넣으므로 그대로 보인다.
코드가 틀린 것이 아니다. 왜 이런 일이 생기는지는 3주차에 배운다. 이번 주에는 관찰한 내용만 적는다.

### 13. 제출하기

숫자를 `3`으로 만든 화면을 캡처한다. 제출물은 세 가지다.

1. `activity_main.xml`
2. `MainActivity.kt`
3. 실행 화면 캡처 1장

두 파일은 Project 창에서 파일을 오른쪽 클릭하고 **Open In › Finder**(Windows는 **Explorer**)를 누르면 폴더에서 찾을 수 있다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 요청한다.
