# 3주차 — Activity 생명주기와 상태 보존

## 이번 주 질문

> 화면을 돌리면 숫자가 `0`으로 돌아간다. 화면에는 무슨 일이 생기는 걸까, 숫자를 남기려면 어디에 저장해야 할까?

2주차 마지막에 숫자를 `3`으로 만들고 화면을 돌리면 `0`이 되는 것을 보았다. 이번 주에는 Android가 화면(Activity)을
만들고 없애는 순서를 Logcat으로 직접 확인하고, 화면이 다시 만들어져도 숫자가 남도록 저장하고 복원한다.
프로젝트는 2주차 `StudentCard`를 그대로 이어서 쓴다.

## 학습 목표

1. Logcat 창에서 `package:mine tag:Life` 필터로 내 앱의 `Log.d` 출력만 골라 본다.
2. 생명주기 콜백 7개(`onCreate`·`onStart`·`onResume`·`onPause`·`onStop`·`onRestart`·`onDestroy`)가 실행·홈·복귀·뒤로·회전에서 불리는 순서를 Logcat으로 확인한다.
3. `Toast`로 잠깐 떴다 사라지는 알림을 띄운다.
4. `?` 타입, `?.`, `?:`로 값이 비어 있을(null) 수 있는 변수를 안전하게 다룬다.
5. `onSaveInstanceState`와 `savedInstanceState`로 화면을 돌려도 숫자가 남게 한다.

## 이번 주 결과물

캡처 2장이다.

```text
(1) 회전한 뒤에도 숫자 3이 남아 있는 화면

내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과

3
[-1] [초기화] [+1]

(2) 회전할 때 찍힌 Logcat (필터 package:mine tag:Life)

onPause
onStop
onSaveInstanceState count=3
onDestroy
onCreate
onStart
onResume
```

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | Logcat 창과 태그 필터, `Log.d`, 생명주기 콜백 7개, 회전하면 화면이 새로 만들어지는 그림, `Toast` | 2주차 프로젝트에 콜백 7개와 `Log.d` 추가 → 실행·홈·복귀·회전·뒤로 순서를 기록표에 적기 → `+1`에 Toast | 콜백 순서 기록표와 Logcat |
| 2일차 | 오늘 문법 null 안전성, `onSaveInstanceState`로 저장, `onCreate`에서 복원, 검증 절차 | 저장·복원 구현 → `3` 만들고 회전해도 `3` 유지 캡처 → 콜백 순서 캡처 → 제출 | 회전해도 숫자가 남는 앱 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 2주차에 완성한 `StudentCard` 프로젝트. 없거나 동작하지 않으면 2주차 완성 코드([activity_main.xml](../week02_views_layout/examples/day2/activity_main.xml) · [MainActivity.kt](../week02_views_layout/examples/day2/MainActivity.kt))를 넣고 시작한다.
- 실습실 PC의 Android Studio와 에뮬레이터 (버전은 수업 공지와 [설치 안내](../../ta_setup_guide.md)를 따른다)

## 이번 주 범위

| 문법·속성 | 이번 주에 알아둘 뜻 |
|---|---|
| `Log.d("Life", "onCreate")` | Logcat에 태그 `Life`로 글자 한 줄을 남긴다. 1주차 `println`의 앱 버전 |
| Logcat 필터 `package:mine tag:Life` | 내 앱이 남긴 `Life` 태그 줄만 본다 |
| 생명주기 콜백 7개 | 화면이 만들어지고(`onCreate`·`onStart`·`onResume`), 사라지고(`onPause`·`onStop`·`onDestroy`), 돌아올 때(`onRestart`) 시스템이 부르는 함수 |
| `override fun onStart() { super.onStart() … }` | 시스템이 부르는 함수에 내 코드를 끼워 넣는다. `super` 줄은 지우지 않는다 |
| `Toast.makeText(this, "…", Toast.LENGTH_SHORT).show()` | 화면 아래에 잠깐 떴다 사라지는 알림 |
| `Bundle?` / `?.` / `?:` | 비어 있을 수 있는 타입 / 비어 있으면 건너뛰기 / 비어 있으면 대신 쓸 값 |
| `override fun onSaveInstanceState(outState: Bundle)` | 화면이 사라지기 전에 시스템이 부른다. `outState.putInt("count", count)`로 숫자를 넣는다 |
| `savedInstanceState?.getInt("count") ?: 0` | 넣어 둔 숫자를 꺼내고, 없으면(처음 실행) `0`을 쓴다 |

`!!`는 쓰지 않는다. 문자열 입력(`EditText`), 두 번째 화면, ViewModel은 이후 주차에서 다룬다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [activity_main.xml](examples/day1/activity_main.xml) · [MainActivity.kt](examples/day1/MainActivity.kt)
- 2일차 완성 코드: [activity_main.xml](examples/day2/activity_main.xml) · [MainActivity.kt](examples/day2/MainActivity.kt)

## 완료 기준

- [ ] Logcat에 `package:mine tag:Life` 필터를 걸고 `onCreate`·`onStart`·`onResume` 세 줄을 본다.
- [ ] 실행·홈·복귀·회전·뒤로 다섯 행동의 콜백 순서를 기록표에 적었다.
- [ ] `+1`을 누르면 Toast가 뜬다.
- [ ] 숫자를 `3`으로 만들고 회전해도 `3`이 남는다.
- [ ] `MainActivity.kt`와 캡처 2장(회전 뒤 `3`, 회전 시 Logcat)을 제출한다.

## 다음 수업 연결

다음 주는 [4주차 — SmartIO 시작: ViewBinding·입력 위젯·두 번째 화면](../week04_fragments_navigation/README.md)이다.
4주차부터는 새 프로젝트 `SmartIO`를 만든다. 글자를 입력받는 `EditText`, 켜고 끄는 `Switch`, 두 번째 화면으로
이동하는 `Intent`를 배우고, `findViewById` 대신 ViewBinding으로 View를 찾는다.

## 공식 참고 자료

- [Activity 생명주기 — Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [UI 상태 저장 — Android Developers](https://developer.android.com/topic/libraries/architecture/saving-states)
- [Logcat으로 로그 보기 — Android Developers](https://developer.android.com/studio/debug/logcat)
- [Toast — Android Developers](https://developer.android.com/guide/topics/ui/notifiers/toasts)
