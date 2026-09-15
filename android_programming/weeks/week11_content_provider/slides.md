---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 11주차
footer: 목록과 저장 · ListView·SharedPreferences·ContentProvider
---

# 목록과 저장: ListView·SharedPreferences·ContentProvider

10주차에는 배터리 방송을 받고 BLE 권한을 요청했습니다.
이번 주에는 연결 화면에 **장치 이름 목록**을 두고, 마지막으로 연결한 장치를 **저장**합니다.

```text
검색된 장치              Smart I/O Controller
ESP32_BLE_A              마지막 장치: ESP32_BLE_B
ESP32_BLE_B
ESP32_BLE_C
```

---

# 1일차 — 검색 목록 만들기

`30분 설명·시연 → 60분 실습`

1. `mutableListOf`로 목록을 만들고 `add`로 늘리기
2. `ListView`에 `ArrayAdapter`를 끼우고, 바꿨으면 `notifyDataSetChanged()`
3. `setOnItemClickListener`로 누른 줄의 이름 꺼내기

---

## 1일차 · 0–5분 — 오늘 문법: mutableListOf·add·size

```kotlin
val devices = mutableListOf<String>()   // 글자를 담는 빈 목록
devices.add("ESP32_BLE_A")
devices.add("ESP32_BLE_B")
val count = devices.size
println("장치 수: $count")               // 장치 수: 2
```

- `mutableListOf`: 늘리고 비울 수 있는 목록입니다. `<String>`은 "글자만 담는다"는 표시입니다.
- `add`는 끝에 하나 넣기, `clear()`는 모두 비우기, `size`는 개수입니다.
- 주의: `"장치 $count개"`는 빌드 오류입니다. Kotlin이 `count개`까지 변수 이름으로 읽습니다.

---

## 1일차 · 5–15분 ① — 목록과 ListView 사이의 어댑터

```text
devices (목록)        ArrayAdapter                  ListView (화면)
[A, B, C]    ──▶   "몇 줄? 0번 줄은 무엇?"   ──▶    ESP32_BLE_A
                    한 줄 모양 simple_list_item_1     ESP32_BLE_B
                                                      ESP32_BLE_C
```

- **ListView**는 여러 줄을 세로로 쌓아 보여 주는 View입니다. 스스로 글자를 갖지 않습니다.
- **어댑터**가 목록의 값을 한 줄씩 View로 만들어 ListView에 넘깁니다.
- 목록(데이터)과 화면을 나누고, 그 사이를 어댑터가 잇습니다.

---

## 1일차 · 5–15분 ② — XML에 ListView 놓기

```xml
<ListView
    android:id="@+id/deviceList"
    android:layout_width="240dp"
    android:layout_height="0dp"
    android:layout_weight="1"
    android:layout_marginTop="8dp" />
```

- 위치: 상태 글자 `stateText` 아래, [연결] 위. 바로 위에 제목 `검색된 장치` TextView를 둡니다.
- `0dp` + `layout_weight="1"`: 남는 세로 공간을 목록이 모두 차지합니다(4주차 `logText`와 같음).
- `wrap_content`로 두면 이름이 늘수록 아래 버튼이 화면 밖으로 밀립니다.

---

## 1일차 · 5–15분 ③ — ArrayAdapter 만들어 끼우기

```kotlin
// onCreate 안, [검색] 블록보다 위
val devices = mutableListOf<String>()
val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)
binding.deviceList.adapter = adapter
```

- 세 값: 화면(`this`), 한 줄의 모양, 목록.
- `android.R.layout.simple_list_item_1`: 우리 앱 `R`이 아니라 **Android가 준비한** 한 줄짜리 모양입니다.
- 아래 리스너들이 `devices`·`adapter`를 함께 씁니다. 그래서 **리스너보다 위**에 둡니다.
- `ArrayAdapter`가 빨간색이면 Alt+Enter(맥 ⌥+Enter) → `android.widget.ArrayAdapter`.

---

## 1일차 · 15–22분 ① — 목록을 바꿨으면 notifyDataSetChanged()

