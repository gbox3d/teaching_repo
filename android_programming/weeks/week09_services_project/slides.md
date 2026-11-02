---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 9주차
footer: 화면 없이 일하는 Service
---

# 화면 없이 일하는 Service

2~7주차에 만든 화면은 모두 **Activity**였습니다.
1일차에는 화면이 없는 컴포넌트 **Service**를 직접 넣어 시작·중지해 보고,
2일차에는 그 Service가 1초마다 센 숫자를 화면에서 **받아** 보여 줍니다.

```text
1일차: 네 컴포넌트 비교 · Service 세 종류 · LogService 시작·중지
2일차: object와 MutableStateFlow로 값 두기 · Service에서 세기 · 화면에서 받기
```

---

# 1일차 — 앱 컴포넌트 비교와 Service

`30분 설명·시연 → 60분 실습`

1. Activity·Service·BroadcastReceiver·ContentProvider 한 표로 비교하기
2. Service 세 종류와 `LogService` 코드 읽기
3. `startService`·`stopService`와 Manifest `<service>` 등록
4. Logcat으로 "Service도 메인 스레드에서 돈다" 확인하기

---

## 1일차 · 0–8분 ① — 앱을 이루는 네 가지 컴포넌트

| 컴포넌트 | 무엇 | 언제 쓰나 | 화면 | 예 |
|---|---|---|---|---|
| Activity | 사용자가 보는 화면 하나 | 누르고 입력받을 때 | 있음 | SmartIO 연결 화면 |
| Service | 화면 없이 일을 맡는 것 | 화면을 떠나도 이어져야 할 때 | 없음 | 음악 재생 |
| BroadcastReceiver | 시스템이 보내는 소식을 받는 것 | 배터리·충전 상태가 바뀔 때 | 없음 | 배터리 잔량 표시 |
| ContentProvider | 다른 앱에 데이터를 내주는 창구 | 연락처·사진을 읽을 때 | 없음 | 연락처 앱 |

- 넷 중 화면이 있는 것은 Activity 하나입니다.
- 넷 다 Android가 직접 부를 수 있는 **앱의 입구**입니다.
- 그래서 `AndroidManifest.xml`에 적습니다(BroadcastReceiver는 코드로 등록하기도 합니다).

---

## 1일차 · 0–8분 ② — 이 과목에서 언제 만나나

| 컴포넌트 | 이 과목 | 우리 코드 |
|---|---|---|
| Activity | 2~7주 매주 | `MainActivity`, `ControlActivity` |
| Service | **오늘 1일차** | `LogService` |
| BroadcastReceiver | 10주 | 배터리 변화 받기 |
| ContentProvider | 11주 비교·시연 | 연락처 이름 읽기 |

- 4주차에 Manifest에서 `<activity android:name=".ControlActivity" …>` 줄을 봤습니다.
- 오늘은 그 옆에 `<service android:name=".LogService" …>` 줄이 생깁니다.
- 오늘 넣는 Service는 SmartIO 본줄기가 아닙니다. 10주차는 7주차 완성본에서 다시 시작합니다.

---

## 1일차 · 8–14분 ① — Service 세 종류

| 종류 | 누가 시작하나 | 언제 끝나나 | 사용자에게 보이나 |
|---|---|---|---|
| started | 화면이 `startService(intent)` | `stopService`를 부르거나 스스로 멈출 때 | 보장되지 않음 |
| bound | 화면이 `bindService`로 묶음 | 묶은 화면이 모두 풀릴 때 | 묶은 화면과 함께 |
| foreground | started + 알림 띄우기 | 멈출 때까지 | **알림이 꼭 보인다** |

- 오늘 만드는 것은 **started** 하나입니다. bound·foreground는 이름만 알아 둡니다.
- 음악 앱이 재생 중에 알림을 띄워 두는 것이 foreground Service입니다.
- 사용자가 알고 있는 일이라 시스템이 foreground Service를 쉽게 멈추지 않습니다.

---

## 1일차 · 8–14분 ② — LogService: 화면 없는 컴포넌트

```kotlin
class LogService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        return START_NOT_STICKY
    }
    override fun onDestroy() { … Log.d("Service", "onDestroy") }   // 줄여 적음
    override fun onBind(intent: Intent?): IBinder? { … return null }
}
```

- 7주차 `ConnViewModel : ViewModel()`처럼 `Service()`를 물려받습니다. layout 파일이 없습니다.
- `onStartCommand`: `startService`를 부를 **때마다** 불립니다.
- `onDestroy`: 멈출 때 한 번. `onBind`: 오늘은 `null`을 돌려주는 **틀**입니다.

---

## 1일차 · 14–20분 ① — 시작·중지와 Manifest 등록

