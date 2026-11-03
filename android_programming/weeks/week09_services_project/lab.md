# 9주차 실습 — Service 시작·중지와 센 숫자 화면에 보여 주기

1일차 60분에는 7주차까지 만든 `SmartIO`에 화면 없는 컴포넌트 `LogService`를 넣고, 버튼으로 시작·중지하며 Logcat에서 스레드 이름을 확인한다.
2일차 60분에는 그 `LogService`가 코루틴으로 1초마다 센 숫자를 같은 `SmartIO`의 연결 화면에 보여 준다.
단계별 코드와 넣을 위치는 [따라하기](walkthrough.md)에 있고, 완성 파일은 [예제 설명](examples/README.md)에 있다.

이번 주에 만드는 것은 10주차 시작점이 아니다. 10주차는 7주차 완성본에서 다시 시작하므로, 이번 주에 더한 서비스 버튼과 숫자 줄은 남겨 두어도 되고 지워도 된다.

## 1일차 — SmartIO에 LogService 넣기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 7주차까지 만든 `SmartIO`를 열고 실행해 [검색]이 도는지 본다. 없으면 7주차 완성본(`week07/examples/day2`)을 받아 시작한다 |
| 5–15분 | `LogService.kt`를 만든다(1번) |
| 15–22분 | Manifest에 `<service>`를 적는다(2번) |
| 22–35분 | 버튼 두 개를 만든다(3번) |
| 35–45분 | 버튼에서 `startService`·`stopService`를 부른다(4번) |
| 45–55분 | Logcat 관찰표를 채운다(5번) |
| 55–60분 | 캡처 1장을 남기고 오늘 확인할 것을 점검한다(6번) |

### 1. LogService.kt 만들기

`SmartIO`의 package 폴더에 `LogService` 클래스를 새로 만든다(New › Kotlin Class/File › Class).

