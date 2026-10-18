# 8주차 — 중간고사(개인 실기)

## 이번 주 질문

> 1~7주 실습에서 한 번씩 만든 것을, 값이 바뀐 문제지만 보고 **혼자 시간 안에** 다시 만들 수 있을까?

이번 주에는 새 문법을 배우지 않는다. 1~7주 실습에서 **실제로 제출한 것**을 한 문제씩으로 정리한 [문제 은행](examples/README.md)으로 연습하고(1일차), 같은 문제를 값만 바꾼 **중간고사**를 본다(2일차).
은행 문제는 수업에서 한 실습을 그대로 다시 하는 수준이다. 문제마다 **힌트**가 있고, 해답 대신 **확인할 것**이 있다. 에뮬레이터 화면과 Logcat 으로 그 항목을 하나씩 맞춰 보면 스스로 맞았는지 안다.

## 학습 목표

1. 은행 문제 하나를 읽고 "할 일"·"확인할 것"·"힌트"·"이 문제의 값"·"설명 물음"이 각각 무엇을 말하는지 구분한다. 시험에서는 "이 문제의 값" 표의 값만 바뀐다.
2. 수업에서 쓴 `StudentCard` 프로젝트(또는 새 프로젝트)에서 XML 과 Kotlin 을 고쳐 실행하고, "확인할 것"을 화면·Logcat 으로 하나씩 맞춘다.
3. 수업에서 나간 범위의 은행 문제를 모두 한 번씩 풀어 둔다. 어디서 막혔는지 알고 시험에 간다.
4. 2일차에 분반 공지가 정한 형식대로 답안(고친 코드·실행 화면 캡처·설명 1~2문장)을 시간 안에 낸다.

## 이번 주 결과물

```text
1일차  은행 문제를 푼 StudentCard 프로젝트와 캡처 — 연습용, 점수 없음
2일차  중간고사 답안 — 고친 XML·Kotlin 코드 + 에뮬레이터 캡처(필요하면 Logcat) + 설명 1~2문장
       내는 곳과 형식은 분반 공지
```

- 이번 주는 주차별 실습 점수 대상이 아니라 **중간고사 20점**으로 본다. 기준은 [채점표](rubric.md)에 있다.

## 2일 수업 흐름

| 일차 | 설명·안내 30분 | 60분 | 결과 |
|---|---|---|---|
| 1일차 | 이번 주는 문제 은행과 시험(같은 문제·값만 바뀜·해답 비공개·확인할 것·힌트) → 문제 하나 읽는 법([a03_name_button](examples/a03_name_button/)) → 확인하는 법(실행·캡처·Logcat) → 채점표 → 오늘 순서 | **연습**: 수업에서 나간 범위의 은행 문제를 차례로 → 문제마다 XML → Kotlin → 실행 → "확인할 것" → 캡처 | 연습 프로젝트와 캡처 |
| 2일차 | 연습에서 막힌 곳, 시험 규칙(분반 공지), 문제 읽는 순서, 답안에 넣을 것, PC 점검(프로젝트 실행·에뮬레이터) | **중간고사**: 공지한 시간 안에 은행 문제를 값만 바꾼 문제를 풀고 답안을 낸다 | 제출 |

각 수업은 `설명 30분 + 60분` 이다. 2일차 60분 가운데 공지한 시간이 **평가 시간**이다. 분 단위 순서는 [실습지](lab.md)에 있다.

## 준비

