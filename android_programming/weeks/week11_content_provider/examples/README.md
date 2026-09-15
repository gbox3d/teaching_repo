# 11주차 예제 — 장치 목록과 마지막 장치 저장

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `deviceJob`, 목록과 어댑터(15·16번), [검색]에서 이름 넣기(17번), [중지]에서 멈추기(18번), 한 줄 누르기(19번) |
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` | `stateText` 아래에 제목 TextView와 `deviceList` 추가 |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | `device_list_title` 추가 |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `MainActivity.kt` | `contactsLauncher`, [연결]에서 저장(20번), 마지막 장치 표시(21번), [연락처 보기] 리스너(22번), `showContacts()`(23번) |
| [day2/ContactsReader.kt](day2/ContactsReader.kt) | `app › kotlin+java › com.example.smartio › ContactsReader.kt` (새 파일, New › Kotlin Class/File › **Object**) | 제공 코드. 받아서 붙여 넣는다 |
| [day2/AndroidManifest.xml](day2/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | `READ_CONTACTS` 권한 선언 추가 |
| [day2/activity_main.xml](day2/activity_main.xml) | `activity_main.xml` | 제목 아래 `lastDeviceText`, `permissionButton` 아래 `contactsButton` 추가 |
| [day2/strings.xml](day2/strings.xml) | `strings.xml` | `last_device_none`, `show_contacts` 추가 |
| `dayN/ConnState.kt`, `dayN/ConnViewModel.kt` | 상태 상수·ViewModel | 7주차 그대로, 바꾸지 않는다 |
| `dayN/ControlActivity.kt`, `dayN/activity_control.xml` | 제어 화면 | 7주차 그대로, 바꾸지 않는다 |
| `dayN/Permissions.kt` | 권한 목록 함수 | 10주차 그대로, 바꾸지 않는다 |
| `day1/AndroidManifest.xml`, `dayN/res/values/themes.xml` | Manifest·테마 | 10주차 그대로. 내 파일에는 아이콘 등 줄이 더 있어도 된다 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`ListView`, `ArrayAdapter`, `SharedPreferences`, `ContentResolver`, `ContactsContract`는 Android 기본 기능이라 `build.gradle.kts`에 더할 것이 없다.
주석 번호는 10주차 1~14에 이어 15~19(1일차), 20~23(2일차)를 붙였다. 번호는 넣은 순서라서 파일 안에서는 차례대로 놓이지 않는다. 15·16번은 2번과 3번 사이에 있고, 19·21·22번은 `onCreate` 안이라 10·11번보다 위에 있다.

## 1. `mutableListOf`·`add`·`size` — 늘어나는 목록

```kotlin
val devices = mutableListOf<String>()
devices.add("ESP32_BLE_A")
devices.add("ESP32_BLE_B")
val count = devices.size
Log.d("Scan", "장치 수: $count")
devices.clear()
```

| 실행 결과 | 값 |
|---|---|
| 두 번 `add` 뒤 `devices` | `[ESP32_BLE_A, ESP32_BLE_B]` |
| `count` | `2` |
| `clear()` 뒤 `devices.size` | `0` |

- `<String>`은 "글자만 담는 목록"이라는 표시다. `add`는 끝에 넣기, `clear`는 모두 비우기, `size`는 개수다.
- `"장치 $count개"`처럼 `$count` 뒤에 한글을 바로 붙이면 `Unresolved reference 'count개'.` 오류가 난다.

## 2. ListView와 `ArrayAdapter` — 목록을 화면에

```xml
<ListView
    android:id="@+id/deviceList"
    android:layout_width="240dp"
    android:layout_height="0dp"
    android:layout_weight="1"
    android:layout_marginTop="8dp" />
