# 1주차 따라하기 — 실행 구조 확인과 Device Info

이 문서는 1주차 시연·실습을 **순서대로 그대로 재현**하기 위한 절차서다.
강의자는 30분 시연을 이 순서로 진행하고, 학생은 실습·복습 때 같은 순서로 따라 한다.
각 단계는 `할 일 → 예상 결과 → 확인` 순서로 되어 있다. 예상 결과가 다르면 다음 단계로 넘어가지 않는다.

## 시작 전 준비

- 강의자가 제공한 **Kotlin + XML Views 기준 프로젝트**를 사용한다. (새로 만들 경우 `Empty Views Activity` 템플릿)
- Android Studio·SDK 버전은 수업 공지의 검증본을 따른다. 임의 업데이트하지 않는다.
- 에뮬레이터 1대가 부팅되어 있거나 실기기 1대가 연결되어 있다.
- 아래 코드의 `package` 줄은 자신의 프로젝트 package 이름으로 바꾼다.

---

## 1일차 — 앱 실행 경로를 증거로 만들기

### 단계 1. 프로젝트 열기와 실행 대상 선택

**할 일**

1. Android Studio에서 기준 프로젝트를 연다. 하단 상태 표시줄의 인덱싱(Indexing)이 끝날 때까지 기다린다.
2. 상단 툴바의 기기 선택 목록에서 사용할 에뮬레이터 또는 실기기를 선택한다.
3. 선택한 대상의 이름을 관찰 노트 첫 줄에 적는다. (예: `Pixel 8 API 34` 또는 실기기 모델명)

**예상 결과** — 툴바에 `app` 구성과 기기 이름이 함께 보인다.

**확인** — [ ] 실행 대상 이름을 기록했다.

### 단계 2. 첫 실행으로 기준선 만들기

**할 일**

1. `Run ▶` 버튼(또는 `Ctrl+R` / `Shift+F10`)을 누른다.
2. 첫 빌드가 끝나고 앱 화면이 뜰 때까지 기다린다.
3. 화면에 보이는 문구를 그대로 적는다.

**예상 결과** — 선택한 기기에서 앱이 실행되고 기준 프로젝트의 초기 화면이 보인다.

**확인** — [ ] 대상 이름 + 화면 문구, 두 가지 증거가 생겼다.

### 단계 3. 프로젝트 지도 — 네 파일의 역할 잇기

**할 일**

1. Project 창 상단의 보기 선택을 `Android` ↔ `Project`로 번갈아 바꿔 본다. 논리 구조와 실제 디스크 경로가 다르게 보이는 것을 확인한다.
2. 다음 네 파일을 차례로 연다.

```text
app/src/main/AndroidManifest.xml        앱·컴포넌트 선언
app/src/main/java/<package>/MainActivity.kt   화면 동작
app/src/main/res/layout/activity_main.xml     View 구조
app/src/main/res/values/strings.xml           표시 문자열
```

3. `MainActivity.kt`의 `R.layout.activity_main`에서 `Ctrl(⌘)+클릭` → layout XML로 이동한다.
4. `AndroidManifest.xml`에서 launcher 선언을 찾는다.

```xml
<intent-filter>
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```

**예상 결과** — 아이콘 클릭 → Manifest의 launcher Activity → `onCreate()` → `setContentView()`가 XML을 inflate, 이 순서를 네 파일로 설명할 수 있다.

**확인** — [ ] `AndroidManifest.xml → MainActivity.kt → activity_main.xml → strings.xml` 역할 지도를 적었다.

### 단계 4. `onCreate()`에 시작 로그 추가

**할 일** — `MainActivity.kt`를 아래처럼 수정하고 다시 실행한다.

```kotlin
import android.util.Log   // import 목록에 추가 (IDE 자동 import 가능)

private const val TAG = "DeviceInfo"

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        Log.d(TAG, "onCreate: screen ready")
    }
}
```

**예상 결과** — 앱 화면은 그대로, Logcat에 새 로그 한 줄이 남는다.

**확인** — [ ] 화면 증거와 로그 증거가 서로 다른 창에서 확인된다.

### 단계 5. Logcat 필터로 좁히기

**할 일**

1. 하단 `Logcat` 창을 연다.
2. 필터 입력란에 다음을 입력한다.

```text
package:mine tag:DeviceInfo
```

3. 앱을 다시 실행하고 `onCreate: screen ready`가 정확히 1번 나타나는지 센다.

