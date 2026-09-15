# 7주차 따라하기 — ViewModel과 StateFlow로 회전해도 남는 연결 화면

6주차 `SmartIO` 프로젝트를 그대로 이어서 쓴다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면이나 Logcat에 보이면 다음 단계로 넘어간다.
6주차 프로젝트가 없거나 실행되지 않으면 강의자에게 6주차 완성본(`examples/day2`)을 받아 시작한다.

이번 주에 새로 만드는 파일은 `ConnViewModel.kt`(1일차)와 `ConnState.kt`(2일차)이고, 고치는 파일은 `MainActivity.kt`(1·2일차), `ConnViewModel.kt`·`activity_main.xml`·`strings.xml`(2일차)이다.
`ControlActivity.kt`, `activity_control.xml`, `AndroidManifest.xml`은 4주차에 만든 그대로 둔다. 전체 내용은 [8단계](#8-바꾸지-않는-파일-확인하기)에 있다.

Logcat은 필터 칸에 `package:mine tag:Conn`을 넣고 본다. 4단계에서 `MainActivity`가 ViewModel 함수를 부르기 시작하면 ViewModel이 이 태그로 문구를 남긴다.

## 1일차

### 1. 6주차 프로젝트 열고 회전해 보기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다. 연결 화면에 아래가 보이면 시작할 수 있다.

```text
Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지]
대기 중
[연결]
```

2. `app › res › layout › activity_main.xml`은 6주차 2일차에 완성한 그대로다. 아래와 같은지 확인한다. id 이름이 다르면 아래 파일로 바꾼다.
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

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/scanButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/scan" />

        <Button
            android:id="@+id/stopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/stop" />

    </LinearLayout>

    <ProgressBar
        android:id="@+id/scanProgress"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:visibility="gone" />

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_idle"
        android:textSize="18sp" />

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />

</LinearLayout>
```

3. `app › res › values › strings.xml`도 6주차 그대로다. 같은 코드가 [examples/day1/strings.xml](examples/day1/strings.xml)에 있다.

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
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
    <string name="retry">다시 시도</string>
</resources>
```

4. 장치 이름을 넣고 [검색]을 누른 뒤 `검색 중… 3`쯤에서 화면을 돌린다. 에뮬레이터 도구 막대의 **회전** 버튼을 누른다. 화면이 안 돌면 빠른 설정에서 **자동 회전**을 켠다.
5. 다시 [검색]을 눌러 `연결 실패`와 [다시 시도]가 나올 때까지 기다린 뒤 화면을 돌린다. 실패가 안 나오면 [뒤로]로 돌아와 다시 누른다. 절반 확률이다.

| 회전한 때 | 회전 뒤 화면 |
|---|---|
| `검색 중… 3` | `대기 중`으로 돌아간다. ProgressBar가 사라지고, 연결도 시도하지 않는다 |
| `연결 실패`와 [다시 시도]가 보일 때 | `대기 중`으로 돌아가고 [다시 시도]가 사라진다 |

3주차에 본 것처럼 회전하면 `onDestroy` 다음에 `onCreate`가 불려 **Activity가 새로 만들어진다.** 새 화면은 XML 처음 모양으로 그려지고,
6주차 `lifecycleScope`에서 돌던 코루틴은 옛 화면과 함께 취소된다. 오늘은 코루틴과 마지막 문구를 화면보다 오래 사는 **ViewModel**로 옮긴다.

### 2. ConnViewModel 클래스 만들기

1. Project 창에서 `app › kotlin+java › com.example.smartio`를 오른쪽 클릭 → **New › Kotlin Class/File**을 고른다.
2. 목록에서 **Class**를 고르고 이름에 `ConnViewModel`을 넣은 뒤 Enter를 누른다. `ConnViewModel.kt`가 열리고 `package` 줄 아래에 `class ConnViewModel {`와 `}` 두 줄이 생긴다.
3. `class ConnViewModel {` 한 줄을 지우고 그 자리에 아래를 넣는다. 클래스의 마지막 `}`는 그대로 둔다.

```kotlin
// 7주차 1일차: 연결 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class ConnViewModel : ViewModel() {
    // 1. 마지막으로 알린 문구. 회전 뒤 새 화면이 onCreate에서 다시 읽는다(7주차 1일차).
    var resultText = "대기 중"

    // 2. 문구가 바뀔 때 부를 화면 쪽 코드. 화면이 onCreate에서 넣고 onDestroy에서 null로 비운다(7주차 1일차).
    //    ViewModel은 화면보다 오래 살므로, 없어진 화면을 붙잡지 않게 반드시 비운다.
    var listener: ((String) -> Unit)? = null

    // 3. [검색]·[다시 시도]가 시작한 코루틴. 6주차에는 MainActivity에 있던 변수다(7주차 1일차).
    private var scanJob: Job? = null
```

4. 빨간 글자를 차례로 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 가져온다.

| 빨간 글자 | 가져올 import |
|---|---|
| `ViewModel` | `androidx.lifecycle.ViewModel` |
| `Job` | `kotlinx.coroutines.Job` |

5. 실행한다. 아직 아무 곳에서도 `ConnViewModel`을 쓰지 않으므로 화면은 1단계와 같다.

- `class ConnViewModel : ViewModel()`: `ViewModel`을 물려받은 클래스다. 화면(Activity)보다 오래 살아서 회전해도 없어지지 않는다. `: ViewModel()`은 "이 틀을 물려받는다"는 뜻으로만 읽는다.
- `var resultText = "대기 중"`: 클래스 안에 둔 변수, 즉 **프로퍼티**다. 이 객체가 들고 있는 값이고, 밖에서는 `viewModel.resultText`처럼 점으로 읽는다(오늘 문법).
- `var listener: ((String) -> Unit)? = null`: 글자 하나를 받는 코드 덩어리를 넣어 두는 변수다. 처음에는 비어 있어서 `null`이다. 1일차에만 쓰는 틀이며 모양을 외우지 않아도 된다.
- `private var scanJob: Job? = null`: 6주차 `MainActivity`에 있던 변수를 이리로 옮겨 온다(`MainActivity`의 것은 4단계에서 지운다).

### 3. 코루틴과 가짜 연결을 ViewModel로 옮기기

1. `ConnViewModel` 안, `scanJob` 줄 아래에 [검색]·[중지]·[다시 시도]가 부를 함수 세 개를 넣는다.

```kotlin
    // 4. [검색]: 5초를 센 뒤 가짜 연결을 시도한다(7주차 1일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다. 회전한 새 화면에서는 [검색]이 다시 켜져 있기 때문이다.
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            for (i in 5 downTo 1) {
                show("검색 중… $i")
                delay(1000)
            }
            tryConnect()
        }
    }

    // 5. [중지]: 카운트다운 코루틴을 취소한다(7주차 1일차).
    fun stopScan() {
        scanJob?.cancel()
    }

    // 6. [다시 시도]: 카운트다운 없이 연결만 다시 시도한다(7주차 1일차).
    fun retry() {
        scanJob = viewModelScope.launch {
            tryConnect()
        }
    }
```

2. 그 아래에 문구를 알리는 함수를 넣는다.

```kotlin
    // 문구를 Logcat에 남기고 resultText에 보관한 뒤, 등록된 화면이 있으면 알린다. 없으면(null) 보관만 한다.
    private fun show(text: String) {
        Log.d("Conn", text)
        resultText = text
        listener?.invoke(text)
    }
```

3. `MainActivity.kt`의 `connectFake()` 함수를 위의 주석 줄까지 **복사**(Ctrl+C, 맥 ⌘+C)해 `show()` 아래에 붙인다. 6주차 코드와 글자까지 같다. `MainActivity`에 있는 원래 함수는 4단계에서 지운다.

```kotlin
    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }
```

4. 그 아래, 클래스의 마지막 `}` 위에 `tryConnect()`를 넣는다. 6주차와 달리 `binding`·`Intent`·`Toast`가 없고 `show(…)`만 부른다.

```kotlin
    // 가짜 연결을 시도하고 결과를 화면에 알린다.
    private suspend fun tryConnect() {
        show("연결 중…")
        var result = "연결됨"
        try {
            connectFake()
        } catch (e: Exception) {
            result = "연결 실패"
        }
        show(result)
    }
```

5. 빨간 글자를 Alt+Enter로 가져온다. `Random`은 6주차처럼 목록에서 **`kotlin.random.Random`**을 고른다.

| 빨간 글자 | 가져올 import |
|---|---|
| `viewModelScope` | `androidx.lifecycle.viewModelScope` |
| `launch` | `kotlinx.coroutines.launch` |
| `delay` | `kotlinx.coroutines.delay` |
| `Log` | `android.util.Log` |
| `withContext` | `kotlinx.coroutines.withContext` |
| `Dispatchers` | `kotlinx.coroutines.Dispatchers` |
| `Random` | `kotlin.random.Random` |

완성한 `ConnViewModel.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/ConnViewModel.kt](examples/day1/ConnViewModel.kt)에 있다.

```kotlin
package com.example.smartio

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

// 7주차 1일차: 연결 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class ConnViewModel : ViewModel() {
    // 1. 마지막으로 알린 문구. 회전 뒤 새 화면이 onCreate에서 다시 읽는다(7주차 1일차).
    var resultText = "대기 중"

    // 2. 문구가 바뀔 때 부를 화면 쪽 코드. 화면이 onCreate에서 넣고 onDestroy에서 null로 비운다(7주차 1일차).
    //    ViewModel은 화면보다 오래 살므로, 없어진 화면을 붙잡지 않게 반드시 비운다.
    var listener: ((String) -> Unit)? = null

    // 3. [검색]·[다시 시도]가 시작한 코루틴. 6주차에는 MainActivity에 있던 변수다(7주차 1일차).
    private var scanJob: Job? = null

    // 4. [검색]: 5초를 센 뒤 가짜 연결을 시도한다(7주차 1일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다. 회전한 새 화면에서는 [검색]이 다시 켜져 있기 때문이다.
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            for (i in 5 downTo 1) {
                show("검색 중… $i")
                delay(1000)
            }
            tryConnect()
        }
    }

    // 5. [중지]: 카운트다운 코루틴을 취소한다(7주차 1일차).
    fun stopScan() {
        scanJob?.cancel()
    }

    // 6. [다시 시도]: 카운트다운 없이 연결만 다시 시도한다(7주차 1일차).
    fun retry() {
        scanJob = viewModelScope.launch {
            tryConnect()
        }
    }

    // 문구를 Logcat에 남기고 resultText에 보관한 뒤, 등록된 화면이 있으면 알린다. 없으면(null) 보관만 한다.
    private fun show(text: String) {
        Log.d("Conn", text)
        resultText = text
        listener?.invoke(text)
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과를 화면에 알린다.
    private suspend fun tryConnect() {
        show("연결 중…")
        var result = "연결됨"
        try {
            connectFake()
        } catch (e: Exception) {
            result = "연결 실패"
        }
        show(result)
    }
}
```

6. 실행한다. 화면은 여전히 6주차와 같다. 다음 단계에서 `MainActivity`가 이 함수들을 부르게 바꾼다.

- `viewModelScope.launch { }`: 6주차 `lifecycleScope.launch { }`와 쓰는 법이 같다. 다른 점은 코루틴이 **ViewModel에 묶인다**는 것이다. 화면이 새로 만들어져도 계속 돌고, ViewModel이 정리될 때 함께 취소된다.
- `if (scanJob?.isActive == true) { return }`: 코루틴이 이미 돌고 있으면 함수를 여기서 끝낸다. 회전한 새 화면에서는 [검색]이 다시 켜져 있어서 한 번 더 누를 수 있기 때문이다. 이 줄은 틀로 둔다.
- `show(text)`: 문구를 Logcat에 남기고 `resultText`에 보관한 뒤, 등록된 화면이 있으면 `listener?.invoke(text)`로 알린다. 3주차 `?.`와 같아서 `listener`가 `null`이면 아무 일도 하지 않는다.
- ViewModel 안에서는 `binding`을 쓰지 않는다. ViewModel은 화면보다 오래 살기 때문에 화면을 모르게 두고, 글자를 View에 넣는 일은 `MainActivity`가 한다.
- `tryConnect()`에서 `show(result)`를 `try` 밖에 둔 것은, 알림을 받은 화면 쪽 코드에서 난 오류가 `연결 실패`로 잘못 잡히지 않게 하려는 것이다.

### 4. MainActivity에서 ViewModel 부르기

이 단계는 `MainActivity.kt` 안 다섯 곳을 바꾼다. 중간에 빨간 줄이 생겨도 5번까지 마친 뒤 실행한다.

1. 클래스 안, `private lateinit var binding` 아래의 `// 6주차 2일차: …` 주석과 `private var scanJob: Job? = null` 두 줄을 지우고 그 자리에 아래를 넣는다. `viewModels`가 빨간색이면 Alt+Enter로 `androidx.activity.viewModels`를 가져온다.

