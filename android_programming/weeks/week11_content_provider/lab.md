# 11주차 실습 — 장치 목록과 마지막 장치 저장

이번 주에는 10주차 `SmartIO` 연결 화면에 장치 이름 목록을 붙이고, 2일차에는 마지막으로 연결한 장치를 저장한 뒤 실기기에서 앱을 실행한다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 한 줄씩 바꿔 가며 화면과 Logcat이 어떻게 달라지는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 장치 목록 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 10주차 `SmartIO`를 실행하고 `strings.xml`·`activity_main.xml`에 목록 자리(`deviceList`)를 만든다 |
| 10–20분 | `devices` 목록과 `adapter`를 만들어 ListView에 끼운다 |
| 20–38분 | [검색]에서 1초마다 이름 세 개를 넣고 [중지]로 멈춘다. `notifyDataSetChanged()`를 빼 보고 되돌린다 |
| 38–52분 | 목록의 한 줄을 누르면 장치 이름 칸에 넣고, [연결]로 제어 화면에 이름을 넘긴다 |
| 52–60분 | 캡처 1을 찍고 프로젝트를 저장한다 |

### 1. 목록 자리 만들기

1. `strings.xml`의 `check_permission` 아래에 `device_list_title`(`검색된 장치`)을 넣는다.
2. `activity_main.xml`에서 `stateText` **아래**, `connectButton` **위**에 두 View를 넣는다.
   - 제목 TextView: 글자 `@string/device_list_title`, 크기 `16sp`, 위 간격 `16dp`
   - ListView: id `deviceList`, 폭 `240dp`, 높이 `0dp`와 `android:layout_weight="1"`, 위 간격 `8dp`
3. 실행해 `연결 안 됨` 아래에 `검색된 장치`가 보이면 다음으로 간다.

