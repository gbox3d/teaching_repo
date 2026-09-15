# 14주차 — 입력 수신·끊김·재연결과 2차 과제 발표

## 이번 주 질문

> 보드가 돌려주는 온도·습도를 3초마다 받아 목록에 쌓고, 보드 전원이 꺼져 연결이 끊기거나 연결이 너무 오래 걸릴 때 앱이 알려 주고 다시 연결하게 하려면 어떻게 써야 할까?

13주차에는 제어 화면에서 보드에 `on 3`을 **보내고** JSON 대답을 명령 로그에 쌓았다. 그때 `result != null`로 걸러 낸 줄이 있었다. 가짜 보드가 10초마다 보내는 입력 이벤트 `{"event":"input","index":0,"value":1}`이다.
이번 주 1일차에는 `dht11`을 3초마다 보내 온도·습도 응답과 입력 이벤트를 **입력 이력** 목록에 시각과 함께 쌓고, 연결이 `끊김`이 되면 알리고 [재연결]하며, 연결을 시작한 뒤 10초 안에 `준비됨`이 되지 않으면 안내하고 끊는다.
2일차에는 4주차부터 만든 Smart I/O Controller로 **2차 과제를 발표**한다. 보드가 없어도 가짜 클라이언트(`useFake = true`)로 끝까지 만들고 시연할 수 있다.

## 학습 목표

1. `split(" ")`로 이력 한 줄을 나누고 `[0]`·`[1]`로 시각과 값을 꺼내며, 제공 helper `BleunoMessage.event(json)`·`BleunoMessage.value(json)`로 받은 JSON에서 값을 꺼낸다.
2. `inputJob = lifecycleScope.launch { while (isActive) { … send("dht11"); delay(3000) } }`로 온습도를 3초마다 요청하고, [중지]·끊김·`onStop`에서 `inputJob?.cancel()`로 멈춘다.
3. 받은 줄을 입력 이벤트·`dht11` 응답·명령 응답 세 가지로 가르고, `SimpleDateFormat` 틀로 시각을 붙여 입력 이력 `ListView`에 쌓는다.
4. 연결 상태가 `끊김`(`ConnState.LOST`)이면 Toast와 [재연결]을 보이고, SharedPreferences에 저장해 둔 주소로 `client.connect(lastAddress)`한다.
5. 연결을 시작하면 `launch` + `suspend fun`의 `delay(10000)`으로 10초 시간 제한을 걸고, 2~3분 시연과 코드 설명(파일·줄·한 문장)으로 2차 과제를 발표한다.

## 이번 주 결과물

```text
(1) 제어 화면 — 온습도를 받는 중 (Fake)

장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)
상태: 준비됨
[3            ]
LED (●)
[전체 끄기]
명령 로그
on 3
응답: {"result":"ok","ms":"led(s) on"}
[온습도 받기 시작] [중지]
입력 이력
12:00:03 [24.5,40.0]
12:00:06 [25.0,41.0]
12:00:09 [25.5,42.0]
[뒤로]

(2) 연결 화면 — 보드 전원이 꺼져 끊겼을 때

끊김
검색된 장치
ESP32_BLE_FAKE1 (00:11:22:33:44:01)
[연결]
[제어 화면]
[다시 시도]
[재연결] [끊김 시험]
연결이 끊겼습니다. [재연결]을 누르세요     ← Toast
```

14주차는 주차별 실습 점수 대상이 아니다. 이번 주 결과물은 **2차 과제(20점 = 발표 12 + 레포트 8)** 이며, 최종 앱의 캡처 세트와 2~3분 시연(권한 안내 → 장치 목록 → `준비됨` → LED on/off → 온습도 3회 수신 또는 입력 이벤트 3줄 → `끊김` + [재연결])이다.
조건은 [과제 안내](project_brief.md), 점수는 [채점표](rubric.md)에 있다. [끊김 시험]은 가짜 보드로 끊김을 만드는 시험용 버튼이며 실보드에서는 보이지 않는다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 60분 | 결과 |
|---|---|---|---|
| 1일차 | `split`·`[0]`·`[1]`와 `BleunoMessage.value/event`, `dht11` 3초마다 요청과 입력 이력, `끊김` 알림과 [재연결], 10초 연결 시간 제한, 발표 준비와 코드 설명 질문 예고 | 입력 이력 자리 → 받은 줄 가르기 → [온습도 받기 시작]·[중지] → 이력 줄 나누기 → [재연결]·[끊김 시험] → 시간 제한 → 캡처 세트와 2~3분 시연 리허설 | 최종 Smart I/O Controller와 시연 절차 |
| 2일차 | 진행 순서와 발표 정원, 채점표 다시 보기, 코드 설명 질문, 발표 전 점검과 실보드가 안 될 때 Fake로 바꾸기 | **발표**: 1인 5분(자리 잡기·보드 연결 확인 + 시연 2~3분 + 질문 1개) | 발표 완료, 레포트·소스 제출 |

