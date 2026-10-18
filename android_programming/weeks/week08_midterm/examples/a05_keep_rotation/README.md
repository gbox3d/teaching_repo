[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a05_keep_rotation — 회전해도 남는 count 와 생명주기 로그

출처: [3주차 실습 제출](../../../week03_activity_lifecycle/lab.md#제출--세-가지) · 권장 10분 · 범위 3주

수업의 회전 과제처럼 화면을 돌려도 `count` 가 남게 하고, Logcat 으로 Activity 가 다시 만들어지는 것을 본다. a03 또는 a04 의 카운터에서 이어서 한다.

## 할 일

1. `var count = 0` 을 `onCreate` 밖, `class MainActivity` 바로 안으로 옮긴다.
2. `override fun onSaveInstanceState(outState: Bundle)` 를 추가하고 `super.onSaveInstanceState(outState)` 다음에 `outState.putInt("count", count)` 를 쓴다.
3. `onCreate` 에서 `count = savedInstanceState?.getInt("count") ?: 0` 으로 꺼내 `countText` 에 보인다.
4. `onCreate` 에 `Log.d("Life", "onCreate")`, `override fun onDestroy()` 안에 `Log.d("Life", "onDestroy")` 를 쓴다.
5. 숫자를 `3` 으로 만들고 에뮬레이터를 돌린다. 가로 화면에 `3` 이 남아 있는 캡처와, Logcat 을 `Life` 로 필터해 `onDestroy` 다음 `onCreate` 가 보이는 캡처를 찍는다. `MainActivity.kt` 전체를 답안에 붙인다.

## 확인할 것

- [ ] 회전한 뒤에도 숫자가 그대로다. 두 번 돌려도 그대로다.
- [ ] Logcat(`Life`)에 회전할 때 `onDestroy` 가 찍히고 바로 `onCreate` 가 찍힌다.
- [ ] 앱을 완전히 끄고(뒤로 가기) 다시 열면 `0` 이다. 저장은 회전처럼 Activity 가 다시 만들어질 때만 쓰인다.

## 힌트

- `putInt` 와 `getInt` 의 키 `"count"` 는 같은 글자여야 한다. 다르면 꺼낼 때 `null` 이 되어 `0` 으로 돌아간다.
- `?.` 는 `savedInstanceState` 가 `null`(처음 실행)이면 건너뛰고, `?: 0` 은 그때 쓸 값이다.
- import 두 줄: `import android.util.Log`, `import android.os.Bundle`(Bundle 은 템플릿에 이미 있다). 빨간 줄에 커서를 두고 Alt+Enter(맥 ⌥+Enter).
- 회전은 에뮬레이터 창 옆 도구 막대의 회전 버튼이다. Logcat 필터 칸에 `Life` 만 쳐도 된다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 저장 키 | `count` |
| 시작값(없을 때 쓸 값) | `0` |
| 회전 전에 만들 숫자 | `3` |
| 로그 태그 / 두 글자 | `Life` / `onCreate`·`onDestroy` |

## 설명 물음(시험에서 1~2문장)

- 저장하지 않으면 회전할 때 `count` 가 처음 값으로 돌아가는 이유는? Android 가 Activity 에 무엇을 하나?
- `savedInstanceState?.getInt("count") ?: 0` 에서 `?.` 와 `?: 0` 은 각각 무슨 뜻인가?
- `onSaveInstanceState` 는 언제 불리나? 화면이 사라지기 전인가, 뒤인가?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
