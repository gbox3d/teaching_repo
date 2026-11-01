# 14주차 — 안전한 명령 전송과 입력 수신·재연결

## 이번 주 질문

> 보내면 안 되는 번호를 앱이 먼저 막고 보드의 오류를 사람이 알아볼 수 있게 보여 주려면, 그리고 보드가 돌려주는 온도·습도를 3초마다 받아 목록에 쌓고 연결이 끊기면 다시 연결하게 하려면 어떻게 써야 할까?

13주차에는 제어 화면에서 보드에 `on 3`을 **보내고** JSON 대답을 명령 로그에 쌓았다. 번호를 아무것이나 적어도 그대로 나갔고, 응답이 `fail`이어도 로그에 JSON 한 줄이 섞여 있을 뿐이었다.
이번 주 1일차에는 허용 번호(`0`~`3`, 전체는 `-1`)만 보내게 막고, `준비됨`이 아니거나 방금 보낸 참이면 버튼을 누를 수 없게 하고, `result`가 `ok`가 아니면 `colors.xml`의 빨간색과 AlertDialog로 알린다.
2일차에는 `dht11`을 3초마다 보내 온도·습도 응답과 입력 이벤트를 **입력 이력** 목록에 시각과 함께 쌓고, 연결이 `끊김`이 되면 알리고 [재연결]하며, 연결을 시작한 뒤 10초 안에 `준비됨`이 되지 않으면 안내하고 끊는다.
두 날 모두 보드가 없어도 가짜 클라이언트(`useFake = true`)로 끝까지 할 수 있다.

## 학습 목표

1. `listOf(0, 1, 2, 3).contains(index)`로 허용 번호를 검사해 `private fun isAllowedIndex(index: Int): Boolean`으로 묶고, 걸리면 명령도 로그도 남기지 않는다.
2. `준비됨`일 때만 버튼을 켜고(`android:enabled="false"` + collect), 보낸 직후 300ms 동안은 `lifecycleScope.launch { delay(300) … }`로 막는다.
3. `colors.xml`에 이름 붙인 색을 `ContextCompat.getColor(this, R.color.log_error)`로 꺼내 로그 글자색을 바꾸고, `result != "ok"`면 `BleunoMessage.message(json)` 설명을 AlertDialog로 알린다.
4. `split(" ")`로 이력 한 줄을 나누고 `[0]`·`[1]`로 시각과 값을 꺼내며, 제공 helper `BleunoMessage.event(json)`·`BleunoMessage.value(json)`로 받은 JSON에서 값을 꺼낸다.
5. `inputJob = lifecycleScope.launch { while (isActive) { … send("dht11"); delay(3000) } }`로 온습도를 3초마다 요청하고, [중지]·끊김·`onStop`에서 `inputJob?.cancel()`로 멈춘다.
6. 받은 줄을 입력 이벤트·`dht11` 응답·명령 응답 세 가지로 가르고, `SimpleDateFormat` 틀로 시각을 붙여 입력 이력 `ListView`에 쌓는다.
7. 연결 상태가 `끊김`(`ConnState.LOST`)이면 Toast와 [재연결]을 보이고, SharedPreferences에 저장해 둔 주소로 `client.connect(lastAddress)`하며, `launch` + `suspend fun`의 `delay(10000)`으로 10초 시간 제한을 건다.

## 이번 주 결과물

```text
(1) 1일차 — 허용되지 않는 번호를 앱이 막았을 때

장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)
상태: 준비됨
[9            ]
LED (●)                 ← 명령 로그에 on 9가 생기지 않는다
[전체 끄기]
명령 로그
on 3
응답: {"result":"ok","ms":"led(s) on"}      ← 초록
허용되지 않는 번호      ← Toast

(2) 1일차 — 보드가 오류를 알렸을 때

명령 로그
on 3
응답: {"result":"fail","ms":"unknown command"}   ← 빨강
┌──────────────────────────────┐
│ 보드가 오류를 알렸습니다      │
│ 응답: fail · unknown command │
│                      [확인]  │
└──────────────────────────────┘

(3) 2일차 — 온습도를 받는 중인 제어 화면 (Fake)

명령 로그
on 3
응답: {"result":"ok","ms":"led(s) on"}
[온습도 받기 시작] [중지]
입력 이력
12:00:03 [24.5,40.0]
12:00:06 [25.0,41.0]
12:00:09 [25.5,42.0]
[뒤로]

(4) 2일차 — 보드 전원이 꺼져 끊겼을 때의 연결 화면

끊김
검색된 장치
ESP32_BLE_FAKE1 (00:11:22:33:44:01)
[연결]
[제어 화면]
[다시 시도]
[재연결] [끊김 시험]
연결이 끊겼습니다. [재연결]을 누르세요     ← Toast
```

