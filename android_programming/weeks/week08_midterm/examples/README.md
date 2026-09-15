# 8주차 예제 — 중간고사 공개 리허설 Rehearsal

새 프로젝트 `Rehearsal`(package `com.example.rehearsal`)이 기준이다. 4주차부터 만든 `SmartIO`와는 별개의 작은 앱이다.
7주차 `examples/day2`의 `ConnViewModel`·`MainActivity` 모양을 버튼 두 개짜리 화면으로 줄였다. 새 문법은 없다.

- `rehearsal_starter/` — 1일차 리허설 시작 코드. 빌드·실행되고 `// TODO` 다섯 곳만 비어 있다. 시험 당일 받는 starter도 이런 모양이다.
- `rehearsal_solution/` — 자기 점검용 완성본. 먼저 혼자 풀고 나서 비교한다.

만드는 순서는 [따라하기](../walkthrough.md)에 있다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 | starter와 solution |
|---|---|---|
| [build.gradle.kts](rehearsal_starter/build.gradle.kts) | `Gradle Scripts › build.gradle.kts (Module :app)` | 같다. 4주차와 같은 의존성. 내 파일에는 4주차처럼 `buildFeatures`와 네 줄만 넣는다 |
| [AndroidManifest.xml](rehearsal_starter/AndroidManifest.xml) | `app › manifests › AndroidManifest.xml` | 같다. 새 프로젝트가 만든 것을 그대로 둔다(아이콘 등 줄이 더 있어도 된다) |
| [activity_main.xml](rehearsal_starter/activity_main.xml) | `app › res › layout › activity_main.xml` | 같다 |
| [strings.xml](rehearsal_starter/strings.xml) | `app › res › values › strings.xml` | 같다 |
| [res/values/themes.xml](rehearsal_starter/res/values/themes.xml) | `app › res › values › themes.xml` | 같다. 새 프로젝트가 만든 그대로(테마 이름 `Theme.Rehearsal`) |
| [MainActivity.kt](rehearsal_starter/MainActivity.kt) → [완성](rehearsal_solution/MainActivity.kt) | `app › kotlin+java › com.example.rehearsal › MainActivity.kt` | TODO(3)·(4)·(5)를 채운 것만 다르다 |
| [RehearsalViewModel.kt](rehearsal_starter/RehearsalViewModel.kt) → [완성](rehearsal_solution/RehearsalViewModel.kt) | 같은 package에서 New › Kotlin Class/File › Class | TODO(1)·(2)를 채운 것만 다르다 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.

## 화면과 이름

| View | id | 처음 글자(`strings.xml`) |
|---|---|---|
| 제목 `TextView` | 없음 | `Rehearsal` (`app_name`) |
| 상태 `TextView` | `stateText` | `대기 중` (`state_idle`) |
| 남은 시간 `TextView` | `timeText` | `남은 초: 0` (`time_idle`) |
| 버튼 | `startButton` | `시작` (`start`) |
| 버튼(`android:enabled="false"`) | `cancelButton` | `취소` (`cancel`) |

상태 문구는 `object` 상수 없이 글자 그대로 쓴다: `대기 중`, `카운트다운 중`, `완료`, `취소됨`. Logcat 태그는 `Rehearsal`이다.

## TODO와 완성 코드 줄

| TODO | starter 위치 | 할 일 | solution 줄 |
|---|---|---|---|
| (1) | `RehearsalViewModel.kt` 26~29행 | 이미 돌고 있으면 돌아가기, `job = viewModelScope.launch { }`, 5→1 카운트다운, 완료 | 26~40행 |
| (2) | `RehearsalViewModel.kt` 34행 | `job?.cancel()`, `취소됨` | 45~47행 |
| (3) | `MainActivity.kt` 35·40행 | `viewModel.startCountdown()` / `viewModel.cancelCountdown()` | 35·40행 |
| (4) | `MainActivity.kt` 47~48행 | `stateText`에 넣기, 버튼 켜기·끄기 | 47~55행 |
| (5) | `MainActivity.kt` 57행 | `timeText`에 `남은 초: N` | 64행 |

## 1. ViewModel 안의 코루틴 — viewModelScope.launch와 job 보관

```kotlin
if (job?.isActive == true) {
    return
}
job = viewModelScope.launch {
    _state.value = "카운트다운 중"
    for (i in 5 downTo 1) {
        _seconds.value = i
        delay(1000)
    }
    _seconds.value = 0
    _state.value = "완료"
}
```

| 실행 결과 | 화면 |
|---|---|
| [시작] 직후 | `카운트다운 중` / `남은 초: 5` |
| 1초마다 | `남은 초: 4` → `3` → `2` → `1` |
| 5초 뒤 | `완료` / `남은 초: 0` |

- `viewModelScope`는 ViewModel에 묶인 코루틴 범위다. 화면이 회전으로 다시 만들어져도 코루틴은 멈추지 않는다.
- 값은 View가 아니라 `_state.value`, `_seconds.value`에 넣는다. ViewModel에는 `binding`이 없다.
- 맨 위의 막음은 7주차 `startScan()`과 같다. 이미 돌고 있는데 또 누르는 틈을 막는다.