```kotlin
    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()
```

2. [검색] 리스너 안의 `scanJob = lifecycleScope.launch { … }` 블록(다섯 줄)을 지우고 `viewModel.startScan()` 한 줄로 바꾼다. 버튼·ProgressBar 네 줄은 그대로 둔다.

```kotlin
        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.retryButton.visibility = View.GONE
            binding.scanProgress.visibility = View.VISIBLE
            viewModel.startScan()
        }
```

3. [중지] 리스너의 첫 줄 `scanJob?.cancel()`을 `viewModel.stopScan()`으로 바꾼다.

```kotlin
        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }
```

4. [다시 시도] 리스너의 `lifecycleScope.launch { … }` 세 줄을 `viewModel.retry()` 한 줄로 바꾼다.

```kotlin
        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            binding.retryButton.visibility = View.GONE
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            viewModel.retry()
        }
```

5. `onCreate()` 아래에 있는 `countDown()`, `connectFake()`, `tryConnect()` 세 함수를 위의 주석 줄까지 모두 지운다. 이제 `ConnViewModel`에 있다.
   파일 위쪽에서 회색으로 바뀐 import 일곱 줄(`lifecycleScope`, `Dispatchers`, `Job`, `delay`, `launch`, `withContext`, `Random`)도 지운다.