- 선언은 `class LogService : Service()`다. 7주차 `class ConnViewModel : ViewModel()`과 같은 모양이다.
- 함수 세 개를 넣는다. `onStartCommand`에서 `Thread.currentThread().name`을 `Log.d("Service", …)`로 찍고 `START_NOT_STICKY`를 돌려준다. `onDestroy`에서 로그 한 줄을 찍는다. `onBind`는 `null`을 돌려주는 틀이다.
- `onBind`의 인자와 반환형에 `?`를 붙인다. 붙이지 않으면 `return null` 줄에 오류가 난다.
- 전체 코드는 [따라하기 2단계](walkthrough.md#2-logservicekt-만들기)에 있다. 먼저 스스로 쓰고 비교한다.

| 확인 | 결과 |
|---|---|
| 빨간 글자가 없다 | import 네 줄(`Service`·`Intent`·`IBinder`·`Log`)이 들어 있다 |
| 실행한다 | 화면은 7주차와 같다. 아직 Service를 부르는 버튼이 없다 |

### 2. Manifest에 service 적기

`AndroidManifest.xml`의 `<application>` 안, `</application>` 위에 `<service>`를 적는다.

- `android:name=".LogService"`의 앞 점은 "이 앱 package 안의"라는 뜻이다. 4주차 `.ControlActivity`와 같다.
- `android:exported="false"`는 이 앱 안에서만 쓴다는 뜻이다.
- 이 세 줄을 빠뜨려도 **빌드는 된다**. 나중에 버튼을 눌렀을 때 Logcat이 비어 있으면 먼저 이 줄을 본다.
- 넣을 자리는 [따라하기 3단계](walkthrough.md#3-manifest에-service-적기)에 있다.

### 3. 버튼 두 개 만들기

`strings.xml`에 글자 두 개(`service_start`·`service_stop`)를 넣고, `activity_main.xml` 맨 아래에 버튼 두 개짜리 가로 줄을 넣는다.

- `id`는 `serviceStartButton`·`serviceStopButton`으로 한다. 코드에서 `binding.serviceStartButton`으로 부른다.
- 가로 줄 만들기는 7주차 [검색]·[중지]·[해제] 줄과 같은 모양이다. 그 줄을 복사해 고치면 빠르다.
- 실행해서 화면 맨 아래에 [서비스 시작] [서비스 중지]가 보이면 된다. 아직 눌러도 아무 일이 없다.
- 전체 XML은 [따라하기 4단계](walkthrough.md#4-버튼-두-개-추가하기)에 있다.

이 화면은 가로로 돌리면 맨 아래 줄이 잘릴 수 있다. 오늘 확인은 세로로 한다.

### 4. startService·stopService 연결하기

`MainActivity.kt`의 `onCreate()` 끝에 리스너 두 개를 넣는다.

- 4주차 [연결] 버튼과 같은 모양이다. `Intent(this, LogService::class.java)`를 만들고 `startService(intent)`를 부른다.
- [서비스 중지]는 같은 두 줄에서 `startService` 자리에 `stopService(intent)`를 쓴다.
- `Intent(this, LogService)`처럼 `::class.java`를 빼면 빌드가 안 된다.
- 새 import는 없다. `Intent`는 4주차부터 들어 있고 `LogService`는 같은 package다.
- 넣을 자리와 전체 코드는 [따라하기 5단계](walkthrough.md#5-startservicestopservice-연결하기)에 있다.

### 5. Logcat 관찰표

Logcat 필터를 `package:mine tag:Service`로 두고 순서대로 누르며 마지막 칸을 채운다.

| 조작 | 화면 | Logcat에 찍힌 줄 |
|---|---|---|
| [서비스 시작] | | |
| [서비스 시작] 한 번 더 | | |
| [서비스 중지] | | |
| 멈춘 상태에서 [서비스 중지] 한 번 더 | | |
| [검색] 카운트다운 중에 [서비스 시작] | | |

- 세 번째 줄까지 채우면 `onStartCommand`가 누를 때마다 불리고 `onDestroy`는 멈출 때 한 번 불린다는 것이 보인다.
- 다섯째 줄에서 카운트다운이 끊기지 않는 이유를 한 문장으로 적어 둔다. 6번에서 쓴다.
- 찍힌 스레드 이름이 무엇인지 반드시 읽는다. 이 이름이 오늘의 결론이다.

### 6. 오늘 확인할 것과 캡처

- [ ] Logcat에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 순서대로 보인다.
- [ ] `thread=main`이 5주차에 본 메인 스레드와 같은 스레드라는 것을 말할 수 있다.
- [ ] "Service는 따로 스레드를 만들지 않는다"와 "오래 걸리는 일은 스레드·코루틴으로 보낸다"를 각각 한 문장으로 말할 수 있다.
- [ ] 캡처 1장: 앱 화면과 Logcat이 함께 보이거나, Logcat 창만 보이는 캡처. 서비스 시작 줄 두 개·중지 줄 하나·스레드 이름이 모두 읽혀야 한다.

캡처에 계정 이름 같은 개인정보가 보이지 않는지 확인한다.

## 2일차 — Service가 센 숫자를 화면에 보여 주기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 1일차에 고친 `SmartIO`를 열고 [서비스 시작]·[서비스 중지]가 Logcat에 찍히는지 다시 확인한다 |
| 5–16분 | `ServiceState.kt`를 만든다(1번) |
| 16–28분 | `LogService`가 코루틴으로 1초마다 세게 한다(2번) |
| 28–36분 | `onDestroy`에서 코루틴을 취소하고 숫자를 되돌린다(3번) |
| 36–45분 | 화면에 숫자 자리를 만든다(4번) |
| 45–55분 | 화면에서 숫자를 받아 쓰고 캡처 1장을 남긴다(5번) |
| 55–60분 | 제어 화면에 갔다 돌아와 보고 캡처 1장을 더 남긴다(6번) |

**2일차 단계 번호는 1일차와 별개다.** 아래에서 `1번`은 2일차 1번을 가리킨다. 1일차 단계를 가리킬 때는 `1일차 1번`처럼 적는다.
오늘은 새 프로젝트를 만들지 않는다. 1일차에 고친 `SmartIO`를 그대로 이어서 고친다. 고치는 파일은 `ServiceState.kt`(새 파일), `LogService.kt`, `strings.xml`, `activity_main.xml`, `MainActivity.kt` 다섯 개다.
단계마다 넣을 자리와 전체 코드는 [따라하기 8~13단계](walkthrough.md#2일차)에 있다. 먼저 스스로 해 보고 비교한다.

### 1. ServiceState.kt 만들기

`SmartIO`의 package 폴더에 `ServiceState`를 새로 만든다(New › Kotlin Class/File › **Object**). 1일차와 달리 Class가 아니라 Object를 고른다.

- `LogService`와 `MainActivity`는 서로 다른 객체다. Service 안에서 만든 변수는 화면에서 볼 수 없고, 화면이 만든 변수는 Service가 볼 수 없다. 둘이 같이 보는 값을 한 군데 둬야 한다.
- `object`는 앱에 하나만 생긴다. 어디서 `ServiceState.tick`을 불러도 같은 것이다. 7주차 `ConnState`를 `object`로 둔 것과 같은 자리다.
- 안에 둘 것은 7주차에 쓴 `MutableStateFlow` 한 줄이다. 시작값은 `0`으로 한다. `kotlinx.coroutines.flow.MutableStateFlow` import 한 줄이 필요하다.
- **여기서 7주차와 다른 점을 한 번 겪어 본다.** 7주차 `ConnViewModel`에서는 바꾸는 쪽(`_seconds`)을 숨기고 읽기 전용 `StateFlow`만 내보냈다.
  그 방식대로 `val tick: StateFlow<Int> = MutableStateFlow(0)`이라고 적어 두고 2번까지 진행한 뒤 빌드한다. 어떤 오류가 어느 줄에 나는지 적고 되돌린다.
  되돌린 뒤 왜 오늘은 나누지 않는지 한 문장으로 적어 둔다. 읽기 전용으로 내보낸 값에는 바깥에서 `.value`를 넣을 수 없다는 것이 오류의 이유다.
  나누고 싶으면 `ServiceState` 안에 값을 올리는 함수를 같이 두고 `LogService`가 그 함수를 부르게 바꾸면 된다. 7주차에 화면이 `viewModel.startScan()`을 부른 것과 같은 모양이다. 오늘은 새 파일을 한 줄로 두려고 나누지 않은 것이니, 못 하는 일이 아니라 고른 것이라고 적으면 된다.
  일부러 감싼 줄을 쓸 때는 `StateFlow` import도 함께 필요하다. 아래 확인 표는 감싸지 않은 보통 경우를 적은 것이다.
- 전체 코드는 [따라하기 9단계](walkthrough.md#9-servicestatekt-만들기)에 있다. 먼저 스스로 쓰고 비교한다.

| 확인 | 결과 |
|---|---|
| 빨간 글자가 없다 | import 한 줄이 들어 있고 `object` 안에 한 줄만 있다 |
| 실행한다 | 아직 아무도 `ServiceState`를 쓰지 않으므로 화면은 1일차와 같다 |

### 2. LogService가 코루틴으로 1초마다 세게 하기

1일차에 Logcat의 `thread=main`을 보고 **Service도 메인 스레드에서 돈다**는 것을 확인했다. 1초마다 세는 일을 `onStartCommand` 안에서 그냥 하면 화면이 멈춘다. 그래서 6주차 코루틴으로 보낸다.

- 클래스 안·함수 밖에 속성 두 개를 둔다. 하나는 코루틴을 돌릴 자리(`CoroutineScope(Dispatchers.Main)`), 하나는 돌고 있는 코루틴을 잡아 둘 `Job?`이다. 7주차 `ConnViewModel`의 `scanJob`과 같은 자리다.
- Service에는 ViewModel의 `viewModelScope`가 없다. 찾지 말고 직접 만든다. `Dispatchers.Main`은 1일차에 Logcat으로 본 그 메인 스레드다. `delay`는 기다리는 동안 스레드를 붙잡지 않으므로 여기서 세도 화면이 멈추지 않는다.
- `onStartCommand` 안에서 그 자리에 코루틴을 하나 띄운다. 안은 `while` 한 겹이고, 1초 쉬고(`delay(1000)`) `ServiceState.tick`의 값을 1 올린다. `while`의 조건으로 `isActive`를 쓰면 취소됐을 때 반복이 끝난다.
- [서비스 시작]을 여러 번 눌러도 코루틴은 하나만 돌아야 한다. 7주차 `startScan`의 "이미 돌고 있으면 그냥 돌아간다" 검사와 같은 모양을 `onStartCommand` 앞쪽에 둔다. `onStartCommand`는 값을 돌려주는 함수이므로 그 안에서도 1일차의 `START_NOT_STICKY`를 돌려줘야 한다.
- **import 여섯 줄이 필요하다.** 자동 import가 `isActive`를 잘 집어 주지 않으므로 [따라하기 10단계](walkthrough.md#10-logservice에-코루틴으로-세기-넣기)의 import 블록을 통째로 보고 줄 수를 맞춘다.
- 1번에서 7주차 방식으로 적어 둔 학생은 여기서 빌드해 오류 문구를 적고 되돌린다.

| 확인 | 결과 |
|---|---|
| 빌드한다 | 빨간 글자가 없다. 세고 있어도 아직 보여 주는 곳이 없어 화면에 변화가 없다 |
| Logcat `tag:Service` | 1일차와 같은 줄만 찍힌다. 세는 숫자는 Logcat에 찍지 않는다 |

### 3. onDestroy에서 취소하고 되돌리기

`onDestroy`에 두 줄을 더한다. 세던 코루틴을 취소하는 줄과 `ServiceState.tick`의 값을 `0`으로 되돌리는 줄이다.

- 두 줄을 먼저 넣어 코드를 끝까지 맞춘다. 이 두 줄이 하는 일은 5번에서 화면에 숫자가 생긴 뒤에 눈으로 확인한다.
- **확인 방법**: 5번까지 끝낸 뒤 이 두 줄을 잠깐 지우고 [서비스 중지] → [서비스 시작]을 눌러 숫자를 적는다. 그다음 두 줄을 되살려 같은 순서로 눌러 보고 차이를 적는다.
- 이 두 줄을 빠뜨려도 **빌드는 통과한다**. 오류 문구로는 드러나지 않고 화면으로만 드러난다.
- `ServiceState`는 앱에 하나뿐이다. 두 줄이 없으면 다음에 시작할 때 숫자가 어디서부터 올라갈지 먼저 생각해 적고, 그다음에 눌러 확인한다. 생각과 다르면 그것도 적는다.
- 취소하는 줄은 6주차 `Job` 취소와 같은 모양이다. 전체 코드는 [따라하기 10단계](walkthrough.md#10-logservice에-코루틴으로-세기-넣기)에 있다.

### 4. 화면에 숫자 자리 만들기

`strings.xml`에 글자 하나(`service_tick_zero`, 내용은 `센 횟수: 0`)를 넣고, `activity_main.xml`의 서비스 버튼 가로 줄 **아래**에 `TextView` 하나를 넣는다.

- `id`는 `serviceTickText`로 한다. 코드에서 `binding.serviceTickText`로 부른다.
- 7주차 `stateText`와 같은 모양이다. 그 줄을 복사해 `id`와 `android:text`만 고치면 빠르다.
- **두 파일을 함께 고친다.** 하나만 고치면 막히는 단계가 달라진다. `TextView`만 넣고 글자를 만들지 않으면 Kotlin이 아니라 자원 단계(`:app:processDebugResources`)에서 막히고, 글자만 만들고 `TextView`를 넣지 않으면 5번에서 Kotlin 단계(`:app:compileDebugKotlin`)에서 막힌다.
- 실행하면 서비스 버튼 줄 아래에 `센 횟수: 0`이 보인다. 아직 [서비스 시작]을 눌러도 이 글자는 그대로다. 여기까지가 정상이다.
- 전체 내용은 [따라하기 11단계](walkthrough.md#11-화면에-숫자-자리-만들기)에 있다.

1일차보다 화면이 한 줄 길어졌다. 가로로 돌리면 아래 줄이 잘릴 수 있으니 오늘 확인도 세로로 한다.

### 5. 화면에서 숫자 받아 쓰기와 캡처 1장

`MainActivity.kt`의 `onCreate()` 안, 1일차 `// 11.` [서비스 중지] 리스너가 끝나는 `}` **아래**, `onCreate()`를 닫는 `}` **위**에 블록 하나를 더한다.

- 7주차 2일차에 쓴 틀 그대로다. `lifecycleScope.launch` → `repeatOnLifecycle(Lifecycle.State.STARTED)` → `collect` 세 겹이고, 받아 오는 곳만 `viewModel.seconds`에서 `ServiceState.tick`으로 바뀐다.
- 같은 파일의 `// 7.`·`// 9.` 블록을 나란히 놓고 보며 세 번째 블록을 만든다. 한 겹을 빼먹기 쉬우니 괄호 수를 센다.
- `collect { }` 안에서 할 일은 한 줄이다. 받은 값을 글자로 만들어 `binding.serviceTickText.text`에 넣는다.
- **이 파일에는 import를 더하지 않는다.** `lifecycleScope`·`repeatOnLifecycle`·`Lifecycle`·`launch`는 1일차 파일에 이미 들어 있다. 빨간 글자가 보이면 import보다 괄호와 철자를 먼저 본다.
- 전체 코드는 [따라하기 12단계](walkthrough.md#12-mainactivity에서-숫자-받아-쓰기)에 있다.

실행해서 아래 순서로 누르고 화면의 숫자와 Logcat을 함께 본다. 마지막 두 칸을 직접 채운다.

| 조작 | 화면의 `센 횟수:` | Logcat `tag:Service` |
|---|---|---|
| [서비스 시작] | | |
| 그대로 몇 초 기다리기 | | |
| [서비스 시작] 한 번 더 | | |
| [서비스 중지] | | |

- 셋째 줄에 적은 것이 2번에서 넣은 "이미 돌고 있으면" 검사의 결과다. 검사를 빼면 어떻게 될지도 한 문장 적어 둔다.
- 넷째 줄에 적은 것이 3번에서 넣은 두 줄의 결과다. 두 줄을 잠깐 지워 보고 다시 넣어 두 번을 비교하면 그 줄이 무엇을 하는지 보인다.

**캡처 1장**: `센 횟수:` 뒤의 수가 `0`이 아닌 화면을 캡처한다. 서비스 버튼 줄과 숫자가 함께 보여야 한다.

### 6. 화면을 옮겼다 돌아오기와 캡처 1장

코드는 더 고치지 않는다. 눈으로만 보고 적는다.

1. [서비스 시작]을 누르고 숫자를 본다.
2. 장치 이름을 넣고 [연결]로 제어 화면에 간다. 몇 초 머문다.
3. 제어 화면의 [뒤로]나 기기 뒤로 가기로 연결 화면에 돌아온다.
4. `센 횟수:` 뒤의 수를 제어 화면에 가기 직전의 수와 비교해 적는다.

| 조작 | 화면의 `센 횟수:`에 적힌 수 | 내가 생각한 이유 |
|---|---|---|
| 제어 화면으로 가기 직전 | | |
| 돌아온 직후 | | |
| 돌아와서 몇 초 뒤 | | |
| 화면을 가로로 돌린 직후 | | |

- `Lifecycle.State.STARTED`는 화면이 보일 때만 받는다는 뜻이다. 제어 화면에 가 있는 동안 연결 화면은 값을 받지 않는다. 그동안 Service는 어떻게 되는지, 돌아왔을 때 숫자가 어디서부터 보이는지를 **직접 보고** 적는다.
- 넷째 줄은 7주차 2일차에 회전으로 확인한 것과 같은 틀이다. 그때와 무엇이 같고 무엇이 다른지 한 문장 적어 둔다.
- 여기서 적은 것이 "Service를 왜 따로 두는가"에 대한 오늘의 답이다. 제어 화면에 가 있는 동안에도 앱은 켜져 있고, Service는 Activity가 아니라 보이는 화면이 바뀌어도 함께 멈추지 않는다.

**캡처 1장**: 제어 화면에 갔다 돌아온 뒤의 연결 화면을 캡처한다. 5번의 캡처와 나란히 놓고 숫자를 비교할 수 있어야 한다.

오늘 확인할 것:

- [ ] `센 횟수:`가 `0`이 아닌 화면과 제어 화면에서 돌아온 화면, 캡처 2장이 있다.
- [ ] `ServiceState`를 `object`로 둔 이유와, 7주차처럼 읽기 전용으로 나누지 않은 이유를 각각 한 문장으로 말할 수 있다.
- [ ] 1초마다 세는 일을 `onStartCommand` 안에서 그냥 하지 않고 코루틴으로 보낸 이유를 1일차 결론과 이어 말할 수 있다.
- [ ] 위 두 표에 직접 본 것을 적었다.

캡처에 계정 이름 같은 개인정보가 보이지 않는지 확인한다.

## 막혔을 때

7주차 코드에서 나는 오류는 [7주차 막혔을 때](../week07_flow_ui_state/lab.md#막혔을-때)를 본다.
아래 표에서 (1일차)로 적은 줄의 오류 문구와 증상은 2026-09-15·16에 Android 14 에뮬레이터와 Kotlin 2.0.21로 확인한 것이다.
(2일차)로 적은 줄의 오류 문구는 2026-11-03에 2일차 완성 예제를 한 군데씩 지워 빌드해 확인한 것이다. 쓰는 도구 버전에 따라 문구가 조금 다를 수 있으니, 글자가 똑같지 않아도 밑줄 그어진 이름이 같으면 같은 문제로 본다.

| 상황 | 확인할 것 |
|---|---|
| `Null cannot be a value of a non-null type 'android.os.IBinder'.`가 `return null` 줄에 난다 | (1일차) `onBind`의 반환형을 `IBinder?`로, 인자를 `intent: Intent?`로 바꾼다. `?`가 없는 타입에는 `null`을 넣을 수 없다(3주차). New › Service › Service 메뉴로 만들면 이 모양이 생긴다 |
| `Class 'LogService' is not abstract and does not implement abstract base class member 'onBind'.` | (1일차) `Service`를 물려받으면 `onBind`가 꼭 있어야 한다. `override fun onBind(intent: Intent?): IBinder? { return null }`을 넣는다 |
| `None of the following candidates is applicable:`와 `Classifier 'class LogService : Service' does not have a companion object, so it cannot be used as an expression.` | (1일차) `Intent(this, LogService)`로 썼다. 4주차처럼 `Intent(this, LogService::class.java)`로 쓴다 |
| `Unresolved reference 'serviceStartButton'.` | (1일차) 오류는 Kotlin 파일에 나오지만 원인은 XML이다. `activity_main.xml`의 `android:id="@+id/serviceStartButton"` 철자를 코드와 맞춘다 |
| 빌드는 되는데 [서비스 시작]을 눌러도 Logcat `tag:Service`에 아무것도 찍히지 않는다 | (1일차) `AndroidManifest.xml`의 `<application>` 안에 `<service android:name=".LogService" android:exported="false" />`가 있는지 본다. 필터를 풀면 `Unable to start service … not found` 줄이 보인다 |
| `onStartCommand`에 `Thread.sleep`을 넣었더니 [서비스 시작] 뒤 화면이 멈춘다 | (1일차) 버그가 아니다. Service도 메인 스레드에서 돈다. 멈춘 동안 버튼을 누르면 응답 없음 창이 뜰 수 있다. 관찰했으면 그 줄을 지운다 |
| Service를 시작한 채 뒤로 가기로 앱을 닫았더니 잠시 뒤 Logcat에 `onDestroy`가 찍힌다 | (1일차) 버그가 아니다. Android 8 이상은 백그라운드로 간 앱의 Service를 멈춘다(확인한 에뮬레이터에서는 약 1분 뒤). 관찰은 앱을 연 채로 한다 |
| `Unresolved reference 'ServiceState'.`·`Unresolved reference 'tick'.`·`Unresolved reference 'value'.`가 `LogService.kt`와 `MainActivity.kt` 양쪽에 난다. `MainActivity.kt`에는 `Cannot infer type for this parameter. Please specify it explicitly.`도 함께 난다 | (2일차) `ServiceState.kt`를 아직 만들지 않았다. 2일차 1번을 먼저 한다. 오류 창에는 `:app:compileDebugKotlin`에서 멈췄다고 나온다 |
| `Unresolved reference 'MutableStateFlow'.`가 `ServiceState.kt`와 `LogService.kt` 양쪽에 난다 | (2일차) `ServiceState.kt`에 `import kotlinx.coroutines.flow.MutableStateFlow` 한 줄이 빠졌다. `:app:compileDebugKotlin`에서 멈춘다 |
| `'val' cannot be reassigned.`가 `LogService.kt`에서 두 줄 난다(값을 1 올리는 줄과 `0`으로 되돌리는 줄) | (2일차) `ServiceState`의 값을 7주차처럼 `val tick: StateFlow<Int> = MutableStateFlow(0)`로 감쌌다. 읽기 전용 `StateFlow`에는 값을 넣을 수 없다. 2일차 1번처럼 `MutableStateFlow` 한 줄로 되돌린다 |
| `Unresolved reference 'isActive'.`가 `while (isActive)` 줄에 난다 | (2일차) `import kotlinx.coroutines.isActive`가 빠졌다. 자동 import가 잘 집어 주지 않으니 [따라하기 10단계](walkthrough.md#10-logservice에-코루틴으로-세기-넣기)의 import 블록과 줄 수를 맞춘다 |
| `Unresolved reference 'delay'.` | (2일차) `import kotlinx.coroutines.delay`가 빠졌다 |
| `Unresolved reference 'CoroutineScope'.`·`'Dispatchers'.`·`'Job'.`과 함께 `Overload resolution ambiguity between candidates:`, `None of the following candidates is applicable:`, `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.`, `Unresolved reference 'cancel'.`까지 일곱 줄이 쏟아진다 | (2일차) 코루틴 import 네 줄(`CoroutineScope`·`Dispatchers`·`Job`·`launch`)을 통째로 빠뜨렸다. 한 줄씩 고치지 말고 따라하기 10단계의 import 블록 전체와 맞춘다 |
| `Suspend function 'suspend fun collect(collector: FlowCollector<Int>): Nothing' should be called only from a coroutine or another suspend function.` | (2일차) `collect`가 `lifecycleScope.launch` 밖에 있다. 7주차 틀처럼 `lifecycleScope.launch` → `repeatOnLifecycle` → `collect` 세 겹 안에 넣는다 |
| `Unresolved reference 'serviceTickText'.`가 `MainActivity.kt`에 난다 | (2일차) 오류는 Kotlin 파일에 나오지만 원인은 layout이다. `activity_main.xml`에 `android:id="@+id/serviceTickText"`를 넣었는지, 철자가 코드와 같은지 본다 |
| `Execution failed for task ':app:processDebugResources'.` 아래에 `Android resource linking failed`, `error: resource string/service_tick_zero (aka com.example.smartio:string/service_tick_zero) not found.`, `error: failed linking file resources.`가 난다 | (2일차) Kotlin 단계가 아니라 **자원 단계**에서 막혔다. `strings.xml`에 `service_tick_zero`가 없다. 오류 문구에 `activity_main.xml`의 줄 번호가 함께 나오니 그 줄을 본다 |
| 빌드는 되는데 [서비스 중지]를 눌러도 `센 횟수:`의 수가 `0`으로 돌아가지 않는다 | (2일차) `onDestroy`에 `tickJob?.cancel()`과 `ServiceState.tick.value = 0` 두 줄이 있는지 본다. 이 두 줄이 없어도 빌드는 통과하므로 오류 문구로는 드러나지 않는다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 3장

1. **1일차 캡처 1장**: Logcat `tag:Service`에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 보이는 화면
2. **2일차 캡처 2장**: ① `센 횟수:` 뒤의 숫자가 `0`이 아닌 화면 ② [연결]로 제어 화면에 갔다 돌아와 숫자가 이어진 화면

파일 이름·제출 위치·마감은 수업 공지를 따른다. 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는지 확인한다.

## 먼저 끝났다면

- 1일차: `onStartCommand` 안에 `Thread.sleep(5000)`을 넣고 [서비스 시작]을 누른 뒤 화면을 눌러 본다. 어떤 일이 생기는지 적고 그 줄을 지운다. 5주차 시연과 같은 이유다.
- 1일차: [서비스 시작]을 누른 뒤 뒤로 가기로 앱을 닫고 Logcat을 한동안 켜 둔다. `onDestroy`가 언제 찍히는지 적어 둔다.
- 2일차: `onDestroy`의 두 줄을 지우고 [서비스 중지]를 누른 뒤 다시 [서비스 시작]을 눌러, 숫자가 어디서부터 올라가는지 적어 둔다. 확인한 뒤 두 줄을 되돌린다.
- 2일차: `delay(1000)`의 수를 `200`으로 바꿔 보고 화면의 숫자가 어떻게 달라지는지 적는다. 확인한 뒤 `1000`으로 되돌린다.
- 2일차: [서비스 시작]을 누른 채로 화면을 여러 번 돌려 보고, 돌릴 때마다 숫자가 어떻게 보이는지 적어 둔다. 7주차 2일차에 회전으로 본 것과 비교한다.
- 2일차: 1번에서 7주차 방식(`val tick: StateFlow<Int> = …`)으로 적었을 때 난 오류 문구를 그대로 적어 두고, 왜 그 오류가 났는지 한 문장으로 쓴다.

추가 과제는 선택 사항이며 채점하지 않는다.
