# 15주차 예제 — 기말고사 공개 리허설 (SmartIO starter·solution)

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)가 기준이다. 제공 라이브러리는 package `com.example.smartio.bleuno`다.
14주차 최종 앱에서 세 기능(권한 확인 흐름, LED 번호 토글과 응답 표시, 연결 시간 제한 안내)의 본문만 비운 것이 리허설 starter다. 새 문법은 없다.

- `rehearsal_starter/` — 1일차 리허설 시작 코드. 빌드·실행되고 `// TODO` 아홉 곳만 비어 있다(TODO 번호는 기능 번호라 (1)·(2)·(3) 세 가지). 시험 당일 받는 starter도 이런 모양이다.
- `rehearsal_solution/` — 자기 점검용 완성본. **14주차 [examples/day1](../../week14_ble_input_project/examples/day1)과 글자 단위로 같다.** 먼저 혼자 풀고 나서 비교한다.

만드는 순서는 [따라하기](../walkthrough.md)에 있다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | starter와 solution |
|---|---|---|
| [MainActivity.kt](rehearsal_starter/MainActivity.kt) → [완성](rehearsal_solution/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | TODO(1) 네 곳·TODO(3) 두 곳 본문만 다르다(starter 472행, 완성 493행) |
| [ControlActivity.kt](rehearsal_starter/ControlActivity.kt) → [완성](rehearsal_solution/ControlActivity.kt) | `… › ControlActivity.kt` | TODO(2) 세 곳 본문만 다르다(starter 247행, 완성 277행) |
| [ContactsReader.kt](rehearsal_starter/ContactsReader.kt) | `… › ContactsReader.kt` | 같다(11주차) |
| [bleuno/](rehearsal_starter/bleuno) 8개 | `… › com.example.smartio › bleuno` | 같다. 제공 [bleuno/src](../../../bleuno/src)와 같다 |
| [activity_main.xml](rehearsal_starter/activity_main.xml), [activity_control.xml](rehearsal_starter/activity_control.xml) | `app › res › layout` | 같다 |
| [strings.xml](rehearsal_starter/strings.xml), [colors.xml](rehearsal_starter/colors.xml), [res/values/themes.xml](rehearsal_starter/res/values/themes.xml) | `app › res › values` | 같다 |
| [AndroidManifest.xml](rehearsal_starter/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | 같다(10주차 BLE 권한, 11주차 연락처 권한) |

- 14주차 프로젝트가 그대로 있으면 **`MainActivity.kt`·`ControlActivity.kt` 두 파일만** 바꾼다. 나머지 15개는 14주차와 같다.
- `build.gradle.kts`는 이 폴더에 없다. 4주차에 만든 파일을 그대로 쓴다([4주차 examples/day1/build.gradle.kts](../../week04_fragments_navigation/examples/day1/build.gradle.kts)). 본시험 starter는 이 파일까지 들어 있는 프로젝트 폴더로 배포한다.
- `.kt` 파일 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
- starter에서 회색으로 보이는 import 네 줄(`MainActivity.kt`의 `android.net.Uri`·`kotlinx.coroutines.delay`, `ControlActivity.kt`의 `androidx.appcompat.app.AlertDialog`·`androidx.core.content.ContextCompat`)은 TODO를 채우면 쓰인다. 지우지 않는다.
- 연결 화면의 `private val useFake = true`는 starter 85행, 완성본 88행이다. 실보드로 시연할 때만 `false`로 바꾼다.

## 화면과 이름

TODO가 쓰는 이름은 모두 14주차에 이미 있다. 이번 주에 새로 생긴 id·문자열·색·파일은 없다.

| 종류 | 이름 | 화면에서 |
|---|---|---|
| id (`activity_main.xml`) | `permissionButton`, `stateText`, `scanProgress`, `scanButton`, `retryButton` | [권한 확인], 상태 글자, 원형 진행 표시, [검색], [다시 시도] |
| id (`activity_control.xml`) | `pinEdit`, `ledSwitch`, `logText` | `LED 번호 (0~3)` 칸, LED Switch, 명령 로그 |
| 색 (`colors.xml`) | `log_ok`, `log_error` | 명령 로그의 초록 글자, 빨간 글자 |
| 상수 (`bleuno/ConnState.kt`) | `ConnState.CONNECTING`, `ConnState.DISCOVERING` | `연결 중`, `서비스 확인 중` |
| 변수 | `permissionLauncher`, `connectTimeoutJob`, `client` | 요청 창 틀, 시간 제한 코루틴, 연결 화면의 클라이언트 |
| 함수 | `hasBlePermissions()`, `showPermissionDialog()`, `waitConnectTimeout()`, `isAllowedIndex()`, `pauseButtons()` | TODO가 채우거나 부르는 함수 |
| 제공 | `PermissionHelper.required()`, `Bleuno.client?.send(…)`, `BleunoMessage.result(json)`·`BleunoMessage.message(json)` | 권한 목록, 명령 보내기, 응답에서 값 꺼내기 |

## TODO와 완성 코드 줄

| TODO | starter 위치 | 할 일 | 완성본 줄 |
|---|---|---|---|
| (1) | `MainActivity.kt` 13번 `hasBlePermissions()` 388~391행(아래 392행 `return true`는 남긴다) | `for`로 권한을 하나씩 확인, 허용 안 된 것이 있으면 `return false` | 392~399행 |
| (1) | 14번 `showPermissionDialog()` 397~400행 | AlertDialog, [설정으로]는 이 앱 정보 화면 | 402~413행 |
| (1) | 클래스 안 `permissionLauncher`의 `{ _ -> }` 65~66행 | 다시 확인해 `권한 OK` 또는 14번 | 64~70행 |
| (1) | 12번 [권한 확인] 리스너 282~284행 | 허용이면 `권한 OK`, 아니면 `permissionLauncher.launch(…)` | 284~290행 |
| (2) | `ControlActivity.kt` 12번 `isAllowedIndex()` 200~202행(아래 203행 `return false`는 남긴다) | 0~3 또는 -1이면 `true` | 226~234행 |
| (2) | 2번 LED Switch 리스너 59~63행 | 빈 칸 → 허용 번호 → `on`/`off` 보내기·로그·`pauseButtons()` | 58~81행 |
| (2) | onStart 8번의 `} else if (result != null) {` 가지 179~182행 | 응답 로그, 오류면 빨간 글자·창, `ok`면 초록 | 195~210행 |
| (3) | `MainActivity.kt` 50번 `startConnectTimeout()` 457~459행 | 앞 코루틴 취소, `launch`로 새로 시작해 보관, 51번 부르기 | 468~473행 |
| (3) | 51번 `waitConnectTimeout()` 466~470행 | 10초 뒤 아직 연결 중이면 Toast·끊기·화면 되돌리기 | 478~492행 |

## 1. 권한을 하나씩 확인하기 — `for`와 `checkSelfPermission`

```kotlin
private fun hasBlePermissions(): Boolean {
    for (permission in PermissionHelper.required()) {
        if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
            return false
        }
    }
    return true
}
```

| 기기 | `PermissionHelper.required()`가 주는 권한 | 모두 허용 | 하나라도 아님 |
|---|---|---|---|
| Android 12(API 31) 이상 | `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` (설정 화면 이름 `근처 기기`) | `true` | `false` |
| Android 11 이하 | `ACCESS_FINE_LOCATION` (설정 화면 이름 `위치`) | `true` | `false` |

- `for (permission in …)`은 6주차 `for (i in 5 downTo 1)`과 같은 모양으로 목록의 칸을 하나씩 꺼낸다.
- 허용 안 된 권한을 만나면 그 자리에서 `return false`로 함수를 끝낸다. 끝까지 돌았으면 모두 허용이라 마지막 줄 `return true`에 닿는다.
- `return true`를 지우면 `Missing return statement.`로 빌드가 멈춘다. `Boolean` 함수는 끝에서 돌려줄 값이 있어야 한다.

## 2. 요청 창과 결과 받기 — `registerForActivityResult` 틀과 `launch`

```kotlin
// 클래스 안(onCreate 밖)
private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
    if (hasBlePermissions()) {
        Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
    } else {
        showPermissionDialog()
    }
}

// onCreate 12번
binding.permissionButton.setOnClickListener {
    if (hasBlePermissions()) {
        Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
    } else {
        permissionLauncher.launch(PermissionHelper.required())
    }
}
```

| 실행 결과 (에뮬레이터 API 33) | 화면 |
|---|---|
| 권한을 허용한 상태에서 [권한 확인] | 요청 창 없이 Toast `권한 OK` |
| 권한을 끈 상태에서 [권한 확인] | 시스템의 `근처 기기` 권한 요청 창 |
| 요청 창에서 허용 | Toast `권한 OK` |
| 요청 창에서 거절 | `권한이 필요합니다` 창(3번) |

- 요청 틀은 **화면이 시작되기 전에** 만들어야 해서 클래스 안에 둔다. 버튼은 이미 만든 틀의 `launch`만 부른다.
- 리스너 안에서 `registerForActivityResult`를 새로 만들어도 빌드는 된다. 하지만 권한이 없는 기기에서 누르는 순간 앱이 멈춘다(Logcat `java.lang.IllegalStateException: LifecycleOwner com.example.smartio.MainActivity@… is attempting to register while current state is RESUMED. LifecycleOwners must call register before they are STARTED.`).
- `{ _ -> }`의 `_`는 넘어오는 결과를 쓰지 않는다는 뜻이다. 결과 대신 13번으로 지금 권한을 다시 확인한다.

## 3. 거절했을 때 — AlertDialog와 암시적 Intent

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
| 요청 창에서 거절한 직후 | 제목 `권한이 필요합니다`, 문구, [취소]·[설정으로] |
| [설정으로] | Smart I/O Controller의 앱 정보 화면(여기서 권한 › 근처 기기를 허용할 수 있다) |
| [취소] | 창만 닫힌다 |

- 12주차 40번 `showLocationDialog()`와 같은 모양이다. 다른 곳은 제목·문구와 Intent 두 줄뿐이다.
- `"package:$packageName"`의 `$packageName`은 이 앱의 package 이름(`com.example.smartio`)으로 바뀐다. 암시적 Intent는 "무엇을 할지(ACTION)와 대상"만 적으면 시스템이 맞는 화면을 연다(10주차).

## 4. 허용 번호만 보내기 — `listOf(…).contains(…)`와 `send`

```kotlin
private fun isAllowedIndex(index: Int): Boolean {
    if (listOf(0, 1, 2, 3).contains(index)) {
        return true
    }
    if (index == -1) {
        return true
    }
    return false
}
```

```kotlin
binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
    val pin = binding.pinEdit.text.toString()
    if (pin.isEmpty()) {
        Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
    } else if (isAllowedIndex(pin.toInt()) == false) {
        Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
    } else if (isChecked) {
        val index = pin.toInt()
        Bleuno.client?.send("on $index")
        binding.logText.append("on $index\n")
        pauseButtons()
    } else {
        val index = pin.toInt()
        Bleuno.client?.send("off $index")
        binding.logText.append("off $index\n")
        pauseButtons()
    }
}
```

| LED 번호 칸 → Switch (Fake, `준비됨`) | 화면 | Logcat `tag:BLE` |
|---|---|---|
| 빈 칸 | Toast `LED 번호를 입력하세요` | 새 줄 없음 |
| `9` | Toast `허용되지 않는 번호` | 새 줄 없음 |
| `3` 켜기 | 명령 로그 `on 3`, Switch·[전체 끄기] 0.3초 회색 | `writeCharacteristic(가짜): "on 3"` |
| `3` 끄기 | 명령 로그 `off 3` | `writeCharacteristic(가짜): "off 3"` |

- 순서가 중요하다. 빈 칸 검사를 먼저 해야 뒤의 `pin.toInt()`가 안전하다. 순서를 바꾸면 빌드는 되지만 빈 칸에서 앱이 멈춘다(Logcat `java.lang.NumberFormatException: For input string: ""`).
- `isAllowedIndex(pin)`처럼 글자를 넘기면 `Argument type mismatch: actual type is 'kotlin.String', but 'kotlin.Int' was expected.`
- 명령 규약은 **명령 이름 + 띄어쓰기 한 칸 + 번호**다. `"on$index"`라 쓰면 빌드는 되고 보드가 `{"result":"fail","ms":"unknown command"}`로 답한다([bleuno README 2절](../../../bleuno/README.md#2-명령과-응답)).

## 5. 응답 표시 — `onMessage`와 `BleunoMessage.result`

```kotlin
} else if (result != null) {
    binding.logText.append("응답: $json\n")
    if (result != "ok") {
        val message = BleunoMessage.message(json) ?: ""
        binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
        AlertDialog.Builder(this)
            .setTitle("보드가 오류를 알렸습니다")
            .setMessage("응답: $result · $message")
            .setPositiveButton("확인", null)
            .show()
    } else {
        binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_ok))
    }
}
```

| 받은 JSON | `result` | 명령 로그 | 창 |
|---|---|---|---|
| `{"result":"ok","ms":"led(s) on"}` | `"ok"` | `응답: {"result":"ok","ms":"led(s) on"}` 초록 | 없음 |
| `{"result":"fail","ms":"unknown command"}` | `"fail"` | `응답: {"result":"fail","ms":"unknown command"}` 빨강 | `보드가 오류를 알렸습니다` / `응답: fail · unknown command` |
| `{"result":"ok","value":"[24.5,40.0]"}` (`dht11`) | `"ok"` | 들어가지 않는다(앞의 23번 가지가 입력 이력에 넣는다) | 없음 |
| `{"event":"input","index":0,"value":1}` (가짜 보드가 10초마다) | `null` | 들어가지 않는다(22번 가지) | 없음 |

- 이 가지는 `onStart`에서 등록한 `onMessage { json -> }` 안의 마지막 가지다. 응답은 명령 하나마다 한 줄씩, 메인 스레드에서 오므로 View를 바로 바꿔도 된다.
- `BleunoMessage.message(json)`은 `"ms"` 키가 없으면 `null`인 `String?`이라 `?: ""`로 받는다.
- 로그 색은 TextView 전체 글자색이다. 한 번 빨개지면 다음 `ok` 응답에서 초록으로 되돌린다.

## 6. 연결 시간 제한 — `Job` 보관과 `suspend fun`의 `delay`

```kotlin
private fun startConnectTimeout() {
    connectTimeoutJob?.cancel()
    connectTimeoutJob = lifecycleScope.launch {
        waitConnectTimeout()
    }
}

private suspend fun waitConnectTimeout() {
    delay(10000)
    val state = client.connectionState.value
    if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
        Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
        client.disconnect()
        binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
        binding.retryButton.visibility = View.VISIBLE
    }
}
```

| 실행 결과 | 화면 |
|---|---|
| Fake 목록 줄 탭 | 약 2초 만에 `준비됨`. 10초가 지나도 안내가 없다(정상) |
| (확인용) `delay(10000)`을 잠시 `delay(1000)`으로 바꾸고 목록 줄 탭 | 약 1초 뒤 상태 `연결 시간 초과 — [다시 시도]를 누르세요`, [검색] 켜짐, [다시 시도] 보임. Toast `연결 시간이 초과되었습니다`는 먼저 뜬 `선택: …` Toast가 사라진 뒤(줄을 누르고 약 2~3초 뒤) 뜬다. Logcat `connectGatt(가짜): 00:11:22:33:44:01` → `disconnect(가짜) → 연결 안 됨`. 확인 뒤 되돌린다 |
| 연결 중에 회전 | onCreate 52번이 시간 제한을 다시 건다(10초를 처음부터 센다) |

- `waitConnectTimeout()`은 코루틴 밖에서 부를 수 없다. `startConnectTimeout()`에서 바로 부르면 `Suspend function 'suspend fun waitConnectTimeout(): Unit' should be called only from a coroutine or another suspend function.`
- `launch { }` 안에 `Toast.makeText(this, …)`를 바로 쓰면 그 `this`가 Activity가 아니라서 `None of the following candidates is applicable:`와 `Unresolved reference 'show'.`가 난다. Toast는 Activity의 함수인 51번 안에 둔다.
- `connectTimeoutJob?.cancel()`을 먼저 해야 앞 연결의 예약이 새 연결을 끊지 않는다(6주차 `scanJob?.cancel()`과 같다).

## 채점표 항목과 코드 줄

| 채점표 항목(구현 15) | 다시 쓰는 개념(처음 배운 주) | `rehearsal_solution` 줄 |
|---|---|---|
| 권한·SharedPreferences 3 | Manifest 선언(10주) → `checkSelfPermission` 반복(10·12주) → 요청 틀과 `launch`(10주) → 결과 `{ _ -> }` → 거절 AlertDialog와 암시적 Intent(10주). 저장·복원(11·14주)은 starter 완성분 | `AndroidManifest.xml` 10~26행, `MainActivity.kt` 64~70행, 284~290행, 392~399행, 402~413행, 저장 133·306·321~331행 |
| `send`·`onMessage`·재연결 3 | `send("on $index")`와 명령 규약, `onMessage { json -> }`와 `BleunoMessage.result/message`, 오류 색·창, 허용 번호(13주). 재연결 버튼(14주)은 starter 완성분 | `ControlActivity.kt` 58~81행, 195~210행, 226~234행, `MainActivity.kt` 350~358행 |
| 코루틴 timeout·취소·오류 3 | `Job` 보관과 `?.cancel()`, `lifecycleScope.launch`, `suspend fun`과 `delay`(6주), `connectionState.value`와 `listOf(…).contains(…)`(7·13·14주) | `MainActivity.kt` 108행, 468~473행, 478~492행 |
| UI·이벤트 3 | `setOnCheckedChangeListener`(4주), `isEmpty()`·`.toInt()`·문자열 템플릿(4주), `Toast`(3주), `isEnabled`로 잠깐 막기(5·13주) | `ControlActivity.kt` 58~81행, 238~250행 |
| 상태 보존·StateFlow 3 | `connectionState` collect 틀(7·12주), 회전하면 시간 제한 다시 걸기(14주) — starter 완성분 | `MainActivity.kt` 235~281행, 335~337행, `ControlActivity.kt` 90~113행 |

세부 기준은 [채점표](../rubric.md)에 있다.

## 공식 참고 자료

- [앱 권한 요청 — Android Developers](https://developer.android.com/training/permissions/requesting)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