[끊김 시험]은 가짜 보드로 끊김을 만드는 시험용 버튼이며 실보드에서는 보이지 않는다. 채점하지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 실습 60분 | 제출 |
|---|---|---|---|
| 1일차 | 보내기 전 허용 번호 확인과 `isAllowedIndex()`, `준비됨`일 때만 누르기와 보낸 직후 300ms 막기, `colors.xml`과 `R.color`, `result`가 `ok`가 아니면 AlertDialog, 오류를 일부러 만들어 확인하기, (확장) `SeekBar`로 `pwm` | `colors.xml` 두 색 → 허용 번호 검사 → `enabled="false"`와 collect → `pauseButtons()` → 오류 표시 → 띄어쓰기를 빼서 확인하고 되돌리기 | 코드 두 개 + 캡처 2장(허용되지 않는 번호 Toast, 오류 대화상자와 빨간 로그) |
| 2일차 | `split`·`[0]`·`[1]`와 `BleunoMessage.value/event`, `dht11` 3초마다 요청과 입력 이력, 받은 줄 세 갈래로 가르기, `끊김` 알림과 [재연결], 10초 연결 시간 제한 | 입력 이력 자리 → 받은 줄 가르기 → [온습도 받기 시작]·[중지] → 이력 줄 나누기 → [재연결]·[끊김 시험] → 시간 제한 | 코드 네 개 + 캡처 2장(입력 이력 2줄, `끊김`과 [재연결]) |

15주차에 내는 과제(완성 앱·캡처 세트·레포트)는 13주차에 발표한 계획안대로 마무리한다. 조건과 채점은 [13주차 과제 안내](../week13_ble_output/project_brief.md)에 있으며, 이번 주 실습 제출과는 별개다.

## 준비

