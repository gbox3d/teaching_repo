# 12주차 — BLE 기초: Bleuno 클라이언트로 검색·연결

## 이번 주 질문

> 가짜 이름을 넣던 검색 목록에 진짜 보드를 띄우고, 한 줄을 눌러 연결한 뒤 두 화면에서 같은 연결 상태를 보려면 어떻게 써야 할까?

11주차에는 [검색]을 누르면 코루틴이 가짜 이름(`ESP32_BLE_A`…)을 목록에 넣었다. 이번 주 1일차에는 제공 라이브러리 **bleuno**를 프로젝트에 넣고, [검색]이 권한과 블루투스를 확인한 뒤 `client.startScan(…)`으로 **보드를 검색**하게 바꾼다. 보드가 없어도 가짜 클라이언트(`useFake = true`)로 똑같이 연습한다.
2일차에는 목록의 한 줄을 눌러 **연결**하고, 7주차 `collect` 틀로 `연결 중` → `서비스 확인 중` → `준비됨`을 화면에 보여 준다. 연결은 `Bleuno.client` 하나에 들어 있어서 제어 화면에서도 같은 상태가 보인다.

## 학습 목표

1. 폰(central)과 보드(peripheral)의 역할, GATT의 service·characteristic·UUID를 bleuno 보드의 실제 값으로 설명한다.
2. `name.startsWith("ESP32_BLE")`로 이름을 거르고, 블루투스가 꺼져 있으면 `ACTION_REQUEST_ENABLE` 요청 창을 10주차 결과 받기 틀(`StartActivityForResult`)로 띄운다.
3. `Bleuno.client ?: Bleuno.create(this, useFake)`로 앱 전체가 함께 쓰는 client를 받고, `startScan`·`stopScan`으로 5초 검색 목록을 만든다.
4. 목록 줄을 눌러 `client.connect(address)`로 연결하고, `client.connectionState`를 7주차 `collect` 틀로 받아 상태 글자·버튼과 제어 화면에 보여 준다.
5. Logcat `tag:BLE`로 연결 콜백 사슬을 읽고, 0개·블루투스 꺼짐·위치 서비스 꺼짐(Android 11 이하)일 때 무엇을 해야 하는지 화면으로 안내한다.

## 이번 주 결과물

```text
(1) 1일차 — [검색] 뒤 목록에 보드 이름 (Fake)

Smart I/O Controller
마지막 장치: 없음
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]
검색 완료 · 장치 수: 2
검색된 장치
ESP32_BLE_FAKE1 (00:11:22:33:44:01)
ESP32_BLE_FAKE2 (00:11:22:33:44:02)
[연결]
[권한 확인]
…

(2) 2일차 — 줄을 눌러 연결한 뒤 "준비됨" + Logcat tag:BLE

[ESP32_BLE_FAKE1 (00:11:22:33:44:01)]
[검색] [중지] [해제]        ← [해제]만 켜짐
준비됨
…
[연결]
[제어 화면]                 ← 준비됨일 때만 켜짐

connectGatt(가짜): 00:11:22:33:44:01
onConnectionStateChange(가짜): STATE_CONNECTED → 서비스 확인 중
onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨

(3) 보드 사진 — 연결 뒤 파랑 깜빡임이 멈추고 LED가 꺼진 보드
```