높이를 `0dp` + `layout_weight`로 두는 방법은 4주차 `activity_control.xml`의 `logText`에 있다. 막히면 [따라하기 2단계](walkthrough.md#2-목록-자리-만들기)를 본다.

### 2. 목록과 어댑터

`onCreate` 안, `// 2.` 자동 연결 Switch 블록 **아래**·`// 3.` [검색] 블록 **위**에 아래 모양을 채운다.

```kotlin
val devices = mutableListOf<String>()
// 어댑터 만들기: ArrayAdapter(화면, 한 줄 모양, 목록)
//   한 줄 모양은 Android가 준비한 android.R.layout.simple_list_item_1
// binding.deviceList.adapter에 어댑터를 넣는다
```

- `ArrayAdapter`가 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 `android.widget.ArrayAdapter`를 import한다.
- 두 `val`을 [검색] 블록 **아래**에 두면 빌드 오류가 난다. [막혔을 때](#막혔을-때)의 문구를 읽어 본다.
- 이 단계에서 실행하면 목록에 아무 줄도 없다. 왜 그런지 한 문장으로 적어 둔다.

### 3. [검색]에서 이름 넣기와 [중지]

1. 클래스 변수 자리, `permissionLauncher` 블록 **아래**에 6주차 `scanJob`과 같은 모양의 `private var deviceJob: Job? = null`을 만든다.
2. [검색] 리스너의 `viewModel.startScan()` **아래**에 아래 모양을 채운다. `Job`, `delay`, `Log`가 빨간색이면 import한다.

```kotlin
devices.clear()
adapter.notifyDataSetChanged()
deviceJob = lifecycleScope.launch {
    for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
        // 1초 기다리기
        // devices에 name 넣기
        // 어댑터에 목록이 바뀌었다고 알리기
        // val count = 목록의 개수, Log.d("Scan", "추가: $name, 장치 수: $count")
    }
}
```

3. [중지] 리스너의 `viewModel.stopScan()` **아래**에서 `deviceJob`을 취소한다(`?.`).
4. 실행하고 Logcat 필터를 `package:mine tag:Scan`으로 둔 뒤 표를 채운다.

| 조작 | 예상 목록 | 실제 목록 | Logcat 마지막 줄 |
|---|---|---|---|
| [검색] 후 3초 넘게 기다리기 |  |  |  |
| [검색] → 이름 두 개가 들어온 직후 [중지] |  |  |  |
| `끊김`(또는 [해제]) 뒤 다시 [검색] |  |  |  |

5. `for` **안**의 `adapter.notifyDataSetChanged()` 한 줄만 지우고 실행해 아래 표를 채운 뒤 **되돌린다**. 이 줄이 없을 때의 화면은 기기마다 조금 다를 수 있다.

| 관찰할 것 | 알림 있음 | 알림 없음 |
|---|---|---|
| Logcat `장치 수`가 1→2→3으로 찍히는가 |  |  |
| 목록이 1초마다 한 줄씩 느는가 |  |  |
| 몇 초 뒤 목록은 어떻게 보이는가 |  |  |

`장치 수`는 `"장치 수: $count"`처럼 `$count` 뒤에 한글을 바로 붙이지 않는다.

### 4. 목록의 한 줄 누르기

`onCreate` 안, `// 12.` [권한 확인] 블록 **아래**·`onCreate`를 닫는 `}` **위**에 리스너를 만든다.

```kotlin
binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    // adapter.getItem(position)으로 그 줄의 이름을 꺼낸다 (String?라서 ?: "")
    // 장치 이름 칸(EditText)에 넣는다: setText
    // Toast "선택: 이름"
}
```

| 누른 줄 | `position` 값 | 장치 이름 칸 |
|---|---|---|
| 첫째 줄 `ESP32_BLE_A` |  |  |
| 둘째 줄 `ESP32_BLE_B` |  |  |
| 셋째 줄 `ESP32_BLE_C` |  |  |

- `ESP32_BLE_B`를 누른 뒤 [연결]을 누르면 제어 화면 상단에 `장치: ESP32_BLE_B`가 보여야 한다. 1번 [연결] 코드는 고치지 않는다.
- EditText에 글자를 넣을 때는 `text = name`이 아니라 `setText(name)`이다.
- 막히면 [1일차 완성 코드](examples/day1/MainActivity.kt)와 한 줄씩 비교한다.

### 5. 오늘 확인할 것

- [ ] [검색]을 누르면 목록이 비워지고 이름 세 개가 1초마다 한 줄씩 늘어난다.
- [ ] [중지]를 누르면 더 늘지 않고, 들어간 이름은 남는다.
- [ ] 한 줄을 누르면 장치 이름 칸에 그 이름이 들어가고 Toast `선택: 이름`이 뜬다.
- [ ] 3번 표를 채웠고 `notifyDataSetChanged()`는 되돌렸다.
- [ ] 세 줄이 모두 보이는 **세로** 연결 화면을 캡처했다(캡처 1).

화면을 돌리면 상태는 이어지지만 목록은 비워진다. 폰 크기 화면을 가로로 돌리면 위아래가 잘려 일부 버튼·글자가 안 보일 수 있다. 확인할 항목이 안 보이면 세로로 되돌려 확인한다. 캡처는 돌리기 전에 세로에서 한다.
프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 마지막 장치 저장과 실기기 준비 (60분)

| 시간 | 할 일 |
|---|---|
| 0–8분 | 1일차 코드를 실행하고 `strings.xml`·`activity_main.xml`에 `lastDeviceText`와 `contactsButton` 자리를 만든다 |
| 8–18분 | [연결]에서 장치 이름을 SharedPreferences에 저장한다 |
| 18–32분 | `onCreate`에서 꺼내 `마지막 장치: …`로 보여 주고 관찰표를 채운다 → 캡처 2 |
| 32–52분 | A. 실기기를 준비해 앱을 실행한다 → 캡처 3 / B. 실기기가 없으면 연락처 읽기를 따라 한다 → 캡처 3 |
| 52–60분 | `MainActivity.kt`와 캡처 3장을 정리해 제출한다 |

### 1. 글자와 버튼 자리

1. `strings.xml`의 `device_list_title` 아래에 `last_device_none`(`마지막 장치: 없음`)과 `show_contacts`(`연락처 보기`)를 넣는다.
2. `activity_main.xml`에서 앱 제목 TextView **아래**·`deviceNameEdit` **위**에 id가 `lastDeviceText`인 TextView(글자 `@string/last_device_none`, `16sp`, 위 간격 `8dp`)를 넣는다.
3. `permissionButton` **아래**·`batteryText` **위**에 id가 `contactsButton`인 버튼(글자 `@string/show_contacts`)을 넣는다. 이 버튼은 5번 B에서 연결한다.
4. 실행해 제목 아래 `마지막 장치: 없음`이 보이면 다음으로 간다.

막히면 [따라하기 10단계](walkthrough.md#10-마지막-장치-글자와-연락처-보기-버튼-자리-만들기)를 본다.

### 2. [연결]에서 저장하기

`// 1.` [연결] 리스너의 `else {` 안, `val intent = …` 줄 **위**에 한 줄을 넣는다. 아래 네 조각을 점으로 이어 붙인다.

| 차례 | 조각 |
|---|---|
| 1 | `getSharedPreferences("smartio", MODE_PRIVATE)` |
| 2 | `.edit()` |
| 3 | `.putString("last", name)` |
| 4 | `.apply()` |

- `if (name.isEmpty())` 쪽이 아니라 `else` 쪽에 넣는 까닭을 한 문장으로 적는다.
- 실행해 [연결]이 1일차처럼 되면 된다. 화면에 달라지는 것은 없다.

### 3. 꺼내 보여 주기

`onCreate` 안, `// 19.` 목록 클릭 블록 **아래**·`onCreate`를 닫는 `}` **위**에 아래 모양을 채운다.

```kotlin
val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
val lastName = prefs.getString("last", "") ?: ""
// lastName이 비어 있으면 lastDeviceText에 "마지막 장치: 없음"
// 아니면 "마지막 장치: $lastName"
```

실행하고 아래 표를 채운다. 앱을 완전히 끄려면 최근 앱 화면에서 SmartIO를 위로 밀거나 Android Studio의 ■ Stop을 누른다.

| 조작 | 예상 글자 | 실제 글자 |
|---|---|---|
| `ESP32_BLE_C` 골라 [연결] → 제어 화면 [뒤로] |  |  |
| 이어서 화면 돌리기(안 보이면 세로로 되돌려 확인) |  |  |
| 앱을 완전히 끄고 다시 실행 |  |  |
| Android Studio에서 다시 `Run ▶` |  |  |
| 앱을 삭제(아이콘 길게 누르기 › 제거)한 뒤 `Run ▶` |  |  |

첫째 줄과 둘째 줄의 결과가 다른 까닭을 `onCreate`로 한 문장 적는다.

**앱을 완전히 끄고 다시 켠 첫 화면**에서 `마지막 장치: …`가 보이고 목록은 비어 있고 상태가 `연결 안 됨`인 화면을 **캡처한다(캡처 2).**

### 4. A. 실기기 준비

Android 폰이 있으면 [따라하기 14단계](walkthrough.md#14-실기기-준비하기)대로 준비하고 하나씩 체크한다.

- [ ] 빌드 번호를 7번 눌러 개발자 옵션을 켰다.
- [ ] 개발자 옵션에서 USB 디버깅을 켰다.
- [ ] USB 케이블로 연결하고 폰의 "USB 디버깅 허용"에서 허용을 눌렀다.
- [ ] Android Studio 기기 목록에 내 폰이 보이고 `Run ▶`으로 앱이 설치·실행되었다.
- [ ] 블루투스와 위치를 켰다.
- [ ] [권한 확인] → 권한 창 허용 → Toast `권한 OK`를 보았다.

12주차에 쓸 정보를 적어 둔다.

| 항목 | 내 폰 |
|---|---|
| 기기 이름(Android Studio 기기 목록) |  |
| Android 버전(설정 › 휴대전화 정보) |  |
| [권한 확인]에서 뜬 권한 창 이름("근처 기기" 또는 "위치") |  |

| 안 될 때 | 확인할 것 |
|---|---|
| 기기 목록에 폰이 없다 | 충전 전용이 아닌 케이블인지, 폰 화면의 허용 창을 눌렀는지, USB 디버깅을 껐다 켠 뒤 다시 꽂았는지 |
| 폰에 허용 창이 뜨지 않는다 | 폰의 잠금을 풀고 케이블을 다시 꽂는다 |
| 설치는 되는데 `마지막 장치: 없음` | 정상. 폰에는 앱이 새로 설치되어 저장한 값이 없다 |

실기기에서 앱이 뜬 연결 화면을 위쪽 상태 표시줄이 함께 보이게(가능하면 Toast `권한 OK`도 함께) **캡처한다(캡처 3).** 알림 내용이 보이지 않게 한다.

### 5. B. 연락처 읽기 (실기기가 없으면)

[따라하기 15~19단계](walkthrough.md#15-연락처-권한-선언하기)를 순서대로 한다.

1. `AndroidManifest.xml`의 `<application` 위에 `READ_CONTACTS` 권한을 선언한다.
2. **New › Kotlin Class/File › Object**로 `ContactsReader.kt`를 만들고 [제공 파일](examples/day2/ContactsReader.kt)의 내용을 붙여 넣는다.
3. `showPermissionDialog()` 아래에 `showContacts()`를 만든다. `ContactsReader.names(contentResolver)`가 비어 있으면 안내 대화상자, 아니면 `setItems`로 목록 대화상자를 띄운다.
4. `deviceJob` 아래에 10주차 `permissionLauncher`와 같은 모양으로 `contactsLauncher`를 만든다. `Manifest`는 `android.Manifest`를 import한다.
5. [연락처 보기] 리스너: 이미 허용이면 `showContacts()`, 아니면 `contactsLauncher.launch(arrayOf(Manifest.permission.READ_CONTACTS))`.

| 조작 | 예상 화면 | 실제 화면 |
|---|---|---|
| 처음 [연락처 보기] |  |  |
| 권한 창 [허용] (연락처 0명) |  |  |
| Contacts 앱에서 두 명 추가 → 돌아와 [연락처 보기] |  |  |
| 권한을 허용 안함으로 바꾼 뒤 [연락처 보기] → [허용 안함] |  |  |

연락처 이름 목록 대화상자(또는 `연락처가 0건입니다`, `연락처 권한 없음` 대화상자)를 **캡처한다(캡처 3).**

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 첫 줄이다. 파일 이름과 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 에뮬레이터에서 조금 다르게 보일 수 있다.

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'ArrayAdapter'.` | `ArrayAdapter`에 커서를 두고 Alt+Enter(맥 ⌥+Enter) → `android.widget.ArrayAdapter`를 import한다 |
| `Unresolved reference 'devicesList'.` (내가 쓴 이름이 따옴표 안에 나온다) | Kotlin의 `binding.` 뒤 이름과 `activity_main.xml`의 `android:id="@+id/deviceList"`가 글자까지 같은지 본다 |
| `Unresolved reference 'clear'.` 과 `Unresolved reference 'add'.` | 목록을 `listOf<String>()`로 만들었다. 넣고 비울 수 있는 `mutableListOf<String>()`로 바꾼다 |
| `Unresolved reference 'devices'.` (`'adapter'`와 함께 여러 줄 나온다) | `val devices`·`val adapter`가 [검색] 블록보다 **아래**에 있다. 선언한 줄보다 위에서는 쓸 수 없으니 [검색] 블록 위로 옮긴다 |
| `Assignment type mismatch: actual type is 'kotlin.String', but 'android.text.Editable!' was expected.` | `binding.deviceNameEdit.text = name`으로 썼다. EditText에는 `binding.deviceNameEdit.setText(name)`으로 넣는다 |
| `Unresolved reference 'count개'.` | `"장치 $count개"`처럼 `$count` 뒤에 한글을 붙였다. `"장치 수: $count"`처럼 뒤에 공백·기호를 두거나 순서를 바꾼다 |
| `No value passed for parameter 'p1'.` (편집기의 빨간 줄 설명에는 `mode`로 보일 수 있다) | `getSharedPreferences("smartio")`에 두 번째 값이 빠졌다. `getSharedPreferences("smartio", MODE_PRIVATE)`로 쓴다 |
| `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'kotlin.String?'.` | `prefs.getString("last", "")` 끝에 `?: ""`가 빠져 `lastName.isEmpty()`에서 막혔다. `?: ""`를 붙인다. `!!`는 쓰지 않는다 |
| [검색] 뒤 Logcat `tag:Scan`에는 `장치 수: 1`~`3`이 찍히는데 목록은 비어 있다. 상태가 `준비됨`이 되는 순간 세 줄이 한꺼번에 나타나고, `끊김`이면 끝까지 비어 있다 | `for` 안의 `devices.add(name)` 다음 줄에 `adapter.notifyDataSetChanged()`가 있는지 본다 |
| (예상) 실행하자마자 앱이 멈추고 Logcat에 `Don't call setOnClickListener for an AdapterView. You probably want setOnItemClickListener instead` | `binding.deviceList.setOnClickListener`로 썼다. `setOnItemClickListener { _, _, position, _ -> }`로 바꾼다 |
| (예상) 빌드도 되고 [연결]도 되는데 앱을 다시 켜도 늘 `마지막 장치: 없음` | 저장 줄 끝에 `.apply()`가 있는지, 저장과 꺼내기의 `"smartio"`·`"last"`가 글자까지 같은지 본다 |
| [연락처 보기]를 눌러도 권한 창이 안 뜨고 곧바로 `연락처 권한 없음`이 뜬다. 앱 정보 › 권한에 "연락처"가 없다 | `AndroidManifest.xml`에 `<uses-permission android:name="android.permission.READ_CONTACTS" />`가 있는지 본다 |
| `Unresolved reference 'permission'.` (`Manifest.permission`이 있는 줄마다 나온다) | 파일 위쪽 import가 `java.util.jar.Manifest`로 잘못 들어갔다. `import android.Manifest`로 바꾼다 |
| 앱을 삭제했다가 다시 설치했더니 `마지막 장치: 없음` | 코드 잘못이 아니다. 앱을 삭제하면 저장소도 함께 지워진다 |
| 화면을 돌리니 목록이 비워졌다 | 코드 잘못이 아니다. `devices`가 화면(Activity) 안에 있어서 새 화면이 빈 목록으로 시작한다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 코드 한 개와 캡처 3장

1. **`MainActivity.kt`**: 2일차 최종 코드
2. **캡처 1**: [검색] 뒤 `검색된 장치` 아래에 `ESP32_BLE_A`·`ESP32_BLE_B`·`ESP32_BLE_C` 세 줄이 보이는 세로 연결 화면
3. **캡처 2**: 앱을 완전히 끄고 다시 켠 첫 화면. 제목 아래 `마지막 장치: 이름`, 빈 목록, `연결 안 됨`이 보여야 한다
4. **캡처 3**: 실기기에서 앱이 실행된 연결 화면. 위쪽 상태 표시줄이 보여 실기기임을 알 수 있어야 한다(에뮬레이터 창을 찍은 캡처는 실기기 캡처로 보지 않는다). 실기기가 없으면 연락처 이름 목록, `연락처가 0건입니다`, `연락처 권한 없음` 대화상자 중 하나

채점은 [README 완료 기준](README.md#완료-기준)의 항목을 이 제출물로 확인한다. 실습지의 관찰표(1일차 3·4번, 2일차 3·5번 표)와 실기기 체크리스트, "내 폰" 표는 스스로 점검하는 것이라 제출하지 않고 채점하지 않는다.
1일차 목록(캡처 1)과 2일차 저장·복원(캡처 2)까지 동작하면 기본 성공이다. 실기기 준비와 연락처 읽기는 예제와 도움을 받아 마무리해도 된다.
캡처에 계정·알림 내용·실제 연락처가 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: 가짜 장치를 `ESP32_BLE_D`까지 네 개로 늘린다. 몇 초 만에 다 들어오는지 본다.
- 1일차: Toast를 `선택: ESP32_BLE_B (줄 번호 2)`처럼 바꾼다. `position`은 0부터 세므로 1을 더한 값을 `val`에 담아 쓴다.
- 2일차: 마지막 장치를 꺼내 보여 주는 코드를 `onCreate`에서 `onStart`로 옮겨, 제어 화면에서 [뒤로]로 돌아와도 곧바로 바뀌게 한다.
- 2일차: `마지막 장치: …` 글자를 누르면 저장된 이름을 장치 이름 칸에 넣는다.
- 2일차(연락처를 한 학생): 연락처 대화상자 제목을 `연락처 수: 2`처럼 바꾼다(`names.size`).

추가 과제는 선택 사항이다.
