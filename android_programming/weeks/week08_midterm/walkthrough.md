# 8주차 따라하기 — 리허설 앱 Rehearsal과 제출 연습

이번 주는 `SmartIO`를 이어 쓰지 않고 작은 새 프로젝트 `Rehearsal`을 만든다. 7주차 2일차 `ConnViewModel`·`MainActivity`와 같은 모양을 버튼 두 개짜리 화면으로 줄인 것이다.
처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다. 리허설을 혼자 먼저 풀어 봤다면 막힌 단계만 연다.

1~4단계는 시험 당일 강의자가 끝내서 나눠 주는 부분(starter)이다. 시험에서 직접 하는 일은 5단계부터다.
새로 배우는 문법은 없다. 막히면 7주차 [ConnViewModel.kt](../week07_flow_ui_state/examples/day2/ConnViewModel.kt)·[MainActivity.kt](../week07_flow_ui_state/examples/day2/MainActivity.kt)와 비교한다.

## 1일차

### 1. 새 프로젝트 만들기

1. Android Studio에서 **File › New › New Project**를 누른다.
2. **Phone and Tablet**에서 **Empty Views Activity**를 고르고 **Next**를 누른다.
3. 아래처럼 입력하고 **Finish**를 누른다.

| 항목 | 입력 |
|---|---|
| Name | `Rehearsal` |
| Package name | `com.example.rehearsal` (Name을 쓰면 자동으로 채워진다) |
| Save location | 기본값 또는 강의자가 안내한 폴더 |
| Language | `Kotlin` |
| Minimum SDK | 수업 공지 값 |
| Build configuration language | 기본값 |

4. 창 아래쪽 진행 표시가 모두 끝나면 `Run ▶`을 누른다. `Hello World!`가 보이면 성공이다.

### 2. build.gradle.kts에 ViewBinding과 라이브러리 넣기

4주차 3단계와 같다. `Gradle Scripts › build.gradle.kts (Module :app)`을 열고 두 곳을 고친다.

1. `android { ... }` 블록 안, `defaultConfig { ... }` 블록이 끝난 다음 줄에 아래를 넣는다.

```kotlin
    buildFeatures {
        viewBinding = true
    }
```

2. 파일 아래쪽 `dependencies { ... }` 블록 안, 마지막 `}` 바로 위에 네 줄을 넣는다. 4주차에 SmartIO에 미리 넣었던 줄이다.

```kotlin
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
```

3. 편집기 위쪽의 **Sync Now**를 누르고 아래쪽 진행 표시가 끝날 때까지 기다린다.

내 파일은 템플릿이 만든 줄이 더 있어서 모양이 다를 수 있다. 위 두 가지만 들어 있으면 된다.
검증에 쓴 전체 파일은 [examples/rehearsal_starter/build.gradle.kts](examples/rehearsal_starter/build.gradle.kts)이며 아래와 같다.

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.rehearsal"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.rehearsal"
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
    // 5~7주에 쓴 라이브러리(ViewModel·코루틴·StateFlow). 4주 SmartIO와 같다. 이미 들어 있다.
    implementation("androidx.activity:activity-ktx:1.9.3")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
}
```

### 3. 화면 XML과 글자 넣기

1. `app › res › values › strings.xml`을 열고 전체를 아래로 바꾼다. 같은 코드가 [examples/rehearsal_starter/strings.xml](examples/rehearsal_starter/strings.xml)에 있다.

```xml
<resources>
    <string name="app_name">Rehearsal</string>
    <string name="state_idle">대기 중</string>
    <string name="time_idle">남은 초: 0</string>
    <string name="start">시작</string>
    <string name="cancel">취소</string>
</resources>
```

2. `app › res › layout › activity_main.xml`을 열고 오른쪽 위 **Code** 보기로 바꾼 뒤 전체를 아래로 바꾼다. 같은 코드가 [examples/rehearsal_starter/activity_main.xml](examples/rehearsal_starter/activity_main.xml)에 있다.

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

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="@string/state_idle"
        android:textSize="24sp" />

    <TextView
        android:id="@+id/timeText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/time_idle"
        android:textSize="18sp" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/startButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/start" />

        <Button
            android:id="@+id/cancelButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/cancel" />

    </LinearLayout>

</LinearLayout>
```

