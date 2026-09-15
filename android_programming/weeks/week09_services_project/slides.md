---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 9주차
footer: 앱 컴포넌트 비교와 1차 과제 발표
---

# 앱 컴포넌트 비교와 1차 과제 발표

2~7주차에 만든 화면은 모두 **Activity**였습니다.
1일차에는 Activity 말고 앱을 이루는 컴포넌트를 더 보고,
2일차에는 7주차까지 만든 앱으로 **1차 과제**를 발표합니다.

```text
1일차: 컴포넌트 비교 · Service 시연 · Fragment 시연 · 과제 안내 → 리허설
2일차: 발표 (1인 3분 = 시연 2분 + 코드 설명 질문 1분)
```

---

# 1일차 — 앱 컴포넌트 비교와 과제 안내

`30분 설명·시연 → 60분 1차 과제 리허설`

1. Activity·Service·BroadcastReceiver·ContentProvider 한 표로 비교하기
2. `LogService`로 "Service도 메인 스레드에서 돈다" 확인하기
3. Fragment를 바꿔 끼우는 시연, Notification 한 장
4. 1차 과제 채점 안내와 발표 정원

---

## 1일차 · 0–8분 ① — 앱을 이루는 네 가지 컴포넌트

| 컴포넌트 | 무엇 | 언제 쓰나 | 화면 | 예 |
|---|---|---|---|---|
| Activity | 사용자가 보는 화면 하나 | 누르고 입력받을 때 | 있음 | SmartIO 연결 화면 |
| Service | 화면 없이 일을 맡는 것 | 화면을 떠나도 이어져야 할 때 | 없음 | 음악 재생 |
| BroadcastReceiver | 시스템이 보내는 소식을 받는 것 | 배터리·충전 상태가 바뀔 때 | 없음 | 배터리 잔량 표시 |
| ContentProvider | 다른 앱에 데이터를 내주는 창구 | 연락처·사진을 읽을 때 | 없음 | 연락처 앱 |

- 넷 다 Android가 직접 부를 수 있는 **앱의 입구**입니다.
- 그래서 `AndroidManifest.xml`에 적습니다(BroadcastReceiver는 코드로 등록하기도 합니다).

---

## 1일차 · 0–8분 ② — 이 과목에서 언제 만나나

| 컴포넌트 | 이 과목 | 우리 코드 |
|---|---|---|
| Activity | 2~7주 매주 | `MainActivity`, `ControlActivity` |
| Service | **오늘 시연** | `LogService` |
| BroadcastReceiver | 10주 | 배터리 변화 받기 |
| ContentProvider | 11주 비교·시연 | 연락처 이름 읽기 |

- 4주차에 Manifest에서 `<activity android:name=".ControlActivity" …>` 줄을 봤습니다.
- 오늘은 그 옆에 `<service android:name=".LogService" …>` 줄이 생깁니다.
- 1차 과제와 시험은 Activity로 만듭니다. 오늘 Service·Fragment는 **보기만** 합니다.

---

## 1일차 · 8–15분 ① — Service 세 종류

| 종류 | 누가 시작하나 | 언제 끝나나 | 사용자에게 보이나 |
|---|---|---|---|
| started | 화면이 `startService(intent)` | `stopService`를 부르거나 스스로 멈출 때 | 보장되지 않음 |
| bound | 화면이 `bindService`로 묶음 | 묶은 화면이 모두 풀릴 때 | 묶은 화면과 함께 |
| foreground | started + 알림 띄우기 | 멈출 때까지 | **알림이 꼭 보인다** |

- 오늘 시연은 **started** 하나입니다. bound·foreground는 이름만 알아 둡니다.
- 음악 앱이 재생 중에 알림을 띄워 두는 것이 foreground Service입니다.

---

## 1일차 · 8–15분 ② — LogService: 화면 없는 컴포넌트

