---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 13주차
footer: BLE 출력 제어 · 문자열 명령과 응답
---

# BLE 출력 제어: 문자열 명령과 응답

12주차에는 목록 줄을 눌러 보드와 `준비됨`까지 연결했습니다.
이번 주에는 그 연결로 **명령을 보내고**, 보드의 **대답을 받습니다.**

```text
상태: 준비됨                         보드
[3        ]  LED (●)   ──"on 3"──▶   LED 3 켜짐
명령 로그                ◀──JSON──
on 3
응답: {"result":"ok","ms":"led(s) on"}
```

보드가 없어도 `useFake = true`로 똑같이 연습합니다.

---

# 1일차 — 명령 보내고 응답 받기

`30분 설명·시연 → 60분 실습`

1. `listOf(0, 1, 2, 3).contains(index)` 미리 보기
2. bleuno 명령 규약: 명령 이름 + 띄어쓰기 + LED 번호
3. 특강의 write·notify가 `send`·`onMessage`로 감싸진 모습
4. Switch → `send`, `onStart`에서 응답 받기, `onStop`에서 풀기

---

## 1일차 · 0–5분 — 오늘 문법: listOf(0, 1, 2, 3).contains(index)

```kotlin
val index = 9
if (listOf(0, 1, 2, 3).contains(index)) {
    println("보낼 수 있는 번호: $index")
} else {
    println("허용되지 않는 번호: $index")
}
```

| `index` | `listOf(0, 1, 2, 3).contains(index)` |
|---|---|
| `3` | `true` |
| `9` / `-1` | `false` |

- 목록 안에 값이 **있으면** `true`. 괄호 안에는 목록과 **같은 종류**(숫자)를 넣습니다.
- `listOf`는 만든 뒤 바꾸지 않는 목록입니다. 앱에는 2일차에 넣습니다.

---

## 1일차 · 5–13분 ① — bleuno 명령 규약

| 보내는 글자 | 뜻 | 보드의 응답 |
|---|---|---|
| `on 3` | 3번 LED 켜기 | `{"result":"ok","ms":"led(s) on"}` |
| `off 3` | 3번 LED 끄기 | `{"result":"ok","ms":"led(s) off"}` |
| `off -1` | 모두 끄기 | `{"result":"ok","ms":"led(s) off"}` |
| `pwm 0 128` | 0번 밝기(0~255) | `{"result":"ok","ms":"pwm set"}` |
| `dht11` | 온도·습도 읽기(14주차) | `{"result":"ok","value":"[24.5,40.0]"}` |
| `on3`, `hello` | 모르는 명령 | `{"result":"fail","ms":"unknown command"}` |

