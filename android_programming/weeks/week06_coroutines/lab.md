# 6주차 실습 — 취소 가능한 fake 장치 연결

## 시나리오

`Smart I/O Controller`의 연결 버튼을 누르면 fake transport가 handshake를 흉내 낸다. 실제 BLE·ESP32-C3·펌웨어는 사용하지 않는다. 사용자가 화면을 떠나거나 다시 연결하면 이전 작업을 정리하고, timeout·실패 뒤에는 복구 행동을 제공한다.

## 공통 규칙

1. 강의자의 Kotlin/XML Views 기준 프로젝트 복사본에서 작업한다.
2. 아래 snippet의 package/import와 의존성 버전은 기준 프로젝트에 맞춘다. 미확정 값은 `TBD`다.
3. 구현 전에 예상 로그 순서와 상태 전이를 적는다.
4. Logcat에는 비밀값·실제 장치 식별자를 남기지 않는다.

## 1일차 60분 — UI를 막지 않는 연결과 scope

### 먼저 예측

다음 두 경우의 버튼 반응, 로그 순서, 회전 뒤 상태를 표로 쓴다.

- click listener에서 `Thread.sleep(2_000)` 호출
- `viewModelScope.launch { delay(2_000) }` 호출

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | 기존 UI·ViewModel과 예상 작성 | 소유자/취소 시점 문장 |
| 8–20분 | blocking 기준선 재현 | 멈춘 UI 영상·thread 로그 |
| 20–35분 | suspend fake 연결로 교체 | UI 연속 클릭 가능 |
| 35–48분 | ViewModel 소유 상태 표시 | 회전 전후 상태 |
| 48–56분 | dispatcher 관찰 | Main/IO 로그와 선택 근거 |
| 56–60분 | 체크·commit | commit id와 예측 비교 |
| 합계 | **60분** | |

### 필수 구현

- `FakeConnectionRepository.connect()`는 `delay` 뒤 `Ready`를 반환한다.
- ViewModel의 `connect()`가 `viewModelScope`에서 실행한다.
- 중복 실행 여부를 화면과 Logcat에서 알 수 있다.
- UI 변경을 위해 임의의 raw `Thread`를 만들지 않는다.
- 화면 회전 전후 상태 변화와 작업 수명을 기록한다.

### 검증

- [ ] 정상: 지연 뒤 `Connecting → Ready`다.
- [ ] 경계: 회전해도 UI가 멈추거나 중복 연결하지 않는다.
- [ ] 실패: fake repository가 던진 예외가 crash 대신 상태로 보인다.

<details>
<summary>힌트 1 — 가장 작은 시작점</summary>

repository는 `delay()`와 반환값만 가진 suspend 함수로 시작한다. dispatcher를 먼저 넣지 않는다.
</details>

<details>
<summary>힌트 2 — 소유권</summary>

click listener는 `viewModel.connect()`만 호출하고 Job은 ViewModel이 보관한다.
</details>

<details>
<summary>힌트 3 — blocking adapter</summary>

정말 blocking인 함수만 `withContext(Dispatchers.IO)`로 감싼다. `delay` 자체를 IO로 옮길 필요는 없다.
</details>

## 2일차 60분 — 취소·timeout·복구

### 먼저 예측

요청 A가 2초, 0.2초 뒤 시작한 요청 B가 0.5초 걸린다고 가정한다. 취소하지 않을 때와 이전 Job을 취소할 때 최종 상태·로그를 적는다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–7분 | 상태도·예상 작성 | A/B timeline |
| 7–20분 | 이전 Job 취소 | 연속 탭 로그 |
| 20–33분 | timeout 정책 | timeout 상태·재시도 |
| 33–45분 | 실패와 cancellation 분리 | 서로 다른 UI/로그 |
| 45–55분 | cleanup·복구 검증 | `finally` 1회 |
| 55–60분 | 제출 묶음·commit | 체크표와 commit id |
| 합계 | **60분** | |

### 필수 구현

- 새 연결은 이전 연결 Job을 취소한다.
- timeout 값은 `TIMEOUT_MS_TBD` 상수로 두고 강의 환경에서 확정한다.
- `CancellationException`을 사용자 오류로 표시하지 않는다.
- 예상된 fake 연결 실패는 오류 문구와 재시도 버튼을 보여 준다.
- 성공·취소·실패 모두에서 attempt 자원이 정확히 한 번 정리된다.

### 검증

- [ ] 정상: 재시도 뒤 `Ready`가 된다.
- [ ] 경계: 5회 연속 탭 후 마지막 요청 결과만 남는다.
- [ ] 실패: timeout과 fake I/O 오류를 구분해 표시한다.
- [ ] 취소: 취소 뒤 빨간 오류가 보이지 않는다.

<details>
<summary>힌트 1 — 최신 Job</summary>

`private var connectJob: Job? = null`을 두고 새 `launch` 전에 `cancel()`한다.
</details>

<details>
<summary>힌트 2 — timeout</summary>

`withTimeoutOrNull`의 null 결과를 timeout 상태로 매핑하면 cancellation catch를 불필요하게 넓히지 않아도 된다.
</details>

<details>
<summary>힌트 3 — callback 경계</summary>

callback API가 실제 작업을 취소하지 못하면 attempt id를 비교해 오래된 결과를 무시한다. 이는 취소와 별도 방어다.
</details>

## 확장

- 두 child 작업을 `coroutineScope`로 묶고 한쪽 실패 시 다른 쪽의 취소 로그를 관찰한다.
- CPU loop에 `ensureActive()`를 넣기 전후 취소 지연을 측정한다.
- dispatcher를 생성자 주입해 테스트에서 제어하는 설계를 스케치한다.

## 제출 증거

- 예측표와 실제 결과 차이
- normal·연속 탭·timeout·오류 화면 및 Logcat
- 회전 전후 상태 캡처
- 1일차·2일차 commit id
- scope와 dispatcher 선택 근거 각 한 문장
