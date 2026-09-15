# 8주차 — 중간고사(개인 실기)

## 이번 주 질문

> 2~7주에 만든 버튼·코루틴·ViewModel·StateFlow를 혼자서 60분 안에 다시 쓸 수 있을까? 그리고 그 코드가 내 에뮬레이터에서만이 아니라 **제출한 파일로도** 똑같이 돌아갈까?

7주차에는 SmartIO의 카운트다운과 연결 상태를 `ViewModel`과 `StateFlow`로 옮겨 화면을 돌려도 이어지게 했다.
이번 주에는 새 문법을 배우지 않는다. 1일차에 시험 범위와 채점표를 공개하고, 본시험과 같은 모양의 **공개 리허설** 앱 `Rehearsal`을 60분 동안 풀어 본다.
2일차에는 시험 절차·허용 자료·장애가 났을 때의 대체 절차를 확인하고, 각자 1일차 `Rehearsal` 프로젝트를 실행해 PC를 함께 점검한 뒤 **본시험**(비공개 문항)을 본다.

## 학습 목표

1. 채점표 다섯 항목(UI·이벤트 / 생명주기·복원 / 코루틴 / StateFlow collect / 실행·제출)이 코드의 어느 줄에서 드러나는지 말한다.
2. starter의 `// TODO` 다섯 곳을 읽고 ViewModel(`RehearsalViewModel.kt`)에 쓸 것과 화면(`MainActivity.kt`)에 쓸 것을 가른다.
3. `viewModelScope.launch` 안에서 `for (i in 5 downTo 1)`과 `delay(1000)`으로 카운트다운을 만들고, 보관한 `job`을 `job?.cancel()`로 멈춘다.
4. `_state`·`_seconds`에 넣은 값을 `repeatOnLifecycle` 틀 안의 `collect { }`에서 받아 글자와 `isEnabled`를 바꾸고, 회전해도 이어지는 것을 확인한다.
5. 저장 → 다시 실행 → 점검표 → 제출 순서로, 제출한 파일이 곧 채점 대상인 답안을 낸다.

## 이번 주 결과물

```text
Rehearsal
카운트다운 중
남은 초: 3
[시작] [취소]        ← [시작]은 회색, [취소]만 켜짐 (회전해도 그대로 이어진다)

--- [취소]를 누르면 ---
Rehearsal
취소됨
남은 초: 3           ← 멈춘 숫자 그대로
[시작] [취소]        ← [시작]만 켜짐
```