- 13주차까지 만든 `SmartIO` 프로젝트(제어 화면에서 LED Switch가 `send`로 명령을 보내고, `onStart`에서 받은 응답을 로그에 쌓는 상태). 없으면 13주차 완성본(`../week13_ble_output/examples/day1`)을 받아 시작한다.
- 2일차는 1일차 완성본(`examples/day1`)에서 이어서 시작한다. 1일차에 못 끝낸 사람은 그 폴더를 받아 시작한다.
- 에뮬레이터(AVD)는 **API 33 이상**. Fake로 번호 검사·오류 표시·입력 받기·끊김·재연결·시간 제한까지 모두 연습할 수 있다.
- 실보드로 하려면 Android 실기기와 수업 보드(파랑 깜빡임 상태)가 있어야 한다. 학생은 펌웨어를 고치거나 올리지 않는다.
- [bleuno README의 명령 규약](../../bleuno/README.md)과 [가짜 클라이언트의 동작](../../bleuno/README.md#7-fakebleunoclient의-동작)을 미리 읽어 온다.
- 다시 쓰는 것: 3주차 `?:`·회전, 5주차 `isEnabled`, 6주차 `Job`·`cancel()`·`suspend fun`·`delay`, 7주차 collect 틀·`ConnState`·`.value`, 10주차 `hasBlePermissions()`·익명 객체 틀·AlertDialog, 11주차 `ListView`·`ArrayAdapter`·`notifyDataSetChanged`·`setOnItemClickListener`·SharedPreferences, 12주차 `connect`·`useFake`, 13주차 `send`·`onMessage`·`BleunoMessage.result`·`listOf(…).contains(…)`.
- `AndroidManifest.xml`과 `build.gradle.kts`에 더할 것이 없다. `dht11` 보내기와 재연결은 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 있고, `ArrayAdapter`·`Job`·`SimpleDateFormat`·`ContextCompat`은 4주차 의존성과 Android 기본 API에 들어 있다.

## 이번 주 범위

1일차에 쓰는 문법·API:

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `private fun isAllowedIndex(index: Int): Boolean` | 보내도 되는 번호면 `true`를 돌려주는 함수. 10주차 `hasBlePermissions()`와 같은 모양이다 |
| `listOf(0, 1, 2, 3).contains(index)` | 목록 안에 `index`가 있으면 `true`. 괄호 안에는 목록과 같은 종류(숫자)를 넣는다. 13주차 오늘 문법이다 |
| `isAllowedIndex(pin.toInt()) == false` | 허용 번호가 **아니면**. 빈 글자를 `toInt()`하면 앱이 멈추므로 빈 칸 검사를 먼저 둔다 |
| `android:enabled="false"` / `binding.ledSwitch.isEnabled = …` | 꺼진 채로 시작한다 / 코드로 켜고 끈다(5주차) |
| `Bleuno.client?.isReady == true` | 지금 명령을 보낼 수 있으면 `true`. client가 없으면(`null`) `false`가 된다 |
| `lifecycleScope.launch { delay(300) … }` | 300ms 기다렸다가 중괄호 뒷부분을 실행한다(6주차) |
| `res/values/colors.xml`의 `<color name="log_error">#FFD32F2F</color>` | 색에 이름을 붙여 둔다. `#AARRGGBB`에서 앞 `FF`는 불투명 |
| `ContextCompat.getColor(this, R.color.log_error)` / `binding.logText.setTextColor(…)` | 이름 붙인 색의 실제 값을 꺼낸다 / TextView 글자색을 바꾼다(로그 칸 전체) |
| `BleunoMessage.message(json) ?: ""` | JSON에서 `"ms"` 설명 값을 꺼낸다. 없으면 `null`이라 3주차 `?:`로 빈 글자를 넣는다 |
| `AlertDialog.Builder(this)…show()` | 10주차와 같은 알림 창. `androidx.appcompat.app.AlertDialog`를 고른다 |
| (확장) `object : SeekBar.OnSeekBarChangeListener { … }` / `android:max="255"` | 10주차 익명 객체 틀. 함수 세 개를 모두 적는다 / 막대 값의 최대 |

2일차에 쓰는 문법·API:

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `"12:00:03 [24.5,40.0]".split(" ")` | 글자를 띄어쓰기가 있는 곳마다 잘라 목록 `[12:00:03, [24.5,40.0]]`으로 돌려준다 |
| `parts[0]` / `parts[1]` / `history[position]` | 목록의 첫째 칸 / 둘째 칸 / 누른 줄 번호의 칸. 번호는 0부터 센다. 12주차 `get(position)`과 같다 |
| `BleunoMessage.event(json)` / `BleunoMessage.value(json)` | JSON에서 `"event"` / `"value"` 값을 꺼낸다. 키가 없으면 `null`(`String?`) |
| 명령 `dht11` / 응답 `{"result":"ok","value":"[24.5,40.0]"}` | 온도·습도를 한 번 읽어 달라는 명령 / `[온도,습도]` 값이 담긴 응답 |
| 입력 이벤트 `{"event":"input","index":0,"value":1}` | 보드가 먼저 보내는 입력(가안). 가짜 보드만 10초마다 보낸다. 실보드는 펌웨어가 확장되기 전에는 보내지 않는다 |
| `private var inputJob: Job? = null` / `inputJob = lifecycleScope.launch { while (isActive) { … } }` / `inputJob?.cancel()` | 반복 코루틴을 보관한다 / 취소되지 않았으면 되풀이한다 / 멈춘다(6주차 `scanJob`과 같다) |
| `SimpleDateFormat("HH:mm:ss", Locale.KOREA).format(Date())` | 지금 시각을 `12:00:03`(시:분:초) 글자로 만드는 틀. `Date`는 `java.util.Date` |
| `android:transcriptMode="alwaysScroll"` | 목록에 새 줄이 들어오면 맨 아래로 내려간다 |
| `ConnState.LOST`(`끊김`) | 사용자가 [해제]하지 않았는데 연결이 끊긴 상태(보드 전원 꺼짐·멀어짐) |
| `client.connect(lastAddress)` | 마지막으로 연결을 시작한 보드 주소로 다시 연결한다 |
| `putString("lastAddress", address)` / `prefs.getString("lastAddress", "") ?: ""` | 11주차 SharedPreferences 틀로 주소를 저장하고 꺼낸다. 화면이 새로 만들어져도 남는다 |
| `private fun showLostToast()` | collect 틀 안의 `this`는 화면이 아니라서 Toast를 화면의 함수로 빼서 부른다 |
| `connectTimeoutJob = lifecycleScope.launch { waitConnectTimeout() }` / `private suspend fun waitConnectTimeout() { delay(10000) … }` | 10초 뒤 아직 `연결 중`·`서비스 확인 중`이면 안내하고 끊는다. 6주차 `countDown()`과 같은 모양 |
| `client.connectionState.value` | 지금 연결 상태 값(7주차 `_state.value`와 같다) |
| (시험용) `val fake = client as FakeBleunoClient` / `fake.simulateLost()` | 가짜 보드로 `끊김`을 만든다. 복사해 쓰는 틀이며 채점하지 않는다 |

로그 한 줄만 색 바꾸기, 앱이 보이지 않을 때 계속 받기, 자동으로 되풀이하는 재연결, 회전해도 입력 이력 남기기, 보드 여러 대 동시 연결은 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습 안내](lab.md)
- [예제 설명](examples/README.md)
- 제공 라이브러리: [bleuno 패키지 README](../../bleuno/README.md) · [src 폴더](../../bleuno/src)
- 1일차 완성 코드: [ControlActivity.kt](examples/day1/ControlActivity.kt) · [activity_control.xml](examples/day1/activity_control.xml) · [strings.xml](examples/day1/strings.xml) · [colors.xml](examples/day1/colors.xml)
- 2일차 완성 코드(최종 앱): [ControlActivity.kt](examples/day2/ControlActivity.kt) · [MainActivity.kt](examples/day2/MainActivity.kt) · [activity_control.xml](examples/day2/activity_control.xml) · [activity_main.xml](examples/day2/activity_main.xml) · [strings.xml](examples/day2/strings.xml)
- 15주차 과제: [13주차 과제 안내](../week13_ble_output/project_brief.md)

