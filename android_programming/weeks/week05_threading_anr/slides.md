---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 5주차
footer: Main thread · Executor · race condition
---

# 메인 스레드, ANR 위험, 경쟁 상태

> “백그라운드”는 빠름이 아니라 책임과 수명의 분리다.

---

# 1일차 — 멈추는 UI에서 응답형 UI로

`30분 설명·시연 → 60분 실습`

---

## 1일차 · 0–4분 — 증상 먼저 보기

```kotlin
statusView.text = "작업 시작"
Thread.sleep(2_000) // 교육용 실패 재현
statusView.text = "작업 완료"
```

관찰:

- 시작 문구가 즉시 그려지는가?
- 다른 버튼과 스크롤이 반응하는가?
- 입력이 작업 뒤 한꺼번에 처리되는가?

---

## 1일차 · 4–10분 — 메인 queue

```text
input ─┐
draw ──┼─▶ Main Message Queue ─▶ Looper/Main Thread
click ─┘                              │
                              한 작업이 길면 뒤가 대기
```

메인 스레드는 View 이벤트와 화면 갱신의 소유자다.

---

## 1일차 · 10–16분 — 멈춤과 ANR

| 용어 | 의미 |
|---|---|
| blocking | 현재 thread가 작업 완료를 기다림 |
| UI freeze/jank | 사용자가 지연·끊김을 느낌 |
| ANR | 시스템이 정해진 상황·시간 기준으로 무응답 판단 |

짧은 멈춤도 UX 실패다. 특정 sleep 시간이 항상 ANR을 보장한다고 가정하지 않는다.

---

## 1일차 · 16–22분 — 작업과 결과의 왕복

```text
Main: 클릭 → Running 표시 → executor.submit
                              │
Worker:                 blocking mock
                              │ result
                              ▼
Main: Handler.post → Success/Error render
```

```kotlin
executor.submit {
    val result = try {
        Result.success(slowMockWork(duration))
    } catch (cancelled: InterruptedException) {
        Thread.currentThread().interrupt()
        return@submit
    } catch (error: Exception) {
        Result.failure(error)
    }
    mainHandler.post { render(result) }
}
```

---

## 1일차 · 22–27분 — UI 상태는 명시적으로

| 상태 | 실행 버튼 | 진행 표시 | 결과 |
|---|---|---|---|
| Idle | 활성 | 숨김 | 안내 |
| Running | 비활성 | 표시 | 실행 중 |
| Success | 활성 | 숨김 | mock 성공 |
| Error | 활성 | 숨김 | 실패 이유·재시도 |

중복 클릭으로 여러 작업을 만들지 않는다.

---

## 1일차 · 27–30분 — 실습 이양

1. blocking 실패를 짧게 재현한다.
2. 같은 duration을 Executor로 옮긴다.
3. UI는 main에서만 갱신한다.
4. `0/800/2500ms`를 같은 표로 비교한다.

**1일차 설명 합계: 4+6+6+6+5+3 = 30분**

---

# 2일차 — 취소와 공유 상태

`30분 설명·시연 → 60분 실습`

---

## 2일차 · 0–5분 — 작업보다 View가 먼저 사라질 수 있다

```text
Control View A ── starts Task T
      │ Back / rotation
      ▼
onDestroyView(A)      Task T finishes later
      │ cancel + token invalidate     │
      └───────────────────────────────┘ ignore stale result
```

---

## 2일차 · 5–11분 — Future와 협력적 취소

```kotlin
override fun onDestroyView() {
    activeToken = null
    runningTask?.cancel(true)
    statusView = null
    super.onDestroyView()
}
```

작업은 interruption을 무시하지 않아야 한다. 취소 요청과 즉시 종료는 같은 말이 아니다.

---

## 2일차 · 11–17분 — race는 실행 순서 문제

```text
counter = 7

Worker A: read 7 ───── write 8
Worker B:    read 7 ───── write 8

두 번 증가했지만 결과는 8
```

`counter += 1`은 원자적 한 동작이라고 가정할 수 없다.

---

## 2일차 · 17–23분 — 한 번 맞았다고 안전하지 않다

| workers | 반복 | unsafe 예상 |
|---:|---:|---|
| 1 | 100,000 | 대체로 기대값, 경쟁 없음 |
| 4 | 각 25,000 | 실행마다 달라질 수 있음 |

경쟁 bug는 비결정적이다. 여러 번 실행하고 thread-safe 근거를 코드에서 찾는다.

---

## 2일차 · 23–27분 — AtomicInteger

```kotlin
val counter = AtomicInteger(0)

repeat(25_000) {
    counter.incrementAndGet()
}
```

```text
4 workers × 25,000 = expected 100,000
```

원자적 연산은 공유 갱신의 계약을 명시한다.

---

## 2일차 · 27–30분 — 실습 이양

- 긴 작업→즉시 Back: stale UI 갱신 없음
- unsafe 1 worker, 4 workers 각각 반복
- atomic 4 workers 5회 모두 기대값
- Executor 종료와 View 참조 정리 확인

**2일차 설명 합계: 5+6+6+6+4+3 = 30분**

---

## 다음 주

동일한 작업을 Coroutine으로 옮겨 dispatcher, scope, cancellation, exception을 하나의 구조 안에서 표현한다.
