# 13주차 예제 — 보드에 명령 보내고 응답 받기

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다. 제공 라이브러리는 package `com.example.smartio.bleuno`다.
아래 파일은 해당 날짜의 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/ControlActivity.kt](day1/ControlActivity.kt) | `app › kotlin+java › com.example.smartio › ControlActivity.kt` | `BleunoMessage` import, 빈 칸 Toast 문구, 켜기·끄기에서 `send`(5·6번), `allOffButton` 리스너(7번), `onStart` 응답 받기(8·9번), `onStop` 해제(10번) |
| [day1/activity_control.xml](day1/activity_control.xml) | `app › res › layout › activity_control.xml` | `pinEdit`에 `android:maxLength="2"`, `ledSwitch` 아래 `allOffButton` 추가 |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | `pin_hint` 값 `핀 번호` → `LED 번호 (0~3)`(이름은 그대로), `all_off` 추가 |
| [day2/ControlActivity.kt](day2/ControlActivity.kt) | `ControlActivity.kt` | import 5개, 허용 번호 검사(11·12번), 준비됨일 때만 켜기(13번), 보낸 직후 300ms(14·15번), 오류 응답 표시(16번), (확장) SeekBar(17번) |
| [day2/activity_control.xml](day2/activity_control.xml) | `activity_control.xml` | `ledSwitch`·`allOffButton`에 `android:enabled="false"`, (확장) `allOffButton` 아래 제목 + `pwmSeekBar` 가로 줄 |
| [day2/strings.xml](day2/strings.xml) | `strings.xml` | (확장) `pwm_title` 추가 |
| [day2/colors.xml](day2/colors.xml) | `app › res › values › colors.xml` | 새 프로젝트에 이미 있는 파일(`black`·`white`)에 `log_ok`·`log_error` 두 줄 추가. 예제는 파일째 바꿔도 되게 네 줄을 모두 두었다 |
| `dayN/MainActivity.kt`, `dayN/activity_main.xml`, `dayN/ContactsReader.kt` | 연결 화면·연락처 읽기 | 12주차 `examples/day2` 그대로, 바꾸지 않는다 |
| [day1/bleuno/](day1/bleuno) 8개 | `app › kotlin+java › com.example.smartio › bleuno` | 12주차에 넣은 제공 코드 그대로. [bleuno/src](../../../bleuno/src)와 같다 |
| `dayN/AndroidManifest.xml`, `dayN/res/values/themes.xml` | Manifest·테마 | 12주차 그대로. 명령 보내기·응답 받기는 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 들어 있다 |

`ControlActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`SeekBar`·`AlertDialog`·`ContextCompat`·`delay`는 4주차 의존성에 들어 있어 `build.gradle.kts`에 더할 것이 없다.
주석 번호는 12주차 1~4에 이어 5~10(1일차), 11~17(2일차)을 붙였다. 번호는 넣은 순서라 파일 안에서는 차례대로 놓이지 않는다(11번은 2번 리스너 안, 12·15번은 파일 끝 함수). 14번은 같은 한 줄(`pauseButtons()`)이라 세 곳에 같은 번호를 달았다.
입력 칸 id `pinEdit`와 문자열 이름 `pin_hint`는 4주차 이름 그대로 두었다. 뜻은 이제 **LED 번호**다.

**(확장) 표시**: 2일차 SeekBar는 17번 주석 첫머리 `(확장)`과 13·15번 안의 줄 끝 `// (확장)`으로 표시했다. 확장을 하지 않으면 `activity_control.xml`의 `LinearLayout` 덩어리(51~71행), `strings.xml`의 `pwm_title`, `ControlActivity.kt`의 `import android.widget.SeekBar`, 17번 덩어리(101~118행), `// (확장)`이 붙은 네 줄(83·87·173·179행)을 넣지 않는다. 하나만 남기면 `Unresolved reference 'pwmSeekBar'.`로 빌드가 안 된다.

## 1. `listOf(0, 1, 2, 3).contains(index)` — 허용 번호인지 묻기

```kotlin
if (listOf(0, 1, 2, 3).contains(index)) {
    return true
}
```

| `index` | 결과 |
|---|---|
| `0`, `1`, `2`, `3` | `true` |
| `4`, `9` | `false` |
| `-1` | `false` (그래서 `isAllowedIndex`는 `index == -1`을 따로 확인한다) |

- 괄호 안에는 목록과 같은 종류의 값을 넣는다. 숫자 목록에 글자(`pin`)를 넣으면 `Type inference failed. …` 오류가 난다.
- `listOf`는 만든 뒤 바꾸지 않는 목록이다. 11주차 `mutableListOf`는 `add`로 늘릴 수 있는 목록이다.

## 2. `send`와 명령 규약 — 보드에 글자 한 줄 보내기

```kotlin
val index = pin.toInt()
Bleuno.client?.send("on $index")
binding.logText.append("on $index\n")
```