- 수업에서 쓴 `StudentCard` 프로젝트. 없거나 열리지 않으면 새 Empty Views Activity 프로젝트를 만든다([1주차 따라하기](../week01_android_kotlin/walkthrough.md#1-새-프로젝트-만들기)).
- 실습실 PC의 Android Studio와 에뮬레이터. 시험 날에는 1교시에 켜 두어 부팅을 끝낸다.
- 다시 읽어 둘 것: 2주차 `findViewById`·`setOnClickListener`·`var`, 3주차 `onSaveInstanceState`·`?.`·`?:`·`Log.d`. 4주차 이후를 배운 반은 `EditText`·`Toast`·`postDelayed`.
- 채점 기준을 미리 읽는다: [채점표](rubric.md) · [시험 운영 안내](exam_structure.md)
- 캡처: 에뮬레이터 창 옆 도구 막대의 카메라 버튼, 또는 Windows **Win+Shift+S** / macOS **⌘+Shift+4**. Logcat 캡처는 Android Studio 창을 찍는다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 중간고사(개인 실기) | midterm (individual hands-on exam) | 期中实操考试 |
| 문제 은행 | problem bank | 题库 |
| 할 일 | tasks | 任务 |
| 확인할 것 | checks | 检查项 |
| 힌트 | hint | 提示 |
| 이 문제의 값 | values of this problem | 本题的值 |
| 설명 물음 | explanation question | 说明题 |
| 캡처 | screenshot | 截图 |
| 채점표 | rubric | 评分表 |

## 이번 주 범위

시험은 1~7주 실습 제출에서만 낸다. 은행 문제는 일곱 개다. 범위는 1~7주 가운데 **수업에서 나간 주차까지**다. 아직 배우지 않은 주의 문제(예: `EditText`·`Toast`·`postDelayed` 를 안 했으면 a06·a07)는 시험에 내지 않는다. 어디까지인지는 분반 공지에 적는다.

| 범위 | 은행 문제 | 수업에서 한 것 | 권장 |
|---|---|---|---:|
| 1주 | [a01_kotlin_card](examples/a01_kotlin_card/) Kotlin Playground 학생 카드 | `val`·`$변수`·`if/else`·`fun` 으로 세 줄 출력 | 8분 |
| 2주 | [a02_info_screen](examples/a02_info_screen/) 내 정보 화면 | 세로 `LinearLayout`·`TextView`·`gravity` | 10분 |
| 2주 | [a03_name_button](examples/a03_name_button/) 코드로 글자 바꾸기와 버튼 하나 | `android:id`·`findViewById`·`setOnClickListener`·`var` | 10분 |
| 2주 | [a04_counter_three](examples/a04_counter_three/) 버튼 셋 카운터 | `+1`·`-1`·`초기화`, 가로 `LinearLayout` | 10분 |
| 3주 | [a05_keep_rotation](examples/a05_keep_rotation/) 회전해도 남는 count 와 생명주기 로그 | `onSaveInstanceState`·`Bundle`·`?.`·`?:`·`Log.d` | 10분 |
| 3~4주 | [a06_input_toast](examples/a06_input_toast/) 입력 칸과 Toast | `EditText` 글자 읽기, 빈 값이면 `Toast` | 10분 |
| 5~6주 | [a07_delay_message](examples/a07_delay_message/) 3초 뒤 글자 바꾸기 | `Handler.postDelayed`(또는 코루틴 `delay`), `isEnabled` | 10분 |

**범위 밖**: ViewBinding·Intent(배우지 않은 반), ViewModel·StateFlow, BroadcastReceiver·권한·ListView·BLE(10주 이후). 범위 밖 기능을 써도 가점은 없다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md) — 1일차 연습 절차, 2일차 시험 날 절차
- [실습과 시험 안내](lab.md)
- [문제 은행 목록](examples/README.md) — 1~7주 문제 일곱 개
- [시험 운영 안내](exam_structure.md) — 범위·형식·허용 자료·제출·장애 대체 절차
- [채점표](rubric.md) — 20점 항목과 기록 양식

## 완료 기준

- [ ] 1일차: 수업에서 나간 범위의 은행 문제를 풀어 "확인할 것"을 스스로 맞춰 봤고, 맞추지 못한 항목이 무엇인지 안다.
- [ ] 1일차: 각 문제의 설명 물음에 힌트를 가리고 한 문장씩 답할 수 있다.
- [ ] 2일차: 공지한 시간 안에 문제를 풀고, 고친 코드·캡처·설명을 공지한 곳에 냈다.

## 다음 수업 연결

9주차는 **앱 컴포넌트 비교와 1차 과제 발표**다. 지금까지 만든 화면은 모두 Activity였다.
9주차 1일차에는 Activity·Service·BroadcastReceiver·ContentProvider 네 컴포넌트를 비교하고, 2일차에는 1차 과제를 발표한다. → [9주차 README](../week09_services_project/README.md)

## 공식 참고 자료

- [LinearLayout — Android Developers](https://developer.android.com/develop/ui/views/layout/linear)
- [버튼 — Android Developers](https://developer.android.com/develop/ui/views/components/button)
- [Activity 생명주기 — Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [UI 상태 저장 — Android Developers](https://developer.android.com/topic/libraries/architecture/saving-states)
- [Logcat으로 로그 보기 — Android Developers](https://developer.android.com/studio/debug/logcat)
- [Toast — Android Developers](https://developer.android.com/guide/topics/ui/notifiers/toasts)