```kotlin
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

- `add`는 목록만 바꿉니다. ListView는 **알려 줘야** 다시 그립니다.
- `for (name in arrayOf(…))`: 10주차 `for (permission in blePermissions())`와 같은 모양입니다.
- 상태 카운트다운(7주차 ViewModel)은 그대로 따로 돕니다.

---

## 1일차 · 15–22분 ② — 알리지 않으면 어떻게 되나

| | `notifyDataSetChanged()` 있음 | 없음 |
|---|---|---|
| Logcat `tag:Scan`의 장치 수 | 1 → 2 → 3 | 1 → 2 → 3 |
| 화면의 목록 | 1초마다 한 줄씩 는다 | 늘지 않거나 나중에 한꺼번에 |

시연: `for` 안의 `notifyDataSetChanged()` 한 줄만 지우고 [검색]을 누릅니다.

- 데이터가 맞아도 화면은 알림을 받아야 바뀝니다. 가장 자주 빠뜨리는 한 줄입니다.
- [검색] 첫머리 `devices.clear()` 뒤에도 알립니다. 안 비우면 `A B C A B C`가 됩니다.
- [중지]에서는 6주차처럼 `deviceJob?.cancel()`로 이름 넣기를 멈춥니다.

---

## 1일차 · 22–27분 — 한 줄 누르기: setOnItemClickListener

```kotlin
binding.deviceList.setOnItemClickListener { _, _, position, _ ->
    val name = adapter.getItem(position) ?: ""
    binding.deviceNameEdit.setText(name)
    Toast.makeText(this, "선택: $name", Toast.LENGTH_SHORT).show()
}
```

- 넘어오는 값 4개 중 **줄 번호 `position`**만 씁니다. 0부터 셉니다(A=0, B=1, C=2).
- `getItem`은 `String?`를 돌려줍니다. 4주차 `getStringExtra(…) ?: ""`와 같은 모양입니다.
- EditText에 글자를 넣을 때는 `setText(name)`. `text = name`은 빌드 오류입니다.
- 1번 [연결]은 이 칸을 읽으므로 **고치지 않아도** 고른 이름이 제어 화면으로 갑니다.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--장치-목록-만들기-60분) · [따라하기](walkthrough.md#1일차)

1. `strings.xml`·`activity_main.xml`에 제목과 `deviceList`를 넣습니다.
2. `devices`·`adapter`를 [검색] 블록 **위**에 만듭니다.
3. [검색]에서 1초마다 이름 3개, [중지]에서 멈춤, 한 줄 누르면 이름 칸에 넣기.
4. 이름 세 줄이 보이는 **세로 화면**을 캡처합니다. 돌리면 목록이 비워집니다.

**설명 합계: 5+10+7+5+3 = 30분**

`Unresolved reference 'devices'.`가 나오면 15·16번이 [검색] 블록보다 위에 있는지 봅니다.

---

# 2일차 — 저장하기, 다른 앱의 데이터, 실기기

`30분 설명·시연 → 60분 실습`

1. SharedPreferences로 마지막 장치를 저장하고 꺼내기
2. ContentProvider는 다른 앱 데이터의 창구 — 연락처 읽기 시연
3. 12주차 전에 실기기에서 앱 실행하기

---

## 2일차 · 0–10분 ① — SharedPreferences: 앱을 꺼도 남는 저장소

| | 3주차 `onSaveInstanceState` | `SharedPreferences` |
|---|---|---|
| 남는 때 | 회전(화면을 다시 만들 때) | 앱을 끄고 다시 켜도 |
| 사라지는 때 | 앱을 완전히 끄면 | 앱을 삭제하면 |
| 모양 | `Bundle`에 이름표-값 | 이름 붙인 저장소에 이름표-값 |
| 이번 주 쓰는 곳 | — | 마지막 연결 장치 이름 |

- 이름표(키) `"last"`에 값 `"ESP32_BLE_B"`를 적어 두는 방식입니다.
- 설정값·마지막 선택처럼 **작은 값**에 씁니다. 긴 목록이나 사진은 넣지 않습니다.

---

## 2일차 · 0–10분 ② — 저장: edit → putString → apply

```kotlin
// [연결] 리스너의 else 안, Intent를 만들기 전
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()
```

| 조각 | 뜻 |
|---|---|
| `getSharedPreferences("smartio", MODE_PRIVATE)` | 이 앱만 쓰는 저장소 `smartio`를 연다(없으면 만든다) |
| `.edit()` | 고치기 시작 |
| `.putString("last", name)` | 이름표 `last`에 글자 넣기 |
| `.apply()` | 저장 확정. 빠뜨리면 저장되지 않는다 |

- [연결]로 **실제로 넘어갈 때만** 저장합니다. 이름이 비면 저장하지 않습니다.

---

## 2일차 · 0–10분 ③ — 꺼내기: getString(이름표, 기본값) ?: ""

```kotlin
// onCreate 끝
val prefs = getSharedPreferences("smartio", MODE_PRIVATE)
val lastName = prefs.getString("last", "") ?: ""
if (lastName.isEmpty()) {
    binding.lastDeviceText.text = "마지막 장치: 없음"
} else {
    binding.lastDeviceText.text = "마지막 장치: $lastName"
}
```

- 저장한 적이 없으면 기본값 `""`. `getString`은 `String?`라서 `?: ""`를 붙입니다.
- `"smartio"`·`"last"`는 저장할 때와 **글자까지 같게**. 다르면 늘 `없음`입니다.
- `onCreate`에서만 읽습니다. [뒤로]로 돌아왔을 때는 아직 안 바뀝니다.

---

## 2일차 · 10–18분 ① — ContentProvider: 다른 앱 데이터의 창구

| | SharedPreferences | ContentProvider |
|---|---|---|
| 누구의 데이터 | 내 앱 | 다른 앱(연락처·사진·일정) |
| 누가 읽나 | 내 앱만 | 허락받은 여러 앱 |
| 모양 | 작은 이름표-값 | 표(줄과 칸) |
| 여는 법 | `getSharedPreferences(…)` | `contentResolver.query(주소, …)` |
| 권한 | 필요 없음 | 연락처는 `READ_CONTACTS`(10주차 흐름) |

- 9주차 비교표의 네 번째 컴포넌트입니다. 오늘은 **만들지 않고 읽기만** 시연합니다.
- 파일·데이터베이스도 저장 방법이지만 이번 학기에는 이름만 압니다.

---

## 2일차 · 10–18분 ② — content URI 해부

```text
content://    com.android.contacts    /contacts
    │                  │                  │
