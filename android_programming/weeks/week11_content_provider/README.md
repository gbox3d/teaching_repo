# 11주차 — 목록과 저장: ListView·SharedPreferences·ContentProvider 비교 + 실기기 준비

## 이번 주 질문

> 검색한 장치 이름을 화면에 한 줄씩 쌓아 고르게 하고, 마지막으로 연결한 장치를 앱을 껐다 켜도 기억하려면 어떻게 써야 할까?

10주차에는 배터리 방송을 받고 [권한 확인]으로 BLE 권한을 요청했다. 이번 주 1일차에는 연결 화면에 **ListView**를 두고, [검색]을 누르면 1초마다 가짜 장치 이름(`ESP32_BLE_A`…)을 목록에 넣는다. 한 줄을 누르면 그 이름이 장치 이름 칸에 들어가 [연결]로 제어 화면에 넘어간다.
2일차에는 마지막으로 연결한 장치 이름을 **SharedPreferences**에 저장해 앱을 다시 켜도 `마지막 장치: …`로 보여 준다. 다른 앱의 데이터를 읽는 **ContentProvider**는 연락처 읽기 시연으로 비교하고, 12주차 BLE 수업 전에 **실기기**에서 앱을 실행해 둔다.

## 학습 목표

1. `mutableListOf<String>()`로 목록을 만들고 `add`·`clear`·`size`로 넣고, 비우고, 센다.
2. `ListView`에 `ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)`를 끼워 목록을 화면에 보여 주고, 목록을 바꾼 뒤 `notifyDataSetChanged()`로 알린다.
3. `setOnItemClickListener { _, _, position, _ -> }`로 누른 줄의 이름을 꺼내 장치 이름 칸에 넣는다.
4. `getSharedPreferences("smartio", MODE_PRIVATE)`에 마지막 연결 장치를 저장하고, `onCreate`에서 꺼내 앱을 껐다 켜도 보이게 한다.
5. SharedPreferences와 ContentProvider의 차이를 비교표와 content URI로 설명하고, USB 디버깅으로 실기기에서 앱을 실행한다.

## 이번 주 결과물

```text
(1) 1일차 — [검색] 뒤 목록에 이름 세 줄

Smart I/O Controller
[ESP32_BLE_B      ]
자동 연결 (○)
[검색] [중지] [해제]
준비됨
검색된 장치
ESP32_BLE_A
ESP32_BLE_B
ESP32_BLE_C
[연결]
[권한 확인]
배터리 100% · 충전 중

(2) 2일차 — 앱을 껐다 켠 첫 화면

Smart I/O Controller
마지막 장치: ESP32_BLE_B
[장치 이름        ]
…
연결 안 됨
검색된 장치
(빈 목록)

(3) 2일차 — 실기기에서 실행한 연결 화면
    (실기기가 없으면 연락처 이름 목록 대화상자)
```