## 완료 기준

1일차:

- [ ] 입력 칸에 `9`를 넣고 Switch를 켜면 Toast `허용되지 않는 번호`만 뜨고, 명령 로그와 Logcat에 `on 9` 줄이 없다.
- [ ] 입력 칸을 비운 채 Switch를 켜도 앱이 멈추지 않는다.
- [ ] `연결 안 됨`으로 제어 화면에 들어오면 LED Switch와 [전체 끄기]가 회색이고, `준비됨`이 되면 켜진다.
- [ ] 명령을 보낸 직후 두 버튼이 잠깐 꺼졌다가 다시 켜진다.
- [ ] 응답이 `ok`면 로그가 초록, `fail`이면 빨강이 되고 AlertDialog `보드가 오류를 알렸습니다`가 뜬다.
- [ ] 확인용으로 바꾼 `"on$index"`를 `"on $index"`로 되돌렸다.

2일차:

- [ ] [온습도 받기 시작]으로 입력 이력에 `시:분:초 [온도,습도]` 줄이 2줄 이상(시각이 약 3초 간격인 줄) 쌓이고 [중지]로 멈춘다(Fake면 입력 이벤트 `입력=1`/`입력=0` 2줄도 된다).
- [ ] 입력 이벤트와 `dht11` 응답이 입력 이력으로, `on`·`off` 응답은 명령 로그로 간다.
- [ ] 이력 줄을 누르면 `받은 시각: … · 값: …` Toast가 뜬다(실습 4번을 했으면).
- [ ] `끊김`이 되면 Toast와 [재연결]이 보이고, [재연결]로 `준비됨`까지 간다. 제어 화면에서 끊겨도 안내가 보인다.
- [ ] 연결을 시작하고 10초 안에 `준비됨`이 아니면 `연결 시간이 초과되었습니다`와 [다시 시도]가 보인다(실습 6번을 했으면).

두 날 공통:

- [ ] 캡처를 세로 화면에서 찍었고, 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [15주차 — 기말고사(개인 실기)와 과제 최종 제출](../week15_final_exam/README.md)이다.
2~14주차 범위로, 공개 starter(화면 / 제공 `bleuno/` / 상수)에서 권한 확인 흐름, 번호 토글(`send`)과 응답 표시, 이번 주에 만든 연결 시간 제한 안내를 혼자 구현하고, 개인 시연과 구술 질문에 답한다.
같은 주에 과제도 최종 제출한다. 13주차에 발표한 계획안대로 완성한 앱과 캡처 세트, 레포트를 낸다([과제 안내](../week13_ble_output/project_brief.md)).

## 공식 참고 자료

- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [색 리소스 — Android Developers](https://developer.android.com/guide/topics/resources/more-resources#Color)
- [대화상자 — Android Developers](https://developer.android.com/develop/ui/views/components/dialogs)
- [키-값 데이터 저장(SharedPreferences) — Android Developers](https://developer.android.com/training/data-storage/shared-preferences)
- [ListView — Android Developers](https://developer.android.com/reference/android/widget/ListView)
- [SimpleDateFormat — Android Developers](https://developer.android.com/reference/java/text/SimpleDateFormat)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [split — Kotlin 표준 라이브러리](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/split.html)
- [bleuno 펌웨어 — GitHub](https://github.com/gbox3d/bleuno)
