# 2주차 예제 스니펫 — 적응형 mock 제어판

## 사용 범위

이 폴더는 수업용 대표 스니펫 문서이며 **빌드 가능한 Gradle 프로젝트를 제공하지 않는다**. 강의자 기준 프로젝트의 dependency, package, theme, 부모 layout을 유지한 채 필요한 부분을 옮긴다.

## 파일명과 문맥

| 파일명 예시 | 위치/역할 |
|---|---|
| `activity_main.xml` | `res/layout/`, 제어판 View 관계 |
| `strings.xml` | `res/values/`, 상태·동작 문구 |
| `dimens.xml` | `res/values/`, 공통 간격 |
| `values-land/dimens.xml` | 가로 방향에서 달라지는 간격만 제공 |
| `MainActivity.kt` | mock 상태 변경과 단일 `render()` |

## `activity_main.xml` 핵심

아래 조각은 `ConstraintLayout` 내부에 들어간다. namespace와 나머지 constraint는 기준 프로젝트 문맥에 맞춘다.

```xml
<TextView
    android:id="@+id/deviceName"
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    android:text="@string/mock_device_name"
    android:textSize="20sp"
    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintEnd_toEndOf="parent"
    app:layout_constraintTop_toTopOf="parent" />

<TextView
    android:id="@+id/connectionStatus"
    android:layout_width="0dp"
    android:layout_height="wrap_content"
    android:text="@string/status_disconnected"
    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintEnd_toEndOf="parent"
    app:layout_constraintTop_toBottomOf="@id/deviceName" />

<Button
    android:id="@+id/connectButton"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@string/connect" />

<Button
    android:id="@+id/outputButton"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:enabled="false"
    android:text="@string/output_on" />
```

## `strings.xml` 핵심

```xml
<resources>
    <string name="mock_device_name">DEMO Smart I/O Mock Device</string>
    <string name="status_disconnected">연결 안 됨 · 연결 후 출력 제어 가능</string>
    <string name="status_ready">제어 준비</string>
    <string name="connect">연결</string>
    <string name="disconnect">연결 해제</string>
    <string name="output_on">출력 켜기</string>
</resources>
```

## `MainActivity.kt` 핵심

```kotlin
enum class MockConnection { DISCONNECTED, READY }

private var connection = MockConnection.DISCONNECTED

private fun render(state: MockConnection) {
    val ready = state == MockConnection.READY
    connectionStatus.setText(
        if (ready) R.string.status_ready else R.string.status_disconnected
    )
    connectButton.setText(if (ready) R.string.disconnect else R.string.connect)
    outputButton.isEnabled = ready
}

private fun bindEvents() {
    connectButton.setOnClickListener {
        connection = if (connection == MockConnection.READY) {
            MockConnection.DISCONNECTED
        } else {
            MockConnection.READY
        }
        render(connection)
    }
}
```

`connectionStatus`, `connectButton`, `outputButton`은 `onCreate()`에서 찾은 View 참조라는 문맥이다. field 선언 방식은 기준 프로젝트를 따른다.

## 예상 관찰

1. 최초에는 `연결 안 됨`이고 출력 버튼은 비활성이다.
2. 연결 버튼을 누르면 상태 문구, 연결 버튼 label, 출력 버튼 활성 여부가 함께 바뀐다.
3. 긴 장치명과 큰 글꼴에서는 고정 폭·높이의 문제가 먼저 드러난다.
4. 회전 뒤 mock 상태가 초기화될 수 있다. 이번 주에는 관찰하고 3주차 상태 보존에서 해결한다.

## 경계 입력

```kotlin
val longMockName =
    "DEMO-LAB-SMART-IO-CONTROLLER-DEVICE-WITH-A-LONG-NAME"
deviceName.text = longMockName
```

실제 BLE 이름을 읽는 코드가 아니다. 개인 장치 식별값도 사용하지 않는다.

## 공식 참고 자료

- [ConstraintLayout — Android Developers](https://developer.android.com/develop/ui/views/layout/constraint-layout)
- [Alternative resources — Android Developers](https://developer.android.com/guide/topics/resources/providing-resources#AlternativeResources)
- [Accessibility principles — Android Developers](https://developer.android.com/guide/topics/ui/accessibility/principles)