캡처 3장을 제출한다. 목록에 장치 이름 세 줄이 쌓인 연결 화면, 앱을 껐다 켠 뒤 `마지막 장치: …`가 보이는 화면, 실기기에서 앱이 실행된 화면이다. 실기기가 없으면 세 번째 캡처는 연락처 이름 목록(또는 `연락처가 0건입니다`, `연락처 권한 없음`) 대화상자로 대신한다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `mutableListOf`·`add`·`size`, ListView와 `ArrayAdapter`, `notifyDataSetChanged`, `setOnItemClickListener` | 목록 자리 → 목록과 어댑터 → [검색]에서 1초마다 이름 넣기·[중지] → 한 줄 누르기 → 캡처 1 | 장치 이름을 골라 연결하는 목록 화면 |
| 2일차 | SharedPreferences 저장·꺼내기, ContentProvider 비교와 연락처 읽기 시연, 실기기 준비, RecyclerView 소개 | 마지막 장치 저장·표시 → 앱 재시작 캡처 2 → 실기기 실행 캡처 3(없으면 연락처 읽기) | 마지막 장치를 기억하는 연결 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 10주차까지 만든 `SmartIO` 프로젝트(배터리 문구와 [권한 확인]이 있는 연결 화면). 없으면 10주차 완성본(`examples/day2`)을 받아 시작한다.
- 6주차에 배운 `lifecycleScope.launch`·`delay`와 `Job`·`cancel()`, 10주차에 배운 `for (permission in blePermissions())`
- 3주차 null 안전성 `?:`와 4주차 `getStringExtra(…) ?: ""`, `isEmpty()`
- 10주차 런타임 권한 흐름(`registerForActivityResult(RequestMultiplePermissions())`, `AlertDialog`)
- 2일차: Android 폰이 있으면 **데이터 전송이 되는 USB 케이블**을 가져온다. 없으면 에뮬레이터로 연락처 읽기를 한다.
- 이번 주에 쓰는 `ListView`, `ArrayAdapter`, `SharedPreferences`, `ContentResolver`는 Android 기본 기능이라 의존성을 더하지 않는다.

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `val devices = mutableListOf<String>()` | 글자를 담는, 늘리고 비울 수 있는 빈 목록. `<String>`은 "글자만 담는다"는 표시 |
| `devices.add(name)` / `devices.clear()` / `devices.size` | 끝에 하나 넣기 / 모두 비우기 / 들어 있는 개수 |
| `<ListView android:id="@+id/deviceList" android:layout_height="0dp" android:layout_weight="1" />` | 여러 줄을 세로로 쌓아 보여 주는 View. 남는 세로 공간을 모두 차지한다 |
| `ArrayAdapter(this, android.R.layout.simple_list_item_1, devices)` | 목록과 ListView를 잇는 어댑터. 가운데 값은 Android가 준비한 한 줄짜리 모양 |
| `binding.deviceList.adapter = adapter` | ListView에 어댑터를 끼운다 |
| `adapter.notifyDataSetChanged()` | 목록을 바꾼 뒤 어댑터에 알린다. 알려야 ListView가 다시 그려진다 |
| `binding.deviceList.setOnItemClickListener { _, _, position, _ -> }` | 한 줄을 누르면 실행된다. `position`은 누른 줄 번호(0부터) |
| `adapter.getItem(position) ?: ""` / `binding.deviceNameEdit.setText(name)` | 그 줄의 이름 꺼내기 / EditText에 글자 넣기 |
| `getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("last", name).apply()` | 이 앱 전용 저장소 `smartio`의 이름표 `last`에 값을 저장한다. 앱을 꺼도 남는다 |
| `prefs.getString("last", "") ?: ""` | 저장한 값을 꺼낸다. 없으면 기본값 `""` |
| ContentProvider, `content://com.android.contacts/contacts` | 다른 앱의 데이터를 내주는 창구와 그 주소. `contentResolver.query`로 요청한다(제공 `ContactsReader`, 시연) |
| `<uses-permission android:name="android.permission.READ_CONTACTS" />` | 연락처 읽기 권한. 10주차처럼 선언하고 실행 중에 허락받는다 |
| `private val contactsLauncher = registerForActivityResult(…)` | 연락처 권한 요청 틀. 10주차 `permissionLauncher`와 같은 모양으로 클래스 변수 자리에 둔다 |
| `ContactsReader.names(contentResolver)` | 제공 `ContactsReader.kt`에서 연락처 이름 목록을 받는다. 연락처가 없으면 빈 목록(0건은 실패가 아니다) |
| `AlertDialog.Builder(this).setItems(names.toTypedArray(), null)` | 대화상자에 이름 목록을 보여 준다. `setItems`가 배열을 받아서 `toTypedArray()`로 목록을 배열로 바꾼다 |
| `while (cursor.moveToNext())` / `cursor.close()` | 제공 `ContactsReader.kt` 안에서만 보는 코드. 결과 표를 한 줄씩 읽고, 다 읽으면 닫는다. 직접 쓰지 않는다 |
| 개발자 옵션 · USB 디버깅 | 실기기에 Android Studio로 앱을 설치·실행하기 위한 폰 설정 |

