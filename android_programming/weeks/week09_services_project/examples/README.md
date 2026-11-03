# 9주차 예제 — 화면 없이 일하는 Service

9주차 예제는 두 폴더다. 둘 다 7주차 `SmartIO`를 이어 가는 같은 프로젝트다.
1일차는 `LogService`를 더해 Logcat으로만 확인하고, 2일차는 그 Service가 센 숫자를 화면에 보여 준다.
두 폴더 모두 `build_examples.sh`로 따로 빌드된다. 만드는 순서는 [따라하기](../walkthrough.md)에 있다.

| 폴더 | 무엇 | package | 시작점 |
|---|---|---|---|
| [day1](day1) | 1일차 `LogService` 시작·중지 | `com.example.smartio` | 7주차 `examples/day2` |
| [day2](day2) | 2일차 Service가 센 숫자를 화면에 보여 주기 | `com.example.smartio` | 9주차 `examples/day1` |

`day2`는 `day1`의 파일을 그대로 두고 그 위에 더한 **2일차 끝 완성본**이다. 1일차에 만든 파일을 지우지 않는다.
두 폴더의 package가 같아서 `day1`을 따라 한 내 `SmartIO`에 그대로 이어서 2일차를 한다. 새 프로젝트를 만들지 않는다.

**두 폴더는 다음 주 시작점이 아니다.** 9주차는 SmartIO 본줄기의 **곁가지**다.
10주차 `examples/day1`은 7주차 `examples/day2`에서 시작하며, 9주차에 더한 `LogService.kt`·`ServiceState.kt`와 [서비스 시작]·[서비스 중지] 버튼, 숫자를 보여 주는 `serviceTickText`는 10주차 이후 예제에 들어가지 않는다.
따라 해 내 `SmartIO`에 그것이 남아 있어도 10주차 진행에 영향이 없고, 지우면 7주차 완성본과 같아진다.
`SmartIO`는 학기 끝까지 Activity 두 개(`MainActivity`·`ControlActivity`)로 간다.

Notification(2일차 22–27분)은 예제 코드가 없다. 알림을 띄우려면 Android 13부터 런타임 권한이 필요하고 런타임 권한은 10주차 2일차 내용이라, 이번 주에는 강의자 시연으로만 본다.

## 파일과 넣을 위치