6. 실행하고 장치 이름을 넣은 뒤 [검색]을 누른다. Logcat 필터는 `package:mine tag:Conn`이다.

| 보이는 곳 | 결과 |
|---|---|
| 화면 | [검색]이 꺼지고 [중지]가 켜지고 ProgressBar가 돈다. 그런데 글자는 **`대기 중` 그대로**이고, 7초가 지나도 바뀌지 않는다 |
| Logcat | `검색 중… 5` … `검색 중… 1`, `연결 중…`, 그리고 `연결됨` 또는 `연결 실패`가 차례로 찍힌다 |

ViewModel은 일을 하고 있지만 화면에 알릴 곳(`listener`)이 비어 있어서 보관만 한다. 다음 단계에서 화면이 알림을 받게 한다. 확인했으면 앱을 멈춘다(Stop ■).

### 5. 문구를 받는 코드 등록하고 풀기

1. `onCreate()`의 마지막 `}` **아래**, 클래스의 마지막 `}` **위**에 문구를 받아 화면을 고치는 함수를 넣는다. 6주차 `tryConnect()`에 있던 `Intent`·`Toast` 코드가 여기로 왔다.

```kotlin
    // 9. ViewModel이 알려 준 문구를 보여 주고, 문구에 맞게 버튼을 고친다(7주차 1일차).
    private fun showState(text: String) {
        binding.stateText.text = text
        if (text == "연결 중…") {
            binding.stopButton.isEnabled = false
        } else if (text == "연결됨") {
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        } else if (text == "연결 실패") {
            Toast.makeText(this, text, Toast.LENGTH_SHORT).show()
            binding.retryButton.visibility = View.VISIBLE
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
        }
    }
```

2. `onCreate()` 안, [다시 시도] 블록 아래에 등록 코드를 넣는다.

```kotlin
        // 6. ViewModel이 문구를 알려 줄 때 부를 코드를 등록한다. 회전으로 새 화면이 생기면 새 화면이 다시 등록한다(7주차 1일차).
        viewModel.listener = { text ->
            showState(text)
        }
```

3. `onCreate()`의 마지막 `}`와 1번에서 넣은 `showState()` 사이에 해제 코드를 넣는다.

```kotlin
    // 8. 화면이 없어질 때(회전 포함) 등록을 푼다. ViewModel이 없어진 옛 화면을 붙잡지 않게 한다(7주차 1일차).
    override fun onDestroy() {
        super.onDestroy()
        viewModel.listener = null
    }
```

`Intent`, `Toast`, `View`는 6주차에 이미 import했다. 빨간색이면 Alt+Enter로 가져온다.

4. 실행하고 [검색]을 누른다. 6주차와 같이 동작하면 성공이다.

| 결과 | 화면 |
|---|---|
| 카운트다운 | `검색 중… 5` → 1초마다 `4`·`3`·`2`·`1` → `연결 중…`([중지]가 꺼진다) |
| 성공 | `연결됨` → 제어 화면으로 넘어가고 위에 `장치: 이름`이 보인다 |
| 실패 | `연결 실패`, Toast `연결 실패`, [다시 시도]가 보이고 [검색]이 켜진다 |

- `viewModel.listener = { text -> showState(text) }`: 5주차 람다 모양이다. "문구가 오면 `showState(text)`를 불러 달라"는 코드를 ViewModel의 `listener` 변수에 넣는다.
- `override fun onDestroy()`: 3주차에 본 생명주기 콜백이다. 화면이 없어질 때 `listener`를 `null`로 비운다. ViewModel은 화면보다 오래 살기 때문에, 비우지 않으면 없어진 옛 화면을 붙잡게 된다.
- 회전하면 옛 화면 `onDestroy`(비우기) → 새 화면 `onCreate`(다시 등록)가 이어진다. 그래서 알림은 늘 **지금 보이는 화면**으로 간다.