ContentProvider를 직접 만드는 법, 파일·데이터베이스 저장, RecyclerView 코드는 다루지 않는다. RecyclerView는 2일차에 소개만 한다.
회전하면 목록이 비워지는 문제(목록을 ViewModel로 옮기기)도 이번 주 범위 밖이다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [MainActivity.kt](examples/day1/MainActivity.kt) · [activity_main.xml](examples/day1/activity_main.xml) · [strings.xml](examples/day1/strings.xml)
- 2일차 완성 코드: [MainActivity.kt](examples/day2/MainActivity.kt) · [ContactsReader.kt](examples/day2/ContactsReader.kt) · [AndroidManifest.xml](examples/day2/AndroidManifest.xml) · [activity_main.xml](examples/day2/activity_main.xml) · [strings.xml](examples/day2/strings.xml)

## 완료 기준

아래 항목은 모두 2일차 제출물(`MainActivity.kt`와 캡처 3장)로 확인한다. 실습지의 관찰표·`position` 표·실기기 체크리스트·"내 폰" 표는 스스로 점검하는 것이고 채점하지 않는다.

- [ ] (1일차) `onCreate` 안, 리스너들보다 위에 `devices` 목록(`mutableListOf<String>()`)과 `ArrayAdapter`가 있고, `deviceList`에 어댑터를 끼웠다.
- [ ] [검색]을 누르면 목록이 비워지고 `ESP32_BLE_A`·`ESP32_BLE_B`·`ESP32_BLE_C`가 1초마다 한 줄씩 늘어난다(`add` 뒤 `notifyDataSetChanged()`). 도중에 [중지]를 누르면 더 늘지 않고, 이미 들어간 이름은 남는다.
- [ ] 목록의 한 줄을 누르면 장치 이름 칸에 그 이름이 들어가고 Toast `선택: 이름`이 뜨며, [연결]로 제어 화면에 그 이름이 보인다.
- [ ] 캡처 1은 [검색] 뒤 `검색된 장치` 아래에 세 줄이 모두 보이는 **세로** 연결 화면이다.
- [ ] (2일차) [연결]할 때 장치 이름을 `smartio` 저장소의 이름표 `last`에 저장하고, `onCreate`에서 꺼내 제목 아래에 `마지막 장치: 이름`(저장한 적이 없으면 `마지막 장치: 없음`)을 보여 준다.
- [ ] 캡처 2는 앱을 완전히 끄고 다시 켠 첫 화면이다. `마지막 장치: 이름`, 빈 목록, `연결 안 됨`이 함께 보인다.
- [ ] 캡처 3은 실기기에서 실행한 연결 화면이다(상태 표시줄이 보이게). 실기기가 없으면 연락처 이름 목록·`연락처가 0건입니다`·`연락처 권한 없음` 대화상자 중 하나다.
- [ ] `MainActivity.kt`와 캡처 3장을 제출한다.
- [ ] 캡처에 계정·알림 내용·실제 연락처 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [12주차 — BLE 기초: Bleuno 클라이언트로 검색·연결](../week12_ble_gatt/README.md)이다.
이번 주 [검색]이 넣던 가짜 이름을 제공 라이브러리의 `client.startScan(…)`이 찾은 진짜 장치 이름으로 바꾼다. 목록과 어댑터, 한 줄 누르기 코드는 그대로 쓴다.
보드와 연결하려면 실기기가 필요하다. 이번 주에 USB 디버깅·블루투스·위치·권한까지 확인해 두어야 12주차 수업 시간을 기기 문제로 쓰지 않는다.

## 공식 참고 자료

- [ListView — Android Developers](https://developer.android.com/reference/android/widget/ListView)
- [ArrayAdapter — Android Developers](https://developer.android.com/reference/android/widget/ArrayAdapter)
- [SharedPreferences로 간단한 데이터 저장 — Android Developers](https://developer.android.com/training/data-storage/shared-preferences)
- [콘텐츠 제공자 기본사항 — Android Developers](https://developer.android.com/guide/topics/providers/content-provider-basics)
- [하드웨어 기기에서 앱 실행 — Android Developers](https://developer.android.com/studio/run/device)
- [RecyclerView로 동적 목록 만들기 — Android Developers](https://developer.android.com/develop/ui/views/layout/recyclerview)
- [리스트 — Kotlin 문서](https://kotlinlang.org/docs/list-operations.html)
