# 5주차 — 메인 스레드와 백그라운드: Thread·Handler

## 이번 주 질문

> 5초 걸리는 검색을 시작해도 화면이 멈추지 않고, 버튼을 다시 누를 수 있게 하려면 어떻게 해야 할까?

4주차에는 연결 화면과 제어 화면 두 개를 만들고 버튼·EditText·Switch를 다뤘다. 이번 주에는 연결 화면에
[검색] 버튼을 달고 5초 걸리는 검색을 흉내 낸다. 클릭 리스너에서 그냥 5초를 기다리면 화면 전체가 멈추는 것을 직접 보고,
`Thread`와 `Handler`로 화면을 멈추지 않게 고친다. 12주차에 실제 BLE 검색을 붙일 자리다.

## 학습 목표

1. 메인 스레드가 그리기와 클릭을 한 줄로 처리한다는 것을 그림으로 설명하고, 메인 스레드를 막으면 화면이 멈추고 ANR이 생기는 이유를 말한다.
2. `Thread { }.start()`로 5초 대기를 다른 스레드에 맡기고, `runOnUiThread { }` 안에서만 화면을 바꾼다.
3. `Handler(Looper.getMainLooper())`의 `postDelayed`로 5초 뒤 할 일을 예약하고 `removeCallbacks`로 취소한다.
4. `ProgressBar`의 `visibility`로 검색 중임을 보여 준다.
5. `isEnabled`로 검색 중에 버튼을 다시 못 누르게 막는다.

## 이번 주 결과물

```text
Smart I/O Controller
장치 이름 [ESP32_BLE      ]
자동 연결                 (  )
      [검색] [중지]
         ◌  ← 돌아가는 원
       검색 중…
        [연결]
```

[검색]을 누르면 위처럼 바뀌고, 5초 뒤 `검색 완료` Toast와 함께 원이 사라진다. [중지]를 누르면 바로 멈춘다.
마지막에는 두 파일과 캡처 2장을 제출한다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 람다 안에서 바깥 변수 쓰기, `Thread.sleep`으로 멈추는 화면, 메인 스레드·메시지 큐·ANR, `Thread`·`runOnUiThread` | [검색] 배치 → 멈춤 관찰 → Thread로 고치기 → 워커에서 View 만지면 생기는 오류 관찰 | 검색 중 화면 |
| 2일차 | 작년 BLE 특강의 `postDelayed`, `Handler`·`removeCallbacks`, `ProgressBar`·`visibility` | [중지]·ProgressBar 배치 → Handler로 예약 → [중지]로 취소 → 검색→완료·검색→중지 확인 → 제출 | 검색·중지가 되는 연결 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 실습실 PC의 Android Studio와 에뮬레이터 (버전은 수업 공지와 [설치 안내](../../ta_setup_guide.md)를 따른다)
- 4주차에 만든 `SmartIO` 프로젝트(연결 화면 `MainActivity`, 제어 화면 `ControlActivity`). 없으면 강의자에게 4주차 완성본(4주차 `examples/day2`)을 요청한다
- 3주차 Logcat 필터(`package:mine`)

## 이번 주 범위

| 문법·속성 | 이번 주에 알아둘 뜻 |
|---|---|
| 람다 안에서 바깥 변수 쓰기 | `{ }` 안에서 바깥의 `val name`·`binding`을 그대로 읽고 바꿀 수 있다. 나중에 실행돼도 기억한다 |
| 메인(UI) 스레드 | 화면 그리기와 버튼 클릭을 순서대로 처리하는 한 줄. 여기서 오래 기다리면 화면이 멈춘다 |
| ANR | 메인 스레드가 5초 넘게 터치에 답하지 못하면 시스템이 앱을 멈춰 세운다 |
| `Thread { … }.start()` | 중괄호 안의 일을 새 스레드에서 한다. `.start()`가 없으면 시작되지 않는다 |
| `runOnUiThread { … }` | 화면을 바꾸는 일을 메인 스레드에 넘긴다. 워커에서 View를 직접 바꾸면 앱이 꺼진다 |
| `Handler(Looper.getMainLooper())` | 메인 스레드의 메시지 큐에 일을 넣어 주는 손잡이 |
| `handler.postDelayed(finishScan, 5000)` | 5000ms 뒤에 `finishScan`을 메인 스레드에서 실행하라고 예약한다 |
| `handler.removeCallbacks(finishScan)` | 아직 실행되지 않은 예약을 취소한다. 같은 이름을 넘겨야 한다 |
| `val finishScan = Runnable { … }` | 나중에 실행할 코드 묶음에 이름을 붙인다 |
| `ProgressBar`, `visibility = View.VISIBLE / View.GONE` | 돌아가는 원을 보이거나 자리까지 숨긴다 |
| `button.isEnabled = false` | 버튼을 회색으로 만들어 누르지 못하게 한다 |

남은 초를 세어 보이는 카운트다운, 코루틴, 실제 BLE 검색은 이후 주차에서 다룬다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [MainActivity.kt](examples/day1/MainActivity.kt) · [activity_main.xml](examples/day1/activity_main.xml) · [strings.xml](examples/day1/strings.xml)
- 2일차 완성 코드: [MainActivity.kt](examples/day2/MainActivity.kt) · [activity_main.xml](examples/day2/activity_main.xml)

## 완료 기준

- [ ] [검색]을 누르면 `검색 중…`이 바로 보이고 버튼이 회색이 되며, 그동안 Switch와 [연결]이 눌린다.
- [ ] 5초 뒤 `검색 완료` Toast가 뜨고 버튼이 복구된다.
- [ ] 2일차에는 검색 중에 돌아가는 원이 보이고, [중지]를 누르면 5초가 지나도 `검색 완료`가 뜨지 않는다.
- [ ] `MainActivity.kt`에 `Thread.sleep`이 남아 있지 않다.
- [ ] `MainActivity.kt`, `activity_main.xml`, 캡처 2장(검색 중 화면 / `검색 완료` Toast 또는 [중지] 뒤 화면)을 제출한다.

## 다음 수업 연결

다음 주는 [6주차 — 코루틴: delay·취소·오류 처리](../week06_coroutines/README.md)다.
검색 중에 남은 초 `5, 4, 3, 2, 1`을 보이려면 `postDelayed`를 다섯 번 겹쳐야 한다. 6주차에는 코루틴의 `delay(1000)`와
`for (i in 5 downTo 1)`로 카운트다운을 만들고, 가짜 연결이 실패했을 때 `try/catch`로 [다시 시도] 버튼을 보인다.

## 공식 참고 자료

- [프로세스 및 스레드 개요 — Android Developers](https://developer.android.com/guide/components/processes-and-threads)
- [앱 응답성 유지(ANR) — Android Developers](https://developer.android.com/topic/performance/vitals/anr)
- [Handler — Android Developers](https://developer.android.com/reference/android/os/Handler)
- [Activity.runOnUiThread — Android Developers](https://developer.android.com/reference/android/app/Activity#runOnUiThread(java.lang.Runnable))
- [ProgressBar — Android Developers](https://developer.android.com/reference/android/widget/ProgressBar)
