# 9주차 예제 — Service·Fragment 시연과 1차 과제 제공 코드

9주차 예제는 `day1`·`day2`가 아니라 **세 폴더**다. 1일차 설명 시간의 시연 두 개와 1차 과제 (b)의 제공 코드이며, 2일차는 발표라 예제가 없다.
세 폴더 모두 `build_examples.sh`로 따로 빌드된다. 만드는 순서는 [따라하기](../walkthrough.md)에 있다.

| 폴더 | 무엇 | package | 시작점 | 채점 |
|---|---|---|---|---|
| [service_demo](service_demo) | 1일차 8–15분 `LogService` 시연 | `com.example.smartio` | 7주차 `examples/day2` | 하지 않는다 |
| [fragment_demo](fragment_demo) | 1일차 15–20분 Fragment 교체 시연 | `com.example.fragmentdemo` | 새 프로젝트 `FragmentDemo` | 하지 않는다 |
| [fake_request](fake_request) | 1차 과제 (b) 제공 함수 `fakeRequest()`와 사용 예 | `com.example.project1` | 새 프로젝트 `Project1` | (b)는 과제에서 |

세 폴더 모두 다음 주 시작점이 아니다. 10주차는 7주차 완성본을 이어서 쓴다. `service_demo`를 따라 해 SmartIO에 [서비스 시작]·[서비스 중지]가 남아 있어도, 지워도 된다.

## 파일과 넣을 위치

