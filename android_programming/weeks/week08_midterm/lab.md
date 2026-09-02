# 8주차 공개 동형 연습 — 비동기 상태 패널

이 실습은 평가 역량을 연습하는 **공개용 중립 시나리오**다. 실제 시험 문항·고유 값·fixture·답안·숨은 testcase와 관련이 없다.

## 시나리오

강의자 기준 프로젝트의 중립 `Status Panel` 화면에 fake 작업의 Idle, Working, Success, Empty, Error를 표시한다. 실제 BLE, 장치명, UUID, ESP32-C3 펌웨어는 사용하지 않는다.

## 1일차 60분 — 제한시간 통합 연습

### 먼저 예측

Working 중 회전, 연속 Start 두 번, 빈 결과, fake exception에서 최종 상태·active Job·render 횟수를 구현 전에 적는다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–7분 | 요구를 state/event/evidence로 분해 | 체크표 |
| 7–15분 | 기준 프로젝트 실행·TODO 탐색 | 변경 전 실행 |
| 15–30분 | UiState·ViewModel·정상 경로 | Working→Success |
| 30–42분 | lifecycle-aware render | 회전/복귀 로그 |
| 42–52분 | Empty/Error/재시도 | 경계·실패 화면 |
| 52–60분 | clean run·자기 채점·commit | rubric/commit id |
| 합계 | **60분** | |

### 공개 연습 요구사항

- XML View는 상태 문구, progress, start/retry 버튼을 갖는다.
- 상태 변경은 ViewModel이 소유하며 UI는 읽기 전용 StateFlow를 수집한다.
- fake 작업은 coroutine으로 실행되고 UI thread를 blocking하지 않는다.
- Fragment View는 `repeatOnLifecycle(STARTED)` 안에서 상태를 collect한다.
- 중복 Start 정책을 정하고 예측과 실제 로그를 비교한다.
- Empty와 Error는 다른 화면 의미와 복구 행동을 갖는다.

### 검증

- [ ] 정상: Working→Success이며 버튼이 계속 반응한다.
- [ ] 경계: Empty가 오류로 표시되지 않고 회전 뒤 최신 상태가 보인다.
- [ ] 실패: fake exception 뒤 Error와 retry가 보이고 복구된다.

<details>
<summary>힌트 1 — 구현 순서</summary>

UI 세부 디자인 전에 sealed UI 상태와 정상 event 흐름을 먼저 완성한다.
</details>

<details>
<summary>힌트 2 — 중복 요청</summary>

새 요청이 이전 요청을 대체한다면 ViewModel이 이전 Job을 취소하고 마지막 의도만 상태에 반영한다.
</details>

<details>
<summary>힌트 3 — 수집 경계</summary>

Fragment 객체가 아닌 View 수명에 맞춰 `viewLifecycleOwner.lifecycleScope`와 `repeatOnLifecycle`를 함께 사용한다.
</details>

## 2일차 60분 — 진단·제출 리허설

### 먼저 예측

아래 증상별 첫 확인 지점을 쓴다: build 실패, click 무반응, spinner 고정, 회전 뒤 crash, 상태 1회 emit에 render 2회.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | 진단 예상표 작성 | 증상→첫 확인 지점 |
| 8–20분 | 강의자 제공 중립 결함 카드 진단 | 재현·원인 메모 |
| 20–33분 | lifecycle/중복 collector 점검 | START/STOP 로그 |
| 33–45분 | normal/boundary/failure 재검증 | 3경로 체크표 |
| 45–54분 | 1분 코드 설명·자기 채점 | rubric 근거 |
| 54–60분 | 제출본 재실행·commit 대조 | 최종 checklist |
| 합계 | **60분** | |

중립 결함 카드는 강의 중 즉석으로 제공하되 실제 시험 코드·fixture를 재사용하지 않는다.

### 검증 순서

1. 첫 build error와 파일/줄 확인
2. launcher Activity/Fragment와 View binding 확인
3. click event가 ViewModel에 도달하는 로그 확인
4. Job 시작·취소·오류 확인
5. StateFlow emit과 visible render 횟수 확인
6. 제출한 revision을 새 실행으로 확인

### 검증

- [ ] 정상: 제출본 새 실행에서 Success를 재현한다.
- [ ] 경계: 회전·STOPPED·연속 Start 결과가 정책과 같다.
- [ ] 실패: Error→retry→Success를 재현한다.
- [ ] 개인정보, 실제 시험 값, 실제 장치 식별자가 없다.

<details>
<summary>힌트 1 — click 무반응</summary>

selector/binding, listener 등록, ViewModel event 로그 순서로 첫 단절 지점을 찾는다.
</details>

<details>
<summary>힌트 2 — 회전 crash</summary>

Fragment View가 파괴된 뒤 binding을 참조하는 collector가 남았는지 확인한다.
</details>

<details>
<summary>힌트 3 — render 중복</summary>

producer emit id와 collector instance id를 함께 기록해 producer 중복과 collector 누적을 구분한다.
</details>

## 확장

- 같은 요구를 callback 기반으로 설계했을 때 취소·상태 보존 복잡도를 비교한다.
- TalkBack용 상태 설명과 버튼 content description을 점검한다.
- 실행 증거를 30초 화면 녹화 하나로 재현하는 시나리오를 만든다.

## 제출 증거

- 두 예측표와 실제 차이
- 공개 연습 normal·boundary·failure 화면/로그
- [20점 rubric](rubric.md) 자기 채점과 항목별 근거
- 1일차·2일차 commit id
- 최종 제출 체크리스트
