# 9주차 실습 — Service 관찰과 중간 앱 발표

## 시나리오

`Smart I/O Controller` 중간 앱은 fake transport 상태를 XML View에 표시한다. 별도 `DemoStatusService`로 Android component 수명과 실행 thread를 관찰하되, Service를 실제 BLE 연결이나 모든 background 작업의 기본 해법으로 가정하지 않는다. ESP32-C3 펌웨어는 다루지 않는다.

## 1일차 60분 — Service는 thread가 아니다

### 먼저 예측

Activity `onStart`, Service `onCreate/onStartCommand`, Service 내부 `Dispatchers.Default` child가 출력할 thread 이름과 Service stop 뒤 child 상태를 적는다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | Service 필요성·예상 로그 작성 | lifetime/thread 두 축 |
| 8–20분 | manifest와 started service 최소 구현 | callback 순서 |
| 20–31분 | Activity/Service thread 비교 | 둘 다 main 로그 |
| 31–44분 | Service-owned coroutine 추가 | worker thread와 UI 응답 |
| 44–54분 | stop/cleanup 및 중복 start | cancellation 1회 |
| 54–60분 | API 선택표·commit | 근거/commit id |
| 합계 | **60분** | |

### 필수 구현

- service는 manifest에 명시하고 외부 노출이 필요 없으면 `android:exported="false"`로 둔다.
- `onCreate`, `onStartCommand`, `onDestroy`에 callback·instance·thread 로그를 남긴다.
- blocking을 흉내 내는 작업은 main callback에서 직접 실행하지 않는다.
- Service 소유 coroutine Job을 종료 시 cancel하고 cleanup 로그를 남긴다.
- 중복 start에서 새 instance/새 callback/작업 중복 여부를 관찰한다.

### 검증

- [ ] 정상: start→작업→stop callback과 cleanup 순서가 설명과 같다.
- [ ] 경계: 연속 start가 무제한 child 작업을 만들지 않는다.
- [ ] 실패: fake worker exception이 process crash나 무한 작업으로 이어지지 않는다.
- [ ] Activity와 Service callback이 기본적으로 같은 main thread임을 기록했다.

<details>
<summary>힌트 1 — 기준 로그</summary>

각 로그에 callback, `System.identityHashCode(this)`, `Thread.currentThread().name`을 넣으면 instance와 thread를 구분할 수 있다.
</details>

<details>
<summary>힌트 2 — Service scope</summary>

Service가 소유한 `SupervisorJob`과 dispatcher로 scope를 만들고 `onDestroy()`에서 cancel한다.
</details>

<details>
<summary>힌트 3 — 중복 start</summary>

현재 Job이 active인지 확인해 무시/교체/병렬 중 하나의 정책을 명시한다.
</details>

## 2일차 60분 — 1차 과제 리허설과 증거

### 먼저 예측

3분 발표 순서별 예상 소요와 실패 시 backup 경로를 적는다. rubric 발표 5점·레포트 5점의 각 항목에 파일/화면/로그 근거를 하나씩 연결한다.

### 시간 상자

| 시간 | 활동 | 확인 증거 |
|---:|---|---|
| 0–8분 | 범위·운영정책·rubric 확인 | 10점 합계/TBD 표시 |
| 8–21분 | normal demo 압축 | 3분 이내 실행 |
| 21–34분 | boundary/failure/retry 재현 | 상태·로그·복구 |
| 34–45분 | architecture/Service 선택 설명 | 흐름도·결정 근거 |
| 45–54분 | 레포트 근거·개인 기여 점검 | commit/작업 기록 |
| 54–60분 | 최종 리허설·commit | 발표 revision |
| 합계 | **60분** | |

### 필수 완료

- [project brief](project_brief.md)의 필수 범위를 3분 이내로 시연한다.
- normal, boundary, failure와 retry를 같은 revision에서 재현한다.
- Service를 사용했거나 사용하지 않은 설계 이유를 수명/가시성/thread 근거로 설명한다.
- 발표 revision, 레포트 commit, 캡처가 서로 일치한다.
- 개인/팀 운영은 `TBD`로 표시하고 개인 설명·기여 증거를 준비한다.

### 검증

- [ ] 정상: 앱 시작→fake 상태→Ready 흐름이 재현된다.
- [ ] 경계: empty 또는 연속 event 정책이 일관된다.
- [ ] 실패: fake 오류→안내→retry→Ready가 재현된다.
- [ ] 발표 5점 + 레포트 5점 = 총 10점임을 확인했다.

<details>
<summary>힌트 1 — 발표 순서</summary>

앱 소개보다 먼저 문제와 상태 흐름을 20초 내 제시하고 normal→실패/복구→설명으로 간다.
</details>

<details>
<summary>힌트 2 — Service 선택 설명</summary>

“background라서”가 아니라 UI 밖 지속 필요성, 사용자 가시성, client 관계, 실행 context를 근거로 답한다.
</details>

<details>
<summary>힌트 3 — 개인 근거</summary>

commit/작업 기록과 본인이 설명할 code location을 연결한다. 팀원 표기 방식 자체는 과목 정책 `TBD`를 따른다.
</details>

## 확장

- local bound service의 Binder API로 read-only 상태를 노출하고 unbind 후 reference 정리를 관찰한다.
- 같은 요구를 ViewModel coroutine, WorkManager, foreground service로 각각 선택했을 때 tradeoff 표를 만든다.
- process recreation을 가정한 상태 복구 전략을 문서로 설계한다.

## 제출 증거

- Service callback/thread/cancellation Logcat
- API 선택표와 이유
- 3분 발표 자료 또는 영상, normal·boundary·failure 캡처
- 레포트와 개인 설명/기여 근거
- 1일차·2일차 commit id
