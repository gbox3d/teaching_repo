---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 3주차
footer: Activity 생명주기 · Logcat · 저장과 복원
---

# Activity 생명주기와 상태 보존

2주차 마지막에 숫자를 `3`으로 만들고 화면을 돌리면 `0`이 되었습니다.
이번 주에는 **왜 그런지** Logcat으로 보고, 돌려도 `3`이 남게 만듭니다.

```text
회전 전                 회전 후
  3          →→→          3
[-1] [초기화] [+1]     [-1] [초기화] [+1]
```

---

# 1일차 — 화면의 일생을 Logcat으로 보기

`30분 설명·시연 → 60분 실습`

1. Logcat 창에서 내 앱의 기록만 골라 보기
2. 생명주기 콜백 7개에 `Log.d` 남기기
3. `+1`을 누르면 Toast 띄우기

---

## 1일차 · 0–8분 ① — Logcat: 앱이 남기는 기록

```kotlin
Log.d("Life", "onCreate")
```

| 1주차 (Playground) | 3주차 (앱) |
|---|---|
| `println("onCreate")` | `Log.d("Life", "onCreate")` |

- `Log.d(태그, 글자)`: Logcat 창에 한 줄을 남깁니다.
- 태그 `Life`는 우리가 정한 이름표입니다. 골라 볼 때 씁니다.
- `Log`가 빨간색이면 **Alt+Enter**(맥 ⌥+Enter) → `android.util.Log`

---

## 1일차 · 0–8분 ② — Logcat 창과 필터

1. 아래쪽 도구 막대의 **Logcat** (없으면 View › Tool Windows › Logcat)
2. 필터 칸에 `package:mine tag:Life` 입력 후 Enter
3. 실행하면 한 줄이 보입니다.

```text
Life   com.example.studentcard   D   onCreate
```

- `package:mine`: 내 앱만 · `tag:Life`: 태그가 `Life`인 줄만
- 아무것도 안 보이면 필터 철자와 기기 선택을 확인합니다.

---

## 1일차 · 8–20분 ① — 생명주기 콜백 7개

```text
onCreate → onStart → onResume    화면이 보이고 만질 수 있다
                        │ 홈 버튼 · 다른 앱 · 회전
                        ▼
              onPause → onStop → onDestroy
                          │
                 onRestart → onStart → onResume   (돌아올 때)
```

- 시스템이 때가 되면 **알아서 부릅니다.** 우리가 부르지 않습니다.
- 만들 때 3개, 사라질 때 3개, 돌아올 때 `onRestart` 1개 = 7개
- 이름을 외우지 말고 Logcat으로 **언제 불리는지** 봅니다.

---

## 1일차 · 8–20분 ② — override로 끼어들기

```kotlin
override fun onStart() {
    super.onStart()
    Log.d("Life", "onStart")
}
```

- `override fun`: 시스템이 부르는 함수에 **내 코드를 끼워 넣습니다.**
- `super.onStart()`: 원래 할 일을 먼저 하게 합니다. **지우면 앱이 꺼집니다.**
- 위치: `onCreate`의 마지막 `}` 아래, class의 마지막 `}` 위
- 나머지 다섯 개도 이름만 바꿔 같은 모양으로 씁니다.

---

## 1일차 · 8–20분 ③ — 회전하면 A가 죽고 B가 태어난다

```text
회전 전   MainActivity A   count = 3
            onPause → onStop → onDestroy        A는 사라진다
회전 후   MainActivity B   count = 0
            onCreate → onStart → onResume       B가 새로 태어난다
```

- 회전은 화면을 돌리는 게 아니라 **Activity를 새로 만드는 일**입니다.
- B의 `onCreate`에서 `var count = 0`이 다시 실행되어 `0`이 됩니다.
- 2일차: A가 사라지기 전에 **저장**하고, B가 태어날 때 **복원**합니다.

---

## 1일차 · 20–25분 — Toast: 잠깐 떴다 사라지는 알림

```kotlin
Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()
```

| 재료 | 뜻 |
|---|---|
| `this` | 어디에: 이 화면(MainActivity) |
| `"지금 숫자: $count"` | 무엇을: 보여 줄 글자 |
| `Toast.LENGTH_SHORT` | 얼마나: 짧게 (`LENGTH_LONG`은 길게) |

- 끝의 `.show()`를 빼면 만들기만 하고 보이지 않습니다.
- `Toast`가 빨간색이면 Alt+Enter → `android.widget.Toast`

---

## 1일차 · 25–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--생명주기-로그와-toast-60분) · [따라하기](walkthrough.md#1일차)

