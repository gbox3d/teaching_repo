---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 10주차
footer: BroadcastReceiver와 런타임 권한
---

# BroadcastReceiver와 런타임 권한

9주차 비교표에서 이름만 본 **BroadcastReceiver**를 이번 주에 직접 만듭니다.
그리고 12주차 BLE 검색 전에 필요한 **권한**을 사용자에게 받습니다.

```text
배터리 80% · 충전 중        권한이 필요합니다
                            [취소] [설정으로]
```

---

# 1일차 — 배터리 방송 받기

`30분 설명·시연 → 60분 실습`

1. `object : BroadcastReceiver()` 틀로 방송을 받는 Receiver 만들기
2. `onStart`에서 등록하고 `onStop`에서 해제하기
3. 방송에 실린 배터리 값을 꺼내 화면에 보여 주기

---

## 1일차 · 0–5분 — 오늘 문법: Receiver 틀과 !=

```kotlin
private val batteryReceiver = object : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        // 방송이 올 때마다 여기가 실행된다
    }
}
```

- `object : BroadcastReceiver() { … }`는 **이름 없는 Receiver 하나**를 만들어 변수에 담는 틀입니다. 통째로 복사해 씁니다.
- `Context?`, `Intent?`의 `?`는 3주차 null 안전성입니다. 비어 있을 수 있습니다.
- 한 줄 더: `!=`는 **같지 않으면**입니다. `==`의 반대입니다.
- `if (plugged != 0) "충전 중" else "충전 안 함"` — 1주차 `if … else` 한 줄과 같은 모양입니다.

---

## 1일차 · 5–15분 ① — 방송과 Receiver

```text
시스템: "배터리가 바뀌었다"  ── Intent(ACTION_BATTERY_CHANGED) ──▶
   IntentFilter(Intent.ACTION_BATTERY_CHANGED)   ← 이 방송만 골라 받기
      └▶ batteryReceiver.onReceive(context, intent) 실행
```

- **방송**은 시스템이나 앱이 "이런 일이 생겼다"고 알리는 `Intent`입니다.
- **Receiver**는 그 방송을 받는 컴포넌트입니다. 화면이 없습니다.
- 받고 싶은 방송은 `IntentFilter`로 고릅니다.
- 오늘은 코드에서 등록합니다. Manifest에는 적지 않습니다.

---

## 1일차 · 5–15분 ② — onStart에서 등록, onStop에서 해제

```kotlin
override fun onStart() {
    super.onStart()
    ContextCompat.registerReceiver(this, batteryReceiver,
        IntentFilter(Intent.ACTION_BATTERY_CHANGED), ContextCompat.RECEIVER_NOT_EXPORTED)
}
override fun onStop() {
    super.onStop()
    unregisterReceiver(batteryReceiver)
}
```

- 두 함수는 `onCreate()` **바깥**, 클래스 안에 둡니다. 3주차 생명주기 콜백과 같은 자리입니다.
- `RECEIVER_NOT_EXPORTED`: 다른 앱이 보낸 방송은 받지 않습니다. 시스템 방송은 받습니다.
- `ContextCompat`·`IntentFilter`가 빨간색이면 Alt+Enter(맥 ⌥+Enter)로 import합니다.

---

## 1일차 · 5–15분 ③ — 등록과 해제는 짝으로

```text
onStart ─ 등록(registerReceiver) ───▶ 방송이 오면 onReceive
onStop  ─ 해제(unregisterReceiver) ─▶ 더 받지 않음
홈·회전·[연결]로 다른 화면 ─▶ onStop … 돌아오면 onStart ─▶ 다시 등록
```

- 화면이 **보이는 동안만** 받습니다. 안 보이는 화면의 글자를 고칠 필요가 없습니다.
- 해제를 빼도 빌드는 됩니다. 그래서 짝을 눈으로 확인해야 합니다.
- `ACTION_BATTERY_CHANGED`는 등록하자마자 **마지막 값이 한 번** 옵니다. 앱을 켜면 곧바로 숫자가 보입니다.

---

## 1일차 · 15–25분 ① — intent에서 배터리 값 꺼내기

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

- `getIntExtra(이름, 기본값)`: 4주차 `getStringExtra`의 정수 판입니다. 값이 없으면 기본값입니다.
- `intent`가 `Intent?`라서 `?.`와 `?:`를 붙입니다. `?: -1`을 빼면 `level * 100`에서 빌드 오류가 납니다.
- `$percent%`의 `%`는 그냥 글자로 붙습니다.

---

## 1일차 · 15–25분 ② — 에뮬레이터로 배터리 바꾸기

| 이름 | 뜻 | 에뮬레이터 처음 값 |
|---|---|---|
| `EXTRA_LEVEL` | 남은 양 | 100 |
| `EXTRA_SCALE` | 가득 찼을 때의 값(보통 100) | 100 |
| `EXTRA_PLUGGED` | 0이면 충전기가 빠짐, 0이 아니면 꽂힘 | 0이 아닌 값(AC charger) |

