---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 4주차
footer: SmartIO 시작 · ViewBinding · EditText · Switch · 두 번째 화면
---

# SmartIO 시작: ViewBinding·입력 위젯·두 번째 화면

지난 3주는 `StudentCard`였습니다.
오늘부터 학기 끝까지 키울 **Smart I/O Controller**를 새로 만듭니다.

```text
[연결 화면]                 [제어 화면]
장치 이름: ESP32_BLE_1  →   장치: ESP32_BLE_1
자동 연결 (O)               핀 번호: 3   LED (O)
      [연결]                명령 로그
                            on 3
                            off 3
```

---

# 1일차 — 연결 화면 만들기

`30분 설명·시연 → 60분 실습`

1. 새 프로젝트 `SmartIO`와 ViewBinding
2. 글자는 `strings.xml`에
3. `EditText`로 입력받고 `Switch`로 켜고 끄기

---

## 1일차 · 0–5분 — 오늘 문법: 문자열 만들기와 빈 값 검사

```kotlin
val pin = "3"
val command = "on $pin"        // "on 3"  (1주차 $변수 그대로)
val number = pin.toInt()       // 3      (글자 → 정수)
val name = ""
name.isEmpty()                 // true   (글자가 하나도 없다)
```

- `"on $pin"`: 13주차에 보드로 보낼 명령 문자열을 이렇게 만듭니다.
- `.toInt()`: 숫자가 아닌 글자면 앱이 꺼지므로 **빈 값 검사 뒤**에 씁니다.
- `isEmpty()`: 입력칸이 비었는지 볼 때 씁니다.

---

## 1일차 · 5–15분 ① — 새 프로젝트 SmartIO

1. **File › New › New Project** → **Empty Views Activity**
2. Name: `SmartIO` · Package: `com.example.smartio` · Language: **Kotlin**
3. **Finish** → 동기화가 끝나면 **Run ▶** → `Hello World!`

| 2주차 | 오늘 |
|---|---|
| `StudentCard` | `SmartIO` (앱 이름 Smart I/O Controller) |
| `findViewById` | **ViewBinding** `binding.xxx` |

`StudentCard`는 닫아 둡니다. 오늘부터는 `SmartIO`만 씁니다.

---

## 1일차 · 5–15분 ② — ViewBinding 켜기

`build.gradle.kts (Module :app)`의 `android { }` 안에 넣고 **Sync Now**

```kotlin
    buildFeatures {
        viewBinding = true
    }
```