캡처 2장과 사진 1장을 제출한다. 목록에 `ESP32_BLE…` 줄이 뜬 연결 화면, `준비됨` 화면과 Logcat `tag:BLE`의 연결 줄, 연결된 보드 사진이다.
실보드로 연결하면 Logcat에 `onConnectionStateChange` → `onMtuChanged` → `onServicesDiscovered` 순서가 보인다. 보드·실기기가 없으면 사진은 생략하고 캡처를 Fake로 찍는다(수업 공지 기준).

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `startsWith`, central/peripheral·GATT·UUID와 bleuno 보드, 블루투스 켜기 요청, `Bleuno.create`·`startScan`·`stopScan` | bleuno 넣기·11주차 파일 정리 → client와 켜기 요청 틀 → [검색]·[중지] 바꾸기 → `onStop`에서 멈추기 → 캡처 1(보드가 있으면 `useFake = false`) | 보드 이름이 뜨는 검색 목록 |
| 2일차 | 콜백 사슬을 Logcat으로 읽기, `connect`·`disconnect`·`connectionState` collect, `object Bleuno`로 두 화면 공유, 0개·위치 꺼짐 안내 | 자리 만들기 → collect 대상 바꾸기·`ConnViewModel.kt` 지우기 → 줄 눌러 연결·[제어 화면] → 0개·위치 안내 → 캡처 2·사진 | `준비됨`까지 연결되는 두 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 11주차까지 만든 `SmartIO` 프로젝트(검색 목록·마지막 장치·[연락처 보기]가 있는 연결 화면). 없으면 11주차 완성본(`examples/day2`)을 받아 시작한다.
- 제공 라이브러리 [bleuno 패키지](../../bleuno/README.md)의 `src/` 파일 8개. 1일차 처음에 프로젝트에 붙여 넣는다.
- 에뮬레이터(AVD)는 **API 33 이상**을 쓴다. 이 이미지들은 가상 블루투스가 켜져 있어 Fake로 검색·연결 연습을 할 수 있다. 블루투스가 없는 이미지에서는 Fake여도 켜기 요청 창에서 막힐 수 있다.
- 실보드 연결은 11주차에 USB 디버깅까지 확인한 **Android 실기기**(Android 12 이상 권장)와 수업 보드(파랑 깜빡임 상태)가 있어야 한다. 에뮬레이터는 실제 보드를 찾을 수 없다. 학생은 펌웨어 코딩·빌드·플래싱을 하지 않는다.
- 3주차 `?.`·`?:`, 5주차 `isEnabled`·`visibility`, 7주차 `repeatOnLifecycle`·`collect`·`when`, 10주차 권한 흐름과 `onStart`/`onStop` 짝, 11주차 `mutableListOf`·`ArrayAdapter`·`setOnItemClickListener`
- `BluetoothGatt`·`StateFlow`·`org.json`은 Android 기본과 4주차 의존성에 들어 있어 `build.gradle.kts`에 더할 것이 없다. `AndroidManifest.xml`의 BLE 권한은 10주차에 넣은 그대로 쓴다.

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `name.startsWith("ESP32_BLE")` | 글자 `name`이 괄호 안 글자로 시작하면 `true`. 보드 이름은 `ESP32_BLE` + 칩 ID(예: `ESP32_BLE7C9EBF`) |
| central / peripheral | 검색하고 연결을 거는 쪽(폰) / 광고하며 연결을 기다리는 쪽(보드) |
| GATT server·client, service, characteristic, UUID | 연결 뒤 값을 주고받는 규칙. 보드(server)가 service 안에 characteristic을 두고, 폰(client)이 UUID로 찾아 쓴다 |
| `PermissionHelper.isBluetoothEnabled(this)` | 블루투스가 켜져 있으면 `true` |
| `registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result -> }` | 다른 창을 띄우고 돌아온 결과를 받는 틀. 10주차 `setResult` 시연과 같은 모양으로 클래스 변수 자리에 둔다 |
| `bluetoothLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE))` / `result.resultCode == RESULT_OK` | 시스템의 블루투스 켜기 요청 창을 띄운다 / 사용자가 [허용]을 눌렀다 |
| `if (…) { } else if (…) { } else { }`, `== false` | 1주차 `if/else`를 이어 붙여 차례로 확인한다. `== false`는 "아니면" |
| `private lateinit var client: BleunoClient` | `onCreate`에서 채우는 변수. `binding`과 같은 틀이다 |
| `client = Bleuno.client ?: Bleuno.create(this, useFake)` | 이미 만든 client가 있으면 그것을, 없으면 만들어 쓴다. 회전해도 같은 연결이 이어진다 |
| `client.startScan(5000, onFound = { device -> }, onFinished = { })` | 5초(5000밀리초) 검색. 보드를 찾을 때마다 `onFound`, 끝나면 `onFinished`. `onFound =`는 어느 칸에 넣는 람다인지 붙인 이름표 |
| `device.name` / `device.address` | 찾은 보드의 이름과 주소. `BleunoDevice`는 값을 묶어 두는 `data class`다 |
| `client.stopScan()` | 검색을 멈춘다. `onFinished`가 한 번 불린다. `onStop`에서도 부른다 |
| `client.connect(address)` / `client.disconnect()` | 그 주소의 보드에 연결을 시작한다 / 연결을 끊는다 |
| `client.connectionState.collect { state -> }` | 7주차 틀 그대로 연결 상태(`연결 안 됨`·`연결 중`·`서비스 확인 중`·`준비됨`·`끊김`)를 받는다 |
| `addresses.get(position)` | 목록에서 그 번호(0부터)의 값을 꺼낸다 |
| `Bleuno.client?.connectionState?.collect { }` | 제어 화면에서 같은 client의 상태를 받는다. `Bleuno.client`는 null일 수 있어 `?.`를 쓴다 |
| `binding.scanButton.performClick()` | 코드로 버튼을 누른다. [다시 시도]가 [검색]을 한 번 더 누른다 |
| `Build.VERSION.SDK_INT <= 30`, `PermissionHelper.isLocationEnabled(this)`, `Settings.ACTION_LOCATION_SOURCE_SETTINGS` | Android 11 이하인지, 위치 서비스가 켜져 있는지 확인하고 위치 설정 화면을 연다 |
| Logcat `package:mine tag:BLE` | 라이브러리가 남기는 검색·연결 콜백 기록. Fake는 `(가짜)`가 붙는다 |