발표 인원이 많아 60분 안에 끝나지 않는 분반은 조교 평가자를 늘려 조를 나눠 동시에 듣는다([발표 정원 계산](project_brief.md#발표-정원-계산)).

## 준비

- 13주차까지 만든 `SmartIO` 프로젝트(제어 화면에서 LED Switch가 `send`로 명령을 보내고, `onStart`에서 받은 응답을 로그에 쌓는 상태). 없으면 13주차 완성본(`examples/day2`)을 받아 시작한다.
- 에뮬레이터(AVD)는 **API 33 이상**. Fake로 입력 받기·끊김·재연결·시간 제한까지 모두 연습할 수 있다.
- 실보드로 하려면 Android 실기기와 수업 보드(파랑 깜빡임 상태)가 있어야 한다. 학생은 펌웨어를 고치거나 올리지 않는다.
- [bleuno README의 입력 이벤트 (가안)](../../bleuno/README.md#입력-이벤트-가안)과 [가짜 클라이언트의 동작](../../bleuno/README.md#7-fakebleunoclient의-동작)을 미리 읽어 온다.
- 다시 쓰는 것: 3주차 `?:`·회전, 6주차 `Job`·`cancel()`·`suspend fun`·`delay`, 7주차 collect 틀·`ConnState`·`.value`, 11주차 `ListView`·`ArrayAdapter`·`notifyDataSetChanged`·`setOnItemClickListener`·SharedPreferences, 12주차 `connect`·`useFake`, 13주차 `send`·`onMessage`·`BleunoMessage.result`·`listOf(…).contains(…)`.
- `AndroidManifest.xml`과 `build.gradle.kts`에 더할 것이 없다. `dht11` 보내기와 재연결은 10주차에 넣은 `BLUETOOTH_CONNECT` 권한 안에 있고, `ArrayAdapter`·`Job`·`SimpleDateFormat`은 4주차 의존성과 Android 기본 API에 들어 있다.
- 2차 과제 [안내](project_brief.md)와 [채점표](rubric.md)를 1일차 전에 읽어 온다.

## 이번 주 범위

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

앱이 보이지 않을 때 계속 받기, 자동으로 되풀이하는 재연결, 회전해도 입력 이력 남기기, 보드 여러 대 동시 연결은 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 발표 안내](lab.md)
- [예제 설명](examples/README.md)
- [2차 과제 안내](project_brief.md) — 필수 기능, 2~3분 시연 절차, 레포트, 발표 정원, 실물 장비가 안 될 때
- [2차 과제 채점표](rubric.md) — 발표 12 + 레포트 8
- 제공 라이브러리: [bleuno 패키지 README](../../bleuno/README.md) · [src 폴더](../../bleuno/src)
- 1일차 완성 코드(최종 앱): [ControlActivity.kt](examples/day1/ControlActivity.kt) · [MainActivity.kt](examples/day1/MainActivity.kt) · [activity_control.xml](examples/day1/activity_control.xml) · [activity_main.xml](examples/day1/activity_main.xml) · [strings.xml](examples/day1/strings.xml)
- 2일차는 발표라 새 코드가 없다.

## 완료 기준

아래 항목은 2차 과제 필수 기능이며, 2일차 발표와 레포트로 확인한다. 점수는 [채점표](rubric.md)로 매긴다.

- [ ] [권한 확인]에서 권한 안내(`권한 OK` 또는 거절 뒤 AlertDialog)가 보인다.
- [ ] [검색] → `ESP32_BLE…` 목록 → 줄 탭 → `연결 중`·`서비스 확인 중`·`준비됨`이 보이고, [해제]로 `연결 안 됨`이 된다.
- [ ] 제어 화면에서 명령 규약(`on 3`, `off -1` 등)대로 출력을 하나 이상 제어하고 응답이 로그에 보인다.
- [ ] [온습도 받기 시작]으로 입력 이력에 `시:분:초 [온도,습도]` 줄이 3줄 이상 쌓이고 [중지]로 멈춘다(Fake면 입력 이벤트 `입력=1`/`입력=0` 3줄도 된다).
- [ ] `끊김`이 되면 Toast와 [재연결]이 보이고, [재연결]로 `준비됨`까지 간다. 제어 화면에서 끊겨도 안내가 보인다.
- [ ] 연결을 시작하고 10초 안에 `준비됨`이 아니면 `연결 시간이 초과되었습니다`와 [다시 시도]가 보인다.
- [ ] 레포트에 넣을 캡처(권한·목록·준비됨·LED·입력 3줄·끊김+[재연결]·시간 초과)와 2~3분 시연 절차를 준비했다.
- [ ] 2일차에 차례대로 발표했고, 레포트와 소스를 [과제 안내](project_brief.md#레포트)대로 제출했다.
- [ ] 캡처·발표 화면에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [15주차 — 기말고사(개인 실기)](../week15_final_exam/README.md)이다.
2~14주차 범위로, 공개 starter(화면 / 제공 `bleuno/` / 상수)에서 권한 확인 흐름, 번호 토글(`send`)과 응답 표시, 이번 주에 만든 연결 시간 제한 안내를 혼자 구현하고, 개인 시연과 구술 질문에 답한다. 1일차 실습이 리허설이다.

## 공식 참고 자료

- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [GATT 서버에 연결 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server)
- [키-값 데이터 저장(SharedPreferences) — Android Developers](https://developer.android.com/training/data-storage/shared-preferences)
- [ListView — Android Developers](https://developer.android.com/reference/android/widget/ListView)
- [SimpleDateFormat — Android Developers](https://developer.android.com/reference/java/text/SimpleDateFormat)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [split — Kotlin 표준 라이브러리](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/split.html)
- [bleuno 펌웨어 — GitHub](https://github.com/gbox3d/bleuno)