### 6. 회전 뒤 남은 문구 다시 읽기

새 화면은 XML 처음 모양(`대기 중`)으로 그려진다. ViewModel에 남아 있는 마지막 문구를 `onCreate`에서 다시 읽어 넣는다.

1. `onCreate()` 안, 5단계 등록 코드 아래(`onCreate()`의 마지막 `}` 위)에 넣는다.

```kotlin
        // 7. 회전으로 새로 만들어진 화면: ViewModel에 남은 문구를 다시 읽어 보여 준다(7주차 1일차).
        binding.stateText.text = viewModel.resultText
        if (viewModel.resultText == "연결 실패") {
            binding.retryButton.visibility = View.VISIBLE
        }
```

2. 실행한다. `연결 실패`와 [다시 시도]가 나올 때까지 [검색]이나 [다시 시도]를 누르고, 나오면 화면을 돌린다. 회전한 뒤에도 `연결 실패`와 [다시 시도]가 그대로 보이면 성공이다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day1/MainActivity.kt](examples/day1/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.smartio.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()

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

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            binding.scanButton.isEnabled = false
            binding.stopButton.isEnabled = true
            binding.retryButton.visibility = View.GONE
            binding.scanProgress.visibility = View.VISIBLE
            viewModel.startScan()
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.stopButton.isEnabled = false
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            binding.retryButton.visibility = View.GONE
            binding.scanButton.isEnabled = false
            binding.scanProgress.visibility = View.VISIBLE
            viewModel.retry()
        }

        // 6. ViewModel이 문구를 알려 줄 때 부를 코드를 등록한다. 회전으로 새 화면이 생기면 새 화면이 다시 등록한다(7주차 1일차).
        viewModel.listener = { text ->
            showState(text)
        }

        // 7. 회전으로 새로 만들어진 화면: ViewModel에 남은 문구를 다시 읽어 보여 준다(7주차 1일차).
        binding.stateText.text = viewModel.resultText
        if (viewModel.resultText == "연결 실패") {
            binding.retryButton.visibility = View.VISIBLE
        }
    }

    // 8. 화면이 없어질 때(회전 포함) 등록을 푼다. ViewModel이 없어진 옛 화면을 붙잡지 않게 한다(7주차 1일차).
    override fun onDestroy() {
        super.onDestroy()
        viewModel.listener = null
    }

    // 9. ViewModel이 알려 준 문구를 보여 주고, 문구에 맞게 버튼을 고친다(7주차 1일차).
    private fun showState(text: String) {
        binding.stateText.text = text
        if (text == "연결 중…") {
            binding.stopButton.isEnabled = false
        } else if (text == "연결됨") {
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            val intent = Intent(this, ControlActivity::class.java)
            intent.putExtra("name", binding.deviceNameEdit.text.toString())
            startActivity(intent)
        } else if (text == "연결 실패") {
            Toast.makeText(this, text, Toast.LENGTH_SHORT).show()
            binding.retryButton.visibility = View.VISIBLE
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
        }
    }
}
```

`package com.example.smartio` 줄은 내 프로젝트의 첫 줄과 같아야 한다. 다르면 첫 줄은 내 것을 그대로 둔다.
4주차 `connectButton`·`autoSwitch` 부분이 내 코드와 조금 달라도 동작이 같으면 그대로 둔다. 주석 번호가 없어도 괜찮다.

### 7. 회전해 보고 캡처하기

여러 때에 화면을 돌려 보고 결과를 [실습지 관찰표](lab.md#5-회전-뒤-다시-읽기와-관찰표)에 적는다.
폰 크기 화면을 가로로 돌리면 아래쪽이 잘려 [다시 시도]·[연결]이 반쯤 가려질 수 있다. 반쯤 가려진 버튼도 보이는 것으로 적는다.

| 회전한 때 | 회전 뒤 화면 | Logcat `tag:Conn` |
|---|---|---|
| `연결 실패`와 [다시 시도]가 보일 때 | **남는다.** `연결 실패`와 [다시 시도]가 그대로 보인다 | 새 줄이 없다 |
| 제어 화면에서 [뒤로]로 돌아와 `연결됨`일 때 | **남는다.** `연결됨`이 보인다. 제어 화면으로 다시 넘어가지는 않는다 | 새 줄이 없다 |
| `검색 중… 3`일 때 | 글자는 곧바로 `검색 중… 3`이 보이고 1초 뒤 `2`로 **이어진다.** 그러나 [검색]은 켜지고 [중지]는 꺼지고 ProgressBar는 없다(XML 처음 모양). 끝나면 새 화면이 제어 화면으로 넘어가거나 Toast와 [다시 시도]를 보인다 | 회전과 상관없이 `검색 중… 2`, `검색 중… 1`, `연결 중…`이 한 번씩 찍힌다 |
| `검색 중… 3`에서 회전한 뒤 [검색] | 코루틴이 하나 더 생기지 않는다. 버튼 모양만 "검색 중"으로 바뀐다([중지] 켬·ProgressBar 보임) | 줄이 두 번씩 찍히지 않는다 |

**글자는 이어지지만 버튼·ProgressBar는 이어지지 않는다.** `onCreate`에서 다시 읽는 것이 글자와 [다시 시도] 하나뿐이기 때문이다. 2일차에는 상태 하나로 글자와 버튼을 함께 되살린다.

캡처 두 장을 연습용으로 저장해 둔다(제출은 2일차에 한다).

1. `연결 실패`와 [다시 시도]가 보이는 상태에서 회전한 가로 화면
2. 카운트다운 중에 회전한 뒤의 가로 화면과 Logcat(`package:mine tag:Conn`). 글자는 이어지지만 ProgressBar가 없고 [중지]가 꺼진 것이 보여야 한다.

### 8. 바꾸지 않는 파일 확인하기

아래 파일은 4주차에 만든 그대로이며(5·6주차에도 바꾸지 않았다) 이번 주에는 손대지 않는다. 내 프로젝트의 파일에 줄이 몇 개 더 있어도 괜찮다.
같은 코드가 [examples/day1](examples/day1)에 있다.

`ControlActivity.kt` — [examples/day1/ControlActivity.kt](examples/day1/ControlActivity.kt)

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

`activity_control.xml` — [examples/day1/activity_control.xml](examples/day1/activity_control.xml)

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

`AndroidManifest.xml` — [examples/day1/AndroidManifest.xml](examples/day1/AndroidManifest.xml). `ControlActivity` 줄이 있는지만 본다. 내 파일에는 아이콘 등의 줄이 더 있다.
이번 주에 만드는 `ConnViewModel.kt`·`ConnState.kt`는 화면이 아니므로 Manifest에 적지 않는다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:label="@string/app_name"
        android:theme="@style/Theme.SmartIO">

        <!-- New › Activity로 만들면 이 줄이 자동으로 생긴다. -->
        <activity
            android:name=".ControlActivity"
            android:exported="false" />

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

`res/values/themes.xml` — [examples/day1/res/values/themes.xml](examples/day1/res/values/themes.xml). 프로젝트를 만들 때 생긴 그대로다. 내 것을 그대로 둔다.

```xml
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
    <style name="Base.Theme.SmartIO" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Customize your light theme here. -->
        <!-- <item name="colorPrimary">@color/my_light_primary</item> -->
    </style>

    <style name="Theme.SmartIO" parent="Base.Theme.SmartIO" />
