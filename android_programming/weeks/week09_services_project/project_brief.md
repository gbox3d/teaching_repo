# 9주차 1차 과제 — Android 중간 앱

## 목적

1–7주차의 Kotlin/XML UI, lifecycle, ViewModel, coroutine, StateFlow를 누적 `Smart I/O Controller`의 중간 단계로 통합한다. 장치 연결은 fake transport로 재현하며 실제 BLE/GATT/ESP32-C3 펌웨어 구현·빌드·플래싱은 범위 밖이다.

## 운영 방식

- 개인 제출 또는 팀 제출 여부: **과목 운영 정책 `TBD`**
- 제출 채널·파일명·마감·지각 정책: LMS 공지 `TBD`
- 발표 시간 기준: 3분 이내 권장, 최종 공지는 `TBD`
- 팀 운영 시에도 각 학생의 코드 설명, 장애 대응, commit/작업 근거를 개별 확인한다.
- 팀원에게 결과를 적용하려면 실제 제출물 또는 명시적 팀원 근거가 있어야 한다.

## 필수 기능

1. Kotlin/XML Views로 상태, progress, 시작/취소 또는 재시도 control을 표시한다.
2. event → ViewModel → fake transport → StateFlow → lifecycle-aware render 흐름을 구현한다.
3. 최소 Idle, Working/Connecting, Ready/Success, Empty 또는 경계, Error 상태를 구분한다.
4. UI thread를 blocking하지 않고 중복 요청/취소 정책을 적용한다.
5. Fragment View에서 `repeatOnLifecycle(STARTED)`로 상태를 수집한다.
6. fake failure 또는 timeout 뒤 사용자 안내와 재시도 경로를 제공한다.
7. Service를 사용한다면 별도 thread가 아니라는 전제에서 필요성과 작업 scope/cleanup을 설명한다. Service 사용 자체는 필수 기능이 아니다.

## 발표 산출물 — 5점

- 문제와 단방향 상태 흐름 그림
- normal 동작 live demo 또는 동등한 재현 증거
- boundary/failure와 복구 demo
- lifecycle/coroutine/Service 선택 근거에 대한 개인 설명
- 실행 실패에 대비한 동일 revision의 짧은 backup 증거

## 레포트 산출물 — 5점

1. 실행 환경과 재현 절차
2. 요구사항→파일/함수→검증 증거 추적표
3. UI state와 lifecycle/coroutine 수명 설계
4. normal·boundary·failure test 기록
5. commit id와 개인 기여/설명 위치. 팀 표기는 과목 정책 `TBD`를 따른다.

## 범위 제외

- 실제 BLE scan/connect/GATT 구현
- 실제 UUID·GPIO·장치 식별자 확정
- ESP32-C3 firmware source, build, flash, 회로 작업
- 불필요한 foreground service 또는 무한 background 실행
- 학생 개인정보·secret·실제 성적을 공개 저장소에 기록

## 완료 체크

- [ ] 앱과 제출 revision이 동일하다.
- [ ] normal·boundary·failure를 3분 이내 재현한다.
- [ ] 회전/STOPPED 복귀와 collector 중복을 확인했다.
- [ ] retry 뒤 정상 상태로 돌아온다.
- [ ] 발표 5점 + 레포트 5점의 근거가 모두 있다.
- [ ] 개인/팀 운영을 임의 확정하지 않고 공식 `TBD` 정책을 확인했다.
