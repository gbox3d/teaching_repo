# 15주차 실습 — 공개 리허설과 본시험

1일차 60분은 점수가 없는 **공개 리허설**이다. starter는 14주차 최종 앱에서 세 기능의 본문만 비운 것이라 빌드·실행되고, `// TODO` 아홉 곳만 비어 있다. 2일차 **본시험**도 같은 모양이다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있지만, 리허설은 시험 연습이므로 **따라하기를 덮고 먼저 혼자** 푼다. 막히면 이 문서의 힌트 → [막혔을 때](#막혔을-때) → 따라하기 순서로 연다.
에뮬레이터는 API 33 이상을 쓰고, 연결 화면의 `private val useFake = true`는 그대로 둔다.

## 1일차 — 공개 리허설 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 14주차 `SmartIO`에 starter 두 파일을 넣고 실행한다(따라하기 1~2단계) |
| 5–10분 | TODO 아홉 곳을 찾아 아래 2번 표를 채운다 |
| 10–25분 | TODO(1) 권한 확인 흐름 네 곳 |
| 25–40분 | TODO(2) LED 번호 토글과 응답 표시 세 곳 |
| 40–50분 | TODO(3) 연결 시간 제한 두 곳, 숫자를 잠시 줄여 확인하고 되돌리기 |
| 50–55분 | 저장 → 다시 실행 → 6번 점검표 |
| 55–60분 | `rehearsal_solution`과 비교하고 채점표로 자기 채점한다 |

5분부터는 본시험 시간 예산(열기 → 기능 셋 → 점검 → 다시 실행 → 제출)을 줄인 순서다. 시계를 보면서 푼다.

### 1. starter 넣고 실행하기

1. 14주차까지 만든 `SmartIO` 프로젝트를 연다. 없거나 실행되지 않으면 [14주차 완성본](../week14_ble_input_project/examples/day1/MainActivity.kt)이 들어 있는 `examples/day1` 파일로 먼저 맞춘다.
2. `MainActivity.kt`와 `ControlActivity.kt`의 내용을 [rehearsal_starter/MainActivity.kt](examples/rehearsal_starter/MainActivity.kt)·[rehearsal_starter/ControlActivity.kt](examples/rehearsal_starter/ControlActivity.kt)로 모두 바꾼다. 다른 파일은 14주차 그대로 둔다.
3. Run ▶으로 실행하고 아래를 확인한다.

| 조작 | 보여야 할 것 |
|---|---|
| 앱 시작 | 14주차와 같은 연결 화면(`마지막 장치: …`, [끊김 시험] 회색) |
| [권한 확인] | **아무 일도 없다** |
| [검색] → `ESP32_BLE_FAKE1` 줄 탭 | 요청 창 없이 검색된다. `연결 중` → `서비스 확인 중` → `준비됨` |
| [제어 화면] → `3` → LED Switch 켜기 | Switch 모양만 바뀌고 명령 로그·Toast가 없다 |
| [전체 끄기] | 명령 로그에 `off -1`. 그 아래 `응답:` 줄은 붙지 않는다 |

starter는 **빌드·실행은 되고 기능만 비어 있는** 상태다. 시험 당일 받는 starter도 이렇게 먼저 확인한다.

- Android Studio가 import 네 줄을 회색으로 보여 준다(`MainActivity.kt`의 `android.net.Uri`·`kotlinx.coroutines.delay`, `ControlActivity.kt`의 `androidx.appcompat.app.AlertDialog`·`androidx.core.content.ContextCompat`). TODO를 채우면 쓰이는 줄이므로 **지우지 않는다.** **Code › Optimize Imports**도 누르지 않는다.

### 2. TODO 아홉 곳 찾고 나누기

메뉴 **View › Tool Windows › TODO**를 열면 TODO가 모여 보인다. 줄을 더블클릭하면 그 자리로 간다. 각 TODO를 읽고 표를 채운다.

| TODO | 파일 | 함수·리스너(주석 번호) | starter 안에서 비슷한 모양의 코드 |
|---|---|---|---|
| (1) |  |  |  |
| (1) |  |  |  |
| (1) |  |  |  |
| (1) |  |  |  |
| (2) |  |  |  |
| (2) |  |  |  |
| (2) |  |  |  |
| (3) |  |  |  |
| (3) |  |  |  |

- 채우는 순서는 **불리는 함수 → 부르는 곳**이다. 예를 들어 13번 `hasBlePermissions()`를 먼저 채우고, 그것을 부르는 12번 [권한 확인]을 나중에 채운다.
- `hasBlePermissions()`의 `return true`, `isAllowedIndex()`의 `return false`는 **남긴다.** TODO 주석만 지우고 그 위에 쓴다.

### 3. TODO(1) — 권한 확인 흐름

네 곳을 아래 순서로 채운다. 한 곳을 채울 때마다 **Build › Make Project**로 빌드되는지 본다.

1. **13번 `hasBlePermissions()`**: `for`로 `PermissionHelper.required()`의 권한을 하나씩 꺼낸다. `ContextCompat.checkSelfPermission(this, 권한)`이 `PackageManager.PERMISSION_GRANTED`가 아니면 그 자리에서 `false`를 돌려준다.
   - 22번 [연락처 보기]의 `checkSelfPermission` 줄이 같은 모양이다. `for (i in 5 downTo 1)`(6주차)처럼 `for (permission in …)`으로 목록을 돈다.
2. **14번 `showPermissionDialog()`**: 40번 `showLocationDialog()`와 같은 모양으로 쓴다. 제목 `권한이 필요합니다`, 문구 `장치를 검색하고 연결하려면 권한이 필요합니다. 설정 › 권한에서 허용해 주세요.`, 버튼 [설정으로]·[취소].
   - [설정으로]는 `Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName"))`로 이 앱의 정보 화면을 연다(10주차).
   - 아직 이 함수를 부르는 곳이 비어 있어 화면은 바뀌지 않는다. 빌드만 확인한다.
3. **`permissionLauncher`의 `{ _ -> }`**: 13번으로 권한을 다시 확인해 모두 허용이면 Toast `권한 OK`, 아니면 14번을 부른다.
   - 바로 아래 `contactsLauncher`가 같은 모양이다. 요청 창 틀은 이미 클래스 안에 있으니 새로 만들지 않는다.
4. **12번 [권한 확인]**: 13번이 `true`면 Toast `권한 OK`, 아니면 `permissionLauncher.launch(PermissionHelper.required())`.
   - 25번 [검색]의 첫 가지에 같은 `launch` 줄이 있다. 리스너 줄(`binding.permissionButton.setOnClickListener {`)은 starter에 있으니 한 줄 더 쓰지 않는다.

권한을 끈 상태는 에뮬레이터에서 앱 아이콘을 길게 누르고 **앱 정보 › 권한 › 근처 기기 › 허용 안함**으로 만든다.

| 조작 | 예상 | 내 앱 (O/X) |
|---|---|---|
| 권한을 끈 채 [권한 확인] | 시스템의 `근처 기기` 권한 요청 창 |  |
| 요청 창에서 허용 | Toast `권한 OK` |  |
| 다시 [권한 확인] | 요청 창 없이 Toast `권한 OK` |  |
| 권한을 다시 끄고 [권한 확인] → 거절 | `권한이 필요합니다` 창, [취소]·[설정으로] |  |
| [설정으로] | Smart I/O Controller의 앱 정보 화면 |  |

- 요청 창에서 거절한 뒤에는 Android가 요청 창을 더 띄우지 않고 곧바로 결과를 돌려주기도 한다. 앱 정보에서 끈 상태는 한 번, 새로 설치한 상태는 두 번 거절하면 그다음 [권한 확인]부터 요청 창 없이 곧바로 `권한이 필요합니다` 창이 뜬다(Android 14 에뮬레이터에서 확인). 앱 정보에서 권한을 다시 바꾸면(`허용` → `허용 안함`) 요청 창이 다시 뜬다.
- 권한 흐름에는 Logcat `tag:BLE` 줄이 없다.

### 4. TODO(2) — LED 번호 토글과 응답 표시

1. **12번 `isAllowedIndex()`**: `listOf(0, 1, 2, 3).contains(index)`이면 `true`, `index == -1`이어도 `true`. 맨 아래 `return false`는 남긴다.
2. **2번 LED Switch**: 순서는 **빈 칸 → 허용 번호 → 켜기/끄기**다.
   - 빈 칸이면 Toast `LED 번호를 입력하세요`. 허용 번호가 아니면 Toast `허용되지 않는 번호`.
   - 켜면 `"on 번호"`, 끄면 `"off 번호"`를 `Bleuno.client?.send`로 보내고, 보낸 명령을 `logText`에 한 줄 `append`한 뒤 `pauseButtons()`를 부른다. 7번 [전체 끄기]가 같은 모양이다.
   - `isAllowedIndex`는 숫자를 받는다. 칸의 글자는 `.toInt()`로 바꿔 넘긴다(4주차).
3. **8번 응답 가지** `} else if (result != null) {` 안: `logText`에 `응답: 받은 JSON` 한 줄을 `append`한다. `result`가 `"ok"`가 아니면 로그 글자를 `R.color.log_error`로 바꾸고 AlertDialog(제목 `보드가 오류를 알렸습니다`, 문구 `응답: result · 설명`, [확인])로 알린다. `"ok"`면 `R.color.log_ok`로 되돌린다.
   - 설명은 `BleunoMessage.message(json)`이 준다. `String?`이라 `?: ""`로 받는다(3주차).

| 조작 (`준비됨` → [제어 화면]) | 예상 | 내 앱 (O/X) |
|---|---|---|
| 번호 칸을 비운 채 Switch | Toast `LED 번호를 입력하세요` |  |
| `9` → Switch | Toast `허용되지 않는 번호`, 명령 로그 새 줄 없음 |  |
| `3` → Switch 켜기 | `on 3` → 약 0.3초 뒤 `응답: {"result":"ok","ms":"led(s) on"}` 초록 글자. Switch·[전체 끄기]가 0.3초 동안 회색 |  |
| Switch 끄기 | `off 3` → `응답: {"result":"ok","ms":"led(s) off"}` |  |
| Logcat `package:mine tag:BLE` | `writeCharacteristic(가짜): "on 3"` → `onCharacteristicChanged(가짜): {"result":"ok","ms":"led(s) on"}` |  |

- Fake에서는 오류 응답이 나올 조작이 거의 없다. 빨간 글자와 창을 보고 싶으면 `send` 줄을 잠시 `"on$index"`로 바꿔 실행해 보고 **되돌린다**([막혔을 때](#막혔을-때) 표의 띄어쓰기 줄).
- `9` 같은 번호는 Fake에서만 해 본다. 보드는 번호 범위를 검사하지 않는다.

### 5. TODO(3) — 연결 시간 제한

1. **50번 `startConnectTimeout()`**: `connectTimeoutJob`에 앞에서 건 코루틴이 있으면 `?.cancel()`로 먼저 멈춘다. `lifecycleScope.launch { }`로 새로 시작해 그 `Job`을 `connectTimeoutJob`에 보관하고, 안에서 51번을 부른다.
2. **51번 `waitConnectTimeout()`**: `delay(10000)` 뒤 `client.connectionState.value`를 읽는다. 그 값이 `ConnState.CONNECTING`·`ConnState.DISCOVERING` 가운데 하나면(52번과 같은 `listOf(…).contains(…)`) Toast `연결 시간이 초과되었습니다`, `client.disconnect()`, 그리고 `stateText`를 `연결 시간 초과 — [다시 시도]를 누르세요`로, `scanProgress` 숨기기, [검색] 켜기, [다시 시도] 보이기.
   - 51번은 이미 `suspend fun`이고, 그 안의 `this`는 Activity라 Toast에 그대로 쓴다. 50번의 `launch { }` 안에 Toast를 직접 쓰지 않는다.
3. Fake는 약 2초 만에 `준비됨`이 되므로 10초를 기다려도 안내가 **뜨지 않는 것이 정상**이다. 51번의 `delay(10000)`을 잠시 `delay(1000)`으로 바꿔 확인한다.

| 조작 (`delay(1000)`으로 바꾼 상태) | 예상 | 내 앱 (O/X) |
|---|---|---|
| [검색] → `ESP32_BLE_FAKE1` 줄 탭 | 약 1초 뒤 상태 `연결 시간 초과 — [다시 시도]를 누르세요`, [검색] 켜짐, [다시 시도] 보임. Toast `연결 시간이 초과되었습니다`는 먼저 뜬 `선택: …` Toast가 사라진 뒤(줄을 누르고 약 2~3초 뒤) 뜬다 |  |
| 줄 탭 직후 곧바로 회전 | 약 1초 뒤 같은 안내. 52번이 시간 제한을 다시 건다 |  |
| Logcat `package:mine tag:BLE` | `connectGatt(가짜): 00:11:22:33:44:01` → `disconnect(가짜) → 연결 안 됨` |  |

4. 확인이 끝나면 **`delay(10000)`으로 되돌린다.**

### 6. 점검표

저장(Ctrl+S, 맥 ⌘+S)하고 Run ▶으로 다시 실행한 뒤 위에서부터 차례로 해 본다. 회전은 에뮬레이터 창 옆 도구 막대의 회전 버튼으로 한다.

| 조작 | 보여야 할 것 | 내 앱 (O/X) |
|---|---|---|
| 권한을 허용한 채 [권한 확인] | 요청 창 없이 `권한 OK` |  |
| 권한을 끈 채 [권한 확인] → 거절 → [설정으로] | `권한이 필요합니다` 창 → 앱 정보 화면 |  |
| [검색] → `ESP32_BLE_FAKE1` 줄 탭 | `연결 중` → `서비스 확인 중` → `준비됨`. 10초가 지나도 안내 없음 |  |
| `준비됨`에서 회전 | 그대로 `준비됨`, [해제]·[제어 화면] 켜짐 |  |
| [제어 화면] → 빈 칸 / `9` / `3` Switch | 4번 표와 같다 |  |
| [뒤로] → [끊김 시험] → [재연결] | `끊김`과 Toast → `준비됨` |  |
| 장치 이름이 있는 채로 [연결] → [뒤로] → 앱을 완전히 닫고 다시 실행 | `마지막 장치: ESP32_BLE_FAKE1 (00:11:22:33:44:01)` |  |
| 51번 코드 | `delay(10000)`으로 되돌려 두었다 |  |

X가 있으면 [막혔을 때](#막혔을-때)부터 본다.

### 7. 자기 채점

[채점표](rubric.md)의 구현 15점(U·S·C·P·M 기준)으로 매긴다. 시연 5점은 2일차에 본다.
그다음 [rehearsal_solution/MainActivity.kt](examples/rehearsal_solution/MainActivity.kt)·[rehearsal_solution/ControlActivity.kt](examples/rehearsal_solution/ControlActivity.kt)와 내 코드를 비교해, 점수를 잃은 기준의 원인이 된 줄을 찾아 적는다. 완성본은 14주차 최종 앱과 글자 단위로 같다.

## 2일차 — 본시험 (60분)

설명 15–22분에 보드·실기기 점검([따라하기 17단계](walkthrough.md#17-실기기와-내-보드-점검))을 마친 뒤 시작한다. 문항지와 starter는 시작할 때 받는다.

| 시간 | 할 일 |
|---|---|
| 0–5분 | starter를 열고 Sync가 끝나면 에뮬레이터로 실행해 첫 화면 확인, 문항지와 TODO 읽기 |
| 5–20분 | 문항지의 기능 1 |
| 20–35분 | 문항지의 기능 2 |
| 35–45분 | 문항지의 기능 3 |
| 45–52분 | 점검표(Fake). 시간 제한은 숫자를 잠시 줄여 확인하고 되돌린다 |
| 52–55분 | 저장 → 다시 실행 |
| 55–60분 | 코드 두 파일 제출 |

좌석 순서대로 평가자가 오면 그때 시연한다(3번). 시연은 본시험 5–55분에 하고, 3분은 모두 똑같이 한 번 쓰므로 제출 마감은 모두 60분이다.

### 1. 시작 전 점검

- [ ] 실기기에 내 `SmartIO`(`useFake = false`)가 설치되어 있고, 내 보드로 `준비됨`·LED 켜기와 `응답:` 줄·입력 이력 2줄을 확인했다. 리허설 TODO(1)·(2)를 끝내지 못했으면 두 파일을 `rehearsal_solution`으로 바꿔 설치했다.
- [ ] 에뮬레이터가 켜져 있고 Android Studio의 Run 대상이 에뮬레이터다.
- [ ] 휴대폰은 가방에 넣었다(시연 기기는 책상 위에 앱 화면만). 브라우저에는 [허용 자료](#허용-자료) 탭만 있다.
- [ ] [장애가 나면](#장애가-나면) 손을 든다는 것을 안다.

### 2. 본시험 규칙

- 문항지에 적힌 문구·숫자·번호 규칙을 그대로 쓴다. 리허설과 다른 곳에 밑줄을 긋고 시작한다.
- `activity_main.xml`·`activity_control.xml`·`strings.xml`·`colors.xml`·`AndroidManifest.xml`·`bleuno/`는 고치지 않는다. 채점에는 starter 원본이 쓰인다.
- starter의 회색 import와 `return` 줄은 지우지 않는다.
- 시간 제한 숫자를 줄여 확인했다면 제출 전에 문항지의 숫자로 되돌린다.

### 3. 시연 차례가 오면

평가자가 자리에 오면 저장(Ctrl+S)하고 편집을 멈춘다. 시연은 한 사람 3분이다.

1. 시연 기기의 `SmartIO` → [검색] → **내 보드 이름** 줄 탭 → `준비됨` → [제어 화면].
2. **출력 제어**: LED 번호 → Switch 켜기 → 보드 LED가 켜진다 → Switch 끄기(또는 [전체 끄기]) → 명령 로그의 응답 줄을 가리킨다. 응답 줄이 없으면 O2를 받지 못하므로, 시연 앱은 설명 시간 점검 때 응답이 붙는 앱(내가 끝낸 리허설 또는 `rehearsal_solution`)으로 설치해 둔다.
3. **입력 수신**: [온습도 받기 시작] → 입력 이력 2줄 → [중지].
4. **구술**: 평가자가 본시험 프로젝트 코드에서 콜백 하나를 가리키면 "언제 불리는지" 한 문장으로 답한다.

- 보드가 검색되지 않으면 손을 든다. 강의자가 확인하면 보드를 바꾸거나 에뮬레이터의 Fake로 시연한다.
- 끝나면 곧바로 본시험으로 돌아간다. 제출 마감은 모두 60분이다. 장비 장애나 평가자 사정으로 3분을 넘긴 몫만 장애 기록지에 적고, 60분 뒤 같은 자리에서 그만큼 이어서 한다.

### 4. 시간이 모자랄 때

- 기능 하나에 정한 시간이 지나면 다음 기능으로 넘어간다. 기능마다 따로 확인되는 기준이 있다.
- 빨간 줄이 사라지지 않는 줄은 앞에 `//`를 붙여 두고 넘어간다. **빌드되는 상태**를 유지해야 실행해서 점수를 받는다.
- 빌드가 되지 않아도 TODO 자리에 쓴 코드는 [기본점수](rubric.md#기본점수-5점--구현-시도-흔적-운영-메모) 판단에 쓰인다. 그래도 빌드되는 제출이 점수를 더 받는다.

### 5. 제출

제출물은 `MainActivity.kt`와 `ControlActivity.kt` 두 파일이다. 캡처는 문항지가 지정할 때만 낸다. 제출하기 전에 저장 → Run ▶ → 점검표를 한 번 더 한다.
파일은 Project 창에서 우클릭 › **Open In › Explorer**(맥 **Finder**)로 찾는다([따라하기 20단계](walkthrough.md#20-저장다시-실행제출)).

## 시험 운영 — 허용 자료·장애·시연 정원

시험 공지(LMS)가 이 절과 다르면 **공지가 우선**한다.

### 허용 자료

| 허용 | 금지 |
|---|---|
| 이 과목 공개 교재(2~15주 README·slides·walkthrough·lab·examples, 리허설 완성본과 bleuno README 포함)를 브라우저로 보기 | 생성형 AI(ChatGPT·Gemini·Copilot 등). 브라우저와 Android Studio의 AI 도우미 모두 |
| 내가 만든 `SmartIO` 프로젝트를 Android Studio로 열어 보기 | 메신저·메일·클라우드 드라이브로 코드나 파일을 주고받기 |
| Android Developers·Kotlin 공식 문서 | 다른 사람과 대화하기, 다른 사람의 화면 보기 |
| Android Studio 기본 기능: 자동 완성, Alt+Enter(맥 ⌥+Enter) import, 오류 메시지, Logcat | 휴대폰 사용(시연 기기는 시연 때만), 검색 사이트·블로그·질문 사이트 |

금지 행동이 확인되면 감독자가 시각과 내용을 기록하고, 처리는 대학 규정과 시험 공지를 따른다.

### 장애가 나면

**먼저 손을 든다.** 조교가 장애 기록지에 시각·증상·조치를 적는다. 장애로 잃은 시간은 기록을 근거로 연장한다.
빨간 줄, 빌드 오류, 앱이 멈추는 것처럼 **내 코드 때문에 생긴 문제는 장애가 아니다.** 학생은 펌웨어를 고치거나 다시 올리지 않는다.

| 상황 | 대체 절차 |
|---|---|
| 에뮬레이터가 켜지지 않거나 멈춘다 | Device Manager에서 그 기기의 ⋮ › **Cold Boot Now**. 5분 안에 안 되면 예비 PC로 옮기고, 작성 중인 두 파일은 조교 USB로 옮긴다 |
| 코드를 고치기 전부터 Sync·빌드가 실패한다 | starter 배포본 문제일 수 있다. 조교가 USB의 starter 복사본을 다시 주거나 자리를 옮긴다 |
| 보드가 파랑으로 깜빡이지 않거나 검색에 나오지 않는다 | 강의자가 확인해 보드를 바꾼다. 해결되지 않으면 시연을 에뮬레이터 Fake로 본다(장애 기록) |
| 실기기가 Android Studio에 잡히지 않는다 | 케이블·USB 디버깅을 조교가 확인하고, 안 되면 대여 단말로 바꾼다 |
| LMS에 올라가지 않는다 | 조교 USB에 `학번_파일이름`으로 복사하고 기록지에 시각을 적는다. 이 복사본을 제출본으로 인정한다 |

### 시연 정원 계산

- 시연 구간은 본시험 5–55분이다(0–5분은 열기, 55–60분은 제출). 한 분반의 인원 `N`, 동시에 시연을 보는 평가자 수 `E`, 한 사람 시연 시간 `D`(분)로 `T_demo = ceil(N / E) × D`를 계산해 **50분을 넘지 않는지** 시험 전에 확인한다. 기본안은 `D = 3`이다(예: `E = 2`이면 `N`은 32명까지, `E = 3`이면 48명까지).
- 50분을 넘으면 평가자(조교)를 늘려 병렬로 본다. 그래도 맞지 않으면 모든 학생에게 같은 조건의 별도 시연 시간을 미리 공지한다.
- 시연 D분은 모든 학생이 똑같이 한 번 쓰므로 제출 마감은 모두 60분이다. 장비 장애나 평가자 사정으로 D분을 넘긴 몫만 장애 기록지에 적고, 60분 뒤 같은 자리에서 그만큼 이어서 한다. 순서가 밀려 55분까지 시연하지 못한 학생은 제출 뒤 같은 자리에서 시연한다.
- 순서나 대기 때문에 어떤 학생의 시연 시간 `D`나 구현 시간을 줄이지 않는다. 시연 순서표와 `N`·`E`·`D`는 시험 공지로 확정한다.

## 막혔을 때

오류 문구는 Android Studio의 Build 창에 나오는 줄이다. `MainActivity.kt:줄:열`의 줄 번호는 내 코드에 따라 다르다.
빌드는 되지만 실행에서 드러나는 증상은 Android 14 에뮬레이터에서 확인한 모습이라, 기기에 따라 조금 다르게 보일 수 있다.

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'delay'.` (51번 `delay(10000)` 줄) | 회색이던 `import kotlinx.coroutines.delay`가 자동 정리(**Optimize Imports**)로 지워졌다. 빨간 `delay`에 커서를 두고 Alt+Enter(맥 ⌥+Enter) → Import. `Uri`·`AlertDialog`·`ContextCompat`도 같은 이유로 지워질 수 있고, 같은 방법으로 되살린다 |
| `Unresolved reference 'permisionButton'.` | `binding.` 뒤 이름이 `activity_main.xml`의 id `permissionButton`과 다르다(`s`가 두 개). starter에 이미 있는 리스너 안에 채우고, 리스너 줄을 새로 쓰지 않는다 |
| `Suspend function 'suspend fun waitConnectTimeout(): Unit' should be called only from a coroutine or another suspend function.` | 50번 `startConnectTimeout()`에서 51번을 코루틴 밖에서 불렀다. `connectTimeoutJob = lifecycleScope.launch { waitConnectTimeout() }`처럼 `launch { }` 안에서 부른다(6주차) |
| `Argument type mismatch: actual type is 'kotlin.String', but 'kotlin.Int' was expected.` (`isAllowedIndex` 줄) | `isAllowedIndex(pin)`처럼 글자를 넘겼다. `pinEdit`의 글자는 `String`, `isAllowedIndex(index: Int)`는 숫자를 받는다. `isAllowedIndex(pin.toInt())` |
| `None of the following candidates is applicable:` 아래 `makeText` 후보 두 줄, 이어서 `Unresolved reference 'show'.` | 메시지가 원인을 직접 말하지 않는다. 50번의 `lifecycleScope.launch { }` 안에 `Toast.makeText(this, …)`를 바로 썼다. 그 안의 `this`는 Activity가 아니라 코루틴이다. Toast는 51번 `waitConnectTimeout()`(Activity의 함수) 안에 두고 `launch` 안에서는 그 함수를 부른다. `show` 줄은 앞 줄 때문에 따라 나온 것이다 |
| `Missing return statement.` | TODO 주석을 지우면서 `hasBlePermissions()`의 `return true` 줄까지 지웠다. 함수 끝에 `return true`를 되살린다. `isAllowedIndex()`의 `return false`를 지워도 같은 오류가 날 것이다 |
| 권한을 끈 상태에서 [권한 확인]을 누르는 순간 앱이 멈춘다. Logcat에 `java.lang.IllegalStateException: LifecycleOwner com.example.smartio.MainActivity@… is attempting to register while current state is RESUMED. LifecycleOwners must call register before they are STARTED.` 이미 허용된 기기에서는 `권한 OK`만 떠서 멀쩡해 보인다 | [권한 확인] 리스너 안에서 `registerForActivityResult(…)`로 요청 틀을 새로 만들었다. 요청 틀은 화면이 시작되기 전에 만들어야 하므로 클래스 안에 있는 `permissionLauncher`를 쓰고, 리스너에서는 `permissionLauncher.launch(PermissionHelper.required())`만 부른다 |
| Android 12 이상에서 요청 창에서 허용했는데 곧바로 `권한이 필요합니다` 창이 뜬다. 설정에서는 `근처 기기`가 허용으로 보이는데 [권한 확인]을 누를 때마다 창이 또 뜨고, [검색]도 요청 창 없이 곧바로 `권한이 필요합니다` 창을 띄우며 검색하지 않는다 | `AndroidManifest.xml`에서 `BLUETOOTH_CONNECT` 권한 줄이 빠졌다. 선언하지 않은 권한은 요청해도 곧바로 거절된다. starter Manifest는 고치지 않는다 |
| `3` → Switch 켜기에 명령 로그 `on 3` 아래 빨간 `응답: {"result":"fail","ms":"unknown command"}`와 `보드가 오류를 알렸습니다` / `응답: fail · unknown command` 창. Logcat에 `writeCharacteristic(가짜): "on3"` | `send("on$index")`처럼 명령 이름과 번호 사이 띄어쓰기가 빠졌다. 로그에 쌓는 글자는 맞아 보여도 보낸 글자가 다르다. `send("on $index")`. Logcat에서 실제로 보낸 글자를 확인한다 |
| 번호 칸을 비운 채 Switch를 누르는 순간 앱이 멈춘다. Logcat에 `java.lang.NumberFormatException: For input string: ""` | 허용 번호 검사(`pin.toInt()`)를 빈 칸 검사보다 앞에 두었다. 순서는 빈 칸 → 허용 번호 → 켜기/끄기 |
| 목록 줄을 누르고 10초를 기다려도 `연결 시간이 초과되었습니다`가 안 뜬다 | 오류가 아니다. Fake는 약 2초 만에 `준비됨`이 된다. 51번 `delay`를 잠시 1000으로 줄여 확인하고 되돌린다 |
| [권한 확인]을 눌러도 아무 일이 없다 | 12번 리스너 안이 아직 비어 있거나, `hasBlePermissions()`가 `true`인데 Toast 줄이 없다. 13번 → 12번 순서로 다시 본다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다(리허설에서만. 본시험에서는 구현 도움을 주지 않는다).

## 제출

- **1일차 리허설**: 제출하지 않는다. 점검표와 자기 채점 결과는 본인이 보관한다.
- **2일차 본시험**: `MainActivity.kt`, `ControlActivity.kt` 두 파일(문항지가 지정하면 캡처도)을 시험 공지의 LMS 제출 칸에 낸다. 채점은 [채점표](rubric.md)로 한다.

## 먼저 끝났다면

1일차 리허설을 일찍 끝냈다면 아래를 해 본다. 모두 2~14주 범위이며, 해 본 뒤에는 완성본 모양으로 되돌려 둔다.

1. [권한 확인]에서 권한이 모자라면 요청 창을 띄우기 전에 Toast `허용 안 된 권한 수: 2`를 먼저 띄운다. `PermissionHelper.missing(this)`가 허용 안 된 권한만 돌려주고, 그 개수는 `.size`(11주차)다. `$count` 바로 뒤에 한글을 붙이지 않는다.
2. 시간 초과 때 Toast 대신 제목 `연결 시간 초과`, [다시 시도]·[닫기]가 있는 AlertDialog를 띄운다. [다시 시도]는 12주차 35번처럼 `binding.scanButton.performClick()`을 부른다.
3. `isAllowedIndex()`의 `if` 두 개를 `listOf(-1, 0, 1, 2, 3).contains(index)` 하나로 줄이고, 4번 표의 결과가 그대로인지 확인한다.
4. 구술 연습: starter의 콜백 다섯 개(`permissionLauncher`의 `{ _ -> }`, `onFound = { device -> }`, `collect { state -> }`, `onMessage { json -> }`, `onStop()`)가 **언제 불리는지** 한 문장씩 적고 짝과 바꿔 읽는다.

추가 과제는 선택 사항이다.
