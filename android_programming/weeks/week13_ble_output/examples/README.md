# 13주차 예제 — 보드에 명령 보내고 응답 받기

4주차부터 만들어 온 `SmartIO` 프로젝트(package `com.example.smartio`)를 기준으로 한다. 제공 라이브러리는 package `com.example.smartio.bleuno`다.
아래 파일은 1일차 **완성본**이다. 먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.
2일차는 과제 계획안 발표라 새 코드가 없다. 그래서 이번 주 예제는 `day1/`만 있다([과제 안내](../project_brief.md)).

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | 이번 주 변경 |
|---|---|---|
| [day1/ControlActivity.kt](day1/ControlActivity.kt) | `app › kotlin+java › com.example.smartio › ControlActivity.kt` | `BleunoMessage` import, 빈 칸 Toast 문구, 켜기·끄기에서 `send`(5·6번), `allOffButton` 리스너(7번), `onStart` 응답 받기(8·9번), `onStop` 해제(10번) |
| [day1/activity_control.xml](day1/activity_control.xml) | `app › res › layout › activity_control.xml` | `pinEdit`에 `android:maxLength="2"`, `ledSwitch` 아래 `allOffButton` 추가 |
| [day1/strings.xml](day1/strings.xml) | `app › res › values › strings.xml` | `pin_hint` 값 `핀 번호` → `LED 번호 (0~3)`(이름은 그대로), `all_off` 추가 |
| `day1/MainActivity.kt`, `day1/activity_main.xml`, `day1/ContactsReader.kt` | 연결 화면·연락처 읽기 | 12주차 `week12_ble_gatt/examples/day2` 그대로, 바꾸지 않는다 |
| [day1/bleuno/](day1/bleuno) 8개 | `app › kotlin+java › com.example.smartio › bleuno` | 12주차에 넣은 제공 코드 그대로. [bleuno/src](../../../bleuno/src)와 같다 |
| `day1/AndroidManifest.xml`, `day1/res/values/themes.xml` | Manifest·테마 | 12주차 그대로. 명령 보내기·응답 받기는 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 들어 있다 |

`ControlActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.
`build.gradle.kts`에 더할 것이 없다. 명령 보내기와 응답 받기는 12주차에 넣은 bleuno 패키지가 한다.
주석 번호는 12주차 1~4에 이어 5~10을 붙였다. 번호는 넣은 순서라 파일 안에서는 차례대로 놓이지 않는다.
입력 칸 id `pinEdit`와 문자열 이름 `pin_hint`는 4주차 이름 그대로 두었다. 뜻은 이제 **LED 번호**다.
허용 번호 검사(`listOf(0, 1, 2, 3).contains`)·버튼 막기·오류 대화상자·`colors.xml`·`SeekBar`는 14주차 예제로 넘어갔다. 1일차 슬라이드의 `listOf` 미리 보기는 그때 쓴다.

## 1. `send`와 명령 규약 — 보드에 글자 한 줄 보내기

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

## 2. `onMessage`와 `BleunoMessage.result` — 응답 받기, 화면이 보일 때만

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
| `{"event":"input","index":0,"value":1}` (Fake가 10초마다) | `null` | 쌓지 않는다(14주차 2일차에 다룬다) |

- `{ json -> }`의 `json`은 보드가 보낸 글자 한 줄이다. 라이브러리가 메인 스레드에서 불러 주므로 `runOnUiThread` 없이 View를 바꾼다.
- 10주차 Receiver처럼 `onStart`에서 등록하고 `onStop`에서 푼다. 홈에 갔다 오면 `onStop` → `onStart` 순서로 풀렸다가 다시 등록된다.
- 두 함수는 onCreate의 `}` 밖, 클래스 안에 둔다. onCreate 안에 넣으면 `Modifier 'override' is not applicable to 'local function'.`
- `onMessage`는 받는 칸이 하나뿐이라 새로 등록하면 앞 것을 덮는다. 연결 화면(`MainActivity`)은 등록하지 않는다.

## 3. 1일차 완성 — 명령과 응답

[day1](day1) 파일을 모두 넣고 실행한 흐름:

```text
목록 줄 탭 ▶ 준비됨 ▶ [제어 화면] ─ onStart: onMessage 등록, collect: 상태: 준비됨 표시
  번호 입력 ─┬─ 비움 ▶ Toast "LED 번호를 입력하세요"
             └─ 숫자 ▶ send("on 3") ▶ 로그 on 3 ▶ 응답 JSON ▶ 로그 응답: {…}
  [전체 끄기] ▶ send("off -1") ▶ 로그 off -1 ▶ 응답 JSON
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
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