| View | id | 처음 글자 |
|---|---|---|
| 상태 `TextView` | `stateText` | `대기 중` |
| 남은 시간 `TextView` | `timeText` | `남은 초: 0` |
| 버튼 | `startButton` | `시작` |
| 버튼 | `cancelButton` | `취소` (`android:enabled="false"`라 처음에는 회색) |

맨 바깥 `LinearLayout`의 id `main`은 `MainActivity`의 insets 틀이 쓰므로 지우지 않는다.

3. 아래 두 파일은 새 프로젝트가 만든 그대로 둔다. 이름만 확인한다.

`AndroidManifest.xml` — [examples/rehearsal_starter/AndroidManifest.xml](examples/rehearsal_starter/AndroidManifest.xml). 내 파일에는 아이콘 등의 줄이 더 있다. `.MainActivity`와 `@style/Theme.Rehearsal` 두 곳만 본다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:label="@string/app_name"
        android:theme="@style/Theme.Rehearsal">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
```

`res/values/themes.xml` — [examples/rehearsal_starter/res/values/themes.xml](examples/rehearsal_starter/res/values/themes.xml). `Theme.Rehearsal` 이름이 Manifest와 같아야 한다.

```xml
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Base.Theme.Rehearsal" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your light theme here. -->
        <!-- <item name="colorPrimary">@color/my_light_primary</item> -->
    </style>

    <style name="Theme.Rehearsal" parent="Base.Theme.Rehearsal" />
