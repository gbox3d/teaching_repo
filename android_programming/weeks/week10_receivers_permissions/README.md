# 10주차 — BroadcastReceiver와 런타임 권한

## 이번 주 질문

> 배터리가 바뀌었다는 시스템의 알림을 앱이 받아 화면에 보여 주려면, 그리고 BLE 장치를 찾기 전에 사용자에게 허락을 받으려면 어떻게 써야 할까?

9주차 앱 컴포넌트 비교표에서 Activity·Service·BroadcastReceiver·ContentProvider의 이름과 쓰임을 보았다. 이번 주에는 그중 **BroadcastReceiver**를 직접 만든다.
1일차에는 시스템이 보내는 배터리 방송을 받아 연결 화면 맨 아래에 `배터리 80% · 충전 중`을 보여 준다. 등록과 해제는 3주차에 본 `onStart`/`onStop`에 짝으로 둔다.
2일차에는 12주차 BLE 검색에 필요한 **런타임 권한**을 [권한 확인] 버튼으로 요청하고, 거절하면 `AlertDialog`로 알린 뒤 설정 화면으로 보낸다.

## 학습 목표

1. `object : BroadcastReceiver() { override fun onReceive(…) { } }` 틀을 복사해 방송을 받는 Receiver를 만든다.
2. `ContextCompat.registerReceiver`로 `onStart`에서 등록하고 `unregisterReceiver`로 `onStop`에서 해제해, 화면이 보이는 동안만 방송을 받는다.
3. `ACTION_BATTERY_CHANGED` 방송의 `intent`에서 `getIntExtra`로 남은 양·충전 여부를 꺼내 문구를 만들고, 에뮬레이터 Battery 설정으로 바뀌는 것을 확인한다.
4. 런타임 권한 5단계(선언 → 확인 → 설명 → 요청 → 결과)를 Manifest, `checkSelfPermission`, `registerForActivityResult(RequestMultiplePermissions())`로 구현한다.
5. 거절하면 `AlertDialog`를 띄우고, 암시적 `Intent`로 이 앱의 설정 화면을 연다.

## 이번 주 결과물

```text
(1) 1일차 — 연결 화면 맨 아래에 배터리 문구

Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]
연결 안 됨
[연결]
배터리 80% · 충전 중

(2) 2일차 — [권한 확인] → 권한 창에서 [허용 안함]

┌ 권한이 필요합니다 ─────────────────────┐
│ 장치를 검색하고 연결하려면 권한이 …    │
│                    [취소]  [설정으로]  │
└────────────────────────────────────────┘

(3) [설정으로] → 설정 앱의 "앱 정보"

Smart I/O Controller
권한 · 알림 · 저장용량 …
```

캡처 3장을 제출한다. 에뮬레이터 Battery 값을 바꾼 뒤 배터리 문구가 보이는 연결 화면, 권한을 거절한 뒤 뜬 `권한이 필요합니다` 대화상자, [설정으로]를 눌러 열린 앱 정보 화면이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `object : BroadcastReceiver()` 틀과 `!=`, 방송과 `IntentFilter`, `onStart` 등록·`onStop` 해제, `getIntExtra`로 배터리 값 꺼내기 | 배터리 글자 자리 만들기 → Receiver 틀 채우기 → 등록·해제 → 에뮬레이터 Battery로 관찰 → 캡처 1 | 배터리 문구가 바뀌는 연결 화면 |
| 2일차 | 런타임 권한 5단계와 Manifest 선언, 버전별 권한 함수, 요청과 결과 틀, `AlertDialog`와 설정 화면 Intent, `setResult` 시연 | 버튼·Manifest·`Permissions.kt` → 권한 확인 함수 → 거절 대화상자 → 요청 틀과 [권한 확인] → 캡처 2·3 | 권한 확인·거절 안내가 되는 연결 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 7주차까지 만든 `SmartIO` 프로젝트(`ConnViewModel`과 StateFlow로 `연결 안 됨`·`준비됨`이 바뀌는 연결 화면). 없으면 7주차 완성본(`examples/day2`)을 받아 시작한다.
- 3주차에 배운 생명주기 콜백(`onStart`·`onStop`)과 null 안전성 `?.`·`?:`
- 4주차에 배운 명시적 `Intent(this, ControlActivity::class.java)`와 `getStringExtra(…) ?: ""`
- 9주차 앱 컴포넌트 비교표(BroadcastReceiver는 "방송을 받는 컴포넌트, 화면 없음")
- 에뮬레이터는 수업 공지 기준을 따른다. Android 12(API 31) 이상이면 권한 창이 "근처 기기" 권한으로 뜬다.
- 이번 주에 쓰는 `ContextCompat`, `registerForActivityResult`, `AlertDialog`는 4주차 `build.gradle.kts`의 의존성에 이미 들어 있다.

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `object : BroadcastReceiver() { override fun onReceive(context: Context?, intent: Intent?) { } }` | (틀) 이름 없는 Receiver 하나를 만들어 변수에 담는다. 방송이 오면 `onReceive` 안이 실행된다 |
| `a != b` | 같지 않으면 참. `==`의 반대다 |
| `IntentFilter(Intent.ACTION_BATTERY_CHANGED)` | 여러 방송 가운데 "배터리가 바뀌었다" 방송만 골라 받는 거름망 |
| `ContextCompat.registerReceiver(this, batteryReceiver, 거름망, ContextCompat.RECEIVER_NOT_EXPORTED)` | Receiver를 등록한다. `RECEIVER_NOT_EXPORTED`는 다른 앱이 보낸 방송은 받지 않는다는 뜻(시스템 방송은 받는다) |
| `unregisterReceiver(batteryReceiver)` | 등록을 푼다. `onStart` 등록과 `onStop` 해제를 짝으로 둔다 |
| `intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1` | 방송에 실려 온 정수 값을 이름으로 꺼낸다. 없으면 기본값. 4주차 `getStringExtra`의 정수 판 |
| `<uses-permission android:name="…" />`, `android:maxSdkVersion="30"` | Manifest에 "이 권한을 쓴다"고 선언한다. `maxSdkVersion`은 그 버전 이하에서만 쓰는 선언 |
| `fun blePermissions(): Array<String>` (`Permissions.kt`, 제공) | 기기 Android 버전에 맞는 권한 이름 묶음(배열)을 돌려주는 함수. 클래스 없이 함수만 든 파일이다 |
| `ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED` | 그 권한이 아직 허용되지 않았으면 참 |
| `for (permission in blePermissions())` | 6주차 `for (i in 5 downTo 1)`처럼, 묶음 안의 것을 하나씩 꺼내 반복한다 |
| `registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ -> }` / `permissionLauncher.launch(blePermissions())` | (틀) 권한 요청 창을 띄우고, 사용자가 고르면 중괄호 안을 실행한다. 클래스 변수 자리(`onCreate` 밖)에서 만든다 |
| `AlertDialog.Builder(this).setTitle(…).setMessage(…).setPositiveButton("설정으로") { _, _ -> }.setNegativeButton("취소", null).show()` | 제목·본문·버튼 두 개가 있는 대화상자를 띄운다 |
| `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))` | 암시적 Intent. 열 화면 대신 할 일(ACTION)과 대상(주소)만 적으면 시스템이 맞는 화면을 찾는다 |

