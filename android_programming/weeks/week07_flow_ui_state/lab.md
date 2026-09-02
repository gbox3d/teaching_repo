# 7주차 실습 — 연결 상태 시뮬레이터

## 시나리오

`Smart I/O Controller` 대시보드가 fake transport의 연결 상태를 지속적으로 표시한다. 화면이 보일 때만 XML View를 render하고, 회전·화면 이동·timeout·일시 실패에도 하나의 최신 상태와 복구 경로를 유지한다. 실제 BLE나 ESP32-C3 펌웨어는 다루지 않는다.

## 공통 규칙

1. 강의자의 Kotlin/XML Views 기준 프로젝트와 fake transport를 사용한다.
2. 의존성 버전, timeout, retry 횟수는 학기 기준표의 `TBD`를 유지한다.
3. 코딩 전에 상태 전이와 로그 순서를 예측한다.
4. UI를 갱신하는 Flow는 bare `launch`/`launchIn`이 아니라 `repeatOnLifecycle(STARTED)` 안에서 collect한다.

## 1일차 60분 — StateFlow와 exhaustive render

### 먼저 예측

collector A가 시작된 뒤 상태가 Idle→Scanning→Ready로 바뀌고 collector B가 나중에 시작한다. cold Flow와 StateFlow에서 각 collector가 볼 값과 producer 실행 횟수를 적는다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | 상태 전이·예측표 | 가능한 상태/금지 조합 |
| 8–20분 | sealed `ControllerUiState` | exhaustive `when` |
| 20–34분 | private MutableStateFlow/public StateFlow | 외부 변경 불가 |
| 34–47분 | fake 상태 stream mapping | 전이 Logcat |
| 47–56분 | 단일 render 함수 | 이전 View 잔상 없음 |
| 56–60분 | 검증·commit | 예측 비교와 commit id |
| 합계 | **60분** | |

### 필수 구현

- Idle, Scanning, Connecting, Ready, Empty, Error 상태를 sealed type으로 만든다.
- ViewModel만 `MutableStateFlow`에 쓰고 외부에는 `StateFlow`를 노출한다.
- fake transport 상태를 UI 상태로 매핑한다.
- 한 `render(state)`가 progress, status text, retry, control enabled를 모두 결정한다.
- 실제 장치명·UUID 대신 공개 가능한 `Demo Device`/`TBD`를 사용한다.

### 검증

- [ ] 정상: Idle→Scanning→Connecting→Ready 순서다.
- [ ] 경계: 빈 검색 결과는 Error가 아니라 Empty다.
- [ ] 실패: fake 예외는 Error와 재시도 버튼으로 바뀐다.
- [ ] 이전 Ready의 장치명이 Empty/Error 화면에 남지 않는다.

<details>
<summary>힌트 1 — 상태부터</summary>

View 속성보다 먼저 화면이 가질 수 있는 상태 목록과 각 상태의 payload를 정한다.
</details>

<details>
<summary>힌트 2 — 읽기 전용 공개</summary>

`private val _uiState = MutableStateFlow(...)`와 `val uiState = _uiState.asStateFlow()`를 분리한다.
</details>

<details>
<summary>힌트 3 — render 잔상</summary>

각 분기에서 필요한 View만 켜지 말고, 함수 시작 또는 분기마다 모든 관련 View를 결정한다.
</details>

## 2일차 60분 — lifecycle, timeout, retry

### 먼저 예측

화면이 STOPPED인 3초 동안 상태가 Connecting→Ready로 바뀐다고 가정한다. render 로그가 언제 찍혀야 하고, 복귀 직후 어떤 값을 받아야 하는지 적는다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | lifecycle 예상·로그 지점 | START/STOP timeline |
| 8–22분 | `repeatOnLifecycle` collect | 숨은 View render 없음 |
| 22–34분 | 회전·복귀 중복 검사 | active collector 1개 |
| 34–46분 | timeout과 제한 retry | 시도 횟수 로그 |
| 46–55분 | 오류 후 수동 재시도 | Error→Ready |
| 55–60분 | 증거·commit | 행렬과 commit id |
| 합계 | **60분** | |

### 필수 구현

- Fragment는 `viewLifecycleOwner.lifecycleScope`에서 `repeatOnLifecycle(STARTED)`를 사용한다.
- collector 시작/종료와 render 횟수를 식별 가능한 로그로 남긴다.
- timeout 뒤 무한 spinner 대신 Error와 재시도를 제공한다.
- I/O 성격의 일시 실패만 `RETRY_COUNT_TBD` 이내에서 retry한다.
- 화면 이동·회전 뒤 한 상태 emit이 한 visible render를 만든다.

### 검증

- [ ] 정상: 화면이 보일 때 모든 전이가 render된다.
- [ ] 경계: STOPPED 동안 render 0회, 복귀 시 최신 Ready 1회다.
- [ ] 실패: 최종 실패 후 retry 버튼으로 Ready까지 복구한다.
- [ ] 중복: 회전을 반복해도 active collector가 누적되지 않는다.

<details>
<summary>힌트 1 — Fragment View 수명</summary>

`viewLifecycleOwner.lifecycleScope.launch { viewLifecycleOwner.repeatOnLifecycle(...) { ... } }` 구조를 사용한다.
</details>

<details>
<summary>힌트 2 — 여러 Flow</summary>

여러 Flow를 같은 반복 block에서 수집한다면 각각 별도 child `launch`가 필요하다. 이번 필수 범위는 하나의 통합 UI 상태가 더 단순하다.
</details>

<details>
<summary>힌트 3 — retry 조건</summary>

predicate에서 예외 종류와 현재 attempt를 로그로 남긴다. 취소나 사용자 조치가 필요한 상태는 false다.
</details>

## 확장

- raw 상태 두 개를 `combine`해 하나의 UI 상태로 만드는 것과 처음부터 통합 상태를 노출하는 것을 비교한다.
- `stateIn`과 `SharingStarted.WhileSubscribed(...)` 정책을 실험하되 지속 시간은 `TBD`로 둔다.
- fake stream을 테스트 dispatcher로 검증하는 테스트 설계를 스케치한다.

## 제출 증거

- 상태 전이표와 단방향 데이터 흐름 그림
- visible/STOPPED/복귀 시 collector·render 로그
- normal·empty·timeout·retry 화면
- 1일차·2일차 commit id
- bare collect가 위험한 이유 한 문장
