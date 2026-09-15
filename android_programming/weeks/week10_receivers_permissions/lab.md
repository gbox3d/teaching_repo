# 10주차 실습 — 배터리 방송 받기와 BLE 권한 요청

이번 주에는 7주차 `SmartIO` 연결 화면에 배터리 문구를 붙이고, 2일차에는 12주차 BLE 검색에 필요한 권한을 요청한다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 에뮬레이터 설정을 바꿔 가며 화면이 어떻게 달라지는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 배터리 상태 받기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 7주차 `SmartIO`를 실행하고 `strings.xml`·`activity_main.xml`에 배터리 글자 자리를 만든다 |
| 10–25분 | `batteryReceiver` 틀을 복사하고 `onReceive` 안에서 문구를 만든다 |
| 25–40분 | `onStart`에서 등록, `onStop`에서 해제하고 실행한다 |
| 40–52분 | 에뮬레이터 Battery를 바꾸며 관찰표를 채운다 |
| 52–60분 | 캡처 1을 찍고 프로젝트를 저장한다 |

### 1. 배터리 글자 자리 만들기

1. `strings.xml`에 `battery_unknown`(`배터리 ?`)을 넣는다.
2. `activity_main.xml`의 `retryButton` 아래, 마지막 `</LinearLayout>` 위에 id가 `batteryText`인 TextView를 넣고 글자를 `@string/battery_unknown`으로 둔다. 크기는 `16sp`, 위 간격은 `16dp`로 시작한다.
3. 실행해 화면 맨 아래에 `배터리 ?`가 보이면 다음으로 간다.

