---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 7주차
footer: ViewModel과 StateFlow · 회전해도 살아 있는 상태
---

# ViewModel과 StateFlow: 회전해도 살아 있는 상태

6주차 카운트다운은 화면을 **돌리면** 사라졌습니다.
이번 주에는 상태를 화면보다 오래 사는 곳에 두고, 화면은 그 상태를 **받아서** 보여 줍니다.

```text
연결 중… 3    ──회전──▶    연결 중… 3 → 2 → 1
[검색] [중지] [해제]        [검색] [중지] [해제]
```

---

# 1일차 — 코루틴과 상태를 ViewModel로

`30분 설명·시연 → 60분 실습`

1. `class`와 프로퍼티 읽기
2. 회전하면 무엇이 사라지는지 보기
3. `ConnViewModel`에 코루틴을 옮기고 `by viewModels()`로 받기

---

## 1일차 · 0–5분 — 오늘 문법: class와 프로퍼티

```kotlin
class Counter {
    var count = 0                      // 프로퍼티: 객체가 들고 있는 값
    fun plus() { count = count + 1 }   // 함수: 객체가 하는 일
}

fun main() {
    val a = Counter()                  // 설계도(class)로 객체 하나를 만든다
    a.plus()
    println(a.count)                   // 1
}
```

- `class`는 설계도, `Counter()`는 그 설계도로 만든 **객체**입니다.
- 점(`.`)으로 객체 안의 값과 함수를 부릅니다. `binding.stateText.text`도 같은 모양입니다.
- 오늘 만드는 `ConnViewModel`도 클래스 하나입니다.

---

## 1일차 · 5–15분 ① — 돌리면 사라지는 카운트다운

시연: 6주차 완성본에서 [검색] → `검색 중… 3`에서 회전

```text
회전 전                  회전 후
검색 중… 3               대기 중
[검색] [중지]            [검색] [중지]
                         (숫자가 사라지고, 연결도 시도하지 않는다)
```

- 3주차: 회전하면 `onDestroy` → `onCreate`. **Activity가 새로 만들어집니다.**
- 6주차 `lifecycleScope`의 코루틴은 옛 화면과 함께 취소됩니다.
- `onSaveInstanceState`는 숫자 하나는 남기지만, **돌고 있던 코루틴**은 이어 가지 못합니다.

---

## 1일차 · 5–15분 ② — 화면보다 오래 사는 ViewModel

```text
화면 A(세로) ── onDestroy ─┐   화면 B(가로) ── onCreate ── …
                           │
ConnViewModel ═════════════╪═══════════════════════ (계속 산다)
  scanJob: 검색 중… 3 → 2 → 1 → 연결 중… → 연결됨
```

- **ViewModel**은 회전해도 없어지지 않고, 새 화면에 **같은 객체**를 돌려줍니다.
- 뒤로가기(◁)로 앱을 닫을 때에만 함께 정리됩니다.
- 그래서 카운트다운 코루틴과 마지막 문구를 **ViewModel로 옮깁니다.**
- ViewModel은 화면(`binding`)을 모릅니다. 문구만 들고 있고, 화면에 넣는 일은 Activity가 합니다.

---

## 1일차 · 15–25분 ① — ConnViewModel과 viewModelScope

```kotlin
class ConnViewModel : ViewModel() {
    private var scanJob: Job? = null        // 6주차 MainActivity에서 옮겨 온 변수

    fun startScan() {
        scanJob = viewModelScope.launch {   // lifecycleScope 대신 viewModelScope
            for (i in 5 downTo 1) {
                show("검색 중… $i")          // binding 줄 대신 show(…)
                delay(1000)
            }
            tryConnect()
        }
    }
}
```

- `viewModelScope`는 **ViewModel에 묶인** 코루틴입니다. 화면이 새로 만들어져도 계속 돕니다.

---

## 1일차 · 15–25분 ② — by viewModels()로 받아 부르기

```kotlin
// MainActivity 클래스 안, binding 아래
private val viewModel: ConnViewModel by viewModels()
```

```kotlin
binding.scanButton.setOnClickListener {
    // 버튼·ProgressBar 네 줄은 6주차 그대로
    viewModel.startScan()
}
```