```kotlin
class LogService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        return START_NOT_STICKY
    }
    override fun onDestroy() { … Log.d("Service", "onDestroy") }   // 줄여 적음
    override fun onBind(intent: Intent?): IBinder? { … return null }
}
```

- `onStartCommand`: `startService`를 부를 **때마다** 불립니다.
- `onDestroy`: 멈출 때 한 번. `onBind`: 오늘은 `null`을 돌려주는 **틀**입니다.

---

## 1일차 · 8–15분 ③ — 시작·중지와 Manifest 등록

```kotlin
binding.serviceStartButton.setOnClickListener {
    val intent = Intent(this, LogService::class.java)
    startService(intent)
}
```

```xml
<service
    android:name=".LogService"
    android:exported="false" />
```

- 4주차 `Intent(this, ControlActivity::class.java)` → `startActivity(intent)`와 같은 모양입니다.
- [서비스 중지]는 같은 두 줄에서 `startService` 자리에 `stopService(intent)`를 씁니다.
- `<service>` 줄이 없어도 **빌드는 됩니다**. 그래도 눌러도 Service가 시작되지 않습니다(예상).

---

## 1일차 · 8–15분 ④ — 시연: Service도 메인 스레드에서 돈다

Logcat 필터 `package:mine tag:Service`

| 누른 버튼 | 화면 | Logcat |
|---|---|---|
| [서비스 시작] | 그대로 | `onStartCommand thread=main` |
| [서비스 시작] 한 번 더 | 그대로 | `onStartCommand thread=main` 한 줄 더 |
| [서비스 중지] | 그대로 | `onDestroy` |

- `thread=main`: 5주차에 본 **메인 스레드**와 같은 스레드입니다.
- Service는 "뒤에서 도는 스레드"가 아닙니다. `onStartCommand`에서 `Thread.sleep`하면 화면이 멈춥니다.
- 오래 걸리는 일은 Service 안에서도 5·6주차처럼 스레드·코루틴으로 보냅니다.

---

## 1일차 · 15–20분 ① — Fragment: Activity 안의 화면 조각