**예상 결과** — 다른 앱의 로그가 사라지고 자신의 태그 로그만 보인다. 실행 1회당 로그 1줄.

**확인** — [ ] 태그(`DeviceInfo`)와 메시지를 구분해 기록했다. 개인정보·토큰은 로그에 없다.

### 단계 6. 실패 하나만 재현하고 복구하기

**할 일**

1. 실행 전에 예측을 적는다: “존재하지 않는 layout 이름을 참조하면 어느 단계에서 실패할까?”
2. `setContentView(R.layout.activity_main)`을 존재하지 않는 이름으로 바꾼다.

```kotlin
setContentView(R.layout.activity_main_x)   // 잠시 틀리게 바꾼다
```

3. `Run`을 누르고 Build Output에서 **첫 관련 오류**의 파일·줄 번호·핵심 문구를 기록한다.

**예상 결과** — 앱이 설치·실행되기 전에 **빌드(컴파일) 단계**에서 멈춘다. 오류는 `Unresolved reference` 계열이며 `MainActivity.kt`의 해당 줄을 가리킨다. 에뮬레이터 재부팅은 이 오류와 무관하다.

4. 바꾼 한 곳만 원래대로 되돌리고 다시 실행한다.

```kotlin
setContentView(R.layout.activity_main)     // 원복
```

**확인** — [ ] 기존 화면과 로그가 기준선대로 돌아왔다. 수정 위치는 정확히 한 곳이었다.

### 단계 7. 회전 관찰 (경계)

**할 일** — 앱이 실행된 상태에서 화면을 한 번 회전시키고(에뮬레이터 회전 버튼), Logcat의 `onCreate` 로그 수를 다시 센다.

**예상 결과** — 기본 설정에서는 Activity가 다시 만들어져 `onCreate: screen ready`가 1줄 **추가**된다. 이유와 대응은 3주차에서 다룬다.

**확인** — [ ] 회전 전후의 로그 횟수를 기록했다. `lab.md`의 1일차 제출 증거를 정리한다.

---

## 2일차 — Device Info 화면 만들기

네 개 파일을 순서대로 작성한다. **각 단계가 끝날 때마다 빌드해** 오류를 그 자리에서 잡는다.

### 단계 1. `strings.xml` — 표시 문자열 먼저

**할 일** — `app/src/main/res/values/strings.xml`을 다음 내용으로 만든다. (`app_name`은 기존 값 유지 가능)

```xml
<resources>
    <string name="app_name">Smart I/O Controller</string>
    <string name="device_unknown">장치 정보를 불러오는 중</string>
    <string name="value_unknown">알 수 없음</string>
    <string name="device_summary_format">%1$s %2$s · API %3$d</string>
    <string name="refresh">새로고침</string>
    <string name="refresh_count_initial">새로고침 0회</string>
    <string name="refresh_count">새로고침 %1$d회</string>
</resources>
```

**예상 결과** — 빌드 성공. 대체 문구와 표시 format이 코드가 아닌 resource에 모였다.

### 단계 2. `DeviceSummary.kt` — 데이터와 정규화 함수

**할 일** — `MainActivity.kt`와 같은 package에 새 Kotlin 파일 `DeviceSummary.kt`를 만든다.

```kotlin
package com.example.smartio   // 자신의 package로 변경

data class DeviceSummary(
    val manufacturer: String,
    val model: String,
    val apiLevel: Int,
)

fun normalizeBuildValue(raw: String?, unknownSentinel: String): String? =
    raw?.trim()?.takeIf {
        it.isNotEmpty() && !it.equals(unknownSentinel, ignoreCase = true)
    }
```

**예상 결과** — 빌드 성공. 이 파일에는 Android import가 하나도 없다(순수 Kotlin).

**확인** — [ ] 데이터 클래스의 프로퍼티가 모두 `val`이다.

### 단계 3. `activity_main.xml` — 세 개의 View

**할 일** — `app/src/main/res/layout/activity_main.xml`을 다음으로 교체한다.
(기준 프로젝트의 부모가 `ConstraintLayout`이면 부모는 그대로 두고 세 View만 추가해도 된다. 그 경우 각 View에 constraint 연결이 필요하다.)

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/deviceSummary"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="@string/device_unknown"
        android:textSize="18sp" />

    <TextView
        android:id="@+id/refreshCount"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/refresh_count_initial" />

    <Button
        android:id="@+id/refreshButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="@string/refresh" />