창구 주소라는      어느 앱의 창구       그 안의 표
   표시             (연락처 앱)        (연락처 목록)
```

- 코드에서는 상수 `ContactsContract.Contacts.CONTENT_URI`로 씁니다. 값이 위 주소입니다.
- 웹 주소가 `https://`로 시작하듯, `content://`는 "ContentProvider에게 묻는 주소"입니다.
- 연락처 앱의 파일을 직접 열 수는 없습니다. 주소를 주고 창구에 **요청**합니다.

---

## 2일차 · 10–18분 ③ — 시연: ContactsReader.names(contentResolver)

```kotlin
// ContactsReader.kt(제공): 주소, 가져올 칸, 조건, 조건 값, 정렬
val cursor = resolver.query(
    ContactsContract.Contacts.CONTENT_URI,
    arrayOf(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY),
    null,
    null,
    ContactsContract.Contacts.DISPLAY_NAME_PRIMARY + " ASC"
)
```

- `cursor`는 결과 표를 한 줄씩 가리키는 손가락. `while (cursor.moveToNext())`로 읽고 `close()`.
- `MainActivity`에서는 `ContactsReader.names(contentResolver)` 한 줄로 부릅니다.
- 권한은 10주차 흐름 그대로: Manifest 선언 → 확인 → 요청 → 결과.
- 에뮬레이터는 처음에 연락처가 **0건**입니다. 0건은 실패가 아닙니다.

---

## 2일차 · 18–27분 ① — 실기기 준비: 개발자 옵션과 USB 디버깅

