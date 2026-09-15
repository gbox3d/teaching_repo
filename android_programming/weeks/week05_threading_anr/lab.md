# 5주차 실습 — 멈추지 않는 검색 버튼 만들기

4주차 `SmartIO` 프로젝트를 이어서 쓴다. 연결 화면에 [검색] 버튼을 달고, 5초 걸리는 검색을 흉내 내면서
화면이 멈추지 않게 만든다. 모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 검색 버튼을 멈추지 않게 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 4주차 `SmartIO`를 열어 실행하고, `strings.xml`에 문자열 세 개를 추가한다 |
| 10–20분 | `activity_main.xml`에 [검색] 버튼과 상태 TextView를 배치한다 |
| 20–30분 | `Thread.sleep(5000)`을 클릭 리스너에 넣어 멈춤을 관찰하고 기록한 뒤 지운다 |
| 30–50분 | `Thread { }`와 `runOnUiThread { }`로 고쳐 검색 중·검색 완료 흐름을 완성한다 |
| 50–55분 | `runOnUiThread`를 빼면 어떻게 되는지 관찰하고 되살린다 |
| 55–60분 | 검색 중 화면을 캡처하고 프로젝트를 저장한다 |

### 1. 문자열과 화면 준비하기

1. `strings.xml`의 4주차 아홉 줄은 그대로 두고 `scan`(검색), `stop`(중지), `state_idle`(대기 중) 세 줄을 추가한다. 전체는 [따라하기 2단계](walkthrough.md#2-문자열-추가하기)에 있다.
2. `activity_main.xml`의 Switch와 [연결] 사이에 `scanButton` 버튼과 `stateText` TextView를 추가한다. 4주차 `deviceNameEdit`·`autoSwitch`·`connectButton`은 그대로 둔다. 전체는 [따라하기 3단계](walkthrough.md#3-검색-버튼과-상태-글자-배치하기)에 있다.
3. 실행해서 [검색]과 `대기 중`이 보이면 다음으로 간다.

### 2. 멈춤 관찰하기

`onCreate()` 마지막 `}` 바로 위(4주차 자동 연결 Switch 코드 아래)에 아래 코드를 넣고 실행한다. [검색]을 누르고 바로 Switch를 켜 본다.

```kotlin
binding.scanButton.setOnClickListener {
    binding.stateText.text = "검색 중…"
    Thread.sleep(5000)
    binding.stateText.text = "검색 완료"
}
```

| 질문 | 예상 | 실제 |
|---|---|---|
| `검색 중…`이 화면에 보이는가? |  |  |
| 5초 동안 Switch가 켜지는가? |  |  |
| Logcat에 `Skipped … frames!` 줄이 있는가? |  |  |

관찰을 적었으면 이 코드를 **지운다.** 메인 스레드에서 5초를 기다리는 코드는 최종본에 남기지 않는다.

### 3. Thread와 runOnUiThread로 고치기

2번 코드를 지운 자리에 새로 만든다. 요구 사항:

- [검색]을 누르면 `binding.scanButton.isEnabled = false`, `stateText`는 `검색 중…`.
- `Thread { … }.start()` 안에서 `Thread.sleep(5000)`.
- 5초 뒤 `runOnUiThread { … }` 안에서 `검색 완료`, 버튼 복구, Toast `검색 완료`.

힌트:

- 새 스레드에서 기다리고, 화면을 바꾸는 줄은 **모두** `runOnUiThread { }` 안에 둔다.
- `Toast`가 빨간색이면 Alt+Enter로 import한다.
- 장치 이름을 `검색 완료: $name`처럼 함께 보이려면 `val name = binding.deviceNameEdit.text.toString()`을 `Thread { }` **바깥**(클릭 리스너 첫 줄)에서 만든다. 람다 안에서 바깥 변수를 그대로 쓸 수 있다.
- 막히면 [따라하기 5단계](walkthrough.md#5-thread와-runonuithread로-고치기)와 [1일차 완성 코드](examples/day1/MainActivity.kt)를 한 줄씩 비교한다.

| 조작 | 예상 화면 | 실제 |
|---|---|---|
| [검색] 누른 직후 |  |  |
| 검색 중에 Switch 켜기 |  |  |
| 5초 뒤 |  |  |

### 4. 워커 스레드에서 View 만지기 (관찰만)

`runOnUiThread {`와 짝이 되는 `}` 두 줄을 지우고 [검색]을 눌러 본다. 5초 뒤 무슨 일이 생기는지, Logcat의 빨간 줄 첫 문장을 적는다.
적었으면 두 줄을 되살린다.

### 5. 오늘 확인할 것

- [ ] [검색]을 누르면 `검색 중…`이 **바로** 보이고 버튼이 회색이 된다.
- [ ] 검색 중에 Switch와 [연결]이 눌린다.
- [ ] 5초 뒤 `검색 완료`, 버튼 복구, Toast가 보인다.
- [ ] `Thread.sleep`은 `Thread { }` 안에만 있고, View를 바꾸는 줄은 `runOnUiThread { }` 안에만 있다.
- [ ] 검색 중 화면을 캡처했다.

## 2일차 — Handler로 예약하고 [중지]로 취소하기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 프로젝트를 열어 실행하고, `activity_main.xml`에 [중지]와 ProgressBar를 배치한다 |
| 10–20분 | `Handler(Looper.getMainLooper())`를 만들고 검색 끝에 할 일 `finishScan`을 `Runnable`로 만든다 |
| 20–35분 | [검색]을 `postDelayed`로, [중지]를 `removeCallbacks`로 완성한다 |
| 35–45분 | 검색 중에만 ProgressBar가 보이는지 확인하고, 네 가지(두 버튼·원·글자)가 함께 바뀌는지 표와 대조한다 |
| 45–55분 | 검색→완료, 검색→중지 두 가지를 확인한다 |
| 55–60분 | 캡처 2장과 파일을 정리해 제출한다 |

### 1. 화면 배치하기

[따라하기 9단계](walkthrough.md#9-중지-버튼과-progressbar-배치하기)의 XML로 1일차 [검색] 버튼 자리에 [검색] [중지]를 나란히 놓고 그 아래 `scanProgress` ProgressBar를 둔다.

- [중지]는 `android:enabled="false"`, ProgressBar는 `android:visibility="gone"`으로 시작한다.
- 실행하면 [중지]가 회색이고 원은 보이지 않는다.

### 2. Handler와 finishScan 만들기

1. 클래스 안, `onCreate()` 바깥에 `private val handler = Handler(Looper.getMainLooper())`를 둔다. import는 **`android.os`** 것을 고른다.
2. `onCreate()` 안에서 1일차 [검색] 코드를 지우고, 검색이 끝났을 때 할 일을 `val finishScan = Runnable { … }`로 만든다.
   안에는 `검색 완료` 표시, ProgressBar `View.GONE`, [검색] 활성, [중지] 비활성, Toast 다섯 가지가 들어간다.

### 3. [검색]과 [중지] 완성하기

아래 표대로 동작하도록 두 버튼의 클릭 리스너를 직접 만든다.

| 상황 | [검색] | [중지] | ProgressBar | 상태 글자 |
|---|---|---|---|---|
| [검색] 누름 | 비활성 | 활성 | `View.VISIBLE` | `검색 중…` |
| 5초 뒤 `finishScan` | 활성 | 비활성 | `View.GONE` | `검색 완료` + Toast |
| [중지] 누름 | 활성 | 비활성 | `View.GONE` | `검색 중지` |

힌트:

- 예약은 `handler.postDelayed(finishScan, 5000)`, 취소는 `handler.removeCallbacks(finishScan)` 한 줄씩이다.
- `Thread`와 `runOnUiThread`는 더 이상 필요 없다. `Handler`가 메인 스레드에서 실행해 준다.
- 취소가 되지 않으면 `removeCallbacks`에 `finishScan`이 아닌 다른 `{ }`를 넘기고 있는지 본다.
- 막히면 [따라하기 12단계](walkthrough.md#12-검색으로-예약하고-중지로-취소하기)를 본다.

### 4. 두 가지 흐름 확인하기

완성한 앱으로 아래 두 가지를 해 보고 실제를 적는다. 두 번째는 5초가 지나도 `검색 완료`·Toast가 **없어야** 한다.

| 조작 | 예상 | 실제 |
|---|---|---|
| [검색] → 그대로 5초 |  |  |
| [검색] → 2초 뒤 [중지] → 그대로 5초 |  |  |

### 5. 오늘 확인할 것

- [ ] [검색]을 누르면 [검색] 비활성, [중지] 활성, 돌아가는 원, `검색 중…`이 함께 바뀐다.
- [ ] 5초 뒤 `검색 완료` Toast가 뜨고 원이 사라진다.
- [ ] [중지]를 누르면 `검색 중지`가 되고, 5초가 지나도 `검색 완료`가 뜨지 않는다.
- [ ] `MainActivity.kt`에 `Thread.sleep`이 없다.

## 막혔을 때

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'View'.` | `View.GONE`·`View.VISIBLE`을 쓰는 줄에서 Alt+Enter → `android.view.View`를 import한다 |
| `Cannot create an instance of an abstract class.` 와 `Unresolved reference 'postDelayed'.` | `Handler`를 `java.util.logging.Handler`로 import했다. 그 import 줄을 `import android.os.Handler`로 고친다 |
| `Argument type mismatch: actual type is 'kotlin.Int', but 'java.lang.Runnable' was expected.` | `postDelayed(5000, finishScan)`처럼 순서를 바꿨다. `postDelayed(finishScan, 5000)`이다 |
| `Assignment type mismatch: actual type is 'kotlin.String', but 'kotlin.Int' was expected.` | `visibility = "gone"`처럼 글자를 넣었다. `View.GONE`을 넣는다 |
| `Assignment type mismatch: actual type is 'kotlin.String', but 'kotlin.Boolean' was expected.` | `isEnabled = "false"`처럼 글자를 넣었다. 따옴표 없이 `false`를 넣는다 |
| 노란 줄 `'constructor(): Handler' is deprecated. Deprecated in Java.` | `Handler()`로 만들었다. 실행은 되지만 `Handler(Looper.getMainLooper())`로 쓴다 |
| [검색]을 누르면 `검색 중…`이 안 보이고 5초 뒤 바로 `검색 완료`가 된다 | `Thread.sleep`이 `Thread { }` 밖(클릭 리스너 바로 안)에 있다. 1일차 2번 코드가 남아 있는지 본다 |
| 5초 뒤 앱이 꺼진다. Logcat: `CalledFromWrongThreadException: Only the original thread that created a view hierarchy can touch its views.` | `Thread { }` 안에서 `binding.…`을 직접 바꿨다. 그 줄들을 `runOnUiThread { }`로 감싼다 |
| [검색]을 누르면 `검색 중…`에서 영원히 멈추고 버튼이 회색이다 | `Thread { … }` 뒤에 `.start()`가 빠졌다. 빌드 오류는 나지 않는다 |
| [중지]를 눌러도 5초 뒤 `검색 완료`가 뜬다 | `removeCallbacks { }`처럼 새 중괄호를 넘겼거나, `finishScan`을 `Runnable { }`이 아니라 `{ }`로 만들었다. `val finishScan = Runnable { … }`, `removeCallbacks(finishScan)`으로 쓴다 |
| 노란색 경고 표시가 있다 | 실행에는 문제가 없다. 빨간 오류부터 해결한다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 세 가지

1. **`MainActivity.kt`**: Handler로 검색·중지가 동작하는 최종 코드
2. **`activity_main.xml`**: [검색] [중지] ProgressBar 상태 TextView가 있는 최종 XML
3. **실행 화면 2장**: 검색 중(버튼 비활성·돌아가는 원) 화면, `검색 완료` Toast 화면 또는 [중지] 뒤 `검색 중지` 화면

1일차 `Thread` 버전까지 동작하면 기본 성공이다. 2일차 [중지]와 ProgressBar는 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: 장치 이름이 비어 있으면 4주차처럼 Toast `장치 이름을 입력하세요`를 띄우고 검색을 시작하지 않게 해 본다(`if`/`else`).
- 2일차: [중지]를 누르면 Toast `검색을 중지했습니다`를 띄워 본다.
- 2일차: [검색]을 누른 뒤 상태 글자를 `검색 중… (5초)`로 바꾸고, 예약 시간을 `10000`으로 늘리면 글자도 함께 바꿔야 한다는 점을 느껴 본다. 남은 초를 세어 보이는 것은 6주차에 한다.
- 2일차: [검색]을 누른 뒤 바로 화면을 돌려 본다. 새 화면은 `대기 중`인데 5초 뒤 사라진 화면의 Toast `검색 완료`만 뜬다. 3주차 `onDestroy()`를 override해 `handler.removeCallbacksAndMessages(null)` 한 줄을 넣으면 남은 예약이 지워져 Toast가 뜨지 않는다. 회전해도 검색이 이어지게 하는 것은 7주차에 한다.

추가 과제는 선택 사항이다.
