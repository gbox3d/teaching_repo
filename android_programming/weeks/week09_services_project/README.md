# 9주차 — 앱 컴포넌트 비교와 1차 과제 발표

## 이번 주 질문

> 지금까지 만든 화면은 모두 Activity였다. 화면이 없는 컴포넌트(Service)는 어디서 돌고, 7주차까지 만든 앱은 발표 3분 안에 무엇을 보여 줘야 할까?

8주차에는 2~7주차 범위로 중간고사를 보았다. 이번 주 1일차에는 Android 앱을 이루는 네 컴포넌트(Activity·Service·BroadcastReceiver·ContentProvider)를 한 표로 비교하고,
`LogService` 시연으로 **Service도 메인 스레드에서 돈다**는 것을 Logcat으로 확인한다. Fragment를 바꿔 끼우는 시연과 Notification 설명도 짧게 본다.
1일차 실습 60분은 **1차 과제 리허설**이고, 2일차에는 7주차까지 만든 앱으로 **1차 과제를 발표**한다.

## 학습 목표

1. Activity·Service·BroadcastReceiver·ContentProvider를 "무엇·언제·화면 유무·예"로 구분해 말한다.
2. started·bound·foreground Service의 차이를 한 문장씩 말하고, `startService`·`stopService`와 Manifest `<service>` 등록이 4주차 `startActivity`와 같은 모양임을 설명한다.
3. Logcat의 `onStartCommand thread=main`을 읽고 "Service는 따로 스레드를 만들지 않는다"를 설명한다.
4. Fragment가 Activity 안의 화면 조각이고, `FragmentContainerView` 자리에 `beginTransaction()` → `replace()` → `commit()`으로 바꿔 끼운다는 것을 시연에서 확인한다.
5. 1차 과제의 채점 축 네 개(정상 흐름 / 실패·재시도 / 회전 유지 / 코드 설명)를 내 앱의 장면과 코드 줄에 연결해 3분 안에 발표한다.

## 이번 주 결과물

```text
--- 1일차 시연 (Logcat package:mine tag:Service) ---
onStartCommand thread=main      ← [서비스 시작]
onStartCommand thread=main      ← [서비스 시작] 한 번 더
onDestroy                       ← [서비스 중지]

--- 2일차 발표 (내 앱, 3분) ---
(a) 장치 이름 → 연결 중… 3 → 끊김 + [다시 시도] → 준비됨 → 제어 화면 로그 + 본인 기능
(b) [요청] → 요청 실패 + [다시 시도] → 결과: 성공 → 돌려도 그대로
```

9주차는 주차별 실습 점수 대상이 아니다. 이번 주 결과물은 **1차 과제(10점 = 발표 5 + 레포트 5)** 이며, 조건은 [과제 안내](project_brief.md), 점수는 [채점표](rubric.md)에 있다. (b)는 수업 공지로 허용한 분반만 고를 수 있다.

## 2일 수업 흐름

| 일차 | 설명·시연 30분 | 60분 | 결과 |
|---|---|---|---|
| 1일차 | 4대 컴포넌트 비교표, Service 세 종류와 `LogService` 시연, Fragment 교체 시연, Notification 한 장, 1차 과제 채점·발표 정원 안내 | **1차 과제 리허설**: 채점 축 점검 → 짝과 2분 시연 연습 → 코드 설명 연습 → 레포트 정리 | 3분 안에 발표할 수 있는 과제 앱과 레포트 초안 |
| 2일차 | 진행 순서, 채점표 다시 보기, 코드 설명 질문 예, 발표 전 점검 | **발표**: 1인 3분(시연 2분 + 질문 1분) | 발표 완료, 레포트 제출 |

