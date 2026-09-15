# 13주차 실습 — 보드에 명령 보내고 응답 받기

이번 주에는 12주차 `SmartIO`의 제어 화면에서 LED Switch가 보드에 진짜 명령을 보내고, 보드의 JSON 응답을 로그에 쌓게 만든다. 2일차에는 보내면 안 되는 번호와 준비되지 않은 상태를 앱이 막고, 오류 응답을 창과 색으로 보여 준다.
처음에는 예제를 그대로 옮기고, 실행에 성공하면 한 곳씩 바꿔 가며 앱 로그와 Logcat `tag:BLE`가 어떻게 달라지는지 직접 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다. 보드가 없는 학생은 `useFake = true`(Fake) 그대로 끝까지 할 수 있다.

이번 주에 고치는 파일은 제어 화면 쪽뿐이다: `ControlActivity.kt`, `activity_control.xml`, `strings.xml`, (2일차) `colors.xml`. `MainActivity.kt`는 12주차 그대로 둔다.
제어 화면에는 **목록 줄 탭 → `준비됨` → [제어 화면]**으로 들어간다. 연결(`준비됨`)이 안 된 채로 제어 화면에 들어오면(목록 줄을 누르지 않았거나 [해제]한 뒤 [연결]로 들어옴) 상태가 `연결 안 됨`이라 명령이 버려진다.

## 1일차 — 명령 보내고 응답 받기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 12주차 `SmartIO`를 실행해 [제어 화면]까지 들어가 본다. `strings.xml`의 입력 칸 문구를 바꾸고 `activity_control.xml`에 `maxLength`와 [전체 끄기] 자리를 만든다 |
| 10–25분 | LED Switch 리스너에서 `send`로 명령을 보낸다. Logcat `tag:BLE`에서 보낸 글자와 보드 응답을 확인한다 |
| 25–40분 | `onStart`에서 응답을 받아 로그에 쌓고 `onStop`에서 푼다. 관찰표를 채운다 |
| 40–50분 | [전체 끄기]에서 `off -1`을 보내고, 홈에 갔다 와도 응답이 찍히는지 확인한다 |
| 50–60분 | 캡처 1을 찍는다. 보드와 실기기가 있으면 `useFake = false`로 LED를 켜고 사진을 찍는다 |

### 1. 제어 화면 자리 만들기

1. 앱을 실행하고 [검색] → `ESP32_BLE_FAKE1` 줄 누르기 → `준비됨` → [제어 화면]으로 들어간다. 상단에 `상태: 준비됨`이 보이면 시작할 수 있다. `3`을 넣고 Switch를 켜면 로그에 `on 3`만 쌓인다(아직 보드에 보내지 않는다).
2. `strings.xml`에서 `pin_hint`의 **값**만 `LED 번호 (0~3)`으로 바꾸고, `state_unknown` 아래에 `all_off`(`전체 끄기`)를 넣는다. 이름 `pin_hint`와 id `pinEdit`는 그대로 둔다.
3. `activity_control.xml`에서 `pinEdit`의 `android:inputType="number"` 아래에 `android:maxLength="2"`를 넣는다.
4. `ledSwitch` **아래**·`명령 로그` 제목 **위**에 id가 `allOffButton`인 버튼(글자 `@string/all_off`, 위 간격 `16dp`)을 넣는다.
5. 실행해 입력 칸 힌트 `LED 번호 (0~3)`과 [전체 끄기]가 보이고, `123`을 치면 `12`까지만 들어가면 다음으로 간다.

