# 8주차 실습 — 공개 리허설과 본시험

1일차 60분은 점수가 없는 **공개 리허설**이다. starter는 빌드·실행되고 `// TODO` 다섯 곳만 비어 있다. 2일차 **본시험**도 같은 모양이다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있지만, 리허설은 시험 연습이므로 **따라하기를 덮고 먼저 혼자** 푼다. 막히면 이 문서의 힌트 → [막혔을 때](#막혔을-때) → 따라하기 순서로 연다.

## 1일차 — 공개 리허설 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 새 프로젝트 `Rehearsal`에 starter 파일을 넣고 실행한다(따라하기 1~4단계) |
| 10–15분 | TODO 다섯 곳을 찾아 읽고 아래 2번 표를 채운다 |
| 15–30분 | TODO(1)·(2): ViewModel의 `startCountdown()`·`cancelCountdown()` |
| 30–42분 | TODO(3)~(5): 버튼 두 개와 `collect` 두 곳 |
| 42–52분 | 저장 → 다시 실행 → 8번 점검표 |
| 52–60분 | `rehearsal_solution`과 비교하고 채점표로 자기 채점한다 |

10분부터는 본시험 60분 시간 예산(열기 → ViewModel → 화면 → 점검 → 다시 실행 → 제출)을 줄인 순서다. 시계를 보면서 푼다.

### 1. starter 실행하기

[따라하기 1~4단계](walkthrough.md#1-새-프로젝트-만들기)로 프로젝트를 만들고 실행한다. 아래 화면이 뜨면 시작할 수 있다.

```text
Rehearsal
대기 중
남은 초: 0
[시작] [취소]        ← [취소]는 회색
```

[시작]을 눌러도 아무 일도 없다. starter는 **빌드·실행은 되고 기능만 비어 있는** 상태다. 시험 당일 받는 starter도 이렇게 확인한다.

### 2. TODO 읽고 나누기

Android Studio 메뉴 **View › Tool Windows › TODO**를 열면 TODO 다섯 곳이 모여 보인다. 각 TODO를 읽고 표를 채운다.

| TODO | 파일 | 바꾸는 것은 값인가, View인가 | 7주차에 비슷한 코드 |
|---|---|---|---|
| (1) |  |  |  |
| (2) |  |  |  |
| (3) |  |  |  |
| (4) |  |  |  |
| (5) |  |  |  |

- `_state`·`_seconds`가 나오면 값(ViewModel), `binding.`이 나오면 View(화면)다. ViewModel에는 `binding`이 없다.
- 채우는 순서는 **값을 만드는 쪽(1·2) → 받는 쪽(3·4·5)** 이다.

### 3. TODO(1) — 카운트다운 시작

`startCountdown()` 안에 TODO 문장대로 쓴다.

1. `job`이 이미 돌고 있으면 그냥 돌아간다.
2. 아니면 코루틴을 시작하고 그 `Job`을 `job`에 보관한다.
3. 코루틴 안: `_state`를 `"카운트다운 중"` → 5부터 1까지 `_seconds`에 넣으며 1초씩 기다림 → `_seconds`를 0, `_state`를 `"완료"`.
4. 로그 두 줄을 넣는다. `for` 안 첫 줄에 `Log.d("Rehearsal", "남은 초: $i")`, `_state`를 `"완료"`로 바꾼 다음 줄에 `Log.d("Rehearsal", "완료")`. 5번과 8번 점검표에서 이 로그로 코루틴이 도는지 본다.

- 7주차 `ConnViewModel.startScan()`과 모양이 거의 같다. 다른 점은 5초 뒤 연결을 시도하지 않고 `"완료"`로 끝나는 것이다.
- `delay`는 `launch { }` 안에서만 부를 수 있다.
- `Log`의 import(`import android.util.Log`)는 starter에 이미 들어 있다. `Log.d`는 3주차에 쓴 그 함수다.
- 다 쓰면 **Build › Make Project**로 빌드만 확인한다. 아직 화면은 바뀌지 않고 Logcat에도 아무것도 찍히지 않는다(버튼이 이 함수를 부르지 않는다).
- 예상 Logcat(5번까지 끝낸 뒤 [시작]): `남은 초: 5` → `남은 초: 4` → `남은 초: 3` → `남은 초: 2` → `남은 초: 1` → `완료`가 1초 간격으로 찍힌다.

### 4. TODO(2) — 취소

`cancelCountdown()` 안에서 보관한 `job`을 취소하고 `_state`를 `"취소됨"`으로 바꾼 뒤, 그다음 줄에 `Log.d("Rehearsal", "취소됨")`을 넣는다.

- 6주차 [중지]의 `scanJob?.cancel()`과 같다. `job`은 아직 `null`일 수 있다.
- `_seconds`는 건드리지 않는다. 멈춘 숫자가 화면에 남아야 취소가 됐는지 눈으로 확인할 수 있다.
- `Log`는 3번과 같은 import(`android.util.Log`, starter에 있음)를 쓴다.
- 예상 Logcat(6번까지 끝낸 뒤 [시작] → `남은 초: 3`에서 [취소]. 그 전에는 [취소]가 회색이라 누를 수 없다): `남은 초: 5` … `남은 초: 3` → `취소됨`. 그 뒤로 `남은 초`·`완료` 줄이 더 찍히지 않는다.

### 5. TODO(3) — 버튼에서 ViewModel 부르기

두 리스너 안에서 ViewModel 함수를 하나씩 부른다. 7주차 [검색] 리스너가 `viewModel.startScan()` 한 줄이었던 것과 같다.

실행하고 [시작]을 누른 뒤 Logcat 필터를 `package:mine tag:Rehearsal`로 맞춘다. `남은 초: 5` … `완료`가 찍히는데 화면은 `대기 중` 그대로다. 왜 그런지 한 문장으로 적는다.

### 6. TODO(4) — 상태를 받아 글자와 버튼 바꾸기

3번 틀의 `collect { state -> }` 안을 채운다.

- 받은 `state`를 `stateText`에 넣는다.
- `state`가 `"카운트다운 중"`이면 [시작] 끄기·[취소] 켜기, 아니면 반대(`isEnabled`). 1주차 `if/else` 한 번이면 된다.
- 비교 글자는 ViewModel에 쓴 `"카운트다운 중"`을 **복사해 붙인다**. 띄어쓰기 하나만 달라도 빌드는 되고 [취소]가 켜지지 않는다.

### 7. TODO(5) — 남은 초 받기

4번 틀의 `collect { seconds -> }` 안에서 `timeText`에 `남은 초: 3` 모양으로 넣는다.

- `$seconds` 바로 뒤에 한글을 붙이지 않는다(`"$seconds초"`는 빌드가 안 된다). 단위를 앞에 둔 `남은 초: ` 모양을 쓴다.

### 8. 점검표

저장(Ctrl+S, 맥 ⌘+S)하고 Run ▶으로 다시 실행한 뒤 위에서부터 차례로 해 본다. 회전은 에뮬레이터 창 옆 도구 막대의 회전 버튼으로 한다.

| 조작 | 보여야 할 것 | 내 앱 (O/X) |
|---|---|---|
| 앱 시작 | `대기 중` / `남은 초: 0` / [시작]만 켜짐 |  |
| [시작] | `카운트다운 중`, `남은 초: 5`→`4`→`3`→`2`→`1` 1초마다, [취소]만 켜짐 |  |
| 5초 뒤 | `완료` / `남은 초: 0`, [시작]만 켜짐 |  |
| 다시 [시작] → `남은 초: 3`에서 [취소] | `취소됨` / `남은 초: 3`, 몇 초 기다려도 숫자가 그대로 |  |
| 다시 [시작] → `남은 초: 3`에서 회전 | 가로 화면에 같은 글자·버튼, 1초 뒤 `2`로 이어짐 |  |
| `완료`에서 회전 | 그대로 `완료` / `남은 초: 0` |  |
| Logcat `tag:Rehearsal` | `취소됨` 뒤에 `남은 초` 줄이 더 없다. 회전해도 줄이 두 번씩 찍히지 않는다 |  |

X가 있으면 [막혔을 때](#막혔을-때)의 "빌드는 되는데" 줄부터 본다. 자기 점검용 캡처 3장(회전한 화면, 취소한 화면, 완료 화면)을 찍어 둔다.

### 9. 자기 채점

[채점표](rubric.md)로 20점 중 몇 점인지 매긴다. 리허설에는 실패하는 일이 없으므로 코루틴 항목의 오류 1점은 화면에서 "`완료` 뒤 다시 [시작]하면 `남은 초: 5`부터 다시 세고 두 번째도 `완료`로 끝난다"로 본다.
그다음 [rehearsal_solution](examples/rehearsal_solution/RehearsalViewModel.kt)과 내 코드를 비교해, 점수를 잃은 항목의 원인이 된 줄을 찾아 적는다.

## 2일차 — 본시험 (60분)

설명 30분 끝부분에서 PC 점검([따라하기 13단계](walkthrough.md#13-시험-전-pc-점검))을 마친 뒤 시작한다. 문항지와 starter는 시작할 때 받는다.

| 시간 | 할 일 |
|---|---|
| 0–5분 | starter를 열고 Sync가 끝나면 실행해 첫 화면 확인, 문항지와 TODO 읽기 |
| 5–25분 | ViewModel 쪽 TODO |
| 25–40분 | 화면 쪽 TODO |
| 40–50분 | 점검표: 시작·완료·취소·회전(문항에 실패가 있으면 실패도) |
| 50–55분 | 저장 → 다시 실행 |
| 55–60분 | 파일 두 개와 캡처 제출 |

### 1. 시작 전 점검

- [ ] 1일차 `Rehearsal` 프로젝트가 실행된다(Sync 끝남, 에뮬레이터 켜짐, Run 성공, Logcat 보임).
- [ ] 휴대폰은 가방에 넣었고, 브라우저에는 [허용 자료](exam_structure.md#허용-자료) 탭만 있다.
- [ ] [장애가 나면](exam_structure.md#장애가-나면) 손을 든다는 것을 안다.

### 2. 본시험 규칙

- 문항지에 적힌 문구·초 수·버튼 규칙을 그대로 쓴다. 리허설과 다른 곳에 밑줄을 긋고 시작한다.
- `activity_main.xml`·`strings.xml`은 문항이 요구하지 않으면 고치지 않는다. 채점에는 starter 원본이 쓰인다.
- 제출은 [시험 운영 안내의 제출](exam_structure.md#제출)을 따른다.

### 3. 시간이 모자랄 때

- 25분이 되면 ViewModel 쪽이 덜 끝났어도 화면 쪽 TODO로 넘어간다. 버튼과 `collect`만 있어도 확인되는 동작이 있다.
- 빨간 줄이 사라지지 않는 줄은 그 줄 앞에 `//`를 붙여 두고 넘어간다. **빌드되는 상태**를 유지해야 실행해서 점수를 받는다.
- 회전 확인은 코드를 고치지 않아도 되는 점검이다. 40–50분에 꼭 한다.

### 4. 제출

제출물은 `MainActivity.kt`, `○○ViewModel.kt`, 문항이 지정한 캡처다. 제출하기 전에 저장 → Run ▶ → 점검표를 한 번 더 한다.
파일은 Project 창에서 우클릭 › **Open In › Explorer**(맥 **Finder**)로 찾는다([따라하기 16단계](walkthrough.md#16-제출할-파일-찾기와-캡처)).

## 막혔을 때

| 상황 | 확인할 것 |
|---|---|
| starter를 붙여 넣자마자 `MainActivity.kt`에서 `Unresolved reference 'databinding'.`, 이어서 `Unresolved reference 'ActivityMainBinding'.`·`Unresolved reference 'startButton'.` 같은 줄이 여러 개 | 프로젝트 이름을 `Rehersal`처럼 잘못 만들어 package가 `com.example.rehersal`이 됐다. 붙여 넣은 두 파일은 `com.example.rehearsal`이다. Project 창의 폴더 이름을 보고, 두 파일 첫 줄 `package`와 `MainActivity.kt`의 `import com.example.rehearsal.databinding.ActivityMainBinding` 줄을 그 이름으로 고친다. 첫 오류 줄만 보면 된다(뒤의 줄은 모두 이 한 원인에서 나온다) |
| `Unresolved reference 'seconds초'.` | `$seconds` 바로 뒤에 한글을 붙였다. Kotlin은 한글도 이름 글자로 읽어 `seconds초`라는 변수를 찾는다. `"남은 초: $seconds"`처럼 단위를 앞에 둔다 |
| `Unresolved reference 'delay'.` | `import kotlinx.coroutines.delay` 줄이 지워졌다. `delay`에 커서를 두고 Alt+Enter(맥 ⌥+Enter)로 import한다 |
| `RehearsalViewModel.kt`에서 `Unresolved reference 'lifecycleScope'.` | ViewModel 안에서는 `viewModelScope`다. `lifecycleScope`는 Activity 쪽 이름이다 |
| `Suspend function 'suspend fun delay(timeMillis: Long): Unit' should be called only from a coroutine or another suspend function.` | `delay`가 `launch { }` 밖에 있다. 반복 전체를 `job = viewModelScope.launch { … }` 안에 넣는다 |
| `Cannot access 'val _state: MutableStateFlow<String>': it is private in 'com/example/rehearsal/RehearsalViewModel'.` | 화면에서 `_state`를 바꾸려 했다. 화면은 `state`를 읽기만 하고, 바꾸는 일은 `viewModel.cancelCountdown()` 같은 ViewModel 함수에 맡긴다 |
| `Assignment type mismatch: actual type is 'kotlin.String', but 'kotlin.Int' was expected.` | `_seconds`는 `MutableStateFlow(0)`이라 숫자만 받는다. `i`만 넣고 `"남은 초: "` 글자는 화면의 `collect` 안에서 붙인다 |
| `MainActivity.kt`에서 `Unresolved reference 'timeText'.` | 원인은 XML이다. `android:id="@+id/timeText"` 철자를 본다. id와 `binding.` 뒤 이름이 글자까지 같아야 한다 |
| `Android resource linking failed` 와 `AAPT: error: resource style/Theme.Rehersal (aka com.example.rehearsal:style/Theme.Rehersal) not found.` | Manifest의 `android:theme` 이름이 `themes.xml`의 `Theme.Rehearsal`과 다르다. 철자를 맞춘다 |
| 빌드는 되는데 [취소]를 누르면 `취소됨`이 됐다가 숫자가 계속 줄고 `완료`로 덮인다 | `job = viewModelScope.launch {`에서 `job = `를 빠뜨렸다. 보관하지 않으면 `job?.cancel()`이 멈출 코루틴이 없다. 빌드가 되므로 **[취소]를 누르고 몇 초 기다려 봐야** 드러난다 |
| 빌드는 되는데 [시작]을 누르면 5초 동안 화면이 멈췄다가 한꺼번에 `완료`가 된다. Logcat에는 1초마다 찍힌다 | `delay(1000)` 대신 `Thread.sleep(1000)`을 썼다. 코루틴 안에서 기다릴 때는 `delay`다(6주차) |
| 빌드는 되는데 카운트다운 중에 [취소]가 켜지지 않는다 (예상 증상) | `if (state == "카운트다운 중")`의 글자가 ViewModel의 글자와 다르다. ViewModel의 글자를 복사해 붙인다 |
| 빌드는 되는데 회전하면 `대기 중` / `남은 초: 0`으로 돌아간다 (예상 증상) | `by viewModels()` 대신 `RehearsalViewModel()`로 직접 만들었다. `private val viewModel: RehearsalViewModel by viewModels()`로 쓴다 |
| 빌드는 되는데 회전하면 `남은 초: 0`으로 돌아가고 더 바뀌지 않는다 (예상 증상) | `collect`를 `repeatOnLifecycle` 틀 밖(예: [시작] 리스너 안)에서 시작했다. 두 틀을 `onCreate()`에 두고 그 안에서 `collect`한다 |

"예상 증상"은 코드에서 정해지는 동작을 적은 것이며, 에뮬레이터 화면에서는 조금 다르게 보일 수 있다.
한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다(리허설에서만. 본시험에서는 구현 도움을 주지 않는다).

## 제출

- **1일차 리허설**: 제출하지 않는다. 캡처 3장과 자기 채점 결과는 본인이 보관한다.
- **2일차 본시험**: [시험 운영 안내의 제출](exam_structure.md#제출)을 따른다. 채점은 [채점표](rubric.md)로 한다.

## 먼저 끝났다면

1일차 리허설을 일찍 끝냈다면 아래를 해 본다. 모두 2~7주 범위다.

1. 카운트다운을 10초로 바꾸고, 회전·취소가 그대로 되는지 점검표를 다시 해 본다.
2. (채점표 '오류' 대비) 카운트다운이 끝나면 `확인 중`으로 바꾸고, 6주차 `connectFake()`처럼 1초 걸리고 절반은 실패하는 `checkFake()`를 ViewModel에 만들어 부른다. `try/catch`로 받아 성공이면 `완료`, 실패면 `실패`를 보여 준다. `확인 중`에는 두 버튼을 모두 끈다.
3. `onCreate()`의 insets 블록 아래에 `Log.d("Rehearsal", "onCreate")`를 넣고 카운트다운 중에 회전한다. Logcat에서 `onCreate`는 다시 찍히는데 `남은 초` 줄은 한 번씩 이어지는 것을 확인한다(3주차 생명주기 + 7주차 ViewModel).
4. [시작]을 누르고 홈으로 나갔다가 6초 뒤 돌아온다. 화면이 `완료`인지 본다.

추가 과제는 선택 사항이다.
