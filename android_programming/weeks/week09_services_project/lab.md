# 9주차 실습 — 1차 과제 리허설과 발표

9주차 실습은 새 기능을 배우는 시간이 아니다. 1일차 60분에는 7주차까지 만든 앱(또는 (b) 자유 앱)으로 1차 과제 발표를 연습하고 레포트를 정리한다.
2일차 60분에는 순서대로 발표한다. 과제 조건은 [과제 안내](project_brief.md), 점수는 [채점표](rubric.md)에 있고,
Service·Fragment 시연을 다시 해 보는 단계와 (b)의 `fakeRequest()` 붙이기는 [따라하기](walkthrough.md)에 있다.

9주차는 주차별 실습 점수 대상이 아니다. 이번 주에 내는 것은 1차 과제 레포트와 소스다.

## 1일차 — 1차 과제 리허설 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 발표 순서표에서 내 차례와 짝(서로 시간을 재 줄 사람)을 확인하고, 과제 앱을 실행한다 |
| 5–20분 | 채점 축 점검표를 채우고 빠진 장면을 고친다(1번). 실패 장면을 캡처해 둔다(2번). (b)는 6번으로 `fakeRequest()`를 붙인다 |
| 20–35분 | 짝과 서로 시간을 재며 2분 시연을 두 번씩 한다 |
| 35–50분 | 코드 설명 질문 다섯 개에 답할 파일과 줄을 찾아 적는다 |
| 50–57분 | 레포트 캡처와 표를 정리한다 |
| 57–60분 | 저장 → 다시 실행 → 앱을 첫 화면에 두고 마친다 |