</resources>
```

## 2일차

### 9. ConnState 상수 묶음 만들기

1일차에는 `"연결 실패"` 같은 글자를 `ConnViewModel`과 `MainActivity` 두 곳에 직접 쳤다. 한 글자만 달라도 빌드는 되고 비교만 틀린다. 오늘은 상태 글자를 한곳에 모은다.

1. Project 창에서 `app › kotlin+java › com.example.smartio`를 오른쪽 클릭 → **New › Kotlin Class/File** → 목록에서 **Object**를 고르고 이름에 `ConnState`를 넣는다.
2. 생긴 파일을 아래와 같이 채운다. 같은 코드가 [examples/day2/ConnState.kt](examples/day2/ConnState.kt)에 있다.

```kotlin
package com.example.smartio

// 1. 연결 상태를 나타내는 한글 문자열 모음. 화면의 TextView에 그대로 넣어 보여 준다(7주차 2일차).
// 12주차 bleuno 라이브러리의 ConnState와 이름·값이 같다. 12주차에는 이 파일 대신 import만 바꾼다.
object ConnState {
    const val DISCONNECTED = "연결 안 됨"   // 처음 상태, 또는 [중지]·[해제]를 누른 뒤
    const val CONNECTING = "연결 중"        // 5초를 세는 중
    const val DISCOVERING = "서비스 확인 중" // 가짜 연결(2초)을 기다리는 중
    const val READY = "준비됨"              // 연결 성공
    const val LOST = "끊김"                 // 연결 실패
}
```

3. 실행한다. 아직 아무 곳에서도 쓰지 않으므로 화면은 1일차와 같다.

- `object ConnState { }`: 이름으로 바로 부르는 **하나뿐인** 묶음이다. `ConnState()`처럼 만들지 않고 `ConnState.READY`로 부른다.
- `const val`: 바뀌지 않는 상수다. `ConnState.REDY`처럼 이름을 틀리면 빌드 오류로 바로 드러난다.
- 값은 화면에 그대로 보여 줄 한글이다. 12주차 bleuno 라이브러리의 `ConnState`와 이름·값이 같아서, 12주차에는 이 파일 대신 import만 바꾼다.

### 10. [해제] 버튼 추가하기

1. `strings.xml`의 `retry` 줄 아래에 `disconnect` 한 줄을 추가한다. 전체는 아래와 같다. 같은 코드가 [examples/day2/strings.xml](examples/day2/strings.xml)에 있다.

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
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
    <string name="retry">다시 시도</string>
    <string name="disconnect">해제</string>
</resources>
```

2. `activity_main.xml`에서 가로 `LinearLayout` 안, `stopButton` 아래이자 그 `</LinearLayout>` 위에 버튼을 넣는다. 처음에는 눌리지 않게 `enabled="false"`로 둔다.

```xml
        <Button
            android:id="@+id/disconnectButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/disconnect" />
```

세로로 한 줄 더 쌓지 않고 가로 줄에 넣는 이유: 회전한 가로 화면은 높이가 낮아서, 폰 크기 화면에서는 지금도 아래쪽 버튼이 반쯤 가려질 수 있다. 가로 줄에 넣으면 높이가 더 늘지 않는다.

전체는 아래와 같다. 같은 코드가 [examples/day2/activity_main.xml](examples/day2/activity_main.xml)에 있다.

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

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/scanButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/scan" />

        <Button
            android:id="@+id/stopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/stop" />

        <Button
            android:id="@+id/disconnectButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/disconnect" />

    </LinearLayout>

    <ProgressBar
        android:id="@+id/scanProgress"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:visibility="gone" />

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_idle"
        android:textSize="18sp" />

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />

</LinearLayout>
```

3. 실행한다. 가로 줄에 [검색] [중지] [해제]가 보이고 [중지]·[해제]는 회색이다. 나머지는 1일차와 같이 동작한다.

### 11. ConnViewModel을 StateFlow로 바꾸기

11·12단계는 `ConnViewModel.kt`와 `MainActivity.kt`를 함께 바꾼다. 11단계를 마치면 `MainActivity.kt`에 빨간 줄이 생긴다(`resultText`·`listener`가 없어졌기 때문이다). 12단계까지 마친 뒤 실행한다.

1. `ConnViewModel.kt`에서 `// 1.`의 `resultText`와 `// 2.`의 `listener`를 주석까지 지우고, 그 자리에 아래를 넣는다.

```kotlin
    // 1. 화면에 보여 줄 값 두 가지: 연결 상태와 카운트다운 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(7주차 2일차).
    private val _state = MutableStateFlow(ConnState.DISCONNECTED)
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds
```

| 빨간 글자 | 가져올 import |
|---|---|
| `MutableStateFlow` | `kotlinx.coroutines.flow.MutableStateFlow` |
| `StateFlow` | `kotlinx.coroutines.flow.StateFlow` |

