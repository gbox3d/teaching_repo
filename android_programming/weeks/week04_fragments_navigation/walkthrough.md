# 4주차 따라하기 — SmartIO 연결 화면과 제어 화면

처음에는 그대로 따라 하고, 결과가 나오면 장치 이름과 핀 번호를 바꿔 본다.
각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.

이번 주는 `StudentCard`를 이어 쓰지 않고 새 프로젝트 `SmartIO`를 만든다. 학기 끝까지 이 프로젝트를 키운다.
코드의 장치 이름 `ESP32_BLE_1`, 핀 번호 `3`은 연습용 값이다.
Android Studio와 에뮬레이터는 실습실 PC에 설치된 것을 사용하며, 버전은 수업 공지를 따른다.

## 1일차

### 1. 새 프로젝트 만들기

1. Android Studio에서 **File › New › New Project**를 누른다.
2. **Phone and Tablet**에서 **Empty Views Activity**를 고르고 **Next**를 누른다. 2주차와 같이 **Empty Activity**는 고르지 않는다.
3. 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Name | `SmartIO` |
| Package name | `com.example.smartio` (Name을 쓰면 자동으로 채워진다) |
| Save location | 기본값 또는 강의자가 안내한 폴더 |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |
| Build configuration language | 기본값 |

4. 창 아래쪽 진행 표시가 모두 끝날 때까지 기다린다.

### 2. 처음 실행하기

기기 목록에서 에뮬레이터를 고르고 `Run ▶`을 누른다. `Hello World!`가 보이면 성공이다.
왼쪽 Project 창이 `Android` 보기인지 확인하고, 아래 세 파일이 어디 있는지 봐 둔다.

| 파일 | 위치 |
|---|---|
| `build.gradle.kts` **(Module :app)** | `Gradle Scripts` 아래. 같은 이름이 두 개이므로 **(Module :app)**을 연다 |
| `strings.xml` | `app › res › values` |
| `MainActivity.kt` | `app › kotlin+java › com.example.smartio` |

### 3. ViewBinding 켜기와 의존성 넣기

`build.gradle.kts (Module :app)`을 열고 두 곳을 고친다.

1. `android { ... }` 블록 안, `defaultConfig { ... }` 블록이 끝난 다음 줄에 아래를 넣는다.

```kotlin
    buildFeatures {
        viewBinding = true
    }
```

2. 파일 아래쪽 `dependencies { ... }` 블록 안, 마지막 `}` 바로 위에 네 줄을 넣는다. 5~7주차에 쓸 라이브러리를 미리 넣어 두는 것이라 이번 주에는 쓰지 않는다. Sync에서 오류가 나면 네 줄을 지우고 다시 Sync한 뒤, 5주차 전에 강의자 안내를 받아 넣는다.

```kotlin
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
```

3. 편집기 위쪽에 나타나는 **Sync Now**를 누르고 아래쪽 진행 표시가 끝날 때까지 기다린다.

내 파일은 템플릿이 만든 줄이 더 있어서 예제와 모양이 다를 수 있다. 위 두 가지만 들어 있으면 된다.
검증에 쓴 전체 파일은 [examples/day1/build.gradle.kts](examples/day1/build.gradle.kts)이며 아래와 같다.

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.smartio"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.smartio"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    // ViewBinding을 켠다. 이 블록이 있어야 ActivityMainBinding이 만들어진다.
    buildFeatures {
        viewBinding = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    // 5~7주에 쓸 라이브러리. 지금 미리 넣어 둔다.
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
}
```

### 4. MainActivity를 ViewBinding 틀로 바꾸기

`MainActivity.kt`를 열고 세 곳을 고친다.

1. `class MainActivity : AppCompatActivity() {` 바로 아랫줄에 한 줄을 넣는다.

```kotlin
    private lateinit var binding: ActivityMainBinding
```

2. `setContentView(R.layout.activity_main)` 한 줄을 지우고 그 자리에 두 줄을 넣는다.

```kotlin
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
```

3. 그 아래 `ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main))`의 `findViewById(R.id.main)`을 `binding.main`으로 바꾼다.

`ActivityMainBinding`이 빨간색이면 그 글자에 커서를 두고 **Alt+Enter**(맥은 ⌥+Enter) → **Import class**를 고른다.
`import com.example.smartio.databinding.ActivityMainBinding` 줄이 생긴다. 실행해서 `Hello World!`가 그대로 보이면 성공이다.

- `ActivityMainBinding`은 `activity_main.xml`에서 자동으로 만들어진 클래스다. 파일 이름이 `activity_control.xml`이면 `ActivityControlBinding`이 된다.
- `lateinit var binding`은 "값은 `onCreate()`에서 넣는다"는 표시다. 이 줄과 `inflate`·`setContentView(binding.root)` 두 줄은 **틀**이므로 그대로 쓴다.
- Import가 되지 않으면 3단계의 `viewBinding = true`와 **Sync Now**를 다시 확인한다.

### 5. strings.xml에 글자 모으기

`app › res › values › strings.xml`을 열고 전체를 아래 코드로 바꾼다.
같은 코드가 [examples/day1/strings.xml](examples/day1/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_name_hint">장치 이름</string>
    <string name="auto_connect">자동 연결</string>
    <string name="connect">연결</string>
</resources>
```