| 명령 | 뜻 | 응답 (Fake·실보드 같음) |
|---|---|---|
| `on 3` | 3번 LED 켜기 | `{"result":"ok","ms":"led(s) on"}` |
| `off 3` | 3번 LED 끄기 | `{"result":"ok","ms":"led(s) off"}` |
| `off -1` | 모두 끄기 | `{"result":"ok","ms":"led(s) off"}` |
| `pwm 0 128` | 0번 LED 밝기 | `{"result":"ok","ms":"pwm set"}` |
| `on3` | 모르는 명령(띄어쓰기 없음) | `{"result":"fail","ms":"unknown command"}` |

| 실행 결과 (Fake, `준비됨`, `3` → Switch 켜기) | 화면 | Logcat `package:mine tag:BLE` |
|---|---|---|
| 누른 직후 | 로그 `on 3` | `writeCharacteristic(가짜): "on 3"` |
| 약 0.3초 뒤 | (8·9번을 넣었으면) `응답: {"result":"ok","ms":"led(s) on"}` | `onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) on"}` |
| `연결 안 됨`에서 누름(연결하지 않았거나 [해제]한 뒤 [연결]로 들어옴) | 로그 `on 3`만, 응답 없음 | `send(가짜): 준비되지 않아 무시함 ("on 3", 상태=연결 안 됨)` |

- 규칙: 명령 이름 + **띄어쓰기 한 칸** + LED 번호. 끝의 `\n`은 `send`가 붙인다. 번호 `N`은 GPIO가 아니라 LED 번호다(3 = GPIO0).
- 실보드 로그: `send: 큐에 추가 "on 3" (대기 1개)` → `writeCharacteristic("on 3") 호출 결과=true` → `onCharacteristicWrite: status=0` → `onCharacteristicChanged: {"result":"ok","ms":"led(s) on"}`. 쓰기가 끝났다는 콜백이 와야 다음 명령이 나간다(write 큐).
- `send`는 글자(`String`)를 받는다. `send(index)`처럼 숫자를 넘기면 `Argument type mismatch: actual type is 'kotlin.Int', but 'kotlin.String' was expected.`
- 보드는 번호를 검사하지 않는다. Fake는 `on 9`에도 `ok`로 답하지만 실보드에는 `0`~`3`만 보낸다.

## 3. `onMessage`와 `BleunoMessage.result` — 응답 받기, 화면이 보일 때만

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

