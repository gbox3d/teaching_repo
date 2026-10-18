[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a03_name_button — 코드로 글자 바꾸기와 버튼 하나

출처: [2주차 실습 제출](../../../week02_views_layout/lab.md#제출--세-가지) · 권장 10분 · 범위 2주

2주차 2일차에 한 것처럼 `id` 로 TextView 를 찾아 글자를 바꾸고, 버튼 하나로 숫자를 바꾼다.

## 할 일

1. a02 의 화면(또는 수업 화면)에서 이름 TextView 에 `android:id="@+id/nameText"` 를 붙이고 글자를 `이름: ?` 로 둔다.
2. 그 아래에 숫자 TextView(`id` `countText`, 글자 `0`, `40sp`)와 Button(`id` `plusButton`, 글자 `+1`)을 추가한다.
3. `MainActivity.kt` 의 `onCreate` 안, `setContentView` 다음에 쓴다.
   - `findViewById` 로 `nameText` 를 찾아 글자를 `이름: 홍길동` 으로 바꾼다.
   - `var count = 0` 을 만들고, `plusButton` 을 누를 때마다 `count` 를 `1` 올려 `countText` 에 보인다.
4. 실행하고 `+1` 을 세 번 눌러 `3` 이 보이는 화면을 캡처한다. 고친 XML 과 Kotlin 코드도 답안에 붙인다.

## 확인할 것

- [ ] 처음 화면에 `이름: 홍길동` 이 보인다(XML 에 쓴 `이름: ?` 가 아니다). 숫자는 `0` 이다.
- [ ] `+1` 을 세 번 누르면 `3`, 다섯 번 누르면 `5` 다.
- [ ] Logcat 에 빨간 줄(`Unresolved reference`, `NullPointerException`)이 없다.

## 힌트

- 찾기: `val nameText = findViewById<TextView>(R.id.nameText)`. 바꾸기: `nameText.text = "이름: $name"`.
- 버튼: `plusButton.setOnClickListener { count = count + 1; countText.text = "$count" }`. 숫자를 글자로 넣을 때 따옴표가 필요하다.
- `R.id.nameText` 에 빨간 줄이 나면 XML 의 `android:id` 철자를 본다. `@+id/` 다음 이름과 `R.id.` 다음 이름이 글자까지 같아야 한다.
- 템플릿의 `enableEdgeToEdge()` 와 insets 블록은 지우지 않는다. 우리 코드는 그 아래에 쓴다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 이름 TextView id | `nameText` |
| 코드가 넣을 이름 글자 | `이름: 홍길동` |
| 숫자 TextView id / 시작값 | `countText` / `0` |
| 버튼 id / 글자 | `plusButton` / `+1` |
| 누를 때마다 더하는 수 | `1` |
| 확인 때 누르는 수 → 보여야 할 숫자 | `3` → `3` |

## 설명 물음(시험에서 1~2문장)

- XML 의 `android:id="@+id/countText"` 와 Kotlin 의 `R.id.countText` 는 어떻게 이어지나?
- `count` 는 왜 `val` 이 아니라 `var` 여야 하나?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
