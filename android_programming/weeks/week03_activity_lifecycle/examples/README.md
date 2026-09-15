# 3주차 예제 — 생명주기 로그와 저장·복원

2주차 `StudentCard` 프로젝트를 이어서 쓴다. 아래 파일은 해당 날짜의 **완성본**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 코드와 비교한다.
학번 `20260001`, 이름 `홍길동`, 전공 `컴퓨터공학과`는 연습용 값이다.

## 파일과 넣을 위치

| 예제 파일 | 내 프로젝트에서 바꿀 파일 |
|---|---|
| [day1/activity_main.xml](day1/activity_main.xml) | `app › res › layout › activity_main.xml` — 2주차 완성본과 같다. 이번 주에는 고치지 않는다 |
| [day1/MainActivity.kt](day1/MainActivity.kt) | `app › kotlin+java › com.example.studentcard › MainActivity.kt` — 콜백 7개 로그와 Toast |
| [day2/activity_main.xml](day2/activity_main.xml) | `app › res › layout › activity_main.xml` — 1일차와 같다 |
| [day2/MainActivity.kt](day2/MainActivity.kt) | `app › kotlin+java › com.example.studentcard › MainActivity.kt` — 저장·복원 추가 |

`MainActivity.kt` 전체를 복사할 때 첫 줄 `package ...`는 내 프로젝트의 첫 줄을 그대로 둔다.

## 1. `Log.d`와 Logcat

```kotlin
Log.d("Life", "onCreate")
```

- 첫 번째 글자 `"Life"`는 태그(이름표), 두 번째 글자가 남길 내용이다.
- Logcat 필터 `package:mine tag:Life`를 걸면 내 앱의 `Life` 태그 줄만 보인다.
- `Log`는 `android.util.Log`다. 빨간색이면 Alt+Enter로 import한다.

## 2. 생명주기 콜백 7개

```kotlin
override fun onStart() {
    super.onStart()
    Log.d("Life", "onStart")
}
```

- `override fun`으로 시스템이 부르는 함수에 끼어든다. `super.onStart()`는 지우지 않는다.
- `onCreate`·`onStart`·`onResume`·`onPause`·`onStop`·`onRestart`·`onDestroy` 일곱 개 모두 같은 모양이다.

[day1/MainActivity.kt](day1/MainActivity.kt)를 넣고 실행했을 때 Logcat 순서(API 35 에뮬레이터):

| 행동 | Logcat 순서 |
|---|---|
| 실행 | `onCreate` → `onStart` → `onResume` |
| 홈 버튼 | `onPause` → `onStop` |
| 복귀 | `onRestart` → `onStart` → `onResume` |
| 회전 | `onPause` → `onStop` → `onDestroy` → `onCreate` → `onStart` → `onResume` |
| 뒤로 | `onPause` → `onStop` → `onDestroy` |

회전에서는 `onDestroy` 뒤에 `onCreate`가 다시 온다. Activity가 새로 만들어지므로 `onCreate` 안의 `var count = 0`이 다시 실행된다.

## 3. Toast

```kotlin
Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()
```

- `this`(이 화면)에 글자를 짧게 보여 준다. `.show()`가 없으면 보이지 않는다.
- `Toast`는 `android.widget.Toast`다.

## 4. 1일차 완성 — 로그와 Toast

[day1/MainActivity.kt](day1/MainActivity.kt)를 넣고 실행하면 화면은 2주차와 같고, `+1`을 누르면 `지금 숫자: 1` Toast가 뜬다.
Logcat에는 위 표의 순서가 찍힌다. 회전하면 숫자는 아직 `0`으로 돌아간다.

## 5. null 안전성

```kotlin
val bag: Bundle? = null        // ?  : 비어 있을(null) 수 있는 타입
bag?.getInt("count")           // ?. : bag이 null이면 이 식 전체가 null
bag?.getInt("count") ?: 0      // ?: : 왼쪽이 null이면 0을 쓴다
```

- `onCreate(savedInstanceState: Bundle?)`의 `savedInstanceState`가 이 타입이다. 처음 실행은 null이다.
- `!!`는 쓰지 않는다. null이면 앱이 꺼진다.

## 6. 저장과 복원

```kotlin
class MainActivity : AppCompatActivity() {
    var count = 0
```

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putInt("count", count)
}
```

```kotlin
count = savedInstanceState?.getInt("count") ?: 0
countText.text = "$count"
```

- `count`는 `onCreate`와 `onSaveInstanceState`가 함께 쓰므로 class 바로 안에 둔다.
- `onSaveInstanceState`는 화면이 사라지기 전에 시스템이 부른다. `outState`에 이름표 `"count"`로 숫자를 넣는다.
- `onCreate`에서 같은 이름표로 꺼내고, 없으면 `0`을 쓴다. 꺼낸 값은 화면에도 다시 쓴다.

## 7. 2일차 완성 — 회전해도 남는 숫자

[day2/MainActivity.kt](day2/MainActivity.kt)를 넣고 실행한 결과(API 35 에뮬레이터):

| 순서 | 할 일 | 결과 |
|---|---|---|
| 1 | `+1` 세 번 | `3` |
| 2 | 회전 | `3` 유지 |
| 3 | 회전한 채로 `+1` 한 번 | `4` |
| 4 | 홈 버튼 → 복귀 | `4` 유지 |
| 5 | 뒤로 → 다시 실행 | `0` (끝낸 앱은 저장하지 않는다) |

회전 때 Logcat:

```text
onPause
onStop
onSaveInstanceState count=3
onDestroy
onCreate
onStart
onResume
```

## 공식 참고 자료

- [Activity 생명주기 — Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [UI 상태 저장 — Android Developers](https://developer.android.com/topic/libraries/architecture/saving-states)
- [Logcat으로 로그 보기 — Android Developers](https://developer.android.com/studio/debug/logcat)
