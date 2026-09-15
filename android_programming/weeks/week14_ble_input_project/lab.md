# 14주차 실습 — 입력 받기·끊김·재연결과 2차 과제 발표

1일차 60분에는 13주차 `SmartIO`에 입력 받기·끊김 알림과 [재연결]·연결 시간 제한을 넣고, 캡처 세트와 2~3분 시연을 한 바퀴 해 본다. 2일차 60분에는 순서대로 2차 과제를 발표한다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 표를 채우며 입력 이력과 Logcat `tag:BLE`가 어떻게 달라지는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. 과제 조건은 [과제 안내](project_brief.md), 점수는 [채점표](rubric.md)에 있다. 보드가 없는 학생은 `useFake = true`(Fake) 그대로 끝까지 할 수 있다.

14주차는 주차별 실습 점수 대상이 아니다. 이번 주에 내는 것은 2차 과제의 레포트·소스·발표다.
이번 주에 고치는 파일은 `ControlActivity.kt`, `MainActivity.kt`, `activity_control.xml`, `activity_main.xml`, `strings.xml` 다섯 개다.

## 1일차 — 입력 받기·끊김·재연결과 시연 리허설 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 1번: 13주차 `SmartIO`를 실행해 `준비됨` 제어 화면에 들어가고, Logcat에서 입력 이벤트 줄을 확인한다 |
| 5–15분 | 2번 1~6: 입력 이력 자리(문자열·XML)와 목록·어댑터·`addHistory`를 만들고, 받은 줄을 세 갈래로 가르는 코드를 넣는다(실행은 다음 구간) |
| 15–25분 | 2번 7의 실행 표를 채우고, 3번 [온습도 받기 시작]·[중지]를 만든다 |
| 25–40분 | 5번: 연결 화면에 주소 저장·[재연결]·(시험용) [끊김 시험]을 넣고, 제어 화면 끊김 Toast를 넣는다 |
| 40–47분 | 시간이 남으면 4번 이력 줄 `split` Toast → 6번 연결 시간 제한 |
| 47–60분 | 7번: 캡처 세트를 찍고, 짝과 서로 시간을 재며 2~3분 시연을 한 바퀴 한다 |

- **47분까지 반드시**: 2·3번(입력 이력·온습도 받기)과 5번(끊김·[재연결]). 이것만 되어도 리허설의 입력 2줄·끊김·[재연결] 장면이 나온다.
- **늦으면 다음으로 미룸**: 4번(이력 줄 `split` Toast), 6번(연결 시간 제한과 `delay(1000)` 확인). 25분에 3번이 끝나지 않았으면 4번을 건너뛰고 5번부터 한다.
- 4번은 시연에서 빼도 된다. 6번은 2차 과제 필수 기능(시간 초과 안내)이므로 발표 전까지 자기 프로젝트에서 넣고, 7번 표의 7번 캡처를 그때 찍는다.
- 구현이 늦어도 47분에는 멈추고 7번 리허설을 되는 데까지 한 번 한다. 남은 구현은 발표 전까지 자기 프로젝트에서 마무리한다.

### 1. 입력 이벤트 줄 먼저 보기

1. 앱을 실행하고 [검색] → `ESP32_BLE_FAKE1` 줄 누르기 → `준비됨` → [제어 화면]으로 들어간다.
2. Logcat 필터를 `package:mine tag:BLE`로 두고 15초쯤 기다린다.
3. 아래 표를 채운다.

| 확인할 것 | 내 화면 |
|---|---|
| 10초마다 Logcat에 찍히는 줄 |  |
| 그 줄이 앱 명령 로그에 들어갔나 |  |
| 그 줄에 `result`가 있나 |  |

- 13주차 9번 `if (result != null)`이 이 줄을 걸렀다. 오늘은 이 줄을 **입력 이력**에 넣는다.

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
    // 13주차 명령 로그·오류 색·AlertDialog 그대로
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

늦으면 미루는 단계다. 25분에 3번이 끝나지 않았으면 5번부터 하고, 이 단계는 리허설 뒤나 발표 전에 한다.

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