8주차는 주차별 실습 점수 대상이 아니다. 리허설 캡처 3장(회전 유지·취소·완료)은 자기 점검용이며 제출하지 않는다.
본시험(20점)의 제출물은 [시험 운영 안내](exam_structure.md#제출)를 따른다.

## 2일 수업 흐름

| 일차 | 설명·안내 30분 | 60분 | 결과 |
|---|---|---|---|
| 1일차 | 시험 범위(2~7주), 채점표 20점, 제출본 기준(저장 후 다시 실행), 60분 시간 예산, starter 둘러보기 | **공개 리허설**: starter의 TODO 다섯 곳 채우기 → 점검표 → `rehearsal_solution`과 비교해 자기 채점 | 회전해도 이어지고 취소되는 `Rehearsal` 앱 |
| 2일차 | 리허설에서 막힌 곳, 시험 순서, 허용 자료, 장애가 나면, PC 점검(내 `Rehearsal` 실행) | **본시험**: 비공개 문항, 리허설과 같은 모양 | 제출한 답안 파일 두 개와 캡처 |

각 수업은 `설명·안내 30분 + 60분`이다. 1일차 60분은 점수가 없는 연습이고, 2일차 60분이 시험이다.

## 준비

- 7주차까지 만든 `SmartIO` 프로젝트(ViewModel·StateFlow 버전). 시험 중에도 열어 볼 수 있다([허용 자료](exam_structure.md#허용-자료)).
- 실습실 PC의 Android Studio와 에뮬레이터. 1일차에 새 프로젝트 `Rehearsal`을 만든다.
- 다시 읽어 둘 것: 3주차 `?.`, 6주차 `for … downTo`·`delay`·`Job`·`try/catch`, 7주차 `by viewModels()`·`MutableStateFlow`·`repeatOnLifecycle` 틀.

## 이번 주 범위

이번 주에는 새 문법이 없다. 아래 표가 **시험 범위(2~7주)** 이고, 리허설과 본시험은 이 안에서만 낸다.

| 문법·API (처음 배운 주) | 이번 주에 알아둘 뜻 | 채점표 항목 |
|---|---|---|
| `setOnClickListener { }` (2주) | 버튼을 누를 때마다 중괄호 안을 실행한다. 리허설에서는 ViewModel 함수 하나만 부른다 | UI·이벤트 |
| `binding.startButton`, `strings.xml` (4주) | XML id로 View를 부른다. id 철자가 글자까지 같아야 한다 | UI·이벤트 |
| `isEnabled = false / true` (5주) | 버튼을 끄고 켠다. 리허설에서는 상태에 따라 `collect` 안에서 바꾼다 | UI·이벤트 |
| `if/else`, `"남은 초: $seconds"` (1·4주) | 상태에 따라 나누기, 글자에 값 넣기. `$변수` 바로 뒤에 한글을 붙이지 않는다 | UI·이벤트 |
| 생명주기, 회전하면 Activity가 다시 만들어진다 (3주) | 화면(Activity)에 둔 값은 회전하면 사라진다 | 생명주기·복원 |
| `class RehearsalViewModel : ViewModel()`, `by viewModels()` (7주) | 화면보다 오래 사는 객체. 회전해도 같은 객체를 돌려준다 | 생명주기·복원 |
| `viewModelScope.launch { }` (7주), `for (i in 5 downTo 1)`·`delay(1000)` (6주) | ViewModel 안에서 코루틴을 시작하고 1초씩 기다린다. 기다리는 동안 화면은 멈추지 않는다 | 코루틴 |
| `private var job: Job? = null`, `job?.cancel()` (6주, 3주 `?.`) | 시작한 코루틴을 보관했다가 멈춘다 | 코루틴 |
| `try { } catch (e: Exception) { }` (6주) | 실패해도 앱이 꺼지지 않게 받는다. 리허설에는 없고 본시험 코루틴 항목에 들어갈 수 있다 | 코루틴 |
| `MutableStateFlow("대기 중")`, `val state: StateFlow<String> = _state` (7주) | 바꾸는 쪽(`_state`)은 ViewModel 안에만, 화면에는 읽기 전용(`state`)만 보인다 | StateFlow collect |
| `lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { … collect { } } }` (7주) | **틀**. 화면이 보일 때만 값을 받는다. 우리 코드는 `collect { }` 안만 채운다 | StateFlow collect |

BroadcastReceiver·권한·목록·BLE(10주~)는 범위가 아니다. 7주차 `when (state)`을 `if/else` 대신 써도 된다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [리허설과 본시험 안내](lab.md)
- [예제 설명](examples/README.md)
- [시험 운영 안내](exam_structure.md) — 범위·순서·허용 자료·제출·장애 대체 절차
- [채점표](rubric.md) — 20점 항목과 기록 양식
- 리허설 시작 코드: [RehearsalViewModel.kt](examples/rehearsal_starter/RehearsalViewModel.kt) · [MainActivity.kt](examples/rehearsal_starter/MainActivity.kt) · [activity_main.xml](examples/rehearsal_starter/activity_main.xml) · [strings.xml](examples/rehearsal_starter/strings.xml)
- 리허설 완성 코드(먼저 혼자 풀고 비교): [RehearsalViewModel.kt](examples/rehearsal_solution/RehearsalViewModel.kt) · [MainActivity.kt](examples/rehearsal_solution/MainActivity.kt)

## 완료 기준

- [ ] `Rehearsal` 앱에서 [시작]을 누르면 `남은 초: 5`→`1`이 1초마다 바뀌고 `완료` / `남은 초: 0`으로 끝난다.
- [ ] 카운트다운 중에는 [취소]만, 그 밖에는 [시작]만 켜진다.
- [ ] [취소]를 누르면 `취소됨`이 되고, 몇 초 기다려도 숫자가 더 줄지 않는다.
- [ ] `남은 초: 3`에서 화면을 돌려도 같은 글자·버튼 상태로 이어진다.
- [ ] 저장 후 다시 실행해 점검표를 확인하고, 채점표로 자기 채점을 했다.
- [ ] 2일차 본시험 답안 파일과 캡처를 시간 안에 제출했다.

## 다음 수업 연결

9주차는 **앱 컴포넌트 비교와 1차 과제 발표**다. 지금까지 만든 화면은 모두 Activity였다.
9주차 1일차에는 Activity·Service·BroadcastReceiver·ContentProvider 네 컴포넌트를 비교하고, 2일차에는 1차 과제를 발표한다.
과제의 채점 축(정상 흐름, 실패와 재시도, 회전 유지, 코드 설명)은 이번 시험에서 연습한 것과 겹친다. → [9주차 README](../week09_services_project/README.md)

## 공식 참고 자료

- [ViewModel 개요 — Android Developers](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Android의 StateFlow와 SharedFlow — Android Developers](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [수명 주기 인식 코루틴 — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [취소와 시간 제한 — Kotlin 문서](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