막히면 [따라하기 2단계](walkthrough.md#2-배터리-글자-자리-만들기)를 본다.

### 2. batteryReceiver 틀 채우기

클래스 안, `viewModel` 줄 아래(`onCreate` **밖**)에 틀을 복사하고 안을 채운다. 빨간 글자는 **Alt+Enter**(맥 ⌥+Enter)로 import한다.

```kotlin
private val batteryReceiver = object : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        // 1) level: intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        // 2) scale(기본값 100), plugged(기본값 0)도 같은 모양
        // 3) level이 -1이면 return
        // 4) percent = level * 100 / scale
        // 5) plugged가 0이 아니면 "충전 중", 0이면 "충전 안 함"
        // 6) binding.batteryText.text = "배터리 80% · 충전 중" 모양
    }
}
```

- `BatteryManager`는 `android.os.BatteryManager`다.
- `?: -1`처럼 기본값을 붙이지 않으면 `level`이 `Int?`가 되어 곱셈에서 빌드 오류가 난다. [막혔을 때](#막혔을-때)의 문구를 읽어 본다.
- 가운뎃점 `·`가 입력하기 어려우면 `-`로 써도 된다.
- 이 단계에서 실행하면 화면은 여전히 `배터리 ?`다. 왜 그런지 한 문장으로 적어 둔다.

### 3. 등록과 해제

1. `onCreate`를 닫는 `}` **아래**에 `override fun onStart()`를 만들고 `super.onStart()` 다음 줄에서 `ContextCompat.registerReceiver(…)`로 등록한다. 인자는 `this`, `batteryReceiver`, `IntentFilter(Intent.ACTION_BATTERY_CHANGED)`, `ContextCompat.RECEIVER_NOT_EXPORTED` 네 개다.
2. 그 아래 `override fun onStop()`에서 `unregisterReceiver(batteryReceiver)`로 해제한다.
3. 실행해 `배터리 ?`가 곧바로 `배터리 100% · 충전 중`처럼 바뀌면 성공이다.

- `ContextCompat`은 `androidx.core.content.ContextCompat`, `IntentFilter`는 `android.content.IntentFilter`를 Alt+Enter로 import한다.

- `onStart`·`onStop`은 `onCreate` **안**에 넣지 않는다. 넣으면 `override`에 빨간 줄이 생긴다.
- 막히면 [1일차 완성 코드](examples/day1/MainActivity.kt)와 한 줄씩 비교한다.

### 4. 에뮬레이터 Battery로 관찰하기

에뮬레이터 도구 막대 **⋯** › **Battery**에서 한 번에 한 가지만 바꾸고 결과를 적는다.

| 조작 | 예상 문구 | 실제 문구 |
|---|---|---|
| Charge level 80 |  |  |
| Charger connection `None` |  |  |
| Charger connection `AC charger` |  |  |
| 홈 → Charge level 50 → 앱으로 돌아오기 |  |  |
| [연결] → 제어 화면 → Charge level 30 → [뒤로] |  |  |

마지막 두 줄에서 문구가 **언제** 바뀌었는지 `onStop`·`onStart`로 한 문장 적는다.

### 5. 오늘 확인할 것

- [ ] 앱을 켜면 `배터리 ?`가 곧바로 숫자 문구로 바뀐다.
- [ ] Charge level과 Charger connection을 바꾸면 문구가 따라 바뀐다.
- [ ] 등록은 `onStart`, 해제는 `onStop`에 있고 둘 다 `onCreate` 밖에 있다.
- [ ] 관찰표를 채웠다.
- [ ] Charge level을 100이 아닌 값으로 바꾼 **세로** 연결 화면을 캡처했다(캡처 1).

가로로 돌리면 맨 아래 배터리 문구가 잘려 안 보일 수 있다. 캡처는 세로에서 한다.
프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 권한 요청과 거절 안내 (60분)

| 시간 | 할 일 |
|---|---|
| 0–12분 | [권한 확인] 버튼을 넣고 Manifest에 권한을 선언하고 `Permissions.kt`를 붙여 넣는다 |
| 12–22분 | `hasBlePermissions()`를 만든다 |
| 22–34분 | `showPermissionDialog()`를 만든다 |
| 34–48분 | `permissionLauncher`와 [권한 확인] 리스너를 넣고 허용·거절을 확인한다 |
| 48–60분 | 캡처 2·3을 찍고 두 파일과 함께 제출한다 |

### 1. 버튼, Manifest, Permissions.kt

1. `strings.xml`에 `check_permission`(`권한 확인`)을, `activity_main.xml`의 `retryButton` 아래·`batteryText` 위에 id가 `permissionButton`인 버튼을 넣는다. 글자는 `@string/check_permission`, 위 간격은 `16dp`다.
2. `AndroidManifest.xml`의 `<manifest>` 태그에 `xmlns:tools="http://schemas.android.com/tools"`가 이미 있는지 먼저 본다. 새 프로젝트 템플릿에는 보통 들어 있으니 있으면 그대로 두고, 없을 때만 한 줄 넣는다(두 번 넣으면 빌드 오류). 그다음 `<application` 위에 `uses-feature` 하나와 `uses-permission` 다섯 개를 넣는다. `<application>` 태그의 `tools:targetApi="31"` 같은 줄은 지우지 않는다. 정확한 내용은 [따라하기 9단계](walkthrough.md#9-manifest에-권한-선언하기)에 있다.
3. **New › Kotlin Class/File › File**로 `Permissions.kt`를 만들고 [제공 파일](examples/day2/Permissions.kt)의 내용을 붙여 넣는다. `Manifest`는 `android.Manifest`를 import한다.
4. 실행해 [권한 확인] 버튼이 보이면 다음으로 간다.

선언한 권한을 아래 표에 정리한다.

| 권한 | Android 12(API 31) 이상에서 요청하나 | Android 11(API 30) 이하에서 요청하나 |
|---|---|---|
| `BLUETOOTH_SCAN` |  |  |
| `BLUETOOTH_CONNECT` |  |  |
| `ACCESS_FINE_LOCATION` |  |  |

`blePermissions()` 코드를 읽고 채운다.

### 2. hasBlePermissions()

`onStop()` 아래에 `private fun hasBlePermissions(): Boolean`을 만든다.

```kotlin
private fun hasBlePermissions(): Boolean {
    for (permission in blePermissions()) {
        if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
            // 허용되지 않은 권한이 있다: false를 돌려주고 끝낸다
        }
    }
    // 반복을 끝까지 통과하면 true
}
```

- 틀은 그대로 복사하고 두 주석 자리에 `return false`와 `return true`를 한 줄씩 채운다. `for (permission in …)` 줄은 외우지 않고 복사한다.
- `return false`는 반복 **안**, `return true`는 반복 **밖**이다.
- `PackageManager`는 `android.content.pm.PackageManager`다.
- 아직 부르는 곳이 없다. 빌드만 되면 된다.

### 3. showPermissionDialog()

`hasBlePermissions()` 아래에 `private fun showPermissionDialog()`를 만든다. 대화상자는 아래 모양이다.

| 부분 | 내용 |
|---|---|
| 제목 | `권한이 필요합니다` |
| 본문 | `장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.` |
| 오른쪽 버튼 | `설정으로` — `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))`로 `startActivity` |
| 왼쪽 버튼 | `취소` — 할 일 없음(`null`) |

- `AlertDialog.Builder(this)`로 시작해 `.setTitle(…)`·`.setMessage(…)`·`.setPositiveButton("설정으로") { _, _ -> … }`·`.setNegativeButton("취소", null)`을 이어 붙이고 `.show()`로 끝낸다.
- `AlertDialog`는 Alt+Enter 목록에서 `androidx.appcompat.app.AlertDialog`를 고른다. `Settings`는 `android.provider.Settings`, `Uri`는 `android.net.Uri`다.
- 막히면 [따라하기 12단계](walkthrough.md#12-showpermissiondialog-만들기)를 본다.

### 4. 요청 틀과 [권한 확인]

1. 클래스 변수 자리, `batteryReceiver` 블록 아래에 요청 틀을 만든다.

```kotlin
private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
    // hasBlePermissions()가 true면 Toast "권한 OK"
    // 아니면 showPermissionDialog()
}
```

2. `onCreate` 안, `// 9.` 틀 아래에 [권한 확인] 리스너를 넣는다. 이미 허용이면 Toast `권한 OK`, 아니면 `permissionLauncher.launch(blePermissions())`.
3. 실행하고 아래 표를 채운다.

| 조작 | 예상 화면 | 실제 화면 |
|---|---|---|
| 처음 [권한 확인] |  |  |
| 권한 창에서 [허용] |  |  |
| 허용한 뒤 다시 [권한 확인] |  |  |
| 권한 창에서 [허용 안함] |  |  |
| 대화상자 [설정으로] |  |  |

- 요청 틀을 버튼 리스너 **안**에서 만들지 않는다. 클래스 변수 자리여야 한다.
- 이미 허용해 버렸으면 설정 › 앱 › Smart I/O Controller › 권한 › 근처 기기 › 허용 안함으로 되돌린 뒤 앱을 다시 실행한다.
- 같은 권한을 두 번 거절하면 이후에는 권한 창 없이 곧바로 대화상자가 뜬다. 코드가 틀린 것이 아니다.

### 5. 캡처 2·3

1. 권한 창에서 [허용 안함]을 누른 직후, 대화상자 `권한이 필요합니다`와 [설정으로]가 보이는 화면을 **캡처한다(캡처 2).**
2. [설정으로]를 누르고 `Smart I/O Controller` 앱 정보 화면을 **캡처한다(캡처 3).**

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 첫 줄이다. 파일 이름과 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 에뮬레이터에서 조금 다르게 보일 수 있다. Logcat 문구의 `@` 뒤 숫자는 실행마다 다르다.

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'BatteryManager'.` (같은 문구가 세 줄에 나온다) | `BatteryManager`에 커서를 두고 Alt+Enter(맥 ⌥+Enter) → `android.os.BatteryManager`를 import한다. 세 줄이 함께 고쳐진다 |
| `Unresolved reference 'batteryTxt'.` (내가 쓴 이름이 따옴표 안에 나온다) | Kotlin의 `binding.` 뒤 이름과 `activity_main.xml`의 `android:id="@+id/batteryText"`가 글자까지 같은지 본다 |
| `Modifier 'override' is not applicable to 'local function'.` | `override fun onStart()`가 `onCreate` **안**에 들어갔다. `onCreate`를 닫는 `}`가 `onStart`보다 위에 오게 옮긴다 |
| `Operator call is prohibited on a nullable receiver of type 'kotlin.Int?'. Use '?.'-qualified call instead.` | `val level = intent?.getIntExtra(…)` 끝에 `?: -1`이 빠졌다. 기본값을 붙여 `Int`로 만든다 |
| `Function invocation 'blePermissions()' expected.` | `launch(blePermissions)`에 괄호가 빠졌다. `launch(blePermissions())`로 쓴다 |
| (예상) 빌드는 되고 화면도 멀쩡한데, 화면을 돌린 뒤 Logcat(Error)에 `has leaked IntentReceiver` … `Are you missing a call to unregisterReceiver()?`. 홈으로 나갈 때는 이 메시지가 찍히지 않으니 회전으로 확인한다 | `onStop`에 `unregisterReceiver(batteryReceiver)`가 있는지 본다 |
| (예상) [연결] → [뒤로]로 돌아온 뒤 Battery를 바꿔도 문구가 그대로이고, 다시 [연결]을 누르면 앱이 멈춘다. Logcat에 `java.lang.IllegalArgumentException: Receiver not registered:` | 등록을 `onCreate`에 두었다. `registerReceiver`를 `onStart`로 옮겨 `onStop`의 해제와 짝을 맞춘다 |
| (예상) [권한 확인]을 눌러도 권한 창이 안 뜨고 곧바로 `권한이 필요합니다`가 뜬다. [설정으로]로 간 권한 목록에 "근처 기기"가 없다 | `AndroidManifest.xml`에 `uses-permission`이 있는지 본다. 선언하지 않은 권한은 요청하자마자 거절로 돌아온다 |
| (예상) 권한이 없는 상태에서 [권한 확인]을 누르는 순간 앱이 멈춘다. Logcat에 `is attempting to register while current state is RESUMED. LifecycleOwners must call register before they are STARTED.` | `registerForActivityResult`를 버튼 리스너 안에서 만들었다. `private val permissionLauncher = …`를 클래스 변수 자리로 옮긴다 |
| (예상) [설정으로]를 누르는 순간 앱이 멈춘다. Logcat에 `android.content.ActivityNotFoundException: No Activity found to handle Intent` | `Uri.parse("package:$packageName")`에서 `package:`가 빠졌는지 본다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 두 파일과 캡처 3장

1. **`MainActivity.kt`, `AndroidManifest.xml`**: 2일차 최종 코드
2. **캡처 1**: Battery 값을 100이 아닌 값으로 바꾼 뒤 `배터리 N% · 충전 중`(또는 `충전 안 함`)이 보이는 세로 연결 화면. 실기기는 값을 바꿀 수 없으니 상태 표시줄의 배터리 %와 같은 숫자면 된다
3. **캡처 2**: 권한을 거절한 뒤 연결 화면 위에 뜬 `권한이 필요합니다` 대화상자와 [설정으로] 버튼
4. **캡처 3**: [설정으로]를 눌러 열린 앱 정보 화면. 앱 이름 `Smart I/O Controller`가 보여야 한다

1일차 배터리 문구와 2일차 [권한 확인] → 권한 창까지 동작하면 기본 성공이다. 거절 대화상자와 설정 이동은 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: 배터리가 20% 이하이면 문구 끝에 ` · 충전 필요`를 붙인다. Charge level을 15로 바꿔 확인한다.
- 1일차: `onStart`의 등록 아래에 `Log.d("Battery", "등록")`, `onStop`의 해제 아래에 `Log.d("Battery", "해제")`를 넣고, Logcat `package:mine tag:Battery`로 홈·복귀·[연결]→[뒤로]마다 두 줄이 짝으로 찍히는지 본다.
- 2일차: 권한 창에서 [허용]하면 [권한 확인] 버튼 글자를 `권한 확인됨`으로 바꾼다.
- 2일차: [검색]을 누를 때 권한이 없으면 검색을 시작하지 않고 권한 요청 창을 먼저 띄운다(12주차에 실제 검색 버튼이 이렇게 동작한다).

추가 과제는 선택 사항이다.