- 4번에서 `Toast.makeText(this, …)`를 collect 안에 바로 쓰지 않고 함수로 빼는 까닭을 `this`로 한 문장 적는다.
- 3번에서 저장하지 않고 변수에만 담았다면 넷째 줄이 어떻게 될지 예상을 적는다.

### 6. 연결 시간 제한

늦으면 미루는 단계다. 47분이 되면 7번 리허설을 먼저 한다. 다만 2차 과제 필수 기능이므로 발표 전까지 자기 프로젝트에서 넣고 시간 초과 화면을 캡처한다.

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

막히면 [따라하기 12단계](walkthrough.md#12-연결-시간-제한-10초)와 [완성 코드](examples/day1/MainActivity.kt)를 본다.

### 7. 캡처 세트와 2~3분 시연 리허설

1. 레포트에 넣을 캡처를 찍는다. **세로 화면**에서 찍는다.

| 번호 | 캡처 | 찍었나 |
|---|---|---|
| 1 | 권한 안내: Toast `권한 OK` 또는 거절 뒤 AlertDialog `권한이 필요합니다` |  |
| 2 | 장치 목록: `검색된 장치`에 `ESP32_BLE…` 줄 |  |
| 3 | 준비됨: 상태 `준비됨`, [제어 화면] 켜짐 |  |
| 4 | LED on/off: 명령 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`(실보드면 LED 사진도). LED를 켠 직후 찍는다 |  |
| 5 | 입력 수신: 입력 이력 2줄 이상(`시:분:초 [온도,습도]`, 시각이 약 3초 간격인 줄, 또는 Fake 입력 이벤트 2줄) |  |
| 6 | 끊김 + [재연결]: 상태 `끊김`과 [재연결] 버튼 |  |
| 7 | 시간 초과: Toast `연결 시간이 초과되었습니다`와 [다시 시도](6번에서 찍은 것) |  |

2. 짝 앞에서 아래 순서로 시연한다. 짝은 시간을 재고 빠진 장면을 적는다. 역할을 바꿔 한 번 더 한다.

```text
0:00  [권한 확인] → 권한 OK
0:10  [검색] → ESP32_BLE_FAKE1 줄 탭 → 연결 중 → 서비스 확인 중 → 준비됨
0:30  [제어 화면] → 3 입력 → LED 켜기·끄기 → on 3 / 응답 줄
0:50  [온습도 받기 시작] → 약 3초 → 이력 2줄 → 이력 줄 하나 탭(Toast) → [중지]
1:20  [뒤로] → [끊김 시험] → 끊김 + Toast + [재연결]
1:40  [재연결] → 준비됨
2:00  [해제] → 연결 안 됨
2:10  마무리 한 문장
```

| 회차 | 걸린 시간 | 빠진 장면 | 다음에 줄일 것 |
|---|---|---|---|
| 첫 번째 |  |  |  |
| 두 번째 |  |  |  |

- 실보드로 발표할 사람은 1:20 줄을 "제어 화면에서 받는 중에 보드 전원 끄기 → `상태: 끊김` + Toast → [뒤로] → 보드 전원 켜기 → 파랑 깜빡임 → [재연결]"로 바꿔 연습한다. 보드가 다시 켜지는 시간까지 재 둔다.
- 3분을 넘으면 LED는 켜기 한 번만, 이력 줄 탭은 빼고 줄인다.
- 코드 설명 질문 예는 [슬라이드 2일차 12–20분](slides.md)에 있다. 질문마다 열 파일과 줄 번호를 적어 둔다.

### 8. 오늘 확인할 것

- [ ] 입력 이력에 입력 이벤트(`입력=1`)와 온습도(`[24.5,40.0]`) 줄이 시각과 함께 쌓이고, 명령 로그에는 들어가지 않는다.
- [ ] [중지]를 누르면 온습도 줄이 더 늘지 않고, 홈에 갔다 오면 받기가 꺼져 있다.
- [ ] 이력 줄을 누르면 `받은 시각: … · 값: …` Toast가 뜬다.
- [ ] `끊김`이면 Toast와 [재연결]이 보이고, [재연결]로 `준비됨`까지 간다. 제어 화면에서 끊겨도 Toast가 뜬다.
- [ ] `delay(1000)`으로 시간 초과를 확인하고 `delay(10000)`으로 되돌렸다.
- [ ] 캡처 일곱 장을 찍었고, 2~3분 시연을 한 바퀴 했다.

## 2일차 — 2차 과제 발표 (60분)

| 시간 | 할 일 |
|---|---|
| 0–60분 | 순서표 차례대로 발표한다. 1인 5분 = 자리 잡기·보드 연결 확인 약 1분 + 시연 2~3분 + 코드 설명 질문 1분 |

인원이 많은 분반은 조교 평가자가 조를 나눠 동시에 듣는다([발표 정원 계산](project_brief.md#발표-정원-계산)). 조와 순서는 수업 공지를 따른다.

### 발표 순서와 규칙

1. 앞 사람이 발표하는 동안 내 앱을 실행해 첫 화면(`연결 안 됨`)에 두고, 코드 설명에 쓸 파일을 편집기 탭에 열어 둔다. 실보드로 하면 보드가 파랑 깜빡임인지 본다.
2. 차례가 되면 1일차 7번 순서대로 시연한다. 3분이 되면 평가자가 멈춘다.
3. 평가자가 고른 질문 한 개에 **파일 열기 → 줄 가리키기 → 한 문장**으로 답한다.
4. 앱을 닫고 다음 사람에게 넘긴다. 실보드는 전원을 끄거나 [해제]해서 다음 사람의 검색을 막지 않는다.

### 실보드가 안 될 때

- **먼저 손을 든다.** 조교가 시각·증상·Logcat `tag:BLE` 마지막 줄을 적는다.
- `useFake = true`로 바꿔 다시 실행하고 같은 순서로 시연한다. 끊김은 [끊김 시험]으로 만든다([따라하기 18단계](walkthrough.md#18-실보드가-안-될-때-fake로-바꾸기)).
- Fake에서 되면 앱은 정상이고 장비 문제다. Fake에서도 안 되면 내 코드 문제이며 장애가 아니다. 판단 기준은 [과제 안내](project_brief.md#실물-장비가-안-될-때--앱과-장비-나누기)에 있다.

### 발표를 마친 뒤

- 다른 사람 발표를 조용히 듣는다. 코드를 고치거나 보드에 연결하지 않는다.
- 레포트 PDF와 소스 압축 파일이 제출 칸에 올라갔는지 확인한다.

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 줄이다. 파일 이름 뒤의 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 기기에서 조금 다르게 보일 수 있다.

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

## 제출 — 레포트·소스·발표

1. **레포트 PDF**: [과제 안내의 레포트](project_brief.md#레포트) 다섯 절(실행 방법과 시연 절차, 필수 기능 캡처와 코드 위치, Logcat 근거, 오류 해결 기록, 확인 환경과 알려진 한계)
2. **소스 압축 파일**: 프로젝트의 `app/src/main` 폴더
3. **발표**: 2일차 순서표 차례에 1인 5분

파일 이름·제출 위치·마감은 [과제 안내](project_brief.md#레포트)와 수업 공지를 따른다. 주차별 실습 점수용 캡처는 없다. 1일차 실습지의 표는 스스로 점검하는 것이라 제출하지 않고 채점하지 않는다.
캡처와 발표 화면에 계정·알림 내용이 보이지 않게 한다.

## 먼저 끝났다면

- 1일차: 가로 버튼 줄의 [중지] 옆에 [이력 지우기] 버튼을 둔다. 누르면 `history.clear()` 뒤 어댑터에 알려 목록을 비운다(12주차 `devices.clear()`와 같은 모양).
- 1일차: 온습도 요청 간격을 5초로 바꿔 이력 시각이 5초씩 벌어지는지 확인하고 되돌린다.
- 1일차: 짝의 앱으로 [슬라이드 2일차](slides.md)의 코드 설명 질문을 서로 한 개씩 내 본다.
- 1일차: 보드와 실기기가 있으면 `useFake = false`로 온습도 2줄과 보드 전원 끄기 → `끊김` → [재연결]을 해 보고 캡처한다.

추가 과제는 선택 사항이며 2차 과제 점수에 더하거나 빼지 않는다.
