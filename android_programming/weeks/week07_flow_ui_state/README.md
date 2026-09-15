# 7주차 — ViewModel과 StateFlow: 회전해도 살아 있는 상태

## 이번 주 질문

> 카운트다운 중에 화면을 돌려도 `연결 중… 3`이 이어지고 버튼도 그 상태에 맞게 켜져 있으려면, 상태를 어디에 두고 화면은 그 상태를 어떻게 받아야 할까?

6주차 마지막에 카운트다운 중에 화면을 돌리면 숫자가 사라지고 `대기 중`으로 돌아가는 것을 보았다. 코루틴이 화면(`lifecycleScope`)과 함께 사라졌기 때문이다.
이번 주 1일차에는 화면보다 오래 사는 **ViewModel**에 코루틴과 마지막 문구를 옮겨, 회전한 뒤에도 글자가 이어지게 한다.
2일차에는 연결 상태를 **StateFlow**에 두고, 화면은 틀 안의 `collect { }`에서 상태를 받아 글자와 버튼을 함께 고친다.

## 학습 목표

1. `class`와 프로퍼티를 읽고, `class ConnViewModel : ViewModel()`에 6주차 카운트다운·가짜 연결 코드를 옮긴다.
2. `by viewModels()`로 받은 ViewModel이 회전해도 같은 객체라서 `viewModelScope.launch`로 시작한 카운트다운이 계속 돈다는 것을 화면과 Logcat으로 확인한다.
3. `object ConnState`의 상수와 `when (state)`로 상태마다 켤 버튼을 정한다.
4. ViewModel 안에서는 `MutableStateFlow`로 값을 바꾸고, 화면에는 읽기 전용 `StateFlow`만 보여 준다.
5. `repeatOnLifecycle(Lifecycle.State.STARTED)` 틀을 복사해 `collect { }` 안에서 글자와 버튼을 고치고, 회전해도 같은 화면이 유지되는 것을 확인한다.

## 이번 주 결과물

```text
(1) 연결 중… 3에서 회전한 가로 화면

Smart I/O Controller
[장치 이름        ]
자동 연결 (○)
[검색] [중지] [해제]     ← [중지]만 켜져 있다
   ◌                     ← ProgressBar
연결 중… 3
[연결]

(2) 준비됨 화면

[검색] [중지] [해제]     ← [해제]만 켜져 있다
준비됨
[연결]
```

폰 크기 가로 화면에서는 [연결]·[다시 시도] 아래쪽이 가려질 수 있지만, 채점하는 숫자·가로 줄 버튼·ProgressBar는 보인다.

캡처 2장을 제출한다. `연결 중… 3`(또는 2)에서 회전한 가로 화면과, `준비됨`에서 가로 줄 버튼 가운데 [해제]만 켜진 화면이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | `class`와 프로퍼티, 회전하면 사라지는 카운트다운, ViewModel, `by viewModels()`, `viewModelScope` | 카운트다운·`connectFake()`를 `ConnViewModel`로 옮기기 → 문구 알림 등록·해제 → 회전 뒤 `resultText` 다시 읽기 → 회전 관찰 | 회전해도 글자가 이어지는 연결 화면(버튼은 아직 처음 모양) |
| 2일차 | `object ConnState`와 `when`, `MutableStateFlow`/`StateFlow`, `repeatOnLifecycle` 틀과 `collect`, 상태별 버튼 | `ConnState.kt`·[해제] 버튼 → StateFlow로 바꾸기 → 틀 두 개 넣고 `collect` 안 채우기 → 회전 확인·캡처 | 회전해도 글자·버튼이 그대로인 연결 화면 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 6주차까지 만든 `SmartIO` 프로젝트([검색]·[중지]·[다시 시도]가 있고 `connectFake()`·`tryConnect()`가 동작하는 상태). 없으면 6주차 완성본(`examples/day2`)을 받아 시작한다.
- 3주차에 본 회전 순서(`onDestroy` 다음에 `onCreate`, Activity가 새로 만들어진다)와 `?.`
- 5주차에 배운 람다 `{ }`, `isEnabled`, `visibility`
- 6주차에 배운 `lifecycleScope.launch`, `delay`, `Job`, `try/catch`
- ViewModel·StateFlow에 필요한 의존성(`activity-ktx`, `lifecycle-viewmodel-ktx`, `lifecycle-runtime-ktx`, `kotlinx-coroutines-android`)은 4주차 `build.gradle.kts`에 이미 들어 있다.

## 이번 주 범위

