[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a06_input_toast — 입력 칸과 Toast

출처: [4주차 실습 제출](../../../week04_fragments_navigation/lab.md#제출--네-가지) · 권장 10분 · 범위 3~4주(배운 반만)

입력 칸의 글자를 읽어 화면에 보이고, 비어 있으면 `Toast` 로 알린다. 3주차 `Toast` 와 4주차 `EditText` 를 함께 쓴다.

## 할 일

1. 화면에 `EditText`(`id` `nameInput`, `android:hint="이름"`), `Button`(`id` `helloButton`, 글자 `인사`), `TextView`(`id` `helloText`, 글자 `?`)를 둔다.
2. 버튼을 누르면 `nameInput.text.toString().trim()` 으로 글자를 읽는다.
   - 비어 있으면 `Toast.makeText(this, "이름을 입력하세요", Toast.LENGTH_SHORT).show()`.
   - 있으면 `helloText.text = "안녕하세요, 이름님"` 처럼 읽은 이름을 넣어 보인다.
3. 캡처 두 장. 이름 `홍길동` 을 넣고 누른 뒤 `안녕하세요, 홍길동님` 이 보이는 화면, 빈 채로 눌러 Toast 가 뜬 화면.

## 확인할 것

- [ ] 이름을 넣고 누르면 `안녕하세요, 홍길동님` 이 보인다. 다른 이름을 넣으면 그 이름이 보인다.
- [ ] 빈 채로(또는 빈칸만) 누르면 Toast 가 뜨고 `helloText` 는 바뀌지 않는다.
- [ ] 빨간 줄 없이 실행된다.

## 힌트

- `EditText` 의 `text` 는 글자가 아니라 `Editable` 이라 `toString()` 이 필요하다. `trim()` 은 앞뒤 빈칸을 뗀다.
- `if (name.isEmpty()) { Toast… } else { helloText.text = "안녕하세요, ${name}님" }`. `$name님` 처럼 `$변수` 바로 뒤에 한글을 붙이면 변수 이름으로 읽히므로 중괄호를 쓴다.
- `Toast.makeText` 의 세 인자는 화면(`this`), 글자, 길이다. `.show()` 를 빠뜨리면 아무것도 안 뜬다.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 입력 칸 id / hint | `nameInput` / `이름` |
| 버튼 id / 글자 | `helloButton` / `인사` |
| 결과 TextView id / 처음 글자 | `helloText` / `?` |
| 인사 글자 꼴 | `안녕하세요, 이름님` |
| 빈 값 Toast 글자 | `이름을 입력하세요` |
| 확인 때 넣는 이름 | `홍길동` |

## 설명 물음(시험에서 1~2문장)

- `nameInput.text` 뒤에 `toString()` 이 필요한 이유는 무엇인가?
- `Toast.makeText(this, 글자, Toast.LENGTH_SHORT)` 의 세 인자는 각각 무엇인가?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
