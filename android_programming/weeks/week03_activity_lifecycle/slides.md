---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 3주차
footer: Activity lifecycle · saved state · result API
---

# Activity 생명주기와 상태 보존

> 화면 객체의 수명과 사용자 상태의 수명은 같지 않다.

---

# 1일차 — callback을 로그로 관찰하기

`30분 설명·시연 → 60분 실습`

---

## 1일차 · 0–4분 — 회전 뒤 무엇이 달라졌나

```text
회전 전 Activity(instance=A, taps=3)
             │ configuration change
             ▼
회전 후 Activity(instance=B, taps=? )
```

같은 화면처럼 보여도 View와 Activity 객체가 새로 만들어질 수 있다.

---

## 1일차 · 4–10분 — 여섯 핵심 callback

```text
onCreate → onStart → onResume
                         │ 화면을 떠남
                         ▼
             onPause → onStop → onDestroy?
```

| 구간 | 중심 질문 |
|---|---|
| Created | 초기 구성은 했는가? |
| Started | 화면이 보이는가? |
| Resumed | 사용자와 상호작용하는가? |

`onDestroy()`는 모든 종료 경로에서 보장되지 않는다.

---

## 1일차 · 10–16분 — 관찰 가능한 로그

```kotlin
private val instanceId = System.identityHashCode(this)

private fun log(event: String) {
    Log.d("LifecycleTrace", "id=$instanceId event=$event")
}

override fun onStart() {
    super.onStart()
    log("onStart")
}
```

callback마다 `super` 호출과 같은 형식의 로그를 둔다.

---

## 1일차 · 16–21분 — 행동별로 달라지는 경로

| 사용자 행동 | 관찰 초점 |
|---|---|
| 최초 실행 | create→start→resume |
| Home | pause/stop, 복귀 경로 |
| 다른 Activity | 가림 정도와 callback |
| 회전 | 이전 id 종료와 새 id 생성 |
| Back | finish 경로 |

정확한 순서를 추측하지 말고 현재 환경에서 로그로 기록한다.

---

## 1일차 · 21–27분 — 상태 책임 선택

```kotlin
override fun onSaveInstanceState(outState: Bundle) {
    outState.putInt(KEY_TAPS, tapCount)
    super.onSaveInstanceState(outState)
}

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    tapCount = savedInstanceState?.getInt(KEY_TAPS) ?: 0
}
```

| 상태 | 대표 선택 |
|---|---|
| 작은 복원 UI 값 | saved instance state |
| configuration change 동안 화면 상태 | ViewModel |
| 앱 재시작 뒤에도 필요한 데이터 | 영구 저장소 |

---

## 1일차 · 27–30분 — 실습 이양

1. 상태 소실을 먼저 재현한다.
2. callback과 instance id를 기록한다.
3. 작은 값 하나만 저장·복원한다.
4. 같은 회전 조건으로 재검증한다.

**1일차 설명 합계: 4+6+6+5+6+3 = 30분**

---

# 2일차 — Activity 사이의 명시적 계약

`30분 설명·시연 → 60분 실습`

---

## 2일차 · 0–5분 — Intent가 전달하는 것

```text
MainActivity
   │ explicit Intent + device name
   ▼
DeviceDetailActivity
   │ result: alias / canceled
   ▼
MainActivity.render()
```

Activity 객체 자체나 View 참조를 전달하지 않는다.

---

## 2일차 · 5–10분 — 명시적 Intent

```kotlin
val intent = Intent(this, DeviceDetailActivity::class.java)
    .putExtra(EXTRA_DEVICE_NAME, mockDeviceName)
editDevice.launch(intent)
```

대상 Activity는 Manifest에 선언되어야 한다. 내부 화면은 명시적 Intent로 대상을 고정한다.

---

## 2일차 · 10–16분 — extra는 입력 계약

```kotlin
val deviceName = intent.getStringExtra(EXTRA_DEVICE_NAME)
    ?.trim()
    ?.takeIf(String::isNotEmpty)

if (deviceName == null) {
    setResult(Activity.RESULT_CANCELED)
    finish()
    return
}
```

정상값뿐 아니라 누락·공백 입력 정책을 정한다.

---

## 2일차 · 16–22분 — Activity Result API

```kotlin
private val editDevice = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode == Activity.RESULT_OK) {
        result.data?.getStringExtra(EXTRA_ALIAS)
            ?.trim()
            ?.takeIf(String::isNotEmpty)
            ?.let { validAlias ->
                alias = validAlias
                render()
            }
    }
}
```

deprecated `startActivityForResult()`/`onActivityResult()`를 사용하지 않는다.

---

## 2일차 · 22–27분 — 저장과 취소는 다른 결과

| 상세 화면 행동 | resultCode | Main 변화 |
|---|---|---|
| 유효 별칭 저장 | `RESULT_OK` | alias 갱신 |
| 빈 별칭 저장 | 화면 오류 | 화면 유지 |
| 취소/Back | `RESULT_CANCELED` | 기존 alias 유지 |
| extra 누락 | canceled 후 종료 | 안전한 기존 상태 |

---

## 2일차 · 27–30분 — 실습 이양

검증 순서:

1. 정상 별칭 저장
2. 공백 입력 거절
3. 취소 시 기존값 유지
4. extra 누락 시 종료하지 않는 앱

**2일차 설명 합계: 5+5+6+6+5+3 = 30분**

---

## Back stack에서 묻는 질문

- 새 화면을 연 것인가, 기존 화면을 새로 만든 것인가?
- Back은 어느 Activity로 돌아가는가?
- 돌아온 화면의 상태는 메모리, saved state, 저장소 중 어디에 있었는가?

---

## 다음 주

Activity 안의 목록·상세 책임을 Fragment와 Navigation으로 나누고, View lifecycle에 맞춰 View 참조를 정리한다.
