[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a07_delay_message — 3초 뒤 글자 바꾸기

출처: [5주차 실습 제출](../../../week05_threading_anr/lab.md#제출--세-가지) · 권장 10분 · 범위 5~6주(배운 반만)

버튼을 누르면 3초 뒤에 글자가 바뀐다. 기다리는 동안 화면이 멈추지 않아야 한다. 5주차 `Handler.postDelayed`(코루틴을 배운 반은 6주차 `delay`)를 쓴다.

## 할 일

1. 화면에 `Button`(`id` `startButton`, 글자 `시작`)과 `TextView`(`id` `stateText`, 글자 `대기 중`)를 둔다.
2. 버튼을 누르면 `stateText` 를 `검색 중…` 으로 바꾸고 버튼을 끈다(`isEnabled = false`).
3. 3초 뒤에 `stateText` 를 `검색 완료` 로 바꾸고 버튼을 다시 켠다. `Handler(Looper.getMainLooper()).postDelayed({ … }, 3000)` 을 쓴다. 코루틴을 배운 반은 `lifecycleScope.launch { delay(3000); … }` 로 해도 된다.
4. 캡처 두 장. 누른 직후(`검색 중…`, 버튼 회색)와 3초 뒤(`검색 완료`, 버튼 켜짐).

## 확인할 것

- [ ] 누른 직후 `검색 중…` 이 보이고 버튼이 회색이다.
- [ ] 3초쯤 뒤 `검색 완료` 가 보이고 버튼이 다시 눌린다.
- [ ] 기다리는 3초 동안 화면이 멈추지 않는다(다른 곳을 눌러도 반응한다). `Thread.sleep` 을 쓰지 않았다.

## 힌트

- 리스너 안에서 `Thread.sleep(3000)` 을 쓰면 화면이 3초 동안 멈춘다(5주차에 본 ANR 위험). 기다리는 일은 `postDelayed` 나 `delay` 에 맡긴다.
- `postDelayed` 의 두 인자는 나중에 실행할 코드 블록과 기다릴 밀리초다. `3000` 이 3초다.
- import: `android.os.Handler`, `android.os.Looper`. 코루틴이면 `androidx.lifecycle.lifecycleScope`, `kotlinx.coroutines.delay`, `kotlinx.coroutines.launch`.

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 버튼 id / 글자 | `startButton` / `시작` |
| 상태 TextView id / 처음 글자 | `stateText` / `대기 중` |
| 누른 직후 글자 | `검색 중…` |
| 기다리는 시간 | `3000`ms(3초) |
| 끝난 뒤 글자 | `검색 완료` |

## 설명 물음(시험에서 1~2문장)

- 리스너 안에서 `Thread.sleep` 으로 기다리면 안 되는 이유는 무엇인가?
- `postDelayed(블록, 3000)` 의 두 인자는 각각 무엇인가?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
