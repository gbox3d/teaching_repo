# 2주차 — 첫 Android 앱: 내 정보 화면과 카운터

## 이번 주 질문

> XML로 그린 앱 화면에 내 정보를 띄우고, Kotlin 코드로 그 화면을 바꿀 수 있을까?

1주차에는 Kotlin Playground에서 학번과 이름을 콘솔에 출력했다. 이번 주에는 Android Studio로
처음 앱을 만들어 같은 정보를 휴대폰 화면에 띄우고, 버튼을 누르면 숫자가 바뀌는 카운터를 만든다.

## 학습 목표

1. `Empty Views Activity` 템플릿으로 새 프로젝트를 만들고 에뮬레이터에서 실행한다.
2. `activity_main.xml`과 `MainActivity.kt`가 각각 무엇을 맡는지 한 문장으로 말한다.
3. LinearLayout의 `orientation`·`gravity`와 TextView의 `text`·`textSize`·`layout_marginTop`으로 학번·이름·전공 화면을 만든다.
4. `android:id`와 `findViewById`로 View를 찾아 글자를 바꾼다.
5. `setOnClickListener`와 `var`로 버튼을 누를 때마다 바뀌는 카운터를 만든다.

## 이번 주 결과물

```text
내 정보
학번: 20260001
이름: 홍길동
전공: 컴퓨터공학과

3
[-1] [초기화] [+1]
```

예제의 학번·이름·전공을 본인 정보로 바꾸면 된다. 마지막에는 두 파일과 실행 화면을 제출한다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 새 프로젝트, Project 창의 세 폴더, 화면 파일 두 개, LinearLayout, TextView 속성 | 프로젝트 실행 → LinearLayout으로 바꾸기 → 학번·이름·전공 표시 → 속성 바꿔 보기 | 내 정보 화면 |
| 2일차 | `android:id`, 템플릿 틀은 그대로 두기, `findViewById`, `setOnClickListener`, `var` 카운터 | 코드로 이름 바꾸기 → `+1` 버튼 → `-1`·`초기화` 직접 완성 → 회전 관찰 → 제출 | 버튼 카운터 앱 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 실습실 PC의 Android Studio와 에뮬레이터 (버전은 수업 공지와 [설치 안내](../../ta_setup_guide.md)를 따른다)
- 1주차에 만든 `StudentCard.kt`의 학번·이름 출력 코드
- 본인의 학번·이름·전공

## 이번 주 범위

| 문법·속성 | 이번 주에 알아둘 뜻 |
|---|---|
| `LinearLayout` | 안에 넣은 View를 순서대로 한 줄씩 쌓는 레이아웃 |
| `android:orientation` | `vertical`은 위에서 아래로, `horizontal`은 왼쪽에서 오른쪽으로 쌓는다 |
| `android:gravity="center"` | 안의 내용을 가운데로 모은다 |
| `wrap_content` / `match_parent` | 내용에 맞는 크기 / 부모만큼의 크기 |
| `sp` / `dp` | 글자 크기 단위 / 간격·크기 단위 |
| `android:layout_marginTop` / `android:layout_marginStart` | 위쪽 간격 / 왼쪽(시작) 간격. 옆으로 놓을 때 쓴다 |
| `android:id="@+id/nameText"` | View에 이름표를 붙인다. Kotlin에서는 `R.id.nameText`로 부른다 |
| `findViewById<TextView>(R.id.nameText)` | id로 화면의 View를 찾는다 |
| `nameText.text = "이름: $name"` | TextView의 글자를 바꾼다 |
| `plusButton.setOnClickListener { }` | 버튼을 누를 때마다 중괄호 안의 코드를 실행한다 |
| `class MainActivity : AppCompatActivity()`, `onCreate`, `insets` 블록 | 템플릿이 만든 **틀**. 지우지도 고치지도 않는다. 우리 코드는 `onCreate()` 안, `insets` 블록 아래에 넣는다 |
| `android:layout_weight="1"` (확장) | 남은 폭을 나눠 갖는 비율. 버튼 세 개에 `0dp` 폭과 함께 주면 가로로 균등해진다 |

문자열 resource(`strings.xml`), ConstraintLayout, 화면을 돌린 뒤 값 유지하기는 이후 주차에서 다룬다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [activity_main.xml](examples/day1/activity_main.xml) · [MainActivity.kt](examples/day1/MainActivity.kt)
- 2일차 완성 코드: [activity_main.xml](examples/day2/activity_main.xml) · [MainActivity.kt](examples/day2/MainActivity.kt)

## 완료 기준

- [ ] `Empty Views Activity`로 만든 `StudentCard` 앱이 에뮬레이터에서 실행된다.
- [ ] LinearLayout 안에 본인의 학번·이름·전공이 세 줄로 보인다.
- [ ] 코드에서 `findViewById`로 이름 TextView의 글자를 바꾼다.
- [ ] `+1`·`-1`·`초기화` 버튼으로 숫자가 바뀐다.
- [ ] 두 파일과 숫자 `3`이 보이는 실행 화면 1장을 제출한다.

## 다음 수업 연결

숫자를 올린 뒤 화면을 돌리면 숫자가 `0`으로 돌아간다. 3주차에는 화면이 다시 만들어지는
Activity 생명주기를 관찰하고, 화면을 돌려도 숫자가 남도록 상태를 저장한다.

## 공식 참고 자료

- [새 프로젝트 만들기 — Android Developers](https://developer.android.com/studio/projects/create-project)
- [앱 빌드 및 실행 — Android Developers](https://developer.android.com/studio/run)
- [View 레이아웃 — Android Developers](https://developer.android.com/develop/ui/views/layout/declaring-layout)
- [LinearLayout — Android Developers](https://developer.android.com/develop/ui/views/layout/linear)
- [버튼 — Android Developers](https://developer.android.com/develop/ui/views/components/button)
