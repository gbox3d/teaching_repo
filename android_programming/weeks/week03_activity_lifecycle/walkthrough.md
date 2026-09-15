# 3주차 따라하기 — 생명주기 로그와 회전해도 남는 숫자

2주차 `StudentCard` 프로젝트를 그대로 이어서 쓴다. 이번 주에는 `activity_main.xml`을 고치지 않고 `MainActivity.kt`만 고친다.
각 단계의 결과가 화면이나 Logcat에 보이면 다음 단계로 넘어간다.

코드의 학번 `20260001`, 이름 `홍길동`, 전공 `컴퓨터공학과`는 연습용 값이다.
Android Studio와 에뮬레이터는 실습실 PC에 설치된 것을 사용하며, 버전은 수업 공지를 따른다.

## 1일차

### 1. 2주차 프로젝트 열기

1. Android Studio를 실행하고 **Recent Projects**에서 `StudentCard`를 연다. 없으면 **Open**으로 저장한 폴더를 고른다.
2. `Run ▶`을 눌러 `+1`·`-1`·`초기화` 버튼이 동작하는지 확인한다.
3. 프로젝트가 없거나 동작하지 않으면 2주차 완성 코드 두 파일을 넣는다.
   [activity_main.xml](../week02_views_layout/examples/day2/activity_main.xml)은 `app › res › layout`에,
   [MainActivity.kt](../week02_views_layout/examples/day2/MainActivity.kt)는 `app › kotlin+java › com.example.studentcard`에 넣는다.

이번 주 `activity_main.xml`은 2주차와 같다. 같은 코드가 [examples/day1/activity_main.xml](examples/day1/activity_main.xml)에 있다.

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

### 2. Logcat 창 열기

1. Android Studio 아래쪽 도구 막대에서 **Logcat**을 누른다. 보이지 않으면 위쪽 메뉴 **View › Tool Windows › Logcat**을 누른다.
2. Logcat 창 위쪽의 필터 칸(돋보기 옆)에 아래 글자를 입력하고 Enter를 누른다.

```text
package:mine tag:Life
```

3. 아직은 아무 줄도 보이지 않는다. `Life` 태그로 남긴 기록이 없기 때문이다.

`package:mine`은 내 앱이 남긴 줄만, `tag:Life`는 태그가 `Life`인 줄만 보여 준다. 필터를 지우면 다른 앱의 줄이 수백 개 쏟아진다.

### 3. onCreate에 Log.d 한 줄 넣기

1. `MainActivity.kt`를 열고 `super.onCreate(savedInstanceState)` 줄 **바로 아래**에 한 줄을 넣는다.

```kotlin
        Log.d("Life", "onCreate")
```

2. `Log`가 빨간색이면 그 글자에 커서를 두고 **Alt+Enter**(맥은 ⌥+Enter)를 눌러 **Import class**를 고른다.
   파일 위쪽에 `import android.util.Log` 줄이 생긴다.
3. 실행한다. Logcat에 아래 한 줄이 보이면 성공이다.

```text
Life   com.example.studentcard   D   onCreate
```

`Log.d("Life", "onCreate")`는 1주차 `println("onCreate")`의 앱 버전이다. 앱에는 콘솔이 없으므로 Logcat에 남긴다.
첫 번째 글자 `"Life"`는 태그(이름표), 두 번째 글자가 남길 내용이다.

### 4. 나머지 콜백 6개 추가하기

`onCreate`의 마지막 `}` **아래**, class의 마지막 `}` **위**에 아래 코드를 넣는다.
`onCreate`의 마지막 `}`는 `resetButton.setOnClickListener { ... }` 블록이 끝난 다음 줄에 있다.

```kotlin
    // 3. 나머지 생명주기 콜백. 불릴 때마다 Logcat에 이름을 남긴다.
    override fun onStart() {
        super.onStart()
        Log.d("Life", "onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d("Life", "onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d("Life", "onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d("Life", "onStop")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("Life", "onRestart")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("Life", "onDestroy")
    }
```

실행하면 Logcat에 세 줄이 순서대로 보인다.

