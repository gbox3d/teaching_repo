# 7주차 실습 — ViewModel과 StateFlow로 회전해도 남는 연결 화면

이번 주에는 6주차 `SmartIO`의 카운트다운과 가짜 연결을 ViewModel로 옮기고, 2일차에는 StateFlow로 상태를 받아 글자와 버튼을 함께 고친다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 화면을 돌려 보며 무엇이 남는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. Logcat 필터는 `package:mine tag:Conn`이다.

## 1일차 — ViewModel로 옮기기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 6주차 `SmartIO`를 실행해 회전 문제를 확인하고 `ConnViewModel.kt` 파일을 만든다 |
| 10–25분 | 카운트다운·`connectFake()`·`tryConnect()`를 `ConnViewModel`로 옮긴다 |
| 25–35분 | `MainActivity`에서 `by viewModels()`로 받아 부르고, 화면 글자와 Logcat을 비교한다 |
| 35–45분 | `showState()` 틀을 복사해 넣고, 문구 알림을 등록·해제한다 |
| 45–53분 | 회전 뒤 `resultText`를 다시 읽게 하고 여러 때에 회전해 본다 |
| 53–60분 | 관찰표를 채우고 연습 캡처를 저장한다 |

### 1. 6주차 프로젝트에서 회전 문제 확인하기

6주차 완성 코드를 실행하고 아래 두 때에 화면을 돌린다. 회전 버튼은 에뮬레이터 도구 막대에 있다. 화면이 안 돌면 빠른 설정에서 **자동 회전**을 켠다.

| 회전한 때 | 회전 뒤 화면 |
|---|---|
| `검색 중… 3` |  |
| `연결 실패`와 [다시 시도]가 보일 때 |  |

왜 이렇게 되는지 3주차 회전 순서(`onDestroy` → `onCreate`)로 한 문장 적는다.

### 2. ConnViewModel 만들기

1. Project 창 `app › kotlin+java › com.example.smartio`에서 **New › Kotlin Class/File › Class**로 `ConnViewModel.kt`를 만든다.
2. 클래스 머리를 `class ConnViewModel : ViewModel()`로 바꾸고 프로퍼티를 둔다.

```kotlin
class ConnViewModel : ViewModel() {
    var resultText = "대기 중"                   // 마지막으로 알린 문구
    var listener: ((String) -> Unit)? = null     // 틀: 문구를 받을 화면 쪽 코드
    // 6주차 MainActivity의 scanJob 변수를 여기로 옮긴다
}
```

- `ViewModel`, `Job`이 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 import한다.
- `listener` 줄은 모양을 그대로 옮겨 쓴다. 채점하지 않는 틀이다.

### 3. 코루틴과 가짜 연결 옮기기

`ConnViewModel` 안에 함수 여섯 개를 둔다. 6주차 `MainActivity`의 코드를 옮기되 **`binding`은 한 줄도 가져오지 않는다.**

| 함수 | 할 일 | 6주차 어디서 가져오나 |
|---|---|---|
| `startScan()` | 이미 돌고 있으면 끝냄 → `viewModelScope.launch`로 5→1 카운트다운 → `tryConnect()` | [검색] 리스너의 `launch` 안과 `countDown()` |
| `stopScan()` | `scanJob?.cancel()` | [중지] 리스너 첫 줄 |
| `retry()` | `viewModelScope.launch`로 `tryConnect()`만 다시 | [다시 시도] 리스너 |
| `show(text)` | Logcat `Conn`에 남기기 → `resultText`에 보관 → `listener?.invoke(text)` | 새로 만든다 |
| `connectFake()` | 그대로 복사 | `connectFake()` |
| `tryConnect()` | `show("연결 중…")` → `try/catch`로 결과 문구 정하기 → `show(결과)` | `tryConnect()`에서 `binding`·`Intent`·`Toast`를 뺀다 |

```kotlin
fun startScan() {
    if (scanJob?.isActive == true) {
        return
    }
    scanJob = viewModelScope.launch {
        // 6주차 countDown()의 for 문. binding 줄 대신 show("검색 중… $i")
        tryConnect()
    }
}
```

