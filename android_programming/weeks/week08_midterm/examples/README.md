[8주차 실습](../lab.md) · [따라하기](../walkthrough.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# 8주차 문제 은행 — 1~7주 실습 제출

1~7주 실습에서 제출한 것을 한 문제씩으로 정리했다. 문제마다 그 주에 배운 것만 쓰고, 프로젝트는 수업에서 쓴 `StudentCard`(또는 새 Empty Views Activity)를 그대로 쓴다. 시작 코드는 따로 없다. 수업에서 한 것을 다시 만든다.

- 2일차 중간고사는 이 은행에서 문제를 골라 **값만 바꿔** 낸다. 문장·할 일·확인하는 방법은 같고, "이 문제의 값" 표의 값(글자·id·숫자·키 이름)만 바뀐다.
- 해답은 공개하지 않는다. 문제 문장의 "확인할 것"이 모두 맞으면 된 것이다. 막히면 **힌트**를 읽는다. 시험의 설명 물음은 힌트에 있는 내용이다.
- 범위는 1~7주 가운데 **수업에서 나간 주차까지**다. a06·a07 은 4주차 이후를 배운 반만 범위다. 어디까지인지는 분반 공지에 적는다.

| 범위 | 문제 | 수업에서 한 것 | 권장 |
|---|---|---|---:|
| 1주 | [a01_kotlin_card](a01_kotlin_card/) Kotlin Playground 학생 카드 | `val`·`$변수`·`if/else`·`fun` 으로 세 줄 출력 | 8분 |
| 2주 | [a02_info_screen](a02_info_screen/) 내 정보 화면 | 세로 `LinearLayout` 과 `TextView` 로 학번·이름·전공 | 10분 |
| 2주 | [a03_name_button](a03_name_button/) 코드로 글자 바꾸기와 버튼 하나 | `android:id`·`findViewById`·`setOnClickListener`·`var` | 10분 |
| 2주 | [a04_counter_three](a04_counter_three/) 버튼 셋 카운터 | `+1`·`-1`·`초기화`, 가로 `LinearLayout` | 10분 |
| 3주 | [a05_keep_rotation](a05_keep_rotation/) 회전해도 남는 count 와 생명주기 로그 | `onSaveInstanceState`·`Bundle`·`?.`·`?:`·`Log.d` | 10분 |
| 3~4주 | [a06_input_toast](a06_input_toast/) 입력 칸과 Toast | `EditText` 의 글자 읽기, 빈 값이면 `Toast` | 10분 |
| 5~6주 | [a07_delay_message](a07_delay_message/) 3초 뒤 글자 바꾸기 | `Handler.postDelayed`(또는 코루틴 `delay`), 버튼 끄고 켜기 | 10분 |

문제 이름을 누르면 문제 문장(할 일·확인할 것·힌트·이 문제의 값·설명 물음)이 보인다.
