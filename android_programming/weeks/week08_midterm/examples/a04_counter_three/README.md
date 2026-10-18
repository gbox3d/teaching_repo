[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a04_counter_three — 버튼 셋 카운터

출처: [2주차 실습 제출](../../../week02_views_layout/lab.md#제출--세-가지) · 권장 10분 · 범위 2주

수업의 카운터 과제처럼 버튼 셋으로 숫자를 바꾼다. 누른 순서대로 숫자가 바뀌는 화면을 세 장 캡처한다.

## 할 일

1. 숫자 TextView(`id` `countText`, 글자 `0`, `40sp`) 아래에 가로 `LinearLayout` 을 두고 그 안에 버튼 셋을 놓는다. `-1`(`id` `minusButton`), `초기화`(`id` `resetButton`), `+1`(`id` `plusButton`). 버튼 사이에 `android:layout_marginStart="8dp"`.
2. `MainActivity.kt` 에 `var count = 0` 과 리스너 셋을 쓴다. `-1` 은 `1` 을 빼고, `초기화` 는 `0` 으로, `+1` 은 `1` 을 더하고, 셋 모두 `countText` 에 새 값을 보인다.
3. 실행하고 다음 순서로 눌러 캡처 세 장을 찍는다. `+1` 세 번(→ `3`) · 이어서 `-1` 한 번(→ `2`) · 이어서 `초기화`(→ `0`).

## 확인할 것

- [ ] 순서표대로 `3` → `2` → `0` 이 보이는 캡처 세 장.
- [ ] `초기화` 뒤 `-1` 을 누르면 `-1` 이 보인다(음수도 그대로 보인다).
- [ ] 버튼 셋이 가로 한 줄로 놓여 있다.

## 힌트

- `+1` 리스너를 복사해 **버튼 이름과 계산 줄만** 바꾼다. 세 리스너가 같은 `count` 와 `countText` 를 쓴다.
- 가로로 놓기: 안쪽 `LinearLayout` 에 `android:orientation="horizontal"`. 그 안의 버튼은 `wrap_content`.
- 리스너 안에서 `count` 를 바꾼 뒤 `countText.text = "$count"` 를 빠뜨리면 숫자는 바뀌어도 화면은 그대로다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 시작값 | `0` |
| 세 버튼 글자 / id | `-1`·`초기화`·`+1` / `minusButton`·`resetButton`·`plusButton` |
| 더하는 수 / 빼는 수 / 초기화 값 | `1` / `1` / `0` |
| 순서표 | `+1` 세 번 → `3`, `-1` 한 번 → `2`, `초기화` → `0` |

## 설명 물음(시험에서 1~2문장)

- 세 리스너의 코드에서 서로 다른 곳은 어디인가?
- `countText.text = "$count"` 에서 따옴표가 필요한 이유는 무엇인가?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