```kotlin
binding.serviceStartButton.setOnClickListener {
    val intent = Intent(this, LogService::class.java)
    startService(intent)
}
```

```xml
<service
    android:name=".LogService"
    android:exported="false" />
```

- 4주차 `Intent(this, ControlActivity::class.java)` → `startActivity(intent)`와 같은 모양입니다.
- [서비스 중지]는 같은 두 줄에서 `startService` 자리에 `stopService(intent)`를 씁니다.
- `<service>` 줄이 없어도 **빌드는 됩니다**. 그래도 눌러도 Service가 시작되지 않습니다.

---

## 1일차 · 14–20분 ② — 시연: Service도 메인 스레드에서 돈다

Logcat 필터 `package:mine tag:Service`

| 누른 버튼 | 화면 | Logcat |
|---|---|---|
| [서비스 시작] | 그대로 | `onStartCommand thread=main` |
| [서비스 시작] 한 번 더 | 그대로 | `onStartCommand thread=main` 한 줄 더 |
| [서비스 중지] | 그대로 | `onDestroy` |

- `thread=main`: 5주차에 본 **메인 스레드**와 같은 스레드입니다.
- Service는 "뒤에서 도는 스레드"가 아닙니다. `onStartCommand`에서 `Thread.sleep`하면 화면이 멈춥니다.
- 오래 걸리는 일은 Service 안에서도 5·6주차처럼 스레드·코루틴으로 보냅니다.

---

## 1일차 · 20–26분 ① — 네 컴포넌트를 한 표로 다시

| 컴포넌트 | Manifest 태그 | 누가 시작하나 | 이 과목에서 만드나 |
|---|---|---|---|
| Activity | `<activity>` | 사용자가 앱을 켜거나 `startActivity` | 2주차부터 매주 |
| Service | `<service>` | 화면이 `startService`·`bindService` | 오늘 1일차 |
| BroadcastReceiver | `<receiver>` 또는 코드 등록 | 시스템이 소식을 보낼 때 | 10주차 1일차 |
| ContentProvider | `<provider>` | 다른 앱이 데이터를 물을 때 | 11주차는 쓰기만 |

- Manifest에 적는 자리가 다르고, **누가 불러 주는지**가 다릅니다.
- Activity만 `setContentView`로 화면을 가집니다. 나머지 셋은 화면이 없습니다.
- Service는 `onCreate`·`onDestroy`로, BroadcastReceiver는 `onReceive` 한 번으로, ContentProvider는 `onCreate`로 Android가 불러 줍니다(3주차 생명주기와 같은 생각).

---

## 1일차 · 20–26분 ② — Service를 쓸 자리와 쓰지 않을 자리

| 하려는 일 | 이 과목에서 쓰는 것 |
|---|---|
| 화면을 보는 동안의 기다림(카운트다운, 가짜 연결) | 6주차 코루틴 + 7주차 ViewModel |
| 회전해도 살아 있어야 하는 상태 | 7주차 ViewModel·StateFlow |
| 화면을 떠나도 이어져야 하는 일(음악 재생, 긴 업로드) | Service |
| 사용자에게 계속 보여야 하는 긴 작업 | foreground Service(알림 필수) |

- 이 주에 넣는 Service는 연습입니다. 10주차부터 이어 갈 SmartIO 본줄기는 7주차 완성본에서 다시 시작합니다.
- "화면 없이 도는 일은 모두 Service"가 아닙니다. 기준은 **화면을 떠나도 이어져야 하는가**입니다.
- Service를 쓰더라도 오래 걸리는 일은 그 안에서 또 스레드·코루틴으로 보냅니다. 내일 그렇게 해 봅니다.

---

## 1일차 · 26–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--smartio에-logservice-넣기-60분) · [따라하기](walkthrough.md#1일차)

1. `LogService.kt`를 새로 만들고 함수 세 개(`onStartCommand`·`onDestroy`·`onBind`)를 넣습니다.
2. Manifest `<application>` 안에 `<service>` 세 줄을 적습니다. 이것을 빠뜨리면 로그가 비어 있습니다.
3. [서비스 시작]·[서비스 중지] 버튼을 만들고 `startService`·`stopService`를 부릅니다.
4. Logcat 필터를 `package:mine tag:Service`로 두고 관찰표를 채운 뒤 **캡처 1장**을 남깁니다.

```text
onStartCommand thread=main   ← 두 번 누르면 두 줄
onDestroy                    ← [서비스 중지]
```

**설명 합계: 8+6+6+6+4 = 30분**

---

# 2일차 — Service가 센 숫자를 화면에 보여 주기

`30분 설명·시연 → 60분 실습`