## 2. job?.cancel() — 취소하면 그 자리에서 멈춘다

```kotlin
fun cancelCountdown() {
    job?.cancel()
    _state.value = "취소됨"
}
```

| 실행 결과 | 화면 |
|---|---|
| `남은 초: 3`에서 [취소] | `취소됨` / `남은 초: 3`. 몇 초 기다려도 숫자가 그대로 |
| 이어서 [시작] | `카운트다운 중` / `남은 초: 5`부터 다시 |

- `launch`가 돌려준 `Job`을 `job`에 보관해야 멈출 수 있다. `job = `를 빠뜨려도 빌드는 되지만 [취소] 뒤에도 숫자가 계속 준다(예상 증상).
- `_seconds`는 0으로 되돌리지 않는다. 멈춘 숫자가 남아야 취소가 실제로 됐는지 화면으로 확인할 수 있다.

## 3. repeatOnLifecycle 틀 안의 collect — 값이 바뀌면 화면을 고친다

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            binding.stateText.text = state
            if (state == "카운트다운 중") {
                binding.startButton.isEnabled = false
                binding.cancelButton.isEnabled = true
            } else {
                binding.startButton.isEnabled = true
                binding.cancelButton.isEnabled = false
            }
        }
    }
}
```

| `state` | [시작] | [취소] |
|---|---|---|
| `대기 중`, `완료`, `취소됨` | 켬 | 끔 |
| `카운트다운 중` | 끔 | 켬 |

- 바깥 세 줄은 7주차 틀 그대로다. 학생이 채우는 곳은 `collect { }` 안뿐이다.
- `"카운트다운 중"` 글자는 ViewModel의 글자와 한 글자도 달라서는 안 된다. 다르면 빌드는 되고 [취소]가 켜지지 않는다.
- 남은 초는 같은 틀을 하나 더 써서 `viewModel.seconds.collect { seconds -> }`로 받는다. 상태와 남은 초가 서로 다른 TextView라 두 틀의 순서는 결과에 영향이 없다.

## 4. by viewModels() — 회전해도 같은 ViewModel

```kotlin
private val viewModel: RehearsalViewModel by viewModels()
```

| 실행 결과 | 화면 |
|---|---|
| `남은 초: 3`에서 회전 | 가로 화면이 곧바로 `카운트다운 중` / `남은 초: 3`, [취소]만 켬. 1초 뒤 `2` |
| `완료`·`취소됨`에서 회전 | 그대로 |
| 뒤로 가기로 앱을 닫고 다시 열기 | `대기 중` / `남은 초: 0` (ViewModel도 정리된다) |

- 회전하면 `MainActivity`는 새로 만들어지지만 `by viewModels()`는 같은 `RehearsalViewModel`을 돌려준다. 새 화면의 `collect`는 마지막 값을 곧바로 받는다.
- `RehearsalViewModel()`로 직접 만들면 빌드는 되지만 회전할 때마다 새 객체가 생겨 `대기 중`으로 돌아간다(예상 증상).

## 5. "남은 초: $seconds" — $변수 바로 뒤에 한글을 붙이지 않는다

```kotlin
binding.timeText.text = "남은 초: $seconds"
```

- `"$seconds초 남음"`처럼 쓰면 Kotlin이 한글까지 이름으로 읽어 `Unresolved reference 'seconds초'.` 오류로 빌드가 안 된다.
- 단위를 앞에 두거나 `$seconds` 뒤에 공백을 둔다.

## 채점표 항목과 코드 줄

| 다시 쓰는 개념(처음 배운 주) | `rehearsal_solution` 줄 | 채점표 항목(20점) |
|---|---|---|
| `setOnClickListener`·`isEnabled`로 버튼 제어(2·5주) | `MainActivity.kt` 34~41행, 49~55행 | UI·이벤트 5 |
| `class … : ViewModel()`·`by viewModels()` — 회전해도 같은 객체(7주) | `RehearsalViewModel.kt` 13행, `MainActivity.kt` 20행 | 생명주기·복원 5 |
| `viewModelScope.launch` + `for (i in 5 downTo 1)` + `delay`, `Job` 보관·`job?.cancel()`(6·7주) | `RehearsalViewModel.kt` 22행, 27~40행, 45행 | 코루틴 delay·취소·오류 5 |
| `MutableStateFlow`/`StateFlow` — 안에서만 바꾸고 밖에는 읽기 전용(7주) | `RehearsalViewModel.kt` 16~19행 | StateFlow collect 3 |
| `repeatOnLifecycle(Lifecycle.State.STARTED)` 틀 안의 `collect`(7주) | `MainActivity.kt` 44~58행, 61~67행 | StateFlow collect 3 |

리허설에는 `try/catch`가 없다. 본시험의 코루틴 항목에는 실패 처리(6주차)가 들어갈 수 있다.

## 공식 참고 자료

- [ViewModel 개요 — Android Developers](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Android의 StateFlow와 SharedFlow — Android Developers](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [수명 주기 인식 코루틴 — Android Developers](https://developer.android.com/topic/libraries/architecture/coroutines)