### service_demo — 7주차 SmartIO에 더한 것

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [LogService.kt](service_demo/LogService.kt) | `app › kotlin+java › com.example.smartio › LogService.kt` | 새 파일(New › Kotlin Class/File › Class) |
| [MainActivity.kt](service_demo/MainActivity.kt) | `app › kotlin+java › com.example.smartio › MainActivity.kt` | `onCreate()` 끝에 `// 10.` [서비스 시작], `// 11.` [서비스 중지] |
| [activity_main.xml](service_demo/activity_main.xml) | `app › res › layout › activity_main.xml` | 맨 아래에 버튼 두 개짜리 가로 줄 |
| [strings.xml](service_demo/strings.xml) | `app › res › values › strings.xml` | `service_start`, `service_stop` |
| [AndroidManifest.xml](service_demo/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | `</application>` 위에 `<service>` 세 줄과 주석 |
| `ConnState.kt`, `ConnViewModel.kt`, `ControlActivity.kt`, `activity_control.xml`, `res/values/themes.xml` | 같은 이름의 파일 | 7주차 `examples/day2` 그대로, 바꾸지 않는다 |

### fragment_demo — 새 프로젝트

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 내용 |
|---|---|---|
| [build.gradle.kts](fragment_demo/build.gradle.kts) | `Gradle Scripts › build.gradle.kts (Module :app)` | 4주차 `examples/day1`과 같고 `namespace`·`applicationId`만 `com.example.fragmentdemo` |
| [AndroidManifest.xml](fragment_demo/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | Activity 하나. Fragment는 적지 않는다 |
| [strings.xml](fragment_demo/strings.xml) | `app › res › values › strings.xml` | 버튼 글자 두 개, 조각 글자 두 개 |
| [activity_main.xml](fragment_demo/activity_main.xml) | `app › res › layout › activity_main.xml` | 버튼 가로 줄 + `FragmentContainerView` |
| [fragment_first.xml](fragment_demo/fragment_first.xml), [fragment_second.xml](fragment_demo/fragment_second.xml) | `app › res › layout` 아래 새 파일 | 가운데 `TextView` 하나 |
| [FirstFragment.kt](fragment_demo/FirstFragment.kt), [SecondFragment.kt](fragment_demo/SecondFragment.kt) | `app › kotlin+java › com.example.fragmentdemo` 아래 새 파일 | `onCreateView`에서 layout을 돌려준다 |
| [MainActivity.kt](fragment_demo/MainActivity.kt) | `app › kotlin+java › com.example.fragmentdemo › MainActivity.kt` | ViewBinding 틀 + 조각 끼우기·바꾸기 |
| [res/values/themes.xml](fragment_demo/res/values/themes.xml) | `app › res › values › themes.xml` | 프로젝트를 만들 때 생긴 그대로(`Theme.FragmentDemo`) |

### fake_request — 1차 과제 (b)

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 내용 |
|---|---|---|
| [FakeRequest.kt](fake_request/FakeRequest.kt) | `app › kotlin+java › <내 package> › FakeRequest.kt` | **제공 코드.** 그대로 복사하고 첫 줄 `package`만 내 것으로 |
| [RequestViewModel.kt](fake_request/RequestViewModel.kt) | `app › kotlin+java › com.example.project1 › RequestViewModel.kt` | 부르는 쪽 본보기(7주차 `ConnViewModel`과 같은 모양) |
| [MainActivity.kt](fake_request/MainActivity.kt) | `app › kotlin+java › com.example.project1 › MainActivity.kt` | 틀 두 개로 결과 문구와 [다시 시도]를 받는다 |
| [activity_main.xml](fake_request/activity_main.xml) | `app › res › layout › activity_main.xml` | 제목, `resultText`, [요청], [다시 시도] |
| [strings.xml](fake_request/strings.xml) | `app › res › values › strings.xml` | `state_idle`, `request`, `retry` |
| [build.gradle.kts](fake_request/build.gradle.kts), [AndroidManifest.xml](fake_request/AndroidManifest.xml), [res/values/themes.xml](fake_request/res/values/themes.xml) | 같은 이름의 파일 | 4주차와 같은 설정(`com.example.project1`, `Theme.Project1`) |

`MainActivity.kt`·`FakeRequest.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
ViewModel·코루틴 의존성은 4주차 `build.gradle.kts`와 같은 줄로 이미 들어 있다. Fragment는 `appcompat`에 함께 들어 있어 따로 넣지 않는다.

## 1. 네 가지 컴포넌트는 Manifest에 적는다

`service_demo/AndroidManifest.xml`에는 4주차의 `<activity>` 줄 옆에 오늘 `<service>` 줄이 있다.

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
| Activity | 있음 | `<activity>` | 2~7주 |
| Service | 없음 | `<service>` | 9주 시연 |
| BroadcastReceiver | 없음 | `<receiver>` 또는 코드로 등록 | 10주 |
| ContentProvider | 없음 | `<provider>` | 11주 비교·시연 |

- `exported="false"`는 이 앱 안에서만 쓴다는 뜻이다.
- `<service>` 줄이 없어도 빌드는 된다. 그러면 [서비스 시작]을 눌러도 Service가 시작되지 않는다(예상 증상: Logcat `tag:Service`에 아무것도 찍히지 않는다).

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
- Service가 돌고 있을 때 뒤로 가기로 앱을 닫으면, Android 8 이상에서는 잠시 뒤 시스템이 Service를 멈춰 `onDestroy`가 찍힐 수 있다(예상). 시연은 앱을 연 채로 한다.

## 4. Service도 메인 스레드에서 돈다

```kotlin
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
```

- Logcat의 `thread=main`은 5주차에 본 메인 스레드다. Service는 따로 스레드를 만들지 않는다.
- 그래서 `onStartCommand` 안에서 `Thread.sleep(10000)`처럼 오래 걸리는 일을 하면 화면이 멈춘다(예상 증상: 10초 동안 버튼이 반응하지 않고, 계속 누르면 "앱이 응답하지 않습니다" 창이 뜰 수 있다). 5주차 1일차 시연과 같다.
- 오래 걸리는 일은 Service 안에서도 5주차 `Thread { }.start()`나 6주차 코루틴으로 보낸다. 이번 주에는 시연만 한다.

## 5. Fragment — Activity 안의 화면 조각

```kotlin
class FirstFragment : Fragment() {
```

```kotlin
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "FirstFragment onCreateView")
        return inflater.inflate(R.layout.fragment_first, container, false)
    }
```

- Fragment는 자기 layout(`fragment_first.xml`)을 가진다. Activity의 `setContentView` 자리에서 `onCreateView`가 조각의 화면을 돌려준다.
- `Fragment` import는 `androidx.fragment.app.Fragment`다. 빠지면 `Unresolved reference 'Fragment'.`과 `'onCreateView' overrides nothing.`이 난다.
- Fragment는 Manifest에 적지 않는다.

## 6. FragmentContainerView와 바꾸기 세 줄

```xml
    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/fragmentContainer"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="16dp" />
```

```kotlin
        if (savedInstanceState == null) {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, FirstFragment())
            transaction.commit()
        }
```

```kotlin
        binding.secondButton.setOnClickListener {
            val transaction = supportFragmentManager.beginTransaction()
            transaction.replace(R.id.fragmentContainer, SecondFragment())
            transaction.commit()
        }