2. `startScan()`을 아래로 바꾼다. 막는 `if`는 그대로이고, `launch` 안에서 `show(…)` 대신 `_state`·`_seconds`에 값을 넣는다.

```kotlin
    // 3. [검색]: 연결 중으로 바꾸고 5초를 센 뒤 가짜 연결을 시도한다. 값은 _state·_seconds에 넣는다(7주차 2일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다(7주차 1일차).
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            _state.value = ConnState.CONNECTING
            for (i in 5 downTo 1) {
                Log.d("Conn", "연결 중… $i")
                _seconds.value = i
                delay(1000)
            }
            _seconds.value = 0
            tryConnect()
        }
    }
```

3. `stopScan()`에 두 줄을 더한다.

```kotlin
    // 4. [중지]: 카운트다운 코루틴을 취소하고 연결 안 됨으로 돌린다(7주차 2일차).
    fun stopScan() {
        scanJob?.cancel()
        _seconds.value = 0
        _state.value = ConnState.DISCONNECTED
    }
```

4. `retry()`는 그대로 두고, 그 아래에 [해제]가 부를 함수를 넣는다.

```kotlin
    // 6. [해제]: 연결 안 됨으로 돌린다(7주차 2일차).
    fun disconnect() {
        _state.value = ConnState.DISCONNECTED
    }
```

5. `show()` 함수를 주석까지 지운다. `connectFake()`는 그대로 두고, `tryConnect()`를 아래로 바꾼다.

```kotlin
    // 가짜 연결을 시도하고 결과 상태를 _state에 넣는다.
    private suspend fun tryConnect() {
        _state.value = ConnState.DISCOVERING
        try {
            connectFake()
            _state.value = ConnState.READY
        } catch (e: Exception) {
            _state.value = ConnState.LOST
        }
        Log.d("Conn", _state.value)
    }
```

완성한 `ConnViewModel.kt` 전체는 아래와 같다. 주석 번호는 달라도 된다. 같은 코드가 [examples/day2/ConnViewModel.kt](examples/day2/ConnViewModel.kt)에 있다.

```kotlin
package com.example.smartio

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlin.random.Random

// 7주차 1일차: 연결 화면의 일을 맡는 ViewModel. 화면(Activity)보다 오래 살아서 회전해도 그대로 남는다.
class ConnViewModel : ViewModel() {
    // 1. 화면에 보여 줄 값 두 가지: 연결 상태와 카운트다운 남은 초.
    //    바꾸는 쪽(_state, _seconds)은 안에만 두고, 화면에는 읽기 전용(state, seconds)만 보여 준다(7주차 2일차).
    private val _state = MutableStateFlow(ConnState.DISCONNECTED)
    val state: StateFlow<String> = _state
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds

    // 2. [검색]·[다시 시도]가 시작한 코루틴. 6주차에는 MainActivity에 있던 변수다(7주차 1일차).
    private var scanJob: Job? = null

    // 3. [검색]: 연결 중으로 바꾸고 5초를 센 뒤 가짜 연결을 시도한다. 값은 _state·_seconds에 넣는다(7주차 2일차).
    fun startScan() {
        // 이미 돌고 있으면 새로 시작하지 않는다(7주차 1일차).
        if (scanJob?.isActive == true) {
            return
        }
        scanJob = viewModelScope.launch {
            _state.value = ConnState.CONNECTING
            for (i in 5 downTo 1) {
                Log.d("Conn", "연결 중… $i")
                _seconds.value = i
                delay(1000)
            }
            _seconds.value = 0
            tryConnect()
        }
    }

    // 4. [중지]: 카운트다운 코루틴을 취소하고 연결 안 됨으로 돌린다(7주차 2일차).
    fun stopScan() {
        scanJob?.cancel()
        _seconds.value = 0
        _state.value = ConnState.DISCONNECTED
    }

    // 5. [다시 시도]: 카운트다운 없이 연결만 다시 시도한다(7주차 1일차).
    fun retry() {
        scanJob = viewModelScope.launch {
            tryConnect()
        }
    }

    // 6. [해제]: 연결 안 됨으로 돌린다(7주차 2일차).
    fun disconnect() {
        _state.value = ConnState.DISCONNECTED
    }

    // 연결을 흉내 낸다. 2초 걸리고 절반은 실패한다. 진짜 막히는 일이므로 IO로 옮긴다.
    private suspend fun connectFake(): Boolean = withContext(Dispatchers.IO) {
        Thread.sleep(2000)
        if (Random.nextBoolean()) {
            throw Exception("연결 실패")
        }
        true
    }

    // 가짜 연결을 시도하고 결과 상태를 _state에 넣는다.
    private suspend fun tryConnect() {
        _state.value = ConnState.DISCOVERING
        try {
            connectFake()
            _state.value = ConnState.READY
        } catch (e: Exception) {
            _state.value = ConnState.LOST
        }
        Log.d("Conn", _state.value)
    }
}
```

- `MutableStateFlow(ConnState.DISCONNECTED)`: **지금 값 하나**를 늘 들고 있는 상자다. 처음 값은 `연결 안 됨`이다. `_state.value = …`로 값을 바꾸면 받는 쪽에 알려 준다.
- `val state: StateFlow<String> = _state`: 같은 상자를 화면에는 **읽기 전용**으로 보여 준다. 이름 앞 `_`는 "안에서만 바꾸는 쪽"이라는 약속이다. `<String>`은 안의 값이 글자라는 표시다.
- 1일차의 `resultText`(보관)와 `listener`(알리기)를 이 상자 하나가 함께 맡는다. 그래서 `show()`가 필요 없어졌다.
- `_seconds`는 카운트다운 남은 초다. 상태 글자(`연결 중`)와 숫자를 따로 두고 화면에서 붙인다.

### 12. 상태를 받아 화면 고치기

1. `MainActivity.kt`의 [검색]·[중지]·[다시 시도] 리스너에서 버튼·ProgressBar를 바꾸던 줄을 모두 지우고 ViewModel 함수 한 줄씩만 남긴다. 버튼 고치기는 3번에서 한곳에 모은다.

