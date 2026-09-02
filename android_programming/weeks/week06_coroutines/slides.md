---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍(Android)
footer: 6주차 · Kotlin Coroutine
---

# Kotlin Coroutine

## 1일차 · [0–4분] 작업의 소유자는 누구인가?

질문: **화면을 떠나면 이 작업은 계속되어야 하는가?**

```text
UI event → owner scope → child job → result
                 └─ cancel ────────┘
```

coroutine은 가벼운 동시성 작업 단위이고, scope가 수명을 결정한다.

---

## 1일차 · [4–9분] `suspend`의 의미

```kotlin
suspend fun openFakeLink(): String {
    delay(1_000)
    return "Ready"
}
```

- `suspend`는 “느린 함수”나 “자동 background thread” 표시가 아니다.
- 중단 가능한 지점에서 현재 coroutine을 양보하고 나중에 재개할 수 있다.
- `delay`는 기다리는 동안 thread를 점유하지 않는다.

예측: `Thread.sleep`으로 바꾸면 버튼 반응은 어떻게 달라질까?

---

## 1일차 · [9–14분] scope와 구조적 동시성

```text
viewModelScope
 └─ connect job
     ├─ handshake child
     └─ status child
```

부모가 취소되면 자식도 취소된다. 화면 상태를 만드는 작업은 보통 ViewModel이 소유한다.

```kotlin
viewModelScope.launch { repository.connect() }
```

---

## 1일차 · [14–20분] dispatcher는 실행 문맥

| 작업 | 후보 | 이유 |
|---|---|---|
| XML View 변경 | Main | UI thread 규칙 |
| blocking 파일/API adapter | IO | blocking 작업 격리 |
| 큰 순수 계산 | Default | CPU 작업 |
| `delay` 기반 fake | 호출 문맥 유지 | thread를 막지 않음 |

```kotlin
val payload = withContext(Dispatchers.IO) { blockingRead() }
```

dispatcher와 lifecycle은 서로 다른 결정이다.

---

## 1일차 · [20–25분] UI는 결과를 관찰한다

```kotlin
fun connect() {
    viewModelScope.launch {
        _status.value = "Connecting"
        _status.value = repository.connect()
    }
}
```

Activity가 직접 장시간 작업을 붙잡지 않게 한다. 오늘은 문자열로 관찰하고 7주차에 `StateFlow<UiState>`로 교체한다.

---

## 1일차 · [25–30분] demo 체크

1. 연결 시작 직후 다른 버튼 클릭
2. Logcat의 thread 이름 관찰
3. 화면 회전
4. 명시적 취소

**실습:** 예측을 먼저 기록하고 `sleep → delay`, 임시 scope → 소유자 scope 순으로 바꾼다.

---

# 취소·timeout·예외

## 2일차 · [0–5분] 취소는 정상 제어 흐름

```kotlin
job?.cancel()
job = viewModelScope.launch { connectOnce() }
```

```text
Idle → Connecting → Ready
          └─ cancel → Idle
          └─ error  → Error
```

새 요청이 이전 요청을 대체한다면 이전 Job을 취소한다.

---

## 2일차 · [5–10분] 협력적 취소

```kotlin
while (isActive) {
    pollOnce()
    delay(250)
}
```

- suspend 함수는 취소를 확인한다.
- 긴 CPU loop는 `isActive` 또는 `ensureActive()`가 필요하다.
- `CancellationException`을 일반 오류로 바꾸지 않는다.

---

## 2일차 · [10–16분] timeout은 정책이다

```kotlin
val result = withTimeoutOrNull(TIMEOUT_MS_TBD) {
    repository.connect()
} ?: return@launch showTimeout()
```

`TIMEOUT_MS_TBD`는 학기 기준 환경에서 측정해 확정한다. timeout 뒤 사용자가 할 다음 행동을 제공한다.

---

## 2일차 · [16–22분] 예외 전파

```kotlin
try {
    connectOnce()
} catch (e: IOException) {
    showRecoverable(e)
} finally {
    releaseAttemptResources()
}
```

```text
child failure → parent policy → UI state
```

모든 `Throwable`을 삼키면 취소까지 실패 화면으로 바뀔 수 있다.

---

## 2일차 · [22–27분] 오래된 결과 방어

```kotlin
private var connectJob: Job? = null

fun connect() {
    connectJob?.cancel()
    connectJob = viewModelScope.launch { connectOnce() }
}
```

연속 탭에서 마지막 의도만 남아야 한다. 취소 이후 늦게 도착하는 callback adapter도 별도 식별자가 필요할 수 있다.

---

## 2일차 · [27–30분] 완료 조건

| 경로 | 기대 상태 |
|---|---|
| 정상 | Connecting → Ready |
| 경계: 연속 탭 | 마지막 요청만 Ready |
| 실패 | Error + 원인 로그 + 재시도 |
| 취소 | Error가 아니라 Idle/Cancelled |

다음 주에는 이 상태를 `StateFlow` 하나로 공개한다.