```

| 조작 | 화면 | Logcat `package:mine tag:Fragment` |
|---|---|---|
| 앱 시작 | 위에 [첫 번째 조각] [두 번째 조각], 가운데 `여기는 FirstFragment` | `FirstFragment onCreateView` |
| [두 번째 조각] | 버튼 줄은 그대로, 아래 글자만 `여기는 SecondFragment` | `SecondFragment onCreateView` |
| [첫 번째 조각] | `여기는 FirstFragment` | `FirstFragment onCreateView` |
| 같은 버튼을 두 번 | 글자는 같다 | 누를 때마다 한 줄씩 찍힌다(새 조각을 만들어 끼운다) |
| SecondFragment를 보다가 회전(예상) | 가로 화면에서도 `여기는 SecondFragment` | `SecondFragment onCreateView` 한 줄 |
| 뒤로 가기(예상) | 앱이 닫힌다 | 조각 단위로 뒤로 가지 않는다 |

- `layout_height="0dp"` + `layout_weight="1"`은 2주차 확장에서 본 "남은 공간 나눠 갖기"다.
- `if (savedInstanceState == null)`: 처음 켤 때만 조각을 끼운다. 회전 뒤에는 보던 조각을 시스템이 되살린다(3주차 복원과 같은 원리).
- `transaction.commit()`을 빼도 빌드는 된다. 그러면 버튼을 눌러도 화면이 바뀌지 않는다(예상).
- XML id 철자가 다르면 `Unresolved reference 'fragmentContainer'.` 오류가 Kotlin 파일에 난다.

## 7. fakeRequest() — 1차 과제 (b) 제공 함수

```kotlin
suspend fun fakeRequest(): String {
    delay(1000)
    if (Random.nextBoolean()) {
        throw Exception("요청 실패")
    }
    return "성공"
}
```

- 클래스 밖에 있는 함수라 어느 파일에서나 `fakeRequest()`로 부른다.
- `delay`를 쓰는 `suspend fun`이라 코루틴 안에서만 부를 수 있다. 밖에서 부르면 `Suspend function 'suspend fun fakeRequest(): String' should be called only from a coroutine or another suspend function.`
- 6주차 `connectFake()`와 달리 `withContext(Dispatchers.IO)`가 없다. `delay`는 스레드를 막지 않으므로 옮길 필요가 없다(6주차 2일차).

## 8. ViewModel에서 부르고 화면은 collect로 받기

```kotlin
    fun request() {
        // 이미 요청 중이면 새로 시작하지 않는다(7주차 1일차).
        if (requestJob?.isActive == true) {
            return
        }
        requestJob = viewModelScope.launch {
            _failed.value = false
            _result.value = "요청 중…"
            try {
                val text = fakeRequest()
                _result.value = "결과: $text"
            } catch (e: Exception) {
                // 4. 실패하면 실패 문구를 넣고 [다시 시도]가 보이게 한다(6주차 2일차).
                _result.value = "요청 실패"
                _failed.value = true
            }
        }
    }
```

```kotlin
                viewModel.failed.collect { failed ->
                    if (failed) {
                        binding.retryButton.visibility = View.VISIBLE
                    } else {
                        binding.retryButton.visibility = View.GONE
                    }
                }
```

| 조작 | `resultText` | [다시 시도] |
|---|---|---|
| 앱 시작 | `대기 중` | 숨김 |
| [요청] 직후 | `요청 중…` | 숨김 |
| 1초 뒤 성공 | `결과: 성공` | 숨김 |
| 1초 뒤 실패 | `요청 실패` | **보임** |
| [다시 시도] | `요청 중…` → 1초 뒤 성공 또는 실패 | 숨김 → 결과대로 |
| `요청 중…`일 때 [요청] 한 번 더 | 바뀌지 않는다(새 요청 없음) | 숨김 |
| `요청 중…`에서 회전(예상) | 가로 화면에서도 `요청 중…`, 1초 안에 결과가 새 화면에 나온다 | 결과대로 |
| `요청 실패`에서 회전(예상) | 가로 화면에서도 `요청 실패` | **보임** 유지 |

- 이 예제 하나로 채점 축 중 화면에 드러나는 세 개(정상 흐름 / 실패·재시도 / 회전 유지)를 모두 볼 수 있다. 네 번째 코드 설명은 발표 때 개인 구술이다.
- `try/catch` 없이 부르면 빌드는 되지만 실패할 때 앱이 꺼진다(예상 증상: Logcat `FATAL EXCEPTION: main`, `java.lang.Exception: 요청 실패` 비슷한 줄). [다시 시도]는 절대 보이지 않는다.
- 6주차처럼 Activity의 `lifecycleScope.launch { }`에서 부르면 회전할 때 `대기 중`으로 돌아간다(예상). 과제의 회전 유지 축을 받으려면 이 예제처럼 ViewModel에서 부른다.
- 50% 확률이라 성공과 실패를 둘 다 보려면 몇 번 눌러야 한다. 이 앱은 Logcat에 로그를 남기지 않는다.

## 공식 참고 자료

- [앱 기본 사항(앱 구성요소) — Android Developers](https://developer.android.com/guide/components/fundamentals)
- [서비스 개요 — Android Developers](https://developer.android.com/develop/background-work/services)
- [프래그먼트 — Android Developers](https://developer.android.com/guide/fragments)
- [프래그먼트 트랜잭션 — Android Developers](https://developer.android.com/guide/fragments/transactions)
- [ViewModel 개요 — Android Developers](https://developer.android.com/topic/libraries/architecture/viewmodel)
