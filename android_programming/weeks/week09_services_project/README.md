# 9주차 — 화면 없이 일하는 Service

## 이번 주 질문

> 지금까지 만든 화면은 모두 Activity였다. 화면이 없는 컴포넌트(Service)는 어느 스레드에서 돌고, 화면을 떠나 있는 동안에도 Service가 센 값을 화면에 다시 보여 주려면 그 값을 어디에 둬야 할까?

8주차에는 수업에서 나간 범위로 중간고사를 보았다. 이번 주 1일차에는 Android 앱을 이루는 네 컴포넌트(Activity·Service·BroadcastReceiver·ContentProvider)를 한 표로 비교하고,
7주차까지 만든 `SmartIO`에 `LogService`를 넣어 [서비스 시작]·[서비스 중지]로 직접 시작·중지하며 Logcat에서 **Service도 메인 스레드에서 돈다**는 것을 확인한다.
2일차에는 그 `LogService`가 **코루틴**으로 1초마다 센 숫자를 화면에 보여 준다. 값은 `object ServiceState`에 두고, 화면은 7주차에 쓴 `repeatOnLifecycle` 틀로 받는다.
수업 끝에는 Notification을 시연으로 한 번 보고 10주차 예고로 넘긴다.

## 학습 목표

1. Activity·Service·BroadcastReceiver·ContentProvider를 "무엇·언제·화면 유무·예"로 구분해 말하고, 네 컴포넌트가 Manifest에 적는 태그를 짝지어 말한다.
2. started·bound·foreground Service의 차이를 한 문장씩 말하고, `startService`·`stopService`와 Manifest `<service>` 등록이 4주차 `startActivity`와 같은 모양임을 설명한다.
3. Logcat의 `onStartCommand thread=main`을 읽고 "Service는 따로 스레드를 만들지 않는다"를 설명한다.
4. Service를 쓸 자리와 6·7주차 코루틴·ViewModel로 충분한 자리를 구분해 말한다.
5. `object ServiceState`에 `MutableStateFlow`를 두어 Service와 화면이 같은 값을 보게 하고, 7주차처럼 읽기 전용 `StateFlow`로 나누지 않는 이유를 말한다.
6. Service 안에서 `CoroutineScope(Dispatchers.Default)`로 코루틴을 만들어 1초마다 값을 올리고, `onDestroy`에서 그 코루틴을 취소하고 값을 되돌린다.
7. `repeatOnLifecycle(Lifecycle.State.STARTED)` 틀로 그 값을 받아 화면에 쓰고, 제어 화면에 갔다 돌아왔을 때 숫자가 어떻게 되는지 직접 보고 설명한다.
8. Notification이 화면 밖 사용자에게 알리는 방법이고 Android 13부터 권한이 필요하다는 것을 말한다(권한 요청은 10주차 2일차).

## 이번 주 결과물

```text
--- 1일차 캡처 (SmartIO + Logcat package:mine tag:Service) ---
onStartCommand thread=main      ← [서비스 시작]
onStartCommand thread=main      ← [서비스 시작] 한 번 더
onDestroy                       ← [서비스 중지]

--- 2일차 캡처 2장 (SmartIO 연결 화면) ---
[서비스 시작] [서비스 중지]       [서비스 시작] [서비스 중지]
센 횟수: (0이 아닌 수)            센 횟수: (앞 캡처보다 큰 수)
                                  ↑ [연결]로 제어 화면에 갔다 돌아온 뒤
```

1일차에는 Logcat에 서비스 시작·중지 줄과 스레드 이름(`thread=main`)이 보이는 캡처 1장, 2일차에는 숫자가 0이 아닌 화면과 제어 화면에 갔다 돌아온 뒤의 화면 캡처 2장을 제출한다.
제출물과 확인 방법은 [실습과 제출 안내](lab.md)에 있다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 4대 컴포넌트 비교표, started·bound·foreground, `LogService`와 Manifest `<service>`, 시작·중지 시연, Service를 쓸 자리와 안 쓸 자리 | `LogService.kt` 만들기 → Manifest에 적기 → 버튼 두 개와 `startService`·`stopService` → Logcat 관찰표 → 캡처 | [서비스 시작]·[서비스 중지]가 Logcat에 찍히는 `SmartIO` |
| 2일차 | Service와 화면은 서로 다른 객체, 값을 둘 자리(`object`와 `MutableStateFlow`), Service 안 코루틴, `repeatOnLifecycle`로 받기, 화면을 옮겨도 이어지는 숫자 시연, Notification 시연·예고 | `ServiceState.kt` 만들기 → `LogService`에 코루틴으로 세기 → `onDestroy`에서 취소·되돌리기 → 화면에 숫자 자리 → `repeatOnLifecycle`로 받기 → 캡처 2장 | `LogService`가 센 숫자를 연결 화면에 보여 주는 `SmartIO` |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 9주차는 일반 수업 주차이므로 두 날 모두 캡처 산출물이 있다.

## 이번 주는 SmartIO의 곁가지다

이번 주에 만드는 것은 학기 본줄기인 `SmartIO`에 쌓이지 않는다.

