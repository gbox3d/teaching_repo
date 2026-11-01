# 14주차 실습 — 안전한 명령 전송과 입력 수신·재연결

두 날 모두 BLE 마무리 실습이다. 1일차 60분에는 보내도 되는 번호만 보내게 막고, `준비됨`일 때만 누르게 하고, 오류 응답을 창과 색으로 알린다. 2일차 60분에는 보드가 보내는 값을 받아 이력에 쌓고, 끊기면 알리고 다시 연결한다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 한 곳씩 바꿔 가며 화면과 Logcat `tag:BLE`가 어떻게 달라지는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. 보드가 없는 학생은 `useFake = true`(Fake) 그대로 두 날 모두 끝까지 할 수 있다.

1일차에 고치는 파일은 `ControlActivity.kt`, `activity_control.xml`, `strings.xml`, `colors.xml` 네 개다. `MainActivity.kt`와 `activity_main.xml`은 1일차에 그대로 둔다.
2일차에 고치는 파일은 `ControlActivity.kt`, `MainActivity.kt`, `activity_control.xml`, `activity_main.xml`, `strings.xml` 다섯 개다.
제어 화면에는 **목록 줄 탭 → `준비됨` → [제어 화면]**으로 들어간다. 연결(`준비됨`)이 안 된 채로 들어오면 상태가 `연결 안 됨`이라 명령이 버려진다.

15주차에 내는 과제(완성 앱·캡처 세트·레포트)는 13주차에 발표한 계획안대로 마무리한다. 조건은 [13주차 과제 안내](../week13_ble_output/project_brief.md)에 있다. 이번 주 실습 제출은 그것과 별개로 각 날 한 번씩이다.

## 1일차 — 번호 검사와 오류 표시 (60분)

| 시간 | 할 일 |
|---|---|
| 0–8분 | 1번: 13주차 `SmartIO`를 실행해 [제어 화면]까지 들어가 보고, `colors.xml`에 로그 색 두 개를 넣는다 |
| 8–22분 | 2번: 허용 번호 검사를 넣고 캡처 1을 찍는다 |
| 22–38분 | 3번: `준비됨`일 때만 버튼을 켜고, 보낸 직후 300ms 동안 버튼을 막는다 |
| 38–52분 | 4번: 오류 응답이면 AlertDialog와 빨간 로그를 보여 준다. 띄어쓰기를 일부러 빼서 확인하고 캡처 2를 찍은 뒤 되돌린다 |
| 52–60분 | 5번: 최종 파일과 캡처 두 장을 정리해 제출한다. 시간이 남으면 6번 (확장) 밝기 조절을 한다 |

- **52분까지 반드시**: 2번(허용 번호 검사·캡처 1)과 4번(오류 표시·캡처 2). 제출 캡처 두 장이 이 두 단계에서 나온다.
- **늦으면 다음으로 미룸**: 6번 (확장) SeekBar. 3번이 38분에 끝나지 않았으면 4번을 먼저 하고 3번을 뒤로 돌린다. 캡처 2는 3번 없이도 찍을 수 있다.

### 1. colors.xml에 로그 색 넣기

1. 13주차 `SmartIO`를 실행해 [검색] → 목록 줄 탭 → `준비됨` → [제어 화면]까지 들어가 본다. `3` → LED Switch를 켜면 로그에 `on 3`과 응답이 쌓인다.
2. `app › res › values › colors.xml`을 연다. `black`·`white` 두 줄 아래에 `log_ok`(`#FF2E7D32`, 초록)와 `log_error`(`#FFD32F2F`, 빨강)를 넣는다.
3. 파일이 없으면 `values`를 오른쪽 클릭 → **New › Values Resource File** → 이름 `colors`로 만든다.
4. 실행해 화면이 13주차와 같으면 다음으로 간다. 색은 4번에서 쓴다.