| 문법·API | 이번 주에 알아둘 뜻 |
|---|---|
| `class Counter { var count = 0 }` | 설계도다. `Counter()`로 객체를 만들고, `a.count`처럼 점으로 객체 안의 값(**프로퍼티**)을 부른다 |
| `class ConnViewModel : ViewModel()` | `ViewModel`을 물려받은 클래스. 화면보다 오래 살아서 회전해도 없어지지 않는다 |
| `private val viewModel: ConnViewModel by viewModels()` | 이 화면의 ViewModel을 받아 온다. 회전한 새 화면에도 같은 객체를 돌려준다. `ConnViewModel()`로 직접 만들지 않는다 |
| `viewModelScope.launch { }` | ViewModel에 묶인 코루틴. 화면이 새로 만들어져도 계속 돌고, ViewModel이 정리될 때 함께 취소된다 |
| `var listener: ((String) -> Unit)? = null` / `listener?.invoke(text)` | (1일차 틀, 채점하지 않음) 글자 하나를 받는 코드를 넣어 두는 변수. 비어 있으면 `null`이라 `?.invoke`로 부른다 |
| `override fun onDestroy()` | 3주차 생명주기 콜백. 1일차에 등록을 풀 때(`listener = null`) 쓴다 |
| `if (scanJob?.isActive == true) { return }` | (틀) 코루틴이 이미 돌고 있으면 함수를 여기서 끝낸다 |
| `object ConnState { const val READY = "준비됨" }` | 이름으로 바로 부르는 하나뿐인 상수 묶음. `ConnState.READY`로 쓴다 |
| `when (state) { ConnState.READY -> { … } }` | 값이 맞는 줄 하나만 실행한다. `if … else if …`를 줄인 모양 |
| `private val _state = MutableStateFlow(ConnState.DISCONNECTED)` / `_state.value = …` | 지금 값 하나를 늘 들고 있는 상자. 값을 바꾸면 받는 쪽에 알린다. ViewModel 안에서만 바꾼다 |
| `val state: StateFlow<String> = _state` | 같은 상자를 화면에는 읽기 전용으로 보여 준다. `<String>`은 안의 값이 글자라는 표시 |
| `lifecycleScope.launch { repeatOnLifecycle(Lifecycle.State.STARTED) { viewModel.state.collect { state -> } } }` | (틀) 화면이 보일 때만 값을 받는다. 다시 받기 시작하면 마지막 값을 곧바로 받는다. 학생은 `collect { }` 안만 채운다 |

`SharedFlow`, Flow를 바꾸는 연산자, Fragment 안에서 받기는 다루지 않는다. 12주차에는 같은 `ConnState`와 틀로 진짜 BLE 연결 상태를 받는다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [ConnViewModel.kt](examples/day1/ConnViewModel.kt) · [MainActivity.kt](examples/day1/MainActivity.kt)
- 2일차 완성 코드: [ConnState.kt](examples/day2/ConnState.kt) · [ConnViewModel.kt](examples/day2/ConnViewModel.kt) · [MainActivity.kt](examples/day2/MainActivity.kt) · [activity_main.xml](examples/day2/activity_main.xml) · [strings.xml](examples/day2/strings.xml)

## 완료 기준

아래 항목은 모두 2일차 제출물(세 파일과 캡처 2장)로 확인한다.
1일차에 스스로 점검할 것(`연결 실패`에서 회전해도 [다시 시도]가 남는지, 회전해도 Logcat 줄이 이어지는지)은 [실습지 1일차 '오늘 확인할 것'](lab.md#6-오늘-확인할-것)에 있고, 채점하지 않는다.

- [ ] `class ConnViewModel : ViewModel()`이고, `MainActivity`는 `by viewModels()`로 받는다(`ConnViewModel()`로 직접 만들지 않는다).
- [ ] 카운트다운과 가짜 연결은 `viewModelScope.launch`에서 돌고, `ConnViewModel.kt`에 `binding`이 한 줄도 없다.
- [ ] `object ConnState`에 상수 다섯 개가 있고, `MainActivity`의 `when (state)`가 이 상수로 켤 버튼을 나눈다.
- [ ] `_state`/`state`, `_seconds`/`seconds`를 `MutableStateFlow`/`StateFlow`로 두고, 화면은 값을 직접 바꾸지 않고 ViewModel 함수만 부른다.
- [ ] 두 `collect`가 모두 `repeatOnLifecycle(Lifecycle.State.STARTED)` 틀 안에 있고, `collect` 안에 `startActivity`·Toast가 없다.
- [ ] 앱을 켜면 `연결 안 됨`([검색]만 켜짐), [검색]을 누르면 `연결 중… 5`→`1` → `서비스 확인 중` → `준비됨`([해제]만 켜짐) 또는 `끊김`([검색]과 [다시 시도])으로 바뀌고, [중지]나 [해제]를 누르면 `연결 안 됨`으로 돌아간다.
- [ ] 캡처 1: `연결 중… 3`(또는 2)에서 회전한 가로 화면에 **숫자**가 보이고, 가로 줄에서 [중지]만 켜져 있고, ProgressBar가 보인다.
- [ ] 캡처 2: `준비됨` 화면에서 가로 줄 [해제]만 켜져 있고, [다시 시도]·ProgressBar는 숨어 있다.
- [ ] `ConnState.kt`, `ConnViewModel.kt`, `MainActivity.kt`와 캡처 2장을 제출한다.
- [ ] 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는다.

## 다음 수업 연결

다음 주는 [8주차 — 중간고사(개인 실기)](../week08_midterm/README.md)다. 범위는 2~7주차이며,
1일차 리허설에서는 같은 화면에 [시작] → 5초 카운트다운 → 완료 문구, [취소]로 중단, 회전해도 상태 유지(ViewModel + StateFlow)를 혼자 만든다.
이번 주의 ViewModel, 틀 두 개, `when`을 예제를 보지 않고 한 번 더 써 보고 온다.

## 공식 참고 자료

- [ViewModel 개요 — Android Developers](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Android의 StateFlow 및 SharedFlow — Android Developers](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [수명 주기 인식 코루틴(repeatOnLifecycle) — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
- [클래스 — Kotlin 문서](https://kotlinlang.org/docs/classes.html)
- [object 선언 — Kotlin 문서](https://kotlinlang.org/docs/object-declarations.html)
- [조건과 when — Kotlin 문서](https://kotlinlang.org/docs/control-flow.html)