`BluetoothGatt` 콜백을 직접 쓰는 일, 명령 보내기(`send`)와 응답 받기(`onMessage`)는 13주차, 끊김 뒤 재연결과 연결 시간 제한은 14주차에 다룬다.
bleuno 패키지 [README 6절](../../bleuno/README.md#6-사용-예--검색--연결--상태-표시--명령--응답)의 사용 예는 요약이다. 이번 주 코드는 [examples/day2](examples/day2)가 기준이다. 6절을 그대로 복사하면 회전할 때 client가 새로 만들어진다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 제공 라이브러리: [bleuno 패키지 README](../../bleuno/README.md) · [src 폴더](../../bleuno/src)
- 1일차 완성 코드: [MainActivity.kt](examples/day1/MainActivity.kt) · [ConnViewModel.kt](examples/day1/ConnViewModel.kt) · [bleuno/](examples/day1/bleuno)
- 2일차 완성 코드: [MainActivity.kt](examples/day2/MainActivity.kt) · [ControlActivity.kt](examples/day2/ControlActivity.kt) · [activity_main.xml](examples/day2/activity_main.xml) · [activity_control.xml](examples/day2/activity_control.xml) · [strings.xml](examples/day2/strings.xml)

## 완료 기준

아래 항목은 모두 2일차 제출물(`MainActivity.kt`·`ControlActivity.kt`, 캡처 2장, 사진 1장)로 확인한다. 실습지의 관찰표·상태별 버튼 표·"내 보드" 표는 스스로 점검하는 것이고 채점하지 않는다.

- [ ] (1일차) `bleuno` 패키지를 넣고, 11주차 `ConnState.kt`·`Permissions.kt` 대신 `com.example.smartio.bleuno`의 `ConnState`와 `PermissionHelper.required()`를 쓴다.
- [ ] `onCreate`에서 `client = Bleuno.client ?: Bleuno.create(this, useFake)`로 client를 받는다.
- [ ] [검색]은 권한 → 블루투스 순서로 확인한 뒤 `client.startScan(5000, onFound = …, onFinished = …)`으로 검색하고, `ESP32_BLE`로 시작하는 보드를 `이름 (주소)`로 목록에 넣는다. [중지]와 `onStop`에서 `client.stopScan()`을 부른다.
- [ ] 캡처 1은 [검색] 뒤 `검색된 장치` 아래에 `ESP32_BLE…` 줄(Fake면 `ESP32_BLE_FAKE1`·`ESP32_BLE_FAKE2`)이 보이는 **세로** 연결 화면이다.
- [ ] (2일차) 목록 줄을 누르면 같은 번호의 주소로 `client.connect(address)`하고, 7번 `collect`가 `client.connectionState`를 받아 상태 글자와 버튼을 바꾼다. `준비됨`일 때만 [해제]·[제어 화면]이 켜지고, [해제]를 누르면 `연결 안 됨`으로 돌아간다.
- [ ] [제어 화면]으로 넘어가면 상단에 `상태: 준비됨`이 보인다(`Bleuno.client?.connectionState` collect).
- [ ] 검색 결과가 0개면 `장치를 찾지 못했습니다 — [다시 시도]를 누르세요`와 [다시 시도]가 보이고, [검색]은 권한 → 블루투스 → 위치(Android 11 이하) 순서로 확인한다.
- [ ] 캡처 2는 `준비됨` 화면과 Logcat `package:mine tag:BLE`의 연결 줄이 함께 보이는 화면이다(한 화면에 담기 어려우면 두 장으로 나눠도 된다). 실보드는 `onConnectionStateChange` → `onMtuChanged` → `onServicesDiscovered`, Fake는 `connectGatt(가짜)` → `onConnectionStateChange(가짜)` → `onServicesDiscovered(가짜) → onDescriptorWrite → 준비됨` 순서다.
- [ ] 사진은 연결 뒤 파랑 깜빡임이 멈추고 LED가 꺼진 보드다. 보드·실기기가 없으면 생략하고 캡처 2를 Fake로 찍는다.
- [ ] `MainActivity.kt`, `ControlActivity.kt`, 캡처 2장, 사진 1장을 제출한다.
- [ ] 캡처와 사진에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [13주차 — BLE 출력 제어: 문자열 명령과 응답](../week13_ble_output/README.md)이다.
오늘 `준비됨`까지 연결한 `Bleuno.client`로 제어 화면에서 `client.send("on 3")`처럼 명령을 보내고, 보드가 돌려주는 JSON 응답을 `client.onMessage { }`로 받아 로그에 쌓는다.
제어 화면의 LED Switch가 로그에 `on 3`을 적기만 하던 4주차 코드가 진짜 보드의 LED를 켜게 된다. 보드 LED 번호가 GPIO가 아니라 인덱스 `0`~`3`이라는 점을 [bleuno README 2절](../../bleuno/README.md#n은-led-인덱스다)에서 미리 읽어 온다.

## 공식 참고 자료

- [Bluetooth Low Energy 개요 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [BLE 기기 찾기 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/find-ble-devices)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [블루투스 설정 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/setup)
- [활동 결과 가져오기 — Android Developers](https://developer.android.com/guide/components/activities/result)
- [bleuno 펌웨어 — GitHub](https://github.com/gbox3d/bleuno)
