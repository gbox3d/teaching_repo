[8주 문제 은행](../README.md) · [실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/android_programming/weeks/week08_midterm)

# a02_info_screen — 내 정보 화면

출처: [2주차 실습 제출](../../../week02_views_layout/lab.md#제출--세-가지) · 권장 10분 · 범위 2주

2주차 1일차에 한 것처럼 `LinearLayout` 과 `TextView` 로 내 정보 화면을 만든다.

## 할 일

1. 수업에서 쓴 `StudentCard` 프로젝트(없으면 새 Empty Views Activity 프로젝트)에서 `activity_main.xml` 을 연다. 맨 바깥 레이아웃을 `LinearLayout` 으로 하고 `android:orientation="vertical"`, `android:gravity="center"` 를 준다.
2. `TextView` 네 개를 위에서부터 둔다. 제목 `내 정보`(`28sp`, `bold`), `학번: 20260001`(`20sp`), `이름: 홍길동`(`20sp`), `전공: 컴퓨터공학과`(`20sp`).
3. 제목 다음 TextView 에는 `android:layout_marginTop="24dp"`, 그 아래 둘에는 `8dp` 를 준다.
4. 실행하고 에뮬레이터 화면을 캡처한다.

## 확인할 것

- [ ] 네 줄이 화면 **가로·세로 가운데**에 위에서 아래로 쌓여 보인다.
- [ ] 제목이 가장 크고 굵다. 제목과 둘째 줄 사이가 다른 줄 사이보다 넓다.
- [ ] 캡처가 디자인 미리보기가 아니라 **실행된 에뮬레이터 화면**이다.
- [ ] 빨간 줄 없이 실행된다.

## 힌트

- `android:orientation="vertical"` 은 위에서 아래로 쌓고, `android:gravity="center"` 는 안에 든 것을 가운데로 모은다.
- 크기 값: `wrap_content` 는 내용만큼, `match_parent` 는 부모만큼. 글자 크기 단위는 `sp`, 간격 단위는 `dp`.
- 템플릿의 `ConstraintLayout` 을 `LinearLayout` 으로 바꾸면 `app:layout_constraint…` 줄은 지운다. `android:id="@+id/main"` 은 남겨 둔다(템플릿 코드가 쓴다).

## 이 문제의 값

| 값 | 이 문제에서 |
|---|---|
| 제목 | `내 정보` |
| 세 줄 | `학번: 20260001` · `이름: 홍길동` · `전공: 컴퓨터공학과` |
| 제목 크기 | `28sp`, 굵게 |
| 줄 크기 | `20sp` |
| 제목 아래 간격 / 줄 사이 간격 | `24dp` / `8dp` |

## 설명 물음(시험에서 1~2문장)

- `android:orientation` 과 `android:gravity` 는 각각 무엇을 정하나?
- `wrap_content` 와 `match_parent` 의 차이는 무엇인가?

시험에서는 같은 문제를 "이 문제의 값" 표의 값만 바꿔서 낸다. 문장·할 일·확인하는 방법은 그대로다. 답안에는 **코드(XML·Kotlin 가운데 고친 부분)·실행 화면 캡처·설명 물음의 답 1~2문장**을 낸다.