- 규칙: **명령 이름 + 띄어쓰기 한 칸 + 번호.** 끝의 `\n`은 라이브러리가 붙입니다.
- 명령 **하나마다** JSON 응답이 **한 줄씩** 옵니다.
- 전체 표: [bleuno README 2절](../../bleuno/README.md#2-명령과-응답)

---

## 1일차 · 5–13분 ② — N은 LED 번호, 응답은 JSON 한 줄

| LED 번호 | 0 | 1 | 2 | 3 | -1 |
|---|---|---|---|---|---|
| 보드 핀 | GPIO4 | GPIO3 | GPIO1 | GPIO0 | 모두 |

- `on 3`의 `3`은 GPIO가 아니라 **LED 번호**입니다. 수업 보드 LED는 4개입니다.
- 보드는 번호가 범위 안인지 **검사하지 않습니다.** 앱이 보내기 전에 막아야 합니다(2일차).
- 오늘 1일차 코드에는 검사가 없습니다. `9`는 **Fake에서만**, 실보드에는 `0`~`3`만.

| `result` | 뜻 |
|---|---|
| `ok` / `err` / `fail` | 성공 / 명령은 맞는데 값이 틀림 / 모르는 명령 |

---

## 1일차 · 13–20분 ① — 특강의 write·notify가 send·onMessage로

```text
앱 (ControlActivity)        RealBleunoClient 안 (특강 코드)            보드
send("on 3")        ──▶  writeCharacteristic("on 3\n")        ──▶  LED 3 켜짐
                         onCharacteristicWrite → 다음 명령
onMessage { json } ◀──  onCharacteristicChanged (notify)     ◀──  {"result":"ok",…}
```

- 특강에서 직접 쓴 `writeCharacteristic`과 알림 콜백이 라이브러리 안에 **그대로** 있습니다.
- 우리는 **보낼 글자**와 **받은 글자**만 다룹니다. UUID·바이트 변환은 라이브러리 몫입니다.
- `onMessage`의 중괄호는 라이브러리가 **메인 스레드**에서 불러 줍니다(5주차 `Handler`).

---

## 1일차 · 13–20분 ② — write 큐: 명령은 하나씩 나간다

```text
send: 큐에 추가 "on 3" (대기 1개)
writeCharacteristic("on 3") 호출 결과=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","ms":"led(s) on"}
```

- BLE는 쓰기가 끝났다는 콜백(`onCharacteristicWrite`)이 와야 **다음 것**을 쓸 수 있습니다.
- 그래서 `send`는 명령을 **큐**에 넣고 차례대로 보냅니다. 빨리 누르면 `대기 2개`가 됩니다.
- Fake 로그: `writeCharacteristic(가짜): "on 3"` → 300ms 뒤 `onCharacteristicChanged(가짜): {…}`
- `준비됨`이 아닐 때 보낸 명령은 `send(가짜): 준비되지 않아 무시함`으로 **버려집니다.**

---

## 1일차 · 20–27분 ① — Switch를 켜면 send

```kotlin
} else if (isChecked) {
    val index = pin.toInt()
    Bleuno.client?.send("on $index")
    binding.logText.append("on $index\n")
} else {
    val index = pin.toInt()
    Bleuno.client?.send("off $index")
    binding.logText.append("off $index\n")
}
```

- 4주차 `append` 줄은 **보낸 명령 기록**으로 남기고, 그 위에 `send` 한 줄을 넣습니다.
- `Bleuno.client`는 12주차처럼 `null`일 수 있어 `?.`입니다. [전체 끄기]는 `send("off -1")`.
- 입력 칸 id는 4주차 `pinEdit` 그대로, 뜻은 **LED 번호**입니다. `maxLength="2"`로 두 글자까지.

---

## 1일차 · 20–27분 ② — onStart에서 응답 받기

```kotlin
override fun onStart() {
    super.onStart()
    Bleuno.client?.onMessage { json ->
        val result = BleunoMessage.result(json)
        if (result != null) {
            binding.logText.append("응답: $json\n")
        }
    }
}
```

- `json`은 보드가 보낸 글자 한 줄입니다. `"응답: $json"`으로 **그대로** 붙입니다.
- `BleunoMessage.result(json)`: `"result"` 값. 없으면 `null`입니다.
- Fake는 `준비됨`이면 10초마다 `{"event":"input",…}`을 보냅니다. `result`가 없어 **건너뜁니다**(14주차).

---

## 1일차 · 20–27분 ③ — onStop에서 풀기와 들어가는 길

```kotlin
override fun onStop() {
    super.onStop()
    Bleuno.client?.onMessage(null)
}
```

- 10주차 Receiver 짝 규칙: **`onStart`에서 등록 ↔ `onStop`에서 해제.**
- 두 함수는 onCreate의 `}` **밖**, 클래스 안입니다. 안에 넣으면 빌드 오류가 납니다.
- 제어 화면은 **목록 줄 탭 → `준비됨` → [제어 화면]**으로 들어갑니다.
- 연결되지 않은 채 들어오면(목록 줄 안 누름, [해제] 뒤 [연결]) `연결 안 됨`이라 명령이 버려집니다.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--명령-보내고-응답-받기-60분) · [따라하기](walkthrough.md#1일차)

1. `strings.xml`·`activity_control.xml`: 입력 칸 문구, `maxLength`, [전체 끄기] 자리
2. Switch 리스너에 `send`, Logcat `tag:BLE`에서 보낸 글자와 응답 확인
3. `onStart`/`onStop`에서 응답 받기·풀기 → 로그에 `응답: {…}`
4. [전체 끄기] `off -1` → 캡처 1(보드가 있으면 LED 사진)

**설명 합계: 5+8+7+7+3 = 30분**

캡처는 제어 화면에 **들어온 직후 첫 조작**에서 찍습니다. 로그 칸이 차면 새 줄이 안 보입니다.

---

# 2일차 — 막고, 알리고, 색으로 보이기

`30분 설명·시연 → 60분 실습`

1. 허용 번호 검사: `9`는 보내지 않고 Toast
2. `준비됨`일 때만, 보낸 직후 300ms는 버튼 막기
3. `result`가 `ok`가 아니면 AlertDialog와 `colors.xml` 빨간 로그
4. (확장) `SeekBar`로 `pwm 0 V`, 2차 과제 공지

---

## 2일차 · 0–6분 ① — 보내기 전에 번호 확인

```kotlin
if (pin.isEmpty()) {
    Toast.makeText(this, "LED 번호를 입력하세요", Toast.LENGTH_SHORT).show()
} else if (isAllowedIndex(pin.toInt()) == false) {
    Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
} else if (isChecked) {
    // 1일차 5번: send("on $index")
```

- 순서: **빈 칸 → 허용 번호 → 켜기/끄기.** 빈 글자를 `toInt()`하면 앱이 멈추므로 빈 칸이 먼저입니다.
- 걸리면 명령도 로그도 없습니다. Logcat에 `writeCharacteristic` 줄이 **안 생기는 것**이 증거입니다.
- `== false`는 12주차처럼 "아니면"입니다.

---

## 2일차 · 0–6분 ② — isAllowedIndex()로 묶기

```kotlin
private fun isAllowedIndex(index: Int): Boolean {
    if (listOf(0, 1, 2, 3).contains(index)) {
        return true
    }
    if (index == -1) {
        return true
    }
    return false
}
```

- 10주차 `hasBlePermissions()`처럼 **참/거짓을 돌려주는** 함수입니다. 클래스 끝에 둡니다.
- `-1`(전체)도 약속된 번호라 허용합니다. 입력 칸은 `-`를 못 적어 [전체 끄기]만 보냅니다.
- `contains(pin)`처럼 **글자**를 넣으면 `Type inference failed …` 오류가 납니다. `pin.toInt()`.

---

## 2일차 · 6–14분 ① — 준비됨일 때만 누를 수 있게

```kotlin
Bleuno.client?.connectionState?.collect { state ->
    binding.stateText.text = "상태: $state"
    binding.ledSwitch.isEnabled = false
    binding.allOffButton.isEnabled = false
    if (state == ConnState.READY) {
        binding.ledSwitch.isEnabled = true
        binding.allOffButton.isEnabled = true
    }
}
```

- 12주차 4번 collect 안에 넣습니다. MainActivity 8번처럼 **먼저 끄고, 준비됨이면 켭니다.**
- XML의 `ledSwitch`·`allOffButton`에 `android:enabled="false"`: 상태가 오기 전에도 꺼져 있게.
- 1일차에 보았던 "`준비되지 않아 무시함`"이 더는 생기지 않습니다.

---

## 2일차 · 6–14분 ② — 보낸 직후 300ms 쉬기

```kotlin
private fun pauseButtons() {
    binding.ledSwitch.isEnabled = false
    binding.allOffButton.isEnabled = false
    lifecycleScope.launch {
        delay(300)
        if (Bleuno.client?.isReady == true) {
            binding.ledSwitch.isEnabled = true
            binding.allOffButton.isEnabled = true
        }
    }
}
```

- 5주차 `isEnabled` + 6주차 `launch { delay() }`. `send` 세 곳 뒤에서 `pauseButtons()`를 부릅니다.
- 300ms 사이 끊겼으면 다시 켜지 않습니다. `?. … == true`는 7주차 `scanJob?.isActive == true` 모양.

---

## 2일차 · 14–22분 ① — colors.xml과 R.color

```xml
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
</resources>
```

```kotlin
binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
```

- `app › res › values › colors.xml`은 새 프로젝트에 이미 있습니다. **두 줄만** 더합니다.
- `strings.xml` → `R.string`처럼 `colors.xml` → `R.color`. `#AARRGGBB`, 앞 `FF`는 불투명.
- 로그 칸 **전체** 글자색이 바뀝니다. 한 줄만 바꾸는 방법은 다루지 않습니다.

---

## 2일차 · 14–22분 ② — result가 ok가 아니면 AlertDialog

```kotlin
if (result != "ok") {
    val message = BleunoMessage.message(json) ?: ""
    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_error))
    AlertDialog.Builder(this)
        .setTitle("보드가 오류를 알렸습니다")
        .setMessage("응답: $result · $message")
        .setPositiveButton("확인", null)
        .show()
} else {
    binding.logText.setTextColor(ContextCompat.getColor(this, R.color.log_ok))
}
```

- 1일차 `if (result != null)` 안, `append` 아래에 넣습니다. `err`·`fail` 둘 다 이 가지.
- `message`는 `String?`이라 3주차 `?:`. 응답은 `onStart`~`onStop` 사이에만 오므로 창을 띄워도 됩니다.

---

## 2일차 · 14–22분 ③ — 오류를 일부러 만들어 확인하기

정상 흐름에서는 `ok`만 옵니다. **한 곳만** 바꿔 오류 응답을 만들고, 확인한 뒤 되돌립니다.

```kotlin
Bleuno.client?.send("on$index")     // 띄어쓰기를 뺐다 (확인 뒤 "on $index"로 되돌리기)
```

```text
로그   on 3
       응답: {"result":"fail","ms":"unknown command"}      ← 빨간색
창     보드가 오류를 알렸습니다 / 응답: fail · unknown command
Logcat writeCharacteristic(가짜): "on3"
```

- 앱 로그에는 `on 3`이지만 **실제로 보낸 글자**는 Logcat의 `"on3"`입니다.
- 제어 화면에 들어온 직후 첫 조작으로 확인합니다. [전체 끄기]의 `ok`로 다시 초록이 됩니다.

---

## 2일차 · 22–26분 — (확장) SeekBar로 pwm 0 V

```kotlin
binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
    override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) { }
    override fun onStartTrackingTouch(seekBar: SeekBar?) { }
    override fun onStopTrackingTouch(seekBar: SeekBar?) {
        val value = binding.pwmSeekBar.progress
        Bleuno.client?.send("pwm 0 $value")
        binding.logText.append("pwm 0 $value\n")
        pauseButtons()
    }
})
```

- 10주차 `object : BroadcastReceiver()`와 같은 익명 객체 틀. 함수 **세 개**를 모두 적습니다.
- 끄는 동안마다 보내면 큐에 수십 개가 쌓입니다. **손을 뗄 때** 한 번. XML `android:max="255"`.

---

## 2일차 · 26–30분 — 2차 과제 공지와 이제 직접 해 보기

[2일차 실습](lab.md#2일차--번호-검사와-오류-표시-60분) · [따라하기](walkthrough.md#2일차)

- **2차 과제**: 14주차 2일차 발표. Smart I/O Controller 2~3분 시연 + 레포트
- 필수: 권한 안내 · 검색·연결·해제·상태 · **출력 제어 1개 이상** · 입력 수신 · 끊김·연결 시간 제한 안내와 재시도 · 명령 규약
- 팀 구성·발표 순서·채점표는 수업 공지로 따로 안내합니다.

1. `colors.xml` 두 색 → 허용 번호 검사 → 캡처 2(`9`와 Toast)
2. `enabled="false"`와 13번 collect, `pauseButtons()`
3. 16번 오류 표시 → `"on$index"`로 확인하고 되돌리기 → 제출

**설명 합계: 6+8+8+4+4 = 30분**

---

## 제출하기

2일차가 끝나면 한 번 제출합니다.

1. **`ControlActivity.kt`**, **`activity_control.xml`**
2. **캡처 1**: `상태: 준비됨`, 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`
3. **캡처 2**: 입력 칸 `9`, Toast `허용되지 않는 번호`, 로그에 `on 9` 없음
4. **사진**: 번호 3 LED가 켜진 보드(보드·실기기가 없으면 생략)

---

## 다음 주 미리 보기

오늘 `result != null`로 **건너뛴** 줄이 있었습니다. `{"event":"input","index":0,"value":1}`

14주차에는 이 입력 이벤트와 `dht11` 온도·습도 응답을 **받아서 목록에 쌓고**,

보드 전원이 꺼져 `끊김`이 되면 [재연결]합니다. 그리고 2차 과제를 발표합니다.