시연: 에뮬레이터 도구 막대 **⋯** › **Battery**

- Charge level을 80으로 → `배터리 80% · 충전 중`
- Charger connection을 `None`으로 → `배터리 80% · 충전 안 함`
- 홈으로 나갔다가 슬라이더를 바꾸고 돌아오기 → 돌아오자마자 새 값

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--배터리-상태-받기-60분) · [따라하기](walkthrough.md#1일차)

1. 연결 화면 맨 아래에 `batteryText`(`배터리 ?`)를 넣습니다.
2. `batteryReceiver` 틀을 복사하고 `onReceive` 안을 채웁니다.
3. `onStart`에서 등록, `onStop`에서 해제합니다.
4. Battery 값을 80 같은 값으로 바꾸고 **세로 화면**을 캡처합니다.

**설명 합계: 5+10+10+5 = 30분**

`override fun onStart()`에 빨간 줄이 생기면 `onCreate`의 닫는 `}` **아래**에 있는지 봅니다.

---

# 2일차 — 권한 요청하고 거절에 대처하기

`30분 설명·시연 → 60분 실습`

1. 런타임 권한 5단계와 Manifest 선언
2. 요청 창을 띄우고 결과 받기
3. 거절하면 `AlertDialog`로 알리고 설정 화면 열기

---

## 2일차 · 0–8분 ① — 런타임 권한 5단계

| 단계 | 하는 일 | 이번 주 코드 |
|---|---|---|
| ① 선언 | "이 권한을 쓴다"고 적는다 | `AndroidManifest.xml`의 `uses-permission` |
| ② 확인 | 이미 허용됐나 본다 | `hasBlePermissions()` |
| ③ 설명 | 왜 필요한지 알린다 | 거절 뒤 `AlertDialog` |
| ④ 요청 | 시스템 권한 창을 띄운다 | `permissionLauncher.launch(…)` |
| ⑤ 결과 | 허용·거절에 맞춰 화면을 바꾼다 | 요청 틀의 `{ _ -> … }` |

- Manifest에 적기만 해서는 안 됩니다. **실행 중에** 사용자가 허락해야 합니다.
- 앱을 켜자마자 묻지 않고, 사용자가 [권한 확인]을 누를 때 묻습니다.

---

## 2일차 · 0–8분 ② — Manifest 선언은 버전마다 다르다

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

- Android 12(API 31) 이상: `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT` / 11 이하: `ACCESS_FINE_LOCATION`
- `maxSdkVersion="30"`: 30 이하에서만 쓰는 선언. `BLUETOOTH`·`BLUETOOTH_ADMIN`도 같은 모양입니다(전체는 따라하기).
- `tools:`를 쓰려면 `<manifest>` 태그에 `xmlns:tools` 한 줄이 있어야 합니다. 새 프로젝트에는 보통 이미 있으니 **확인만** 하고, 없을 때만 넣습니다(두 번 넣으면 빌드 오류).

---

## 2일차 · 8–15분 ① — 버전에 맞는 권한 고르기(제공 함수)

**오늘 새로 보는 모양 3가지** — 받아서 붙여 넣는 파일이라 읽을 줄만 알면 됩니다.
① 함수만 든 파일 ② `arrayOf(…)` ③ `return 값`

```kotlin
fun blePermissions(): Array<String> {
    if (Build.VERSION.SDK_INT >= 31) {
        return arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
    } else {
        return arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }
}
```

- ① 클래스 없이 함수만 든 **파일**입니다. New › Kotlin Class/File › **File**, 이름 `Permissions`. 받아서 붙여 넣습니다.
- ② `Array<String>` / `arrayOf(…)`: 글자 여러 개를 묶은 배열입니다. 목록 문법은 11주차에 배웁니다.
- ③ `return 값`: 7주차 `return`에 돌려줄 값을 붙인 모양입니다. `Build.VERSION.SDK_INT`는 기기의 Android 버전 번호입니다.

---

## 2일차 · 8–15분 ② — 요청 창을 띄우고 결과 받기

```kotlin
private val permissionLauncher =
    registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (hasBlePermissions()) {
            Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
        } else {
            showPermissionDialog()
        }
    }
```

- 요청 틀은 **클래스 변수 자리**(`onCreate` 밖)에서 만듭니다. 버튼 안에서 만들면 누르는 순간 앱이 멈춥니다.
- 버튼에서는 `permissionLauncher.launch(blePermissions())`로 요청 창을 띄웁니다.
- `{ _ -> }`: 넘어오는 결과는 읽지 않고(`_`), 지금 권한을 **다시 확인**합니다.

---

## 2일차 · 8–15분 ③ — checkSelfPermission으로 하나씩 확인

```kotlin
private fun hasBlePermissions(): Boolean {
    for (permission in blePermissions()) {
        if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
            return false
        }
    }
    return true
}
```

- `for (permission in blePermissions())`: 6주차 `for (i in 5 downTo 1)`의 "묶음 안의 것을 하나씩" 판입니다. 외우지 않고 이 줄은 복사합니다.
- 하나라도 허용되지 않았으면 `return false`, 끝까지 통과하면 `true`입니다.
- [권한 확인] 버튼(요청 전)과 요청 틀(요청 뒤)이 같은 함수로 확인합니다.

---

## 2일차 · 15–23분 ① — 거절하면 AlertDialog

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

- `AlertDialog`는 Alt+Enter 목록에서 **`androidx.appcompat.app.AlertDialog`**를 고릅니다.
- `{ _, _ -> }`: 4주차 `{ _, isChecked -> }`처럼 안 쓰는 값은 `_`로 둡니다.

---

## 2일차 · 15–23분 ② — 암시적 Intent로 설정 화면 열기

| | 4주차 명시적 Intent | 오늘 암시적 Intent |
|---|---|---|
| 코드 | `Intent(this, ControlActivity::class.java)` | `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))` |
| 적는 것 | 열 화면(클래스) | 할 일(ACTION) + 대상(주소) |
| 화면을 찾는 쪽 | 내가 정한다 | 시스템이 맞는 화면을 찾는다 |

- `$packageName`은 이 앱의 package 이름(`com.example.smartio`)입니다.
- 주소는 반드시 `package:`로 시작합니다. 빼면 [설정으로]를 누르는 순간 앱이 멈춥니다.
- 설정에서 허용하고 돌아와도 글자가 저절로 바뀌지는 않습니다. [권한 확인]을 다시 누릅니다.

---

## 2일차 · 23–27분 ① — 시연: 다른 화면의 결과 받기

```kotlin
// MainActivity 클래스 변수 자리: 권한 요청 틀과 같은 모양
private val controlLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
    if (result.resultCode == RESULT_OK) {
        val message = result.data?.getStringExtra("message") ?: ""
        Toast.makeText(this, "돌아온 값: $message", Toast.LENGTH_SHORT).show()
    }
}
```

- [연결] 리스너의 `startActivity(intent)`를 `controlLauncher.launch(intent)`로 바꿉니다.
- `result.data?.getStringExtra(…) ?: ""`는 3주차 `?.`·`?:`와 4주차 `getStringExtra`입니다.
- 오늘은 **시연만** 합니다. 완성본에는 넣지 않습니다.

---

## 2일차 · 23–27분 ② — 시연: setResult로 돌려주기

```kotlin
// ControlActivity의 [뒤로] 버튼
binding.backButton.setOnClickListener {
    val result = Intent()
    result.putExtra("message", "제어 화면을 닫음")
    setResult(RESULT_OK, result)
    finish()
}
```

- [뒤로]로 닫으면 연결 화면에 Toast `돌아온 값: 제어 화면을 닫음`이 뜹니다.
- 뒤로 가기 제스처로 닫으면 `setResult`를 거치지 않아 Toast가 뜨지 않습니다.
- 12주차에 "블루투스 켜기" 요청 결과를 이 틀로 받습니다.

---

## 2일차 · 27–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--권한-요청과-거절-안내-60분) · [따라하기](walkthrough.md#2일차)

1. [권한 확인] 버튼, Manifest 권한 선언, `Permissions.kt`를 넣습니다.
2. `hasBlePermissions()`와 `showPermissionDialog()`를 만듭니다.
3. 요청 틀 `permissionLauncher`와 [권한 확인] 리스너를 넣습니다.
4. 거절 대화상자와 설정 앱 화면을 캡처합니다.

**설명 합계: 8+7+8+4+3 = 30분**

권한 창이 안 뜨고 바로 대화상자가 나오면 Manifest의 `uses-permission`부터 확인합니다.

---

## 제출하기

2일차가 끝나면 한 번 제출합니다.

1. **`MainActivity.kt`, `AndroidManifest.xml`**
2. **캡처 1**: Battery 값을 바꾼 뒤 `배터리 80% · 충전 중`처럼 보이는 연결 화면(세로)
3. **캡처 2**: 권한을 거절한 뒤 뜬 `권한이 필요합니다` 대화상자
4. **캡처 3**: [설정으로]를 눌러 열린 `Smart I/O Controller` 앱 정보 화면

---

## 다음 주 미리 보기

11주차에는 연결 화면에 **장치 이름 목록**을 두고, 마지막으로 연결한 장치를 **저장**합니다.

앱을 껐다 켜도 `마지막 장치: …`가 남으려면 어디에 적어 두어야 할까요?

12주차 BLE 수업 전에 실기기를 연결하고, 이번 주 권한 흐름으로 권한까지 받아 둡니다.