### day1 — 7주차 SmartIO에 더한 것

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [LogService.kt](day1/LogService.kt) | `app › kotlin+java › com.example.smartio › LogService.kt` | 새 파일(New › Kotlin Class/File › Class) |
| [MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `onCreate()` 끝에 `// 10.` [서비스 시작], `// 11.` [서비스 중지] |
| [activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` | 맨 아래에 버튼 두 개짜리 가로 줄 |
| [strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | `service_start`, `service_stop` |
| [AndroidManifest.xml](day1/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | `</application>` 위에 `<service>` 세 줄과 주석 |
| `ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `activity_control.xml`, `res/values/themes.xml` | 같은 이름의 파일 | 7주차 `examples/day2` 그대로, 바꾸지 않는다 |

### day2 — 1일차 SmartIO에 더한 것

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [ServiceState.kt](day2/ServiceState.kt) | `app › kotlin+java › com.example.smartio › ServiceState.kt` | 새 파일(New › Kotlin Class/File › Object) |
| [LogService.kt](day2/LogService.kt) | `app › kotlin+java › com.example.smartio › LogService.kt` | 코루틴 import 여섯 줄, `scope`·`tickJob` 두 줄, `// 5.` 겹쳐 시작 막기, `// 6.` 1초마다 세기, `// 7.` 취소·되돌리기 |
| [activity_main.xml](day2/activity_main.xml) | `app › res › layout › activity_main.xml` | 서비스 버튼 줄 아래에 `serviceTickText` TextView |
| [MainActivity.kt](day2/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `onCreate()` 끝에 `// 12.` 숫자 받아 쓰기 |
| [strings.xml](day2/strings.xml) | `app › res › values › strings.xml` | `service_tick_zero` |
| `AndroidManifest.xml`, `ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `activity_control.xml`, `res/values/themes.xml` | 같은 이름의 파일 | 1일차 그대로, 바꾸지 않는다 |

Kotlin 파일 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`day2`에서 더한 줄의 주석에는 `(9주차 2일차)` 꼬리표가 붙어 있고, 번호는 1일차 번호에서 이어진다(`LogService.kt`는 5·6·7번, `MainActivity.kt`는 12번, 새 파일 `ServiceState.kt`는 1·2번).
코루틴·`StateFlow`·`repeatOnLifecycle`에 필요한 라이브러리는 4주차 `build.gradle.kts`에 이미 들어 있어 따로 넣지 않는다.
Logcat 필터는 두 일차 모두 `package:mine tag:Service`다. 2일차에 더한 숫자는 Logcat이 아니라 화면에서 본다.

아래 1~4절은 1일차 내용(컴포넌트와 Service), 5~7절은 2일차 내용(값을 둘 자리·코루틴·화면에서 받기)이다.

## 1. 네 가지 컴포넌트는 Manifest에 적는다

`day1/AndroidManifest.xml`에는 4주차의 `<activity>` 줄 옆에 1일차에 넣은 `<service>` 줄이 있다.

```xml
        <activity
            android:name=".ControlActivity"
            android:exported="false" />
```

```xml
        <service
            android:name=".LogService"
            android:exported="false" />
```

| 컴포넌트 | 화면 | Manifest | 이 과목 |
|---|---|---|---|
| Activity | 있음 | `<activity>` | 2~7주 매주 |
| Service | 없음 | `<service>` | 9주 1일차 |
| BroadcastReceiver | 없음 | `<receiver>` 또는 코드로 등록 | 10주 |
| ContentProvider | 없음 | `<provider>` | 11주 비교·시연 |

- `exported="false"`는 이 앱 안에서만 쓴다는 뜻이다.
- `<service>` 줄이 없어도 빌드는 된다. 그러면 [서비스 시작]을 눌러도 Service가 시작되지 않는다(Logcat `tag:Service`에 아무것도 찍히지 않는다).

## 2. started Service — onStartCommand·onDestroy·onBind

```kotlin
class LogService : Service() {
```

```kotlin
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        // 2. 시스템이 이 Service를 강제로 끝내도 다시 살리지 않는다(9주차 1일차).
        return START_NOT_STICKY
    }
```

```kotlin
    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
```

- `onStartCommand`는 `startService`를 부를 **때마다** 불린다. 이미 돌고 있어도 다시 불린다.
- `onDestroy`는 `stopService`로 멈출 때 한 번 불린다.
- `onBind`는 화면과 묶어 쓰는(bound) Service가 아니면 `null`을 돌려주는 틀이다. 빼면 `Class 'LogService' is not abstract and does not implement abstract base class member 'onBind'.` 오류로 빌드가 안 된다.
- 반환형을 `IBinder`(물음표 없음)로 쓰면 `return null` 줄에 `Null cannot be a value of a non-null type 'android.os.IBinder'.` 오류가 난다. New › Service › Service로 만들면 이 모양으로 생기므로 `IBinder?`로 고친다.

## 3. startService / stopService — 4주차 startActivity와 같은 모양

```kotlin
        binding.serviceStartButton.setOnClickListener {
            val intent = Intent(this, LogService::class.java)
            startService(intent)
        }
```

```kotlin
        binding.serviceStopButton.setOnClickListener {
            val intent = Intent(this, LogService::class.java)
            stopService(intent)
        }
```

| 조작 | 화면 | Logcat `package:mine tag:Service` |
|---|---|---|
| [서비스 시작] | 바뀌지 않는다(Service는 화면이 없다) | `onStartCommand thread=main` |
| [서비스 시작] 한 번 더 | 바뀌지 않는다 | `onStartCommand thread=main` 한 줄이 더 찍힌다 |
| [서비스 중지] | 바뀌지 않는다 | `onDestroy` |
| 멈춘 상태에서 [서비스 중지] 한 번 더 | 바뀌지 않는다 | 아무것도 찍히지 않는다 |
| [검색] 카운트다운 중 [서비스 시작] | 카운트다운이 끊기지 않는다 | `onStartCommand thread=main` |

- `LogService::class.java`를 빼고 `Intent(this, LogService)`로 쓰면 `None of the following candidates is applicable:` 과 `Classifier 'class LogService : Service' does not have a companion object, so it cannot be used as an expression.` 오류가 난다.
- Service가 돌고 있을 때 뒤로 가기로 앱을 닫으면, Android 8 이상에서는 잠시 뒤 시스템이 Service를 멈춰 `onDestroy`가 찍힌다(Android 14 에뮬레이터에서 약 1분 뒤). 확인은 앱을 연 채로 한다.

## 4. Service도 메인 스레드에서 돈다

```kotlin
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
```

- Logcat의 `thread=main`은 5주차에 본 메인 스레드다. Service는 따로 스레드를 만들지 않는다.
- 그래서 `onStartCommand` 안에서 `Thread.sleep(10000)`처럼 오래 걸리는 일을 하면 화면이 10초 동안 멈춘다. 5주차 1일차 시연과 같다. 멈춘 동안 버튼을 누르면 약 5초 뒤 "Smart I/O Controller이(가) 응답하지 않음" 창([앱 닫기]·[대기])이 뜨고, 10초가 지나 앱이 풀리면 창은 저절로 닫힌다(Android 14 에뮬레이터에서 확인).
- 오래 걸리는 일은 Service 안에서도 5주차 `Thread { }.start()`나 6주차 코루틴으로 보낸다. 1일차 `LogService`는 로그 한 줄만 찍고 곧바로 끝낸다. 2일차 6절에서 코루틴을 넣는다.

## 5. 값을 둘 자리 — object와 MutableStateFlow

```kotlin
object ServiceState {
    val tick = MutableStateFlow(0)
}
```

- `LogService`와 `MainActivity`는 서로 다른 객체다. Service는 화면을 모르고, 화면은 Service가 만든 변수를 볼 수 없다. 둘이 같이 보는 값을 한 군데 둬야 한다.
- `object`는 앱에 하나만 생긴다. 어디서 `ServiceState.tick`을 불러도 같은 것이다. 7주차 `ConnState`를 `object`로 둔 것과 같은 자리다.
- 7주차 `ConnViewModel`은 바꾸는 쪽 `private val _seconds`와 읽기 전용 `val seconds: StateFlow<Int>`를 나눴다. 값을 바꾸는 곳이 그 클래스 안이었기 때문이다.
- 이번에는 값을 올리는 곳이 이 파일 바깥의 `LogService`다. 나누려면 값을 올리는 함수를 `ServiceState`에 같이 두고 `LogService`가 그 함수를 부르게 해야 한다(그 모양도 빌드로 확인).
- 이번 예제는 새 파일을 한 줄로 두려고 나누지 않는 쪽을 골랐다. 못 나누는 것이 아니다.
- 7주차처럼 `val tick: StateFlow<Int> = MutableStateFlow(0)`로 감싸 두기만 하면, `LogService`에서 값을 올리는 두 줄에 `'val' cannot be reassigned.` 오류가 난다(빌드로 확인).
- `import kotlinx.coroutines.flow.MutableStateFlow`가 빠지면 `Unresolved reference 'MutableStateFlow'.`가 난다(빌드로 확인).
- `ServiceState.kt`를 만들지 않고 다른 파일을 먼저 고치면 `Unresolved reference 'ServiceState'.`가 `LogService.kt`와 `MainActivity.kt` 양쪽에 난다(빌드로 확인).

## 6. Service가 코루틴으로 1초마다 센다

```kotlin
    private val scope = CoroutineScope(Dispatchers.Main)
```

```kotlin
    private var tickJob: Job? = null
```

```kotlin
        if (tickJob?.isActive == true) {
            return START_NOT_STICKY
        }
```

```kotlin
        tickJob = scope.launch {
            while (isActive) {
                delay(1000)
                ServiceState.tick.value++
            }
        }
```

```kotlin
        tickJob?.cancel()
        ServiceState.tick.value = 0
```

- 4절에서 Service도 메인 스레드에서 돈다는 것을 봤다. 1초마다 세는 일을 `onStartCommand` 안에서 그냥 하면 화면이 멈춘다. 그래서 6주차 코루틴으로 보낸다. 이것이 1일차에서 본 문제의 해결이다.
- `delay(1000)`은 기다리는 동안 스레드를 붙잡지 않는다. 5주차 `Thread.sleep`과 다른 점이다.
- Service에는 ViewModel의 `viewModelScope`가 없다. `CoroutineScope(Dispatchers.Main)`으로 코루틴을 돌릴 자리를 직접 만든다. `Dispatchers.Main`은 4절에서 Logcat으로 본 그 메인 스레드다. 바로 위 줄에서 본 대로 `delay`가 스레드를 붙잡지 않으므로 메인 스레드에서 세도 화면이 멈추지 않는다.
- `if (tickJob?.isActive == true)`는 7주차 `ConnViewModel.startScan`과 같은 검사다. [서비스 시작]을 여러 번 눌러도 코루틴은 하나만 돈다.
- `onDestroy`의 `tickJob?.cancel()`과 `ServiceState.tick.value = 0`은 세기를 멈추고 숫자를 되돌린다. 이 두 줄을 빼도 **빌드는 된다**(빌드로 확인). 그러면 [서비스 중지] 뒤에도 코루틴이 그대로 돌고, `ServiceState`는 앱에 하나뿐이라 값이 남는다.
- `while (isActive)`의 `isActive`는 `import kotlinx.coroutines.isActive`가 필요하다. 빠지면 `Unresolved reference 'isActive'.`가 난다(빌드로 확인).
- `delay` import가 빠지면 `Unresolved reference 'delay'.`가 난다(빌드로 확인).

| 조작 | 코드가 하는 일 |
|---|---|
| [서비스 시작] | `onStartCommand`가 코루틴을 시작한다. 1초마다 `ServiceState.tick`이 1 올라간다 |
| [서비스 시작] 한 번 더 | `onStartCommand`는 또 불리지만 `tickJob`이 살아 있어 코루틴을 새로 시작하지 않는다. 세던 숫자가 끊기지 않는다 |
| [서비스 중지] | `onDestroy`가 코루틴을 취소하고 `ServiceState.tick`을 0으로 되돌린다 |
| 멈춘 상태에서 [서비스 중지] 한 번 더 | `onDestroy`가 불리지 않는다. 아무것도 바뀌지 않는다 |

## 7. 화면에서 받기 — repeatOnLifecycle

```xml
    <TextView
        android:id="@+id/serviceTickText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/service_tick_zero"
        android:textSize="18sp" />
```

```kotlin
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                ServiceState.tick.collect { tick ->
                    binding.serviceTickText.text = "센 횟수: $tick"
                }
            }
        }
```

- 7주차 2일차 `viewModel.seconds.collect`와 같은 틀이다. `lifecycleScope.launch` → `repeatOnLifecycle` → `collect` 세 겹이 그대로고, 받아 오는 곳만 ViewModel에서 `ServiceState`로 바뀌었다.
- `Lifecycle.State.STARTED`는 화면이 보일 때만 받는다는 뜻이다. [연결]로 제어 화면에 가 있는 동안에는 받지 않는다.
- 그동안에도 Service는 계속 센다. 화면이 다시 보이면 `StateFlow`가 마지막 값을 한 번 내주므로 숫자가 이어진 자리에서 보인다. Service를 따로 두는 이유가 여기서 드러난다.
- 회전해도 같은 틀로 마지막 값을 다시 받는다. 7주차 2일차와 같다.
- `collect`를 `lifecycleScope.launch` 밖에 두면 `Suspend function 'suspend fun collect(collector: FlowCollector<Int>): Nothing' should be called only from a coroutine or another suspend function.` 오류가 난다(빌드로 확인).
- layout에 `serviceTickText`를 넣지 않고 Kotlin만 고치면 `Unresolved reference 'serviceTickText'.`가 난다(빌드로 확인).
- `strings.xml`에 `service_tick_zero`가 없으면 Kotlin이 아니라 자원 단계에서 막힌다. `error: resource string/service_tick_zero (aka com.example.smartio:string/service_tick_zero) not found.`가 `activity_main.xml` 줄 번호와 함께 나온다(빌드로 확인).

## 공식 참고 자료

- [앱 기본 사항(앱 구성요소) — Android Developers](https://developer.android.com/guide/components/fundamentals)
- [서비스 개요 — Android Developers](https://developer.android.com/develop/background-work/services)
- [Android의 Kotlin 코루틴 — Android Developers](https://developer.android.com/kotlin/coroutines)
- [Android의 StateFlow 및 SharedFlow — Android Developers](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [수명 주기 인식 코루틴(repeatOnLifecycle) — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [알림 개요 — Android Developers](https://developer.android.com/develop/ui/views/notifications)