Manifest에 적는 Receiver, 앱이 직접 방송 보내기, 권한을 요청하기 전에 보여 주는 설명 화면은 다루지 않는다. 실제 장치 검색은 12주차에 이번 주 권한 흐름을 그대로 써서 한다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [MainActivity.kt](examples/day1/MainActivity.kt) · [activity_main.xml](examples/day1/activity_main.xml) · [strings.xml](examples/day1/strings.xml)
- 2일차 완성 코드: [MainActivity.kt](examples/day2/MainActivity.kt) · [Permissions.kt](examples/day2/Permissions.kt) · [AndroidManifest.xml](examples/day2/AndroidManifest.xml) · [activity_main.xml](examples/day2/activity_main.xml) · [strings.xml](examples/day2/strings.xml)

## 완료 기준

아래 항목은 모두 2일차 제출물(두 파일과 캡처 3장)로 확인한다. 실습지의 관찰표와 권한 표는 스스로 점검하는 것이고 채점하지 않는다.

- [ ] (1일차) 앱을 켜면 연결 화면 맨 아래 `배터리 ?`가 곧바로 `배터리 100% · 충전 중`처럼 숫자로 바뀐다.
- [ ] 에뮬레이터 Battery의 Charge level을 바꾸면 문구의 숫자가, Charger connection을 `None`으로 바꾸면 `충전 안 함`이 보인다.
- [ ] 등록은 `onStart`, 해제는 `onStop`에 있고 둘 다 `onCreate` 밖에 있다.
- [ ] 캡처 1은 Charge level을 100이 아닌 값으로 바꾼 **세로** 연결 화면이다(실기기는 상태 표시줄의 배터리 %와 같은 숫자면 된다).
- [ ] (2일차) `AndroidManifest.xml`의 `<application` 위에 `BLUETOOTH_SCAN`·`BLUETOOTH_CONNECT`와 `maxSdkVersion="30"`인 `ACCESS_FINE_LOCATION`이 선언되어 있다.
- [ ] [권한 확인]을 누르면 권한 창이 뜨고, 허용하면 Toast `권한 OK`가 보인다.
- [ ] 권한 창에서 거절하면 `권한이 필요합니다` 대화상자가 뜨고, [설정으로]를 누르면 이 앱의 앱 정보 화면이 열린다.
- [ ] `MainActivity.kt`, `AndroidManifest.xml`과 캡처 3장을 제출한다.
- [ ] 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [11주차 — 목록과 저장: ListView·SharedPreferences·ContentProvider 비교 + 실기기 준비](../week11_content_provider/README.md)다.
연결 화면에 장치 이름 목록을 두고, 마지막으로 연결한 장치 이름을 앱을 껐다 켜도 남게 저장한다.
2일차에는 이번 주 권한 흐름으로 연락처를 읽는 시연을 보고, 12주차 BLE 수업 전에 실기기를 연결해 권한까지 확인해 둔다.

## 공식 참고 자료

- [브로드캐스트 개요 — Android Developers](https://developer.android.com/develop/background-work/background-tasks/broadcasts)
- [배터리 상태 모니터링 — Android Developers](https://developer.android.com/training/monitoring-device-state/battery-monitoring)
- [런타임 권한 요청 — Android Developers](https://developer.android.com/training/permissions/requesting)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [대화상자 — Android Developers](https://developer.android.com/develop/ui/views/components/dialogs)
