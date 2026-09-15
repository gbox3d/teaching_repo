---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 14주차
footer: 입력 수신·끊김·재연결과 2차 과제 발표
---

# 입력 수신·끊김·재연결과 2차 과제 발표

13주차에는 보드에 **보내고** 대답을 받았습니다.
이번 주에는 보드에서 **받아 쌓고**, 끊기면 **다시 연결**합니다.

```text
입력 이력                      연결 화면
12:00:03 [24.5,40.0]           끊김
12:00:06 [25.0,41.0]           [다시 시도]
12:00:10 입력=1                [재연결] [끊김 시험]
```

2일차에는 지금까지 만든 Smart I/O Controller로 **2차 과제**를 발표합니다.

---

# 1일차 — 입력 받기·끊김·재연결

`30분 설명·시연 → 60분 구현과 시연 리허설`

1. `split(" ")`·`[0]`·`[1]`와 `BleunoMessage.value/event`
2. `dht11`을 3초마다 보내고 입력 이력에 쌓기
3. `끊김`이면 알리고 [재연결]
4. 10초 안에 `준비됨`이 아니면 시간 초과 안내
5. 발표 준비와 코드 설명 질문 예고

---

## 1일차 · 0–5분 ① — 오늘 문법: split(" ")과 [0]·[1]

```kotlin
val line = "12:00:03 [24.5,40.0]"
val parts = line.split(" ")
println(parts[0])
println(parts[1])
```

| 식 | 결과 |
|---|---|
| `line.split(" ")` | `[12:00:03, [24.5,40.0]]` — 띄어쓰기마다 자른 목록 |
| `parts[0]` / `parts[1]` | `12:00:03` / `[24.5,40.0]`. 번호는 **0부터** |
| `parts[2]` | 칸이 없다 → 실행하면 앱이 멈춘다 |

- `parts[0]`은 12주차 `addresses.get(position)`의 `get`과 같은 "번호로 꺼내기"입니다.

---

## 1일차 · 0–5분 ② — 제공 helper로 JSON에서 값 꺼내기

| 받은 JSON | `BleunoMessage.event(json)` | `BleunoMessage.value(json)` |
|---|---|---|
| `{"event":"input","index":0,"value":1}` | `"input"` | `"1"` |
| `{"result":"ok","value":"[24.5,40.0]"}` | `null` | `"[24.5,40.0]"` |
| `{"result":"ok","ms":"led(s) on"}` | `null` | `null` |

- 13주차 `BleunoMessage.result(json)`과 같은 모양입니다. 키가 없으면 `null`.
- JSON은 `split`으로 자르지 않습니다. **제공 helper**로 꺼냅니다.
- 입력 이벤트에도 `"value"`가 있습니다. 그래서 `event`를 **먼저** 봅니다.
- 입력 이벤트는 가짜 보드만 10초마다 보냅니다. 실보드는 `dht11` 응답으로 받습니다.

---

## 1일차 · 5–13분 ① — dht11을 3초마다 보내기

```kotlin
binding.inputStartButton.setOnClickListener {
    binding.inputStartButton.isEnabled = false
    binding.inputStopButton.isEnabled = true
    inputJob = lifecycleScope.launch {
        while (isActive) {
            Bleuno.client?.send("dht11")
            delay(3000)
        }
    }
}
```

- 6주차 `scanJob = lifecycleScope.launch { }` 모양. `while (isActive)` = 취소되지 않았으면 되풀이.
- [중지]·끊김·`onStop`에서 `stopInput()` → `inputJob?.cancel()`. 받지 못하는 동안은 보내지도 않습니다.

---

## 1일차 · 5–13분 ② — 받은 줄을 세 갈래로 가르기

```kotlin
val result = BleunoMessage.result(json)
val event = BleunoMessage.event(json)
val value = BleunoMessage.value(json)
if (event == "input") {
    addHistory("입력=$value")
} else if (value != null) {
    addHistory(value)
} else if (result != null) {
    binding.logText.append("응답: $json\n")
    // … 13주차 오류 색·AlertDialog 그대로
}
```

- 입력 이벤트 → 이력 `입력=1` / `dht11` 응답 → 이력 `[24.5,40.0]` / 명령 응답 → 명령 로그
- 순서를 바꾸면 이벤트가 `12:00:10 1`로 들어갑니다. 빌드는 되니 더 찾기 어렵습니다.

