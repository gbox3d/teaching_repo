# 10주차 예제 — 배터리 방송과 BLE 권한

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `batteryReceiver`, `onStart` 등록(10번), `onStop` 해제(11번) |
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` | 맨 아래 `batteryText` 추가 |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | `battery_unknown` 추가 |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` | `permissionLauncher`, [권한 확인] 리스너(12번), `hasBlePermissions()`(13번), `showPermissionDialog()`(14번) |
| [day2/Permissions.kt](day2/Permissions.kt) | `app › kotlin+java › com.example.smartio › Permissions.kt` (새 파일, New › Kotlin Class/File › **File**) | 제공 함수 `blePermissions()`. 받아서 붙여 넣는다 |
| [day2/AndroidManifest.xml](day2/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | `uses-feature` 1개, `uses-permission` 5개. `<manifest>` 태그에 `xmlns:tools`가 이미 있는지 먼저 보고, 없을 때만 한 줄 넣는다(두 번 넣으면 빌드 오류) |
| [day2/activity_main.xml](day2/activity_main.xml) | `activity_main.xml` | `retryButton` 아래 `permissionButton` 추가 |
| [day2/strings.xml](day2/strings.xml) | `strings.xml` | `check_permission` 추가 |
| `dayN/ConnState.kt`, `dayN/ConnViewModel.kt` | 상태 상수·ViewModel | 7주차 그대로, 바꾸지 않는다 |
| `dayN/ControlActivity.kt`, `dayN/activity_control.xml` | 제어 화면 | 7주차 그대로, 바꾸지 않는다 |
| `day1/AndroidManifest.xml`, `dayN/res/values/themes.xml` | Manifest·테마 | 7주차 그대로. 내 파일에는 아이콘 등 줄이 더 있어도 된다 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`ContextCompat`(core-ktx), `registerForActivityResult`(activity-ktx), `AlertDialog`(appcompat)는 4주차 `build.gradle.kts`의 의존성에 이미 들어 있다.
주석 번호는 7주차 1~9에 이어 붙였다. 12번은 `onCreate` 안이라 파일에서는 10·11번보다 위에 있다.

## 1. `object : BroadcastReceiver()` — 방송을 받는 틀

```kotlin
private val batteryReceiver = object : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        // 방송이 올 때마다 여기가 실행된다
    }
}
```

- 이름 없는 Receiver 하나를 만들어 `batteryReceiver`에 담는다. 틀은 그대로 복사하고 `onReceive` 안만 채운다.
- 클래스 변수 자리(`onCreate` 밖)에 둔다. Manifest에는 적지 않는다.

## 2. 등록과 해제 — `onStart`와 `onStop`

```kotlin
override fun onStart() {
    super.onStart()
    ContextCompat.registerReceiver(
        this,
        batteryReceiver,
        IntentFilter(Intent.ACTION_BATTERY_CHANGED),
        ContextCompat.RECEIVER_NOT_EXPORTED
    )
}

override fun onStop() {
    super.onStop()
    unregisterReceiver(batteryReceiver)
}
```

| 실행 결과 | 화면 |
|---|---|
| 앱 시작 | `배터리 ?`가 곧바로 `배터리 100% · 충전 중`(에뮬레이터 처음 값) |
| 홈 → Battery 값 바꾸기 → 복귀 | 돌아오자마자 새 값 |
| [연결] → 제어 화면 → [뒤로] | 돌아오자마자 현재 값 |

- `IntentFilter(Intent.ACTION_BATTERY_CHANGED)`: 배터리 방송만 골라 받는다.
- `RECEIVER_NOT_EXPORTED`: 다른 앱이 보낸 방송은 받지 않는다. 배터리 방송은 시스템이 보내므로 받는다.
- `ACTION_BATTERY_CHANGED`는 등록하자마자 마지막 값이 한 번 온다.
- 해제를 빼도 빌드는 된다. 등록·해제는 `onStart`/`onStop` 짝으로 둔다.

## 3. 배터리 값 꺼내기 — `getIntExtra`

```kotlin
val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) ?: 0
if (level == -1) {
    return
}
val percent = level * 100 / scale
val charging = if (plugged != 0) "충전 중" else "충전 안 함"
binding.batteryText.text = "배터리 $percent% · $charging"
```

| 에뮬레이터 ⋯ › Battery 조작 | 화면 |
|---|---|
| Charge level 80 | `배터리 80% · 충전 중` |
| Charger connection `None` | `배터리 80% · 충전 안 함` |
| Charger connection `AC charger` | `배터리 80% · 충전 중` |

- `getIntExtra(이름, 기본값)`: 4주차 `getStringExtra`의 정수 판이다. `intent`가 `Intent?`라 `?.`와 `?:`를 붙인다.
- `?: -1`을 빼면 `level`이 `Int?`가 되어 `level * 100`에서 `Operator call is prohibited on a nullable receiver of type 'kotlin.Int?'. Use '?.'-qualified call instead.` 오류가 난다.
- `!=`는 "같지 않으면"이다. `$percent%`의 `%`는 글자로 붙는다.
- 연결 화면은 스크롤이 없어 가로 화면에서는 맨 아래 문구가 잘릴 수 있다. 확인과 캡처는 세로에서 한다.

## 4. Manifest 선언 — 버전마다 다른 권한

```xml
<uses-permission
    android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation"
    tools:targetApi="s" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission
    android:name="android.permission.ACCESS_FINE_LOCATION"
    android:maxSdkVersion="30" />
```

| 선언 | Android 버전 | 실행 중 허락 |
|---|---|---|
| `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` | 12(API 31) 이상 | 필요 |
| `BLUETOOTH`, `BLUETOOTH_ADMIN` (`maxSdkVersion="30"`) | 11(API 30) 이하 | 필요 없음 |
| `ACCESS_FINE_LOCATION` (`maxSdkVersion="30"`) | 11(API 30) 이하 | 필요 |

- 전체 파일은 [day2/AndroidManifest.xml](day2/AndroidManifest.xml)이다. `tools:` 속성을 쓰려고 `<manifest>` 태그에 `xmlns:tools`가 있다. 새 프로젝트 템플릿에는 보통 이미 들어 있으니 내 파일에 있으면 다시 넣지 않는다.
- `neverForLocation`은 검색 결과로 위치를 알아내지 않는다는 표시, `tools:targetApi="s"`는 Android 12용 속성이라고 편집기에 알리는 표시다. 외우지 않는다.
- 선언을 빼도 빌드는 된다. 그러면 [권한 확인]을 눌러도 권한 창이 뜨지 않고 곧바로 거절로 처리된다(예상).

## 5. `blePermissions()` — 버전에 맞는 권한 고르기(제공)

```kotlin
fun blePermissions(): Array<String> {
    if (Build.VERSION.SDK_INT >= 31) {
        return arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        return arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }
}
```

| 기기 | 돌려주는 값 |
|---|---|
| Android 12(API 31) 이상 | `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` |
| Android 11(API 30) 이하 | `ACCESS_FINE_LOCATION` |

- 클래스 없이 함수만 든 파일이다. 같은 package 어디서나 `blePermissions()`로 부른다.
- `Manifest`는 `android.Manifest`를 import한다.
- 12주차 `bleuno` 라이브러리의 `PermissionHelper.required()`도 같은 목록을 돌려준다.

## 6. 확인과 요청 — `checkSelfPermission`과 `registerForActivityResult`

```kotlin
private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
    if (hasBlePermissions()) {
        Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
    } else {
        showPermissionDialog()
    }
}

private fun hasBlePermissions(): Boolean {
    for (permission in blePermissions()) {
        if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
            return false
        }
    }
    return true
}
```

```kotlin
binding.permissionButton.setOnClickListener {
    if (hasBlePermissions()) {
        Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
    } else {
        permissionLauncher.launch(blePermissions())
    }
}
```

| 실행 결과 | 화면 |
|---|---|
| 처음 [권한 확인] | 시스템 권한 창 한 개(Android 12 이상은 "근처 기기") |
| 권한 창 [허용] | Toast `권한 OK` |
| 허용한 뒤 [권한 확인] | 창 없이 Toast `권한 OK` |
| 권한 창 [허용 안함] | 대화상자 `권한이 필요합니다` |
| 같은 권한을 두 번 거절한 뒤 [권한 확인] | 권한 창 없이 곧바로 대화상자 |

- 요청 틀은 클래스 변수 자리에서 만든다. 버튼 리스너 안에서 만들면 빌드는 되지만 누르는 순간 앱이 멈춘다(예상).
- `{ _ -> }`: 결과 묶음은 읽지 않고 `hasBlePermissions()`로 지금 권한을 다시 확인한다.
- 권한 창 문구와 버튼 이름은 OS 버전과 언어 설정에 따라 조금 다르다.

## 7. `AlertDialog`와 암시적 Intent — 설정 화면 열기

```kotlin
private fun showPermissionDialog() {
    AlertDialog.Builder(this)
        .setTitle("권한이 필요합니다")
        .setMessage("장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.")
        .setPositiveButton("설정으로") { _, _ ->
            val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))
            startActivity(intent)
        }
        .setNegativeButton("취소", null)
        .show()
}
```

| 실행 결과 | 화면 |
|---|---|
| [설정으로] | 설정 앱의 `Smart I/O Controller` 앱 정보 화면 |
| [취소] | 대화상자만 닫힘 |
| 설정에서 허용 → 뒤로 → [권한 확인] | Toast `권한 OK` |

- `AlertDialog`는 `androidx.appcompat.app.AlertDialog`를 import한다.
- 4주차 명시적 Intent는 열 화면(`ControlActivity::class.java`)을 정했다. 암시적 Intent는 할 일(ACTION)과 대상(`package:…` 주소)만 적고 시스템이 화면을 찾는다.
- `package:`를 빼면 [설정으로]를 누르는 순간 앱이 멈춘다(예상).

## 8. 강의 시연 — `setResult`로 결과 받기(완성본에 없음)

2일차 23–27분 시연 코드다. 실습하지 않으며 `day2`에도 넣지 않았다. 12주차 "블루투스 켜기" 요청 결과를 같은 틀로 받는다.

```kotlin
// MainActivity 클래스 변수 자리
private val controlLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    if (result.resultCode == RESULT_OK) {
        val message = result.data?.getStringExtra("message") ?: ""
        Toast.makeText(this, "돌아온 값: $message", Toast.LENGTH_SHORT).show()
    }
}
// [연결] 리스너: startActivity(intent) → controlLauncher.launch(intent)
```

```kotlin
// ControlActivity [뒤로] 리스너 (import android.content.Intent 추가)
binding.backButton.setOnClickListener {
    val result = Intent()
    result.putExtra("message", "제어 화면을 닫음")
    setResult(RESULT_OK, result)
    finish()
}
```

| 실행 결과 | 화면 |
|---|---|
| [연결] → 제어 화면 → [뒤로] | 연결 화면에 Toast `돌아온 값: 제어 화면을 닫음` |
| 뒤로 가기 제스처로 닫기 | Toast 없음(`setResult`를 거치지 않음) |

## 9. 2일차 완성 — 배터리 문구와 권한 흐름

[day2](day2) 파일을 모두 넣고 실행한 흐름:

```text
앱 시작 → onStart 등록 → 배터리 100% · 충전 중
[권한 확인] ─┬─ 이미 허용 ─────────────▶ Toast "권한 OK"
             └─ 권한 창 ─┬─ 허용 ──────▶ Toast "권한 OK"
                         └─ 허용 안함 ─▶ 권한이 필요합니다 ─┬─ [설정으로] ▶ 앱 정보 화면
                                                            └─ [취소]
```

## 공식 참고 자료

- [브로드캐스트 개요 — Android Developers](https://developer.android.com/develop/background-work/background-tasks/broadcasts)
- [배터리 상태 모니터링 — Android Developers](https://developer.android.com/training/monitoring-device-state/battery-monitoring)
- [런타임 권한 요청 — Android Developers](https://developer.android.com/training/permissions/requesting)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
