# 6주차 — 코루틴: delay·취소·오류 처리

## 이번 주 질문

> 5초를 기다리는 동안 화면을 멈추지 않고 숫자를 하나씩 줄이려면, 그리고 도중에 멈추거나 실패했을 때 앱이 꺼지지 않게 하려면 어떻게 써야 할까?

5주차에는 `Thread`와 `Handler`로 5초 뒤에 "검색 완료"를 띄웠다. 이번 주에는 같은 일을 **코루틴**으로 다시 쓴다.
`lifecycleScope.launch { }` 안에서 `delay(1000)`을 부르면 화면은 그대로 움직이면서 1초씩 기다릴 수 있고,
`Job`을 보관해 두면 [중지]로 멈출 수 있다. 2일차에는 절반은 실패하는 가짜 연결을 만들어 `try/catch`로 받고 [다시 시도] 버튼을 띄운다.

## 학습 목표

1. `lifecycleScope.launch { }` 안에서 `delay(1000)`으로 1초씩 기다리며 화면 글자를 바꾼다.
2. `for (i in 5 downTo 1)`로 5부터 1까지 세는 카운트다운을 만든다.
3. `suspend fun`이 "멈췄다 이어지는 함수"라는 것을 `delay`와 `Thread.sleep`의 차이로 설명한다.
4. `scanJob = lifecycleScope.launch { }`로 받아 둔 `Job`을 `scanJob?.cancel()`해서 [중지] 버튼을 만든다.
5. 진짜 막히는 일(`Thread.sleep`)만 `withContext(Dispatchers.IO)`로 옮기고, 실패는 `try/catch`로 받아 [다시 시도] 버튼을 보여 준다.

## 이번 주 결과물

```text
Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지]
검색 중… 3
[연결]

--- 연결에 실패하면 ---
[검색] [중지]
연결 실패
[연결]
[다시 시도]        ← Toast "연결 실패"
```

캡처 2장을 제출한다. [중지]로 카운트다운이 멈춘 화면(예: `검색 중… 3`에서 정지)과, 가짜 연결이 실패해 Toast와 [다시 시도] 버튼이 보이는 화면이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `for … downTo`, `lifecycleScope.launch`와 `delay`, `sleep`과 비교, `suspend fun` | Handler 검색을 코루틴 카운트다운 5→1로 바꾸기 → `sleep`으로 바꿔 관찰 → `countDown()`으로 묶기 | 카운트다운이 보이는 검색 화면 |
| 2일차 | `try/catch`·`throw`, `Job.cancel()`, `withContext(Dispatchers.IO)`, `connectFake()`와 재시도 | [중지]로 취소 → 가짜 연결 → 성공이면 제어 화면 이동, 실패면 Toast + [다시 시도] | 중지·실패·재시도가 되는 연결 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 5주차까지 만든 `SmartIO` 프로젝트(연결 화면에 [검색]·[중지]·ProgressBar `scanProgress`·상태 글자 `stateText`가 있는 상태). 없으면 5주차 완성본(`examples/day2`)을 받아 시작한다.
- 5주차에 배운 `isEnabled`, `visibility = View.VISIBLE / View.GONE`, 람다 안에서 바깥 변수 쓰기
- 3주차에 배운 `?`, `?.` (2일차 `scanJob?.cancel()`에서 다시 쓴다)

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `for (i in 5 downTo 1) { }` | `i`가 5, 4, 3, 2, 1로 바뀌며 중괄호 안을 다섯 번 실행한다 |
| `lifecycleScope.launch { }` | 중괄호 안을 코루틴으로 시작한다. 이 화면이 사라지면 함께 사라진다 |
| `delay(1000)` | 1초 기다린다. 기다리는 동안 화면은 계속 움직인다. 코루틴 안에서만 쓸 수 있다 |
| `suspend fun` | `delay`처럼 멈췄다 이어지는 함수. 코루틴 안이나 다른 `suspend fun` 안에서만 부른다 |
| `private var scanJob: Job? = null` / `scanJob = lifecycleScope.launch { }` / `scanJob?.cancel()` | 시작한 코루틴을 클래스 변수 `scanJob`에 `Job`으로 받아 두고, 다른 버튼에서 `cancel()`로 멈춘다. 아직 없으면 `null`이라 3주차 `?.`로 부른다 |
| `try { … } catch (e: Exception) { … }` | `try` 안에서 오류가 나면 앱이 꺼지는 대신 `catch` 안이 실행된다 |
| `throw Exception("연결 실패")` | 오류를 일부러 낸다. `e.message`가 `"연결 실패"`가 된다 |
| `withContext(Dispatchers.IO) { }` | 진짜 막히는 일(`Thread.sleep`, 파일, 네트워크)을 다른 스레드에서 하고 결과만 받아 온다 |
| `fun f(): Boolean = …` | `: Boolean`은 참/거짓 하나를 돌려준다는 표시, `=`는 오른쪽 결과를 그대로 돌려주는 짧은 모양. `connectFake()` 한 곳에서만 쓴다 |

`viewModelScope`, `StateFlow`, 회전해도 카운트다운이 이어지게 하는 방법은 7주차에서 다룬다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [MainActivity.kt](examples/day1/MainActivity.kt) · [activity_main.xml](examples/day1/activity_main.xml)
- 2일차 완성 코드: [MainActivity.kt](examples/day2/MainActivity.kt) · [activity_main.xml](examples/day2/activity_main.xml) · [strings.xml](examples/day2/strings.xml)

## 완료 기준

- [ ] [검색]을 누르면 `검색 중… 5`부터 `검색 중… 1`까지 1초마다 바뀌고, 끝나면 `검색 완료`가 보인다.
- [ ] 카운트다운 중에도 EditText에 글자를 넣을 수 있다(화면이 멈추지 않는다).
- [ ] [중지]를 누르면 카운트다운이 그 숫자에서 멈추고 [검색]이 다시 눌린다.
- [ ] 카운트다운이 끝나면 `연결 중…`이 2초 보이고, 성공이면 `연결됨` 뒤 제어 화면으로 넘어간다.
- [ ] 실패하면 앱이 꺼지지 않고 `연결 실패` Toast와 [다시 시도] 버튼이 보이며, [다시 시도]가 동작한다.
- [ ] `MainActivity.kt`와 캡처 2장을 제출한다.
- [ ] 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

카운트다운 중에 화면을 돌리면 숫자가 사라지고 `대기 중`으로 돌아간다. `lifecycleScope`가 화면과 함께 사라지기 때문이다.
7주차에는 화면보다 오래 사는 `ViewModel`에 코루틴과 상태를 옮겨, 회전해도 `연결 중… 3`이 이어지게 만든다.

## 공식 참고 자료

- [Android의 Kotlin 코루틴 — Android Developers](https://developer.android.com/kotlin/coroutines)
- [수명 주기 인식 코루틴(lifecycleScope) — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [코루틴 기초 — Kotlin 문서](https://kotlinlang.org/docs/coroutines-basics.html)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [예외 — Kotlin 문서](https://kotlinlang.org/docs/exceptions.html)