- **10주차 시작점은 7주차 완성본(`week07/examples/day2`)이다.** 9주차에 더한 [서비스 시작]·[서비스 중지] 버튼과 `LogService.kt`·`ServiceState.kt`, 숫자를 보여 주는 줄은 10주차 이후 예제에 들어가지 않는다.
- 1일차 예제([examples/day1](examples/day1))는 7주차 완성본에 `LogService`와 버튼 두 개만 더한 것이다. 2일차는 이 상태에서 이어서 만든다.
- 2일차 예제([examples/day2](examples/day2))는 1일차 예제에 `ServiceState.kt`와 숫자를 보여 주는 줄만 더한 2일차 끝 완성본이다. 같은 프로젝트(package `com.example.smartio`)이므로 새 프로젝트를 만들지 않는다.
- 두 날에 더한 파일과 버튼은 내 프로젝트에 남겨 두어도 되고 확인한 뒤 지워도 된다. 지우면 7주차 완성본과 같아진다. `SmartIO`는 학기 끝까지 Activity 두 개(`MainActivity`·`ControlActivity`)로 간다.
- 학기 과제는 BLE로 보드를 찾는 법을 배우는 12주차 1일차에 공지한다. 13주차 2일차에 계획안을 발표하고, 15주차에 완성본을 낸다. → [12주차](../week12_ble_gatt/README.md)

## 준비

- 7주차까지 만든 `SmartIO` 프로젝트(ViewModel·StateFlow 버전, [검색]·[중지]·[다시 시도]·[해제]가 동작하는 상태). 없으면 7주차 완성본([week07/examples/day2](../week07_flow_ui_state/examples/day2))을 받아 시작한다.
- 2일차에는 새 프로젝트를 만들지 않는다. 1일차에 고친 `SmartIO`에 그대로 이어서 한다.
- 다시 읽어 둘 것: 4주차 `Intent(this, ControlActivity::class.java)`·Manifest `<activity>`, 5주차 메인 스레드, 6주차 `delay`와 `Job` 취소, 7주차 `by viewModels()`·`MutableStateFlow`·`repeatOnLifecycle` 틀.
- Logcat 필터는 두 날 모두 `package:mine tag:Service`를 쓴다. 2일차에 더한 숫자는 Logcat이 아니라 화면에서 본다.

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| Activity / Service / BroadcastReceiver / ContentProvider | 앱의 네 가지 컴포넌트. 화면 / 화면 없이 일 맡기 / 시스템 소식 받기 / 다른 앱에 데이터 내주기 |
| `<activity>` / `<service>` / `<receiver>` / `<provider>` | 네 컴포넌트를 Manifest에 적는 태그. BroadcastReceiver는 코드로 등록하기도 한다 |
| started / bound / foreground Service | `startService`로 시작해 멈출 때까지 / 화면이 묶어 쓰는 동안 / 알림을 띄우고 계속. 이번 주에 만드는 것은 started 하나다 |
| `class LogService : Service()` | `Service`를 물려받은 화면 없는 컴포넌트 |
| `override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int` | `startService`를 부를 때마다 불린다. `return START_NOT_STICKY`는 "시스템이 끝내도 다시 살리지 않는다" |
| `override fun onDestroy()` | Service가 멈출 때 불린다 |
| `override fun onBind(intent: Intent?): IBinder? { return null }` | **틀**. 묶어 쓰지 않는 Service는 `null`을 돌려준다. 빼면 빌드가 안 된다 |
| `startService(intent)` / `stopService(intent)` | `Intent(this, LogService::class.java)`로 Service를 시작하고 멈춘다. 4주차 `startActivity`와 같은 모양 |
| `<service android:name=".LogService" android:exported="false" />` | Manifest 등록. `exported="false"`는 이 앱 안에서만 쓴다는 뜻 |
| `Thread.currentThread().name` | 지금 코드가 도는 스레드 이름. 메인 스레드면 `main` |
| `object ServiceState` | Service와 화면이 같이 보는 값을 두는 자리. `object`는 앱에 하나만 생긴다. 7주차 `object ConnState`와 같은 자리다 |
| `val tick = MutableStateFlow(0)` | 7주차와 같은 `MutableStateFlow`인데 두는 자리가 다르다. 7주차는 ViewModel 안에 숨기고 읽기 전용 `StateFlow`만 내보냈고, 여기서는 값을 올리는 쪽이 파일 바깥인 Service여서 숨기지 않는다 |
| `CoroutineScope(Dispatchers.Default)` | Service에는 ViewModel의 `viewModelScope`가 없다. 코루틴을 돌릴 자리를 직접 만든다. `Dispatchers.Default`는 메인 스레드가 아닌 곳이다 |
| `scope.launch { while (isActive) { delay(1000); … } }` | 6주차 `delay`를 그대로 쓴다. 7주차는 `viewModelScope`에서 돌렸고, 여기서는 직접 만든 scope에서 돈다 |
| `tickJob?.isActive == true` | 이미 세고 있으면 새로 시작하지 않는 검사. 7주차 `startScan`의 검사와 같은 모양이다 |
| `tickJob?.cancel()` | `onDestroy`에서 세던 코루틴을 취소한다. 6주차 `Job` 취소와 같다 |
| `repeatOnLifecycle(Lifecycle.State.STARTED)` 안의 `collect` | 7주차 2일차 틀 그대로다. 세 겹(`lifecycleScope.launch` → `repeatOnLifecycle` → `collect`)이 같고, 받아 오는 곳만 ViewModel에서 `object`로 바뀐다 |
| Notification | (시연·예고) 화면 밖 사용자에게 알리는 것. foreground Service는 꼭 띄운다. Android 13부터 권한이 필요하다 |

