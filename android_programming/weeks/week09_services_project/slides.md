---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍(Android)
footer: 9주차 · Service와 1차 과제
---

# Android Service

## 1일차 · [0–4분] 두 질문을 분리

```text
Q1. 화면 밖에서도 계속되어야 하는가? → component/lifetime
Q2. main thread를 막는가?            → execution context
```

**Service는 Q1의 component이며 Q2를 자동 해결하지 않는다.**

---

## 1일차 · [4–9분] Service 유형

| 유형 | 시작/관계 | 대표 수명 | 사용자 인지 |
|---|---|---|---|
| started | `startService` 계열 | 스스로/외부에서 stop할 때까지 | 보장 아님 |
| bound | `bindService` | client가 bind한 동안 | 보통 client UI와 연동 |
| foreground | started + foreground 승격 | 사용자가 인지하는 지속 작업 | 필수 notification |

foreground service는 모든 background 작업의 기본값이 아니다.

---

## 1일차 · [9–14분] Service도 main thread

```kotlin
override fun onStartCommand(intent: Intent?, flags: Int, id: Int): Int {
    Log.d(TAG, Thread.currentThread().name)
    return START_NOT_STICKY
}
```

```text
Activity callback ─┐
Service callback  ─┴─ hosting process main thread (기본)
```

blocking 작업은 ANR 위험이 있다.

---

## 1일차 · [14–20분] Service 내부 작업 scope

```kotlin
private val serviceJob = SupervisorJob()
private val serviceScope = CoroutineScope(serviceJob + Dispatchers.Default)

override fun onDestroy() {
    serviceJob.cancel()
    super.onDestroy()
}
```

- scope 수명은 Service 수명에 맞춘다.
- 실제 blocking I/O는 `Dispatchers.IO`로 격리한다.
- 연결 정책과 resource cleanup을 명시한다.

---

## 1일차 · [20–25분] started와 bound

```text
started: caller ─ start ─▶ Service ─ stopSelf/stopService
bound  : client ─ bind  ─▶ Binder API ─ unbind
```

Bound Service는 client-server interface다. 같은 process의 local binder도 lifecycle 정리가 필요하다.

---

## 1일차 · [25–30분] API 선택

| 요구 | 우선 검토 |
|---|---|
| 화면이 보일 때 비동기 | ViewModel + coroutine |
| 조건 기반 지연/보장 작업 | WorkManager 등 background API |
| client가 상호작용 | bound service |
| 사용자가 인지하는 지속 작업 | foreground service 조건 검토 |

**실습:** 같은 작업을 Service로 할 이유를 한 문장으로 먼저 쓴다.

---

# Foreground Service와 1차 과제

## 2일차 · [0–5분] foreground의 계약

```text
사용자가 인지하는 지속 작업
 ├─ 적합한 service type/권한
 ├─ 사용자에게 보이는 notification
 └─ 시작·종료·제한 준수
```

target OS/SDK별 세부 요건은 학기 기준표 `TBD`에서 검증한다.

---

## 2일차 · [5–10분] 제한을 피하려고 쓰지 않는다

- background 시작 제한이 있다.
- type과 permission 요구가 target별로 달라질 수 있다.
- notification은 사용자 가시성 계약이다.
- 짧은 UI 작업에는 과도한 선택이다.

정확한 요구가 없으면 foreground service를 기본 처방하지 않는다.

---

## 2일차 · [10–15분] 누적 앱 구조

```text
XML View event
  → ViewModel/UiState
    → fake transport
      → Idle/Working/Ready/Error

Service 실험은 별도 경계로 관찰
```

1차 과제는 BLE/펌웨어가 아니라 Android 중간 앱의 구조와 증거를 평가한다.

---

## 2일차 · [15–21분] 3분 발표 흐름

1. 문제와 상태 흐름
2. normal demo
3. boundary/failure와 복구
4. scope/lifecycle 선택 설명

화면 녹화는 backup이고 가능하면 재현 가능한 live 흐름을 준비한다.

---

## 2일차 · [21–26분] 10점 평가

| 구분 | 점수 | 핵심 증거 |
|---|---:|---|
| 발표 | 5 | 동작·구조·실패 복구·설명 |
| 레포트 | 5 | 요구 추적·설계·검증·재현/개인 근거 |
| 합계 | 10 | |

개인/팀 운영은 과목 정책 `TBD`; 개인별 설명·기여 증거는 확인한다.

---

## 2일차 · [26–30분] 제출 전 검증

- 발표 revision과 레포트 commit 일치
- normal·boundary·failure 3분 내 재현
- Service=thread라는 표현 없음
- 실제 BLE UUID/비밀값/학생 데이터 없음
- ESP32-C3 펌웨어 작업 없음

**실습:** rubric 근거가 비어 있는 항목부터 보완한다.