```

```kotlin
val devices = mutableListOf<String>()
val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
binding.deviceList.adapter = adapter
```

- 어댑터는 목록(`devices`)의 값을 한 줄씩 View로 만들어 ListView에 넘긴다. 세 값은 화면(`this`), 한 줄의 모양, 목록이다.
- `android.R.layout.simple_list_item_1`은 Android가 준비한 한 줄짜리 글자 모양이다. 우리 앱의 `R`이 아니다.
- 두 `val`은 `onCreate` 안, 이 둘을 쓰는 리스너들(3·4·19번)보다 **위**에 둔다. 아래에 두면 `Unresolved reference 'devices'.` 오류가 난다.
- `layout_height="0dp"` + `layout_weight="1"`은 남는 세로 공간을 목록이 모두 차지하게 한다. 연결 화면은 스크롤이 없다. 폰 크기 화면을 가로로 돌리면 위아래가 잘려 일부 버튼·글자가 안 보일 수 있고, 목록은 높이가 0이 되어 보이지 않는다. 확인할 항목이 안 보이면 세로로 되돌려 확인한다.

## 3. `notifyDataSetChanged()` — 바꿨으면 알린다

```kotlin
devices.clear()
adapter.notifyDataSetChanged()
deviceJob = lifecycleScope.launch {
    for (name in arrayOf("ESP32_BLE_A", "ESP32_BLE_B", "ESP32_BLE_C")) {
        delay(1000)
        devices.add(name)
        adapter.notifyDataSetChanged()
        val count = devices.size
        Log.d("Scan", "추가: $name, 장치 수: $count")
    }
}
```

| 실행 결과 | 화면 | Logcat `package:mine tag:Scan` |
|---|---|---|
| [검색] 직후 | 목록 비움, 상태 `연결 중… 5` | — |
| 1초·2초·3초 뒤 | `ESP32_BLE_A` → `B` → `C`가 한 줄씩 늘어남 | `추가: ESP32_BLE_A, 장치 수: 1` … `장치 수: 3` |
| 이름 두 개일 때 [중지] — `deviceJob?.cancel()` | 상태 `연결 안 됨`, A·B만 남음 | 두 줄에서 멈춤 |
| `끊김` 뒤 다시 [검색] | 목록이 비워지고 A·B·C가 다시 들어감 | 1부터 다시 |
| 화면 돌리기 | 상태는 이어지지만 목록은 비워지고 추가도 멈춤 | 멈춤 |

- `add`는 목록만 바꾼다. `notifyDataSetChanged()`로 알려야 ListView가 다시 그린다. `for` 안의 이 줄을 빼면 Logcat 개수는 늘어도 목록은 비어 있다. 상태가 `준비됨`이 되는 순간 세 줄이 한꺼번에 나타나고, `끊김`이면 끝까지 비어 있다.
- 이름을 넣는 코루틴은 화면의 `lifecycleScope`에서 돈다(6주차). 상태 카운트다운은 7주차 ViewModel에서 따로 돈다.
- 회전하면 `devices`가 새 화면에서 빈 목록으로 다시 만들어진다. 이번 주에는 고치지 않는다.

## 4. `setOnItemClickListener` — 누른 줄의 이름 꺼내기

```kotlin
binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    val name = adapter.getItem(position) ?: ""
    binding.deviceNameEdit.setText(name)
    Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
}
```

| 실행 결과 | 화면 |
|---|---|
| `ESP32_BLE_B`(둘째 줄, `position` 1) 누르기 | 장치 이름 칸 `ESP32_BLE_B`, Toast `선택: ESP32_BLE_B` |
| 이어서 [연결] | 제어 화면 상단 `장치: ESP32_BLE_B` |
| 제어 화면 [뒤로] | 연결 화면. 목록 그대로 |

- 넘어오는 값 네 개 가운데 줄 번호 `position`(0부터)만 쓰고 나머지는 `_`로 둔다.
- `getItem`은 `String?`를 돌려주므로 `?: ""`를 붙인다.
- EditText에는 `setText(name)`으로 넣는다. `binding.deviceNameEdit.text = name`은 `Assignment type mismatch: actual type is 'kotlin.String', but 'android.text.Editable!' was expected.` 오류가 난다.
- 1번 [연결]은 장치 이름 칸을 읽으므로 고치지 않는다.

## 5. SharedPreferences — 앱을 꺼도 남는 마지막 장치

```kotlin
// [연결] 리스너의 else 안 (20번)
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()
```

```kotlin
// onCreate 끝 (21번)
val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
val lastName = prefs.getString("last", "") ?: ""
if (lastName.isEmpty()) {
    binding.lastDeviceText.text = "마지막 장치: 없음"
} else {
    binding.lastDeviceText.text = "마지막 장치: $lastName"
}
```

| 실행 결과 | 제목 아래 글자 |
|---|---|
| 처음 설치 | `마지막 장치: 없음` |
| `ESP32_BLE_B` 골라 [연결] → [뒤로] | 그대로(`onCreate`에서만 읽는다) |
| 화면 돌리기(안 보이면 세로로 되돌려 확인), 또는 앱을 완전히 끄고 다시 실행 | `마지막 장치: ESP32_BLE_B` |
| Android Studio에서 다시 `Run ▶` | 그대로 남는다 |
| 앱 삭제 뒤 다시 설치 | `마지막 장치: 없음` |

- `smartio`는 저장소 이름, `last`는 이름표(키)다. 저장과 꺼내기에서 글자까지 같아야 한다.
- `MODE_PRIVATE`를 빼면 `No value passed for parameter 'p1'.`, `?: ""`를 빼면 `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'kotlin.String?'.` 오류가 난다.
- `.apply()`를 빠뜨리면 빌드는 되지만 저장되지 않는다(예상).
- 3주차 `onSaveInstanceState`는 회전할 때만 값을 넘긴다. SharedPreferences는 앱을 껐다 켜도 남는다.

## 6. ContentProvider와 `ContactsReader`(제공) — 다른 앱의 데이터 읽기

| | SharedPreferences | ContentProvider |
|---|---|---|
| 데이터 주인 | 내 앱 | 다른 앱(연락처·사진·일정) |
| 읽는 곳 | 내 앱만 | 허락받은 여러 앱 |
| 여는 법 | `getSharedPreferences(…)` | `contentResolver.query(주소, …)` |

```kotlin
val cursor = resolver.query(
    ContactsContract.Contacts.CONTENT_URI,
    arrayOf(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY),
    null,
    null,
    ContactsContract.Contacts.DISPLAY_NAME_PRIMARY + " ASC"
)
```

- `ContactsContract.Contacts.CONTENT_URI`의 값은 `content://com.android.contacts/contacts`다. `content://`(ContentProvider 주소라는 표시) + `com.android.contacts`(연락처 앱의 창구 이름) + `/contacts`(그 안의 표).
- `query`의 다섯 값은 주소, 가져올 칸, 조건, 조건 값, 정렬이다. `null`은 조건 없이 모두.
- 결과 `cursor`를 `while (cursor.moveToNext())`로 한 줄씩 읽어 이름을 목록에 넣고, 다 읽으면 `cursor.close()`한다. 전체는 [day2/ContactsReader.kt](day2/ContactsReader.kt)다.
- 연락처가 없으면 빈 목록을 돌려준다. 0건은 실패가 아니다.