```text
onCreate
onStart
onResume
```

- `override fun onStart()`: 시스템이 부르는 `onStart`에 내 코드를 끼워 넣는다. `override`를 빼면 빌드 오류가 난다.
- `super.onStart()`: 원래 할 일을 먼저 하게 한다. 이 줄을 지우면 실행하자마자 앱이 꺼진다.
  그 이유는 필터 `tag:Life`에 걸러져 보이지 않으므로, 필터에서 `tag:Life`를 지우고 `package:mine`만 남긴 뒤
  빨간 줄(`FATAL EXCEPTION`)을 읽는다. 다 읽으면 필터를 되돌린다.
- 여섯 개는 이름만 다르고 모양이 같다. 하나를 쓰고 복사해서 이름만 바꿔도 된다.

### 5. 행동별 순서 관찰하기

Logcat 왼쪽 위의 **휴지통** 아이콘을 누르면 지금까지의 줄이 지워진다. 행동 하나마다 지우고 다시 보면 읽기 쉽다.

| 행동 | 에뮬레이터에서 하는 법 |
|---|---|
| 홈 버튼 | 에뮬레이터 오른쪽 도구 막대의 **○** 버튼, 또는 화면 아래에서 위로 쓸어 올리기 |
| 복귀 | 앱 목록에서 `StudentCard` 아이콘을 다시 누르기 |
| 회전 | 에뮬레이터 도구 막대의 **회전** 버튼. 화면이 안 돌면 빠른 설정에서 **자동 회전**을 켠다 |
| 뒤로 | 에뮬레이터 도구 막대의 **◁** 버튼 |

실행하면 Logcat에 이렇게 찍힌다.

| 행동 | Logcat 순서 |
|---|---|
| 실행 | `onCreate` → `onStart` → `onResume` |
| 홈 버튼 | `onPause` → `onStop` |
| 복귀 | `onRestart` → `onStart` → `onResume` |
| 회전 | `onPause` → `onStop` → `onDestroy` → `onCreate` → `onStart` → `onResume` |
| 뒤로 | `onPause` → `onStop` → `onDestroy` |

회전에서 `onDestroy` 뒤에 `onCreate`가 다시 나온다. 화면이 도는 것이 아니라 **Activity가 새로 만들어진다.**
그래서 `onCreate` 안의 `var count = 0`이 다시 실행되어 숫자가 `0`이 된다. 홈 버튼 뒤 복귀에서는 `onCreate`가 없으므로 숫자가 남는다.

### 6. +1 버튼에 Toast 넣기

1. `plusButton.setOnClickListener { ... }` 안, `countText.text = "$count"` 줄 **아래**에 한 줄을 넣는다.

```kotlin
            Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()
```

2. `Toast`가 빨간색이면 3단계처럼 **Alt+Enter**로 import한다. `import android.widget.Toast` 줄이 생긴다.
3. 실행하고 `+1`을 누르면 화면 아래에 `지금 숫자: 1`이 잠깐 떴다 사라진다.

- `Toast.makeText(어디에, 무엇을, 얼마나)`: `this`는 이 화면(MainActivity), 글자, `LENGTH_SHORT`는 짧게.
- 끝의 `.show()`를 빼면 빌드는 되지만 아무것도 보이지 않는다.