- `app_name`은 앱 목록에 보이는 앱 이름이다. 이미 있던 줄의 값만 바꾼 것이다.
- XML에서 `@string/connect`라고 쓰면 `연결`이 들어간다. 2주차에 본 노란 `Hardcoded string` 경고가 사라진다.
- 코드에서 만드는 문장(`"연결: $name"`)은 `strings.xml`에 넣지 않아도 된다.

### 6. 연결 화면 배치하기

`activity_main.xml`의 내용을 **모두 지우고** 아래 코드를 넣은 뒤 실행한다.
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
        android:text="@string/app_name"
        android:textSize="28sp"
        android:textStyle="bold" />

    <EditText
        android:id="@+id/deviceNameEdit"
        android:layout_width="240dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:hint="@string/device_name_hint"
        android:inputType="text" />

    <Switch
        android:id="@+id/autoSwitch"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/auto_connect" />

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

</LinearLayout>
```

실행하면 제목 아래에 흐린 글자 `장치 이름`이 있는 입력칸, `자동 연결` 스위치, `연결` 버튼이 보인다.
입력칸을 누르면 키보드가 올라오고 글자를 넣을 수 있다. 아직 버튼과 스위치는 아무 일도 하지 않는다.

| 속성 | 뜻 |
|---|---|
| `android:hint` | 입력칸이 비었을 때 흐리게 보이는 안내 글자. 글자를 넣으면 사라진다 |
| `android:inputType="text"` | 일반 글자 키보드. 2일차에는 `number`를 쓴다 |
| `android:layout_width="240dp"` | 입력칸은 `wrap_content`로 두면 너무 좁아지므로 폭을 정해 준다 |
| `<Switch>` | 켜고 끄는 스위치. `android:text`는 옆에 붙는 글자다 |

`Switch` 아래 노란 줄이 생길 수 있다. 경고일 뿐 실행에는 문제가 없다.

### 7. [연결] 버튼: 빈 값 검사와 Toast

`MainActivity.kt`의 `onCreate()` **마지막 `}` 바로 위**(insets 블록 아래)에 넣는다.

```kotlin
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "연결: $name", Toast.LENGTH_SHORT).show()
            }
        }
```

`Toast`가 빨간색이면 **Alt+Enter**로 import한다(`android.widget.Toast`).
실행해서 빈 채로 [연결]을 누르면 `장치 이름을 입력하세요`, `ESP32_BLE_1`을 넣고 누르면 `연결: ESP32_BLE_1`이 아래쪽에 잠깐 보이면 성공이다.

- `binding.deviceNameEdit`: XML의 `@+id/deviceNameEdit`를 `findViewById` 없이 바로 부른다. 철자가 다르면 빨간 줄이다.
- `.text.toString()`: 입력칸의 글자를 String으로 꺼낸다. `.toString()`을 빼면 `==`로 비교할 때 오류가 난다.
- `name.isEmpty()`: 글자가 하나도 없으면 `true`다.

### 8. 자동 연결 Switch

7단계 코드 **아래**에 이어서 넣는다.

```kotlin
        binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
            }
        }
```

실행해서 스위치를 켜면 `자동 연결 켜짐`, 다시 끄면 `자동 연결 꺼짐`이 보이면 성공이다.

- `{ _, isChecked -> ... }`: 화살표 앞의 두 이름은 틀이다. 첫째는 스위치 자신인데 쓰지 않으므로 `_`로 두고, 둘째 `isChecked`는 켜졌으면 `true`다.
- 켤 때도 끌 때도 `{ }` 안이 실행된다. `if (isChecked)`로 구분한다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. [연결] 버튼: 장치 이름이 비었는지 확인한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "연결: $name", Toast.LENGTH_SHORT).show()
            }
        }

        // 2. 자동 연결 Switch: 켜고 끌 때마다 알린다.
        binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
```

`//` 뒤의 설명은 넣지 않아도 된다. `findViewById`가 한 줄도 없는지 확인한다.

### 9. 캡처하고 보관하기