</resources>
```

### 4. starter 코드 넣고 실행하기

1. `app › kotlin+java › com.example.rehearsal › MainActivity.kt`를 열고 전체를 아래로 바꾼다. 같은 코드가 [examples/rehearsal_starter/MainActivity.kt](examples/rehearsal_starter/MainActivity.kt)에 있다.
   `RehearsalViewModel`이 빨간색인 것은 아직 파일이 없어서다. 2번을 하면 사라진다.

```kotlin
package com.example.rehearsal

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.rehearsal.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 8주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: RehearsalViewModel by viewModels()

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

        // 1. [시작] 버튼: 카운트다운은 ViewModel에 맡긴다(8주차 1일차).
        binding.startButton.setOnClickListener {
            // TODO(3) ViewModel의 카운트다운 시작 함수를 부른다.
        }

        // 2. [취소] 버튼: 카운트다운 코루틴을 취소한다(8주차 1일차).
        binding.cancelButton.setOnClickListener {
            // TODO(3) ViewModel의 취소 함수를 부른다.
        }

        // 3. 상태를 받아 문구와 버튼을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(8주차 1일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    // TODO(4) 받은 state를 stateText에 넣는다.
                    //         state가 "카운트다운 중"이면 [시작]은 끄고 [취소]는 켠다. 아니면 반대로 한다(isEnabled).
                }
            }
        }

        // 4. 남은 초를 받아 보여 준다. 3번과 같은 틀을 하나 더 쓴다(8주차 1일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    // TODO(5) 받은 seconds를 "남은 초: 3"처럼 timeText에 넣는다.
                }
            }
        }
    }
}
```

2. Project 창에서 `com.example.rehearsal` 폴더를 우클릭 › **New › Kotlin Class/File**을 누르고, 목록에서 **Class**를 고른 뒤 이름 `RehearsalViewModel`을 입력하고 Enter를 누른다.
   생긴 파일의 내용을 모두 지우고 아래로 바꾼다. 같은 코드가 [examples/rehearsal_starter/RehearsalViewModel.kt](examples/rehearsal_starter/RehearsalViewModel.kt)에 있다.

```kotlin
package com.example.rehearsal

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// 8주차 1일차: 리허설 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class RehearsalViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 상태 문구와 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(8주차 1일차).
    private val _state = MutableStateFlow("대기 중")
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds

    // 2. [시작]이 시작한 코루틴. [취소]에서 멈추려고 보관한다. 아직 없으면 null이다(8주차 1일차).
    private var job: Job? = null

    // 3. [시작]: 카운트다운 중으로 바꾸고 5초를 센 뒤 완료로 바꾼다(8주차 1일차).
    fun startCountdown() {
        // TODO(1) job이 이미 돌고 있으면(isActive) 그냥 돌아간다.
        //         아니면 viewModelScope.launch로 코루틴을 시작하고 그 Job을 job에 보관한다. 코루틴 안에서는
        //         _state를 "카운트다운 중"으로 바꾸고, 5부터 1까지 _seconds에 넣으며 1초씩 기다린 뒤,
        //         _seconds를 0, _state를 "완료"로 바꾼다. Log.d("Rehearsal", …)로 남은 초를 찍어도 좋다.
    }

    // 4. [취소]: 카운트다운 코루틴을 멈추고 취소됨으로 바꾼다. 남은 초는 멈춘 숫자 그대로 둔다(8주차 1일차).
    fun cancelCountdown() {
        // TODO(2) 보관한 job을 취소하고 _state를 "취소됨"으로 바꾼다. job은 null일 수 있다.
    }
}
```

import는 두 파일에 모두 들어 있다. 붙여 넣은 뒤에도 빨간 글자가 남으면 그 글자에 커서를 두고 **Alt+Enter**(맥 ⌥+Enter) → **Import**를 고른다. `ActivityMainBinding`이 빨간색이면 2단계의 `viewBinding = true`와 **Sync Now**를 다시 확인한다.

3. `Run ▶`을 누른다. 아래 화면이 뜨면 starter가 준비된 것이다.

```text
Rehearsal
대기 중
남은 초: 0
[시작] [취소]        ← [취소]는 회색
```

[시작]을 눌러도 아무 일도 없고, 회전해도 같다. **빌드·실행은 되고 기능만 비어 있다**가 starter 확인 기준이다. 시험 당일 받는 starter도 먼저 이렇게 확인한다.

### 5. TODO 다섯 곳 찾기

메뉴 **View › Tool Windows › TODO**를 열면 TODO가 모여 보인다. 줄을 더블클릭하면 그 자리로 간다.

| TODO | 파일 | 자리 | 할 일 |
|---|---|---|---|
| (1) | `RehearsalViewModel.kt` | `fun startCountdown() {` 안 | 막음, 코루틴 시작·보관, 5→1 카운트다운, 완료 |
| (2) | `RehearsalViewModel.kt` | `fun cancelCountdown() {` 안 | 코루틴 취소, 취소됨 |
| (3) | `MainActivity.kt` | 1번 [시작]·2번 [취소] 리스너 안 | ViewModel 함수 부르기 |
| (4) | `MainActivity.kt` | 3번 틀의 `viewModel.state.collect { state ->` 안 | 상태 글자, 버튼 켜기·끄기 |
| (5) | `MainActivity.kt` | 4번 틀의 `viewModel.seconds.collect { seconds ->` 안 | 남은 초 글자 |

**값을 만드는 쪽(1·2) → 받는 쪽(3·4·5)** 순서로 채운다. 이미 들어 있는 `_state`·`state`·`_seconds`·`seconds`·`job` 선언과 `repeatOnLifecycle` 틀은 고치지 않는다.

### 6. TODO(1) — startCountdown() 채우기

`RehearsalViewModel.kt`의 `fun startCountdown() {` 아래에서 `// TODO(1)`로 시작하는 **주석 네 줄**을 지우고, 그 자리에 아래를 넣는다.

```kotlin
        // 이미 돌고 있으면 새로 시작하지 않는다.
        if (job?.isActive == true) {
            return
        }
        job = viewModelScope.launch {
            _state.value = "카운트다운 중"
            for (i in 5 downTo 1) {
                Log.d("Rehearsal", "남은 초: $i")
                _seconds.value = i
                delay(1000)
            }
            _seconds.value = 0
            _state.value = "완료"
            Log.d("Rehearsal", "완료")
        }
```

- `if (job?.isActive == true) { return }`: 이미 돌고 있으면 새로 시작하지 않는다. 7주차 `startScan()`의 막음과 같다.
- `job = viewModelScope.launch {`: 코루틴을 시작하고 `Job`을 보관한다. 보관해야 7단계의 [취소]가 멈출 수 있다.
- `for (i in 5 downTo 1)`과 `delay(1000)`은 6주차 그대로다. 숫자는 View가 아니라 `_seconds.value`에 넣는다.
- `Log.d("Rehearsal", …)`는 화면이 아직 안 바뀌어도 코루틴이 도는지 Logcat으로 보려고 넣는다.

메뉴 **Build › Make Project**를 눌러 빌드만 확인한다. 아직 화면은 바뀌지 않는다. 이 함수를 부르는 버튼이 비어 있기 때문이다.

### 7. TODO(2) — cancelCountdown() 채우기

`fun cancelCountdown() {` 아래의 `// TODO(2)` 주석 한 줄을 지우고 그 자리에 넣는다.

```kotlin
        job?.cancel()
        _state.value = "취소됨"
        Log.d("Rehearsal", "취소됨")
```

- `job?.cancel()`: 아직 [시작]을 안 눌렀으면 `job`이 `null`이다. 3주차 `?.`로 안전하게 부른다.
- `_seconds`는 건드리지 않는다. 멈춘 숫자가 화면에 남아 취소가 실제로 됐는지 볼 수 있다(7주차 `stopScan()`은 0으로 되돌렸다).

### 8. TODO(3) — 버튼에서 ViewModel 부르기

`MainActivity.kt`의 두 리스너 안에서 `// TODO(3)` 주석을 지우고 한 줄씩 넣는다.

```kotlin
        binding.startButton.setOnClickListener {
            viewModel.startCountdown()
        }
```

```kotlin
        binding.cancelButton.setOnClickListener {
            viewModel.cancelCountdown()
        }
```

실행하고 [시작]을 누른다. 아래쪽 **Logcat** 창의 필터에 `package:mine tag:Rehearsal`을 넣으면 1초마다 `남은 초: 5` … `남은 초: 1`, 그다음 `완료`가 찍힌다.
그런데 화면은 `대기 중` / `남은 초: 0` 그대로다. ViewModel의 값은 바뀌었지만 **받는 쪽(`collect`)이 비어 있기** 때문이다.

### 9. TODO(4) — 상태를 받아 글자와 버튼 바꾸기

3번 틀에서 `viewModel.state.collect { state ->` 아래의 `// TODO(4)` 주석 두 줄을 지우고 그 자리에 넣는다. 아래는 `collect { state ->` 줄부터 짝 `}`까지다. 그 사이 아홉 줄이 넣을 줄이다.

```kotlin
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 카운트다운 중에는 [취소]만, 그 밖에는 [시작]만 켠다.
                    if (state == "카운트다운 중") {
                        binding.startButton.isEnabled = false
                        binding.cancelButton.isEnabled = true
                    } else {
                        binding.startButton.isEnabled = true
                        binding.cancelButton.isEnabled = false
                    }
                }
```

- `binding.stateText.text = state`: ViewModel이 `_state`에 넣은 글자가 그대로 온다.
- `"카운트다운 중"`은 ViewModel 31행의 글자를 **복사해 붙인다**. 띄어쓰기가 하나라도 다르면 빌드는 되는데 [취소]가 켜지지 않는다.
- 상태가 넷이지만 버튼 규칙은 둘뿐이라 `if/else` 한 번이면 된다. 7주차처럼 `when`을 써도 된다.

실행하고 [시작]을 누른다. `카운트다운 중`이 되고 [시작]은 회색, [취소]는 켜진다. 5초 뒤 `완료`가 되고 [시작]이 다시 켜진다. 남은 초 글자는 아직 `남은 초: 0` 그대로다.

### 10. TODO(5) — 남은 초 받기

4번 틀에서 `viewModel.seconds.collect { seconds ->` 아래의 `// TODO(5)` 주석을 지우고 한 줄을 넣는다.

```kotlin
                viewModel.seconds.collect { seconds ->
                    binding.timeText.text = "남은 초: $seconds"
                }
```

`"$seconds초"`처럼 `$seconds` 바로 뒤에 한글을 붙이면 Kotlin이 `seconds초`를 한 이름으로 읽어 `Unresolved reference 'seconds초'.` 오류가 난다. 그래서 단위를 앞(`남은 초: `)에 두었다.

실행하고 [시작]을 누른다. `남은 초: 5`부터 1초마다 줄어들고 5초 뒤 `완료` / `남은 초: 0`이 되면 성공이다.

완성한 `RehearsalViewModel.kt` 전체는 아래와 같다. 같은 코드가 [examples/rehearsal_solution/RehearsalViewModel.kt](examples/rehearsal_solution/RehearsalViewModel.kt)에 있다.

```kotlin
package com.example.rehearsal

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

// 8주차 1일차: 리허설 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class RehearsalViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 상태 문구와 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(8주차 1일차).
    private val _state = MutableStateFlow("대기 중")
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds

    // 2. [시작]이 시작한 코루틴. [취소]에서 멈추려고 보관한다. 아직 없으면 null이다(8주차 1일차).
    private var job: Job? = null

    // 3. [시작]: 카운트다운 중으로 바꾸고 5초를 센 뒤 완료로 바꾼다(8주차 1일차).
    fun startCountdown() {
        // 이미 돌고 있으면 새로 시작하지 않는다.
        if (job?.isActive == true) {
            return
        }
        job = viewModelScope.launch {
            _state.value = "카운트다운 중"
            for (i in 5 downTo 1) {
                Log.d("Rehearsal", "남은 초: $i")
                _seconds.value = i
                delay(1000)
            }
            _seconds.value = 0
            _state.value = "완료"
            Log.d("Rehearsal", "완료")
        }
    }

    // 4. [취소]: 카운트다운 코루틴을 멈추고 취소됨으로 바꾼다. 남은 초는 멈춘 숫자 그대로 둔다(8주차 1일차).
    fun cancelCountdown() {
        job?.cancel()
        _state.value = "취소됨"
        Log.d("Rehearsal", "취소됨")
    }
}
```

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/rehearsal_solution/MainActivity.kt](examples/rehearsal_solution/MainActivity.kt)에 있다.

```kotlin
package com.example.rehearsal

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.rehearsal.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 8주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: RehearsalViewModel by viewModels()

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

        // 1. [시작] 버튼: 카운트다운은 ViewModel에 맡긴다(8주차 1일차).
        binding.startButton.setOnClickListener {
            viewModel.startCountdown()
        }

        // 2. [취소] 버튼: 카운트다운 코루틴을 취소한다(8주차 1일차).
        binding.cancelButton.setOnClickListener {
            viewModel.cancelCountdown()
        }

        // 3. 상태를 받아 문구와 버튼을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(8주차 1일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 카운트다운 중에는 [취소]만, 그 밖에는 [시작]만 켠다.
                    if (state == "카운트다운 중") {
                        binding.startButton.isEnabled = false
                        binding.cancelButton.isEnabled = true
                    } else {
                        binding.startButton.isEnabled = true
                        binding.cancelButton.isEnabled = false
                    }
                }
            }
        }

        // 4. 남은 초를 받아 보여 준다. 3번과 같은 틀을 하나 더 쓴다(8주차 1일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    binding.timeText.text = "남은 초: $seconds"
                }
            }
        }
    }
}
```

`build.gradle.kts`, `AndroidManifest.xml`, `activity_main.xml`, `strings.xml`, `themes.xml`은 starter와 완성본이 글자 단위로 같다.

### 11. 점검표로 확인하기

저장(Ctrl+S, 맥 ⌘+S)하고 `Run ▶`으로 다시 실행한다. 위에서부터 차례로 해 본다. 회전은 에뮬레이터 창 옆 도구 막대의 회전 버튼으로 한다.

| 조작 | `stateText` | `timeText` | [시작] | [취소] | Logcat `tag:Rehearsal` |
|---|---|---|---|---|---|
| 앱 시작 | `대기 중` | `남은 초: 0` | 켬 | 끔 | 없음 |
| [시작] | `카운트다운 중` | `남은 초: 5` → 1초마다 `4`·`3`·`2`·`1` | 끔 | 켬 | `남은 초: 5` … `남은 초: 1` |
| 5초 뒤 | `완료` | `남은 초: 0` | 켬 | 끔 | `완료` |
| 카운트다운 중(예: 3) [취소] | `취소됨` | `남은 초: 3`(멈춘 숫자 그대로) | 켬 | 끔 | `취소됨`. 그 뒤 `남은 초` 줄이 더 없다 |
| `완료`·`취소됨`에서 [시작] | `카운트다운 중` | `남은 초: 5`부터 | 끔 | 켬 | `남은 초: 5`부터 |
| `남은 초: 3`에서 회전 | `카운트다운 중` | `남은 초: 3` → 1초 뒤 `2` | 끔 | 켬 | 끊기지 않고 두 번씩 찍히지 않는다 |
| `완료`·`취소됨`에서 회전 | 그대로 | 그대로 | 켬 | 끔 | 새 줄 없음 |

- 홈으로 나갔다가 돌아와도 같다. 나가 있는 동안 카운트다운이 끝났으면 돌아온 화면은 `완료` / `남은 초: 0`이다.
- 뒤로 가기로 앱을 닫고 다시 열면 `대기 중`이다. ViewModel도 함께 정리되기 때문이다.

### 12. 캡처하고 자기 채점하기

자기 점검용으로 세 장을 찍는다(제출하지 않는다).

1. `남은 초: 3`(또는 2)일 때 회전한 가로 화면 — `카운트다운 중`, [시작] 회색·[취소] 켬
2. [취소] 뒤 화면 — `취소됨` / 멈춘 숫자, [시작] 켬·[취소] 회색
3. `완료` / `남은 초: 0` 화면

[채점표](rubric.md)로 20점 중 몇 점인지 매기고, 점수를 잃은 항목이 있으면 10단계의 완성 코드와 한 줄씩 비교한다.

## 2일차

### 13. 시험 전 PC 점검

2일차 설명 시간(22–27분)에 모두 함께 한다. 목적은 코드가 아니라 **PC·에뮬레이터·Gradle이 시험 전에 제대로 도는지** 확인하는 것이다.

1. Android Studio에서 1일차 `Rehearsal` 프로젝트를 연다. 목록에 없으면 **File › Open**으로 프로젝트 폴더를 고른다.
2. 아래쪽 진행 표시(Gradle Sync)가 끝날 때까지 기다린다.
3. `Run ▶`을 누른다. 1일차에 완성했다면 완성 화면이, 못 했다면 starter 화면이 뜬다. 어느 쪽이든 앱이 뜨면 된다.
4. Logcat 창을 열어 둔다.

| 확인 | 됨 |
|---|---|
| Gradle Sync가 오류 없이 끝났다 | ☐ |
| 에뮬레이터가 켜져 있다 | ☐ |
| `Run ▶`으로 앱이 떴다 | ☐ |
| Logcat 창이 보인다 | ☐ |

하나라도 안 되면 바로 손을 든다. 시험 시작 전에 자리를 옮기는 것이 가장 빠르다. 에뮬레이터는 끄지 않고 시험을 시작한다.

### 14. 본시험 starter 열기

시험 시작 뒤 0–5분에 한다.

1. 강의자가 배포한 starter 폴더를 받는다. 압축 파일이면 먼저 푼다.
2. **File › Open**을 누르고, 안에 `settings.gradle.kts`가 들어 있는 폴더를 고른다. 프로젝트를 믿겠느냐고 물으면 **Trust Project**를 누른다.
3. Gradle Sync가 끝나면 `Run ▶`을 누르고 첫 화면이 뜨는지 본다. 뜨지 않으면 코드를 고치기 전에 손을 든다.
4. **View › Tool Windows › TODO**로 TODO 목록을 열고, 문항지와 함께 읽는다.

package·파일 이름·문구는 문항지와 starter를 따른다. 리허설과 다른 곳에 밑줄을 긋는다.

### 15. 저장하고 다시 실행하기

40–55분에 한다. 마지막으로 코드를 고친 뒤에도 한 번 더 한다.

1. **Ctrl+S**(맥 ⌘+S)로 저장한다.
2. `Run ▶`을 누른다. 앱이 처음 화면부터 다시 뜨는지 본다.
3. 11단계와 같은 점검표를 한 바퀴 돈다. 문항에 실패가 있으면 실패 화면이 나올 때까지 몇 번 반복한다.

채점자는 제출한 파일을 starter에 넣어 실행한다. 다시 실행해서 확인하지 않은 코드는 채점 때 처음 실행되는 코드다.

### 16. 제출할 파일 찾기와 캡처

55–60분에 한다. 리허설에서는 올리지 않고 파일 위치만 찾아본다.

1. Project 창에서 `MainActivity.kt`를 우클릭 › **Open In › Explorer**(맥 **Finder**)를 누른다. `app/src/main/java/com/example/rehearsal/` 폴더가 열리고 `MainActivity.kt`와 `RehearsalViewModel.kt`가 보인다.
2. 캡처는 에뮬레이터 창 도구 막대의 카메라 모양 버튼(**Take Screenshot**)으로 찍는다. 저장된 위치를 확인해 둔다.
3. 본시험에서는 두 파일과 캡처를 시험 공지의 LMS 제출 칸에 올린다. 파일 이름은 바꾸지 않는다.

### 17. 제출 전 마지막 확인

- [ ] 마지막으로 고친 뒤 저장하고 다시 실행했다.
- [ ] 빨간 줄이 남은 파일이 없다(끝내지 못한 줄은 앞에 `//`를 붙였다).
- [ ] 올린 파일이 `MainActivity.kt`와 `○○ViewModel.kt` 두 개다. 다른 프로젝트의 같은 이름 파일이 아니다.
- [ ] 캡처에 문항이 지정한 화면이 보이고, 계정·알림 같은 개인정보가 보이지 않는다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 확인할 곳은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
빌드는 되는데 화면이 점검표와 다르면 같은 표의 "빌드는 되는데" 줄을 본다.
