# 14주차 실습 — 입력 notification과 통합 시연

## 공통 시나리오

`Smart I/O Controller`가 수업용 ESP32-C3에 연결되어 출력을 제어하고 입력 변화를 notification으로 표시한다. 연결이 끊기면 출력은 비활성화되고 입력은 `Stale/Unknown`이 된다. 새 epoch의 연결 시작과 Ready 진입에서는 입력을 `Unknown`으로 초기화하며, 그 epoch의 새 notification 또는 pinned snapshot 뒤에만 `Current`가 된다.

> **COURSE_POLICY_TBD:** 개인/2인 팀 제출 단위와 점수 적용 방식은 강의자 공식 공지로 확정한다. 모든 학생은 개인 구술·예측·장애 대응 증거를 제출한다.

## 실행 전 예측

| 사건 | LinkState | 입력 상태 | 출력 가능 | 다음 행동 |
|---|---|---|---:|---|
| 구독 성공 | Discovering |  |  |  |
| 같은 level 3회 | Ready |  |  |  |
| link lost | Ready |  |  |  |
| 재연결 직후 | Discovering |  |  |  |
| 새 epoch Ready, 새 입력 없음 | Ready |  |  |  |
| 이전 epoch 사건 도착 | Ready(new epoch) |  |  |  |

## 1일차 60분 — fake 입력과 재연결

### 시간표 — 합계 60분

- 0~10분: notification 경로·Ready 조건·예측표 작성
- 10~25분: 입력 Flow를 ViewModel 상태와 XML View에 연결
- 25~40분: 정상·빠른 반복·동일값 notification 검증
- 40~55분: disconnect/reconnect·old epoch·timeout 주입
- 55~60분: 증거 캡처, commit, 개인 회고

### 필수 구현

1. 입력 event를 `level + receivedAt + connectionEpoch` 상태로 변환한다.
2. View lifecycle이 STARTED인 동안 lifecycle-aware하게 수집한다.
3. disconnect 즉시 입력을 `Stale`, 새 epoch 연결 시작과 Ready 진입에서는 `Unknown`으로 만들고 출력을 비활성으로 만든다.
4. 이전 connectionEpoch 사건이 새 세션의 현재 값을 덮지 못하게 하며, 새 notification/snapshot만 `Current`로 만든다.

### 검증 매트릭스

| 종류 | 주입 | 기대 관찰 | 불변 조건 |
|---|---|---|---|
| 정상 | Ready + HIGH notification | Current(HIGH), 시각 표시 | 출력 상태 불변 |
| 경계 | HIGH 3회 연속 | crash·목록 폭증 없음 | 최신 상태 HIGH |
| 경계 | 빠른 LOW/HIGH | 마지막 수신 상태 표시 | UI thread block 없음 |
| 실패 | link lost | Disconnected + Stale/Unknown | 출력 write 금지 |
| 실패 | old epoch event | 무시 + 진단 로그 | 새 세션 상태 불변 |
| 실패 | subscription timeout | Error + 재연결/재시도 안내 | Ready 금지 |

<details>
<summary>힌트 1 — 두 Flow 수집</summary>

`repeatOnLifecycle` 블록 안에서 link state와 input state를 각각 child coroutine으로 수집한다.

</details>

<details>
<summary>힌트 2 — 현재성</summary>

```text
if (event.connectionEpoch == currentEpoch && linkState == Ready)
    currentInput = Current(event)
else
    recordDiagnostic("stale input ignored")
```

</details>

<details>
<summary>힌트 3 — reconnect</summary>

새 연결은 새 epoch를 만들고 입력을 Unknown으로 시작한다. 새 notification 또는 pinned snapshot/read 계약이 올 때만 Current로 바꾼다.

</details>

## 2일차 60분 — real 통합·리허설·증거

### 시간표 — 합계 60분

- 0~10분: fake 회귀, 보드 라벨, protocol `TBD/확정` 점검
- 10~25분: real connect·output·input 정상 통합
- 25~40분: board off → reconnect → 새 입력 복구 시나리오
- 40~55분: 2~3분 리허설/현장 시연과 개인 구술 기록
- 55~60분: 보고서·rubric·제출 체크리스트·commit SHA 확인

### 필수 구현

1. 연결 상태 기계의 모든 중간 상태가 UI에 보인다.
2. Ready에서 제공 출력 채널을 제어하고 확인 가능한 범위를 정확히 말한다.
3. 입력 변화를 notification으로 표시하고 수신 시각/currentness를 보인다.
4. 보드 off 뒤 출력 금지·입력 stale·재연결·새 입력까지 복구한다.
5. 실물 장비 장애 시 같은 시나리오를 fake transport로 재현한다.

### 검증 매트릭스

| 종류 | 절차 | 기대 관찰 | 제출 증거 |
|---|---|---|---|
| 정상 | scan → Ready | 상태 전이 완주 | event trace |
| 정상 | output 변경 | 계약 범위 내 처리 | UI·event·물리 관찰 |
| 정상 | input 변경 | Current + receivedAt | UI·notification log |
| 경계 | 동일 input 반복 | 안정적 동일 상태 | event 수/최종 state |
| 실패 | board off | Disconnected, output off, input stale | 3개 상태 동시 캡처 |
| 복구 | reconnect | ConnectionStarted → Unknown → Ready/Unknown → 새 notification 또는 snapshot → Current | 새 epoch trace |

<details>
<summary>힌트 1 — 3분 시연</summary>

메뉴 설명을 줄이고 `연결 → 출력 → 입력 → 실패 → 복구` 한 줄만 재현한다. 각 단계에 하나의 로그 근거를 연결한다.

</details>

<details>
<summary>힌트 2 — 보드가 고장났을 때</summary>

보드 교환을 요청하고 기다리는 동안 fake trace로 앱 계약을 증명한다. 학생이 펌웨어를 재플래시하지 않는다.

</details>

<details>
<summary>힌트 3 — 개인 구술</summary>

현재 LinkState, 다음 event, 출력 허용 여부, 입력 현재성 판단을 자신의 말로 답한다. 팀원의 역할이나 코드를 대신 암기하지 않는다.

</details>

## 확장 문제

- 입력 event를 제한 길이 이력으로 표시하고 rotation 뒤 상태를 유지한다.
- reconnect backoff 정책을 설계하되 무제한 background 연결은 별도 제약으로 분석한다.
- 여러 입력 채널을 같은 reducer에 추가할 때 식별·현재성 규칙을 표로 만든다.

## 제출

- [project_brief.md](project_brief.md)의 필수 산출물
- [rubric.md](rubric.md) 자기 점검표
- fake/real 정상·경계·실패·복구 증거
- 개인 구술 기록
- 보고서와 submission checklist
- 최종 commit SHA