장치 이름을 입력한 화면을 캡처한다. 2일차에는 같은 `SmartIO` 프로젝트를 다시 연다.

## 2일차

### 10. ControlActivity 만들기

1. Project 창에서 `app › kotlin+java › com.example.smartio` 폴더를 **오른쪽 클릭** → **New › Activity › Empty Views Activity**를 고른다.
2. 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Activity Name | `ControlActivity` |
| Layout Name | `activity_control` (자동으로 채워진다) |
| Launcher Activity | **체크하지 않는다** |
| Package name | `com.example.smartio` (그대로) |
| Source Language | `Kotlin` |

세 곳이 바뀐다. `ControlActivity.kt`와 `activity_control.xml`이 생기고, Manifest에 한 줄이 추가된다.

### 11. Manifest 확인하기

`app › manifests › AndroidManifest.xml`을 열어 `<application>` 안에 아래 줄이 생겼는지 확인한다.

```xml
        <activity
            android:name=".ControlActivity"
            android:exported="false" />
```

- Activity는 Manifest에 **등록**되어야 열 수 있다. 마법사로 만들면 자동으로 들어간다.
- 이 줄이 없으면 빌드는 되지만 [연결]을 누르는 순간 앱이 꺼진다. 내 Manifest는 그대로 두고 이 줄만 확인한다.
- 전체 모양은 [examples/day2/AndroidManifest.xml](examples/day2/AndroidManifest.xml)에 있다. 확인에 필요한 줄만 남긴 것이라 내 파일에 `android:icon` 같은 줄이 더 있어도 된다.
- [examples/day2/res/values/themes.xml](examples/day2/res/values/themes.xml)은 예제를 단독으로 빌드하기 위한 파일이다. 내 프로젝트의 `themes.xml`은 고치지 않는다.

### 12. [연결]에서 제어 화면으로 이동하기

`MainActivity.kt`에서 7단계의 `else { ... }` 안에 있던 Toast 한 줄을 지우고 세 줄을 넣는다.

```kotlin
                val intent = Intent(this, ControlActivity::class.java)
                intent.putExtra("name", name)
                startActivity(intent)
```

`Intent`가 빨간색이면 **Alt+Enter**로 import한다(`android.content.Intent`).
실행해서 이름을 넣고 [연결]을 누르면 `Hello World!`가 있는 새 화면(ControlActivity)이 열리고, 기기의 뒤로 가기(◀)로 돌아오면 성공이다.

| 줄 | 뜻 |
|---|---|
| `Intent(this, ControlActivity::class.java)` | "이 화면(`this`)에서 `ControlActivity`로" 가겠다는 명시적 Intent. `::class.java`까지가 한 덩어리다 |
| `intent.putExtra("name", name)` | 이름표 `"name"`에 값을 넣어 함께 보낸다 |
| `startActivity(intent)` | 다음 화면을 연다 |

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. [연결] 버튼: 이름이 비면 Toast, 아니면 제어 화면으로 이름을 들고 이동한다.
        binding.connectButton.setOnClickListener {
            val name = binding.deviceNameEdit.text.toString()
            if (name.isEmpty()) {
                Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
            } else {
                val intent = Intent(this, ControlActivity::class.java)
                intent.putExtra("name", name)
                startActivity(intent)
            }
        }

        // 2. 자동 연결 Switch: 켜고 끌 때마다 알린다.
        binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "자동 연결 꺼짐", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
```

`activity_main.xml`은 1일차 그대로다.

### 13. 제어 화면 배치하기

1. `strings.xml`에 다섯 줄을 추가한다. 전체는 아래와 같다. 같은 코드가 [examples/day2/strings.xml](examples/day2/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_name_hint">장치 이름</string>
    <string name="auto_connect">자동 연결</string>
    <string name="connect">연결</string>
    <string name="device_unknown">장치: ?</string>
    <string name="pin_hint">핀 번호</string>
    <string name="led">LED</string>
    <string name="log_title">명령 로그</string>
    <string name="back">뒤로</string>
</resources>
```

2. `app › res › layout › activity_control.xml`을 열고(그림 화면이면 **Code**) 내용을 **모두 지우고** 아래 코드를 넣는다.
같은 코드가 [examples/day2/activity_control.xml](examples/day2/activity_control.xml)에 있다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center_horizontal"
    android:orientation="vertical">

    <TextView
        android:id="@+id/deviceText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="@string/device_unknown"
        android:textSize="24sp"
        android:textStyle="bold" />

    <EditText
        android:id="@+id/pinEdit"
        android:layout_width="160dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:hint="@string/pin_hint"
        android:inputType="number" />

    <Switch
        android:id="@+id/ledSwitch"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/led" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="@string/log_title"
        android:textSize="16sp" />

    <TextView
        android:id="@+id/logText"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="8dp"
        android:textSize="18sp" />

    <Button
        android:id="@+id/backButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="24dp"
        android:text="@string/back" />

