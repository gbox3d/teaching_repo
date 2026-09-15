# 13주차 — BLE 출력 제어: 문자열 명령과 응답

## 이번 주 질문

> 제어 화면의 LED Switch를 켜면 보드의 LED가 진짜로 켜지고, 보드가 돌려준 대답까지 화면에서 확인하려면 어떻게 써야 할까?

12주차에는 목록 줄을 눌러 보드와 `준비됨`까지 연결했다. 그런데 제어 화면의 LED Switch는 아직 4주차처럼 로그에 `on 3`을 **적기만** 한다.
이번 주 1일차에는 같은 연결 `Bleuno.client`로 `send("on 3")`을 불러 **보드에 명령을 보내고**, 보드가 돌려주는 JSON 한 줄 `{"result":"ok","ms":"led(s) on"}`을 `onMessage { }`로 받아 로그에 쌓는다.
2일차에는 보드에 보내면 안 되는 번호(예: `9`)를 앱이 먼저 막고, 준비되지 않았거나 방금 보낸 참이면 버튼을 잠시 막고, 보드가 오류를 알리면 AlertDialog와 빨간 로그로 보여 준다. 보드가 없어도 가짜 클라이언트(`useFake = true`)로 끝까지 연습한다.

## 학습 목표

1. bleuno 명령 규약(명령 이름 + 띄어쓰기 한 칸 + LED 번호 `0`~`3`, `-1`은 전체)에 맞춰 `Bleuno.client?.send("on $index")`로 보드 LED를 켜고 끈다.
2. 특강의 `writeCharacteristic`·알림(notify)이 제공 라이브러리의 `send`·`onMessage`로 감싸져 있고, 명령은 큐에 들어가 하나씩 나간다는 것을 Logcat `tag:BLE`로 설명한다.
3. `onStart`에서 `Bleuno.client?.onMessage { json -> }`로 응답을 받아 `BleunoMessage.result(json)`로 응답 줄만 로그에 쌓고, `onStop`에서 `onMessage(null)`로 푼다.
4. `listOf(0, 1, 2, 3).contains(index)`로 허용 번호를 검사하고, `준비됨`이 아니거나 보낸 직후 300ms 동안은 버튼을 누를 수 없게 한다.
5. `result`가 `ok`가 아니면 `BleunoMessage.message(json)`로 설명을 꺼내 AlertDialog로 알리고, `colors.xml`의 색으로 로그 글자색을 바꾼다.

## 이번 주 결과물

```text
(1) 1일차 — Switch를 켜면 명령과 응답이 로그에 쌓인 제어 화면 (Fake)

장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)
상태: 준비됨
[3            ]
LED (●)
[전체 끄기]
명령 로그
on 3
응답: {"result":"ok","ms":"led(s) on"}
[뒤로]

(2) 사진 — 번호 3 LED(GPIO0)가 켜진 보드

(3) 2일차 — 9를 넣고 Switch를 켰을 때

[9            ]
LED (●)                 ← 로그에 on 9가 생기지 않는다
[전체 끄기]
LED 0 밝기 ─────○        (확장)
명령 로그
허용되지 않는 번호       ← Toast
```