- `ConnViewModel()`로 **직접 만들지 않습니다.** 직접 만들면 회전할 때마다 새 객체가 생깁니다.
- `by viewModels()`는 이 화면의 ViewModel이 이미 있으면 **그것을** 돌려줍니다.
- `viewModelScope`는 `: ViewModel()`을 물려받은 클래스 안에서만 쓸 수 있습니다.
- `viewModels`가 빨간색이면 Alt+Enter(맥 ⌥+Enter) → `androidx.activity.viewModels`

---

## 1일차 · 15–25분 ③ — 문구를 화면에 알리고, 회전 뒤 다시 읽기

```kotlin
// ConnViewModel: 마지막 문구를 보관하고, 등록된 화면이 있으면 알린다
private fun show(text: String) {
    resultText = text
    listener?.invoke(text)
}
```

```kotlin
// MainActivity onCreate: 등록하고, 남은 문구를 다시 읽는다
viewModel.listener = { text -> showState(text) }
binding.stateText.text = viewModel.resultText
// onDestroy: viewModel.listener = null
```

- `showState(text)`는 6주차 `tryConnect()`에 있던 글자·버튼·Intent·Toast 줄을 옮겨 둔 `MainActivity` 함수입니다.
- `listener`는 "글자 하나를 받는 코드"를 넣어 두는 변수(틀), 비어 있으면 `null`입니다. 회전하면 옛 화면 `onDestroy`에서 비우고 → 새 화면 `onCreate`에서 다시 등록합니다.

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--viewmodel로-옮기기-60분) · [따라하기](walkthrough.md#1일차)

1. 6주차 프로젝트에서 회전해 문제를 확인합니다.
2. `ConnViewModel.kt`를 만들고 카운트다운·`connectFake()`·`tryConnect()`를 옮깁니다.
3. `by viewModels()`로 받아 부르고, 등록·해제·다시 읽기를 넣습니다.
4. 회전해서 **남는 것**과 **남지 않는 것**을 관찰표에 적습니다.

**설명 합계: 5+10+10+5 = 30분**

오늘은 글자만 이어지고 버튼·ProgressBar는 처음 모양으로 돌아갑니다. 내일 고칩니다.

---

# 2일차 — 상태를 StateFlow로 받기

`30분 설명·시연 → 60분 실습`

1. `object ConnState` 상수 묶음과 `when`
2. `MutableStateFlow`·`StateFlow`로 상태 보관하기
3. 틀 안의 `collect`로 받아 글자와 버튼을 함께 고치기

---

## 2일차 · 0–5분 — 오늘 문법: object 상수 묶음과 when

```kotlin
object ConnState {
    const val CONNECTING = "연결 중"
    const val READY = "준비됨"
    // DISCONNECTED·DISCOVERING·LOST까지 모두 다섯 개
}
```

```kotlin
when (state) {
    ConnState.CONNECTING -> { binding.stopButton.isEnabled = true }
    ConnState.READY -> { binding.disconnectButton.isEnabled = true }
}
```

- `object`는 이름으로 바로 부르는 하나뿐인 묶음, `const val`은 바뀌지 않는 상수입니다. 이름을 틀리면 **빌드 오류**로 드러납니다.
- `when (state)`는 값이 맞는 줄 하나만 실행합니다. `if … else if …`를 줄인 모양입니다.

---

## 2일차 · 5–13분 — MutableStateFlow와 StateFlow

```kotlin
// ConnViewModel 안
private val _state = MutableStateFlow(ConnState.DISCONNECTED)   // 바꾸는 쪽: 안에만
val state: StateFlow<String> = _state                           // 읽는 쪽: 화면에 공개

fun disconnect() {
    _state.value = ConnState.DISCONNECTED    // 값 바꾸기는 ViewModel 함수 안에서
}
```

- `StateFlow`는 **지금 값 하나**를 늘 들고 있는 상자입니다. 값이 바뀌면 받는 쪽에 알려 줍니다.
- `<String>`은 상자 안의 값이 글자라는 표시입니다.
- 1일차의 `resultText`(보관)와 `listener`(알리기)를 이 상자가 함께 맡습니다.
- 화면에서 `viewModel.state.value = …`로 바꾸려 하면 `'val' cannot be reassigned.`

---

## 2일차 · 13–23분 ① — 틀: 화면이 보일 때만 받는다

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            binding.stateText.text = state   // ← 학생은 이 중괄호 안만 채운다
        }
    }
}
```

| 줄 | 뜻 |
|---|---|
| `lifecycleScope.launch` | 6주차의 코루틴 시작. `collect`도 멈췄다 이어지는 함수라 필요 |
| `repeatOnLifecycle(STARTED)` | 화면이 보이면 안을 시작, 안 보이면 멈춤, 다시 보이면 또 시작 |
| `collect { state -> }` | 상태가 바뀔 때마다 중괄호 안을 실행 |

---

## 2일차 · 13–23분 ② — 받기 시작하면 마지막 값부터

```text
[검색]      ─▶ _state = 연결 중,  _seconds = 5, 4, 3 …
회전        ─▶ 옛 화면 onStop: 받기 멈춤 → onDestroy
               새 화면 보임: 다시 받기 시작 → 곧바로 "연결 중" + 3
