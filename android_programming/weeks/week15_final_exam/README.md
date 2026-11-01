# 15주차 — 기말고사(개인 실기)와 과제 최종 제출

## 이번 주 질문

> 2~14주에 만든 Smart I/O Controller의 **권한 확인**, **LED 명령과 응답**, **연결 시간 제한**을 혼자서 60분 안에 다시 쓸 수 있을까? 그리고 보드 앞에서 그 앱을 움직여 보이고, "이 콜백은 언제 불리나"에 한 문장으로 답할 수 있을까?

14주차에는 [입력 수신·끊김·재연결](../week14_ble_input_project/README.md)에서 `dht11` 온습도를 3초마다 받아 입력 이력에 쌓고, `끊김`이면 [재연결]을 보여 주고, 연결을 시작한 뒤 10초 안에 `준비됨`이 아니면 안내하고 끊었다. 그렇게 Smart I/O Controller가 완성되었다.
이번 주에는 새 문법을 배우지 않는다. 1일차에 시험 범위·채점표·starter 구조를 공개하고, 본시험과 같은 모양의 **공개 리허설**을 60분 동안 풀어 본다. starter는 14주차 최종 앱에서 세 기능의 본문만 비운 것이다.
2일차에는 시험 절차를 확인하고 보드를 받아 실기기로 점검한 뒤 **본시험**(비공개 문항)을 본다. 60분 동안 구현하면서, 좌석 순서대로 한 사람씩 보드 앞에서 **개인 시연과 구술**을 한다.

## 이번 주 할 일

이번 주에는 서로 다른 두 가지를 한다. 점수도 따로 매긴다.

- **기말 실기(20점 = 구현 15 + 시연 5)** — 시험 시간에 배포 starter의 빈 곳을 **그 자리에서** 채우는 개인 시험이다. 범위는 2~14주이고, 기준은 [15주 채점표](rubric.md)에 있다.
- **과제 최종 제출(20점)** — 12주 1일차에 공지하고 13주 2일차에 계획안을 발표한 뒤, 각자 만들어 온 **Smart I/O Controller 완성본**을 내는 것이다. 요구사항과 배점은 [13주 과제 안내](../week13_ble_output/project_brief.md)와 [13주 과제 채점표](../week13_ble_output/rubric.md)에 있다.

기말 실기는 시험 시간에 혼자 쓴 코드로 받고, 과제는 4주차부터 만들어 온 앱으로 받는다. 한쪽이 다른 쪽을 대신하지 못한다.
과제 최종 제출물은 **완성 앱(프로젝트), 캡처 세트, 레포트** 셋이다. 기말 주차에 내며, 정확한 마감 시각과 제출 위치는 **수업 공지**를 따른다.
보드가 없거나 실보드가 끝까지 되지 않으면 가짜 클라이언트(`useFake = true`)로 같은 흐름을 보여 내도 된다. 그 사실은 레포트에 적는다.

## 학습 목표

1. 채점표 구현 다섯 항목(UI·이벤트 / 상태 보존·StateFlow / 코루틴 timeout·취소·오류 / 권한·SharedPreferences / `send`·`onMessage`·재연결)이 SmartIO 코드의 어느 줄에서 드러나는지 말한다.
2. starter의 TODO(1)을 채워 `for (permission in PermissionHelper.required())`로 권한을 확인하고, 요청 창 → 결과 받기 → 거절 AlertDialog → 설정 화면으로 이어지는 권한 흐름을 완성한다.
3. TODO(2)를 채워 허용 번호(`listOf(0, 1, 2, 3).contains(index)` 또는 `-1`)만 `Bleuno.client?.send("on $index")`로 보내고, `onMessage { json -> }`로 받은 응답을 로그에 쌓아 오류면 빨간 글자와 창으로 알린다.
4. TODO(3)을 채워 `connectTimeoutJob`에 보관한 코루틴에서 `delay(10000)` 뒤에도 연결 중이면 안내하고 끊으며, Fake에서는 숫자를 잠시 줄여 확인한다.
5. 실보드 앞에서 출력 제어(LED)와 입력 수신(`dht11`)을 시연하고, 평가자가 가리킨 콜백이 언제 불리는지 한 문장으로 답한다.