- `viewModelScope`는 `androidx.lifecycle.viewModelScope`, `Log`는 `android.util.Log`다. `Random`은 6주차처럼 `kotlin.random.Random`을 고른다.
- 이 단계가 끝나도 화면은 6주차와 같다. 빌드만 되면 된다. 막히면 [따라하기 3단계](walkthrough.md#3-코루틴과-가짜-연결을-viewmodel로-옮기기)를 본다.

### 4. MainActivity에서 부르고 알림 받기

1. `scanJob` 변수 자리에 `private val viewModel: ConnViewModel by viewModels()`를 둔다.
2. [검색]·[중지]·[다시 시도] 리스너의 코루틴 코드를 `viewModel.startScan()`·`viewModel.stopScan()`·`viewModel.retry()`로 바꾼다. 버튼·ProgressBar 줄은 남긴다.
3. `MainActivity`의 `countDown()`·`connectFake()`·`tryConnect()`를 지운다.
4. 실행해 [검색]을 누르고 **화면 글자**와 **Logcat**을 비교한다. 무엇이 다른지 한 줄로 적는다.
5. 문구를 받아 화면을 고치는 `showState()`를 넣는다. 6주차 `tryConnect()`에 있던 글자·버튼·`Intent`·`Toast` 줄을 문구별로 모은 함수다. 아래를 **그대로 복사**해 `onCreate()`의 마지막 `}` 아래에 붙인다(따라하기 5단계와 같다).

```kotlin
private fun showState(text: String) {
    binding.stateText.text = text
    if (text == "연결 중…") {
        binding.stopButton.isEnabled = false
    } else if (text == "연결됨") {
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
        val intent = Intent(this, ControlActivity::class.java)
        intent.putExtra("name", binding.deviceNameEdit.text.toString())
        startActivity(intent)
    } else if (text == "연결 실패") {
        Toast.makeText(this, text, Toast.LENGTH_SHORT).show()
        binding.retryButton.visibility = View.VISIBLE
        binding.scanProgress.visibility = View.GONE
        binding.scanButton.isEnabled = true
    }
}
```

6. 등록과 해제를 직접 채운다.

```kotlin
// onCreate 안, [다시 시도] 블록 아래
viewModel.listener = { text ->
    showState(text)
}

// onCreate 아래: 화면이 없어질 때 등록을 푼다
override fun onDestroy() {
    super.onDestroy()
    // listener 비우기
}
```

- 6주차와 같이 카운트다운 → `연결됨`(제어 화면) 또는 `연결 실패`(Toast·[다시 시도])가 보이면 성공이다.

### 5. 회전 뒤 다시 읽기와 관찰표

`onCreate`의 끝에서 `viewModel.resultText`를 `stateText`에 넣고, 그 값이 `"연결 실패"`면 [다시 시도]를 보이게 한다.
막히면 [따라하기 6단계](walkthrough.md#6-회전-뒤-남은-문구-다시-읽기)를 본다. 그다음 아래 때에 회전하고 표를 채운다.
폰 크기 화면을 가로로 돌리면 아래쪽이 잘려 [다시 시도]·[연결]이 반쯤 가려질 수 있다. 반쯤 가려진 버튼도 보이는 것으로 적는다.

| 회전한 때 | 글자 | [검색]·[중지]·ProgressBar | Logcat `tag:Conn` |
|---|---|---|---|
| `연결 실패`와 [다시 시도]가 보일 때 |  |  |  |
| `검색 중… 3` |  |  |  |
| `검색 중… 3`에서 회전한 뒤 [검색] |  |  |  |

글자는 이어지는데 버튼이 처음 모양으로 돌아가는 까닭을 한 문장으로 적는다. 2일차에 이 문제를 해결한다.

연습 캡처 두 장을 저장해 둔다(제출은 2일차).

1. `연결 실패`와 [다시 시도]가 보이는 상태에서 회전한 가로 화면
2. 카운트다운 중에 회전한 뒤의 가로 화면과 Logcat. 글자는 이어지지만 ProgressBar가 없고 [중지]가 꺼져 있다.

### 6. 오늘 확인할 것

- [ ] `ConnViewModel.kt`에 `binding`이 한 줄도 없다.
- [ ] [검색] → 카운트다운 → `연결됨`(제어 화면) 또는 `연결 실패`(Toast·[다시 시도])가 6주차처럼 동작한다.
- [ ] `연결 실패`에서 회전해도 `연결 실패`와 [다시 시도]가 남는다.
- [ ] 카운트다운 중에 회전하면 글자가 이어진다(버튼은 처음 모양이어도 된다).
- [ ] `onDestroy()`에서 `listener`를 비운다.
- [ ] 관찰표를 채웠다.

프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — StateFlow로 상태 받기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–8분 | `ConnState.kt`를 만들고 [해제] 버튼을 XML에 넣는다 |
| 8–22분 | `ConnViewModel`을 `_state`·`_seconds`로 바꾼다 |
| 22–40분 | `MainActivity`에 틀을 넣고 `collect { }` 안에서 글자와 버튼을 고친다 |
| 40–50분 | 남은 초 틀을 넣고 `연결 중… 3`에서 회전해 캡처한다 → 캡처 1 |
| 50–60분 | `준비됨` 화면을 캡처하고(캡처 2) 세 파일과 함께 제출한다 |

### 1. ConnState와 [해제] 버튼 만들기

1. **New › Kotlin Class/File › Object**로 `ConnState.kt`를 만들고 `const val` 상수 다섯 개를 둔다.

| 상수 | 값 | 이번 주 뜻 |
|---|---|---|
| `DISCONNECTED` | `연결 안 됨` | 처음, 또는 [중지]·[해제]를 누른 뒤 |
| `CONNECTING` | `연결 중` | 5초를 세는 중 |
| `DISCOVERING` | `서비스 확인 중` | 가짜 연결(2초)을 기다리는 중 |
| `READY` | `준비됨` | 연결 성공 |
| `LOST` | `끊김` | 연결 실패 |

2. `strings.xml`에 `disconnect`(`해제`)를 넣고, `activity_main.xml`의 **가로 줄** `stopButton` 아래에 `disconnectButton`을 `android:enabled="false"`로 넣는다.
3. 실행해 가로 줄에 [검색] [중지] [해제]가 보이면 다음으로 간다.

### 2. ConnViewModel을 StateFlow로 바꾸기

1일차 코드에서 아래처럼 바꾼다.

| 1일차 | 2일차 |
|---|---|
| `var resultText`, `var listener` | `_state`/`state`, `_seconds`/`seconds` |
| `show("검색 중… $i")` | `_seconds.value = i` (반복 전에 `_state.value = ConnState.CONNECTING`, 반복 뒤 `_seconds.value = 0`) |
| `show("연결 중…")` | `_state.value = ConnState.DISCOVERING` |
| `show("연결됨")` / `show("연결 실패")` | `ConnState.READY` / `ConnState.LOST` |
| `stopScan()`: 취소만 | 취소 + 남은 초 `0` + `ConnState.DISCONNECTED` |
| 없음 | `fun disconnect()`: `ConnState.DISCONNECTED` |

```kotlin
private val _state = MutableStateFlow(ConnState.DISCONNECTED)
val state: StateFlow<String> = _state
// _seconds / seconds도 같은 모양. 처음 값은 0
```

- `show()`는 지운다. Logcat은 반복 안에서 `Log.d("Conn", "연결 중… $i")`, `tryConnect()` 끝에서 `Log.d("Conn", _state.value)`로 남긴다.
- `MutableStateFlow`, `StateFlow`는 Alt+Enter로 `kotlinx.coroutines.flow`의 것을 가져온다.
- 이 단계를 마치면 `MainActivity.kt`에 빨간 줄이 생긴다. 3번까지 마치고 실행한다.

### 3. 틀 넣고 collect 안 채우기

코드를 바꾸기 전에 상태마다 무엇을 켤지 표를 먼저 채운다. 첫 줄은 채워 두었다.

| 상태 | [검색] | [중지] | [해제] | [다시 시도] | ProgressBar |
|---|---|---|---|---|---|
| `DISCONNECTED` | 켬 | 끔 | 끔 | 숨김 | 숨김 |
| `CONNECTING` |  |  |  |  |  |
| `DISCOVERING` |  |  |  |  |  |
| `READY` |  |  |  |  |  |
| `LOST` |  |  |  |  |  |

1. 세 리스너는 ViewModel 함수 한 줄씩만 남기고, [해제] 리스너에서 `viewModel.disconnect()`를 부른다.
2. 1일차의 등록·다시 읽기 코드와 `onDestroy()`, `showState()`를 지운다.
3. `onCreate` 끝에 틀을 복사해 넣고 `collect { }` 안을 채운다.

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            // 1) stateText에 state 넣기
            // 2) [검색]·[중지]·[해제] 모두 끄기, [다시 시도]·ProgressBar 숨기기
            // 3) when (state)로 그 상태에 켤 것만 켜기
        }
    }
}
```

- [연결]은 4주차 그대로 항상 켜 둔다. 표와 `collect` 안에 넣지 않는다.
- `collect` 안에는 `startActivity`와 Toast를 넣지 않는다. 회전하거나 돌아올 때마다 다시 실행된다.
- `lifecycleScope`, `launch`, `repeatOnLifecycle`, `Lifecycle`이 빨간색이면 Alt+Enter로 import한다.
- 실행하면 `연결 안 됨` → [검색] → `연결 중` → `서비스 확인 중` → `준비됨` 또는 `끊김`이 보인다. 아직 숫자는 없다.

### 4. 남은 초 받고 회전하기

1. 같은 틀을 첫 틀 **아래**에 하나 더 넣고 `viewModel.seconds.collect { seconds -> }` 안에서, `seconds`가 0보다 크면 `stateText`를 `연결 중… $seconds`로 바꾼다.
2. `연결 중… 5`→`1`이 보이면 `연결 중… 3`에서 회전한다. 숫자·[중지]·ProgressBar가 이어지면 **캡처 1**을 찍는다. 폰 크기 가로 화면에서는 아래쪽 [연결]이 반쯤 가려져도 된다.
3. 홈으로 나갔다 돌아와도 같은지 본다.

### 5. 준비됨 화면과 제출 준비

| 조작 | 예상 화면 | 실제 화면 |
|---|---|---|
| [검색] → 성공 |  |  |
| [검색] → 실패 |  |  |
| `끊김`에서 [다시 시도] |  |  |
| `준비됨`에서 [해제] |  |  |
| `연결 중… 2`에서 [중지] |  |  |
| `준비됨`에서 [연결] → 제어 화면에서 [뒤로] |  |  |

`준비됨` 화면에서 가로 줄 [해제]만 켜져 있으면 **캡처 2**를 찍는다. 실패가 먼저 나오면 [다시 시도]를 누른다. 절반 확률이다.

9주차 1차 과제는 이번 주 화면을 이어서 만든다. 안내는 수업 공지를 따른다.

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 첫 줄이다. 파일 이름과 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 에뮬레이터에서 조금 다르게 보일 수 있다.

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'viewModels'.` | `viewModels`에 커서를 두고 Alt+Enter(맥 ⌥+Enter) → `androidx.activity.viewModels`를 import한다 |
| `Unresolved reference. None of the following candidates is applicable because of a receiver type mismatch:` 다음 줄 `val ViewModel.viewModelScope: CoroutineScope` | 클래스 머리가 `class ConnViewModel : ViewModel()`인지 본다. `viewModelScope`는 `ViewModel`을 물려받은 클래스 안에서만 쓸 수 있다 |
| `ConnViewModel.kt`에서 `Unresolved reference 'binding'.` | ViewModel은 화면(`binding`)을 모른다. 1일차는 `show("검색 중… $i")`로, 2일차는 `_state.value`·`_seconds.value`에 넣는다. 6주차 `tryConnect()`를 그대로 옮기면 이 오류와 함께 `Intent(this, …)`·`Toast.makeText(this, …)` 줄에 `None of the following candidates is applicable:`, `startActivity` 줄에 `Unresolved reference 'startActivity'.`도 나온다. 이 줄들은 모두 `MainActivity`의 `showState()`로 옮긴다 |
| `Reference has a nullable type 'kotlin.Function1<kotlin.String, kotlin.Unit>?'. Use explicit '?.invoke' to make a function-like call instead.` | `listener(text)`를 `listener?.invoke(text)`로 쓴다. 화면이 등록하기 전과 해제한 뒤에는 `null`이다 |
| `Unresolved reference 'REDY'.` (다른 상수 이름도 같은 모양) | `ConnState.`까지 치고 자동 완성 목록에서 고른다 |
| `Const 'val' is only allowed on top level, in named objects, or in companion objects.` (이어서 상수를 쓴 곳마다 `Unresolved reference`) | `class ConnState`를 `object ConnState`로 바꾼다. `ConnState.kt`의 첫 오류만 고치면 나머지는 함께 사라진다 |
| `MainActivity.kt`에서 `'val' cannot be reassigned.` | 화면에서 `viewModel.state.value = …`로 바꾸지 않는다. `viewModel.disconnect()`처럼 ViewModel 함수를 부른다 |
| `Suspend function 'suspend fun collect(collector: FlowCollector<Int>): Nothing' should be called only from a coroutine or another suspend function.` (`<Int>` 자리는 받는 값에 따라 달라서, `state`를 받을 때는 `<String>`으로 나온다) | `collect`를 틀 없이 `onCreate`에 바로 썼다. 틀(`lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { } }`) 안에 넣는다. `seconds` 틀이면 `state` 틀 **아래**에 둔다 |
| `Unresolved reference 'repeatOnLifecycle'.` 과 `Suspension functions can only be called within coroutine body.` | Alt+Enter로 `androidx.lifecycle.repeatOnLifecycle`을 import한다. 두 번째 메시지는 함께 사라진다 |
| `Unresolved reference 'disconnectButton'.` | `activity_main.xml`의 `android:id="@+id/disconnectButton"` 철자를 본다. 오류는 Kotlin 파일에 나오지만 원인은 XML이다 |
| 빌드는 되는데 `연결 실패`에서 회전하면 `대기 중`으로 돌아가고 [다시 시도]가 사라진다 | `private val viewModel = ConnViewModel()`로 직접 만들었는지 본다. `by viewModels()`로 받는다 |
| (예상, 1일차) 회전한 뒤 숫자가 멈추고 끝까지 바뀌지 않는다 | `onCreate`의 `viewModel.listener = { … }` 등록이 빠졌는지 본다. 회전하면 새 화면이 다시 등록해야 한다 |
| (예상, 2일차) 회전 직후 `연결 중… 3` 대신 `연결 중`만 보이고 1초 뒤에야 숫자가 나온다 | `seconds` 틀이 `state` 틀 위에 있는지 본다. 아래로 옮긴다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 세 파일과 캡처 2장