막히면 [따라하기 1단계](walkthrough.md#1-colorsxml에-로그-색-두-개-넣기)를 본다.

### 2. 허용 번호 검사 → 캡처 1

1. LED Switch 리스너의 빈 칸 가지 **아래**·`else if (isChecked)` **위**에 가지 하나를 더 넣는다.

```kotlin
} else if (/* 허용 번호가 아니면 */) {
    // Toast "허용되지 않는 번호" (보내지도, 로그에 쌓지도 않는다)
} else if (isChecked) {
```

2. 클래스 끝(`onStop()` 아래)에 참/거짓을 돌려주는 함수를 만든다. 10주차 `hasBlePermissions()`와 같은 모양이다.

```kotlin
private fun isAllowedIndex(index: Int): Boolean {
    // listOf(0, 1, 2, 3)에 index가 있으면 true를 돌려준다
    // index가 -1(전체)이어도 true
    // 아니면 false
}
```

3. 1번 가지의 조건에서 `pin`을 숫자로 바꿔 이 함수를 부르고 `== false`로 확인한다.
4. 실행하고 표를 채운다.

| 입력 칸 → Switch 켜기 | 예상 | 실제 | Logcat `writeCharacteristic` 줄이 생겼나 |
|---|---|---|---|
| `3` |  |  |  |
| `4` |  |  |  |
| `9` |  |  |  |
| (비움) |  |  |  |

5. `9` → Switch 켜기 → Toast `허용되지 않는 번호`가 보이고 로그에 `on 9`가 없는 화면을 **캡처한다(캡처 1).** Toast는 2초 만에 사라지니 뜨자마자 찍는다. Fake로 찍어도 된다.

- 빈 칸 검사를 허용 번호 검사보다 **먼저** 두는 까닭을 `toInt()`로 한 문장 적는다.
- 표의 `4`는 허용 번호인데도 수업 보드에 LED가 없는 번호다. 앱이 막는 것과 보드가 못 하는 것이 어떻게 다른지 한 문장 적는다.

막히면 [따라하기 2단계](walkthrough.md#2-허용되지-않는-번호-막기)를 본다.

### 3. 준비됨일 때만, 보낸 직후 300ms는 막기

1. `activity_control.xml`의 `ledSwitch`와 `allOffButton`에 `android:enabled="false"`를 넣는다.
2. `// 4.` collect 안, `binding.stateText.text = "상태: $state"` **아래**에서 Switch·[전체 끄기]를 먼저 끄고, `state`가 `ConnState.READY`이면 켠다. `ConnState`는 Alt+Enter로 `com.example.smartio.bleuno.ConnState`를 import한다.
3. 클래스 끝(`isAllowedIndex` 아래)에 `private fun pauseButtons()`를 만든다. 두 버튼을 끄고, `lifecycleScope.launch { }` 안에서 `delay(300)` 뒤 `Bleuno.client?.isReady == true`이면 다시 켠다.
4. `send`를 부르는 세 곳(켜기·끄기·[전체 끄기])의 `append` 줄 **아래**에서 `pauseButtons()`를 부른다.
5. 표를 채운다. 300ms는 눈으로 보기 짧으니 잠깐 `delay(3000)`으로 바꿔 관찰한 뒤 **`delay(300)`으로 되돌린다.**

| 조작 | LED Switch·[전체 끄기] |
|---|---|
| 목록 줄 탭 → `준비됨` → [제어 화면] |  |
| [뒤로] → [해제] → [연결]로 들어오기 |  |
| `delay(3000)`으로 바꿔 다시 실행 → 목록 줄 탭 → `준비됨` → [제어 화면] → `3` → Switch 켜기 직후 |  |
| 그 3초 뒤 |  |

- `Bleuno.client?.isReady == true`에서 `== true`를 붙이는 까닭을 "client가 없으면"으로 한 문장 적는다.

막히면 [따라하기 3단계](walkthrough.md#3-준비됨일-때만-누르고-보낸-직후-300ms-쉬기)를 본다.

### 4. 오류 응답을 창과 색으로 알리기 → 캡처 2

1. `onStart()`의 `if (result != null) {` 안, `append` 줄 **아래**에 가지를 넣는다.

```kotlin
if (result != "ok") {
    // BleunoMessage.message(json)로 설명을 꺼낸다 (null이면 "" — 3주차 ?:)
    // 로그 글자색을 R.color.log_error로 (ContextCompat.getColor)
    // AlertDialog: 제목 "보드가 오류를 알렸습니다", 내용 "응답: $result · $message", [확인]
} else {
    // 로그 글자색을 R.color.log_ok로
}
```

2. `AlertDialog`는 Alt+Enter 목록에서 **`androidx.appcompat.app.AlertDialog`**, `ContextCompat`은 `androidx.core.content.ContextCompat`을 고른다.
3. 실행해 `3` → Switch 켜기 → 로그가 초록색이 되는지 본다.
4. 오류 응답을 일부러 만든다. 켜기 가지의 `send` 줄만 `"on $index"`를 `"on$index"`(띄어쓰기 없음)로 바꾸고 실행한다. [제어 화면]에 **들어온 직후** `3` → Switch 켜기를 하고 표를 채운다.

| 확인할 것 | 실제 |
|---|---|
| 앱 로그의 새 두 줄 |  |
| 로그 글자색 |  |
| AlertDialog 제목과 내용 |  |
| Logcat `writeCharacteristic(가짜):` 뒤의 글자 |  |
| [확인] → [전체 끄기] 뒤 로그 글자색 |  |

5. 창이 떠 있는 동안 **캡처한다(캡처 2).** 빨간 로그와 AlertDialog가 함께 보여야 한다.
6. 확인이 끝나면 **반드시 `"on $index"`로 되돌린다.**

- 앱 로그의 명령과 Logcat의 글자가 다른 까닭을 한 문장 적는다. 명령이 이상하면 어느 쪽을 믿어야 할까?
- `err`와 `fail`이 같은 가지로 가는 까닭을 조건 `result != "ok"`로 한 문장 적는다.

막히면 [따라하기 4단계](walkthrough.md#4-오류-응답을-alertdialog와-색으로-알리기)를 본다.

### 5. 제출 정리

1. 되돌린 코드로 한 번 더 실행해 `3` → Switch 켜기가 초록 `ok`로 끝나는지 본다.
2. `ControlActivity.kt`, `activity_control.xml`, 캡처 1, 캡처 2를 모은다. 캡처는 **세로 화면**에서 찍은 것을 쓴다.

### 6. (확장) SeekBar로 LED 0 밝기

1. `strings.xml`에 `pwm_title`(`LED 0 밝기`), `activity_control.xml`의 `allOffButton` 아래에 가로 `LinearLayout`(제목 `TextView` + id `pwmSeekBar`인 `SeekBar`, 폭 `160dp`, `android:max="255"`, `android:enabled="false"`)을 넣는다.
2. onCreate 끝에 `binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener { … })`를 만든다. 함수 세 개(`onProgressChanged`·`onStartTrackingTouch`·`onStopTrackingTouch`)를 모두 적고, **손을 뗄 때만** `pwm 0 값`을 보내고 로그에 쌓은 뒤 `pauseButtons()`를 부른다.
3. 3번의 collect와 `pauseButtons()`에서 `pwmSeekBar`도 같이 끄고 켠다.
4. 막대를 끌었다 놓으면 로그에 `pwm 0 값`과 `응답: {"result":"ok","ms":"pwm set"}`이 쌓이는지 본다. 실보드면 0번 LED 밝기가 바뀐다.

막히면 [따라하기 5단계](walkthrough.md#5-확장-seekbar로-led-0-밝기-조절하기)와 [1일차 완성 코드](examples/day1/ControlActivity.kt)를 본다.

### 7. 오늘 확인할 것

- [ ] `9`를 넣고 Switch를 켜면 Toast만 뜨고 명령 로그와 Logcat에 아무 줄도 생기지 않는다.
- [ ] 입력 칸을 비운 채 Switch를 켜도 앱이 멈추지 않는다.
- [ ] `연결 안 됨`으로 제어 화면에 들어오면 Switch와 [전체 끄기]가 회색이다.
- [ ] 명령을 보낸 직후 두 버튼이 잠깐 꺼졌다가 다시 켜진다.
- [ ] `ok` 응답이면 로그가 초록, `fail` 응답이면 로그가 빨강이 되고 창이 뜬다.
- [ ] `"on$index"`를 `"on $index"`로 되돌렸다.
- [ ] 캡처 두 장을 세로 화면에서 찍었다.

## 2일차 — 입력 받기·끊김·재연결 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 1번: 1일차 `SmartIO`를 실행해 `준비됨` 제어 화면에 들어가고, Logcat에서 입력 이벤트 줄을 확인한다 |
| 5–15분 | 2번 1~6: 입력 이력 자리(문자열·XML)와 목록·어댑터·`addHistory`를 만들고, 받은 줄을 세 갈래로 가르는 코드를 넣는다(실행은 다음 구간) |
| 15–25분 | 2번 7의 실행 표를 채우고, 3번 [온습도 받기 시작]·[중지]를 만든다 |
| 25–40분 | 5번: 연결 화면에 주소 저장·[재연결]·(시험용) [끊김 시험]을 넣고, 제어 화면 끊김 Toast를 넣는다 |
| 40–52분 | 4번 이력 줄 `split` Toast → 6번 연결 시간 제한 |
| 52–60분 | 7번: 캡처 두 장을 찍어 제출한다 |

- **52분까지 반드시**: 2·3번(입력 이력·온습도 받기)과 5번(끊김·[재연결]). 제출 캡처 두 장이 이 세 단계에서 나온다.
- **늦으면 다음으로 미룸**: 4번(이력 줄 `split` Toast), 6번(연결 시간 제한과 `delay(1000)` 확인). 25분에 3번이 끝나지 않았으면 4번을 건너뛰고 5번부터 한다.
- 6번 연결 시간 제한은 15주차 과제의 필수 기능이므로, 이번 주에 못 넣었으면 최종 제출 전에 자기 프로젝트에서 넣고 시간 초과 화면을 캡처해 둔다.

### 1. 입력 이벤트 줄 먼저 보기

1. 앱을 실행하고 [검색] → `ESP32_BLE_FAKE1` 줄 누르기 → `준비됨` → [제어 화면]으로 들어간다.
2. Logcat 필터를 `package:mine tag:BLE`로 두고 15초쯤 기다린다.
3. 아래 표를 채운다.

| 확인할 것 | 내 화면 |
|---|---|
| 10초마다 Logcat에 찍히는 줄 |  |
| 그 줄이 앱 명령 로그에 들어갔나 |  |
| 그 줄에 `result`가 있나 |  |

- 1일차 오류 표시(16번)를 넣은 코드에서 이 줄이 창을 띄우지 않는 까닭을 `if (result != null)`로 한 문장 적는다.

### 2. 입력 이력 자리와 받은 줄 가르기

1. `strings.xml`에 `input_start`(`온습도 받기 시작`), `input_history_title`(`입력 이력`), `reconnect`(`재연결`), `lost_test`(`끊김 시험`) 네 줄을 넣는다. [중지]는 기존 `stop`을 쓴다.
2. `activity_control.xml`의 명령 로그 칸(`logText`) **아래**·[뒤로] **위**에 가로 `LinearLayout`([온습도 받기 시작] `inputStartButton`, [중지] `inputStopButton`, 둘 다 `android:enabled="false"`), 제목 `TextView`(`@string/input_history_title`), `ListView`(`inputList`, 폭 `240dp`, 높이 `0dp`, `layout_weight="2"`, `transcriptMode="alwaysScroll"`)를 넣는다. 막히면 [따라하기 3단계](walkthrough.md#3-제어-화면에-입력-이력-자리-만들기).
3. `ControlActivity.kt` 클래스 안에 이력 목록 `history`(11주차 `mutableListOf<String>()`)와 `private lateinit var historyAdapter: ArrayAdapter<String>`을 두고, onCreate 끝에서 어댑터를 만들어 `binding.inputList`에 붙인다.
4. 클래스 끝에 이력 한 줄을 넣는 함수를 만든다.

```kotlin
private fun addHistory(text: String) {
    // 지금 시각 글자: SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())
    // history에 "시각 text" 한 줄을 add
    // 어댑터에 알린다 (11주차)
}
```

5. `onStart()`의 응답 처리를 세 갈래로 바꾼다.

```kotlin
val result = BleunoMessage.result(json)
// event와 value도 꺼낸다 (BleunoMessage.event / BleunoMessage.value)
if (/* event가 "input"이면 */) {
    // 이력에 "입력=값" (띄어쓰기 없이)
} else if (/* value가 있으면 */) {
    // 이력에 값
} else if (result != null) {
    // 1일차 명령 로그·오류 색·AlertDialog 그대로
}
```

6. `SimpleDateFormat`·`Date`·`Locale`이 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 import한다. `Date`는 목록에서 **`java.util.Date`**를 고른다.
7. 실행하고 표를 채운다.

| 조작 | 예상 입력 이력 | 실제 입력 이력 | 명령 로그 새 줄 |
|---|---|---|---|
| `준비됨` 제어 화면에서 25초 두기 |  |  |  |
| `3` → LED Switch 켜기 |  |  |  |

- `event` 가지와 `value` 가지의 순서를 바꾸면 입력 이벤트가 이력에 어떤 모양으로 들어갈지 **예상만** 적는다(바꾸지 않는다). 힌트: 입력 이벤트 JSON에도 `"value"`가 있다.

### 3. 온습도 3초마다 받기와 [중지]

1. 클래스 안에 `private var inputJob: Job? = null`을 둔다.
2. onCreate에서 [온습도 받기 시작] 리스너를 만든다.

```kotlin
binding.inputStartButton.setOnClickListener {
    // [온습도 받기 시작] 끄기, [중지] 켜기
    inputJob = lifecycleScope.launch {
        // 취소되지 않았으면(isActive) 되풀이: "dht11"을 보내고 3초 기다리기
    }
}
```

3. 클래스 끝에 `private fun stopInput()`을 만든다. `inputJob?.cancel()`, 두 버튼 끄기, `Bleuno.client?.isReady == true`이면 [온습도 받기 시작]만 켜기.
4. `stopInput()`을 세 곳에서 부른다. [중지] 리스너 안, `// 4.` collect의 `// 13.` `if (state == ConnState.READY) { … }` 아래, `onStop()`의 `onMessage(null)` 아래.
5. `Job`·`isActive`를 import한다. `isActive`는 `kotlinx.coroutines.isActive`다.
6. 실행하고 표를 채운다. 폰 크기 화면을 가로로 돌리면 위아래가 잘려 일부 버튼·글자가 안 보일 수 있다. 제어 화면은 가로에서 `명령 로그` 아래([온습도 받기 시작]·[중지]·입력 이력·[뒤로])가 화면 밖이다. 확인할 항목이 안 보이면 세로로 되돌려 확인한다(숫자 키보드가 뜨면 닫고 본다).

| 조작 | [온습도 받기 시작] | [중지] | 입력 이력 |
|---|---|---|---|
| `준비됨` 제어 화면에 들어옴 |  |  |  |
| [온습도 받기 시작] 뒤 10초 |  |  |  |
| [중지] 뒤 10초 |  |  |  |
| 받는 중 홈 → 앱으로 돌아오기 |  |  |  |
| 받는 중 화면 돌리기 |  |  |  |

- Logcat `tag:BLE`에서 `writeCharacteristic(가짜): "dht11"`과 `onCharacteristicChanged(가짜): {"result":"ok","value":"[…]"}`가 몇 초 간격인지 적는다.
- collect 안의 `stopInput()`이 받는 중에 반복을 멈추지 않는 까닭을 "StateFlow는 언제 값을 주나"(7주차)로 한 문장 적는다.

막히면 [따라하기 6단계](walkthrough.md#6-온습도-3초마다-받기와-중지)를 본다.

### 4. 이력 줄 나누기 — 오늘 문법 split

늦으면 미루는 단계다. 25분에 3번이 끝나지 않았으면 5번부터 하고, 이 단계는 6번 뒤나 다음에 한다.

onCreate에 입력 이력 줄 누르기 리스너를 만든다. 11주차 `setOnItemClickListener`와 같은 틀이다.

```kotlin
binding.inputList.setOnItemClickListener { _, _, position, _ ->
    // 누른 줄 history[position]을 split(" ")로 나눠 parts에 담는다
    // parts[0]은 시각, parts[1]은 값 → 각각 val에 담는다
    // Toast "받은 시각: 시각 · 값: 값"
}
```

| 누른 줄 | `parts[0]` | `parts[1]` | Toast |
|---|---|---|---|
| `시:분:초 [온도,습도]` 줄 |  |  |  |
| `시:분:초 입력=1` 줄 |  |  |  |

- 2번 5의 입력 이벤트 가지에서 `입력 1`처럼 띄어 써서 넣었다면 그 줄의 `[1]`이 무엇이 될지 한 문장 적는다.
- Toast 글자에 `$parts[0]`을 바로 쓰지 않고 `val`에 담는 까닭을 한 문장 적는다.

### 5. 끊김과 [재연결]

1. `activity_main.xml`의 [다시 시도] 버튼 `retryButton` **아래**·[권한 확인] **위**에 가로 `LinearLayout`([재연결] `reconnectButton`은 `visibility="gone"`, [끊김 시험] `lostTestButton`은 `enabled="false"`·`visibility="gone"`)을 넣는다.
2. `MainActivity.kt` 클래스 안에 `private var lastAddress = ""`를 둔다.
3. `// 19.` 목록 줄 리스너의 `client.connect(address)` 아래에서 `lastAddress = address`로 담고, 11주차 틀로 `"smartio"` 저장소에 `"lastAddress"` 이름표로 저장한다. onCreate의 `// 21.` 아래에서 같은 이름표로 꺼내 `lastAddress`에 넣는다.
4. `// 7.` collect에서 [재연결]을 먼저 숨기고, `ConnState.LOST ->` 가지에서 보이게 한 뒤 `showLostToast()`를 부른다. 이 함수는 클래스 끝에 만든다(Toast `연결이 끊겼습니다. [재연결]을 누르세요`).
5. [재연결] 리스너: `lastAddress`가 비었으면 Toast `마지막 주소가 없습니다. [검색]부터 하세요`, 아니면 `client.connect(lastAddress)`.
6. (시험용) [끊김 시험]은 [따라하기 10단계](walkthrough.md#10-시험용-끊김-시험으로-보드-없이-끊김-만들기)의 코드를 그대로 넣는다. 채점하지 않는다.
7. `ControlActivity.kt`의 `// 4.` collect에서 `stopInput()` 아래, `state`가 `ConnState.LOST`면 제어 화면용 `showLostToast()`(Toast `연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요`)를 부른다.
8. 실행하고 표를 채운다.

| 조작 | 연결 화면 상태와 보이는 버튼 | Toast |
|---|---|---|
| `준비됨` → [끊김 시험] |  |  |
| 이어서 [재연결] |  |  |
| [끊김 시험] 뒤 화면 돌리기 |  |  |
| `준비됨` → [제어 화면] → 화면 돌리기 → 가로인 채로 기기의 뒤로 가기 → [끊김 시험] → [재연결] |  |  |
| [끊김 시험] 뒤 [연결]로 제어 화면 들어가기 → [뒤로] |  |  |

9. `끊김` 상태와 [재연결] 버튼이 함께 보이는 연결 화면을 **캡처한다(캡처 2).** Toast가 같이 찍히면 더 좋다.

- 4번에서 `Toast.makeText(this, …)`를 collect 안에 바로 쓰지 않고 함수로 빼는 까닭을 `this`로 한 문장 적는다.
- 3번에서 저장하지 않고 변수에만 담았다면 넷째 줄이 어떻게 될지 예상을 적는다.

### 6. 연결 시간 제한

늦으면 미루는 단계다. 52분이 되면 7번 캡처를 먼저 한다.

1. 클래스 안에 `private var connectTimeoutJob: Job? = null`을 둔다.
2. 클래스 끝에 두 함수를 만든다. 6주차 `scanJob`·`countDown()`과 같은 모양이다.

```kotlin
private fun startConnectTimeout() {
    // 앞에서 건 예약이 있으면 취소 (?.cancel())
    // connectTimeoutJob = lifecycleScope.launch { waitConnectTimeout() }
}

private suspend fun waitConnectTimeout() {
    // 10초 기다리기 (밀리초)
    // 지금 상태 client.connectionState.value가 연결 중·서비스 확인 중이면 (listOf(…).contains(…)):
    //   Toast "연결 시간이 초과되었습니다", client.disconnect()
    //   stateText "연결 시간 초과 — [다시 시도]를 누르세요", ProgressBar 숨기기, [검색] 켜기, [다시 시도] 보이기
}
```

3. `startConnectTimeout()`을 연결을 시작하는 두 곳(목록 줄 리스너의 저장 줄 아래, [재연결]의 `connect` 아래)에서 부른다. onCreate의 주소 꺼내기 아래에서는 상태가 아직 연결 중·서비스 확인 중일 때만 부른다(회전 대비).
4. `Job`·`delay`를 import한다.
5. 실행해 목록 줄을 누른다. 가짜 보드는 약 2초 만에 `준비됨`이라 시간 초과가 나지 않는다. `delay(10000)`을 **잠시** `delay(1000)`으로 바꾸고 다시 실행해 표를 채운 뒤, 시간 초과 화면을 캡처하고 **반드시 되돌린다.**

| 확인할 것 | `delay(10000)` | `delay(1000)` |
|---|---|---|
| 목록 줄 누른 뒤 Toast |  |  |
| 상태 글자 |  |  |
| [검색]·[다시 시도] |  |  |

- 조건을 "연결 중·서비스 확인 중일 때만"이 아니라 `client.isReady == false`로 쓰면, `준비됨` 뒤 10초 안에 [끊김 시험]을 눌렀을 때 무엇이 달라질지 **예상만** 적는다.

막히면 [따라하기 12단계](walkthrough.md#12-연결-시간-제한-10초)와 [2일차 완성 코드](examples/day2/MainActivity.kt)를 본다.

### 7. 캡처와 제출

**세로 화면**에서 아래 두 장을 찍는다. 캡처 2는 5번 9에서 이미 찍었다.

| 번호 | 캡처 | 찍는 곳 |
|---|---|---|
| 1 | 입력 이력에 `시:분:초 [온도,습도]` 줄 2줄 이상(시각이 약 3초 간격)과 켜진 [중지]. Fake면 `시:분:초 입력=1`/`입력=0` 2줄도 된다 | 제어 화면 |
| 2 | 상태 `끊김`과 [재연결] 버튼 | 연결 화면 |

`ControlActivity.kt`, `MainActivity.kt`, `activity_control.xml`, `activity_main.xml`과 두 캡처를 모아 낸다.

### 8. 오늘 확인할 것

- [ ] 입력 이력에 입력 이벤트(`입력=1`)와 온습도(`[24.5,40.0]`) 줄이 시각과 함께 쌓이고, 명령 로그에는 들어가지 않는다.
- [ ] [중지]를 누르면 온습도 줄이 더 늘지 않고, 홈에 갔다 오면 받기가 꺼져 있다.
- [ ] 이력 줄을 누르면 `받은 시각: … · 값: …` Toast가 뜬다(4번을 했으면).
- [ ] `끊김`이면 Toast와 [재연결]이 보이고, [재연결]로 `준비됨`까지 간다. 제어 화면에서 끊겨도 Toast가 뜬다.
- [ ] `delay(1000)`으로 시간 초과를 확인하고 `delay(10000)`으로 되돌렸다(6번을 했으면).
- [ ] 캡처 두 장을 세로 화면에서 찍었다.

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 줄이다. 파일 이름 뒤의 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 기기에서 조금 다르게 보일 수 있다.

### 1일차

| 상황 | 확인할 것 |
|---|---|
| `Type inference failed. The value of the type parameter 'T' should be mentioned in input types (argument types, receiver type, or expected type). Try to specify it explicitly.` (`contains` 줄) | 메시지가 원인을 직접 말하지 않는다. 숫자 목록 `listOf(0, 1, 2, 3)`에서 글자 `pin`을 찾았다. `pin.toInt()`로 숫자를 넣는다 |
| `Unresolved reference 'log_error'.` (`R.color.log_error` 줄. `log_ok` 줄에는 `Unresolved reference 'log_ok'.`) | `colors.xml`에 두 색 줄을 넣지 않았거나 이름 철자가 코드와 다르다. `app › res › values › colors.xml`에서 `log_ok`·`log_error` 두 줄과 철자를 본다. `colors.xml` 파일이 아예 없으면 같은 줄에 `Unresolved reference 'color'.`로 나온다 |
| `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` (`pauseButtons` 안) | `delay(300)`을 `lifecycleScope.launch { }` 밖에서 불렀다. 6주차처럼 `launch { }` 안에 둔다 |
| `Unresolved reference 'ContextCompat'.` 또는 `Unresolved reference 'AlertDialog'.` | Alt+Enter로 import한다. `AlertDialog`는 후보가 두 개 뜨면 `androidx.appcompat.app.AlertDialog`를 고른다(10주차와 같다) |
| Fake로 `준비됨` 제어 화면에 가만히 있으면 10초마다 로그가 빨개지고 `응답: null · ` 창이 뜬다 | `if (result != null)` 검사가 빠졌다. 입력 이벤트 줄에는 `result`가 없다. 실보드는 이 줄을 보내지 않아 Fake에서만 드러난다 |
| `3` → Switch 켜기에 `응답: {"result":"fail","ms":"unknown command"}`, 로그가 빨갛고 창이 뜬다. Logcat에 `writeCharacteristic(가짜): "on3"` | 4번에서 일부러 바꾼 띄어쓰기가 그대로 남아 있다. `"on $index"`로 되돌린다. 앱 로그 줄이 아니라 Logcat에서 실제로 보낸 글자를 확인한다 |
| (예상) 입력 칸을 비운 채 Switch를 누르자 앱이 멈춘다. Logcat에 `java.lang.NumberFormatException: For input string: ""` | 허용 번호 가지를 빈 칸 가지보다 앞에 두었다. 순서는 빈 칸 → 허용 번호 → 켜기/끄기 |
| (예상) 아주 긴 숫자를 넣고 Switch를 누르자 앱이 멈춘다. Logcat에 `java.lang.NumberFormatException` | `pinEdit`의 `android:maxLength="2"`가 빠졌다 |
| (예상) `0`~`3`을 넣으면 `허용되지 않는 번호`, `9`를 넣으면 `on 9`가 나간다 | 조건에서 `== false`가 빠졌다. `isAllowedIndex(pin.toInt()) == false` |
| Switch·[전체 끄기]가 늘 회색이다 | 상단이 `상태: 준비됨`인지 본다. 준비됨인데도 회색이면 collect 안에서 `ConnState.READY`일 때 켜는 줄이 있는지 본다 |
| [전체 끄기]를 눌렀는데 Switch가 켜진 모양 그대로다 | 정상이다. [전체 끄기]는 보드에 명령만 보낸다. Switch를 다시 켜려면 한 번 끄고 켠다 |

### 2일차

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'isActive'.` | `isActive`는 `launch`·`delay`와 다른 이름이라 따로 import한다. 빨간 글자에 Alt+Enter(맥 ⌥+Enter) → `kotlinx.coroutines.isActive` |
| `Unresolved reference 'inputList'.` 아래에 `Cannot infer type for this parameter. Please specify it explicitly.`가 여러 줄 | 오류는 `ControlActivity.kt`에 뜨지만 고칠 곳은 `activity_control.xml`이다. `android:id="@+id/inputList"`가 있는지, 철자가 같은지 본다. 맨 위 줄을 고치면 따라 나온 줄도 사라진다 |
| `None of the following candidates is applicable:`(아래에 `static fun makeText(…)` 후보 두 줄)과 `Unresolved reference 'show'.` | 메시지가 원인을 직접 말하지 않는다. collect·`launch` 틀 안에서 `Toast.makeText(this, …)`를 썼다. 그 안의 `this`는 화면이 아니다. Toast를 화면의 함수(`showLostToast()`)로 빼서 부른다 |
| `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` (`waitConnectTimeout` 안) | 안에서 `delay`를 부르는 함수에 `suspend`가 빠졌다. `private suspend fun waitConnectTimeout()`. 6주차 `countDown()`과 같다 |
| `Argument type mismatch: actual type is 'kotlin.String?', but 'kotlin.String' was expected.` (`addHistory` 줄) | `addHistory(BleunoMessage.value(json))`처럼 꺼내자마자 넘겼다. `if (value != null)`로 확인한 변수 `value`를 넘긴다(3주차) |
| `Unresolved reference 'split'.` 아래에 `Cannot infer type for this parameter. Please specify it explicitly.` 두 줄 | `history.split(" ")`처럼 목록 전체에 썼다. `split`은 글자 하나에 쓴다. `history[position].split(" ")` |
| `Assignment type mismatch: actual type is 'kotlin.String?', but 'kotlin.String' was expected.` (`getString` 줄) | `prefs.getString("lastAddress", "")` 뒤에 `?: ""`가 빠졌다. 11주차 `lastName`과 같은 이유다 |
| `SimpleDateFormat`·`Date`·`Locale`이 빨간색 | Alt+Enter로 `java.text.SimpleDateFormat`, `java.util.Date`, `java.util.Locale`을 import한다. `Date`는 `java.sql.Date`가 아니라 `java.util.Date`를 고른다 |
| Fake 제어 화면에서 이력에 `12:00:10 1`, `12:00:20 0`처럼 숫자 하나만 있는 줄이 생기고 `입력=1` 줄은 나오지 않는다 | `if (value != null)` 가지를 `if (event == "input")`보다 먼저 두었다. 입력 이벤트 JSON에도 `"value"`가 있다. `event`를 먼저 본다 |
| Logcat `tag:BLE`에는 받은 줄(`onCharacteristicChanged`)이 찍히는데 입력 이력이 끝까지 늘지 않는다. 앱은 멈추지 않는다 | `addHistory()`에서 `add` 뒤 `historyAdapter.notifyDataSetChanged()`가 빠졌다(11주차) |
| [중지]를 누르면 버튼 모양만 바뀌고 이력은 계속 3초마다 늘어난다. 다시 시작하면 3초에 두 줄씩 쌓인다 | `lifecycleScope.launch {` 앞에 `inputJob =`이 빠졌다. `inputJob`이 늘 `null`이라 `cancel()`이 아무것도 멈추지 못한다. 6주차 `scanJob =`과 같다 |
| 제어 화면은 열리는데 첫 이력 줄이 들어오는 순간 앱이 멈춘다. Logcat에 `kotlin.UninitializedPropertyAccessException: lateinit property historyAdapter has not been initialized` | onCreate에서 `historyAdapter = ArrayAdapter(…)`와 `binding.inputList.adapter = historyAdapter` 두 줄이 빠졌다. `lateinit`은 넣기 전에 쓰면 멈춘다 |
| 목록 줄을 누르자마자 `연결 시간이 초과되었습니다`가 뜨고 몇 번 눌러도 `준비됨`이 되지 않는다 | `delay(10)`처럼 적었다. `delay`의 숫자는 **밀리초**라 10초는 `10000`이다. `delay(1000)`으로 확인한 뒤 되돌리지 않았는지도 본다 |
| 이력 줄을 누르면 Toast가 `받은 시각: [12:00:03, [24.5,40.0]][0] · 값: …`처럼 나온다 | 문자열 안에 `$parts[0]`을 바로 썼다. `$`는 `parts`까지만 읽는다. `val time = parts[0]`에 담아 `$time`으로 쓴다 |
| 이력 줄을 누르는 순간 앱이 멈춘다. Logcat에 `java.lang.IndexOutOfBoundsException` | `parts[2]`처럼 없는 칸을 꺼냈다. 이력 줄은 칸이 두 개(`[0]`·`[1]`)뿐이다. 번호는 0부터 센다 |
| 끊김 Toast가 화면을 돌리거나 [뒤로]로 돌아오거나 홈에서 돌아올 때마다 또 뜬다 | 정상이다. StateFlow가 새로 보이는 화면에 마지막 값 `끊김`을 다시 준다(7주차) |
| 받는 중에 화면을 돌렸더니 입력 이력이 비고 받기가 꺼졌다 | 정상이다. 이력은 그 화면이 가진 목록이라 화면이 새로 만들어지면 비고, `onStop`이 받기를 멈춘다. 캡처는 세로에서 찍는다 |
| (예상) [재연결]을 누르면 Toast `마지막 주소가 없습니다. [검색]부터 하세요`만 뜬다 | 목록 줄로 연결한 적이 없거나, 목록 줄 리스너의 `putString("lastAddress", …)` 저장 줄 또는 onCreate의 꺼내기 줄이 빠졌다 |
| [온습도 받기 시작]이 늘 회색이다 | 상단이 `상태: 준비됨`인지 본다. 준비됨인데도 회색이면 `// 4.` collect 안에서 `stopInput()`을 부르는지, `stopInput()`이 `isReady == true`일 때 켜는지 본다 |
| 실보드에서 입력 이벤트 줄이 생기지 않는다 | 정상이다. 지금 펌웨어는 보드가 먼저 보내는 메시지가 없다. 실보드는 [온습도 받기 시작]의 `dht11` 응답으로 입력을 받는다 |
| 실보드가 `연결 중`에 머물다 10초 뒤 시간 초과가 된다 | 보드 LED가 파랑 깜빡임인지(다른 폰이 연결했는지), 전원·거리를 본다. 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.
보드 문제인지 앱 문제인지 모르겠으면 Logcat `tag:BLE`에서 `writeCharacteristic` 뒤에 `onCharacteristicChanged`가 오는지 본다.

## 제출 — 두 날, 코드와 캡처 두 장씩

| 날 | 코드 | 캡처 1 | 캡처 2 |
|---|---|---|---|
| 1일차 | `ControlActivity.kt`, `activity_control.xml` | 입력 칸 `9`, Toast `허용되지 않는 번호`, 로그에 `on 9` 없음 | 빨간 로그와 AlertDialog `보드가 오류를 알렸습니다` |
| 2일차 | `ControlActivity.kt`, `MainActivity.kt`, `activity_control.xml`, `activity_main.xml` | 입력 이력 2줄과 켜진 [중지] | 상태 `끊김`과 [재연결] |

채점은 [README 완료 기준](README.md#완료-기준)의 항목을 이 제출물로 확인한다. 실습지의 관찰표는 스스로 점검하는 것이라 제출하지 않고 채점하지 않는다.
1일차 허용 번호 검사(캡처 1)와 2일차 입력 이력(캡처 1)까지 동작하면 기본 성공이다. 버튼 막기·오류 표시·연결 시간 제한은 예제와 도움을 받아 마무리해도 된다.
캡처는 세로 화면에서 찍고, 계정 이름·알림 내용이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.
15주차 과제 최종 제출(완성 앱·캡처 세트·레포트)은 이 실습 제출과 별개다. 조건은 [13주차 과제 안내](../week13_ble_output/project_brief.md)에 있다.

## 먼저 끝났다면

- 1일차: [전체 끄기] 옆에 [전체 켜기] 버튼을 둔다. 누르면 `on -1`을 보내고 로그에 쌓는다. `준비됨`일 때만 켜지고 보낸 직후 300ms 동안 꺼지게 collect와 `pauseButtons()`에 한 줄씩 더한다.
- 1일차: [전체 끄기] 뒤 `binding.ledSwitch.isChecked = false`로 Switch 모양도 끄면 무엇이 한 번 더 나갈지 예상하고, 로그로 확인해 본다(확인 뒤 되돌린다).
- 2일차: 가로 버튼 줄의 [중지] 옆에 [이력 지우기] 버튼을 둔다. 누르면 `history.clear()` 뒤 어댑터에 알려 목록을 비운다(12주차 `devices.clear()`와 같은 모양).
- 2일차: 온습도 요청 간격을 5초로 바꿔 이력 시각이 5초씩 벌어지는지 확인하고 되돌린다.
- 2일차: 보드와 실기기가 있으면 `useFake = false`로 온습도 2줄과 보드 전원 끄기 → `끊김` → [재연결]을 해 보고 캡처한다.

추가 과제는 선택 사항이며 점수에 더하거나 빼지 않는다.