홈 → 복귀   ─▶ 같은 방식으로 마지막 값을 다시 받는다
```

- 1일차에 **손으로** 한 등록(onCreate)·해제(onDestroy)·다시 읽기를 틀이 대신합니다.
- 받을 값이 두 개(`state`, `seconds`)면 틀을 **두 번** 씁니다. `seconds` 틀은 `state` 틀 **아래**에 둡니다.
- 틀 없이 `onCreate`에서 바로 `collect`하면 빌드 오류입니다. 틀 안에 넣습니다:
  `Suspend function 'suspend fun collect(collector: FlowCollector<Int>): Nothing' should be called only from a coroutine or another suspend function.`
  (`seconds`를 받으면 `<Int>`, `state`를 받으면 `<String>`으로 나옵니다)

---

## 2일차 · 23–27분 — 상태별 버튼: 먼저 끄고, 켤 것만 켠다

```kotlin
binding.scanButton.isEnabled = false
binding.stopButton.isEnabled = false
binding.disconnectButton.isEnabled = false
binding.retryButton.visibility = View.GONE
binding.scanProgress.visibility = View.GONE
when (state) {
    ConnState.READY -> {
        binding.disconnectButton.isEnabled = true
    }
    // DISCONNECTED·CONNECTING·DISCOVERING·LOST도 같은 모양
}
```

- 먼저 모두 끄면 이전 상태에서 켠 버튼이 **남지 않습니다.**
- [연결]은 4주차 그대로 항상 켜 둡니다. `collect` 안에는 `startActivity`·Toast를 넣지 않습니다(다시 받을 때마다 또 실행).

---

## 2일차 · 27–30분 ① — 1차 과제 미리 알림

- **9주차 2일차 발표**: 발표 5 + 레포트 5
- 주제: SmartIO 시뮬레이터
  장치 이름 → 검색 카운트다운 → 가짜 연결 성공/실패·재시도 → 제어 화면 명령 로그 + **본인 기능 1개**
- 채점 축: 정상 흐름 / 실패·재시도 / **회전 유지** / 코드 설명(개인 구술)
- 이번 주 화면이 과제의 뼈대입니다. 자세한 안내문과 제출 방법은 9주차 자료와 수업 공지로 나갑니다.

---

## 2일차 · 27–30분 ② — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--stateflow로-상태-받기-60분) · [따라하기](walkthrough.md#2일차)

1. `ConnState.kt`와 [해제] 버튼을 만듭니다.
2. `ConnViewModel`의 `resultText`·`listener`를 `_state`·`_seconds`로 바꿉니다.
3. `MainActivity`에 틀 두 개를 넣고 `collect { }` 안을 채웁니다.
4. `연결 중… 3`에서 회전한 가로 화면, `준비됨`에서 [해제]만 켜진 화면을 캡처합니다.

**설명 합계: 5+8+10+4+3 = 30분**

---

## 제출하기

2일차가 끝나면 한 번 제출합니다.

1. **`ConnState.kt`, `ConnViewModel.kt`, `MainActivity.kt`**
2. **캡처 1**: `연결 중… 3`에서 회전한 가로 화면([중지]만 켜짐, ProgressBar 보임)
3. **캡처 2**: `준비됨` 화면. 가로 줄 [검색]·[중지]·[해제] 가운데 **[해제]만** 켜짐

---

## 다음 주 미리 보기

8주차는 **중간고사(개인 실기)**입니다. 범위는 2~7주차입니다.

1일차 리허설: 같은 화면에서 [시작] → 5초 카운트다운 → 완료 문구, [취소]로 중단, **회전해도 상태 유지(ViewModel + StateFlow)**

이번 주 틀 두 개와 `when`을 예제를 보지 않고 다시 써 보세요.