1. 설정 › 휴대전화 정보 › 소프트웨어 정보 › **빌드 번호**를 7번 누릅니다.
2. 설정 › **개발자 옵션** › **USB 디버깅**을 켭니다.
3. 데이터가 오가는 USB 케이블로 PC에 연결합니다. 충전 전용 케이블은 안 됩니다.
4. 폰에 뜬 "USB 디버깅을 허용하시겠습니까?"에서 **허용**합니다.
5. Android Studio 위쪽 기기 목록에서 내 폰을 고르고 `Run ▶`.

- 메뉴 이름·위치는 제조사와 Android 버전마다 조금 다릅니다.
- 폰에는 앱이 새로 설치됩니다. 에뮬레이터에 저장한 `마지막 장치`는 없습니다.

---

## 2일차 · 18–27분 ② — 12주차 전에 털어낼 것

| 확인 | 어떻게 | 안 되면 |
|---|---|---|
| 기기 인식 | 기기 목록에 폰 이름 | 케이블 바꾸기, 허용 창 확인, USB 디버깅 껐다 켜기 |
| 블루투스 | 빠른 설정에서 켜기 | 12주차 검색이 되지 않는다 |
| 위치 | 빠른 설정에서 켜기 | Android 11 이하는 검색 결과가 0개 |
| 권한 | [권한 확인] → Toast `권한 OK` | 10주차 거절 안내 → 설정에서 허용 |

- 12주차 제공 라이브러리의 `PermissionHelper.hasAll()`도 [권한 확인]과 같은 확인을 합니다.
- 실기기가 없으면 실습 32–52분에 연락처 읽기(2일차 실습 5번)로 캡처 3을 만듭니다.

---

## 2일차 · 27–30분 ① — 확장 소개: RecyclerView

| | ListView (이번 주) | RecyclerView |
|---|---|---|
| 한 줄 모양 | `simple_list_item_1` 그대로 | 내가 만든 한 줄 XML |
| 어댑터 | `ArrayAdapter` 한 줄 | 어댑터 클래스를 직접 작성 |
| 아주 긴 목록 | 된다 | 화면 밖 줄의 View를 다시 써서 더 가볍다 |
| 이번 학기 | 12~14주차에 계속 사용 | 소개만, 실습·채점 없음 |

- 요즘 앱의 긴 목록은 대부분 RecyclerView입니다. 목록 → 어댑터 → 화면 구조는 같습니다.

---

## 2일차 · 27–30분 ② — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--마지막-장치-저장과-실기기-준비-60분) · [따라하기](walkthrough.md#2일차)

1. `lastDeviceText`·`contactsButton` 자리를 만듭니다.
2. [연결]에서 저장하고 `onCreate`에서 꺼냅니다. 앱을 끄고 다시 켜서 캡처합니다.
3. 실기기가 있으면 USB 디버깅으로 실행해 캡처합니다.
4. 없으면 연락처 읽기를 따라 하고 대화상자를 캡처합니다.

**설명 합계: 10+8+9+3 = 30분**

앱을 **삭제**하면 저장소도 지워집니다. `없음`으로 돌아가도 코드 잘못이 아닙니다.

---

## 제출하기

2일차가 끝나면 한 번 제출합니다.

1. **`MainActivity.kt`**
2. **캡처 1**: [검색] 뒤 목록에 장치 이름 세 줄이 쌓인 연결 화면(세로)
3. **캡처 2**: 앱을 완전히 끄고 다시 켠 첫 화면 — `마지막 장치: …`, 빈 목록, `연결 안 됨`
4. **캡처 3**: 실기기에서 앱이 실행된 연결 화면, 상태 표시줄이 보이게(없으면 연락처 대화상자)

---

## 다음 주 미리 보기

이번 주 [검색]은 가짜 이름 `ESP32_BLE_A`·`B`·`C`를 넣었습니다.

12주차에는 제공 라이브러리의 `client.startScan(…)`이 **진짜 보드 이름**을 찾아 줍니다.

목록·어댑터·한 줄 누르기 코드는 그대로 두고, 이름을 넣는 곳만 바꿉니다.