1. Service와 화면이 서로 다른 객체라서 값을 둘 자리가 필요하다는 것 보기
2. `object ServiceState`에 7주차 `MutableStateFlow` 두기
3. Service에서 코루틴으로 1초마다 값 올리기
4. 7주차 `repeatOnLifecycle` 틀로 화면에서 받아 쓰기

---

## 2일차 · 0–6분 ① — 1일차 Service는 Logcat에만 남았다

| 1일차에 누른 것 | 화면 | Logcat |
|---|---|---|
| [서비스 시작] | 그대로 | `onStartCommand thread=main` |
| [서비스 중지] | 그대로 | `onDestroy` |

- Service가 돌고 있는지 **화면만 보고는** 알 수 없었습니다. Logcat을 열어야 보였습니다.
- 오늘은 Service가 1초마다 숫자를 세고, 화면이 그 숫자를 받아 `센 횟수:` 뒤에 씁니다.
- 1일차에 말한 대로 Service 안의 오래 걸리는 일은 코루틴으로 보냅니다. 오늘 그 코루틴을 씁니다.
- 1일차 코드는 지우지 않습니다. 새 파일 하나를 만들고 네 파일에 더합니다.

---

## 2일차 · 0–6분 ② — Service와 화면은 서로 다른 객체다

```text
LogService  ──▶  ServiceState.tick  ──▶  MainActivity
1초마다 1 올림    object: 앱에 하나      collect로 받아 화면에 쓴다
```

| 이렇게 해 보면 | 어떻게 되나 |
|---|---|
| Service가 `MainActivity`의 변수에 값 쓰기 | Service는 그 화면 객체를 알지 못한다 |
| `startService(intent)`로 값 돌려받기 | Intent는 **보내는** 쪽이고 돌려받는 길이 없다 |
| 둘이 함께 보는 자리를 하나 두기 | 오늘 쓰는 방법 |

- Service와 Activity는 Android가 **각각 만들어 주는 서로 다른 객체**입니다.
- 그래서 값을 건네려면 둘 다 아는 자리가 필요합니다. 그 자리를 다음 장에서 만듭니다.

---

## 2일차 · 6–14분 ① — 값을 둘 자리: object와 MutableStateFlow

```kotlin
import kotlinx.coroutines.flow.MutableStateFlow

object ServiceState {
    val tick = MutableStateFlow(0)
}
```

- `object`는 앱에 하나만 생기는 묶음입니다. 7주차 2일차의 `ConnState`도 object였습니다.
- `MutableStateFlow(0)`은 7주차에 본 **지금 값 하나를 들고 있는 상자**이고, 처음 값은 0입니다.
- 7주차에는 바꾸는 쪽(`_state`)을 숨기고 읽는 쪽(`state`)만 화면에 내보냈습니다.
- 오늘은 값을 올리는 쪽이 이 파일 **바깥**의 `LogService`라서 한 줄만 두고 숨기지 않습니다.
- 7주차처럼 `StateFlow`로 감싸면 `LogService.kt`에 `'val' cannot be reassigned.`가 납니다.

---

## 2일차 · 6–14분 ② — Service가 코루틴으로 1초마다 센다

```kotlin
    private val scope = CoroutineScope(Dispatchers.Default)
    private var tickJob: Job? = null
```

```kotlin
        tickJob = scope.launch {
            while (isActive) {
                delay(1000)
                ServiceState.tick.value++
            }
        }
```

- Service에는 7주차 `viewModelScope` 같은 것이 없어 코루틴 자리를 **직접 만듭니다**. `Dispatchers.Default`는 메인 스레드가 아닌 곳입니다.
- `delay(1000)`은 6주차에 쓴 그 함수입니다. 1초 쉬고 값을 1 올리는 일을 `while (isActive)` 동안 되풀이합니다.
- [서비스 시작]을 여러 번 눌러도 코루틴이 하나만 돌도록, 이미 돌고 있으면 `if (tickJob?.isActive == true)`에서 바로 돌아갑니다.

---

## 2일차 · 14–22분 ① — 화면에서 받기: repeatOnLifecycle

```kotlin
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                ServiceState.tick.collect { tick ->
                    binding.serviceTickText.text = "센 횟수: $tick"
                }
            }
        }
```

- 7주차 2일차의 틀 그대로이고, **받는 대상만** `viewModel.state`에서 `ServiceState.tick`으로 바뀌었습니다.
- `onCreate()` 안, 11번 블록 뒤에 둡니다. `MainActivity.kt`에 import는 하나도 더하지 않습니다.
- 화면이 보일 때(`STARTED`)만 받습니다. 제어 화면에 가 있는 동안에는 받지 않습니다.
- 숫자를 쓸 자리는 `activity_main.xml`의 `serviceTickText`이고, 처음 글자는 `strings.xml`에 둡니다.

