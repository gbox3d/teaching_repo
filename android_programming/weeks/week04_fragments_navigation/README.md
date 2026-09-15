# 4주차 — SmartIO 시작: ViewBinding·입력 위젯·두 번째 화면

## 이번 주 질문

> 사용자가 입력한 장치 이름을 받아 두 번째 화면으로 넘기고, 그 화면에서 LED 명령을 쌓아 보여 줄 수 있을까?

2~3주차에는 `StudentCard` 앱에서 화면을 그리고 버튼으로 숫자를 바꾸고, 회전해도 값이 남게 했다.
이번 주부터는 학기 끝까지 키워 갈 **Smart I/O Controller** 앱(`SmartIO` 프로젝트)을 새로 만든다.
연결 화면에서 장치 이름을 입력해 제어 화면으로 넘기고, 제어 화면에서 LED Switch를 켜고 끌 때마다
`on 3`·`off 3` 같은 명령이 로그에 쌓이게 한다. 이 명령 문자열은 13주차에 실제 보드로 보낸다.

## 학습 목표

1. 새 프로젝트 `SmartIO`를 만들고 `buildFeatures { viewBinding = true }`를 켜서 `binding.xxx`로 View를 다룬다.
2. 화면의 글자를 `strings.xml`에 두고 `@string/이름`으로 부른다.
3. `EditText`에서 `text.toString()`으로 입력을 읽고, `isEmpty()`로 빈 값을 검사한다.
4. `Switch`의 `setOnCheckedChangeListener`에서 `isChecked`로 켜짐·꺼짐을 구분한다.
5. 두 번째 Activity를 만들고 명시적 `Intent`와 `putExtra`/`getStringExtra`로 이름을 전달하고 `finish()`로 돌아온다.

## 이번 주 결과물

```text
[연결 화면]                       [제어 화면]
Smart I/O Controller              장치: ESP32_BLE_1
┌ 장치 이름 ─────────┐            ┌ 핀 번호 ┐
│ ESP32_BLE_1        │            │ 3       │
└────────────────────┘            └─────────┘
자동 연결        (O)              LED        (O)
      [ 연결 ]                    명령 로그
                                  on 3
                                  off 3
                                  on 3
                                        [ 뒤로 ]
```

캡처 2장을 제출한다. 연결 화면에 장치 이름을 입력한 화면, 제어 화면 상단에 그 이름이 보이고 로그에 `on 3`·`off 3`이 쌓인 화면.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 오늘 문법(`"on $pin"`·`toInt()`·`isEmpty()`), 새 프로젝트와 ViewBinding, `strings.xml`, `EditText`·`Switch` | `SmartIO` 만들기 → ViewBinding 켜기 → 연결 화면 배치 → [연결] 빈 값 검사 Toast → Switch Toast | 연결 화면 |
| 2일차 | 오늘 문법(`getStringExtra(...) ?: ""`·`else if`), 두 번째 Activity, Manifest, `Intent`·`putExtra`·`finish()`, Fragment 한 장 | `ControlActivity` 만들기 → 이름 전달·표시 → 핀 `EditText`·LED `Switch`·로그 → [뒤로] → 제출 | 두 화면 앱 |

각 수업은 `설명·함께 따라하기 30분 + 실습 60분`이다. 먼저 끝난 학생은 실습지의 추가 과제를 해 보고,
시간이 필요한 학생은 따라하기 문서의 단계를 하나씩 반복한다.

## 준비

- 실습실 PC의 Android Studio와 에뮬레이터 (버전은 수업 공지와 [설치 안내](../../ta_setup_guide.md)를 따른다)
- 2주차의 `findViewById`·`setOnClickListener`, 3주차의 `Toast`와 `?:` 사용법
- 이번 주는 `StudentCard`를 이어 쓰지 않고 새 프로젝트 `SmartIO`를 만든다

## 이번 주 범위