1. **`ConnState.kt`, `ConnViewModel.kt`, `MainActivity.kt`**: 2일차 최종 코드
2. **캡처 1**: [검색] 뒤 `연결 중… 3`(또는 2)에서 회전한 가로 화면. **숫자**가 보이고, [중지]만 켜져 있고, ProgressBar가 보인다. 숫자 없이 `연결 중`만 보이면 [4번](#4-남은-초-받고-회전하기)의 남은 초 틀을 확인하고 다시 찍는다
3. **캡처 2**: `준비됨` 화면. 가로 줄 [검색]·[중지]·[해제] 가운데 [해제]만 켜져 있고 [다시 시도]·ProgressBar는 숨어 있다

채점은 [README 완료 기준](README.md#완료-기준)의 항목으로 하고, 제출물은 모두 2일차 결과다. 1일차 관찰표와 연습 캡처는 내지 않는다.
1일차를 끝내지 못했으면 1일차 완성 코드(`examples/day1`)로 바꿔 2일차를 이어 한다. 2일차 틀과 `when`은 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: 회전한 뒤 `resultText`가 `연결 중…`이면 ProgressBar도 보이게 `onCreate`의 다시 읽기 코드에 `if`를 하나 더 둔다.
- 1일차: `ConnViewModel`에 `var scanCount = 0`을 두고 `startScan()`이 새로 시작할 때마다 1씩 늘린다. [검색]을 누를 때 Toast `검색 횟수: 3`처럼 보여 주고, 회전한 뒤에도 횟수가 이어지는지 확인한다.
- 2일차: [해제]를 누르면 Toast `연결을 해제했습니다`를 띄운다. `collect` 안이 아니라 리스너 안에 둔다.
- 2일차: [연결]을 `준비됨`일 때만 켜지게 바꾼다(`collect` 안의 끄기 목록과 `when`에 한 줄씩).

추가 과제는 선택 사항이다.