막히면 [따라하기 2단계](walkthrough.md#2-입력-칸-문구와-전체-끄기-자리-만들기)를 본다.

### 2. Switch에서 명령 보내기

`ControlActivity.kt`의 `// 2.` LED Switch 리스너를 아래 모양으로 채운다. 빈 칸 Toast 문구도 `LED 번호를 입력하세요`로 바꾼다.

```kotlin
binding.ledSwitch.setOnCheckedChangeListener { _, isChecked ->
    val pin = binding.pinEdit.text.toString()
    if (pin.isEmpty()) {
        // Toast "LED 번호를 입력하세요"
    } else if (isChecked) {
        // pin을 숫자로 바꿔 index에 담는다 (4주차 toInt)
        // Bleuno.client에 "on 번호" 명령을 보낸다 (띄어쓰기 한 칸, ?.)
        // 보낸 명령을 로그에 append (4주차 그대로)
    } else {
        // 같은 모양으로 "off 번호"
    }
}
```

- Logcat 필터를 `package:mine tag:BLE`로 두고 `3` → Switch 켜기를 한다. `writeCharacteristic(가짜): "on 3"` 다음 줄에 무엇이 찍히는지 적는다.
- 앱 로그에는 아직 `on 3`만 있다. 보드는 답했는데 화면이 받지 않는 상태다. 3번에서 받는다.
- 명령 글자의 모양은 [bleuno README 2절](../../bleuno/README.md#2-명령과-응답)의 표를 본다. 막히면 [1일차 완성 코드](examples/day1/ControlActivity.kt)와 한 줄씩 비교한다.

### 3. 응답 받기: onStart에서 등록, onStop에서 해제

1. onCreate를 닫는 `}` **아래**, 클래스를 닫는 `}` **위**에 두 함수를 만든다.

```kotlin
override fun onStart() {
    super.onStart()
    // Bleuno.client?.onMessage { json -> … } 로 받기를 등록한다
    // BleunoMessage.result(json)이 null이 아니면 "응답: $json" 한 줄을 로그에 append
}

override fun onStop() {
    super.onStop()
    // 받기를 푼다: Bleuno.client?.onMessage(null)
}
```

2. `BleunoMessage`가 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 `com.example.smartio.bleuno.BleunoMessage`를 import한다.
3. 실행하고 [제어 화면]에 들어온 직후부터 표를 채운다.

| 조작 | 예상 앱 로그 | 실제 앱 로그 | Logcat `tag:BLE` 새 줄 |
|---|---|---|---|
| `3` → Switch 켜기 |  |  |  |
| Switch 끄기 |  |  |  |
| 입력 칸을 비우고 Switch 켜기 |  |  |  |
| `준비됨`에서 15초 그대로 두기 |  |  |  |
| (Fake에서만) 빈 칸 그대로 Switch 끄기 → `9` → Switch 켜기 |  |  |  |
| [뒤로] → [해제] → [연결]로 들어와 `3` → Switch 켜기 |  |  |  |

- `9` 같은 번호는 **Fake에서만** 해 본다. 실보드(`useFake = false`)에서는 `0`~`3`만 넣는다. 보드는 번호를 검사하지 않아 범위 밖 번호에 어떻게 동작할지 알 수 없다(2일차에 앱이 막는다).
- 15초 두는 동안 Logcat에만 찍히고 앱 로그에는 안 들어오는 줄이 있다. 그 줄에 `result`가 있는지 보고, 9번 `if (result != null)`이 왜 필요한지 한 문장으로 적는다.
- 마지막 줄에서 응답이 없는 까닭을 Logcat의 경고 줄(`W`)을 읽고 적는다.

### 4. [전체 끄기]와 짝 규칙 확인

1. `// 4.` collect 블록 **아래**(onCreate 안 끝)에 [전체 끄기] 리스너를 만든다. 번호 자리에 `-1`을 넣은 `off -1`을 보내고, 보낸 글자를 로그에 쌓는다.
2. 다시 실행해 [검색] → 목록 줄 탭 → `준비됨` → [제어 화면]으로 들어온다. 3번 표 마지막 줄 뒤라 연결이 끊긴 상태이기 때문이다.
3. 아래 순서로 조작하고 표를 채운다.

| 조작 | 앱 로그 새 줄 | LED Switch 모양 |
|---|---|---|
| `3` → Switch 켜기 → [전체 끄기] |  |  |
| 홈 버튼 → 앱으로 돌아오기 → Switch 끄기 |  |  |

- 홈에 갔다 왔는데도 응답이 찍히는 까닭을 `onStop`·`onStart` 두 낱말로 한 문장 적는다.
- `onMessage { }` 등록을 `onStart`가 아니라 `onCreate`에 두면 홈에 갔다 온 뒤 어떻게 될지 예상만 적어 본다(바꾸지 않는다).
- [전체 끄기] 뒤에도 Switch가 켜진 모양으로 남는다. 코드가 틀린 것이 아니다.

### 5. 캡처 1과 보드 사진

1. [뒤로] → [제어 화면]으로 다시 들어온다(새 화면이라 로그가 비어 있다). `3` → Switch 켜기 → 로그에 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`이 보이면 **세로 화면을 캡처한다(캡처 1).** JSON 줄은 두 줄로 접혀도 된다.
2. 보드와 실기기가 있으면 `MainActivity.kt`의 `private val useFake = true`를 `false`로 바꾸고 실기기로 실행한다. 보드에 연결해 `3` → Switch 켜기 → **번호 3 LED(GPIO0)가 켜진 보드를 사진으로 찍는다.**
3. 실보드에서 Switch를 빠르게 여러 번 켰다 껐다 하며 Logcat의 `send: 큐에 추가 … (대기 N개)` 줄을 본다.

| 항목 | 내 보드 |
|---|---|
| `3` → 켜기 뒤 켜진 LED 위치 |  |
| 가장 크게 본 `대기 N개`의 N |  |

- 로그 칸은 스크롤이 없어 명령을 몇 번 보내면 새 줄이 아래로 밀려 안 보인다. 캡처는 들어온 직후 첫 조작에서 찍는다.
- 에뮬레이터로 돌아갈 때는 `useFake = true`로 되돌린다.

### 6. 오늘 확인할 것

- [ ] 입력 칸 힌트가 `LED 번호 (0~3)`이고 두 글자까지만 들어간다.
- [ ] `3` → Switch 켜기 → 로그 `on 3` 뒤에 `응답: {"result":"ok","ms":"led(s) on"}`이 쌓인다.
- [ ] [전체 끄기] → `off -1`과 `응답: {"result":"ok","ms":"led(s) off"}`.
- [ ] 홈에 갔다 와도 응답이 찍힌다. `준비됨`에서 가만히 두어도 앱 로그에 새 줄이 생기지 않는다.
- [ ] 캡처 1을 찍었다(보드가 있으면 사진도).

프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 번호 검사와 오류 표시 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 코드를 실행하고 `colors.xml`에 로그 색 두 개를 넣는다 |
| 10–25분 | 허용 번호 검사를 넣고 캡처 2를 찍는다 |
| 25–40분 | `준비됨`일 때만 버튼을 켜고, 보낸 직후 300ms 동안 버튼을 막는다 |
| 40–52분 | 오류 응답이면 AlertDialog와 빨간 로그를 보여 준다. 띄어쓰기를 일부러 빼서 확인하고 되돌린다 |
| 52–60분 | 최종 파일과 캡처·사진을 정리해 제출한다. 시간이 남으면 (확장) 밝기 조절을 한다 |

### 1. colors.xml에 로그 색 넣기

1. `app › res › values › colors.xml`을 연다. `black`·`white` 두 줄 아래에 `log_ok`(`#FF2E7D32`, 초록)와 `log_error`(`#FFD32F2F`, 빨강)를 넣는다.
2. 파일이 없으면 `values`를 오른쪽 클릭 → **New › Values Resource File** → 이름 `colors`로 만든다.
3. 실행해 화면이 1일차와 같으면 다음으로 간다. 색은 4번에서 쓴다.

막히면 [따라하기 8단계](walkthrough.md#8-colorsxml에-로그-색-두-개-넣기)를 본다.

### 2. 허용 번호 검사 → 캡처 2

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

5. `9` → Switch 켜기 → Toast `허용되지 않는 번호`가 보이고 로그에 `on 9`가 없는 화면을 **캡처한다(캡처 2).** Toast는 2초 만에 사라지니 뜨자마자 찍는다. Fake로 찍어도 된다.

- 빈 칸 검사를 허용 번호 검사보다 **먼저** 두는 까닭을 `toInt()`로 한 문장 적는다.

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

### 4. 오류 응답을 창과 색으로 알리기

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

5. 확인이 끝나면 **반드시 `"on $index"`로 되돌린다.**

- 앱 로그의 명령과 Logcat의 글자가 다른 까닭을 한 문장 적는다. 명령이 이상하면 어느 쪽을 믿어야 할까?

### 5. 제출 정리

1. 되돌린 코드로 한 번 더 실행해 `3` → Switch 켜기가 초록 `ok`로 끝나는지 본다.
2. `ControlActivity.kt`, `activity_control.xml`, 캡처 1·2, 사진(있으면)을 모은다.

### 6. (확장) SeekBar로 LED 0 밝기

1. `strings.xml`에 `pwm_title`(`LED 0 밝기`), `activity_control.xml`의 `allOffButton` 아래에 가로 `LinearLayout`(제목 `TextView` + id `pwmSeekBar`인 `SeekBar`, 폭 `160dp`, `android:max="255"`, `android:enabled="false"`)을 넣는다.
2. onCreate 끝에 `binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener { … })`를 만든다. 함수 세 개(`onProgressChanged`·`onStartTrackingTouch`·`onStopTrackingTouch`)를 모두 적고, **손을 뗄 때만** `pwm 0 값`을 보내고 로그에 쌓은 뒤 `pauseButtons()`를 부른다.
3. 3번의 collect와 `pauseButtons()`에서 `pwmSeekBar`도 같이 끄고 켠다.
4. 막대를 끌었다 놓으면 로그에 `pwm 0 값`과 `응답: {"result":"ok","ms":"pwm set"}`이 쌓이는지 본다. 실보드면 0번 LED 밝기가 바뀐다.

막히면 [따라하기 12단계](walkthrough.md#12-확장-seekbar로-led-0-밝기-조절하기)와 [2일차 완성 코드](examples/day2/ControlActivity.kt)를 본다.

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 줄이다. 파일 이름 뒤의 줄 번호는 내 코드에 따라 다르다.
**(예상)** 표시는 빌드는 되지만 실행에서 드러나는 증상을 코드로 짐작해 적은 것이라, 기기에서 조금 다르게 보일 수 있다.

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'BleunoMessage'.` | `Bleuno`는 12주차에 import했지만 `BleunoMessage`는 다른 이름이라 따로 import해야 한다. 빨간 글자에 Alt+Enter(맥 ⌥+Enter) → Import. `ConnState`도 같은 모양이다 |
| `Argument type mismatch: actual type is 'kotlin.Int', but 'kotlin.String' was expected.` (`send` 줄) | `send(index)`처럼 숫자를 넘겼다. `send`는 명령 글자 한 줄을 받는다. `send("on $index")` |
| `Modifier 'override' is not applicable to 'local function'.` | `override fun onStart()`를 onCreate 안에 붙여 넣었다. onCreate를 닫는 `}` **밖**, 클래스 안으로 옮긴다. "local function"은 함수 안에 만든 함수라는 뜻이다 |
| `Unresolved reference 'allOffButton'.` (`ControlActivity.kt`에 표시된다) | 고칠 곳은 `activity_control.xml`이다. `android:id="@+id/allOffButton"` 버튼이 있는지, 철자가 같은지 본다 |
| `Type inference failed. The value of the type parameter 'T' should be mentioned in input types (argument types, receiver type, or expected type). Try to specify it explicitly.` (`contains` 줄) | 메시지가 원인을 직접 말하지 않는다. 숫자 목록 `listOf(0, 1, 2, 3)`에서 글자 `pin`을 찾았다. `pin.toInt()`로 숫자를 넣는다 |
| `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` (`pauseButtons` 안) | `delay(300)`을 `lifecycleScope.launch { }` 밖에서 불렀다. 6주차처럼 `launch { }` 안에 둔다 |
| `Unresolved reference 'log_error'.` (`R.color.log_error` 줄. `log_ok` 줄에는 `Unresolved reference 'log_ok'.`) | `colors.xml`에 두 색 줄을 넣지 않았거나 이름 철자가 코드와 다르다. `app › res › values › colors.xml`에서 `log_ok`·`log_error` 두 줄과 철자를 본다. `colors.xml` 파일이 아예 없으면 같은 줄에 `Unresolved reference 'color'.`로 나온다 |
| `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'com.example.smartio.bleuno.BleunoClient?'.` | `Bleuno.client.send(…)`처럼 `?.`를 뺐다. `Bleuno.client?.send(…)`. 12주차와 같은 메시지다. `!!`는 쓰지 않는다 |
| Switch를 켜면 앱 로그에 `on 3`만 쌓이고 `응답:` 줄이 없다. 상단이 `상태: 연결 안 됨`이고 Logcat에 `send(가짜): 준비되지 않아 무시함` | 연결되지 않은 채 들어왔다(목록 줄을 누르지 않았거나 [해제]한 뒤 [연결]로 들어옴). [뒤로] → 목록 줄 탭 → `준비됨` → [제어 화면]으로 들어온다 |
| 처음에는 응답이 찍히다가 홈에 갔다 오면 명령 줄만 쌓이고 `응답:` 줄이 안 생긴다. Logcat에는 `onCharacteristicChanged(가짜): {"result":"ok",…}`가 계속 찍힌다 | `onMessage { }` 등록을 `onCreate`에 두었다. 다시 보일 때 불리는 것은 `onStart`다. 등록을 `onStart()` 안으로 옮긴다 |
| Fake로 `준비됨` 제어 화면에 가만히 있으면 10초마다 로그에 `응답: {"event":"input","index":0,"value":1}` 줄이 생긴다. 2일차 코드면 로그가 빨개지고 `응답: null · ` 창이 뜬다 | `if (result != null)` 검사가 빠졌다. 입력 이벤트 줄에는 `result`가 없다. 실보드는 이 줄을 보내지 않아 Fake에서만 드러난다 |
| `3` → Switch 켜기에 `응답: {"result":"fail","ms":"unknown command"}`, 로그가 빨갛고 창이 뜬다. Logcat에 `writeCharacteristic(가짜): "on3"` | `send` 줄에서 명령 이름과 번호 사이 띄어쓰기가 빠졌다. `"on $index"`. 앱 로그 줄이 아니라 Logcat에서 실제로 보낸 글자를 확인한다 |
| (예상) 입력 칸을 비운 채 Switch를 누르자 앱이 멈춘다. Logcat에 `java.lang.NumberFormatException: For input string: ""` | 허용 번호 가지를 빈 칸 가지보다 앞에 두었다. 순서는 빈 칸 → 허용 번호 → 켜기/끄기 |
| (예상) 아주 긴 숫자를 넣고 Switch를 누르자 앱이 멈춘다. Logcat에 `java.lang.NumberFormatException` | `pinEdit`의 `android:maxLength="2"`가 빠졌다 |
| (예상) `0`~`3`을 넣으면 `허용되지 않는 번호`, `9`를 넣으면 `on 9`가 나간다 | 조건에서 `== false`가 빠졌다. `isAllowedIndex(pin.toInt()) == false` |
| 명령을 몇 번 보냈더니 새 줄이 로그에 안 보인다 | 코드 잘못이 아니다. 로그 칸에 스크롤이 없어 아래로 밀렸다. [뒤로] → [제어 화면]으로 다시 들어오면 빈 로그로 시작한다 |
| 화면을 돌렸다 세로로 되돌리니 로그가 비워지고 `on 3`과 응답이 찍혀 있다. 폰 크기 가로 화면에서는 로그 칸이 안 보여, 돌릴 때 다시 나간 `on 3`은 Logcat에만 찍힌다(2일차 코드에서 입력 칸이 `9`면 돌릴 때마다 Toast가 다시 뜬다) | Switch 켜짐 상태가 되살아나며 리스너가 한 번 더 불린 것이다(3주차 회전). 가로로 돌릴 때 한 번, 세로로 되돌릴 때 또 한 번 나간다. LED는 이미 켜져 있어 보드에는 변화가 없다 |
| [전체 끄기]를 눌렀는데 Switch가 켜진 모양 그대로다 | 정상이다. [전체 끄기]는 보드에 명령만 보낸다. Switch를 다시 켜려면 한 번 끄고 켠다 |
| 2일차에 Switch·[전체 끄기]가 늘 회색이다 | 상단이 `상태: 준비됨`인지 본다. 준비됨인데도 회색이면 collect 안에서 `ConnState.READY`일 때 켜는 줄이 있는지 본다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.
보드 문제인지 앱 문제인지 모르겠으면 `useFake = true`로 같은 동작을 해 본다. Logcat `tag:BLE`에서 `writeCharacteristic` 뒤에 `onCharacteristicChanged`가 오는지가 단서다.

## 제출 — 코드 두 개, 캡처 2장, 사진 1장

1. **`ControlActivity.kt`**, **`activity_control.xml`**: 2일차 최종 코드(확장을 했으면 확장까지)
2. **캡처 1**: `상태: 준비됨` 제어 화면, 로그에 `on 3`(0~3 가운데 다른 번호도 된다)과 그 아래 `응답: {"result":"ok","ms":"led(s) on"}`(세로)
3. **캡처 2**: 입력 칸 `9`, Toast `허용되지 않는 번호`, 로그에 `on 9`가 없는 제어 화면(Fake 가능)
4. **사진**: 번호 3 LED(다른 번호를 보냈으면 그 번호 LED)가 켜진 보드. 보드·실기기가 없으면 생략한다

채점은 [README 완료 기준](README.md#완료-기준)의 항목을 이 제출물로 확인한다. 실습지의 관찰표(1일차 3·4·5번, 2일차 2·3·4번 표)는 스스로 점검하는 것이라 제출하지 않고 채점하지 않는다.
1일차 명령·응답(캡처 1)과 2일차 허용 번호 검사(캡처 2)까지 동작하면 기본 성공이다. 버튼 막기·오류 표시와 실보드 사진은 예제와 도움을 받아 마무리해도 된다.
캡처와 사진에 계정·알림 내용이 보이지 않게 한다. 제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: [전체 끄기] 옆에 [전체 켜기] 버튼을 둔다. 누르면 `on -1`을 보내고 로그에 쌓는다. 버튼 두 개는 5주차 [검색]·[중지]처럼 가로 `LinearLayout`에 나란히 둔다.
- 1일차: [로그 지우기] 버튼을 둔다. 누르면 `binding.logText.text = ""`로 로그 칸을 비운다. 넘친 로그를 [뒤로] 없이 비울 수 있다(버튼 한 줄만큼 로그 칸은 줄어든다).
- 2일차: [전체 켜기]도 `준비됨`일 때만 켜지고, 보낸 직후 300ms 동안 꺼지게 한다(collect와 `pauseButtons()`에 한 줄씩).
- 2일차: [전체 끄기] 뒤 `binding.ledSwitch.isChecked = false`로 Switch 모양도 끄면 무엇이 한 번 더 나갈지 예상하고, 로그로 확인해 본다(확인 뒤 되돌린다).

추가 과제는 선택 사항이다.
