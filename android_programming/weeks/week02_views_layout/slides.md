---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 2주차
footer: XML Views · Adaptive Smart I/O Controller
---

# XML View와 적응형 장치 제어판

> 화면은 픽셀 좌표가 아니라 관계와 상태의 표현이다.

---

# 1일차 — View tree와 resource

`30분 설명·시연 → 60분 실습`

---

## 1일차 · 0–4분 — 화면을 계약으로 읽기

| 사용자 질문 | UI가 답해야 하는 것 |
|---|---|
| 어떤 장치인가? | 장치 이름 |
| 지금 연결됐나? | 상태 문구·색 이외의 단서 |
| 무엇을 할 수 있나? | 활성화된 동작 |
| 실패하면? | 이유와 다음 행동 |

이번 주는 실제 장치 대신 mock 상태를 사용한다.

---

## 1일차 · 4–9분 — XML은 View tree가 된다

```text
ConstraintLayout
├─ TextView   title
├─ TextView   deviceName
├─ TextView   connectionStatus
├─ Button     connectButton
└─ Button     outputButton
```

부모가 자식의 측정과 배치에 참여한다. 깊은 중첩은 읽기와 측정 비용을 키운다.

---

## 1일차 · 9–15분 — 크기와 단위

| 표현 | 의미 |
|---|---|
| `wrap_content` | 내용에 필요한 크기 |
| `match_parent` | 부모가 허용한 크기 |
| ConstraintLayout의 `0dp` | 연결된 constraint 사이 크기 |
| `dp` | 레이아웃·간격 |
| `sp` | 사용자 글꼴 배율을 따르는 텍스트 |

```xml
android:layout_width="0dp"
android:layout_height="wrap_content"
android:textSize="18sp"
```

---

## 1일차 · 15–21분 — 위치보다 관계

```xml
app:layout_constraintStart_toStartOf="parent"
app:layout_constraintEnd_toEndOf="parent"
app:layout_constraintTop_toBottomOf="@id/deviceName"
```

```text
parent start ├──── status(0dp) ────┤ parent end
                         ▲
                    deviceName 아래
```

절대 좌표가 아니라 어떤 View와 연결되는지를 읽는다.

---

## 1일차 · 21–27분 — resource와 단일 render

```kotlin
enum class MockConnection { DISCONNECTED, READY }

fun render(state: MockConnection) {
    statusView.setText(
        if (state == MockConnection.READY)
            R.string.status_ready else R.string.status_disconnected
    )
    outputButton.isEnabled = state == MockConnection.READY
}
```

문구는 `strings.xml`, 상태별 표시 결정은 `render()` 한 곳에 둔다.

---

## 1일차 · 27–30분 — 실습 이양

1. View tree와 폭 정책을 먼저 그린다.
2. 세로 화면 기준선을 만든다.
3. mock 상태를 두 번 전환한다.
4. 화면·로그·활성 상태를 함께 확인한다.

**1일차 설명 합계: 4+5+6+6+6+3 = 30분**

---

# 2일차 — 화면 변화와 접근성

`30분 설명·시연 → 60분 실습`

---

## 2일차 · 0–5분 — configuration은 입력 조건

```text
같은 layout + 다른 조건
├─ portrait / landscape
├─ 작은 폭 / 큰 폭
├─ 기본 글꼴 / 큰 글꼴
└─ 짧은 번역 / 긴 번역
```

한 기기에서 한 번 보인 화면은 충분한 검증이 아니다.

---

## 2일차 · 5–11분 — resource qualifier

```text
res/
├─ values/dimens.xml
├─ values-land/dimens.xml
├─ layout/activity_main.xml
└─ values/strings.xml
```

```xml
<!-- values-land/dimens.xml -->
<dimen name="screen_padding">32dp</dimen>
```

공통 구조는 유지하고 필요한 값만 조건별로 바꾼다.

---

## 2일차 · 11–17분 — 긴 내용과 스크롤

나쁜 신호:

- 고정 폭·높이 때문에 글자 잘림
- 가로에서 버튼이 화면 밖으로 밀림
- 큰 글꼴에서 상태와 버튼이 겹침

우선순위:

1. `wrap_content`와 constraint 확인
2. 불필요한 고정 높이 제거
3. 내용이 화면보다 길 수 있으면 스크롤 컨테이너 검토

---

## 2일차 · 17–23분 — 접근 가능한 상태

| 항목 | 점검 질문 |
|---|---|
| label | 아이콘만으로 의미를 강요하는가? |
| 상태 | 색 외에 `연결됨/연결 안 됨` 문구가 있는가? |
| 조작 | 비활성 버튼의 이유를 주변 문구로 아는가? |
| 읽기 | 큰 글꼴에서도 핵심 정보가 남는가? |

텍스트가 이미 의미를 말하는 버튼에는 중복 설명을 만들지 않는다.

---

## 2일차 · 23–27분 — 상태와 행동의 일관성

| 상태 | 연결 버튼 | 출력 버튼 | 상태 문구 |
|---|---|---|---|
| `DISCONNECTED` | 연결 | 비활성 | 연결 안 됨 |
| `READY` | 연결 해제 | 활성 | 제어 준비 |

상태 문구, 버튼 label, `isEnabled`를 서로 다른 listener에 흩뜨리지 않는다.

---

## 2일차 · 27–30분 — 실습 이양

검증 매트릭스:

- 세로 / 가로
- 기본 글꼴 / 큰 글꼴
- 짧은 이름 / 긴 이름
- `DISCONNECTED` / `READY`

**2일차 설명 합계: 5+6+6+6+4+3 = 30분**

---

## Compose 비교 — 확장 관찰만

Compose의 Modifier도 크기·관계·접근성 의미를 선언하지만 이번 주 구현과 평가는 XML View/resource 구조를 기준으로 한다.

---

## 다음 주 질문

회전으로 화면 객체가 다시 만들어질 때 어떤 callback이 호출되고 어떤 상태를 어디에 보존해야 할까?