## 이번 주 결과물

```text
(1) 리허설 완성 — 제어 화면 (Fake)

장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)
상태: 준비됨
[3            ]
LED (●)
[전체 끄기]
LED 0 밝기 ○─────
명령 로그
on 3
응답: {"result":"ok","ms":"led(s) on"}       ← 초록 글자
[온습도 받기 시작] [중지]
입력 이력
[뒤로]

(2) 리허설 완성 — 연결 화면에서 권한을 거절했을 때

권한이 필요합니다
장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.
                                  [취소] [설정으로]
```

15주차는 주차별 실습 점수 대상이 아니다. 리허설 결과는 자기 점검용이며 제출하지 않는다.
기말 실기는 **20점(기말 20%) = 구현 15 + 시연 5**다. 구현은 제출한 파일을 채점 PC에서 가짜 클라이언트(`useFake = true`)로 실행해 채점하고, 시연은 실보드 앞에서 본다. 기준은 [채점표](rubric.md)에 있다.
**과제 최종 제출 20점은 기말 실기와 다른 점수**다. 위 리허설 화면은 기말 실기 연습이고, 과제로 내는 것은 내가 만들어 온 완성 앱이다.

## 2일 수업 흐름

| 일차 | 설명·안내 30분 | 60분 | 결과 |
|---|---|---|---|
| 1일차 | 기말 범위(2~14주)와 두 날, 채점표(구현 15 + 시연 5, 기본점수 5점), starter 구조(화면 / 제공 `bleuno/` / 상수), 리허설 세 기능과 TODO 아홉 곳, starter에서 지키는 세 가지 | **공개 리허설**: 14주차 `SmartIO`에 starter 두 파일 넣기 → TODO(1) 권한 → TODO(2) LED·응답 → TODO(3) 시간 제한 → 점검표 → `rehearsal_solution`과 비교해 자기 채점 | 14주차 최종 앱과 같게 동작하는 리허설 앱 |
| 2일차 | 리허설에서 막힌 곳, 시험 순서와 제출본 기준, 허용 자료와 장애 절차, 보드 배부와 실기기 점검, 시연 순서와 구술 한 문항 | **본시험**: 문제1 구현(비공개 문항, 리허설과 같은 모양, Fake로 실행) + 문제2 좌석 순서대로 개인 시연·구술 | 제출한 코드 두 파일, 시연·구술 기록 |

각 수업은 `설명·안내 30분 + 60분`이다. 1일차 60분은 점수가 없는 연습이고, 2일차 60분이 시험이다.

## 준비

