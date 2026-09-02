---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 1주차
footer: Kotlin + XML Views · Smart I/O Controller
---

# Android 실행 구조와 Kotlin 진단

## 이번 주 질문

앱의 시작점, 화면, 로그를 하나의 실행 흐름으로 설명할 수 있는가?

---

# 1일차 — 앱이 실행되기까지

`30분 설명·시연 → 60분 실습`

---

## 1일차 · 0–4분 — 결과에서 출발

실행 증거는 세 층으로 남긴다.

| 층 | 질문 | 증거 |
|---|---|---|
| 대상 | 어디서 실행했나? | 기기/에뮬레이터 이름 |
| UI | 무엇이 보이나? | 화면과 상태 문구 |
| 런타임 | 어떤 코드가 지났나? | Logcat 태그 |

> “화면이 떴다”만으로는 어느 코드가 실행됐는지 알 수 없다.

---

## 1일차 · 4–9분 — 프로젝트 지도

```text
app/
├─ src/main/AndroidManifest.xml   앱·컴포넌트 선언
├─ src/main/java/.../MainActivity.kt
├─ src/main/res/layout/activity_main.xml
└─ src/main/res/values/strings.xml
```

`Kotlin 코드 → resource ID → XML View` 연결을 따라간다.

---

## 1일차 · 9–15분 — 시작 흐름

```text
Launcher 아이콘
      │ Intent
      ▼
AndroidManifest의 launcher Activity
      │ onCreate()
      ▼
setContentView(...) ──▶ XML inflate ──▶ View tree
```

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
}
```

---

## 1일차 · 15–21분 — 실행 대상과 실패 층

| 증상 | 먼저 확인할 곳 |
|---|---|
| Run 대상이 없음 | Device Manager / USB 연결 |
| 빌드 실패 | Build Output의 첫 원인 |
| 설치 실패 | 선택 기기와 저장 공간 |
| 실행 중 종료 | Logcat의 예외와 `Caused by` |
| 화면 내용이 다름 | 설치된 앱·Activity·layout |

여러 줄을 한꺼번에 고치기 전에 실패 층을 좁힌다.

---

## 1일차 · 21–27분 — Logcat은 실행 증거

```kotlin
private const val TAG = "DeviceInfo"

Log.d(TAG, "onCreate: screen ready")
```

필터 기준:

- 실행 중인 앱 프로세스
- 자신의 고유한 `TAG`
- 오류 수준만 보지 말고 최초 예외 원인 확인

개인정보나 토큰을 로그에 남기지 않는다.

---

## 1일차 · 27–30분 — 실습 이양

실습 순서:

1. 실행 전 결과를 예측한다.
2. 정상 실행의 대상·화면·로그를 기록한다.
3. 안전한 오류 하나를 재현한다.
4. 첫 원인 줄로 수정 범위를 좁힌다.

**1일차 설명 합계: 4+5+6+6+6+3 = 30분**

---

# 2일차 — Kotlin으로 화면 상태 만들기

`30분 설명·시연 → 60분 실습`

---

## 2일차 · 0–5분 — 값과 변경 가능성

```kotlin
val model: String = Build.MODEL       // 다시 대입하지 않음
var refreshCount: Int = 0             // 상태 변화 의도

fun label(name: String, value: String) = "$name: $value"
```

기본값은 `val`. 변경이 요구될 때만 `var`를 선택한다.

---

## 2일차 · 5–10분 — 데이터 구조와 문자열 가공

```kotlin
data class DeviceSummary(
    val manufacturer: String,
    val model: String,
    val apiLevel: Int,
)

val summaryText = getString(
    R.string.device_summary_format,
    summary.manufacturer,
    summary.model,
    summary.apiLevel,
)
```

원본 데이터와 지역화 가능한 화면 형식을 구분한다.

---

## 2일차 · 10–16분 — nullable은 가능한 상태

```kotlin
fun normalizeBuildValue(raw: String?, unknownSentinel: String): String? =
    raw?.trim()?.takeIf {
        it.isNotEmpty() && !it.equals(unknownSentinel, ignoreCase = true)
    }
```

| 입력 | 결과 |
|---|---|
| `" Pixel "` | `Pixel` |
| `"   "` | `null` |
| `null` | `null` |
| `"unknown"` | `null` |

`!!`는 불확실성을 없애지 않고 예외로 미룬다.

---

## 2일차 · 16–22분 — XML View와 Kotlin 연결

```xml
<TextView
    android:id="@+id/deviceSummary"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:text="@string/device_unknown" />
```

```kotlin
findViewById<TextView>(R.id.deviceSummary).text = getString(
    R.string.device_summary_format,
    summary.manufacturer,
    summary.model,
    summary.apiLevel,
)
```

대체 문구와 표시 format은 `strings.xml`에 둔다.

---

## 2일차 · 22–27분 — 입력 → 가공 → 표시

```text
Build 값 / 테스트 입력
          │
          ▼
 normalizeBuildValue(), DeviceSummary
          │
          ▼
       TextView.text
```

테스트는 단말의 “정상값”만 보지 않는다.

- 정상: 실제 제조사·모델
- 경계: 공백 문자열
- 실패 가능: nullable 입력

---

## 2일차 · 27–30분 — 실습 이양

완료 조건:

- `Device Info`가 실행된다.
- 새로고침 횟수가 화면과 로그에 일치한다.
- `null`·공백·`Build.UNKNOWN`이 resource의 `알 수 없음`으로 표시된다.
- `!!` 없이 처리 이유를 설명한다.

**2일차 설명 합계: 5+5+6+6+5+3 = 30분**

---

## Compose와의 비교 — 이번 주 평가 범위 아님

Compose는 Kotlin 함수로 UI를 선언한다. 이 수업은 Android의 View tree, XML resource, Activity 연결을 명시적으로 관찰하기 위해 **Kotlin + XML Views**를 기준으로 한다. Compose 문법은 구현·평가하지 않는다.

---

## 다음 주

하나의 정보 문구를 여러 View, style, dimension, 문자열 리소스로 분리하고 화면 크기·회전·접근성에 대응한다.