</LinearLayout>
```

실행해서 [연결]로 넘어가면 위에 `장치: ?`, 그 아래 `핀 번호` 입력칸, `LED` 스위치, `명령 로그`, 맨 아래 `뒤로` 버튼이 보인다.

- `android:inputType="number"`: 숫자 키패드만 뜬다. 글자를 넣을 수 없다.
- `android:gravity="center_horizontal"`: 가로로만 가운데. 세로는 위에서부터 쌓는다.
- 로그 TextView의 `layout_height="0dp"` + `layout_weight="1"`: 남는 세로 공간을 로그가 다 쓴다. 그래서 [뒤로]가 맨 아래에 붙는다.
- `장치: ?`는 코드가 바꾸기 전의 처음 글자다. 2주차의 `이름: ?`와 같은 방식이다.

### 14. 이름 받아 표시하고 로그 쌓기

`ControlActivity.kt`를 4단계와 같은 방법으로 ViewBinding 틀로 바꾼다. 클래스 이름은 `ActivityControlBinding`이다.
그다음 `onCreate()` 마지막 `}` 바로 위에 세 부분을 넣는다. 완성한 전체는 아래와 같다.
같은 코드가 [examples/day2/ControlActivity.kt](examples/day2/ControlActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityControlBinding

class ControlActivity : AppCompatActivity() {
    // ViewBinding 틀: activity_control.xml → ActivityControlBinding
    private lateinit var binding: ActivityControlBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityControlBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // 1. 연결 화면이 보낸 장치 이름을 꺼내 상단에 보여 준다.
        val name = intent.getStringExtra("name") ?: ""
        binding.deviceText.text = "장치: $name"

        // 2. LED Switch: 켜면 on, 끄면 off 명령을 로그에 쌓는다.
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "핀 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                binding.logText.append("on $pin\n")
            } else {
                binding.logText.append("off $pin\n")
            }
        }

        // 3. [뒤로] 버튼: 이 화면을 닫고 연결 화면으로 돌아간다.
        binding.backButton.setOnClickListener {
            finish()
        }
    }
}
```

`ActivityControlBinding`·`Toast`가 빨간색이면 **Alt+Enter**로 import한다.

- `intent.getStringExtra("name") ?: ""`: 연결 화면이 `putExtra("name", …)`로 넣은 값을 꺼낸다. 값이 없으면 `null`이므로 3주차의 `?:`로 `""`을 쓴다. `"name"` 철자가 넣는 쪽과 같아야 한다.
- `binding.logText.append("on $pin\n")`: `.text = `는 글자를 통째로 바꾸지만 `append`는 뒤에 덧붙인다. `\n`은 줄바꿈이다.
- `else if`: `if`가 아니면서 또 다른 조건일 때. `if/else`를 이어 붙인 것이다.
- `finish()`: 이 화면을 닫는다. 뒤로 가기(◀)와 같은 일이 일어난다.

### 15. 두 화면 오가며 확인하기

| 할 일 | 보이는 것 |
|---|---|
| 연결 화면에 `ESP32_BLE_1` 입력 → [연결] | 제어 화면 위에 `장치: ESP32_BLE_1` |
| 핀 번호를 비운 채 LED 스위치 켜기 | Toast `핀 번호를 입력하세요`. 스위치는 켜진 채로 남는다 |
| 스위치를 다시 끄고, 핀 번호에 `3` 입력 → 스위치 켜기 | 로그에 `on 3` |
| 스위치 끄기 → 다시 켜기 | 로그에 `off 3`, `on 3`이 아래로 쌓인다 |
| [뒤로] | 연결 화면으로 돌아온다. 입력했던 이름이 그대로 있다 |
| 다시 [연결] | 제어 화면이 **새로** 열린다. 로그는 비어 있다 |

### 16. 제출하기

로그에 `on 3`·`off 3`이 쌓인 제어 화면을 캡처한다. 제출물은 네 가지다.

1. `MainActivity.kt`
2. `ControlActivity.kt`
3. 캡처 1: 연결 화면에 장치 이름을 입력한 화면
4. 캡처 2: 제어 화면 상단에 그 이름이 보이고 로그가 쌓인 화면

파일은 Project 창에서 오른쪽 클릭 → **Open In › Finder**(Windows는 **Explorer**)로 찾는다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
한 곳을 고친 다음 다시 실행하고, 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 요청한다.