- 14주차까지 만든 `SmartIO` 프로젝트. 없거나 실행되지 않으면 14주차 완성본([examples/day2](../week14_ble_input_project/examples/day2))을 받아 시작한다. 리허설 starter는 이 프로젝트에 두 파일만 덮어쓴다.
- 에뮬레이터(AVD)는 **API 33 이상**. 리허설과 본시험 구현은 Fake로 끝까지 할 수 있다.
- 2일차 시연용 **Android 실기기**(Android 12 이상 권장)와 USB 케이블. 없으면 1일차 전에 대여 단말을 신청한다. 보드는 2일차에 좌석별로 나눠 준다. 학생은 펌웨어를 고치거나 올리지 않는다.
- 다시 읽어 둘 것: 10주차 권한 요청 틀과 AlertDialog, 13주차 `send`·`onMessage`·`BleunoMessage.result`, 14주차 허용 번호 검사와 오류 색·대화상자·`connectTimeoutJob`·`waitConnectTimeout()`, [bleuno README의 명령과 응답](../../bleuno/README.md#2-명령과-응답).
- `AndroidManifest.xml`과 `build.gradle.kts`에 더할 것이 없다. 리허설 starter의 Manifest·XML·`bleuno/`는 14주차 2일차 완성본(`examples/day2`)과 글자 단위로 같다.

## 이번 주 범위

이번 주에는 새 문법이 없다. 아래 표가 **시험 범위(2~14주)** 이고, 리허설과 본시험은 이 안에서만 낸다.

| 문법·API (처음 배운 주) | 이번 주에 알아둘 뜻 | 채점표 항목 |
|---|---|---|
| `setOnClickListener { }`, `setOnCheckedChangeListener { _, isChecked -> }` (2·4주) | 버튼을 누를 때, Switch를 켜고 끌 때마다 중괄호 안을 실행한다 | UI·이벤트 |
| `text.toString()`, `isEmpty()`, `.toInt()`, `"on $index"` (4주) | 입력 글자를 꺼내 비었는지 보고, 숫자로 바꾸고, 명령 글자에 넣는다. 빈 칸 검사를 `toInt()`보다 먼저 한다 | UI·이벤트 |
| `Toast`(3주), `isEnabled`·`visibility`(5주) | 짧은 알림, 버튼 켜고 끄기, 보이고 숨기기 | UI·이벤트 |
| 회전하면 Activity가 다시 만들어진다 (3주) | 화면이 새로 만들어져도 연결 상태는 `Bleuno.client`에 남는다 | 상태 보존·StateFlow |
| `repeatOnLifecycle` 틀 안의 `client.connectionState.collect { state -> }`, `ConnState`, `when` (7·12주) | **틀**. 화면이 보일 때 연결 상태를 받아 글자와 버튼을 고친다. starter에 완성되어 있다 | 상태 보존·StateFlow |
| `lifecycleScope.launch { }`, `suspend fun`, `delay(10000)` (6주) | 코루틴을 시작하고, 멈췄다 이어지는 함수 안에서 10초 기다린다 | 코루틴 timeout·취소·오류 |
| `private var connectTimeoutJob: Job? = null`, `connectTimeoutJob?.cancel()` (6주, 3주 `?.`) | 시작한 코루틴을 보관했다가 새로 걸기 전에 앞 것을 멈춘다 | 코루틴 timeout·취소·오류 |
| `client.connectionState.value`, `listOf(ConnState.CONNECTING, ConnState.DISCOVERING).contains(state)` (7·13·14주) | 지금 연결 상태 값을 읽어 "아직 연결 중인가"를 확인한다 | 코루틴 timeout·취소·오류 |
| `for (permission in PermissionHelper.required())`, `ContextCompat.checkSelfPermission(…)` (6·10·12주) | 필요한 권한을 하나씩 꺼내 허용됐는지 본다. 하나라도 아니면 그 자리에서 `return false` | 권한·SharedPreferences |
| `registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { _ -> }`, `launch(…)` (10주) | 요청 창 틀. 클래스 안(onCreate 밖)에 만들어 두고, 버튼에서는 `launch`만 부른다. 고른 뒤 `{ _ -> }`가 불린다 | 권한·SharedPreferences |
| `AlertDialog.Builder(this)`, `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))` (10주) | 거절했을 때 안내 창과, 이 앱의 정보 화면을 여는 암시적 Intent | 권한·SharedPreferences |
| `getSharedPreferences("smartio", MODE_PRIVATE)`, `putString`, `getString(…) ?: ""` (11주) | 마지막 장치 이름·주소를 저장하고 꺼낸다. starter에 완성되어 있다 | 권한·SharedPreferences |
| `Bleuno.client?.send("on $index")`, `onMessage { json -> }` / `onMessage(null)` (13주) | 명령 한 줄을 보내고, 응답 JSON 한 줄을 `onStart`~`onStop` 사이에 받는다 | `send`·`onMessage`·재연결 |
| `BleunoMessage.result(json)` (13주) | 응답에서 `ok`·`err`·`fail`을 꺼낸다 | `send`·`onMessage`·재연결 |
| `BleunoMessage.message(json)`, `ContextCompat.getColor(this, R.color.log_error)` (14주) | 오류 설명을 꺼내고 로그 글자색을 바꾼다 | `send`·`onMessage`·재연결 |
| `listOf(0, 1, 2, 3).contains(index)` (13주) | 보드에 보내도 되는 LED 번호인지 확인한다 | `send`·`onMessage`·재연결 |
| `ConnState.LOST`, `client.connect(lastAddress)` (14주) | 끊김이면 저장해 둔 주소로 다시 연결한다. starter에 완성되어 있다 | `send`·`onMessage`·재연결 |
| `dht11`, `split(" ")`, `BleunoMessage.value(json)` (14주) | 온습도를 받아 입력 이력에 쌓는다. starter에 완성되어 있고 **시연**에서 쓴다 | 시연(입력 수신) |

펌웨어 수정, Service·Fragment(9주 실습), RecyclerView, 보드 여러 대 동시 연결은 범위가 아니다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [리허설과 본시험 안내](lab.md) — 시간표, 허용 자료, 장애가 나면, 시연 정원 계산, 막혔을 때
- [예제 설명](examples/README.md)
- [채점표](rubric.md) — 기말 실기의 구현 15 + 시연 5, 기본점수 운영 메모, 기록 양식
- [13주 과제 안내](../week13_ble_output/project_brief.md) · [13주 과제 채점표](../week13_ble_output/rubric.md) — 과제 최종 제출의 요구사항과 20점 배분
- 리허설 시작 코드: [MainActivity.kt](examples/rehearsal_starter/MainActivity.kt) · [ControlActivity.kt](examples/rehearsal_starter/ControlActivity.kt) (나머지 15개 파일은 14주차 2일차 완성본 `examples/day2`와 같다)
- 리허설 완성 코드(먼저 혼자 풀고 비교): [MainActivity.kt](examples/rehearsal_solution/MainActivity.kt) · [ControlActivity.kt](examples/rehearsal_solution/ControlActivity.kt)
- 제공 라이브러리: [bleuno 패키지 README](../../bleuno/README.md)

## 이 폴더에 넣지 않는 것

- 본시험 문항·본시험 starter·정답과 채점 사례
- 학생 코드, 이름·학번·점수, 장애 기록지

본시험 문항은 리허설과 같은 모양으로 따로 만들어 시험 시작 때 배포한다.

## 완료 기준

- [ ] 리허설 앱에서 권한이 없을 때 [권한 확인] → 요청 창 → 허용하면 `권한 OK`, 거절하면 `권한이 필요합니다` 창 → [설정으로]가 이 앱의 정보 화면을 연다.
- [ ] `준비됨` 제어 화면에서 `3` → Switch 켜기로 `on 3`과 `응답: {"result":"ok","ms":"led(s) on"}`이 쌓이고, 빈 칸이면 `LED 번호를 입력하세요`, `9`면 `허용되지 않는 번호`가 뜬다.
- [ ] `delay`를 잠시 1000으로 줄였을 때 `연결 시간이 초과되었습니다`가 뜨는 것을 확인하고 10000으로 되돌렸다.
- [ ] 점검표와 [채점표](rubric.md)로 자기 채점을 하고 완성본과 다른 줄을 찾았다.
- [ ] 2일차 설명 시간에 실기기에서 내 보드와 `준비됨`, LED 켜기, 입력 이력 2줄을 확인했다.
- [ ] 2일차 본시험 코드 두 파일을 시간 안에 제출하고, 차례에 시연과 구술을 마쳤다.
- [ ] 과제 최종 제출물 세 가지(완성 앱, 캡처 세트, 레포트)를 공지한 마감까지 공지한 제출 위치에 냈다. 실보드가 되지 않아 Fake로 보인 부분은 레포트에 적었다.

## 다음 수업 연결

15주차가 이 과목의 마지막 주다. 다음 수업은 없다. 기말 실기와 과제 최종 제출을 모두 내면 이 과목의 평가가 끝난다.
4주차 빈 화면에서 시작한 Smart I/O Controller는 화면·Intent(4주) → 스레드·코루틴(5·6주) → ViewModel·StateFlow(7주) → 권한(10주) → 목록·저장(11주) → BLE 검색·명령·입력(12~14주)을 거쳐 완성되었다. 시험이 끝나면 [bleuno README의 명령 표](../../bleuno/README.md#2-명령과-응답)에서 `blink`·`about`도 보내 보자. 학기 전체 흐름은 → [전체 주차 색인](../README.md)에서 다시 볼 수 있다.

## 공식 참고 자료

- [앱 권한 요청 — Android Developers](https://developer.android.com/training/permissions/requesting)
- [블루투스 권한 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [BLE 데이터 전송 — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
- [수명 주기 인식 코루틴 — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [bleuno 펌웨어 — GitHub](https://github.com/gbox3d/bleuno)
