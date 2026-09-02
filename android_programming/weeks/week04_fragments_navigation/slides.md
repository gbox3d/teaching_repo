---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 4주차
footer: Fragment · Navigation · RecyclerView
---

# Fragment, Navigation, RecyclerView

> 화면 책임과 View 수명을 함께 나눈다.

---

# 1일차 — Fragment 경계와 Navigation

`30분 설명·시연 → 60분 실습`

---

## 1일차 · 0–4분 — Activity 하나의 과부하

```text
MainActivity
├─ 장치 목록 XML/이벤트
├─ 선택 상태
├─ 제어 입력 XML/이벤트
└─ Back 처리
```

화면 책임을 분리하되 상태와 View 참조의 수명을 명확히 한다.

---

## 1일차 · 4–10분 — 두 개의 수명

```text
Fragment: onCreate ───────────────────── onDestroy
View:             onCreateView ─ onDestroyView
```

Fragment가 back stack에 남아도 View는 파괴될 수 있다.

- View 접근: `onViewCreated()` 이후
- 관찰 owner: `viewLifecycleOwner`
- View 참조 정리: `onDestroyView()`까지

---

## 1일차 · 10–16분 — NavHost와 graph

```text
MainActivity
└─ NavHostFragment
   ├─ DeviceListFragment (start)
   └─ DeviceControlFragment
```

```xml
<action
    android:id="@+id/action_list_to_control"
    app:destination="@id/deviceControlFragment" />
```

화면 이동 관계를 graph에 선언한다.

---

## 1일차 · 16–21분 — 안정적인 argument

```kotlin
val args = bundleOf(ARG_DEVICE_ID to device.id)
findNavController().navigate(R.id.action_list_to_control, args)
```

전달할 것: 작은 ID와 화면에 필요한 최소값

전달하지 않을 것: Activity, Fragment, View, 연결 객체

---

## 1일차 · 21–27분 — 누락 입력과 Back

```kotlin
val deviceId = arguments
    ?.getString(ARG_DEVICE_ID)
    ?.takeIf { it.isNotBlank() }

if (deviceId == null) renderMissingDevice()
```

| 흐름 | 기대 |
|---|---|
| 목록 항목 선택 | 제어 화면 + ID |
| Back | 기존 목록으로 복귀 |
| argument 누락 | 오류 안내 + 제어 비활성 |

---

## 1일차 · 27–30분 — 실습 이양

1. graph를 그림으로 먼저 확인한다.
2. 두 Fragment의 View 로그를 남긴다.
3. 이동과 Back을 관찰한다.
4. argument 누락을 안전하게 재현한다.

**1일차 설명 합계: 4+6+6+5+6+3 = 30분**

---

# 2일차 — 목록과 검증 가능한 입력

`30분 설명·시연 → 60분 실습`

---

## 2일차 · 0–5분 — RecyclerView 파이프라인

```text
List<MockDevice>
      │ submitList
      ▼
ListAdapter ── creates/binds ──▶ ViewHolder ──▶ item XML
      │ click(item)
      └────────────────────────▶ navigate(device.id)
```

---

## 2일차 · 5–11분 — 화면 item 모델

```kotlin
data class MockDevice(
    val id: String,
    val name: String,
    val ready: Boolean,
)
```

ID는 항목 동일성, name/ready는 표시 내용이다.

```kotlin
override fun areItemsTheSame(old: MockDevice, new: MockDevice) =
    old.id == new.id
```

---

## 2일차 · 11–17분 — bind는 현재 item 전체를 그린다

```kotlin
fun bind(item: MockDevice) {
    nameView.text = item.name
    statusView.setText(
        if (item.ready) R.string.status_ready
        else R.string.status_disconnected
    )
    itemView.setOnClickListener { onClick(item) }
}
```

재사용되는 View에 이전 item 상태를 남기지 않는다.

---

## 2일차 · 17–23분 — 입력 검증 순서

```kotlin
val text = pulseInput.text.toString().trim()
val looksLikeInteger = text.matches(Regex("[+-]?\\d+"))
val millis = text.toLongOrNull()

when {
    text.isEmpty() -> showRequired()
    !looksLikeInteger -> showNumberOnly()
    millis == null || millis !in 100L..5000L -> showRange()
    else -> renderMockPulse(millis.toInt())
}
```

빈 값 → 정수 형식 → `Long` 변환·범위 → 정상 처리 순서다.

---

## 2일차 · 23–27분 — 경계와 실패를 표로 고정

| 입력 | 기대 |
|---:|---|
| `100`, `5000` | 성공 경계 |
| `99`, `5001` | 범위 오류 |
| 매우 긴 숫자열 | 범위 오류 |
| `500` | 정상 mock 결과 |
| 빈 값 | 필수 오류 |
| `abc` | 숫자 형식 오류 |

실제 출력 명령은 보내지 않는다.

---

## 2일차 · 27–30분 — 실습 이양

완료 조건:

- 0개·1개·여러 개 목록 확인
- item 데이터 기반 클릭
- 정상·양쪽 경계·세 실패 입력 확인
- 누락 device ID에서 제어 비활성

**2일차 설명 합계: 5+6+6+6+4+3 = 30분**

---

## 다음 주 질문

mock 펄스 계산을 오래 걸리는 작업으로 바꾸었을 때 RecyclerView 스크롤과 버튼 응답을 멈추지 않으려면 어떻게 해야 할까?
