# 15주차 따라하기 — 기말고사 공개 리허설과 시험 준비

14주차 `SmartIO` 프로젝트를 이어서 쓴다. 시작점은 14주차 완성본([examples/day1](../week14_ble_input_project/examples/day1))이다. 처음에는 그대로 따라 하고, 각 단계의 결과가 화면에 보이면 다음 단계로 넘어간다.
리허설은 시험 연습이다. [실습지](lab.md)로 먼저 혼자 풀어 보고, 막힌 단계만 여기서 연다. 1~2단계(14주차 확인과 starter 넣기)는 시험 당일 강의자가 끝내서 나눠 주는 부분이다.

이번 주에 바꾸는 파일은 두 개뿐이다. `MainActivity.kt`·`ControlActivity.kt`를 starter로 바꾼 뒤 TODO를 채운다.
`AndroidManifest.xml`, `ContactsReader.kt`, `activity_main.xml`, `activity_control.xml`, `strings.xml`, `colors.xml`, `res/values/themes.xml`, `bleuno` 패키지 8개는 14주차 그대로 둔다. 전체 내용은 [부록 A](#부록-a--바꾸지-않는-파일-전체)와 [부록 B](#부록-b--제공-bleuno-파일-전체)에 있다.
새로 배우는 문법은 없고, 넣을 import도 없다(필요한 import는 starter에 모두 들어 있다).

에뮬레이터는 API 33 이상 이미지를 쓰고 연결 화면의 `useFake = true`는 그대로 둔다. 2일차 시연 준비(17단계)에서만 실기기와 보드를 쓴다.

## 1일차

### 1. 14주차 프로젝트 확인하기

1. Android Studio에서 `SmartIO` 프로젝트를 열고 `Run ▶`을 누른다.
2. 아래쪽 **Logcat** 창의 필터에 `package:mine tag:BLE`를 넣어 둔다.
3. [검색]을 누르고 목록에 `ESP32_BLE_FAKE1 (00:11:22:33:44:01)`이 들어오면 그 줄을 누른다. 상태가 `연결 중` → `서비스 확인 중` → `준비됨`이 되면 [제어 화면]을 누른다.
4. 입력 칸에 `3`을 넣고 LED Switch를 켠다. 명령 로그에 아래 두 줄이 쌓이면 14주차 앱이 완성된 상태다.

```text
on 3
응답: {"result":"ok","ms":"led(s) on"}
```

5. [뒤로]로 연결 화면에 돌아와 [권한 확인]을 눌러 본다. `권한 OK`가 뜨면 이 에뮬레이터에는 권한이 이미 허용되어 있다.

로그가 다르거나 실행되지 않으면 14주차 완성본 파일로 먼저 맞춘다. 파일마다 넣을 위치는 [예제 설명의 파일 표](examples/README.md#파일과-넣을-위치)에 있다.

### 2. starter 두 파일로 바꾸기

1. 브라우저에서 [examples/rehearsal_starter/MainActivity.kt](examples/rehearsal_starter/MainActivity.kt)(472행)를 열어 전체를 복사한다. Project 창에서 `app › kotlin+java › com.example.smartio › MainActivity.kt`를 열고 **전체를 선택해 붙여 넣는다.** 첫 줄 `package com.example.smartio`는 내 프로젝트와 같다.
2. 같은 방법으로 `ControlActivity.kt` 전체를 [examples/rehearsal_starter/ControlActivity.kt](examples/rehearsal_starter/ControlActivity.kt)(247행)로 바꾼다.

   두 파일은 14주차 완성본에서 TODO 아홉 곳의 **본문만** 비운 것이다. 함수를 여는 줄과 닫는 `}`, 그 위 주석, import는 한 줄도 바뀌지 않았다. 비운 자리는 아래처럼 TODO 주석만 남아 있다(`MainActivity.kt` 13번).

```kotlin
    // 13. PermissionHelper.required()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    //     12주차 1일차: 10주차 blePermissions()를 bleuno 패키지의 PermissionHelper.required()로 바꿨다. 돌려주는 권한 목록은 같다.
    private fun hasBlePermissions(): Boolean {
        // TODO(1) 권한 확인 흐름 — 권한을 하나씩 확인하기(15주차 1일차 리허설).
        //         for로 PermissionHelper.required()의 권한을 하나씩 꺼내 ContextCompat.checkSelfPermission(this, 권한)으로 확인한다.
        //         PackageManager.PERMISSION_GRANTED가 아닌 권한이 하나라도 있으면 그 자리에서 false를 돌려준다.
        //         아래 return true는 "모두 허용"일 때 돌려주는 줄이다. 지우지 말고 그 위에 채운다(지우면 빌드가 안 된다).
        return true
    }
```

3. 두 파일에서 import 네 줄이 **회색**으로 보인다. `MainActivity.kt`의 `import android.net.Uri`·`import kotlinx.coroutines.delay`, `ControlActivity.kt`의 `import androidx.appcompat.app.AlertDialog`·`import androidx.core.content.ContextCompat`이다. 아직 쓰는 줄이 비어 있을 뿐 TODO를 채우면 쓴다. **지우지 않는다.**
   - 메뉴 **Code › Optimize Imports**를 누르지 않는다.
   - **Settings(맥 Settings…) › Editor › General › Auto Import**의 **Optimize imports on the fly**가 켜져 있으면 끈다. 켜져 있으면 저장할 때 회색 줄이 저절로 지워진다.
4. `Run ▶`을 누르고 아래를 확인한다.

| 조작 | 보여야 할 것 |
|---|---|
| 앱 시작 | 14주차와 같은 연결 화면. `마지막 장치: …`, [끊김 시험] 회색 |
| [권한 확인] | **아무 일도 없다**(TODO(1)) |
| [검색] → `ESP32_BLE_FAKE1` 줄 탭 | 권한 요청 창 없이 검색되고 `연결 중` → `서비스 확인 중` → `준비됨` |
| [제어 화면] → `3` → LED Switch 켜기 | Switch 모양만 바뀐다. 명령 로그·Toast·Logcat 전송 줄이 없다(TODO(2)) |
| [전체 끄기] | 명령 로그 `off -1`. 약 0.3초 뒤 `응답:` 줄이 **붙지 않는다** |
| Logcat `tag:BLE` | `writeCharacteristic(가짜): "off -1"` → `onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) off"}` |

   대답은 오는데 받는 가지가 비어 있어서 로그에 붙지 않는 것이다. [온습도 받기 시작], [끊김 시험] → [재연결]은 14주차와 같이 동작한다(완성된 기능).

- starter의 13번 `hasBlePermissions()`는 비어 있어서 늘 `true`를 돌려준다. 그래서 TODO(1)을 채우기 전에도 [검색]이 곧바로 검색하고, TODO(2)·(3)을 먼저 풀어도 제어 화면까지 갈 수 있다. 가짜 클라이언트는 권한 없이도 동작한다.

### 3. TODO 아홉 곳 찾기

메뉴 **View › Tool Windows › TODO**를 열면 TODO가 모여 보인다. 줄을 더블클릭하면 그 자리로 간다.

| TODO | 파일 | 자리(주석 번호) | 할 일 | 단계 |
|---|---|---|---|---|
| (1) | `MainActivity.kt` | 13번 `private fun hasBlePermissions(): Boolean {` 안 | 권한을 하나씩 확인 | 4 |
| (1) | `MainActivity.kt` | 14번 `private fun showPermissionDialog() {` 안 | 거절했을 때 안내 창 | 5 |
| (1) | `MainActivity.kt` | 클래스 안 `permissionLauncher = registerForActivityResult(…) { _ ->` 안 | 요청 창의 결과 받기 | 6 |
| (1) | `MainActivity.kt` | onCreate 12번 `binding.permissionButton.setOnClickListener {` 안 | [권한 확인] 버튼 | 7 |
| (2) | `ControlActivity.kt` | 12번 `private fun isAllowedIndex(index: Int): Boolean {` 안 | 보내도 되는 번호인지 확인 | 8 |
| (2) | `ControlActivity.kt` | onCreate 2번 `binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->` 안 | `send`로 명령 보내기 | 9 |
| (2) | `ControlActivity.kt` | onStart 8번 `onMessage { json ->` 안의 `} else if (result != null) {` 가지 | 응답 표시 | 10 |
| (3) | `MainActivity.kt` | 50번 `private fun startConnectTimeout() {` 안 | 시간 제한 걸기 | 11 |
| (3) | `MainActivity.kt` | 51번 `private suspend fun waitConnectTimeout() {` 안 | 10초 기다린 뒤 안내하기 | 12 |

**불리는 함수 → 부르는 곳** 순서로 채운다. 한 단계를 끝낼 때마다 빌드가 된다. 함수를 여는 줄·닫는 `}`·그 위 주석은 starter에 이미 있으므로 **TODO 주석 줄만 지우고** 그 자리에 쓴다.

### 4. TODO(1) ① hasBlePermissions() — 권한을 하나씩 확인하기

`MainActivity.kt`의 13번 `private fun hasBlePermissions(): Boolean {` 아래에서 `// TODO(1)`로 시작하는 **주석 네 줄**을 지우고, 남아 있는 `return true` 줄 **위**에 `for` 다섯 줄을 넣는다. 함수 전체가 아래 모양이 되면 된다.

```kotlin
    // 13. PermissionHelper.required()의 권한을 하나씩 checkSelfPermission으로 확인한다. 하나라도 허용 안 됐으면 false(10주차 2일차).
    //     12주차 1일차: 10주차 blePermissions()를 bleuno 패키지의 PermissionHelper.required()로 바꿨다. 돌려주는 권한 목록은 같다.
    private fun hasBlePermissions(): Boolean {
        for (permission in PermissionHelper.required()) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        return true
    }
```

- `for (permission in PermissionHelper.required())`: 6주차 `for (i in 5 downTo 1)`과 같은 모양으로 권한 목록의 칸을 하나씩 꺼낸다. Android 12 이상이면 `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT` 두 개다.
- `ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED`: 허용되지 않았으면 그 자리에서 `return false`로 함수를 끝낸다. 22번 [연락처 보기]의 `checkSelfPermission` 줄과 같은 모양이다. `ContextCompat`·`PackageManager` import는 이미 쓰이고 있다.
- 마지막 `return true`는 "끝까지 돌았다 = 모두 허용"일 때 돌려주는 줄이다. 지우면 `Missing return statement.`로 빌드가 멈춘다.

실행한다. 권한이 이미 허용된 에뮬레이터면 [검색]이 전과 같다. 이제 권한을 끈 상태를 만들어 본다.

1. 에뮬레이터 홈에서 Smart I/O Controller 아이콘을 길게 누르고 **앱 정보 › 권한 › 근처 기기 › 허용 안함**을 고른다.
2. 앱을 다시 열고 [검색]을 누른다. 시스템의 `근처 기기` 권한 요청 창이 뜬다(25번 [검색]이 13번을 부르기 시작했다).
3. 허용을 눌러도 **아무 일도 없다.** 요청 창의 결과를 받는 곳이 아직 비어 있기 때문이다(6단계). [검색]을 다시 누르면 검색된다.

### 5. TODO(1) ② showPermissionDialog() — 거절했을 때 안내 창

14번 `private fun showPermissionDialog() {` 아래의 `// TODO(1)` **주석 네 줄**을 지우고 그 자리에 넣는다. 함수 전체는 아래와 같다.

```kotlin
    // 14. 거절했을 때 보여 주는 AlertDialog. [설정으로]를 누르면 이 앱의 정보(권한) 화면을 연다(10주차 2일차).
    private fun showPermissionDialog() {
        AlertDialog.Builder(this)
            .setTitle("권한이 필요합니다")
            .setMessage("장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.")
            .setPositiveButton("설정으로") { _, _ ->
                // 암시적 Intent: 무엇을 할지(ACTION)와 대상(package:앱 이름)만 적으면 시스템이 맞는 화면을 찾아 연다.
                val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))
                startActivity(intent)
            }
            .setNegativeButton("취소", null)
            .show()
    }
```

- 12주차 40번 `showLocationDialog()`와 같은 모양이다. 제목·문구와 [설정으로] 안의 Intent 두 줄이 다르다.
- `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))`: 이 앱의 정보 화면을 여는 암시적 Intent다(10주차). `$packageName`은 `com.example.smartio`로 바뀐다.
- 회색이던 `import android.net.Uri`가 이제 보통 색이 된다. `Uri`가 빨간색이면 import가 지워진 것이다. `Uri`에 커서를 두고 **Alt+Enter**(맥 ⌥+Enter) → **Import** → `android.net.Uri`를 고른다.

메뉴 **Build › Make Project**로 빌드만 확인한다. 이 함수를 부르는 곳(6단계)이 아직 비어 있어 화면은 바뀌지 않는다.

### 6. TODO(1) ③ permissionLauncher — 요청 창의 결과 받기

클래스 안(onCreate 밖) `private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->` 아래의 `// TODO(1)` **주석 두 줄**을 지우고 그 자리에 넣는다. 위 주석 두 줄부터 닫는 `}`까지는 아래와 같다.

```kotlin
    // 10주차 2일차: 권한 요청 창을 띄우고 결과를 받는 틀. 화면이 시작되기 전에 만들어 두어야 하므로 클래스 안(onCreate 밖)에 둔다.
    // 사용자가 요청 창에서 고르면 { _ -> … }가 불린다. 넘어오는 결과는 쓰지 않고(_), 13번 함수로 지금 권한을 다시 확인한다.
    private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ ->
        if (hasBlePermissions()) {
            Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
        } else {
            showPermissionDialog()
        }
    }
```

- 사용자가 요청 창에서 허용이나 거절을 고르면 `{ _ -> }`가 불린다. 넘어온 결과(`_`)는 쓰지 않고 13번으로 지금 권한을 다시 확인한다.
- 바로 아래 11주차 `contactsLauncher`와 같은 모양이다. 이 중괄호는 클래스 안에 있는 틀이라 `this`가 Activity다. Toast에 그대로 쓴다.
- 요청 틀(`registerForActivityResult`)은 새로 만들지 않는다. 화면이 시작되기 전에 만들어야 하므로 이미 클래스 안에 있다.

실행한다. 4단계처럼 권한을 끈 뒤 [검색]을 누른다.

| 조작 | 보여야 할 것 |
|---|---|
| 요청 창에서 허용 | Toast `권한 OK`. [검색]을 한 번 더 누르면 검색된다 |
| 권한을 다시 끄고 [검색] → 요청 창에서 거절 | `권한이 필요합니다` 창. 문구 `장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.`, 버튼 [취소]·[설정으로] |
| [설정으로] | Smart I/O Controller의 앱 정보 화면. 뒤로 가기로 앱에 돌아온다 |

같은 권한을 여러 번 거절하면 Android가 요청 창을 더 띄우지 않고 곧바로 결과를 돌려줄 수 있다. 그때는 [검색]을 누르자마자 `권한이 필요합니다` 창이 뜬다(예상). 앱 정보에서 권한을 다시 바꾸면 요청 창이 다시 뜬다.

### 7. TODO(1) ④ [권한 확인] 버튼

onCreate 12번 `binding.permissionButton.setOnClickListener {` 아래의 `// TODO(1)` **주석 세 줄**을 지우고 그 자리에 넣는다. 리스너를 여는 줄은 starter에 있으므로 새로 쓰지 않는다.

```kotlin
        // 12. [권한 확인] 버튼: 이미 모두 허용이면 "권한 OK", 하나라도 없으면 요청 창을 띄운다(10주차 2일차).
        binding.permissionButton.setOnClickListener {
            if (hasBlePermissions()) {
                Toast.makeText(this, "권한 OK", Toast.LENGTH_SHORT).show()
            } else {
                permissionLauncher.launch(PermissionHelper.required())
            }
        }
```

- 이미 모두 허용이면 요청 창 없이 `권한 OK`, 하나라도 없으면 6단계의 틀로 요청 창을 띄운다. 25번 [검색]의 첫 가지에 같은 `permissionLauncher.launch(PermissionHelper.required())` 줄이 있다.
- 리스너 줄을 한 번 더 쓰다가 `binding.permisionButton`처럼 id 철자가 틀리면 `Unresolved reference 'permisionButton'.`이 난다.

실행한다.

| 조작 | 보여야 할 것 |
|---|---|
| 권한이 허용된 상태에서 [권한 확인] | 요청 창 없이 Toast `권한 OK` |
| 권한을 끈 상태에서 [권한 확인] | `근처 기기` 권한 요청 창 → 허용하면 `권한 OK`, 거절하면 `권한이 필요합니다` 창 |

TODO(1)이 끝났다. 권한 흐름에는 Logcat `tag:BLE` 줄이 없다. 다음 단계로 가기 전에 권한을 **허용**해 둔다.

### 8. TODO(2) ① isAllowedIndex() — 보내도 되는 번호인지 확인하기

`ControlActivity.kt`의 12번 `private fun isAllowedIndex(index: Int): Boolean {` 아래에서 `// TODO(2)` **주석 세 줄**을 지우고, 남아 있는 `return false` 줄 **위**에 넣는다. 위 주석부터 함수 끝까지는 아래와 같다.

```kotlin
    // 12. 보드에 보내도 되는 번호면 true, 아니면 false(13주차 2일차).
    //     수업 보드의 LED 번호는 0~3이고, -1은 "전체"라는 약속이다(7번 [전체 끄기]). 입력 칸은 inputType이 number라 -를 적을 수 없다.
    //     펌웨어는 번호 범위를 확인하지 않아서 이 밖의 번호를 보내면 보드가 어떻게 될지 모른다. 그래서 보내기 전에 앱이 막는다.
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

- `listOf(0, 1, 2, 3).contains(index)`: 13주차 오늘 문법이다. 수업 보드의 LED 번호는 0~3이고, `-1`은 "전체"라는 약속이라 따로 허용한다.
- 마지막 `return false`는 "그 밖의 번호"일 때 돌려주는 줄이다. 지우면 빌드가 멈춘다.

**Build › Make Project**로 빌드만 확인한다. 이 함수를 부르는 Switch(9단계)가 아직 비어 있다.

### 9. TODO(2) ② LED Switch에서 명령 보내기

onCreate 2번 `binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->` 아래의 `// TODO(2)` **주석 다섯 줄**을 지우고 그 자리에 넣는다. 리스너 전체는 아래와 같다.

```kotlin
        binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
            val pin = binding.pinEdit.text.toString()
            if (pin.isEmpty()) {
                Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
            } else if (isAllowedIndex(pin.toInt()) == false) {
                // 11. 허용되지 않는 번호면 보드에 보내지 않고 Toast로 알린다. 번호 확인은 12번 함수가 한다(13주차 2일차).
                Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
            } else if (isChecked) {
                // 5. 입력한 글자를 숫자(LED 번호)로 바꿔 "on 번호" 명령을 보드에 보내고, 보낸 명령을 로그에 남긴다(13주차 1일차).
                //    send는 끝에 "\n"을 붙여 차례대로 보낸다. Bleuno.client가 없으면(null) ?.에서 멈추고 아무것도 보내지 않는다.
                val index = pin.toInt()
                Bleuno.client?.send("on $index")
                binding.logText.append("on $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다. 끄고 켜는 일은 15번 함수가 한다(13주차 2일차).
                pauseButtons()
            } else {
                // 6. 끄면 "off 번호" 명령을 보낸다. 5번과 같은 모양이다(13주차 1일차).
                val index = pin.toInt()
                Bleuno.client?.send("off $index")
                binding.logText.append("off $index\n")
                // 14. 보낸 직후 300ms 동안 버튼을 꺼 둔다(13주차 2일차).
                pauseButtons()
            }
        }
```

- 순서는 **빈 칸 → 허용 번호 → 켜기/끄기**다. 빈 칸 검사를 먼저 해야 뒤의 `pin.toInt()`가 안전하다.
- `isAllowedIndex(pin.toInt())`: 칸의 글자(`String`)를 숫자로 바꿔 넘긴다. `pin`을 그대로 넘기면 `Argument type mismatch: actual type is 'kotlin.String', but 'kotlin.Int' was expected.`
- `Bleuno.client?.send("on $index")`: 명령 이름, 띄어쓰기 한 칸, 번호. 7번 [전체 끄기]가 같은 모양(`send` → `append` → `pauseButtons()`)이다.
- `Toast`·`Bleuno` import는 이미 쓰이고 있다.

실행하고 [검색] → 줄 탭 → `준비됨` → [제어 화면]으로 들어간다.

| 조작 | 보여야 할 것 |
|---|---|
| 번호 칸을 비운 채 Switch | Toast `LED 번호를 입력하세요`(Switch 모양은 바뀐다) |
| `9` → Switch | Toast `허용되지 않는 번호`, 명령 로그 새 줄 없음 |
| `3` → Switch 켜기 | 명령 로그 `on 3`, Switch·[전체 끄기]가 약 0.3초 회색 |
| Switch 끄기 | 명령 로그 `off 3` |

Logcat `tag:BLE`에는 `writeCharacteristic(가짜): "on 3"` 다음에 `onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) on"}`이 찍힌다. 대답은 왔지만 로그에 `응답:` 줄은 아직 없다(10단계).

### 10. TODO(2) ③ 응답 표시

onStart 8번 `Bleuno.client?.onMessage { json ->` 안, 마지막 가지 `} else if (result != null) {` 아래의 `// TODO(2)` **주석 네 줄**을 지우고 그 자리에 넣는다. 가지 전체는 아래와 같다.

```kotlin
            } else if (result != null) {
                binding.logText.append("응답: $json\n")
                // 16. result가 "ok"가 아니면(err·fail) 로그 글자를 colors.xml의 빨간색으로 바꾸고, "ms"(설명) 값을 꺼내 AlertDialog로 알린다(13주차 2일차).
                //     ok면 초록색으로 되돌린다. 응답은 onStart~onStop 사이(거의 항상 화면이 보이는 동안)에만 받으므로 여기서 창을 띄운다.
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

- `binding.logText.append("응답: $json\n")`: 받은 JSON 한 줄을 그대로 로그에 쌓는다(13주차 1일차).
- `result != "ok"`면 `R.color.log_error`(빨강)로 바꾸고 AlertDialog로 알린다. `BleunoMessage.message(json)`은 `String?`이라 `?: ""`로 받는다. `ok`면 `R.color.log_ok`(초록)로 되돌린다.
- 회색이던 `AlertDialog`·`ContextCompat` import가 보통 색이 된다. 빨간색이면 그 글자에서 **Alt+Enter**(맥 ⌥+Enter) → **Import**로 `androidx.appcompat.app.AlertDialog`, `androidx.core.content.ContextCompat`을 고른다.
- 앞의 22번(입력 이벤트)·23번(`dht11` 응답) 가지는 14주차 입력 이력 기능이라 그대로 둔다.

실행하고 제어 화면에서 확인한다.

| 조작 | 보여야 할 것 |
|---|---|
| `3` → Switch 켜기 | `on 3` → 약 0.3초 뒤 `응답: {"result":"ok","ms":"led(s) on"}`. 로그 글자가 초록 |
| Switch 끄기 | `off 3` → `응답: {"result":"ok","ms":"led(s) off"}` |
| [전체 끄기] | `off -1` → `응답: {"result":"ok","ms":"led(s) off"}` |
| [온습도 받기 시작] | 명령 로그에는 새 줄이 없고, 입력 이력에 `시:분:초 [24.5,40.0]`이 3초마다 |

오류 응답을 보고 싶으면 9단계의 `Bleuno.client?.send("on $index")`를 잠시 `"on$index"`로 바꿔 실행한다. `3` → Switch 켜기에 빨간 `응답: {"result":"fail","ms":"unknown command"}`과 `보드가 오류를 알렸습니다` / `응답: fail · unknown command` 창이 뜰 것이다(예상). 확인한 뒤 **띄어쓰기를 되돌린다.**

### 11. TODO(3) ① startConnectTimeout() — 시간 제한 걸기

`MainActivity.kt`의 50번 `private fun startConnectTimeout() {` 아래의 `// TODO(3)` **주석 세 줄**을 지우고 그 자리에 넣는다. 위 주석부터 함수 끝까지는 아래와 같다.

```kotlin
    // 50. 연결 시간 제한을 건다. 앞에서 건 제한이 남아 있으면 먼저 취소한다(14주차 1일차).
    //     취소하지 않으면 앞 연결의 10초 예약이 새 연결을 끊을 수 있다. 6주차 [중지]의 scanJob?.cancel()과 같은 방법이다.
    private fun startConnectTimeout() {
        connectTimeoutJob?.cancel()
        connectTimeoutJob = lifecycleScope.launch {
            waitConnectTimeout()
        }
    }
```

- `connectTimeoutJob?.cancel()`: 앞 연결에서 건 10초 예약이 남아 있으면 먼저 멈춘다. 아직 없으면(`null`) `?.`에서 멈춘다(6주차 `scanJob?.cancel()`과 같다).
- `connectTimeoutJob = lifecycleScope.launch { … }`: 새 코루틴을 시작하고 그 `Job`을 보관한다. `connectTimeoutJob` 변수는 클래스 안 108행에 이미 있다.
- 51번 `waitConnectTimeout()`은 `suspend fun`이라 `launch { }` 안에서 부른다. 밖에서 바로 부르면 `Suspend function 'suspend fun waitConnectTimeout(): Unit' should be called only from a coroutine or another suspend function.`

**Build › Make Project**로 빌드만 확인한다. 이 함수는 목록 줄 탭(49번)·[재연결] 버튼(49번)·회전(52번)에서 이미 불리고 있었지만, 51번이 비어 있어 아직 아무 일도 하지 않는다.

### 12. TODO(3) ② waitConnectTimeout() — 10초 기다린 뒤 안내하기

51번 `private suspend fun waitConnectTimeout() {` 아래의 `// TODO(3)` **주석 다섯 줄**을 지우고 그 자리에 넣는다. 위 주석부터 함수 끝까지는 아래와 같다.

```kotlin
    // 51. 10초를 기다린 뒤에도 아직 연결 중·서비스 확인 중이면 "연결 시간이 초과되었습니다"를 알리고 연결을 끊는다(14주차 1일차).
    //     그사이 준비됨·끊김·연결 안 됨이 되었으면 아무것도 하지 않는다. listOf(…).contains(…)는 13주차 오늘 문법이다.
    //     delay를 쓰므로 suspend가 붙는다(6주차 countDown과 같다). 이 함수 안의 this는 Activity라서 Toast에 그대로 쓴다.
    private suspend fun waitConnectTimeout() {
        delay(10000)
        val state = client.connectionState.value
        if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
            Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
            client.disconnect()
            // 실제 보드는 아직 맺어지지 않은 연결을 끊으면 "끊겼다"는 알림이 오지 않는 기기가 있다. 그러면 상태가 "연결 중"에 머물러
            // 7번이 화면을 고치지 않으므로, 여기서 직접 [검색]·[다시 시도]를 쓸 수 있는 모양으로 되돌린다(12주차 34번과 같은 모양).
            // 나중에 알림이 오면 7번이 "연결 안 됨" 모양으로 다시 고친다.
            binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
            binding.scanProgress.visibility = View.GONE
            binding.scanButton.isEnabled = true
            binding.retryButton.visibility = View.VISIBLE
        }
    }
```

- `delay(10000)`: 10초(10000ms)를 기다린다. 기다리는 동안 화면은 멈추지 않는다(6주차).
- `client.connectionState.value`로 지금 상태를 읽어 `연결 중`·`서비스 확인 중`일 때만 안내하고 끊는다. 그사이 `준비됨`이나 `끊김`이 되었으면 아무것도 하지 않는다. 52번과 같은 `listOf(…).contains(…)` 검사다.
- 이 함수 안의 `this`는 Activity라서 Toast에 그대로 쓴다. 50번의 `launch { }` 안에 Toast를 바로 쓰면 그 `this`는 코루틴이라 `None of the following candidates is applicable:`와 `Unresolved reference 'show'.`가 난다.
- 아래 네 줄(`stateText`·`scanProgress`·`scanButton`·`retryButton`)은 끊겼다는 알림이 늦게 오는 실보드에서 [검색]·[다시 시도]를 곧바로 쓸 수 있게 화면을 되돌리는 줄이다(14주차).
- 회색이던 `import kotlinx.coroutines.delay`가 보통 색이 된다. `delay`가 빨간색이면 **Alt+Enter**(맥 ⌥+Enter) → **Import** → `kotlinx.coroutines.delay`를 고른다. 이 import가 지워져 있었다면 Build 창에 `Unresolved reference 'delay'.`가 난다.

실행하고 [검색] → `ESP32_BLE_FAKE1` 줄을 누른 뒤 10초를 기다린다. 약 2초 만에 `준비됨`이 되고 10초가 지나도 **안내가 뜨지 않는다.** 가짜 보드는 빨리 연결되기 때문이며 정상이다.

### 13. 시간 초과를 짧게 만들어 확인하기

1. 12단계 함수의 `delay(10000)`을 잠시 `delay(1000)`으로 바꾼다.
2. `Run ▶` → [검색] → `ESP32_BLE_FAKE1` 줄을 누른다.

| 조작 | 보여야 할 것(예상) |
|---|---|
| 줄 탭 | 약 1초 뒤 Toast `연결 시간이 초과되었습니다`. 상태 글자 `연결 시간 초과 — [다시 시도]를 누르세요`, [검색] 켜짐, [다시 시도] 보임, 원형 진행 표시 없음 |
| [검색] → 줄 탭 직후 곧바로 회전 | 약 1초 뒤 같은 안내. 회전으로 앞 화면의 예약은 사라지지만 onCreate 52번이 시간 제한을 다시 건다 |
| Logcat `tag:BLE` | `connectGatt(가짜): 00:11:22:33:44:01` → `disconnect(가짜) → 연결 안 됨` |

3. 확인이 끝나면 **`delay(10000)`으로 되돌린다.** 되돌리지 않으면 Fake에서 늘 1초 만에 끊겨 `준비됨`까지 가지 못한다.

### 14. 완성 파일 전체와 비교하기

TODO를 모두 채운 전체 파일은 [examples/rehearsal_solution/MainActivity.kt](examples/rehearsal_solution/MainActivity.kt)(493행)와 [examples/rehearsal_solution/ControlActivity.kt](examples/rehearsal_solution/ControlActivity.kt)(277행)다. 두 파일은 14주차 [examples/day1/MainActivity.kt](../week14_ble_input_project/examples/day1/MainActivity.kt)·[examples/day1/ControlActivity.kt](../week14_ble_input_project/examples/day1/ControlActivity.kt)와 글자 단위로 같아서 여기에는 다시 싣지 않는다. 4~12단계에서 채운 아홉 덩어리 말고는 starter와 한 글자도 다르지 않다.

| 채운 곳 | 완성본 줄 | 단계 |
|---|---|---|
| `MainActivity.kt` `permissionLauncher` | 64~70행 | 6 |
| `MainActivity.kt` 12번 [권한 확인] | 284~290행 | 7 |
| `MainActivity.kt` 13번 `hasBlePermissions()` | 392~399행 | 4 |
| `MainActivity.kt` 14번 `showPermissionDialog()` | 402~413행 | 5 |
| `MainActivity.kt` 50번 `startConnectTimeout()` | 468~473행 | 11 |
| `MainActivity.kt` 51번 `waitConnectTimeout()` | 478~492행 | 12 |
| `ControlActivity.kt` 2번 LED Switch | 58~81행 | 9 |
| `ControlActivity.kt` 8번 응답 가지 | 195~210행 | 10 |
| `ControlActivity.kt` 12번 `isAllowedIndex()` | 226~234행 | 8 |

내 파일과 한 줄씩 비교하려면 Android Studio에서 두 파일을 골라 오른쪽 클릭 › **Compare Files**를 쓴다. 주석이 없거나 달라도 동작은 같다.

### 15. 점검표로 확인하기

저장(Ctrl+S, 맥 ⌘+S)하고 `Run ▶`으로 다시 실행한다. 위에서부터 차례로 해 본다. 회전은 에뮬레이터 창 옆 도구 막대의 회전 버튼으로 한다.

| 조작 | 화면 | Logcat `tag:BLE` |
|---|---|---|
| 권한을 허용한 채 [권한 확인] | 요청 창 없이 `권한 OK` | 없음 |
| 권한을 끈 채 [권한 확인] → 거절 → [설정으로] | `권한이 필요합니다` 창 → 앱 정보 화면 | 없음 |
| (권한 허용 뒤) [검색] → `ESP32_BLE_FAKE1` 줄 탭 | `연결 중` → `서비스 확인 중` → `준비됨`, 10초 뒤에도 안내 없음 | `connectGatt(가짜): 00:11:22:33:44:01` … `onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨` |
| `준비됨`에서 회전 | 그대로 `준비됨`, [해제]·[제어 화면] 켜짐 | 새 줄 없음 |
| [제어 화면] → 빈 칸 Switch | Toast `LED 번호를 입력하세요` | 새 줄 없음 |
| `9` → Switch | Toast `허용되지 않는 번호` | 새 줄 없음 |
| `3` → Switch 켜기 | `on 3` → `응답: {"result":"ok","ms":"led(s) on"}` 초록, 0.3초 회색 | `writeCharacteristic(가짜): "on 3"` → `onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) on"}` |
| [뒤로] → [끊김 시험] → [재연결] | `끊김`과 Toast `연결이 끊겼습니다. [재연결]을 누르세요` → `준비됨` | `simulateLost(가짜) → 끊김` → `connectGatt(가짜): …` |
| 장치 이름이 있는 채로 [연결] → [뒤로] → 앱을 완전히 닫고 다시 실행 | `마지막 장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)` | 없음 |

51번이 `delay(10000)`으로 되돌려져 있는지도 본다.

### 16. 자기 채점하기

[채점표](rubric.md)의 구현 15점(U1~M3)으로 매긴다. 시연 5점은 2일차에 본다. 점수를 잃은 기준이 있으면 14단계의 완성 코드와 한 줄씩 비교한다. 리허설은 제출하지 않는다.

## 2일차

### 17. 실기기와 내 보드 점검

2일차 설명 시간(15–22분)에 모두 함께 한다. 목적은 **시연에 쓸 앱을 실기기에 설치해 두고, 내 보드와 연결되는지 시험 전에 확인**하는 것이다.

1. 강의자에게 보드(필요하면 대여 기기)를 받는다. 보드에 붙은 이름 `ESP32_BLE…`를 적어 둔다. 보드를 USB 전원에 꽂으면 빨강 → 파랑 깜빡임이 된다.
2. Android 실기기를 USB로 연결한다. 개발자 옵션·USB 디버깅은 11주차에 켰다. Android Studio 위쪽 기기 목록에 기기 이름이 보이면 된다. 기기의 블루투스를 켠다(Android 11 이하 기기는 위치도 켠다).
3. 1일차 리허설의 점검표(15단계)에서 TODO(1)이나 TODO(2)의 줄에 X가 남았다면, 먼저 `MainActivity.kt`·`ControlActivity.kt` 전체를 [rehearsal_solution/MainActivity.kt](examples/rehearsal_solution/MainActivity.kt)·[rehearsal_solution/ControlActivity.kt](examples/rehearsal_solution/ControlActivity.kt)로 바꾼다(2단계와 같은 방법). 완성본은 허용 자료다.
   - 시연 출력 제어의 응답 줄(O2)은 TODO(2)의 응답 가지가 있어야 생긴다. `LED 0 밝기` 막대로 LED만 켜서는 응답 줄이 붙지 않는다.
   - TODO(1)이 빈 starter는 권한을 늘 허용으로 본다. 권한이 없는 실기기에서 블루투스를 끈 채 [검색]을 누르면 앱이 멈출 수 있다(예상).
4. `MainActivity.kt`에서 아래 줄을 찾아 `true`를 `false`로 바꾼다. 완성본에서는 88행이다(내가 채운 파일은 줄 번호가 조금 다를 수 있다).

```kotlin
    // 12주차 1일차: true면 보드 없이 연습하는 가짜 클라이언트, false면 실제 보드에 연결하는 클라이언트를 만든다.
    // 실기기와 보드가 있으면 이 한 줄만 false로 바꾼다. 나머지 코드는 그대로 둔다.
    private val useFake = true
```

5. 기기 목록에서 실기기를 고르고 `Run ▶`을 누른다. 앱이 기기에 설치되어 열린다. [권한 확인] → `근처 기기` 허용 → `권한 OK`.
6. [검색]을 누른다. 목록에 옆자리 보드도 함께 보이므로 **내 보드 이름** 줄을 누른다. `연결 중` → `서비스 확인 중` → `준비됨`이 되고 보드의 파랑 깜빡임이 멈춘다.
7. [제어 화면] → `0` → LED Switch 켜기 → 보드의 0번 LED가 켜진다. 로그에 `응답: {"result":"ok","ms":"led(s) on"}`. Switch를 끄면 꺼진다. Switch에 반응이 없거나 `응답:` 줄이 없으면 3번으로 돌아가 두 파일을 완성본으로 바꾼다.
8. [온습도 받기 시작] → 입력 이력에 `시:분:초 [온도,습도]` 줄이 3줄 쌓이면 [중지].
9. 앱은 기기에 **그대로 둔다**(시연 때 이 앱을 쓴다). Android Studio에서는 `useFake = true`로 되돌리고 기기 목록을 에뮬레이터로 바꾼다.

| 확인 | 됨 |
|---|---|
| 실기기가 Android Studio 기기 목록에 보인다 | ☐ |
| 실기기 앱에서 `권한 OK` | ☐ |
| 내 보드 이름으로 `준비됨` | ☐ |
| LED 0이 켜지고 꺼지며, 명령 로그에 `응답:` 줄이 붙는다 | ☐ |
| 입력 이력 3줄 | ☐ |

하나라도 안 되면 바로 손을 든다. 시험 시작 전에 보드·케이블·기기를 바꾸는 것이 가장 빠르다. 보드 문제인지 앱 문제인지 모르겠으면 에뮬레이터에서 `useFake = true`로 같은 조작을 해 본다.
22분까지 다섯 칸을 끝내지 못하면 조교가 본시험 0–5분에 이어서 확인하고, 내 시연 차례는 순서표 맨 뒤로 미뤄진다.

### 18. 본시험 starter 열기

시험 시작 뒤 0–5분에 한다.

1. 강의자가 배포한 starter 폴더를 받는다. 압축 파일이면 먼저 푼다.
2. **File › Open**을 누르고, 안에 `settings.gradle.kts`가 들어 있는 폴더를 고른다. 프로젝트를 믿겠느냐고 물으면 **Trust Project**를 누른다.
3. Gradle Sync가 끝나면 기기 목록이 **에뮬레이터**인지 보고 `Run ▶`을 누른다. 첫 화면이 뜨지 않으면 코드를 고치기 전에 손을 든다.
4. **View › Tool Windows › TODO**로 TODO 목록을 열고 문항지와 함께 읽는다. 리허설과 다른 문구·숫자에 밑줄을 긋는다.
5. 회색 import와 `return` 줄은 리허설과 같이 지우지 않는다.

### 19. 시연 차례에 할 일

평가자가 자리에 오면 **Ctrl+S**(맥 ⌘+S)로 저장하고 편집을 멈춘다. 시연은 한 사람 3분이다.

1. (약 30초) 실기기에서 17단계에 설치해 둔 `SmartIO`를 연다 → [검색] → 내 보드 이름 줄 → `준비됨` → [제어 화면].
2. (약 1분) **출력 제어**: LED 번호를 넣고 Switch를 켜 LED가 켜지는 것을 보인다 → Switch를 끄거나 [전체 끄기]로 끈다 → 명령 로그에서 보낸 명령과 `응답:` 줄을 손가락으로 가리킨다.
3. (약 1분) **입력 수신**: [온습도 받기 시작] → 입력 이력 3줄 → [중지] → 새 줄이 더 안 쌓이는 것을 평가자와 함께 본다.
4. (약 30초) **구술**: 평가자가 에뮬레이터 쪽 본시험 코드에서 콜백 하나를 가리키고 "이 콜백은 언제 불리나"를 묻는다. "사용자가 ○○을 누를 때마다", "보드가 JSON 한 줄을 보낼 때마다"처럼 **때와 조건**을 한 문장으로 답한다.

끝나면 곧바로 본시험으로 돌아간다. 시연은 본시험 5–55분에 하고, 3분은 모두 똑같이 한 번 쓰므로 제출 마감은 모두 60분이다. 장비 장애나 평가자 사정으로 3분을 넘긴 몫만 장애 기록지에 적고, 60분 뒤 같은 자리에서 그만큼 이어서 한다.

### 20. 저장·다시 실행·제출

45–60분에 한다. 마지막으로 코드를 고친 뒤에도 한 번 더 한다.

1. 시간 제한 숫자를 줄여 확인했다면 **문항지의 숫자로 되돌린다.**
2. **Ctrl+S**(맥 ⌘+S)로 저장하고 `Run ▶`을 누른다. 앱이 처음 화면부터 다시 뜨는지 본다.
3. 15단계와 같은 모양의 점검표를 문항지 문구로 한 바퀴 돈다.
4. Project 창에서 `MainActivity.kt`를 우클릭 › **Open In › Explorer**(맥 **Finder**)를 누른다. `app/src/main/java/com/example/smartio/` 폴더에 `MainActivity.kt`와 `ControlActivity.kt`가 보인다.
5. 두 파일을 시험 공지의 LMS 제출 칸에 올린다. 파일 이름은 바꾸지 않는다. 캡처는 문항지가 지정할 때만 낸다.

### 21. 제출 전 마지막 확인

- [ ] 마지막으로 고친 뒤 저장하고 다시 실행했다.
- [ ] 빨간 줄이 남은 파일이 없다(끝내지 못한 줄은 앞에 `//`를 붙였다).
- [ ] 시간 제한 숫자가 문항지와 같다. `useFake = true`다.
- [ ] 올린 파일이 본시험 프로젝트의 `MainActivity.kt`와 `ControlActivity.kt`다. 1일차 리허설 프로젝트의 같은 이름 파일이 아니다.

## 오류가 나면

먼저 **빨간 오류**의 첫 줄을 읽는다. 노란 경고와 회색 import는 실행을 막지 않는다.
자주 나오는 오류와 확인할 곳은 [실습지의 막혔을 때](lab.md#막혔을-때)에 있다.
앱이 실행 중에 멈췄다면 Logcat 필터를 `package:mine`으로 바꾸고 `FATAL EXCEPTION` 줄 아래의 예외 이름과 메시지를 읽는다.
명령이 안 먹으면 Logcat `tag:BLE`에서 `writeCharacteristic` 줄(보낸 글자)과 `onCharacteristicChanged` 줄(받은 대답)을 차례로 본다.

## 부록 A — 바꾸지 않는 파일 전체

아래 파일은 14주차 `examples/day1`과 글자 단위로 같고, 리허설 starter와 완성본에서도 같다. 같은 코드가 [examples/rehearsal_starter](examples/rehearsal_starter)와 [examples/rehearsal_solution](examples/rehearsal_solution)에 있다.

`AndroidManifest.xml` — [examples/rehearsal_starter/AndroidManifest.xml](examples/rehearsal_starter/AndroidManifest.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- 10주차 2일차: BLE를 쓰는 앱이라고 알린다. -->
    <uses-feature
        android:name="android.hardware.bluetooth_le"
        android:required="true" />

    <!-- 10주차 2일차: Android 12(API 31) 이상에서 쓰는 BLE 권한. 실행 중에도 허락받아야 한다. -->
    <uses-permission
        android:name="android.permission.BLUETOOTH_SCAN"
        android:usesPermissionFlags="neverForLocation"
        tools:targetApi="s" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

    <!-- 10주차 2일차: Android 11(API 30) 이하에서 쓰는 권한. ACCESS_FINE_LOCATION은 실행 중에도 허락받아야 한다. -->
    <uses-permission
        android:name="android.permission.BLUETOOTH"
        android:maxSdkVersion="30" />
    <uses-permission
        android:name="android.permission.BLUETOOTH_ADMIN"
        android:maxSdkVersion="30" />
    <uses-permission
        android:name="android.permission.ACCESS_FINE_LOCATION"
        android:maxSdkVersion="30" />

    <!-- 11주차 2일차: 연락처 앱의 데이터(ContentProvider)를 읽는 권한. 실행 중에도 허락받아야 한다. -->
    <uses-permission android:name="android.permission.READ_CONTACTS" />

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

`ContactsReader.kt` — [examples/rehearsal_starter/ContactsReader.kt](examples/rehearsal_starter/ContactsReader.kt)

```kotlin
package com.example.smartio

import android.content.ContentResolver
import android.provider.ContactsContract

// 1. 연락처 앱이 ContentProvider로 내주는 연락처 이름을 읽어 목록으로 돌려준다(11주차 2일차, 제공 코드).
//    다른 앱의 데이터는 직접 열 수 없고, ContentResolver에 content URI(창구 주소)를 주고 query로 요청한다.
//    READ_CONTACTS 권한이 허용된 뒤에만 부른다. 연락처가 없으면 빈 목록(0건)을 돌려준다. 0건은 실패가 아니다.
object ContactsReader {
    fun names(resolver: ContentResolver): List<String> {
        val names = mutableListOf<String>()

        // 2. query(주소, 가져올 칸, 조건, 조건 값, 정렬): 연락처 목록에서 "표시 이름" 칸만 이름순으로 달라고 요청한다.
        val cursor = resolver.query(
            ContactsContract.Contacts.CONTENT_URI,
            arrayOf(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY),
            null,
            null,
            ContactsContract.Contacts.DISPLAY_NAME_PRIMARY + " ASC"
        )
        // 결과를 못 받으면(null) 빈 목록을 그대로 돌려준다.
        if (cursor == null) {
            return names
        }

        // 3. cursor는 결과 표를 한 줄씩 가리키는 손가락이다. moveToNext()가 다음 줄로 옮기고, 더 없으면 false가 되어 반복이 끝난다.
        val nameColumn = cursor.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY)
        while (cursor.moveToNext()) {
            val name: String? = cursor.getString(nameColumn)
            if (name != null) {
                names.add(name)
            }
        }

        // 4. 다 읽었으면 반드시 닫는다. 닫지 않으면 결과 표가 메모리에 계속 남는다.
        cursor.close()
        return names
    }
}
```

`activity_main.xml` — [examples/rehearsal_starter/activity_main.xml](examples/rehearsal_starter/activity_main.xml)

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
        android:id="@+id/lastDeviceText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/last_device_none"
        android:textSize="16sp" />

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

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/device_list_title"
        android:textSize="16sp" />

    <ListView
        android:id="@+id/deviceList"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="8dp" />

    <Button
        android:id="@+id/connectButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/connect" />

    <Button
        android:id="@+id/controlButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:enabled="false"
        android:text="@string/control_screen" />

    <Button
        android:id="@+id/retryButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/retry"
        android:visibility="gone" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/reconnectButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/reconnect"
            android:visibility="gone" />

        <Button
            android:id="@+id/lostTestButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/lost_test"
            android:visibility="gone" />

    </LinearLayout>

    <Button
        android:id="@+id/permissionButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/check_permission" />

    <Button
        android:id="@+id/contactsButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/show_contacts" />

    <TextView
        android:id="@+id/batteryText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/battery_unknown"
        android:textSize="16sp" />

</LinearLayout>
```

`activity_control.xml` — [examples/rehearsal_starter/activity_control.xml](examples/rehearsal_starter/activity_control.xml)

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

    <TextView
        android:id="@+id/stateText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/state_unknown"
        android:textSize="18sp" />

    <EditText
        android:id="@+id/pinEdit"
        android:layout_width="160dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:hint="@string/pin_hint"
        android:inputType="number"
        android:maxLength="2" />

    <Switch
        android:id="@+id/ledSwitch"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/led" />

    <Button
        android:id="@+id/allOffButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:enabled="false"
        android:text="@string/all_off" />

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:gravity="center_vertical"
        android:orientation="horizontal">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@string/pwm_title"
            android:textSize="16sp" />

        <SeekBar
            android:id="@+id/pwmSeekBar"
            android:layout_width="160dp"
            android:layout_height="wrap_content"
            android:enabled="false"
            android:max="255" />

    </LinearLayout>

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

    <LinearLayout
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/inputStartButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:enabled="false"
            android:text="@string/input_start" />

        <Button
            android:id="@+id/inputStopButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            android:enabled="false"
            android:text="@string/stop" />

    </LinearLayout>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/input_history_title"
        android:textSize="16sp" />

    <ListView
        android:id="@+id/inputList"
        android:layout_width="240dp"
        android:layout_height="0dp"
        android:layout_weight="2"
        android:layout_marginTop="8dp"
        android:transcriptMode="alwaysScroll" />

    <Button
        android:id="@+id/backButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginBottom="24dp"
        android:text="@string/back" />

</LinearLayout>
```

`strings.xml` — [examples/rehearsal_starter/strings.xml](examples/rehearsal_starter/strings.xml)

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_name_hint">장치 이름</string>
    <string name="auto_connect">자동 연결</string>
    <string name="connect">연결</string>
    <string name="device_unknown">장치: ?</string>
    <string name="pin_hint">LED 번호 (0~3)</string>
    <string name="led">LED</string>
    <string name="log_title">명령 로그</string>
    <string name="back">뒤로</string>
    <string name="scan">검색</string>
    <string name="stop">중지</string>
    <string name="state_idle">대기 중</string>
    <string name="retry">다시 시도</string>
    <string name="disconnect">해제</string>
    <string name="battery_unknown">배터리 ?</string>
    <string name="check_permission">권한 확인</string>
    <string name="device_list_title">검색된 장치</string>
    <string name="last_device_none">마지막 장치: 없음</string>
    <string name="show_contacts">연락처 보기</string>
    <string name="control_screen">제어 화면</string>
    <string name="state_unknown">상태: ?</string>
    <string name="all_off">전체 끄기</string>
    <string name="pwm_title">LED 0 밝기</string>
    <string name="input_start">온습도 받기 시작</string>
    <string name="input_history_title">입력 이력</string>
    <string name="reconnect">재연결</string>
    <string name="lost_test">끊김 시험</string>
</resources>
```

`colors.xml` — [examples/rehearsal_starter/colors.xml](examples/rehearsal_starter/colors.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

`res/values/themes.xml` — [examples/rehearsal_starter/res/values/themes.xml](examples/rehearsal_starter/res/values/themes.xml)

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

## 부록 B — 제공 bleuno 파일 전체

`app › kotlin+java › com.example.smartio › bleuno` 패키지의 8개 파일이다. 12주차에 넣은 그대로이며 제공 [bleuno/src](../../bleuno/src)와 글자 단위로 같다. 사용법은 [bleuno README](../../bleuno/README.md)에 있다. 고치지 않는다.

### ConnState.kt

```kotlin
package com.example.smartio.bleuno

// 연결 상태를 나타내는 한글 문자열 모음.
// 화면의 TextView에 그대로 넣어 보여 준다. 7주차 ConnViewModel의 ConnState와 같은 다섯 가지다.
object ConnState {
    const val DISCONNECTED = "연결 안 됨"   // 처음 상태, 또는 사용자가 해제한 뒤
    const val CONNECTING = "연결 중"        // connect()를 부른 뒤 보드와 연결되기 전
    const val DISCOVERING = "서비스 확인 중" // 연결은 되었고 서비스·특성을 찾는 중
    const val READY = "준비됨"              // 명령을 보낼 수 있는 상태
    const val LOST = "끊김"                 // 사용자가 해제하지 않았는데 연결이 끊어짐
}
```

### BleunoDevice.kt

```kotlin
package com.example.smartio.bleuno

// 검색으로 찾은 보드 하나의 정보.
// name: 기기 이름(ESP32_BLE로 시작), address: 연결할 때 쓰는 주소, rssi: 신호 세기(클수록 가까움, 보통 음수)
data class BleunoDevice(val name: String, val address: String, val rssi: Int)
```

### BleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import kotlinx.coroutines.flow.StateFlow

// bleuno 보드와 이야기하는 방법을 정한 인터페이스.
// 실제 보드용 RealBleunoClient와 보드 없이 연습하는 FakeBleunoClient가 이 인터페이스를 똑같이 구현한다.
// 앱 코드는 이 인터페이스만 보고 쓰므로 fake ↔ real을 바꿔도 앱 코드는 그대로다.
interface BleunoClient {

    // 현재 연결 상태. 값은 ConnState의 다섯 문자열 중 하나다. collect { }로 화면에 반영한다.
    val connectionState: StateFlow<String>

    // 지금 명령을 보낼 수 있으면 true (connectionState.value == ConnState.READY)
    val isReady: Boolean

    // 보드를 검색한다. 찾을 때마다 onFound가, timeoutMs가 지나면 onFinished가 메인 스레드에서 불린다.
    fun startScan(timeoutMs: Long = 5000, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit = {})

    // 검색을 바로 멈춘다. 이때도 onFinished가 한 번 불린다.
    fun stopScan()

    // 주소로 연결을 시작한다. 상태가 연결 중 → 서비스 확인 중 → 준비됨 순서로 바뀐다.
    fun connect(address: String)

    // 연결을 끊는다. 끝나면 상태가 "연결 안 됨"이 된다.
    fun disconnect()

    // 명령 한 줄을 보낸다. 끝의 "\n"은 자동으로 붙인다. 큐에 넣고 순서대로 하나씩 보낸다.
    fun send(command: String)

    // 보드가 보낸 응답·이벤트(JSON 한 줄)를 받을 리스너. 메인 스레드에서 불린다. null이면 해제한다.
    fun onMessage(listener: ((String) -> Unit)?)
}
```

### Bleuno.kt

```kotlin
package com.example.smartio.bleuno

import android.content.Context

// 앱 전체가 공유하는 BleunoClient 보관소.
// MainActivity에서 create()로 만들고, ControlActivity에서는 Bleuno.client로 같은 연결을 이어 쓴다.
object Bleuno {

    // 앱 어디서나 같은 객체를 쓴다. create()를 부르기 전에는 null이다.
    var client: BleunoClient? = null

    // fake = true 면 보드 없이 동작하는 FakeBleunoClient, false 면 실제 보드용 RealBleunoClient를 만든다.
    // 만든 객체는 client에 보관한 뒤 그대로 돌려준다.
    fun create(context: Context, fake: Boolean): BleunoClient {
        val created: BleunoClient = if (fake) {
            FakeBleunoClient()
        } else {
            RealBleunoClient(context.applicationContext)
        }
        client = created
        return created
    }
}
```

### PermissionHelper.kt

```kotlin
package com.example.smartio.bleuno

import android.Manifest
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.pm.PackageManager
import android.location.LocationManager
import android.os.Build
import androidx.core.content.ContextCompat

// BLE에 필요한 런타임 권한과 기기 설정을 확인하는 도우미.
// Android 12(API 31)부터는 BLUETOOTH_SCAN·BLUETOOTH_CONNECT, 그 이하는 ACCESS_FINE_LOCATION이 필요하다.
object PermissionHelper {

    // 이 기기의 Android 버전에서 사용자에게 요청해야 하는 권한 목록
    fun required(): Array<String> {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
        } else {
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
        }
    }

    // required() 중 아직 허용되지 않은 권한만 골라 준다. 비어 있으면 모두 허용된 것이다.
    fun missing(context: Context): Array<String> {
        return required().filter { permission ->
            ContextCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()
    }

    // 필요한 권한이 모두 허용되어 있으면 true
    fun hasAll(context: Context): Boolean = missing(context).isEmpty()

    // 블루투스가 켜져 있으면 true. 블루투스가 없는 기기(일부 에뮬레이터)에서는 false.
    fun isBluetoothEnabled(context: Context): Boolean {
        val manager = context.getSystemService(Context.BLUETOOTH_SERVICE) as? BluetoothManager
        val adapter = manager?.adapter ?: return false
        return adapter.isEnabled
    }

    // 위치 서비스가 켜져 있으면 true. Android 11 이하에서 검색 결과가 0개일 때 원인을 찾는 용도다.
    // API 28 미만에는 확인 API가 없으므로 true로 본다.
    fun isLocationEnabled(context: Context): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.P) return true
        val manager = context.getSystemService(Context.LOCATION_SERVICE) as? LocationManager
        return manager?.isLocationEnabled ?: true
    }
}
```

### BleunoMessage.kt

```kotlin
package com.example.smartio.bleuno

import org.json.JSONException
import org.json.JSONObject

// 보드가 보낸 JSON 한 줄에서 값을 꺼내는 도우미.
// 예: {"result":"ok","ms":"led(s) on"} → result(json) == "ok", message(json) == "led(s) on"
// 잘못된 JSON이면 예외를 던지지 않고 null을 돌려준다.
object BleunoMessage {

    // "result" 값: "ok" | "err" | "fail" | null(없거나 JSON이 아님)
    fun result(json: String): String? = field(json, "result")

    // "ms" 값: 사람이 읽는 메시지 (예: "led(s) on", "unknown command")
    fun message(json: String): String? = field(json, "ms")

    // "value" 값: dht11 응답의 "[24.5,40.0]" 처럼 값이 들어 있는 문자열
    fun value(json: String): String? = field(json, "value")

    // "event" 값: 보드가 먼저 보내는 이벤트 종류 (입력 이벤트 가안: "input")
    fun event(json: String): String? = field(json, "event")

    // result가 "ok"이면 true
    fun isOk(json: String): Boolean = result(json) == "ok"

    // 키 하나를 문자열로 꺼낸다. 키가 없거나 JSON이 아니면 null.
    private fun field(json: String, key: String): String? {
        return try {
            val obj = JSONObject(json)
            if (obj.has(key)) obj.getString(key) else null
        } catch (e: JSONException) {
            null
        }
    }
}
```

### FakeBleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.json.JSONObject

// 보드 없이 앱을 만들고 시험할 때 쓰는 가짜 클라이언트.
// RealBleunoClient와 같은 순서·같은 JSON으로 답하되, 시간은 모두 메인 스레드 Handler.postDelayed로 흉내 낸다.
//   검색: 1초 뒤 ESP32_BLE_FAKE1, 2초 뒤 ESP32_BLE_FAKE2 발견, timeoutMs 뒤 onFinished
//   연결: connect → 연결 중(1초) → 서비스 확인 중(1초) → 준비됨
//   전송: send → 300ms 뒤 펌웨어와 같은 JSON 응답
//   이벤트: 준비됨 상태에서 10초마다 {"event":"input","index":0,"value":0|1}
//   simulateLost(): 보드 전원이 꺼진 것처럼 "끊김"으로 만든다
class FakeBleunoClient : BleunoClient {

    companion object {
        const val TAG = "BLE"
        const val FOUND_DELAY_1 = 1000L
        const val FOUND_DELAY_2 = 2000L
        const val CONNECT_DELAY = 1000L
        const val DISCOVER_DELAY = 1000L
        const val RESPONSE_DELAY = 300L
        const val INPUT_EVENT_INTERVAL = 10000L
        const val LED_COUNT = 4          // 수업 보드의 LED 개수 (인덱스 0~3)
    }

    private val fakeDevices = listOf(
        BleunoDevice("ESP32_BLE_FAKE1", "00:11:22:33:44:01", -50),
        BleunoDevice("ESP32_BLE_FAKE2", "00:11:22:33:44:02", -70),
    )

    // 용도별로 Handler를 나눠서 removeCallbacksAndMessages(null)로 그 용도의 예약만 취소한다
    private val scanHandler = Handler(Looper.getMainLooper())
    private val connectHandler = Handler(Looper.getMainLooper())
    private val sendHandler = Handler(Looper.getMainLooper())
    private val eventHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    private var isScanning = false
    private var onFinishedListener: (() -> Unit)? = null
    private var messageListener: ((String) -> Unit)? = null

    private var inputValue = 0     // 입력 이벤트의 value, 10초마다 0/1 토글
    private var dhtCount = 0       // dht11 응답 값을 조금씩 바꾸기 위한 횟수

    // ---------------------------------------------------------------- 검색

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (isScanning) stopScan()
        isScanning = true
        onFinishedListener = onFinished
        Log.d(TAG, "startScan(가짜): ${timeoutMs}ms 동안 검색")
        scanHandler.postDelayed({
            Log.d(TAG, "onScanResult(가짜): ${fakeDevices[0].name}")
            onFound(fakeDevices[0])
        }, FOUND_DELAY_1)
        scanHandler.postDelayed({
            Log.d(TAG, "onScanResult(가짜): ${fakeDevices[1].name}")
            onFound(fakeDevices[1])
        }, FOUND_DELAY_2)
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout(가짜) (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanHandler.removeCallbacksAndMessages(null)
        Log.d(TAG, "stopScan(가짜)")
        val finished = onFinishedListener
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    override fun connect(address: String) {
        connectHandler.removeCallbacksAndMessages(null)
        eventHandler.removeCallbacksAndMessages(null)
        Log.d(TAG, "connectGatt(가짜): $address")
        _connectionState.value = ConnState.CONNECTING
        connectHandler.postDelayed({
            Log.d(TAG, "onConnectionStateChange(가짜): STATE_CONNECTED → 서비스 확인 중")
            _connectionState.value = ConnState.DISCOVERING
            connectHandler.postDelayed({
                Log.d(TAG, "onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨")
                _connectionState.value = ConnState.READY
                scheduleInputEvent()
            }, DISCOVER_DELAY)
        }, CONNECT_DELAY)
    }

    override fun disconnect() {
        cancelAll()
        Log.d(TAG, "disconnect(가짜) → 연결 안 됨")
        _connectionState.value = ConnState.DISCONNECTED
    }

    // 보드 전원이 꺼진 상황을 흉내 낸다. 상태가 "끊김"이 된다.
    fun simulateLost() {
        cancelAll()
        Log.d(TAG, "simulateLost(가짜) → 끊김")
        _connectionState.value = ConnState.LOST
    }

    private fun cancelAll() {
        connectHandler.removeCallbacksAndMessages(null)
        sendHandler.removeCallbacksAndMessages(null)
        eventHandler.removeCallbacksAndMessages(null)
    }

    // 준비됨 상태인 동안 10초마다 입력 이벤트를 보낸다 (보드 버튼 입력 가안 형식)
    private fun scheduleInputEvent() {
        eventHandler.postDelayed({
            if (!isReady) return@postDelayed
            inputValue = 1 - inputValue
            val json = JSONObject()
            json.put("event", "input")
            json.put("index", 0)
            json.put("value", inputValue)
            deliver(json.toString())
            scheduleInputEvent()
        }, INPUT_EVENT_INTERVAL)
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!isReady) {
            Log.w(TAG, "send(가짜): 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        Log.d(TAG, "writeCharacteristic(가짜): \"$command\"")
        // 펌웨어처럼 "\n"으로 나눈 명령마다 응답 한 줄씩 보낸다
        val lines = command.split("\n").filter { it.isNotBlank() }
        for (line in lines) {
            sendHandler.postDelayed({
                deliver(respond(line.trim()))
            }, RESPONSE_DELAY)
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }

    private fun deliver(json: String) {
        Log.d(TAG, "onCharacteristicChanged(가짜): $json")
        messageListener?.invoke(json)
    }

    // 펌웨어 parseCmd와 같은 규칙으로 응답 JSON을 만든다
    private fun respond(line: String): String {
        val tokens = line.split(Regex("\\s+")).filter { it.isNotEmpty() }
        val res = JSONObject()
        if (tokens.isEmpty()) {
            res.put("result", "fail")
            res.put("ms", "need command")
            return res.toString()
        }
        when (tokens[0]) {
            "on" -> {
                if (tokens.size > 1) {
                    res.put("result", "ok")
                    res.put("ms", "led(s) on")
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index")
                }
            }
            "off" -> {
                if (tokens.size > 1) {
                    res.put("result", "ok")
                    res.put("ms", "led(s) off")
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index")
                }
            }
            "pwm" -> {
                if (tokens.size > 2) {
                    val index = tokens[1].toIntOrNull() ?: 0
                    val value = tokens[2].toIntOrNull() ?: 0
                    if (index < 0) {
                        res.put("result", "ok")
                        res.put("ms", "pwm set")
                    } else if (index >= LED_COUNT) {
                        res.put("result", "err")
                        res.put("ms", "pwm pin index error")
                    } else if (value < 0 || value > 255) {
                        res.put("result", "err")
                        res.put("ms", "pwm value range 0~255")
                    } else {
                        res.put("result", "ok")
                        res.put("ms", "pwm set")
                    }
                } else {
                    res.put("result", "err")
                    res.put("ms", "need pin index and pwm value")
                }
            }
            "dht11" -> {
                // 매번 조금씩 다른 값을 돌려줘서 이력 목록에서 구분되게 한다: 24.5/40.0 → 25.0/41.0 → 25.5/42.0 → 반복
                val step = dhtCount % 3
                dhtCount++
                val temperature = 24.5 + step * 0.5
                val humidity = 40.0 + step * 1.0
                res.put("result", "ok")
                res.put("value", String.format(java.util.Locale.US, "[%.1f,%.1f]", temperature, humidity))
            }
            "about" -> {
                res.put("result", "ok")
                res.put("os", "cronos-v1")
                res.put("app", "BLEuno")
                res.put("version", "1.0.5_dev")
                res.put("author", "gbox3d")
                res.put("chipid", 1234567890L)
            }
            "blink" -> {
                res.put("result", "ok")
                res.put("ms", "led blink")
            }
            "stopblk" -> {
                res.put("result", "ok")
                res.put("ms", "led stop blink")
            }
            else -> {
                res.put("result", "fail")
                res.put("ms", "unknown command")
            }
        }
        return res.toString()
    }
}
```

### RealBleunoClient.kt

```kotlin
package com.example.smartio.bleuno

import android.annotation.SuppressLint
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
import android.bluetooth.BluetoothStatusCodes
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.Context
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID

// 실제 bleuno 보드와 BluetoothGatt로 이야기하는 클라이언트.
// 콜백 사슬: startScan → (timeoutMs 뒤) stopScan → connectGatt → onConnectionStateChange(CONNECTED)
//   → requestMtu(185) → onMtuChanged → discoverServices → onServicesDiscovered
//   → setCharacteristicNotification + CCCD 쓰기 → onDescriptorWrite → 준비됨
//   → writeCharacteristic → onCharacteristicWrite(다음 명령) / onCharacteristicChanged(응답)
// 모든 콜백은 Log.d("BLE", …)로 남기므로 Logcat에서 태그 BLE로 순서를 볼 수 있다.
// 권한 검사는 PermissionHelper.hasAll로 하고, 없으면 로그만 남기고 아무것도 하지 않는다(요청은 앱 책임).
@SuppressLint("MissingPermission")
class RealBleunoClient(
    context: Context,
    private val nameFilter: String = "ESP32_BLE",   // 이 문자열로 시작하는 이름의 기기만 onFound에 알린다
) : BleunoClient {

    companion object {
        const val TAG = "BLE"
        val SERVICE_UUID: UUID = UUID.fromString("c6f8b088-2af8-4388-8364-ca2a907bdeb8")
        val CHARACTERISTIC_UUID: UUID = UUID.fromString("f6aa83ca-de53-46b4-bdea-28a7cb57942e")
        val CCCD_UUID: UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
        const val MTU = 185
    }

    private val appContext: Context = context.applicationContext
    private val bluetoothManager: BluetoothManager? =
        appContext.getSystemService(Context.BLUETOOTH_SERVICE) as? BluetoothManager

    // 콜백은 바인더 스레드에서 오므로, 화면과 리스너에는 항상 이 Handler로 메인 스레드에서 전달한다
    private val mainHandler = Handler(Looper.getMainLooper())
    // 검색 시간 초과 전용 Handler (removeCallbacksAndMessages로 검색 것만 취소하기 위해 분리)
    private val scanHandler = Handler(Looper.getMainLooper())

    private val _connectionState = MutableStateFlow(ConnState.DISCONNECTED)
    override val connectionState: StateFlow<String> = _connectionState
    override val isReady: Boolean
        get() = _connectionState.value == ConnState.READY

    // ---- 검색 ----
    private var isScanning = false
    private var onFoundListener: ((BleunoDevice) -> Unit)? = null
    private var onFinishedListener: (() -> Unit)? = null
    private val foundAddresses = HashSet<String>()   // 같은 기기를 두 번 알리지 않기 위한 주소 집합

    // ---- 연결 ----
    private var gatt: BluetoothGatt? = null
    private var characteristic: BluetoothGattCharacteristic? = null
    private var userDisconnect = false               // disconnect()를 사용자가 불렀는지

    // ---- 전송 큐 ----
    private val queue = ArrayDeque<String>()         // 아직 보내지 않은 명령("\n" 포함)
    private var writing = false                      // onCharacteristicWrite를 기다리는 중이면 true

    private var messageListener: ((String) -> Unit)? = null

    // ---------------------------------------------------------------- 검색

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val device = result.device ?: return
            val name = result.scanRecord?.deviceName ?: device.name ?: return
            if (!name.startsWith(nameFilter)) return
            val found = BleunoDevice(name, device.address, result.rssi)
            mainHandler.post {
                if (!isScanning) return@post
                if (!foundAddresses.add(found.address)) return@post   // 이미 알린 기기
                Log.d(TAG, "onScanResult: ${found.name} ${found.address} rssi=${found.rssi}")
                onFoundListener?.invoke(found)
            }
        }

        override fun onScanFailed(errorCode: Int) {
            Log.w(TAG, "onScanFailed: errorCode=$errorCode")
            mainHandler.post { stopScan() }
        }
    }

    override fun startScan(timeoutMs: Long, onFound: (BleunoDevice) -> Unit, onFinished: () -> Unit) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "startScan: 권한이 없어 무시함 (${PermissionHelper.missing(appContext).joinToString()})")
            return
        }
        val scanner = bluetoothManager?.adapter?.bluetoothLeScanner
        if (scanner == null) {
            Log.w(TAG, "startScan: 블루투스가 꺼져 있거나 없음 → onFinished")
            onFinished()
            return
        }
        if (isScanning) stopScan()
        foundAddresses.clear()
        onFoundListener = onFound
        onFinishedListener = onFinished
        isScanning = true
        val settings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
            .build()
        scanner.startScan(null, settings, scanCallback)
        Log.d(TAG, "startScan: ${timeoutMs}ms 동안 \"$nameFilter\"로 시작하는 기기 검색")
        scanHandler.postDelayed({
            Log.d(TAG, "scan timeout (${timeoutMs}ms)")
            stopScan()
        }, timeoutMs)
    }

    override fun stopScan() {
        if (!isScanning) return
        isScanning = false
        scanHandler.removeCallbacksAndMessages(null)
        bluetoothManager?.adapter?.bluetoothLeScanner?.stopScan(scanCallback)
        Log.d(TAG, "stopScan: 찾은 기기 ${foundAddresses.size}개")
        val finished = onFinishedListener
        onFoundListener = null
        onFinishedListener = null
        finished?.invoke()
    }

    // ---------------------------------------------------------------- 연결

    private val gattCallback = object : BluetoothGattCallback() {

        override fun onConnectionStateChange(g: BluetoothGatt, status: Int, newState: Int) {
            Log.d(TAG, "onConnectionStateChange: status=$status newState=$newState")
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.d(TAG, "STATE_CONNECTED → requestMtu($MTU)")
                mainHandler.post { _connectionState.value = ConnState.DISCOVERING }
                val requested = g.requestMtu(MTU)
                Log.d(TAG, "requestMtu($MTU) 호출 결과=$requested")
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.d(TAG, "STATE_DISCONNECTED → gatt.close()")
                g.close()
                mainHandler.post {
                    gatt = null
                    characteristic = null
                    queue.clear()
                    writing = false
                    _connectionState.value = if (userDisconnect) ConnState.DISCONNECTED else ConnState.LOST
                }
            }
        }

        override fun onMtuChanged(g: BluetoothGatt, mtu: Int, status: Int) {
            Log.d(TAG, "onMtuChanged: mtu=$mtu status=$status → discoverServices()")
            // MTU 변경이 실패해도 기본 MTU로 쓸 수 있으므로 서비스 탐색은 그대로 진행한다
            val started = g.discoverServices()
            Log.d(TAG, "discoverServices() 호출 결과=$started")
        }

        override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
            Log.d(TAG, "onServicesDiscovered: status=$status")
            val service = g.getService(SERVICE_UUID)
            val ch = service?.getCharacteristic(CHARACTERISTIC_UUID)
            if (ch == null) {
                Log.w(TAG, "서비스 또는 특성을 찾지 못함 → disconnect()")
                g.disconnect()
                return
            }
            Log.d(TAG, "characteristic 확보: ${ch.uuid}")
            mainHandler.post { characteristic = ch }
            g.setCharacteristicNotification(ch, true)
            val descriptor = ch.getDescriptor(CCCD_UUID)
            if (descriptor == null) {
                Log.w(TAG, "CCCD descriptor 없음 → disconnect()")
                g.disconnect()
                return
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                g.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE)
            } else {
                @Suppress("DEPRECATION")
                descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                @Suppress("DEPRECATION")
                g.writeDescriptor(descriptor)
            }
            Log.d(TAG, "writeDescriptor(CCCD, ENABLE_NOTIFICATION_VALUE)")
        }

        override fun onDescriptorWrite(g: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int) {
            Log.d(TAG, "onDescriptorWrite: status=$status → 준비됨")
            mainHandler.post { _connectionState.value = ConnState.READY }
        }

        override fun onCharacteristicWrite(g: BluetoothGatt, ch: BluetoothGattCharacteristic, status: Int) {
            Log.d(TAG, "onCharacteristicWrite: status=$status")
            mainHandler.post {
                writing = false
                writeNext()
            }
        }

        // API 33 이상에서 불리는 응답 콜백
        override fun onCharacteristicChanged(g: BluetoothGatt, ch: BluetoothGattCharacteristic, value: ByteArray) {
            deliver(value)
        }

        // API 32 이하에서 불리는 응답 콜백
        @Deprecated("Deprecated in Java")
        override fun onCharacteristicChanged(g: BluetoothGatt, ch: BluetoothGattCharacteristic) {
            @Suppress("DEPRECATION")
            val value = ch.value ?: return
            deliver(value)
        }
    }

    // 받은 바이트를 UTF-8 문자열로 바꿔 메인 스레드에서 리스너에 전달한다
    private fun deliver(bytes: ByteArray) {
        val text = String(bytes, Charsets.UTF_8)
        Log.d(TAG, "onCharacteristicChanged: $text")
        mainHandler.post { messageListener?.invoke(text) }
    }

    override fun connect(address: String) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "connect: 권한이 없어 무시함")
            return
        }
        val adapter = bluetoothManager?.adapter
        if (adapter == null) {
            Log.w(TAG, "connect: 블루투스 어댑터 없음")
            return
        }
        val device = try {
            adapter.getRemoteDevice(address)
        } catch (e: IllegalArgumentException) {
            Log.w(TAG, "connect: 잘못된 주소 $address")
            return
        }
        // 이전 연결이 남아 있으면 정리하고 새로 시작한다
        gatt?.close()
        gatt = null
        characteristic = null
        queue.clear()
        writing = false
        userDisconnect = false

        _connectionState.value = ConnState.CONNECTING
        Log.d(TAG, "connectGatt($address, autoConnect=false)")
        val created = device.connectGatt(appContext, false, gattCallback)
        if (created == null) {
            Log.w(TAG, "connectGatt 실패 (블루투스 꺼짐?)")
            _connectionState.value = ConnState.DISCONNECTED
            return
        }
        gatt = created
    }

    override fun disconnect() {
        userDisconnect = true
        val g = gatt
        if (g == null) {
            Log.d(TAG, "disconnect: 연결 없음 → 연결 안 됨")
            _connectionState.value = ConnState.DISCONNECTED
            return
        }
        Log.d(TAG, "gatt.disconnect()")
        g.disconnect()   // 결과는 onConnectionStateChange(STATE_DISCONNECTED)에서 처리
    }

    // ---------------------------------------------------------------- 전송

    override fun send(command: String) {
        if (!PermissionHelper.hasAll(appContext)) {
            Log.w(TAG, "send: 권한이 없어 무시함")
            return
        }
        if (!isReady) {
            Log.w(TAG, "send: 준비되지 않아 무시함 (\"$command\", 상태=${_connectionState.value})")
            return
        }
        queue.addLast(command + "\n")
        Log.d(TAG, "send: 큐에 추가 \"$command\" (대기 ${queue.size}개)")
        if (!writing) writeNext()
    }

    // 큐의 맨 앞 명령 하나를 보낸다. 다음 것은 onCharacteristicWrite가 온 뒤에 보낸다.
    private fun writeNext() {
        val g = gatt ?: return
        val ch = characteristic ?: return
        val text = queue.removeFirstOrNull() ?: return
        val bytes = text.toByteArray(Charsets.UTF_8)
        writing = true
        val ok = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            val code = g.writeCharacteristic(ch, bytes, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
            code == BluetoothStatusCodes.SUCCESS
        } else {
            @Suppress("DEPRECATION")
            ch.value = bytes
            @Suppress("DEPRECATION")
            g.writeCharacteristic(ch)
        }
        Log.d(TAG, "writeCharacteristic(\"${text.trim()}\") 호출 결과=$ok")
        if (!ok) {
            // 호출 자체가 실패하면 onCharacteristicWrite가 오지 않으므로 바로 다음 것을 시도한다
            writing = false
            writeNext()
        }
    }

    override fun onMessage(listener: ((String) -> Unit)?) {
        messageListener = listener
    }
}
```