사진 1장과 캡처 2장을 제출한다. 번호 3 LED가 켜진 보드 사진, 로그에 `on 3`과 응답 `응답: {"result":"ok","ms":"led(s) on"}`이 보이는 제어 화면, 입력 칸 `9`에 Toast `허용되지 않는 번호`가 뜬 제어 화면이다.
JSON 줄은 로그 칸 폭 때문에 두 줄로 접혀 보일 수 있다. 보드·실기기가 없으면 사진은 생략하고 캡처 두 장을 Fake로 찍는다(수업 공지 기준).

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `listOf(…).contains`, bleuno 명령 규약과 LED 번호, 특강의 write·notify가 `send`·`onMessage`로 감싸진 모습과 write 큐, Switch → `send`, `onStart`/`onStop`에서 응답 받기·풀기 | 입력 칸 문구·[전체 끄기] 자리 → Switch에서 `send` → `onStart`/`onStop` 응답 받기 → [전체 끄기] `off -1` → 캡처 1(보드가 있으면 사진) | 명령과 응답이 쌓이는 제어 화면 |
| 2일차 | 허용 번호 검사와 Toast, `준비됨`일 때만 버튼 켜기와 보낸 직후 300ms 막기, 오류 응답 AlertDialog와 `colors.xml`, (확장) `SeekBar`로 `pwm 0 V`, 2차 과제 공지 | `colors.xml` → 허용 번호 검사 → 캡처 2 → 버튼 막기 → 오류 표시 확인 → 제출, (확장) 밝기 조절 | 막고, 알리고, 색으로 보이는 제어 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 12주차까지 만든 `SmartIO` 프로젝트(목록 줄을 눌러 `준비됨`이 되면 [제어 화면]이 켜지고, 제어 화면 상단에 `상태: 준비됨`이 보이는 상태). 없으면 12주차 완성본(`examples/day2`)을 받아 시작한다.
- 에뮬레이터(AVD)는 12주차와 같이 **API 33 이상**을 쓴다. Fake로 명령·응답 연습을 끝까지 할 수 있다.
- 실보드 제어는 Android 실기기와 수업 보드(파랑 깜빡임 상태)가 있어야 한다. 학생은 펌웨어를 고치거나 올리지 않는다.
- [bleuno README 2절](../../bleuno/README.md#2-명령과-응답)의 명령 표와 [N은 LED 인덱스다](../../bleuno/README.md#n은-led-인덱스다)를 미리 읽어 온다.
- 3주차 `?.`·`?:`·생명주기 콜백, 4주차 `.toInt()`·`isEmpty()`·`append`·`@string/`, 5주차 `isEnabled`, 6주차 `lifecycleScope.launch`·`delay`, 7주차 `collect` 틀·`ConnState`, 10주차 `onStart`/`onStop` 짝·`AlertDialog`·익명 객체 틀, 12주차 `Bleuno.client`
- `AndroidManifest.xml`과 `build.gradle.kts`에 더할 것이 없다. 명령 보내기와 응답 받기는 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 들어 있고, `SeekBar`·`AlertDialog`·`ContextCompat`·`delay`는 4주차 의존성에 들어 있다.

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `listOf(0, 1, 2, 3).contains(index)` | 목록 안에 `index`가 있으면 `true`. 괄호 안에는 목록과 같은 종류의 값(숫자 목록이면 숫자)을 넣는다. `listOf`는 만든 뒤 바꾸지 않는 목록이다(11주차 `mutableListOf`와 다르다) |
| 명령 `on N` · `off N` · `off -1` · `pwm N V` | 보드에 보내는 글자 한 줄. 명령 이름, 띄어쓰기 한 칸, LED 번호. `N`은 GPIO가 아니라 LED 번호 `0`~`3`이고 `-1`은 전체다 |
| 응답 `{"result":"ok","ms":"led(s) on"}` | 명령마다 보드가 돌려주는 JSON 한 줄. `result`가 `ok`면 성공, `err`면 값이 틀림, `fail`이면 모르는 명령 |
| `Bleuno.client?.send("on $index")` | 명령 한 줄을 보낸다. 끝의 `\n`은 라이브러리가 붙이고, 큐에 넣어 하나씩 보낸다. `준비됨`이 아니면 라이브러리가 버린다 |
| `Bleuno.client?.onMessage { json -> }` / `onMessage(null)` | 보드가 보낸 JSON 한 줄을 받을 때마다 중괄호 안을 실행한다(메인 스레드) / 받기를 푼다 |
| `BleunoMessage.result(json)` / `BleunoMessage.message(json)` | JSON에서 `"result"` 값(`ok`·`err`·`fail`, 없으면 `null`) / `"ms"` 설명 값을 꺼낸다 |
| `override fun onStart()` / `override fun onStop()` | 3주차 생명주기 콜백. 10주차 Receiver처럼 `onStart`에서 등록하고 `onStop`에서 푼다. onCreate 괄호 **밖**, 클래스 안에 둔다 |
| `android:maxLength="2"` | 입력 칸에 두 글자까지만 들어간다 |
| `private fun isAllowedIndex(index: Int): Boolean` | 보내도 되는 번호면 `true`를 돌려주는 함수. 10주차 `hasBlePermissions()`와 같은 모양이다 |
| `android:enabled="false"` / `binding.ledSwitch.isEnabled = …` | 꺼진 채로 시작한다 / 코드로 켜고 끈다(5주차) |
| `Bleuno.client?.isReady == true` | 지금 명령을 보낼 수 있으면 `true`. client가 없으면(`null`) `false`가 된다 |
| `lifecycleScope.launch { delay(300) … }` | 300ms 기다렸다가 중괄호 뒷부분을 실행한다(6주차) |
| `res/values/colors.xml`의 `<color name="log_error">#FFD32F2F</color>` | 색에 이름을 붙여 둔다. `#AARRGGBB`에서 앞 `FF`는 불투명 |
| `ContextCompat.getColor(this, R.color.log_error)` / `binding.logText.setTextColor(…)` | 이름 붙인 색의 실제 값을 꺼낸다 / TextView 글자색을 바꾼다(로그 칸 전체) |
| `AlertDialog.Builder(this)…show()` | 10주차와 같은 알림 창 |
| (확장) `SeekBar`, `android:max="255"`, `object : SeekBar.OnSeekBarChangeListener { … }`, `progress` | 끌어서 값을 고르는 막대. 10주차 익명 객체 틀로 함수 세 개를 채우고, 손을 뗄 때 `progress` 값을 보낸다 |
| Logcat `package:mine tag:BLE` | `writeCharacteristic`(보낸 글자)과 `onCharacteristicChanged`(받은 JSON)가 찍힌다. Fake는 `(가짜)`가 붙는다 |

온도·습도(`dht11`)를 주기적으로 받기, 입력 이벤트(`{"event":"input",…}`) 해석, 끊김 뒤 재연결과 연결 시간 제한은 14주차에 다룬다.
로그의 **한 줄만** 색을 바꾸는 방법은 다루지 않는다(이번 주에는 로그 칸 전체 글자색을 바꾼다).

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 제공 라이브러리: [bleuno 패키지 README](../../bleuno/README.md) · [src 폴더](../../bleuno/src)
- 1일차 완성 코드: [ControlActivity.kt](examples/day1/ControlActivity.kt) · [activity_control.xml](examples/day1/activity_control.xml) · [strings.xml](examples/day1/strings.xml)
- 2일차 완성 코드: [ControlActivity.kt](examples/day2/ControlActivity.kt) · [activity_control.xml](examples/day2/activity_control.xml) · [strings.xml](examples/day2/strings.xml) · [colors.xml](examples/day2/colors.xml)

## 완료 기준

아래 항목은 모두 2일차 제출물(`ControlActivity.kt`·`activity_control.xml`, 캡처 2장, 사진 1장)로 확인한다. 실습지의 관찰표는 스스로 점검하는 것이고 채점하지 않는다.

- [ ] (1일차) LED Switch를 켜면 `Bleuno.client?.send("on $index")`, 끄면 `send("off $index")`로 명령을 보내고 보낸 명령을 로그에 쌓는다. [전체 끄기]는 `off -1`을 보낸다.
- [ ] `onStart`에서 `Bleuno.client?.onMessage { json -> }`로 등록해 `BleunoMessage.result(json)`가 `null`이 아닌 줄을 `응답: {…}`으로 로그에 쌓고, `onStop`에서 `Bleuno.client?.onMessage(null)`로 푼다.
- [ ] 캡처 1은 `상태: 준비됨` 제어 화면에서 로그에 `on 3`(0~3 가운데 다른 번호도 된다)과 그 아래 `응답: {"result":"ok","ms":"led(s) on"}`이 보이는 **세로** 화면이다.
- [ ] 사진은 번호 3 LED(다른 번호를 보냈으면 그 번호 LED)가 켜진 보드다. 보드·실기기가 없으면 생략한다.
- [ ] (2일차) 번호가 `0`~`3`(또는 `-1`)이 아니면 보내지 않고 Toast `허용되지 않는 번호`를 띄운다. `listOf(0, 1, 2, 3).contains(…)`로 검사한다.
- [ ] 캡처 2는 입력 칸 `9`와 Toast `허용되지 않는 번호`가 보이고 로그에 `on 9`가 **없는** 제어 화면이다(Fake로 찍어도 된다).
- [ ] `준비됨`이 아니면 LED Switch·[전체 끄기]가 꺼져 있고(연결 상태 `collect` 안에서 끄고 켠다), 명령을 보낸 직후 300ms 동안 꺼졌다가 다시 켜진다.
- [ ] 응답의 `result`가 `ok`가 아니면 로그 글자가 `colors.xml`의 빨간색이 되고 AlertDialog가 뜨며, `ok`면 초록색이 된다.
- [ ] `ControlActivity.kt`, `activity_control.xml`, 캡처 2장, 사진 1장을 제출한다.
- [ ] 캡처와 사진에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [14주차 — 입력 수신·끊김·재연결과 2차 과제 발표](../week14_ble_input_project/README.md)이다.
이번 주에는 보드에 **보내고** 그 대답을 받았다. 14주차에는 `dht11`을 3초마다 보내 온도·습도를 목록에 쌓고, 이번 주 `result != null`로 걸러 냈던 `{"event":"input",…}` 줄을 입력 이벤트로 읽는다.
보드 전원이 꺼져 `끊김`이 되면 [재연결]하고, 연결이 10초 안에 `준비됨`이 되지 않으면 안내한다. 2일차에는 지금까지 만든 Smart I/O Controller로 2차 과제를 발표한다.

## 공식 참고 자료

- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [Bluetooth Low Energy 개요 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/ble-overview)
- [색상 리소스 — Android Developers](https://developer.android.com/guide/topics/resources/more-resources#Color)
- [대화상자 — Android Developers](https://developer.android.com/develop/ui/views/components/dialogs)
- [SeekBar — Android Developers](https://developer.android.com/reference/android/widget/SeekBar)
- [컬렉션 개요 — Kotlin 문서](https://kotlinlang.org/docs/collections-overview.html)
- [bleuno 펌웨어 — GitHub](https://github.com/gbox3d/bleuno)