```kotlin
        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            viewModel.startScan()
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }
```

2. `// 6.` 등록 코드(주석 한 줄과 `viewModel.listener = { … }` 세 줄, 모두 네 줄)를 지우고, 그 자리에 [해제] 리스너를 넣는다.

```kotlin
        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            viewModel.disconnect()
        }
```

3. `// 7.` 다시 읽기 코드(주석, `binding.stateText.text = viewModel.resultText`, `if` 블록)를 지우고, 그 자리(`onCreate()`의 마지막 `}` 위)에 틀을 넣는다.

```kotlin
        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            binding.stopButton.isEnabled = true
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }
```

| 빨간 글자 | 가져올 import |
|---|---|
| `lifecycleScope` | `androidx.lifecycle.lifecycleScope` |
| `launch` | `kotlinx.coroutines.launch` |
| `repeatOnLifecycle` | `androidx.lifecycle.repeatOnLifecycle` |
| `Lifecycle` | `androidx.lifecycle.Lifecycle` |

4. `onCreate()` 아래의 `// 8.` `onDestroy()`와 `// 9.` `showState()`를 주석까지 모두 지운다. 등록·해제는 틀이, 버튼 고치기는 `when`이 맡는다.

5. 실행하고 [검색]을 누른다.

| 때 | `stateText` | 가로 줄에서 켜진 버튼 | ProgressBar |
|---|---|---|---|
| 앱 시작 | `연결 안 됨` | [검색] | 숨김 |
| [검색] 직후 5초 | `연결 중` (아직 숫자가 없다) | [중지] | 보임 |
| 그 뒤 2초 | `서비스 확인 중` | 없음 | 보임 |
| 성공 | `준비됨` | [해제] | 숨김 |
| 실패 | `끊김` | [검색], 아래에 [다시 시도]가 보임 | 숨김 |

[연결]은 어느 때나 켜져 있다(4주차 버튼). Toast와 제어 화면 자동 이동은 없어졌다. 이유는 14단계에서 본다.

- 틀 `lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { … } }`: 화면이 **보일 때만** 안을 실행하고, 안 보이면 멈췄다가 다시 보이면 또 시작한다. 복사해서 쓰고 모양을 바꾸지 않는다.
- `viewModel.state.collect { state -> … }`: 상태가 바뀔 때마다 중괄호 안을 실행한다. 받기를 시작하면 **지금 값부터** 곧바로 받는다. `collect`는 6주차 `delay`처럼 멈췄다 이어지는 함수라서 틀 안에 둔다.
- `// 8.` 다섯 줄: 먼저 모두 끄고 숨긴다. 그다음 `when (state)`에서 그 상태에 켤 것만 켠다. 이렇게 하면 이전 상태에서 켠 버튼이 남지 않는다.
- `when (state) { ConnState.READY -> { … } }`: `state`가 `ConnState.READY`와 같으면 그 중괄호만 실행한다. `if … else if …`를 줄인 모양이다(오늘 문법).

### 13. 남은 초 받기

1. 12단계 3번 틀 **아래**(`onCreate()`의 마지막 `}` 위)에 같은 틀을 하나 더 넣고 `seconds`를 받는다.

```kotlin
        // 9. 남은 초를 받아 "연결 중… 3"처럼 붙여 보여 준다. 7번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        //    반드시 7번 틀 아래에 둔다. 7번이 "연결 중"을 먼저 쓰고 9번이 숫자를 붙여야 회전 뒤에도 숫자가 보인다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    if (seconds > 0) {
                        binding.stateText.text = "연결 중… $seconds"
                    }
                }
            }
        }
```

2. 실행하고 [검색]을 누른다. `연결 중… 5`부터 `연결 중… 1`까지 1초마다 바뀌면 성공이다.

- 받을 값이 두 개(`state`, `seconds`)라 틀을 두 번 쓴다. 한 틀 안에 `collect`를 두 번 이어 쓰면 첫 `collect`가 끝나지 않아서 두 번째가 시작되지 않는다.
- 반드시 `state` 틀 아래에 둔다. 회전 뒤 `state` 틀이 `연결 중`을 먼저 쓰고 이 틀이 숫자를 붙여야 숫자가 바로 보인다.
- `if (seconds > 0)`: 카운트다운 중이 아닐 때(`0`)는 글자를 건드리지 않는다.

완성한 `MainActivity.kt` 전체는 아래와 같다. 같은 코드가 [examples/day2/MainActivity.kt](examples/day2/MainActivity.kt)에 있다.

```kotlin
package com.example.smartio

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import com.example.smartio.databinding.ActivityMainBinding
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    // ViewBinding 틀: 화면의 View를 binding.xxx로 부른다.
    private lateinit var binding: ActivityMainBinding

    // 7주차 1일차: 화면보다 오래 사는 ViewModel을 받아 온다. 회전해도 같은 객체를 돌려준다.
    private val viewModel: ConnViewModel by viewModels()

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

        // 3. [검색] 버튼: 카운트다운이 끝나면 가짜 연결을 시도한다.
        binding.scanButton.setOnClickListener {
            viewModel.startScan()
        }

        // 4. [중지] 버튼: 카운트다운 코루틴을 취소하고 화면을 되돌린다.
        binding.stopButton.setOnClickListener {
            viewModel.stopScan()
        }

        // 5. [다시 시도] 버튼: 카운트다운 없이 연결만 다시 시도한다.
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }

        // 6. [해제] 버튼: 연결을 끊고 연결 안 됨으로 돌아간다(7주차 2일차).
        binding.disconnectButton.setOnClickListener {
            viewModel.disconnect()
        }

        // 7. 상태를 받아 화면을 고친다. 화면이 보일 때(STARTED)만 받고, 회전 뒤에는 마지막 값을 바로 다시 받는다(7주차 2일차).
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    binding.stateText.text = state
                    // 8. 먼저 모두 끄고, 상태에 맞는 것만 켠다. [연결]은 4주차 그대로 항상 켜 둔다(7주차 2일차).
                    binding.scanButton.isEnabled = false
                    binding.stopButton.isEnabled = false
                    binding.disconnectButton.isEnabled = false
                    binding.retryButton.visibility = View.GONE
                    binding.scanProgress.visibility = View.GONE
                    when (state) {
                        ConnState.DISCONNECTED -> {
                            binding.scanButton.isEnabled = true
                        }
                        ConnState.CONNECTING -> {
                            binding.stopButton.isEnabled = true
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.DISCOVERING -> {
                            binding.scanProgress.visibility = View.VISIBLE
                        }
                        ConnState.READY -> {
                            binding.disconnectButton.isEnabled = true
                        }
                        ConnState.LOST -> {
                            binding.scanButton.isEnabled = true
                            binding.retryButton.visibility = View.VISIBLE
                        }
                    }
                }
            }
        }

        // 9. 남은 초를 받아 "연결 중… 3"처럼 붙여 보여 준다. 7번과 같은 틀을 하나 더 쓴다(7주차 2일차).
        //    반드시 7번 틀 아래에 둔다. 7번이 "연결 중"을 먼저 쓰고 9번이 숫자를 붙여야 회전 뒤에도 숫자가 보인다.
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.seconds.collect { seconds ->
                    if (seconds > 0) {
                        binding.stateText.text = "연결 중… $seconds"
                    }
                }
            }
        }
    }
}
```