```text
┌ MainActivity ────────────────────┐
│ [첫 번째 조각] [두 번째 조각]     │  ← 그대로 있다
│ ┌ FragmentContainerView ───────┐ │
│ │  여기는 FirstFragment         │ │  ← 이 자리만
│ │  (또는 SecondFragment)        │ │     바꿔 끼운다
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

- Fragment는 **자기 layout**(`fragment_first.xml`)을 가진 화면 조각입니다.
- Activity의 `setContentView` 대신 `onCreateView`가 조각의 화면을 돌려줍니다.
- Manifest에는 적지 않습니다. 4주차 2일차에 예고한 내용의 실물입니다.

---

## 1일차 · 15–20분 ② — 빈 자리와 바꾸기 세 줄

```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/fragmentContainer"
```

```kotlin
binding.secondButton.setOnClickListener {
    val transaction = supportFragmentManager.beginTransaction()
    transaction.replace(R.id.fragmentContainer, SecondFragment())
    transaction.commit()
}
```

- 바꾸기 시작 → 자리에 조각 넣기 → **확정(commit)**. `commit()`을 빼면 아무것도 바뀌지 않습니다.
- 시연: 누를 때마다 Logcat `tag:Fragment`에 `SecondFragment onCreateView`가 찍힙니다.

---

## 1일차 · 20–24분 — Notification: 화면 밖에서 알리기

```text
상태 표시줄을 내리면
┌──────────────────────────────────┐
│ Smart I/O Controller             │
│ 연결이 끊겼습니다                │
└──────────────────────────────────┘
```

- 알림(Notification) = 앱 화면을 보고 있지 않은 사용자에게 알리는 것입니다.
- foreground Service는 **알림을 꼭 띄워야** 합니다(Service 세 종류 표의 셋째 줄).
- Android 13부터는 알림을 띄우려면 사용자에게 **권한**을 받아야 합니다.
- 권한 요청은 10주차 2일차에 배웁니다. 오늘은 코드 없이 모양만 봅니다.

---

## 1일차 · 24–30분 ① — 1차 과제: 둘 중 하나

| | (a) SmartIO 시뮬레이터 | (b) 자유 앱 (5~7주 범위) |
|---|---|---|
| 흐름 | 장치 이름 → 검색 카운트다운 → 가짜 연결 성공/실패·재시도 → 제어 화면 명령 로그 | 내가 정한 화면 흐름 |
| 더할 것 | **본인 기능 1개** | 제공 `fakeRequest()`를 한 곳 이상 부르고 **[다시 시도]** 두기 |
| 시작점 | 7주차까지 만든 `SmartIO` | 새 프로젝트 |

(b)는 수업 공지로 허용한 분반만 고를 수 있습니다.

채점 축은 같습니다: **정상 흐름 / 실패·재시도 / 회전 유지 / 코드 설명(개인 구술)**

자세한 조건: [과제 안내](project_brief.md) · [채점표](rubric.md)

---

## 1일차 · 24–30분 ② — 채점과 발표 정원

| 발표 5점 | 레포트 5점 |
|---|---|
| 정상 흐름 1.5 · 실패·재시도 1 · 회전 유지 1 · 코드 설명 1.5 | 실행 방법·파일 1 · 캡처와 코드 위치 2 · 본인 기능 설명 1 · 오류 해결 기록 1 |

발표는 1인 **3분**입니다. 60분 안에 끝나는지 먼저 계산합니다.

```text
발표 시간 = ceil(N / E) × 3분 ≤ 60분     N = 발표 인원, E = 동시에 듣는 평가자 수
예) N = 38, E = 2 → 19 × 3 = 57분 → 2일차 60분에 끝난다
예) N = 26, E = 1 → 26 × 3 = 78분 → 앞 순서 13명은 오늘 실습 20–60분에 발표
```

---

## 1일차 · 24–30분 ③ — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--1차-과제-리허설-60분) · [따라하기](walkthrough.md#1일차)

1. 발표 순서표에서 내 차례를 확인하고, 내 앱에서 채점 축 네 개가 보이는지 점검합니다.
2. 실패 문구와 [다시 시도]가 함께 보이는 화면을 **지금** 캡처해 둡니다.
3. 짝과 서로 시간을 재며 **2분 시연**을 두 번씩 연습합니다.
4. 코드 설명 질문에 답할 파일과 줄을 찾아 두고, 레포트를 정리합니다.

**설명 합계: 8+7+5+4+6 = 30분**

(b)를 고른 사람은 따라하기의 `fakeRequest()` 단계를 봅니다. Service·Fragment 시연은 따라하기에서 다시 해 볼 수 있습니다(채점하지 않음).

---

# 2일차 — 1차 과제 발표

`30분 발표 안내·점검 → 60분 발표`

1. 오늘 진행 순서
2. 채점표 다시 보기
3. 코드 설명 질문 미리 보기
4. 발표 전 점검 → 발표 시작

---

## 2일차 · 0–5분 — 오늘 진행 순서

| 순서 | 할 일 | 시간 |
|---|---|---|
| 1 | 앞 사람이 발표할 때 내 앱을 첫 화면에 켜 둔다 | 기다리는 동안 |
| 2 | 시연: 정상 흐름 → 실패·재시도 → 회전 | 2분 |
| 3 | 평가자 질문 한 개에 코드 줄을 보여 주며 답한다 | 1분 |
| 4 | 다음 사람에게 넘긴다 | 3분 안에 포함 |

- 2분이 되면 시연을 멈추고 질문으로 넘어갑니다. 못 보인 장면은 레포트 캡처로 보되 그 항목은 최대 절반입니다(장애 기록, 실패가 안 나온 경우는 채점표 예외).
- 발표 장소(앞 화면 / 내 자리)와 순서는 분반 공지를 따릅니다. 순서 바꾸기는 강의자에게 먼저 말합니다.

---

## 2일차 · 5–12분 — 채점표 다시 보기: 발표 5 + 레포트 5

| 발표 항목 | 점수 | 만점이 되는 장면 |
|---|---|---|
| 정상 흐름 | 1.5 | 처음부터 끝까지 막힘 없이. (a)는 본인 기능까지 |
| 실패·재시도 | 1 | 실패 문구 → [다시 시도] → 성공 |
| 회전 유지 | 1 | 진행 중이나 실패 화면에서 돌려도 글자·버튼이 그대로 |
| 코드 설명 | 1.5 | 질문에 파일과 줄을 가리키며 한 문장으로 답한다 |

| 레포트 항목 | 점수 |
|---|---|
| 실행 방법과 파일 목록 | 1 |
| 채점 축 캡처와 코드 위치 | 2 |
| 본인 기능((b)는 `fakeRequest()`를 부르는 곳) 설명 | 1 |
| 오류 해결 기록 | 1 |

---

## 2일차 · 12–20분 — 코드 설명 질문은 이렇게 나온다

| 질문 예 | 가리킬 곳 |
|---|---|
| 화면을 돌려도 상태가 남는 이유는? | `by viewModels()` 줄과 `viewModelScope.launch` |
| 실패해도 앱이 꺼지지 않는 이유는? | `try { … } catch (e: Exception) { … }` |
| [다시 시도]는 어디서 보이게 하나요? | `collect { }` 안의 `when` 또는 `if` |
| [검색]을 두 번 눌러도 하나만 도는 이유는? | `if (scanJob?.isActive == true) {` |
| 본인 기능은 어느 줄인가요? | 내가 고친 파일과 줄 |

답하는 순서: **파일 열기 → 줄 가리키기 → 한 문장**

"원래 이렇게 돼요"는 점수가 되지 않습니다. 줄을 가리킵니다.

---

## 2일차 · 20–27분 — 발표 전 점검

- [ ] 마지막으로 고친 뒤 **저장 → Run ▶ 다시 실행**했다
- [ ] 에뮬레이터 빠른 설정에서 **자동 회전**이 켜져 있고, 회전 버튼으로 앱이 실제로 돈다
- [ ] 앱이 첫 화면(`연결 안 됨` 또는 `대기 중`)에 있다
- [ ] 실패가 몇 번 만에 나오는지 알고, 안 나올 때 보여 줄 **실패 캡처**가 있다
- [ ] 코드 설명에 쓸 파일을 편집기 탭에 열어 두었다
- [ ] 레포트를 제출했거나 제출 방법을 안다

지금 7분 동안 각자 한 바퀴 돌려 봅니다. 에뮬레이터가 켜지지 않는 PC는 손을 듭니다.

---

## 2일차 · 27–30분 — 발표 시작

[2일차 실습](lab.md#2일차--1차-과제-발표-60분) · [따라하기](walkthrough.md#2일차)

1. 첫 순서 세 사람은 앱을 켜 두고 차례를 기다립니다.
2. 발표를 마친 사람은 다른 사람 발표를 듣고, 레포트 제출을 확인합니다.
3. 장비가 멈추면 손을 듭니다. 조교가 시각을 적고 순서를 뒤로 미룹니다.

**설명 합계: 5+7+8+7+3 = 30분**

---

## 다음 주 미리 보기

오늘 표의 셋째 줄, **BroadcastReceiver**를 직접 만듭니다.

- 에뮬레이터의 배터리를 바꾸면 SmartIO 화면의 `배터리 80% · 충전 중`이 따라 바뀌게 합니다.
- 12주차 BLE를 쓰려면 사용자에게 **권한**을 받아야 합니다. 그 흐름을 10주차 2일차에 만듭니다.
