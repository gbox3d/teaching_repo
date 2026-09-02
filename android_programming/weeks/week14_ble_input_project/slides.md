---
marp: true
theme: default
paginate: true
title: 14주차 BLE 입력 알림과 Smart I/O 통합 프로젝트
---

# 14주차

## BLE 입력 알림과 Smart I/O 통합 프로젝트

현재 값에는 **어느 연결에서 언제 받은 값인지**가 포함된다.

---

# 평가 구조

| 구분 | 점수 |
|---|---:|
| 발표 | 12 |
| 보고서 | 8 |
| 합계 | 20 |

`COURSE_POLICY_TBD`: 개인/팀 제출 단위는 공식 공지로 확정한다. 개인 구술 증거는 모든 경우에 남긴다.

---

<!-- _class: lead -->
# 1일차 — 입력 notification과 재연결

30분 설명·라이브 시연

---

## 0–5분 — read와 notification

| 방식 | 시작 | 결과 |
|---|---|---|
| read | client 요청 | 한 시점의 값 |
| notification | client가 구독 설정 | characteristic 변화가 callback으로 전달 |

구독 설정 성공 전에는 입력 관찰이 준비됐다고 단정하지 않는다.

---

## 5–10분 — 입력 사건 경로

```text
ESP32 input change
  → GATT notification
    → provided transport callback
      → BleGateway InputEvent Flow
        → ViewModel reducer
          → XML View
```

학생은 제공 abstraction 위에서 상태·오류·UI를 구현한다.

---

## 10–15분 — Ready의 수업 계약

```text
Connecting
   → Discovering
      ├─ required service/characteristics match
      ├─ required input subscription succeeds
      └─ Ready
```

UUID와 descriptor/payload 세부값은 instructor-pinned protocol까지 `TBD`다.

---

## 15–20분 — 현재성(freshness)

~~~kotlin
data class ObservedInput(
    val channel: InputChannel,
    val level: InputLevel,
    val receivedAt: Instant,
    val connectionEpoch: Long,
)
~~~

- disconnect 즉시 현재 값을 `Stale/Unknown`으로 표시
- 이전 epoch의 늦은 사건은 현재 세션에 적용하지 않음

---

## 20–25분 — lifecycle-aware 수집

```text
viewLifecycleOwner.lifecycleScope
  └─ repeatOnLifecycle(STARTED)
      ├─ collect link state
      └─ collect input state
```

화면이 보이지 않을 때 사라진 View를 직접 갱신하지 않는다.

---

## 25–30분 — fake 재연결 시연

```text
Ready(epoch=4) → Input(HIGH,e4) → LinkLost
→ Stale(HIGH) → ConnectionStarted(epoch=5) → Unknown
→ Ready(epoch=5) / Unknown
→ old Input(LOW,e4) [ignore]
→ Input(LOW,e5) [current]
```

빠른 반복, timeout, 오래된 사건을 예측하고 실습한다.

---

<!-- _class: lead -->
# 2일차 — 통합·리허설·평가 증거

30분 설명·라이브 시연

---

## 0–5분 — 최종 앱의 한 문장

> 제공 펌웨어의 ESP32-C3를 찾아 연결하고, Android에서 출력을 제어하며, 입력 변화를 관찰하고, 실패 뒤 복구하는 XML View 앱

Wi-Fi·cloud·firmware 개발은 기본 평가 범위가 아니다.

---

## 5–10분 — 2~3분 시연 구조

1. 20초: 문제·구조·보드 라벨
2. 40초: scan/connect/discover/Ready
3. 40초: 출력 제어와 확인 범위
4. 40초: 입력 notification
5. 30초: disconnect/reconnect
6. 10초: 회고와 commit

시간은 연습 기준이며 실제 운영 공지는 별도다.

---

## 10–15분 — 통합 상태 표

| LinkState | 출력 | 입력 표시 |
|---|---|---|
| Scanning/Connecting/Discovering | 금지 | Unknown |
| Ready | 계약에 따라 허용 | Unknown → 새 notification/snapshot 뒤 Current + 수신 시각 |
| Disconnected | 금지 | Stale/Unknown |
| Error | 금지 | 원인 + 복구 |

기능 수보다 모순 없는 상태가 우선이다.

---

## 15–20분 — 실패 시연은 복구까지

```text
보드 전원 off
→ Disconnected 표시
→ 출력 비활성 + 입력 Stale
→ 사용자 재연결
→ Discovering/구독
→ Ready / Unknown
→ 새 입력 → Current
```

오류 화면만 보여주고 끝내지 않는다.

---

## 20–25분 — 20점 루브릭

| 발표 12 | 점수 | 보고서 8 | 점수 |
|---|---:|---|---:|
| 핵심 시나리오 | 3 | 구조·경계 | 2 |
| 입출력 통합 | 3 | 구현 증거 | 2 |
| 실패·복구 | 2 | 테스트 매트릭스 | 2 |
| 상태·구조 설명 | 2 | 재현·출처·회고 | 2 |
| 개인 구술 증거 | 2 |  |  |

---

## 25–30분 — 정책·제출 체크

- `COURSE_POLICY_TBD`: 개인/2인 팀은 공식 공지 대기
- 팀이 허용돼도 개인 구술·장애 대응 기록
- source, report, demo evidence, checklist, commit SHA
- UUID/GPIO/protocol `TBD`를 임의 확정하지 않음
- 실제 제출 채널·마감은 LMS 공지 우선

---

# 공식 자료

- Android Developers: Transfer BLE data
- Android Developers: BLE in the background
- Android Developers: Lifecycle-aware coroutines for Views
- Kotlin Documentation: Flow