## 7. `READ_CONTACTS` 요청과 연락처 대화상자

```xml
<uses-permission android:name="android.permission.READ_CONTACTS" />
```

```kotlin
binding.contactsButton.setOnClickListener {
    if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
        showContacts()
    } else {
        contactsLauncher.launch(arrayOf(Manifest.permission.READ_CONTACTS))
    }
}
```

| 실행 결과 | 화면 |
|---|---|
| 처음 [연락처 보기] | 시스템 권한 창(연락처 액세스 허용) |
| [허용], 연락처 0명 | 대화상자 `연락처` / `연락처가 0건입니다. 연락처 앱에서 한 명을 추가한 뒤 다시 눌러 보세요.` |
| 연락처 두 명 추가 뒤 [연락처 보기] | 권한 창 없이 대화상자 `연락처`에 이름순 두 줄, [닫기] |
| 권한 창 [허용 안함] | 대화상자 `연락처 권한 없음` |

- `contactsLauncher`는 10주차 `permissionLauncher`와 같은 모양으로 클래스 변수 자리에 만든다. 결과는 `_`로 두고 `checkSelfPermission`으로 다시 확인한다.
- 목록 대화상자는 `.setItems(names.toTypedArray(), null)`로 띄운다. `setItems`가 배열을 받아서 목록을 배열로 바꿔 넘긴다.
- `Manifest`는 `android.Manifest`를 import한다.
- Manifest 선언을 빼도 빌드는 된다. 그러면 권한 창 없이 곧바로 `연락처 권한 없음`이 뜬다.
- 권한 창 문구와 버튼 이름은 OS 버전과 언어 설정에 따라 조금 다르다.

## 8. 2일차 완성 — 목록, 저장, 연락처

[day2](day2) 파일을 모두 넣고 실행한 흐름:

```text
앱 시작(onCreate) → 저장소 smartio의 last 읽기 → 마지막 장치: 없음 / 이름
[검색] → 목록 비움 → 1초마다 A·B·C 추가 ─ [중지] ▶ 추가 멈춤
목록 한 줄 누르기 → 장치 이름 칸 + Toast 선택: 이름
[연결] → last에 이름 저장 → 제어 화면 장치: 이름
앱을 끄고 다시 켜기 → 마지막 장치: 이름
[연락처 보기] ─┬─ 허용 ─┬─ 0건 ▶ 연락처가 0건입니다
               │        └─ n건 ▶ 이름 목록 대화상자
               └─ 거절 ────────▶ 연락처 권한 없음
```

## 공식 참고 자료

- [ListView — Android Developers](https://developer.android.com/reference/android/widget/ListView)
- [ArrayAdapter — Android Developers](https://developer.android.com/reference/android/widget/ArrayAdapter)
- [SharedPreferences로 간단한 데이터 저장 — Android Developers](https://developer.android.com/training/data-storage/shared-preferences)
- [콘텐츠 제공자 기본사항 — Android Developers](https://developer.android.com/guide/topics/providers/content-provider-basics)