---

## 1일차 · 5–13분 ③ — 시각을 붙여 입력 이력에 쌓기

```kotlin
private fun addHistory(text: String) {
    val time = SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())
    history.add("$time $text")
    historyAdapter.notifyDataSetChanged()
}
```

```xml
<ListView
    android:id="@+id/inputList"
    android:transcriptMode="alwaysScroll" />
```

- `SimpleDateFormat(…).format(Date())`: 지금 시각을 `12:00:03`으로 만드는 **틀**. `Date`는 `java.util.Date`.
- 11주차 장치 목록 틀 그대로: `mutableListOf` → `ArrayAdapter` → `add` → `notifyDataSetChanged()`.
- `history`는 onStart에서도 쓰므로 클래스 안에 둡니다. 회전하면 빈 목록으로 다시 시작합니다.

---

## 1일차 · 13–19분 ① — 끊김이면 알리고 [재연결] 보이기

```kotlin
ConnState.LOST -> {
    binding.scanButton.isEnabled = true
    binding.retryButton.visibility = View.VISIBLE
    binding.reconnectButton.visibility = View.VISIBLE
    showLostToast()
}
```

```kotlin
private fun showLostToast() {
    Toast.makeText(this, "연결이 끊겼습니다. [재연결]을 누르세요", Toast.LENGTH_SHORT).show()
}
```

- 12주차 7번 collect의 `LOST` 가지에 두 줄을 더합니다. [재연결]은 끊김일 때만 보입니다.
- collect 틀 안의 `this`는 화면이 아닙니다. Toast는 **화면의 함수**로 빼서 부릅니다.

---

## 1일차 · 13–19분 ② — 주소를 저장해 두고 [재연결]

```kotlin
// 목록 줄을 누를 때(43번): 담고 저장
lastAddress = address
getSharedPreferences("smartio", MODE_PRIVATE).edit().putString("lastAddress", address).apply()
// onCreate(48번): 꺼내기
lastAddress = prefs.getString("lastAddress", "") ?: ""
// [재연결] 버튼 리스너(47번): 연결
client.connect(lastAddress)
```

- 목록 줄을 누를 때 저장, onCreate에서 꺼내기, [재연결]에서 연결합니다(11주차 틀).
- 변수에만 두면 회전하면 `""`로 돌아갑니다. 저장해 두면 앱을 껐다 켜도 남습니다.
- 끊김 Toast는 회전·[뒤로]·홈에서 돌아올 때 **또 뜹니다**. StateFlow가 마지막 값을 다시 줍니다.
- 실보드는 전원을 끕니다. Fake는 (시험용) [끊김 시험]: `val fake = client as FakeBleunoClient` → `fake.simulateLost()`
- 제어 화면에서 끊기면 Toast `연결이 끊겼습니다. [뒤로] → [재연결]을 누르세요`.

---

## 1일차 · 19–25분 ① — 10초 연결 시간 제한 걸기

```kotlin
private fun startConnectTimeout() {
    connectTimeoutJob?.cancel()
    connectTimeoutJob = lifecycleScope.launch {
        waitConnectTimeout()
    }
}
```

- 연결을 시작하는 두 곳(목록 줄 탭, [재연결])에서 부릅니다.
- 6주차 `scanJob = lifecycleScope.launch { countDown() }`와 같은 모양입니다.
- 앞 예약을 먼저 `cancel()`해서 앞 연결의 10초가 새 연결을 끊지 않게 합니다.
- 회전하면 예약이 화면과 함께 사라지므로, onCreate에서 아직 `연결 중`이면 다시 겁니다.

---

## 1일차 · 19–25분 ② — 10초 뒤에도 연결 중이면 안내하고 끊기

```kotlin
private suspend fun waitConnectTimeout() {
    delay(10000)
    val state = client.connectionState.value
    if (listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)) {
        Toast.makeText(this, "연결 시간이 초과되었습니다", Toast.LENGTH_SHORT).show()
        client.disconnect()
        binding.stateText.text = "연결 시간 초과 — [다시 시도]를 누르세요"
        // … ProgressBar 숨기기, [검색] 켜기, [다시 시도] 보이기
    }
}
```