---

## 2일차 · 14–22분 ② — 시연: 화면을 옮겼다 와도 이어진다

| 조작 | 화면에서 볼 것 |
|---|---|
| [서비스 시작] | `센 횟수:` 뒤의 숫자가 1초 간격으로 바뀌어 보입니다 |
| [서비스 시작] 한 번 더 | 숫자가 그대로 이어져 보입니다. 코루틴을 새로 시작하지 않습니다 |
| 이름을 넣고 [연결] → 제어 화면 → [뒤로] | 돌아온 화면의 숫자가 떠날 때보다 커져 보입니다 |
| 화면 회전 | 마지막 값이 다시 보입니다(7주차 복원 틀) |
| [서비스 중지] | `onDestroy`에서 0으로 되돌리므로 `센 횟수: 0`이 보입니다 |

- 제어 화면에 있는 동안 화면은 받기를 멈추지만 Service는 계속 셉니다. 돌아오면 마지막 값을 바로 받습니다.
- 화면을 떠나도 일이 이어지는 것이 Service를 쓰는 이유입니다. 1일차에 세운 기준이 여기서 눈에 보입니다.
- `onDestroy`의 `tickJob?.cancel()`을 빼면 빌드는 됩니다. 그 뒤에 무슨 일이 생기는지는 실습에서 직접 보세요.

---

## 2일차 · 22–27분 — Notification: 화면 밖에서 알리기

```text
상태 표시줄을 내리면
┌──────────────────────────────────┐
│ Smart I/O Controller             │
│ 연결이 끊겼습니다                │
└──────────────────────────────────┘
```

- 알림(Notification) = 앱 화면을 보고 있지 않은 사용자에게 알리는 것입니다.
- 1일차 Service 표의 셋째 줄, foreground Service는 **알림을 꼭 띄워야** 합니다.
- Android 13부터는 알림을 띄우려면 사용자에게 **권한**을 받아야 합니다.
- 권한이 없으면 `notify`를 불러도 알림이 뜨지 않습니다. `areNotificationsEnabled()`와 Logcat으로 확인합니다.
- 런타임 권한은 10주차 2일차 내용이라, 오늘은 **시연으로만 보고 실습에는 넣지 않습니다**.

---

## 2일차 · 27–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--service가-센-숫자를-화면에-보여-주기-60분) · [따라하기](walkthrough.md#2일차)

1. `ServiceState.kt`를 **Object**로 새로 만들고 `val tick = MutableStateFlow(0)` 한 줄을 넣습니다.
2. `LogService.kt`에 `scope`·`tickJob`을 두고 1초마다 `ServiceState.tick`을 올립니다.
3. `onDestroy`에서 세던 코루틴을 취소하고 값을 0으로 되돌립니다.
4. `activity_main.xml`에 `serviceTickText` 자리를, `strings.xml`에 처음 글자를 넣습니다.
5. `MainActivity.kt`에 7주차 collect 틀을 하나 더 쓰고 **캡처 2장**을 남깁니다.

```text
센 횟수: 0  →  [서비스 시작] 뒤에는 0이 아닌 숫자
            →  제어 화면에 갔다 돌아오면 더 큰 숫자
```

**설명 합계: 6+8+8+5+3 = 30분**

---

## 제출하기

1일차 캡처 한 장, 2일차 캡처 두 장을 남깁니다.

1. **1일차 캡처 1장**: Logcat `tag:Service`에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 보이는 화면
2. **2일차 캡처 2장**: ① `센 횟수:` 뒤의 숫자가 0이 아닌 화면 ② 제어 화면에 갔다 돌아와 숫자가 이어진 화면

파일 이름·제출 위치·마감은 수업 공지를 따릅니다. 캡처에 개인정보가 보이지 않는지 확인합니다.

---

## 다음 주 미리 보기

1일차 표의 셋째 줄, **BroadcastReceiver**를 직접 만들고 **런타임 권한**을 받습니다.

- 에뮬레이터의 배터리를 바꾸면 SmartIO 화면의 `배터리 80% · 충전 중`이 따라 바뀌게 합니다.
- 오늘 시연으로 본 알림 권한처럼, 쓰기 직전에 사용자에게 묻는 권한을 10주차 2일차에 직접 만듭니다.
- 12주차 **BLE**(Bluetooth Low Energy, 저전력 블루투스)에서는 보드의 상태를 오늘 쓴 collect 틀로 받습니다.
- 10주차 시작점은 7주차 완성본입니다. 오늘 더한 Service는 9주차에서 끝냅니다.
