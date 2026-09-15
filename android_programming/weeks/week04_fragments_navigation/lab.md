# 4주차 실습 — SmartIO 연결 화면과 제어 화면 만들기

이번 주부터 학기 끝까지 키울 `SmartIO` 프로젝트를 새로 만든다. 처음에는 예제를 그대로 옮기고,
실행에 성공하면 장치 이름과 핀 번호를 바꿔 가며 동작을 확인한다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 연결 화면 만들기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 새 프로젝트 `SmartIO`를 만들고 `Hello World!`를 실행한다 |
| 10–20분 | ViewBinding을 켜고 Sync, `MainActivity.kt`를 ViewBinding 틀로 바꿔 다시 실행한다 |
| 20–35분 | `strings.xml`에 글자를 넣고 연결 화면(제목·`EditText`·`Switch`·[연결])을 배치한다 |
| 35–50분 | [연결] 버튼의 빈 값 검사 Toast와 Switch Toast를 만든다 |
| 50–60분 | 이름을 입력한 화면을 캡처하고 확인 목록을 점검한다 |

### 1. 새 프로젝트와 ViewBinding

1. **File › New › New Project → Empty Views Activity**, Name `SmartIO`, Language `Kotlin`으로 만들고 실행한다.
2. `build.gradle.kts (Module :app)`의 `android { }` 안에 `buildFeatures { viewBinding = true }`를 넣고, `dependencies { }`에 [따라하기 3단계](walkthrough.md#3-viewbinding-켜기와-의존성-넣기)의 네 줄을 넣은 뒤 **Sync Now**를 누른다. 네 줄은 이번 주에 쓰지 않으므로 Sync 오류가 나면 지우고 다시 Sync해도 된다.
3. `MainActivity.kt`에 `private lateinit var binding: ActivityMainBinding`을 선언하고, `setContentView(R.layout.activity_main)`을 `binding = ActivityMainBinding.inflate(layoutInflater)` + `setContentView(binding.root)`로 바꾼다. `findViewById(R.id.main)`은 `binding.main`으로 바꾼다.

실행해서 `Hello World!`가 그대로 보이면 다음으로 간다. `ActivityMainBinding`이 빨간색이면 **Alt+Enter**로 import한다.

### 2. strings.xml과 연결 화면

`strings.xml`에 `app_name`(Smart I/O Controller)·`device_name_hint`·`auto_connect`·`connect` 네 개를 만들고,
`activity_main.xml`을 아래 결과가 되게 배치한다. 글자는 모두 `@string/이름`으로 쓴다.

```text
Smart I/O Controller
[ 장치 이름          ]   ← EditText, id deviceNameEdit, inputType text
자동 연결 (O)            ← Switch, id autoSwitch
     [ 연결 ]            ← Button, id connectButton
```

- 2주차처럼 루트 `LinearLayout`(`vertical`·`center`·`@+id/main`)을 쓴다.
- `EditText`에는 `android:hint`와 `android:inputType`을 넣는다. 폭은 `240dp`로 시작한다.
- 막히면 [1일차 완성 XML](examples/day1/activity_main.xml)을 열어 내 코드와 한 줄씩 비교한다.

### 3. [연결] 버튼: 빈 값 검사

`onCreate()` 마지막 `}` 바로 위에 [연결] 버튼 코드를 넣는다.

- 입력칸의 글자는 `binding.deviceNameEdit.text.toString()`으로 꺼낸다.
- 비었으면(`isEmpty()`) Toast `장치 이름을 입력하세요`, 아니면 Toast `연결: 이름`.

| 입력 | 예상 Toast | 실제 Toast |
|---|---|---|
| 빈 채로 [연결] |  |  |
| `ESP32_BLE_1` 입력 후 [연결] |  |  |

### 4. 자동 연결 Switch 직접 완성하기

`binding.autoSwitch.setOnCheckedChangeListener { _, isChecked -> }` 안을 채운다.

- 켜면 Toast `자동 연결 켜짐`. 슬라이드에 있는 코드다.
- 끌 때 Toast `자동 연결 꺼짐`은 **직접** 완성한다. `if (isChecked)`에 `else`를 붙이면 된다.

### 5. 오늘 확인할 것

- [ ] `SmartIO` 프로젝트가 실행되고 `MainActivity.kt`에 `findViewById`가 없다.
- [ ] 화면의 글자가 `strings.xml`에서 온다(XML에 한글을 직접 쓴 곳이 없다).
- [ ] [연결]이 빈 값과 입력된 값을 구분해 Toast를 띄운다.
- [ ] Switch를 켜고 끌 때 Toast가 다르게 나온다.
- [ ] 장치 이름을 입력한 화면을 캡처했다.

프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 제어 화면과 명령 로그 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 `SmartIO`를 열어 실행하고 **New › Activity › Empty Views Activity**로 `ControlActivity`를 만든다 |
| 10–20분 | Manifest의 `<activity>` 줄을 확인하고 [연결]에서 `Intent`로 이동·이름 전달을 만든다 |
| 20–35분 | `strings.xml`에 다섯 줄을 추가하고 제어 화면(`장치: ?`·핀 `EditText`·LED `Switch`·로그·[뒤로])을 배치한다 |
| 35–50분 | `ControlActivity`에서 이름을 받아 표시하고, Switch로 `on`·`off` 로그를 쌓고, [뒤로]를 만든다 |
| 50–60분 | 두 화면을 오가며 확인하고 캡처 2장과 파일을 제출한다 |

### 1. ControlActivity 만들기와 이동

1. `com.example.smartio` 폴더를 오른쪽 클릭 → **New › Activity › Empty Views Activity**, Activity Name `ControlActivity`, Launcher Activity는 체크하지 않는다.
2. `AndroidManifest.xml`에 `<activity android:name=".ControlActivity" android:exported="false" />`가 생겼는지 확인한다.
3. `MainActivity.kt`의 [연결] 코드에서 `연결: 이름` Toast 자리를 아래로 바꾼다.

```kotlin
val intent = Intent(this, ControlActivity::class.java)
intent.putExtra("name", name)
startActivity(intent)
```

이름을 넣고 [연결]을 누르면 새 화면이 열리고, 뒤로 가기(◀)로 돌아오면 성공이다. 빈 값 Toast는 그대로 남긴다.

### 2. 제어 화면 배치하기

`strings.xml`에 `device_unknown`(장치: ?)·`pin_hint`·`led`·`log_title`·`back`을 추가하고 `activity_control.xml`을 아래 결과가 되게 배치한다.

```text
장치: ?                  ← TextView, id deviceText
[ 핀 번호 ]              ← EditText, id pinEdit, inputType number
LED (O)                  ← Switch, id ledSwitch
명령 로그
(비어 있음)              ← TextView, id logText
        [ 뒤로 ]         ← Button, id backButton
```

- 루트는 `LinearLayout`(`vertical`, `gravity="center_horizontal"`, `@+id/main`)이다.
- 로그 TextView는 `layout_height="0dp"`·`layout_weight="1"`로 남는 공간을 다 쓰게 한다. 그러면 [뒤로]가 맨 아래에 붙는다.
- 막히면 [2일차 완성 XML](examples/day2/activity_control.xml)과 비교한다.

### 3. 이름 받아 표시하기

`ControlActivity.kt`를 ViewBinding 틀(`ActivityControlBinding`)로 바꾸고 `onCreate()` 마지막 `}` 위에 넣는다.

```kotlin
val name = intent.getStringExtra("name") ?: ""
binding.deviceText.text = "장치: $name"
```

연결 화면에서 `ESP32_BLE_1`을 넣고 [연결]을 누르면 위에 `장치: ESP32_BLE_1`이 보여야 한다.

### 4. LED Switch로 로그 쌓기 — 직접 완성하기

`binding.ledSwitch.setOnCheckedChangeListener { _, isChecked -> }` 안을 채운다. 1일차 Switch 코드와 [연결]의 빈 값 검사를 합치면 된다.

- 핀 번호는 `binding.pinEdit.text.toString()`으로 꺼낸다.
- 비었으면 Toast `핀 번호를 입력하세요`.
- 켜면 `binding.logText.append("on $pin\n")`, 끄면 `off`. `.text =`가 아니라 `append`다.
- 세 갈래는 `if (…) { } else if (…) { } else { }`로 쓰거나, `else { if … else … }`로 중첩해도 된다.
- [뒤로] 버튼은 `finish()` 한 줄이다.

| 누른 순서 | 예상 로그 | 실제 로그 |
|---|---|---|
| 핀 비운 채 스위치 켜기 |  |  |
| 스위치 끄기 → 핀 `3` 입력 → 스위치 켜기 |  |  |
| 이어서 스위치 끄기 |  |  |
| 이어서 스위치 켜기 |  |  |
| [뒤로] → 다시 [연결] |  |  |

### 5. 제출 전 확인

- [ ] 연결 화면 → 제어 화면 → [뒤로] → 연결 화면이 오간다.
- [ ] 제어 화면 상단에 입력한 이름이 보인다.
- [ ] 로그에 `on 3`·`off 3`이 위에서 아래로 쌓인다.
- [ ] 핀이 비면 Toast가 뜬다.

## 막혔을 때

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'databinding'` 또는 `Unresolved reference 'ActivityMainBinding'` 오류 | `build.gradle.kts (Module :app)`에 `buildFeatures { viewBinding = true }`가 있는지, **Sync Now**를 눌렀는지 본다 |
| `Unresolved reference 'deviceNameEdt'`처럼 `binding.` 뒤가 빨갛다 | XML의 `@+id/deviceNameEdit`와 코드의 `binding.deviceNameEdit` 철자를 대조한다 |
| `error: resource string/connect_btn (aka com.example.smartio:string/connect_btn) not found.` | XML의 `@string/이름`이 `strings.xml`에 있는지 본다 |
| `Unresolved reference 'Toast'` / `Unresolved reference 'Intent'` | **Alt+Enter**(맥 ⌥+Enter)로 import한다 |
| `Operator '==' cannot be applied to 'android.text.Editable!' and 'kotlin.String'.` | `binding.deviceNameEdit.text` 뒤에 `.toString()`을 붙이고 `isEmpty()`로 검사한다 |
| `Argument type mismatch: actual type is 'kotlin.Function1<...>', but 'kotlin.Function2<...>' was expected.` | Switch의 `{ isChecked -> }`에 이름이 하나뿐이다. `{ _, isChecked -> }`로 쓴다 |
| `Classifier 'class ControlActivity : AppCompatActivity' does not have a companion object, so it cannot be used as an expression.` | `Intent(this, ControlActivity)`에 `::class.java`가 빠졌다 |
| 빌드는 되는데 앱을 켜자마자 꺼진다. Logcat에 `lateinit property binding has not been initialized` | `setContentView(binding.root)`가 `binding = ActivityMainBinding.inflate(layoutInflater)`보다 **위**에 있다. 순서를 바꾼다 |
| 버튼을 눌러도, 스위치를 켜도 아무 일도 없다 | `setContentView(R.layout.activity_main)`이 남아 있다. `setContentView(binding.root)`로 바꾼다 |
| [연결]을 누르면 앱이 꺼진다. Logcat에 `ActivityNotFoundException: Unable to find explicit activity class ... have you declared this activity in your AndroidManifest.xml` | Manifest에 `<activity android:name=".ControlActivity" ... />` 줄을 넣는다 |
| 제어 화면에 `장치: `만 보이거나 `장치: null`이 보인다 | `putExtra("name", …)`과 `getStringExtra("name")`의 `"name"` 철자가 같은지, `?: ""`를 붙였는지 본다 |
| 로그가 쌓이지 않고 마지막 한 줄만 보인다 | `binding.logText.text = …`를 썼다. `append`로 바꾼다 |
| 스위치를 켜자마자 앱이 꺼진다. Logcat에 `NumberFormatException: For input string: ""` | 빈 글자에 `.toInt()`를 썼다. `isEmpty()` 검사를 먼저 한다 |
| 노란색 경고 표시가 있다 | 실행에는 문제가 없다. 빨간 오류부터 해결한다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 네 가지

1. **`MainActivity.kt`**: ViewBinding으로 [연결]·Switch가 동작하고 `ControlActivity`로 이동하는 코드
2. **`ControlActivity.kt`**: 이름 표시·LED 로그·[뒤로]가 동작하는 코드
3. **캡처 1**: 연결 화면에 장치 이름을 입력한 화면
4. **캡처 2**: 제어 화면 상단에 그 이름이 보이고 로그에 `on 3`·`off 3`이 쌓인 화면

[연결]로 제어 화면이 열리고 이름이 보이면 기본 성공이다. 로그와 [뒤로]는 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 1일차: Switch가 켜져 있을 때만 [연결]이 `연결: 이름 (자동)`을 띄우게 해 본다. `binding.autoSwitch.isChecked`로 스위치 상태를 읽을 수 있다.
- 2일차: 핀 번호가 `0`~`3`이 아니면 Toast `허용되지 않는 번호`를 띄우고 로그에 쌓지 않는다. `pin.toInt()`는 빈 값 검사 **뒤**에 쓴다.
- 2일차: 연결 화면의 자동 연결 값도 `putExtra("auto", binding.autoSwitch.isChecked)`로 넘겨 제어 화면 상단에 `(자동)`을 붙여 본다. 받는 쪽은 `intent.getBooleanExtra("auto", false)`다.

추가 과제는 선택 사항이다.
