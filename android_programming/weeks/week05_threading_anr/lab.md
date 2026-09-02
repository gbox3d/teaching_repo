# 5주차 실습 — 멈추는 mock 작업을 응답형 작업으로 바꾸기

## 공통 규칙

- blocking 코드는 강의자가 지정한 교육용 복사본에서 짧게 재현하고 최종 코드에서 제거한다.
- 실제 BLE scan/write나 ESP32-C3 작업을 호출하지 않는다.
- worker thread에서 View를 직접 변경하지 않는다.
- freeze를 관찰했다고 ANR 발생을 단정하지 않고 실제 증거에 맞는 용어를 쓴다.
- 반복 실험 중 에뮬레이터가 불안정하면 기준 프로젝트로 복구하고 강의자에게 알린다.

## 1일차 실습 — blocking과 Executor 비교 (60분)

### 상황과 문제

mock 출력 펄스 준비에 시간이 걸린다는 가정으로 click listener에서 대기했더니 상태 문구, 스크롤, 취소 버튼이 함께 멈췄다. 같은 지연 작업을 worker에서 실행하고 UI 상태만 main thread에서 갱신하라.

### 시간 배분

| 단계 | 구간 | 시간 | 활동 |
|---|---:|---:|---|
| 결과 예측 | 0–8분 | 8분 | duration별 UI·로그 예상 |
| blocking 재현 | 8–19분 | 11분 | 짧은 멈춤과 timestamp 관찰 |
| Executor 구현 | 19–36분 | 17분 | worker 작업과 main 결과 전달 |
| UI 상태 연결 | 36–48분 | 12분 | Idle/Running/Success/Error render |
| 경계·실패 검증 | 48–56분 | 8분 | 0/800/2500ms와 중복 클릭 |
| 정리·제출 | 56–60분 | 4분 | 실패 코드 제거와 증거 정리 |
| **합계** |  | **60분** |  |

### 1. 실행 전 예측

| 구현/입력 | 시작 문구 즉시 보임? | 다른 버튼 반응? | 예상 thread | 실제 |
|---|---|---|---|---|
| main blocking 800ms |  |  |  |  |
| executor 0ms |  |  |  |  |
| executor 800ms |  |  |  |  |
| executor 2500ms |  |  |  |  |

### 2. 교육용 blocking 실패 재현

별도 복사본의 click listener에서만 다음 흐름을 사용한다.

```kotlin
renderRunning()
Thread.sleep(durationMs) // 실패 재현 전용
renderSuccess(durationMs)
```

1. duration은 먼저 800ms로 제한한다.
2. click 시작/종료와 thread 이름을 로그로 남긴다.
3. 실행 중 보조 버튼을 눌러 callback timestamp를 비교한다.
4. 시작 상태가 언제 그려지는지 기록한다.
5. 관찰 후 이 blocking 구현을 최종 코드에서 제거한다.

### 3. Executor와 main Handler로 개선

요구사항:

- Fragment field에 단일 worker `ExecutorService`를 만든다.
- main looper와 연결된 `Handler`를 만든다.
- click 시 main에서 `Running`을 render하고 중복 실행 버튼을 비활성화한다.
- `executor.submit` 안에서는 mock 지연과 결과 계산만 한다.
- 완료/오류 UI는 `mainHandler.post`에서 render한다.
- 로그에 `Thread.currentThread().name`을 남겨 worker와 main을 구분한다.

### 4. UI 상태표 구현

| 상태 | 실행 버튼 | ProgressBar | 상태 문구 |
|---|---|---|---|
| Idle | 활성 | 숨김 | 대기 |
| Running | 비활성 | 표시 | mock 작업 중 |
| Success | 활성 | 숨김 | `Nms mock 완료` |
| Error | 활성 | 숨김 | 오류와 재시도 안내 |

모든 View 변경은 `render(state)` 한 곳에서 한다. 성공 문구가 실제 하드웨어 명령 성공으로 읽히지 않게 `mock`을 포함한다.