- 켜면 레이아웃마다 클래스가 생깁니다: `activity_main.xml` → `ActivityMainBinding`
- `dependencies { }`에는 5~7주에 쓸 줄 네 개를 [따라하기 3단계](walkthrough.md#3-viewbinding-켜기와-의존성-넣기)대로 붙여 넣습니다.
  이번 주에는 쓰지 않으므로 빠져도 됩니다. Sync 오류가 나면 네 줄을 지우고 다시 Sync합니다.

---

## 1일차 · 5–15분 ③ — binding으로 View 부르기

```kotlin
private lateinit var binding: ActivityMainBinding      // 틀

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    enableEdgeToEdge()
    binding = ActivityMainBinding.inflate(layoutInflater)   // 틀
    setContentView(binding.root)                             // 틀
    ViewCompat.setOnApplyWindowInsetsListener(binding.main) { v, insets -> … }

    binding.connectButton.setOnClickListener { … }          // findViewById 없음
}
```

- `@+id/connectButton` → `binding.connectButton`. 철자가 다르면 빨간 줄입니다.
- `lateinit var binding`은 "나중에 넣는다"는 표시입니다. 세 줄은 그대로 씁니다.

---

## 1일차 · 15–20분 — strings.xml과 Hardcoded string 경고

```xml
<!-- res/values/strings.xml -->
<string name="app_name">Smart I/O Controller</string>
<string name="connect">연결</string>
```

```xml
<Button android:text="@string/connect" … />
```

- XML에 글자를 직접 쓰면 노란 `Hardcoded string` 경고가 뜹니다(2주차에 본 것).
- 글자를 `strings.xml`에 모아 두고 `@string/이름`으로 부릅니다.
- 코드에서 만드는 문장(`"연결: $name"`)은 그대로 써도 됩니다.

---

## 1일차 · 20–27분 ① — EditText: 입력 읽기

```xml
<EditText android:id="@+id/deviceNameEdit"
    android:hint="@string/device_name_hint" android:inputType="text" … />
```

```kotlin
val name = binding.deviceNameEdit.text.toString()
if (name.isEmpty()) {
    Toast.makeText(this, "장치 이름을 입력하세요", Toast.LENGTH_SHORT).show()
} else {
    Toast.makeText(this, "연결: $name", Toast.LENGTH_SHORT).show()
}
```

- `hint`는 비었을 때 흐리게 보이는 안내 글자입니다.
- `.text`는 글자 상자이고, `.toString()`을 붙여야 String이 됩니다.

---

## 1일차 · 20–27분 ② — Switch: 켜짐·꺼짐

```xml
<Switch
    android:id="@+id/autoSwitch"
    android:text="@string/auto_connect" … />
```

```kotlin
binding.autoSwitch.setOnCheckedChangeListener { _, isChecked ->
    if (isChecked) {
        Toast.makeText(this, "자동 연결 켜짐", Toast.LENGTH_SHORT).show()
    }
}
```

- 화살표 앞 두 이름: 첫째는 스위치 자신(안 쓰므로 `_`), 둘째 `isChecked`는 켜졌는지.
- 켤 때도 끌 때도 `{ }`가 실행됩니다. `isChecked`로 구분합니다.

---

## 1일차 · 27–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--연결-화면-만들기-60분) · [따라하기](walkthrough.md#1일차)

1. `SmartIO`를 만들고 ViewBinding을 켭니다.
2. 제목·장치 이름 `EditText`·자동 연결 `Switch`·[연결] 버튼을 놓습니다.
3. [연결]: 비면 `장치 이름을 입력하세요`, 아니면 `연결: 이름` Toast.
4. Switch를 켜면 `자동 연결 켜짐` Toast. 끌 때는 **직접** 완성합니다.

**설명 합계: 5+10+5+7+3 = 30분**

막히면 `viewBinding = true`와 Sync, `binding.` 뒤 철자부터 확인합니다.

---

# 2일차 — 두 번째 화면으로 이름 넘기기

`30분 설명·시연 → 60분 실습`

1. `ControlActivity` 만들기와 Manifest
2. `Intent`·`putExtra`로 이름 넘기기, `finish()`로 돌아오기
3. 제어 화면: 핀 번호 · LED Switch · 명령 로그

---

## 2일차 · 0–5분 — 오늘 문법: 넘겨받은 값이 없을 때 · else if

```kotlin
val name = intent.getStringExtra("name") ?: ""
binding.deviceText.text = "장치: $name"
```

- `getStringExtra("name")`은 값이 **없을 수도** 있어서 `String?`입니다(3주차).
- `?: ""` — 없으면 빈 글자로. `!!`는 쓰지 않습니다.
- 넣는 쪽 `putExtra("name", …)`과 꺼내는 쪽의 `"name"`이 같아야 합니다.

```kotlin
if (pin.isEmpty()) { … } else if (isChecked) { … } else { … }
```

- `else if`: 조건을 하나 더 이어 붙입니다. `if` 안에 `if/else`를 넣어도 됩니다.

---

## 2일차 · 5–20분 ① — 두 번째 Activity 만들기

Project 창의 `com.example.smartio`에서 오른쪽 클릭
**New › Activity › Empty Views Activity**

| 항목 | 입력 |
|---|---|
| Activity Name | `ControlActivity` |
| Layout Name | `activity_control` (자동) |
| Launcher Activity | **체크하지 않음** |

세 파일이 생깁니다: `ControlActivity.kt` · `activity_control.xml` · Manifest의 한 줄

---

## 2일차 · 5–20분 ② — Manifest에 생긴 줄

`app › manifests › AndroidManifest.xml`

```xml
<activity
    android:name=".ControlActivity"
    android:exported="false" />
```

- Activity는 Manifest에 **등록**되어야 열 수 있습니다. 마법사가 자동으로 넣어 줍니다.
- 직접 만든 Activity 파일이면 이 줄을 손으로 넣어야 합니다.
- `exported="false"`: 다른 앱이 이 화면을 열 수 없다는 뜻입니다.

---

## 2일차 · 5–20분 ③ — Intent로 이동하고 값 넘기기

```kotlin
val intent = Intent(this, ControlActivity::class.java)
intent.putExtra("name", name)
startActivity(intent)
```

| 줄 | 뜻 |
|---|---|
| `Intent(this, ControlActivity::class.java)` | "여기서 ControlActivity로" — 명시적 Intent |
| `putExtra("name", name)` | 이름표 `"name"`에 값을 넣는다 |
| `startActivity(intent)` | 다음 화면을 연다 |

`Intent`가 빨간색이면 **Alt+Enter**로 `android.content.Intent`를 import합니다.

---

## 2일차 · 5–20분 ④ — 받는 쪽과 finish()

```kotlin
// ControlActivity.kt
val name = intent.getStringExtra("name") ?: ""
binding.deviceText.text = "장치: $name"

binding.backButton.setOnClickListener {
    finish()          // 이 화면을 닫고 이전 화면으로
}
```

```text
MainActivity ──startActivity──▶ ControlActivity
MainActivity ◀───finish()────── ControlActivity
```

뒤로 가기 버튼(◀)도 `finish()`와 같은 일을 합니다.

---

## 2일차 · 20–25분 — Activity와 Fragment

```text
Activity (화면 하나)            Activity
┌──────────────┐               ┌──────────────┐
│              │               │ Fragment A   │  ← 화면 조각
│  View들      │               ├──────────────┤
│              │               │ Fragment B   │  ← 바꿔 끼울 수 있다
└──────────────┘               └──────────────┘
```

- Fragment는 **Activity 안의 화면 조각**입니다. 한 Activity에 여러 개를 넣거나 바꿔 끼웁니다.
- 이번 학기 SmartIO는 Activity 두 개로 만듭니다. Fragment 시연은 9주차에 봅니다.

---

## 2일차 · 25–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--제어-화면과-명령-로그-60분) · [따라하기](walkthrough.md#2일차)

1. `ControlActivity`를 만들고 [연결]에서 이름을 넘겨 상단에 `장치: 이름`을 띄웁니다.
2. 핀 번호 `EditText`(`inputType="number"`), LED `Switch`, 로그 `TextView`를 놓습니다.
3. Switch를 켜면 `on 3`, 끄면 `off 3`을 로그에 `append`. 핀이 비면 Toast.
4. [뒤로]는 `finish()`. 캡처 2장을 제출합니다.

**설명 합계: 5+15+5+5 = 30분**

---

## 제출하기

2일차가 끝나면 네 가지를 한 번 제출합니다.

1. **`MainActivity.kt`**
2. **`ControlActivity.kt`**
3. **캡처 1**: 연결 화면에 장치 이름을 입력한 화면
4. **캡처 2**: 제어 화면 상단에 그 이름이 보이고 로그에 `on 3`·`off 3`이 쌓인 화면

---

## 다음 주 미리 보기

[연결]을 누르면 **바로** 제어 화면으로 넘어갑니다.

실제 장치 검색은 5초쯤 걸립니다. 그 5초 동안 화면이 멈추면 어떻게 될까요?

5주차에는 **메인 스레드와 백그라운드**를 배우고 [검색] 버튼을 만듭니다.