override fun onStop() {
    super.onStop()
    Bleuno.client?.onMessage(null)
}
```

| 받은 JSON | `BleunoMessage.result(json)` | 로그 |
|---|---|---|
| `{"result":"ok","ms":"led(s) on"}` | `"ok"` | `응답: {"result":"ok","ms":"led(s) on"}` |
| `{"result":"fail","ms":"unknown command"}` | `"fail"` | `응답: {"result":"fail","ms":"unknown command"}` |
| `{"event":"input","index":0,"value":1}` (Fake가 10초마다) | `null` | 쌓지 않는다(14주차에 다룬다) |

- `{ json -> }`의 `json`은 보드가 보낸 글자 한 줄이다. 라이브러리가 메인 스레드에서 불러 주므로 `runOnUiThread` 없이 View를 바꾼다.
- 10주차 Receiver처럼 `onStart`에서 등록하고 `onStop`에서 푼다. 홈에 갔다 오면 `onStop` → `onStart` 순서로 풀렸다가 다시 등록된다.
- 두 함수는 onCreate의 `}` 밖, 클래스 안에 둔다. onCreate 안에 넣으면 `Modifier 'override' is not applicable to 'local function'.`
- `onMessage`는 받는 칸이 하나뿐이라 새로 등록하면 앞 것을 덮는다. 연결 화면(`MainActivity`)은 등록하지 않는다.

## 4. 허용 번호 검사 — 보내기 전에 앱이 막는다

```kotlin
} else if (isAllowedIndex(pin.toInt()) == false) {
    Toast.makeText(this, "허용되지 않는 번호", Toast.LENGTH_SHORT).show()
} else if (isChecked) {
```

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

| 실행 결과 (Switch 켜기) | 화면 | Logcat `tag:BLE` |
|---|---|---|
| `3` | 로그 `on 3` → `응답: {…ok…}` | `writeCharacteristic(가짜): "on 3"` |
| `9` | Toast `허용되지 않는 번호`, 로그 변화 없음, Switch 모양만 켜짐 | 새 줄 없음 |
| 비움 | Toast `LED 번호를 입력하세요` | 새 줄 없음 |

- 사슬 순서는 빈 칸 → 허용 번호 → 켜기/끄기다. 빈 칸 검사가 먼저라 `"".toInt()`가 불리지 않는다.
- 입력 칸은 `inputType="number"`라 `-`를 적을 수 없다. `-1`은 [전체 끄기]가 보낸다.

## 5. 준비됨일 때만, 보낸 직후 300ms는 막기

```kotlin
binding.ledSwitch.isEnabled = false
binding.allOffButton.isEnabled = false
if (state == ConnState.READY) {
    binding.ledSwitch.isEnabled = true
    binding.allOffButton.isEnabled = true
}
```

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

| 실행 결과 | LED Switch·[전체 끄기] |
|---|---|
| `준비됨` 제어 화면 | 켜짐 |
| 연결되지 않은 채 들어옴([해제]한 뒤 [연결], `연결 안 됨`) | 회색, 눌리지 않음 |
| 명령을 보낸 직후 | 0.3초 회색 → 다시 켜짐 |
| 제어 화면에 있는 동안 연결이 끊김(실보드 전원 끔) | `상태: 끊김`, 곧바로 회색 |

- 첫 코드는 12주차 4번 collect 안(`상태: $state` 아래)에 둔다. XML의 `android:enabled="false"`로 상태가 오기 전에도 꺼져 있다.
- `Bleuno.client?.isReady == true`: client가 없으면 `null == true`라 `false`다. 7주차 `scanJob?.isActive == true`와 같은 모양이다.
- `delay`를 `launch { }` 밖에서 부르면 `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.`

## 6. 오류 응답 — AlertDialog와 colors.xml

```xml
    <color name="log_ok">#FF2E7D32</color>
    <color name="log_error">#FFD32F2F</color>
```

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

| 실행 결과 | 화면 |
|---|---|
| `ok` 응답 | 로그 전체 글자가 초록색 |
| `fail`·`err` 응답 | 로그 전체 글자가 빨간색, AlertDialog `보드가 오류를 알렸습니다` / `응답: fail · unknown command` / [확인] |
| 오류 뒤 [전체 끄기] | `ok`라 다시 초록색 |

- 2일차 완성본은 허용 번호만 보내므로 정상 흐름에서는 `ok`만 온다. 확인하려면 5번 `send` 줄만 잠시 `"on$index"`로 바꿔 실행하고(제어 화면에 들어온 직후 첫 조작), 확인한 뒤 되돌린다.
- `BleunoMessage.message(json)`는 `"ms"` 값이고 `String?`이라 `?:`로 빈 글자를 대신 넣는다.
- 색은 로그 칸 **전체**에 적용된다. `colors.xml`에 두 줄을 넣지 않으면 `R.color.log_error` 줄에 `Unresolved reference 'log_error'.`(`log_ok` 줄은 `'log_ok'`), 파일이 아예 없으면 `Unresolved reference 'color'.`

## 7. (확장) SeekBar로 `pwm 0 V`

```kotlin
binding.pwmSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
    override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
    }

    override fun onStartTrackingTouch(seekBar: SeekBar?) {
    }

    override fun onStopTrackingTouch(seekBar: SeekBar?) {
        val value = binding.pwmSeekBar.progress
        Bleuno.client?.send("pwm 0 $value")
        binding.logText.append("pwm 0 $value\n")
        pauseButtons()
    }
})
```

| 실행 결과 | 화면 |
|---|---|
| 막대를 가운데쯤 끌었다 놓기 | 놓는 순간 로그 `pwm 0 127`(값은 위치에 따라 다름) → `응답: {"result":"ok","ms":"pwm set"}` |
| 실보드 | 0번 LED(GPIO4) 밝기가 바뀐다 |

- 10주차 `object : BroadcastReceiver() { … }`와 같은 익명 객체 틀이다. 할 일이 세 개인 리스너라 함수 세 개를 모두 적는다.
- 끄는 동안(`onProgressChanged`)마다 보내면 write 큐에 명령이 수십 개 쌓인다. 손을 뗄 때(`onStopTrackingTouch`) 한 번만 보낸다.
- XML `android:max="255"`라 값은 늘 `0`~`255`다.

## 8. 2일차 완성 — 명령, 응답, 막기, 알리기

[day2](day2) 파일을 모두 넣고 실행한 흐름:

```text
목록 줄 탭 ▶ 준비됨 ▶ [제어 화면] ─ onStart: onMessage 등록, collect: 준비됨이면 버튼 켜기
  번호 입력 ─┬─ 비움 ▶ Toast "LED 번호를 입력하세요"
             ├─ 0~3 아님 ▶ Toast "허용되지 않는 번호" (보내지 않음)
             └─ 0~3 ▶ send("on 3") ▶ 로그 on 3 ▶ 버튼 0.3초 회색
                      ▶ 응답 JSON ─┬─ ok ▶ 로그 응답: {…} 초록
                                   └─ err·fail ▶ 로그 빨강 + AlertDialog
  [전체 끄기] ▶ send("off -1")    (확장) SeekBar 놓기 ▶ send("pwm 0 V")
[뒤로]·홈 ▶ onStop: onMessage(null)
```

실보드 연결 뒤 명령 하나를 보낼 때 Logcat `tag:BLE`에 남는 줄([bleuno README](../../../bleuno/README.md) 8절):

```text
send: 큐에 추가 "on 3" (대기 1개)
writeCharacteristic("on 3") 호출 결과=true
onCharacteristicWrite: status=0
onCharacteristicChanged: {"result":"ok","ms":"led(s) on"}
```

## 공식 참고 자료

- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [색상 리소스 — Android Developers](https://developer.android.com/guide/topics/resources/more-resources#Color)
- [대화상자 — Android Developers](https://developer.android.com/develop/ui/views/components/dialogs)
- [SeekBar — Android Developers](https://developer.android.com/reference/android/widget/SeekBar)