발표 인원이 60분을 넘는 분반([발표 정원 계산](project_brief.md#발표-정원-계산))은 아래 시간표를 쓴다. 앞 순서 사람은 오늘 발표한다.

| 시간 | 할 일 |
|---|---|
| 0–20분 | 1번 점검표 → 2번 실패 캡처 → 4번 질문 표(파일과 줄) 순서로 먼저 한다. 3번 짝 시연은 시간이 남을 때만 한 번 |
| 20–60분 | 앞 순서 발표(1인 3분, 최대 13명). 오늘 발표하지 않는 사람은 발표를 들으면서 자기 자리에서 소리 없이 3~5번 표를 채워도 된다 |

- 1일차 발표자는 희망자와 준비된 사람부터 정한다. 코드 설명 질문은 4번 표와 같은 다섯 개에서 나온다.

### 1. 채점 축 점검표 채우기

내 앱에서 아래 장면이 실제로 보이는지 하나씩 눌러 보고 마지막 칸을 채운다.

| 축 | (a) SmartIO에서 보여 줄 장면 | (b) 자유 앱에서 보여 줄 장면 | 내 앱에서 된다 / 안 된다 |
|---|---|---|---|
| 정상 흐름 | 장치 이름 → [검색] → `연결 중… 5`→`1` → `서비스 확인 중` → `준비됨` → [연결] → 제어 화면 Switch로 `on 3` 로그, 그리고 본인 기능 | 앱의 주 흐름과 `fakeRequest()` 성공 결과(예: `결과: 성공`) |  |
| 실패·재시도 | `끊김`과 [다시 시도] → 다시 시도해 `준비됨` | 실패 문구와 [다시 시도] → 다시 시도해 성공 |  |
| 회전 유지 | `연결 중… 3`이나 `끊김`에서 돌려도 글자·숫자·버튼이 그대로 | 요청 중이나 실패 화면에서 돌려도 문구·[다시 시도]가 그대로 |  |
| 코드 설명 | 4번 표 | 4번 표 |  |

- 7주차 완성본 흐름이 그대로 동작하면 (a)의 앞 세 축은 이미 된다. 남은 것은 **본인 기능 1개**다. 예시는 [과제 안내](project_brief.md#a-smartio-시뮬레이터--본인-기능-1개)에 있다.
- 본인 기능을 넣은 뒤에는 세 축을 처음부터 다시 확인한다. 새로 넣은 코드가 [다시 시도]나 회전을 망가뜨리는 경우가 많다.
- (b)에서 회전하면 처음 문구로 돌아간다면, `fakeRequest()`를 어디서 부르는지 본다. [따라하기 16단계](walkthrough.md#16-requestviewmodel-만들기)의 ViewModel 모양으로 옮긴다.

### 2. 실패 장면을 확실히 보여 주는 법

가짜 연결(`connectFake()`)과 `fakeRequest()`는 절반 확률로 실패한다. 발표 중에 실패가 안 나오면 실패·재시도 축을 보여 줄 수 없다.

1. [검색](또는 [요청])을 열 번 눌러 보며 실패가 몇 번째에 나오는지 적어 둔다.
2. 실패 문구와 [다시 시도]가 함께 보이는 화면을 **지금** 캡처해 둔다. 레포트에도 넣는다.
3. 발표에서 세 번 눌러도 실패가 안 나오면 이 캡처를 보여 주고 넘어간다. 질문 시간에 한 번 더 눌러 나오면 만점, 그래도 안 나오면 캡처를 보여 주며 `catch` 줄을 가리키면 만점이다([채점표](rubric.md)).

- 이 경우 말고, 2분 안에 못 보인 장면을 캡처로 대신하면 그 항목은 **최대 절반**이다.

- `Random.nextBoolean()`을 `true`나 `false`로 고정하지 않는다. 고정하면 성공이나 실패 중 하나가 나오지 않는다.

### 3. 2분 시연 연습

아래 순서로 짝 앞에서 두 번 시연한다. 짝은 시간을 재고 빠진 장면을 표에 적는다. 역할을 바꿔 한 번 더 한다.

```text
0:00–0:15  앱 이름, 고른 주제 (a)/(b), 본인 기능 한 문장
0:15–1:00  정상 흐름
1:00–1:30  실패 → [다시 시도] → 성공
1:30–1:50  진행 중이나 실패 화면에서 회전
1:50–2:00  마무리 한 문장
```

| 회차 | 걸린 시간 | 빠진 장면 | 다음에 줄일 것 |
|---|---|---|---|
| 첫 번째 |  |  |  |
| 두 번째 |  |  |  |

- 2분을 넘으면 정상 흐름에서 장치 이름을 짧게 넣거나, 제어 화면 로그를 한 줄만 보인다.
- 회전은 에뮬레이터 옆 도구 막대의 회전 버튼으로 한다. 앱이 돌지 않으면 빠른 설정의 **자동 회전**을 켠다.

### 4. 코드 설명 연습

평가자는 질문 한 개를 고른다. 아래 다섯 질문에 대해 **열 파일과 줄 번호**를 적고, 짝에게 한 문장으로 답해 본다.

| 질문 | 힌트: 먼저 열어 볼 파일 | 내 파일과 줄 |
|---|---|---|
| 화면을 돌려도 상태가 남는 이유는? | `MainActivity.kt`의 `by viewModels()` 줄, ViewModel의 `viewModelScope.launch` |  |
| 실패해도 앱이 꺼지지 않는 이유는? | ViewModel의 `try { … } catch (e: Exception) { … }` |  |
| [다시 시도]는 어느 줄이 보이게 하나? | `MainActivity.kt`의 `collect { }` 안 |  |
| [검색](또는 [요청])을 두 번 눌러도 하나만 도는 이유는? | ViewModel 함수 첫머리의 `isActive == true` 검사 |  |
| 본인 기능((b)는 `fakeRequest()`를 부르는 곳)은 어디인가? | 내가 고친 파일 |  |

- 답하는 순서는 **파일 열기 → 줄 가리키기 → 한 문장**이다. "원래 이렇게 돼요"는 점수가 되지 않는다.
- 줄 번호는 편집기 왼쪽에 보인다. 레포트 3절 표의 "코드 위치" 칸에 같은 번호를 쓴다.

### 5. 레포트 정리

[과제 안내의 레포트](project_brief.md#레포트) 다섯 절 중 오늘은 3절(채점 축 캡처와 코드 위치)과 5절(오류 해결 기록)을 먼저 채운다.

- 회전 캡처는 같은 상태의 세로 화면과 가로 화면 두 장이다.
- 오류 해결 기록은 5~7주에 겪은 오류도 된다. 오류 메시지 원문을 그대로 옮겨 적는다.
- 캡처에 계정·알림 내용이 보이지 않는지 확인한다.

### 6. (b)를 골랐다면: fakeRequest() 붙이기

1. [FakeRequest.kt](examples/fake_request/FakeRequest.kt)를 내 프로젝트의 package 폴더에 복사하고, 첫 줄 `package`만 내 것으로 바꾼다.
2. ViewModel 안의 `viewModelScope.launch { }`에서 `try` 안에 `fakeRequest()`를 부른다.
3. `catch` 안에서 실패 문구를 넣고 [다시 시도]가 보이게 한다. 화면은 `collect { }` 안에서 고친다.
4. 막히면 [따라하기 13~18단계](walkthrough.md#13-b-새-프로젝트-project1-만들기)를 새 프로젝트로 한 번 따라 한 뒤 내 앱과 비교한다.

## 2일차 — 1차 과제 발표 (60분)

| 시간 | 할 일 |
|---|---|
| 0–60분 | 순서표 차례대로 발표한다. 1인 3분 = 시연 2분 + 코드 설명 질문 1분(자리 교체 포함) |

### 발표 순서와 규칙

1. 앞 사람이 발표하는 동안 내 앱을 실행해 첫 화면에 두고, 코드 설명에 쓸 파일을 편집기 탭에 열어 둔다.
2. 차례가 되면 3번 연습 순서대로 2분 시연한다. 2분이 되면 평가자가 멈춘다.
3. 평가자가 고른 질문 한 개에 파일을 열고 줄을 가리키며 답한다.
4. 앱을 닫고 다음 사람에게 넘긴다.

- 에뮬레이터·PC가 멈추면 손을 든다. 조교가 시각을 적고 순서를 뒤로 미룬다([장애가 나면](project_brief.md#장애가-나면)).
- 내 코드 때문에 앱이 꺼지는 것은 장애가 아니다. 남은 시간 동안 보일 수 있는 장면을 보이고, 레포트 캡처로 설명한다.

### 발표를 마친 뒤

- 다른 사람 발표를 조용히 듣는다. 코드를 고치거나 다시 실행하지 않는다.
- 레포트 PDF와 소스 압축 파일이 제출 칸에 올라갔는지 확인한다.

## 막혔을 때

6·7주차 코드에서 나는 오류는 [6주차 막혔을 때](../week06_coroutines/lab.md#막혔을-때)와 [7주차 막혔을 때](../week07_flow_ui_state/lab.md#막혔을-때)를 본다.
아래 표의 "빌드는 되는데 …" 줄은 실행해서 드러나는 **예상 증상**이다. 문구는 기기와 버전에 따라 조금 다를 수 있다.

| 상황 | 확인할 것 |
|---|---|
| `Suspend function 'suspend fun fakeRequest(): String' should be called only from a coroutine or another suspend function.` | `fakeRequest()`는 suspend 함수다. ViewModel이면 `viewModelScope.launch { }` 안, Activity면 `lifecycleScope.launch { }` 안에서 부른다. 회전 유지까지 얻으려면 ViewModel 쪽이다 |
| `Suspend function 'suspend fun collect(collector: FlowCollector<String>): Nothing' should be called only from a coroutine or another suspend function.` | `collect`도 suspend 함수다. 7주차 틀 `lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { … } }` 안에 넣고 `collect { }` 안만 채운다 |
| 빌드는 되는데 [요청]을 몇 번 누르면 앱이 꺼진다. Logcat에 `FATAL EXCEPTION: main`과 `java.lang.Exception: 요청 실패` 비슷한 줄(예상) | `fakeRequest()`를 `try { … } catch (e: Exception) { … }` 없이 불렀다. 감싸고, `catch` 안에서 실패 문구와 `_failed.value = true`를 넣어 [다시 시도]를 보인다 |
| 빌드는 되는데 요청 중이나 결과가 나온 뒤 회전하면 `대기 중`으로 돌아가고 [다시 시도]가 사라진다(예상) | Activity의 `lifecycleScope.launch { }` 안에서 불렀다. `RequestViewModel`의 `viewModelScope.launch { }`로 옮기고, 화면은 `StateFlow`를 `collect`해서 고친다(7주차) |
| `요청 중…`일 때 [요청]을 다시 눌러도 아무 일이 없다 | 버그가 아니다. `request()` 첫머리의 `requestJob?.isActive == true` 검사가 중복 시작을 막는다(7주차 `startScan()`과 같다) |
| `Null cannot be a value of a non-null type 'android.os.IBinder'.` | (따라하기 A) `onBind`의 반환형을 `IBinder?`로, 인자를 `intent: Intent?`로 바꾼다. `?`가 없는 타입에는 `null`을 넣을 수 없다(3주차). New › Service › Service로 만들면 이 모양이 생긴다 |
| `Class 'LogService' is not abstract and does not implement abstract base class member 'onBind'.` | (따라하기 A) `Service`를 물려받으면 `onBind`가 꼭 있어야 한다. `override fun onBind(intent: Intent?): IBinder? { return null }`을 넣는다 |
| `None of the following candidates is applicable:` 과 `Classifier 'class LogService : Service' does not have a companion object, so it cannot be used as an expression.` | (따라하기 A) `Intent(this, LogService)`로 썼다. 4주차처럼 `Intent(this, LogService::class.java)`로 쓴다 |
| 빌드는 되는데 [서비스 시작]을 눌러도 Logcat `tag:Service`에 아무것도 찍히지 않는다(예상) | (따라하기 A) `AndroidManifest.xml`의 `<application>` 안에 `<service android:name=".LogService" android:exported="false" />`가 있는지 본다. 로그가 안 찍히면 먼저 Manifest를 본다 |
| `onStartCommand`에 `Thread.sleep`을 넣었더니 [서비스 시작] 뒤 화면이 멈춘다(예상) | (따라하기 A) Service도 메인 스레드에서 돈다. 오래 걸리는 일은 5주차 `Thread { }.start()`나 6주차 코루틴으로 보낸다. 관찰했으면 지운다 |
| Service를 시작한 채 뒤로 가기로 앱을 닫았더니 잠시 뒤 Logcat에 `onDestroy`가 찍힌다(예상) | (따라하기 A) 버그가 아니다. Android 8 이상은 백그라운드로 간 앱의 Service를 멈춘다. 시연은 앱을 연 채로 한다 |
| `Unresolved reference 'Fragment'.` 과 `'onCreateView' overrides nothing.` | (따라하기 B) `Fragment`에 커서를 두고 Alt+Enter(맥 ⌥+Enter) → `androidx.fragment.app.Fragment`. 고치면 `MainActivity.kt`의 `Argument type mismatch: actual type is 'com.example.fragmentdemo.FirstFragment', but 'androidx.fragment.app.Fragment' was expected.`도 함께 사라진다. `android.app.Fragment`는 고르지 않는다 |
| `Unresolved reference 'fragmentContainer'.` | (따라하기 B) 오류는 Kotlin 파일에 나오지만 원인은 XML이다. `activity_main.xml`의 `android:id="@+id/fragmentContainer"` 철자가 코드의 `R.id.fragmentContainer`와 같은지 본다 |
| 빌드는 되는데 [두 번째 조각]을 눌러도 화면이 `여기는 FirstFragment` 그대로다(예상) | (따라하기 B) 그 리스너에 `transaction.commit()` 줄이 있는지 본다. 세 버튼 코드의 줄 수를 나란히 비교하면 빠진 줄이 보인다 |
| 조각을 바꾼 뒤 뒤로 가기를 누르면 앞 조각으로 가지 않고 앱이 닫힌다(예상) | (따라하기 B) 버그가 아니다. 조각의 뒤로 가기 기록은 따로 넣어야 생기며 이번 시연 범위 밖이다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 레포트와 소스

1. **레포트 PDF**: [과제 안내의 레포트](project_brief.md#레포트) 다섯 절(앱 소개와 실행 방법, 파일 목록, 채점 축 캡처와 코드 위치, 본인 기능 설명, 오류 해결 기록)
2. **소스 압축 파일**: 프로젝트의 `app/src/main` 폴더
3. **발표**: 2일차(또는 순서표에 따라 1일차 실습 시간의 뒤쪽 40분, 20–60분)에 3분

파일 이름·제출 위치·마감은 [과제 안내](project_brief.md#레포트)와 수업 공지를 따른다. 주차별 실습 점수용 캡처는 없다.

## 먼저 끝났다면

- [따라하기 A](walkthrough.md#1-smartio-열고-실행하기-a)로 `LogService`를 SmartIO에 넣고 Logcat에서 `thread=main`을 직접 확인한다. 발표 전이면 과제 앱이 아닌 SmartIO 사본에서 한다.
- [따라하기 B](walkthrough.md#8-fragmentdemo-새-프로젝트-만들기-b)로 새 프로젝트 `FragmentDemo`를 만들고 조각을 바꿔 끼운다. 회전해도 보던 조각이 남는지 본다.
- 짝의 앱으로 4번 표의 질문을 서로 한 개씩 내 본다.
- (a) 본인 기능을 하나 더 넣어 본다. 발표에서는 하나만 소개한다.

추가 과제는 선택 사항이며 채점하지 않는다.