bound Service, foreground Service 코드, 알림 권한 요청 코드, Service 안에서 화면을 직접 고치기, 여러 Service를 묶어 쓰기는 다루지 않는다.
알림 권한은 런타임 권한이라 10주차 2일차 내용이다. 그래서 Notification은 이번 주에 **학생 실습으로 넣지 않고** 강의자 시연으로만 본다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [LogService.kt](examples/day1/LogService.kt) · [MainActivity.kt](examples/day1/MainActivity.kt) · [AndroidManifest.xml](examples/day1/AndroidManifest.xml) · [activity_main.xml](examples/day1/activity_main.xml) · [strings.xml](examples/day1/strings.xml)
- 2일차 완성 코드: [ServiceState.kt](examples/day2/ServiceState.kt) · [LogService.kt](examples/day2/LogService.kt) · [MainActivity.kt](examples/day2/MainActivity.kt) · [activity_main.xml](examples/day2/activity_main.xml) · [strings.xml](examples/day2/strings.xml)

## 완료 기준

아래 열 줄 가운데 제출해서 채점받는 것은 캡처 세 장이다(아홉째 줄). 코드 항목은 실습 시간에 스스로 확인하고, 막히면 순회하는 강의자에게 보여 준다.

- [ ] 네 컴포넌트 중 화면이 있는 것은 Activity 하나라는 것과, 각 컴포넌트의 예와 Manifest 태그를 하나씩 말할 수 있다.
- [ ] `LogService.kt`에 `onStartCommand`·`onDestroy`·`onBind` 세 함수가 있고, Manifest `<application>` 안에 `<service android:name=".LogService" android:exported="false" />`가 있다.
- [ ] [서비스 시작]을 두 번, [서비스 중지]를 한 번 눌러 Logcat `tag:Service`에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 순서대로 찍힌다.
- [ ] `thread=main`을 보고 "Service도 메인 스레드에서 돈다"와 "오래 걸리는 일은 스레드·코루틴으로 보낸다"를 설명할 수 있다.
- [ ] `ServiceState.kt`가 `object`이고 안에 `MutableStateFlow` 한 줄이 있다. 7주차처럼 읽기 전용 `StateFlow`로 나누지 않은 이유를 말할 수 있다.
- [ ] `LogService`가 `onStartCommand`에서 코루틴을 시작해 1초마다 `ServiceState.tick`을 올리고, 이미 세고 있으면 새로 시작하지 않는다.
- [ ] `onDestroy`에 `tickJob?.cancel()`과 `ServiceState.tick.value = 0` 두 줄이 있다.
- [ ] 화면의 숫자를 받는 코드가 `lifecycleScope.launch` → `repeatOnLifecycle(Lifecycle.State.STARTED)` → `collect` 세 겹 안에 있다.
- [ ] 캡처 1장(1일차 Logcat)과 캡처 2장(2일차 화면 두 장)을 제출한다.
- [ ] 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [10주차 — BroadcastReceiver와 런타임 권한](../week10_receivers_permissions/README.md)이다.
오늘 비교표의 셋째 줄 **BroadcastReceiver**를 직접 만들어 에뮬레이터 배터리 잔량·충전 상태를 SmartIO 연결 화면에 보여 주고,
2일차에는 12주차 BLE에 필요한 **런타임 권한**을 요청하고 거절되면 AlertDialog로 설정 화면에 보내는 흐름을 만든다.
10주차 시작점은 7주차 완성본이다. 이번 주에 더한 서비스 버튼과 숫자 줄은 있어도 없어도 된다.
오늘 2일차에 쓴 `object` + `MutableStateFlow` + `repeatOnLifecycle` 모양은 12주차에 보드의 연결 상태를 화면에서 받을 때 그대로 다시 쓴다.

## 공식 참고 자료

- [앱 기본 사항(앱 구성요소) — Android Developers](https://developer.android.com/guide/components/fundamentals)
- [서비스 개요 — Android Developers](https://developer.android.com/develop/background-work/services)
- [포그라운드 서비스 — Android Developers](https://developer.android.com/develop/background-work/services/fgs)
- [Android의 Kotlin 코루틴 — Android Developers](https://developer.android.com/kotlin/coroutines)
- [Android의 StateFlow 및 SharedFlow — Android Developers](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [수명 주기 인식 코루틴(repeatOnLifecycle) — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [알림 개요 — Android Developers](https://developer.android.com/develop/ui/views/notifications)