| 문법·속성 | 이번 주에 알아둘 뜻 |
|---|---|
| `"on $pin"` | 1주차 `$변수`와 같다. 명령 문자열을 만들 때 쓴다 |
| `"3".toInt()` | 글자를 정수로 바꾼다. 숫자가 아닌 글자면 앱이 꺼지므로 빈 값 검사 뒤에 쓴다 |
| `name.isEmpty()` | 글자가 하나도 없으면 `true` |
| `if (…) { } else if (…) { } else { }` | 1주차 `if/else`에 조건을 하나 더 이어 붙인 것. `if` 안에 `if/else`를 넣어도 된다 |
| `buildFeatures { viewBinding = true }` | `build.gradle.kts`에 넣으면 레이아웃마다 `ActivityMainBinding` 같은 클래스가 생긴다 |
| `binding = ActivityMainBinding.inflate(layoutInflater)` / `setContentView(binding.root)` | 틀. `findViewById` 대신 `binding.connectButton`처럼 id로 바로 부른다 |
| `lateinit var binding` | 틀. "나중에 넣는다"는 표시로, `onCreate()`에서 넣는다 |
| `@string/connect` | `strings.xml`의 `<string name="connect">연결</string>`을 가리킨다 |
| `EditText` · `android:inputType` | 글자를 입력받는 칸. `text`면 글자, `number`면 숫자 키패드 |
| `binding.deviceNameEdit.text.toString()` | 입력칸의 글자를 String으로 꺼낸다 |
| `Switch` · `setOnCheckedChangeListener { _, isChecked -> }` | 켜고 끌 때마다 실행. `isChecked`가 `true`면 켜짐 |
| `Intent(this, ControlActivity::class.java)` | "이 화면에서 ControlActivity로" 가는 명시적 Intent |
| `intent.putExtra("name", name)` / `intent.getStringExtra("name") ?: ""` | 이름을 넣어 보내고, 받는 쪽에서 꺼낸다. 없으면 `""` |
| `startActivity(intent)` / `finish()` | 다음 화면을 연다 / 지금 화면을 닫고 이전 화면으로 돌아간다 |

Fragment는 "Activity 안의 화면 조각"이라는 한 장만 보고 9주차에 시연한다. 스레드·코루틴·ViewModel은 5~7주차에 다룬다.

## 수업 자료

- [슬라이드](slides.md)
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- 1일차 완성 코드: [build.gradle.kts](examples/day1/build.gradle.kts) · [strings.xml](examples/day1/strings.xml) · [activity_main.xml](examples/day1/activity_main.xml) · [MainActivity.kt](examples/day1/MainActivity.kt)
- 2일차 완성 코드: [MainActivity.kt](examples/day2/MainActivity.kt) · [ControlActivity.kt](examples/day2/ControlActivity.kt) · [activity_control.xml](examples/day2/activity_control.xml) · [strings.xml](examples/day2/strings.xml) · [AndroidManifest.xml](examples/day2/AndroidManifest.xml)

## 완료 기준

- [ ] `SmartIO` 프로젝트가 ViewBinding으로 실행되고 `MainActivity.kt`에 `findViewById`가 없다.
- [ ] 연결 화면의 글자(제목·힌트·버튼)가 `strings.xml`에서 온다.
- [ ] 장치 이름이 비면 Toast `장치 이름을 입력하세요`, 있으면 제어 화면으로 이동한다.
- [ ] 제어 화면 상단에 전달받은 이름이 `장치: 이름`으로 보인다.
- [ ] LED Switch를 켜면 `on 3`, 끄면 `off 3`이 로그에 쌓이고, 핀이 비면 Toast가 뜬다. [뒤로]로 연결 화면에 돌아온다.
- [ ] 캡처 2장(연결 화면 입력, 제어 화면 로그)과 `MainActivity.kt`·`ControlActivity.kt`를 제출한다.

## 다음 수업 연결

연결 화면의 [연결]은 지금 바로 다음 화면으로 넘어간다. 실제 장치 검색은 몇 초가 걸린다.
5주차에는 [검색] 버튼을 누르면 5초 동안 기다리는 일을 화면을 멈추지 않고 처리하는 방법(메인 스레드와 백그라운드)을 배운다.

## 공식 참고 자료

- [뷰 결합(ViewBinding) — Android Developers](https://developer.android.com/topic/libraries/view-binding)
- [문자열 리소스 — Android Developers](https://developer.android.com/guide/topics/resources/string-resource)
- [텍스트 필드(EditText) — Android Developers](https://developer.android.com/develop/ui/views/components/text-fields)
- [토글 버튼과 스위치 — Android Developers](https://developer.android.com/develop/ui/views/components/togglebutton)
- [다른 액티비티 시작하기 — Android Developers](https://developer.android.com/training/basics/firstapp/starting-activity)
- [Fragment 개요 — Android Developers](https://developer.android.com/guide/fragments)