발표 인원이 많아 60분 안에 끝나지 않는 분반은 1일차 실습 시간의 뒤쪽 40분(20–60분)에 앞 순서 발표를 시작한다([발표 정원 계산](project_brief.md#발표-정원-계산)).

## 준비

- 7주차까지 만든 `SmartIO` 프로젝트(ViewModel·StateFlow 버전, [검색]·[중지]·[다시 시도]·[해제]가 동작하는 상태). 없으면 7주차 완성본(`examples/day2`)을 받아 시작한다.
- 1차 과제 (b)를 고른 사람은 5~7주 범위로 만든 자기 앱과 제공 파일 [FakeRequest.kt](examples/fake_request/FakeRequest.kt).
- 다시 읽어 둘 것: 4주차 `Intent(this, ControlActivity::class.java)`·Manifest, 5주차 메인 스레드, 6주차 `try/catch`, 7주차 `by viewModels()`·`repeatOnLifecycle` 틀.
- 에뮬레이터 빠른 설정의 **자동 회전**(회전 유지 시연에 필요).

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| Activity / Service / BroadcastReceiver / ContentProvider | 앱의 네 가지 컴포넌트. 화면 / 화면 없이 일 맡기 / 시스템 소식 받기 / 다른 앱에 데이터 내주기 |
| started / bound / foreground Service | `startService`로 시작해 멈출 때까지 / 화면이 묶어 쓰는 동안 / 알림을 띄우고 계속. 이름만 알아 둔다 |
| `class LogService : Service()` | `Service`를 물려받은 화면 없는 컴포넌트 |
| `override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int` | `startService`를 부를 때마다 불린다. `return START_NOT_STICKY`는 "시스템이 끝내도 다시 살리지 않는다" |
| `override fun onDestroy()` | Service가 멈출 때 불린다 |
| `override fun onBind(intent: Intent?): IBinder? { return null }` | **틀**. 묶어 쓰지 않는 Service는 `null`을 돌려준다. 빼면 빌드가 안 된다 |
| `startService(intent)` / `stopService(intent)` | `Intent(this, LogService::class.java)`로 Service를 시작하고 멈춘다. 4주차 `startActivity`와 같은 모양 |
| `<service android:name=".LogService" android:exported="false" />` | Manifest 등록. `exported="false"`는 이 앱 안에서만 쓴다는 뜻 |
| `Thread.currentThread().name` | 지금 코드가 도는 스레드 이름. 메인 스레드면 `main` |
| `class FirstFragment : Fragment()`, `onCreateView` | (시연) 자기 layout을 가진 화면 조각. `onCreateView`가 조각의 화면을 돌려준다 |
| `androidx.fragment.app.FragmentContainerView` | (시연) 조각을 끼울 빈 자리 |
| `supportFragmentManager.beginTransaction()` → `replace(자리, 조각)` → `commit()` | (시연) 빈 자리의 조각을 바꾸는 세 줄. `commit()`이 없으면 바뀌지 않는다 |
| Notification | (설명) 화면 밖 사용자에게 알리는 것. foreground Service는 꼭 띄운다. Android 13부터 권한이 필요하다 |
| `suspend fun fakeRequest(): String` | (1차 과제 (b)) 1초 뒤 절반은 `throw`, 나머지는 `"성공"`을 돌려주는 제공 함수 |

Service·Fragment·Notification은 1차 과제 채점 대상이 아니다. bound Service, foreground Service 코드, 알림 권한, Fragment 뒤로 가기 기록(`addToBackStack`)은 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [리허설과 발표 안내](lab.md)
- [예제 설명](examples/README.md)
- [1차 과제 안내](project_brief.md) — 주제 (a)/(b), 필수 조건, 발표 3분·레포트, 발표 정원
- [1차 과제 채점표](rubric.md) — 발표 5 + 레포트 5
- Service 시연 코드: [LogService.kt](examples/service_demo/LogService.kt) · [MainActivity.kt](examples/service_demo/MainActivity.kt) · [AndroidManifest.xml](examples/service_demo/AndroidManifest.xml) · [activity_main.xml](examples/service_demo/activity_main.xml)
- Fragment 시연 코드: [MainActivity.kt](examples/fragment_demo/MainActivity.kt) · [FirstFragment.kt](examples/fragment_demo/FirstFragment.kt) · [SecondFragment.kt](examples/fragment_demo/SecondFragment.kt) · [activity_main.xml](examples/fragment_demo/activity_main.xml)
- 1차 과제 (b) 제공 코드와 사용 예: [FakeRequest.kt](examples/fake_request/FakeRequest.kt) · [RequestViewModel.kt](examples/fake_request/RequestViewModel.kt) · [MainActivity.kt](examples/fake_request/MainActivity.kt)

## 완료 기준

- [ ] 네 컴포넌트 중 화면이 있는 것은 Activity 하나라는 것과, 각 컴포넌트의 예를 하나씩 말할 수 있다.
- [ ] `LogService` 시연의 `thread=main`을 보고 "Service도 메인 스레드에서 돈다"를 설명할 수 있다.
- [ ] 내 과제 앱에서 정상 흐름·실패와 [다시 시도]·회전 유지 세 장면을 2분 안에 보여 줄 수 있다.
- [ ] 리허설 4번 표에 코드 설명 질문마다 답할 파일과 줄을 적었다(레포트 3절 코드 위치와 같은 번호).
- [ ] 2일차에 순서대로 발표했고, 레포트를 [과제 안내](project_brief.md#레포트)대로 제출했다.
- [ ] 발표 화면·레포트 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [10주차 — BroadcastReceiver와 런타임 권한](../week10_receivers_permissions/README.md)이다.
오늘 비교표의 셋째 줄 **BroadcastReceiver**를 직접 만들어 에뮬레이터 배터리 잔량·충전 상태를 SmartIO 연결 화면에 보여 주고,
2일차에는 12주차 BLE에 필요한 **런타임 권한**을 요청하고 거절되면 AlertDialog로 설정 화면에 보내는 흐름을 만든다. 시작점은 7주차 완성본이다.

## 공식 참고 자료

- [앱 기본 사항(앱 구성요소) — Android Developers](https://developer.android.com/guide/components/fundamentals)
- [서비스 개요 — Android Developers](https://developer.android.com/develop/background-work/services)
- [포그라운드 서비스 — Android Developers](https://developer.android.com/develop/background-work/services/fgs)
- [프래그먼트 — Android Developers](https://developer.android.com/guide/fragments)
- [프래그먼트 트랜잭션 — Android Developers](https://developer.android.com/guide/fragments/transactions)
- [알림 개요 — Android Developers](https://developer.android.com/develop/ui/views/notifications)