</LinearLayout>
```

**예상 결과** — 미리보기(Design/Split)에 문자열 resource의 기본 문구가 보인다. 하드코딩된 한글 문구는 XML에 없다.

### 단계 4. `MainActivity.kt` — 연결과 상태

**할 일** — `MainActivity.kt`를 다음으로 교체한다.

```kotlin
package com.example.smartio   // 자신의 package로 변경

import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

private const val TAG = "DeviceInfo"

class MainActivity : AppCompatActivity() {
    private var refreshCount = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val summaryView = findViewById<TextView>(R.id.deviceSummary)
        val countView = findViewById<TextView>(R.id.refreshCount)
        val refreshButton = findViewById<Button>(R.id.refreshButton)

        val unknownText = getString(R.string.value_unknown)
        val summary = DeviceSummary(
            manufacturer = normalizeBuildValue(Build.MANUFACTURER, Build.UNKNOWN)
                ?: unknownText,
            model = normalizeBuildValue(Build.MODEL, Build.UNKNOWN)
                ?: unknownText,
            apiLevel = Build.VERSION.SDK_INT,
        )
        summaryView.text = getString(
            R.string.device_summary_format,
            summary.manufacturer,
            summary.model,
            summary.apiLevel,
        )

        refreshButton.setOnClickListener {
            refreshCount += 1
            countView.text = getString(R.string.refresh_count, refreshCount)
            Log.d(TAG, "refreshCount=$refreshCount")
        }
        Log.d(TAG, "onCreate: screen ready")
    }
}
```

**예상 결과** — 실행하면 첫 화면에 `제조사 모델 · API 수준` 요약과 `새로고침 0회`가 보인다.

**확인** — [ ] `!!`가 코드에 없다. `refreshCount`만 `var`이고 나머지는 `val`이다.

### 단계 5. 클릭 3회 검증

**할 일** — 버튼을 세 번 누르면서 화면 문구와 Logcat(`package:mine tag:DeviceInfo`)을 비교한다.

**예상 결과**

| 클릭 | 화면 | Logcat 마지막 줄 |
|---:|---|---|
| 0회 | 새로고침 0회 | `onCreate: screen ready` |
| 1회 | 새로고침 1회 | `refreshCount=1` |
| 3회 | 새로고침 3회 | `refreshCount=3` |

**확인** — [ ] 화면 횟수와 로그 횟수가 항상 같다.

### 단계 6. 정상·경계·실패 입력 시험

**할 일** — `onCreate()` 끝에 임시 테스트 코드를 추가하고 실행 후 결과를 관찰한 뒤 **삭제**한다.

```kotlin
val samples = listOf(" Pixel ", "   ", null, "unknown")
samples.forEach { raw ->
    Log.d(TAG, "normalized=" + normalizeBuildValue(raw, Build.UNKNOWN))
}
```

**예상 결과** — Logcat에 차례로 `Pixel`, `null`, `null`, `null`. 개인 단말의 고유 식별 정보는 출력하지 않는다.

**확인** — [ ] `lab.md`의 예상/실제 표를 채웠고 예상과 다른 칸에 이유를 적었다.

### 단계 7. 회전 관찰과 제출 정리

**할 일** — 클릭 3회 상태에서 화면을 회전시키고 횟수 문구를 확인한다.

**예상 결과** — 기본 설정에서는 Activity 재생성으로 `새로고침 0회`로 돌아간다. 이번 주에는 **관찰만** 기록하고 고치지 않는다(3주차 주제).

**확인** — [ ] `lab.md`의 2일차 제출 증거 4종을 정리했다.

---

## 문제가 생겼을 때

| 증상 | 이 문서에서 돌아갈 단계 |
|---|---|
| Run 대상이 없다 | 1일차 단계 1 |
| 빌드 오류 | 1일차 단계 6의 진단 순서 (첫 오류의 파일·줄부터) |
| 로그가 안 보인다 | 1일차 단계 5의 필터 |
| 화면 문구가 예상과 다르다 | 2일차 단계 1·3의 resource 이름 대조 |
| 클릭 횟수와 로그가 다르다 | 2일차 단계 4의 리스너 내부 확인 |

세부 판정 기준과 힌트는 [`lab.md`](lab.md)에 있다. 정답과 해설은 실습이 끝난 뒤 강의자가 별도로 안내한다.