### 7. 1일차 완성 코드

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.studentcard

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("Life", "onCreate")
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

        // 2. 버튼을 누를 때마다 숫자를 바꾼다. +1은 Toast로도 알린다.
        var count = 0
        val countText = findViewById<TextView>(R.id.countText)
        val plusButton = findViewById<Button>(R.id.plusButton)
        val minusButton = findViewById<Button>(R.id.minusButton)
        val resetButton = findViewById<Button>(R.id.resetButton)

        plusButton.setOnClickListener {
            count = count + 1
            countText.text = "$count"
            Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()
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

    // 3. 나머지 생명주기 콜백. 불릴 때마다 Logcat에 이름을 남긴다.
    override fun onStart() {
        super.onStart()
        Log.d("Life", "onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d("Life", "onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d("Life", "onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d("Life", "onStop")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("Life", "onRestart")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("Life", "onDestroy")
    }
}
```

`package com.example.studentcard` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
`//` 뒤의 설명은 넣지 않아도 된다.

### 8. 기록하고 보관하기

5단계의 순서표를 [실습지](lab.md#3-콜백-6개-추가하고-순서-기록표-채우기)에 옮겨 적고, 회전 때의 Logcat을 캡처해 둔다.
Android Studio는 파일을 자동으로 저장하므로 프로젝트를 닫아도 된다. 2일차에는 같은 프로젝트를 다시 연다.

## 2일차

### 9. 문제 다시 보기

1일차 프로젝트를 열고 실행한다. `+1`을 세 번 눌러 `3`을 만들고 회전한다. 숫자가 `0`이 되고 Logcat에는
`onDestroy` 다음에 `onCreate`가 찍힌다. 오늘은 `onDestroy` **전에 저장**하고 `onCreate`**에서 복원**한다.

### 10. count를 class 바로 안으로 옮기기

1. `onCreate` 안의 `var count = 0` 줄과 그 바로 위의 `// 2. 버튼을 누를 때마다 …` 주석 줄을 지운다.
2. `class MainActivity : AppCompatActivity() {` 줄 **바로 아래**에 아래 두 줄을 넣는다.

```kotlin
    // 숫자를 onCreate 밖, class 바로 안에 둔다. onCreate와 onSaveInstanceState가 함께 쓴다.
    var count = 0
```

3. 실행한다. 버튼은 전과 똑같이 동작한다.

`onCreate` 안에 있던 `count`는 `onCreate` 안에서만 쓸 수 있었다. 곧 만들 저장 함수에서도 써야 하므로 class 바로 안으로 옮긴다.
class 바로 안에 둔 변수는 그 class의 모든 함수에서 쓸 수 있다.

### 11. onSaveInstanceState로 저장하기

`onCreate`의 마지막 `}` **아래**, `override fun onStart()` **위**에 아래 코드를 넣는다.

```kotlin
    // 4. 화면이 사라지기 전에 시스템이 부른다. 여기서 숫자를 저장한다.
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("count", count)
        Log.d("Life", "onSaveInstanceState count=$count")
    }
```

실행하고 `3`을 만든 뒤 회전한다. 숫자는 **아직 `0`**이지만, Logcat에 `onSaveInstanceState count=3`이 찍힌다.
저장은 되었고 아직 꺼내지 않았을 뿐이다.

- `outState`는 값을 담는 가방(`Bundle`)이다. 시스템이 만들어서 넘겨 주므로 `?`가 없다.
- `putInt("count", count)`: 이름표 `"count"`를 붙여 숫자를 넣는다. 이름표는 꺼낼 때 다시 쓴다.
- `onSaveInstanceState(outState: Bundle?)`처럼 `?`를 붙이면 `overrides nothing` 오류가 난다.

### 12. onCreate에서 복원하기

`onCreate` 안의 `val countText = findViewById<TextView>(R.id.countText)` 줄을 찾아, 그 줄 **위**에 주석과 복원 한 줄, **아래**에 화면에 쓰는 한 줄을 넣는다.
이어서 `val plusButton = …` 줄 위에 빈 줄과 `// 3. …` 주석을 넣는다. 완성된 모양은 아래와 같다. `//` 주석 줄은 넣지 않아도 된다.

```kotlin
        // 2. 저장해 둔 숫자가 있으면 꺼내 쓰고, 없으면(처음 실행) 0으로 시작한다.
        count = savedInstanceState?.getInt("count") ?: 0
        val countText = findViewById<TextView>(R.id.countText)
        countText.text = "$count"

        // 3. 버튼을 누를 때마다 숫자를 바꾼다. +1은 Toast로도 알린다.
        val plusButton = findViewById<Button>(R.id.plusButton)
```

실행하고 `+1`을 세 번 눌러 `3`을 만든 뒤 회전한다. `3`이 그대로 남으면 성공이다.

| 코드 | 뜻 |
|---|---|
| `savedInstanceState` | `onCreate`가 받는 `Bundle?`. 처음 실행은 null, 회전 뒤에는 11단계에서 저장한 가방 |
| `?.getInt("count")` | 가방이 null이면 이 식 전체가 null, 아니면 이름표 `"count"`의 숫자 |
| `?: 0` | 왼쪽이 null이면(처음 실행) `0`을 쓴다 |
| `countText.text = "$count"` | 꺼낸 숫자를 화면에도 쓴다. 없으면 숫자는 `3`인데 화면은 `0`으로 보인다 |

`savedInstanceState.getInt("count")`처럼 `?.` 대신 `.`을 쓰면 `Only safe (?.) or non-null asserted (!!.) calls are allowed` 오류가 난다.
`!!`로 고치라는 뜻이 아니다. `?.`와 `?: 0`을 쓴다.

### 13. 검증하고 캡처하기

| 순서 | 할 일 | 보여야 하는 것 |
|---|---|---|
| 1 | 실행 → `+1` 세 번 | `3` |
| 2 | 회전 | `3` 그대로 → **캡처 1** |
| 3 | Logcat | 아래 순서 → **캡처 2** |
| 4 | 회전한 채로 `+1` 한 번 | `4` (복원한 숫자에서 이어서 센다) |
| 5 | 홈 버튼 → 복귀 | `4` 그대로. `onRestart`가 찍히고 `onCreate`는 없다 |
| 6 | 뒤로 → 앱 다시 실행 | `0`. 뒤로로 끝낸 앱은 저장하지 않는다. 정상이다 |

```text
onPause
onStop
onSaveInstanceState count=3
onDestroy
onCreate
onStart
onResume
```

`onSaveInstanceState`는 `onStop` 다음, `onDestroy` 전에 찍힌다. 홈 버튼을 눌렀을 때도 찍히지만, 그때는 A가 살아 있어 복원할 일이 없다.

### 14. 2일차 완성 코드

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.studentcard

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    // 숫자를 onCreate 밖, class 바로 안에 둔다. onCreate와 onSaveInstanceState가 함께 쓴다.
    var count = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("Life", "onCreate")
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

        // 2. 저장해 둔 숫자가 있으면 꺼내 쓰고, 없으면(처음 실행) 0으로 시작한다.
        count = savedInstanceState?.getInt("count") ?: 0
        val countText = findViewById<TextView>(R.id.countText)
        countText.text = "$count"

        // 3. 버튼을 누를 때마다 숫자를 바꾼다. +1은 Toast로도 알린다.
        val plusButton = findViewById<Button>(R.id.plusButton)
        val minusButton = findViewById<Button>(R.id.minusButton)
        val resetButton = findViewById<Button>(R.id.resetButton)

        plusButton.setOnClickListener {
            count = count + 1
            countText.text = "$count"
            Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()
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

    // 4. 화면이 사라지기 전에 시스템이 부른다. 여기서 숫자를 저장한다.
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("count", count)
        Log.d("Life", "onSaveInstanceState count=$count")
    }

    // 5. 나머지 생명주기 콜백. 불릴 때마다 Logcat에 이름을 남긴다.
    override fun onStart() {
        super.onStart()
        Log.d("Life", "onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d("Life", "onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d("Life", "onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d("Life", "onStop")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("Life", "onRestart")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("Life", "onDestroy")
    }
}
```

1일차 코드와 다른 곳은 세 군데다. `var count = 0`의 위치, `onCreate`의 복원 두 줄, `onSaveInstanceState` 함수. `//` 주석의 번호는 달라도 된다.

### 15. 제출하기

제출물은 세 가지다.

1. `MainActivity.kt`
2. 캡처 1: 회전한 뒤에도 숫자 `3`이 보이는 화면
3. 캡처 2: 회전할 때 `onSaveInstanceState count=3`이 찍힌 Logcat

파일은 Project 창에서 오른쪽 클릭하고 **Open In › Finder**(Windows는 **Explorer**)를 누르면 폴더에서 찾을 수 있다.
Logcat은 창을 넓힌 뒤 화면 캡처 도구로 찍는다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 요청한다.