### 14. 상태별 버튼과 회전 확인하기

1. 아래 표의 순서대로 눌러 보고 화면이 같은지 확인한다. 실패가 먼저 나오면 [다시 시도]를, 성공이 먼저 나오면 [해제] 뒤 [검색]을 다시 누른다. 절반 확률이다.

| 상태(`state`) | `stateText` | [검색] | [중지] | [해제] | [다시 시도] | ProgressBar | [연결] |
|---|---|---|---|---|---|---|---|
| 시작 `DISCONNECTED` | `연결 안 됨` | 켬 | 끔 | 끔 | 숨김 | 숨김 | 켬 |
| [검색] → `CONNECTING` | `연결 중… 5` → `4`·`3`·`2`·`1` | 끔 | 켬 | 끔 | 숨김 | 보임 | 켬 |
| 5초 뒤 `DISCOVERING` | `서비스 확인 중` (2초) | 끔 | 끔 | 끔 | 숨김 | 보임 | 켬 |
| 성공 `READY` | `준비됨` | 끔 | 끔 | **켬** | 숨김 | 숨김 | 켬 |
| 실패 `LOST` | `끊김` | 켬 | 끔 | 끔 | **보임** | 숨김 | 켬 |
| `CONNECTING`에서 [중지] | `연결 안 됨` | 켬 | 끔 | 끔 | 숨김 | 숨김 | 켬 |
| `READY`에서 [해제] | `연결 안 됨` | 켬 | 끔 | 끔 | 숨김 | 숨김 | 켬 |
| `LOST`에서 [다시 시도] | `서비스 확인 중` → `준비됨` 또는 `끊김` | 위 표와 같다 | | | | | 켬 |

2. **회전**: `연결 중… 3`에서 돌리면 새 화면이 곧바로 `연결 중… 3`을 보이고 1초 뒤 `2`로 이어진다. [중지]만 켜져 있고 ProgressBar도 보인다. 다른 상태에서 돌려도 같은 글자·버튼이 그대로 보인다. 홈으로 나갔다 돌아와도 같다.
3. **Logcat** `tag:Conn`: `연결 중… 5` … `연결 중… 1`, 이어서 `준비됨` 또는 `끊김`이 찍힌다. 회전해도 끊기지 않고 두 번씩 찍히지 않는다.
4. [연결]은 어느 상태에서든 4주차와 같다. 이름이 비면 Toast `장치 이름을 입력하세요`, 아니면 제어 화면 `장치: 이름`. [뒤로]로 돌아오면 그 전 상태(예: `준비됨`)가 그대로 보인다.

1일차와 달라진 점:

- 문구가 `ConnState` 값으로 바뀌었다(`대기 중`→`연결 안 됨`, `검색 중… N`→`연결 중… N`, `연결 중…`→`서비스 확인 중`, `연결됨`→`준비됨`, `연결 실패`→`끊김`).
- 성공해도 제어 화면으로 **자동 이동하지 않는다.** `collect`는 회전하거나 제어 화면에서 돌아와 화면이 다시 보일 때마다 마지막 값 `준비됨`을 다시 받는다. `collect` 안에 `startActivity`를 두면 그때마다 제어 화면이 또 열린다. `준비됨`에서 [연결]을 누른다.
- 실패 Toast가 없다. 같은 이유로 `collect` 안의 Toast는 회전할 때마다 다시 뜬다. `끊김`과 [다시 시도]로 알린다.

제출 캡처 두 장을 찍는다.

1. **캡처 1**: [검색] 뒤 `연결 중… 3`(또는 2)에서 회전한 **가로 화면**. [중지]만 켜져 있고 ProgressBar가 보여야 한다. 폰 크기 가로 화면에서는 아래쪽 [연결]이 반쯤 가려져도 된다. 회전 전 세로 화면도 함께 찍어 두면 숫자가 이어진 것이 드러난다.
2. **캡처 2**: `준비됨` 화면. 가로 줄 [검색]·[중지]·[해제] 가운데 **[해제]만** 켜져 있어야 한다. 아래쪽 [연결]은 항상 켜져 있는 4주차 버튼이다.

### 15. 제출하기

제출물은 다섯 가지다.

1. `ConnState.kt`
2. `ConnViewModel.kt`
3. `MainActivity.kt`
4. 캡처 1: `연결 중… 3`에서 회전한 가로 화면
5. 캡처 2: `준비됨`에서 [해제]만 켜진 화면

`ControlActivity.kt`와 XML 파일은 내지 않는다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고는 실행을 막지 않는다.
자주 나오는 오류와 해결 방법은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 꺼졌다면 Logcat에서 `FATAL EXCEPTION` 줄을 찾아 그 아래 `Caused by`를 읽는다.