- `연결 중`·`서비스 확인 중`일 **때만**. `끊김`·`준비됨`이 된 화면은 덮지 않습니다.
- 함수 안의 `this`는 화면이라 Toast를 씁니다. `delay`가 있으니 `suspend`, `10000`은 밀리초.
- Fake는 2초 만에 `준비됨` → 확인은 `delay(1000)`으로 잠깐 바꿔 보고 되돌립니다.

---

## 1일차 · 25–30분 ① — 발표 준비와 코드 설명 질문 예고

| 2차 과제 | 내용 |
|---|---|
| 필수 기능 | 권한 안내 · 검색·연결·해제·상태 · 출력 1개 이상 · 입력 수신 · 끊김·시간 초과 안내와 재시도 · 명령 규약 · 2~3분 시연 절차 |
| 발표 | 1인 **5분** = 자리 잡기·보드 연결 확인 + 시연 2~3분 + 코드 설명 질문 1개 |
| 점수 | 발표 12 + 레포트 8 = 20 · [과제 안내](project_brief.md) · [채점표](rubric.md) |

코드 설명 질문 예 — **파일 열기 → 줄 가리키기 → 한 문장**

- [중지]를 누르면 반복이 멈추는 까닭은? / 입력 이벤트가 숫자 한 줄로 들어가지 않는 까닭은?
- 회전해도 [재연결]이 같은 주소를 쓰는 까닭은? / 10초가 넘으면 어느 줄이 알리나?

---

## 1일차 · 25–30분 ② — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--입력-받기끊김재연결과-시연-리허설-60분) · [따라하기](walkthrough.md#1일차)

1. 제어 화면: 입력 이력 자리 → 받은 줄 가르기 → [온습도 받기 시작]·[중지]
2. 연결 화면: 주소 저장·[재연결]·(시험용) [끊김 시험] → 제어 화면 끊김 Toast
3. 시간이 남으면: 이력 줄 `split` Toast → 연결 시간 제한(`delay(1000)`으로 확인하고 되돌리기)
4. 47분: 캡처 세트, 2~3분 시연 한 바퀴

**설명 합계: 5+8+6+6+5 = 30분**

**47분까지 반드시 1·2.** 3은 늦으면 미룹니다. 시간 제한은 필수 기능이라 발표 전까지 넣습니다.
구현이 늦어도 47분에는 멈추고 리허설을 한 번 합니다. 발표 전까지 자기 프로젝트에서 마무리합니다.

---

# 2일차 — 2차 과제 발표

`30분 발표 안내·점검 → 60분 발표`

1. 오늘 진행 순서와 발표 정원
2. 채점표 다시 보기: 발표 12 + 레포트 8
3. 코드 설명 질문 미리 보기
4. 발표 전 점검, 실보드가 안 될 때 Fake로 → 발표 시작

---

## 2일차 · 0–5분 — 오늘 진행 순서와 발표 정원

| 순서 | 할 일 | 시간 |
|---|---|---|
| 1 | 앞 사람 발표 중에 앱을 첫 화면에, 보드는 파랑 깜빡임으로 | 기다리는 동안 |
| 2 | 자리 잡기·보드 연결 확인 | 약 1분 |
| 3 | 시연: 권한 → 목록 → 준비됨 → LED → 입력 3줄 → 끊김 → [재연결] → [해제] | 2~3분 |
| 4 | 코드 설명 질문 한 개 | 1분 |

```text
발표 시간 = ceil(N / E) × 5분 ≤ 60분      N = 발표 인원, E = 동시에 듣는 평가자 수
예) N = 24, E = 2 → 12 × 5 = 60분
예) N = 30, E = 2 → 15 × 5 = 75분 → 조교 평가자를 늘려 E = 3 → 10 × 5 = 50분
```

---

## 2일차 · 5–12분 — 채점표 다시 보기: 발표 12 + 레포트 8