1. 2주차 프로젝트를 열고 Logcat 필터 `package:mine tag:Life`를 겁니다.
2. 콜백 7개에 `Log.d`를 넣고 실행·홈·복귀·회전·뒤로 순서를 기록표에 적습니다.
3. `+1`을 누르면 Toast가 뜨게 합니다.

**설명 합계: 8+12+5+5 = 30분**

막히면 `super` 줄, `override`, import부터 확인합니다.

---

# 2일차 — 회전해도 숫자가 남게

`30분 설명·시연 → 60분 실습`

1. 오늘 문법: 비어 있을 수 있는 값 다루기
2. 사라지기 전에 저장: `onSaveInstanceState`
3. 태어날 때 복원: `savedInstanceState`

---

## 2일차 · 0–5분 — 오늘 문법: null 안전성

```kotlin
val bag: Bundle? = null        // ?  : 비어 있을(null) 수 있는 타입
bag?.getInt("count")           // ?. : bag이 null이면 이 식 전체가 null
bag?.getInt("count") ?: 0      // ?: : 왼쪽이 null이면 0을 쓴다
```

- `?`가 붙은 타입은 값이 **없을 수도** 있다는 뜻입니다.
- `!!`는 쓰지 않습니다. null이면 앱이 꺼집니다.
- `onCreate(savedInstanceState: Bundle?)`의 `savedInstanceState`가 바로 이 타입입니다.
  처음 실행은 null, 회전 뒤에는 저장해 둔 값이 들어 있습니다.

---

## 2일차 · 5–17분 ① — count를 class 바로 안으로

```kotlin
class MainActivity : AppCompatActivity() {
    var count = 0

    override fun onCreate(savedInstanceState: Bundle?) {
```

- `onCreate` 안의 `var count = 0`은 `onCreate` 안에서만 보입니다.
- 저장하는 함수에서도 써야 하므로 **class 바로 안**으로 옮깁니다.
- `onCreate` 안의 `var count = 0` 줄은 지웁니다. 버튼 코드는 그대로 둡니다.

---

## 2일차 · 5–17분 ② — onSaveInstanceState로 저장

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putInt("count", count)
    Log.d("Life", "onSaveInstanceState count=$count")
}
```

- 화면이 사라지기 전에 시스템이 부릅니다. `outState`는 값을 담는 가방(Bundle)입니다.
- `putInt("count", count)`: 이름표 `"count"`를 붙여 숫자를 넣습니다.
- `outState: Bundle`에는 `?`가 **없습니다.** 가방은 항상 옵니다.

---

## 2일차 · 5–17분 ③ — onCreate에서 복원

```kotlin
count = savedInstanceState?.getInt("count") ?: 0
countText.text = "$count"
```

| 상황 | `savedInstanceState` | `count` |
|---|---|---|
| 처음 실행 | null | `0` |
| 회전 뒤 | 저장해 둔 가방 | `3` |

- 넣을 때 쓴 이름표 `"count"`와 꺼낼 때 이름표가 **한 글자도** 달라선 안 됩니다.
- 꺼낸 숫자를 화면에도 다시 써 줍니다.

---

## 2일차 · 17–25분 — 복원 검증 절차

1. 실행 → `+1` 세 번 → `3`
2. 회전 → `3`이 남아 있다 **(캡처 1)**
3. Logcat **(캡처 2)**

```text
onPause → onStop → onSaveInstanceState count=3 → onDestroy
→ onCreate → onStart → onResume
```

4. 홈 → 복귀: `3` 그대로 (A가 살아 있어서)
5. 뒤로 → 다시 실행: `0` (끝낸 앱은 저장하지 않는다. 정상)

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--회전해도-숫자가-남게-60분) · [따라하기](walkthrough.md#2일차)

1. `count`를 class 바로 안으로 옮기고 `onSaveInstanceState`에서 저장합니다.
2. `onCreate`에서 `?.`와 `?:`로 꺼내 화면에 씁니다.
3. `3` → 회전 → `3`을 확인하고 캡처 2장을 남깁니다.

**설명 합계: 5+12+8+5 = 30분**

---

## 제출하기

2일차가 끝나면 세 가지를 한 번 제출합니다.

1. **`MainActivity.kt`**: 콜백 7개 로그, Toast, 저장·복원이 있는 최종 코드
2. **캡처 1**: 회전한 뒤에도 숫자 `3`이 보이는 화면
3. **캡처 2**: 회전할 때 `onSaveInstanceState count=3`이 찍힌 Logcat

---

## 다음 주 미리 보기

4주차부터 새 프로젝트 **SmartIO**를 만듭니다.

장치 이름을 **입력**받고, 스위치를 **켜고 끄고**, **두 번째 화면**으로 넘어갑니다.

`findViewById`는 4주차부터 ViewBinding으로 바뀝니다.