### 5. 정상·경계·실패 확인

- **정상:** executor 800ms 실행 중 보조 버튼과 목록 스크롤이 반응한다.
- **경계:** 0ms에서도 Running→Success 전이가 모순 없이 끝나고, 2500ms에도 중복 task가 생기지 않는다.
- **실패:** main blocking 800ms에서 입력 callback 지연을 재현하고 최종 구현에서는 해당 blocking 코드가 없다.
- **thread:** mock 작업 로그는 worker, `render()` 로그는 main thread다.

### 단계별 힌트

<details>
<summary>힌트 1 — 시작 문구가 작업 뒤에 보인다</summary>

문구를 대입한 직후에도 main thread가 click handler에서 돌아오지 않으면 다음 frame을 그릴 수 없다. 지연 작업이 어느 thread에서 실행되는지 로그로 확인한다.
</details>

<details>
<summary>힌트 2 — background 작업 뒤 View 변경 오류가 난다</summary>

worker block 안에서 TextView, Button, ProgressBar를 직접 만지는 줄을 찾는다. 결과 값만 만든 뒤 main Handler에 post한다.
</details>

<details>
<summary>힌트 3 — 버튼을 두 번 누르면 결과가 두 번 온다</summary>

Running 상태로 바꿀 때 실행 버튼을 비활성화하고, 별도 `runningTask`가 이미 완료되지 않았다면 새 submit을 하지 않는다.
</details>

### 확장

mock 함수가 음수 duration을 받으면 `IllegalArgumentException`을 발생시키도록 하고, 일반 실패는 Error UI와 재시도 가능한 상태로 바뀌는지 검증한다. 취소로 발생한 `InterruptedException`은 일반 오류로 렌더링하지 말고 interrupt 상태를 복원한 뒤 작업을 종료한다.

### 1일차 제출 증거

- `day1-responsiveness.md`: 네 조건의 예상/실제와 timestamp
- main/worker thread 이름 로그
- blocking 실패 코드가 최종본에서 제거됐다는 확인
- 상태표와 Running/Success 화면

## 2일차 실습 — View 취소 경계와 race condition (60분)

### 상황과 문제

긴 mock 작업 중 Back을 눌렀는데 이전 결과가 새 제어 화면에 나타난다. 또 여러 worker가 성공 횟수를 증가시켰더니 기대값보다 작은 값이 가끔 나온다. View 수명과 공유 갱신을 각각 안전하게 만들어라.

### 시간 배분

| 단계 | 구간 | 시간 | 활동 |
|---|---:|---:|---|
| 결과 예측 | 0–8분 | 8분 | 취소·race 결과 예상 |
| 취소 경계 | 8–22분 | 14분 | Future, token, View 정리 |
| unsafe counter | 22–35분 | 13분 | 1/4 worker 반복 실험 |
| atomic 수정 | 35–47분 | 12분 | AtomicInteger와 완료 신호 |
| 반복 검증 | 47–56분 | 9분 | 각 조건 5회와 Back 재검증 |
| 종료·제출 | 56–60분 | 4분 | executor 종료·표 정리 |
| **합계** |  | **60분** |  |

### 1. 코드 전 예측

| 조건 | expected | actual 예상 | 이유 | 실제 5회 |
|---|---:|---|---|---|
| unsafe, 1 worker × 100000 | 100000 |  |  |  |
| unsafe, 4 workers × 25000 | 100000 |  |  |  |
| atomic, 4 workers × 25000 | 100000 |  |  |  |

취소 시나리오도 먼저 적는다.

| 행동 | 이전 task 결과가 새 View에 보여야 하나? | 취소 로그 예상 |
|---|---|---|
| 2500ms 시작→즉시 Back |  |  |
| 시작→회전→새 Control View |  |  |

### 2. View 수명에 맞춘 취소

요구사항:

1. submit 결과 `Future`를 현재 task로 보관한다.
2. 각 실행에 고유한 in-memory token을 만든다.
3. `onDestroyView()`에서 token을 무효화하고 `Future.cancel(true)`를 요청한다.
4. View 참조를 정리한다.
5. main Handler callback은 token이 현재 실행과 같을 때만 render한다.
6. Fragment의 `onDestroy()`에서 소유한 executor를 `shutdownNow()`한다.

`cancel(true)`만 믿지 말고 stale result 검사를 함께 둔다.

### 3. unsafe counter 재현

교육용 실패 함수에서 공유 `Int`에 다음 read–modify–write를 여러 worker가 수행한다.

```kotlin
val current = unsafeCounter
if (iteration % 100 == 0) Thread.yield()
unsafeCounter = current + 1
```

- 1 worker × 100000을 5회 실행한다.
- 4 workers × 각 25000을 5회 실행한다.
- expected와 actual을 모두 기록한다.
- actual이 한 번 expected와 같아도 안전하다고 판정하지 않는다.

### 4. AtomicInteger로 수정

공유 값을 `AtomicInteger(0)`으로 바꾸고 각 worker에서 `incrementAndGet()`을 호출한다. worker 완료 수를 별도의 thread-safe 값으로 세어 마지막 worker만 결과를 main Handler에 전달한다.

같은 4×25000 조건을 5회 실행한다.

### 5. 정상·경계·실패 확인

- **정상:** atomic 4-worker 결과는 5회 모두 100000이다.
- **경계:** unsafe라도 1 worker에서는 경쟁이 없어 100000일 수 있다. 이것이 다중 thread 안전성을 증명하지 않음을 적는다.
- **실패:** unsafe 4-worker 결과가 어긋나는 run을 관찰하거나, 어긋나지 않았어도 read–modify–write interleaving으로 위험을 증명한다.
- **취소:** 2500ms 시작 직후 Back/회전에서 이전 결과가 새 View를 덮지 않는다.
- **수명:** Fragment 종료 후 새 task를 받지 않으며 executor 종료 로그가 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — cancel했는데 완료 로그가 남는다</summary>

interruption 요청과 작업 종료는 다르다. mock work가 `InterruptedException`을 삼키는지 보고, UI callback에서는 실행 token이 아직 유효한지 별도로 확인한다.
</details>

<details>
<summary>힌트 2 — unsafe 결과가 계속 100000이다</summary>

한 번의 결과로 판정하지 않는다. worker 수, 반복 횟수, 동일한 공유 변수 사용을 확인하고 강의자 기준의 `Thread.yield()` 지점을 적용해 5회 반복한다.
</details>

<details>
<summary>힌트 3 — 마지막 worker를 판단하기 어렵다</summary>

counter 값과 완료한 worker 수는 다른 상태다. 완료 수에는 별도의 `AtomicInteger`를 두고 `incrementAndGet() == workerCount`일 때만 결과를 post한다.
</details>

### 확장

single-thread executor가 unsafe counter를 우연히 안전하게 보이게 하는 이유와, fixed thread pool + AtomicInteger의 계약 차이를 4문장으로 비교한다.

### 2일차 제출 증거

- `day2-concurrency.md`: 세 조건 5회 결과와 interleaving 그림
- Back/회전 취소 로그와 stale result 미표시 증거
- `Future.cancel`, token 검사, AtomicInteger 핵심 코드
- “취소 요청이 즉시 종료 보장이 아닌 이유” 2문장

## 최종 제출 체크

- [ ] 두 날의 60분 실습 결과가 분리되어 있다.
- [ ] main thread blocking 실패 코드는 최종본에서 제거했다.
- [ ] worker가 View를 직접 갱신하지 않는다.
- [ ] 정상·경계·실패·취소를 모두 검증했다.
- [ ] 실제 BLE/GPIO/펌웨어 동작을 주장하지 않는다.