| 발표 항목 | 점수 | 레포트 항목 | 점수 |
|---|---|---|---|
| 연결 흐름(권한·목록·상태·해제) | 3 | 실행 방법과 시연 절차 | 2 |
| 출력 제어와 명령 규약 | 2 | 필수 기능 캡처와 코드 위치 | 3 |
| 입력 수신과 입력 이력 | 2 | Logcat 근거 | 1 |
| 끊김·재연결·시간 제한 | 2 | 오류 해결 기록 | 1 |
| 코드 설명(개인 구술) | 3 | 확인 환경과 알려진 한계 | 1 |

- 시연은 3분에서 멈춥니다. 못 보인 장면은 레포트 캡처로 보되 그 항목은 **최대 절반**입니다(시간 초과는 레포트 캡처로도 만점).
- 장비 장애(조교 기록)로 못 보인 장면은 Fake 시연이나 캡처로 만점까지 봅니다.
- Fake와 실보드는 같은 기준으로 봅니다. 같은 원인으로 두 번 깎지 않습니다.

---

## 2일차 · 12–20분 — 코드 설명 질문은 이렇게 나온다

| 질문 예 | 가리킬 곳 |
|---|---|
| [중지]를 누르면 반복이 멈추는 까닭은? | `inputJob = lifecycleScope.launch {`와 `stopInput()`의 `inputJob?.cancel()` |
| 입력 이벤트와 온습도 응답을 어떻게 가르나? | `if (event == "input")` → `else if (value != null)` 순서 |
| 이력 한 줄에서 시각만 꺼내는 줄은? | `history[position].split(" ")`과 `parts[0]` |
| 끊겼을 때 [재연결]이 보이게 되는 줄은? | 연결 상태 collect의 `ConnState.LOST ->` 가지 |
| 연결이 10초를 넘으면 무엇이 알리나? | `waitConnectTimeout()`의 `delay(10000)`과 `contains(state)` |
| Toast를 collect 안에 바로 쓰지 않은 까닭은? | `showLostToast()` 함수와 collect 틀의 `this` |

답하는 순서: **파일 열기 → 줄 가리키기 → 한 문장**. "원래 이렇게 돼요"는 점수가 되지 않습니다.

---

## 2일차 · 20–27분 — 발표 전 점검과 실보드가 안 될 때

- [ ] 저장 → `Run ▶` 다시 실행, 앱은 첫 화면(`연결 안 됨`)
- [ ] `useFake`가 오늘 시연 방법(실보드 `false` / 에뮬레이터 `true`)과 맞다
- [ ] Logcat `package:mine tag:BLE`를 켜 두고, 편집기에 두 Activity 탭을 열어 두었다
- [ ] 레포트에 입력 3줄·끊김+[재연결]·시간 초과 캡처가 있다

실보드가 안 되면: **손 들기** → 조교가 시각·증상·Logcat 마지막 줄을 적는다 → `useFake = true`로 바꿔 같은 순서로 시연

Fake에서 되면 앱은 정상, 장비 문제입니다(장애 기록). Fake에서도 안 되면 내 코드 문제입니다.

---

## 2일차 · 27–30분 — 발표 시작

[2일차 실습](lab.md#2일차--2차-과제-발표-60분) · [따라하기](walkthrough.md#2일차)

1. 첫 순서 세 사람은 앱과 보드를 켜 두고 기다립니다.
2. 발표를 마친 사람은 조용히 듣고, 레포트와 소스 제출을 확인합니다.
3. 장비가 멈추면 손을 듭니다. 내 코드 때문에 앱이 꺼지는 것은 장애가 아닙니다.

**설명 합계: 5+7+8+7+3 = 30분**

---

## 제출하기

2차 과제는 세 가지를 냅니다([과제 안내의 레포트](project_brief.md#레포트)).

1. **레포트 PDF**: 실행 방법과 시연 절차, 필수 기능 캡처와 코드 위치, Logcat 근거, 오류 해결 기록, 확인 환경과 알려진 한계
2. **소스 압축 파일**: 프로젝트의 `app/src/main` 폴더
3. **발표**: 2일차 1인 5분

---

## 다음 주 미리 보기

15주차는 **기말고사(개인 실기)**입니다.

- 공개 starter(화면 / 제공 `bleuno/` / 상수) 위에 세 기능: 권한 확인 흐름, 번호 토글(`send`)과 응답 표시, 연결 시간 제한 안내
- 1일차 실습은 리허설, 2일차는 본시험과 개인 시연·구술 질문입니다.
