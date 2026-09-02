# 15주차 — 기말 개인 실기

## 이번 주 질문

제한 시간 안에 낯선 starter의 상태·비동기·BLE 경계를 읽고, 요구 변경을 구현한 뒤 정상과 실패를 자신의 말로 어떻게 증명할까?

## 측정 가능한 평가 목표

- 공개된 구조를 바탕으로 시험 당일 제시되는 요구를 입력·출력·정상·경계·실패 조건으로 분해한다.
- Kotlin/XML View 앱의 상태, lifecycle-aware coroutine/Flow, Android component 또는 데이터 경계를 수정하고 근거를 설명한다.
- 제공 BLE abstraction을 사용해 연결 상태와 권한·disconnect·timeout 중 요구된 경로를 구현·검증한다.
- 최소 정상·경계·실패 증거와 최종 source/commit을 제한 시간 안에 제출한다.
- 지정 코드 흐름, 상태 전이, 관찰된 실패와 다음 진단을 개인 시연·구술로 답한다.

## 평가 배점

| 구분 | 점수 |
|---|---:|
| 구현 | 15 |
| 시연 | 5 |
| **합계** | **20** |

세부 공개 기준은 [examples/rubric.md](examples/rubric.md)를 따른다.

## 1일차 — 요구 분석과 1차 구현

| 구간 | 내용 |
|---|---|
| 설명·절차 시연 30분 | 시험 규칙, 공개 starter 구조, 요구 분해, 상태·증거·장애 절차 |
| 개인 실기 60분 | 시험 당일 공개 요구 분석, 핵심 정상 경로 구현, 중간 저장·검증 |

## 2일차 — 실패 대응과 개인 시연

| 구간 | 내용 |
|---|---|
| 설명·절차 시연 30분 | 제출 무결성, 실패 검증, 시연·구술 기준, 장비/네트워크 장애 절차 |
| 개인 실기·시연 60분 | 구현 마무리, 정상·경계·실패 검증, 최종 제출, 개인 시연·구술 |

두 수업일 모두 정확히 `30분 설명·절차 시연 + 60분 개인 실기`다. 분반 인원에 따른 시연 순서·보조 기록 방식은 동일한 구현 시간과 개인 설명 기회를 보장하도록 별도 공지한다.

> **DEMO_CAPACITY_TBD:** 개강 전에 분반 인원 `N`, 동시에 평가할 수 있는 평가자 수 `E`, 학생당 시연 시간 `D`분을 고정하고 `T_demo = ceil(N / E) × D`를 계산해 `T_demo ≤ 60분`인지 검증한다. 60분에 맞지 않으면 평가자를 늘려 병렬 평가하거나, 모든 학생에게 동일한 별도 공식 시연 슬롯을 사전 공지한다. 순서나 대기열 때문에 특정 학생의 `D` 또는 실기시간을 줄이지 않는다. 최종 `N/E/D`와 운영안은 공식 시험 공지가 확정한다.

## 선수 지식과 준비물

- 1~14주차 Kotlin/XML View, lifecycle, coroutine/Flow, Android component, Provider, 권한, BLE 상태·입출력
- 시험 공지에서 허용한 Android Studio·JDK·SDK 기준 환경
- 강의자가 제공한 시험 starter, BLE abstraction, fake transport
- 실물 장치 사용 여부와 제공 범위는 시험 공지 우선이며 학생 firmware 작업은 평가하지 않는다.

## 공개 자료

- [Marp 안내 슬라이드](slides.md)
- 감독·설명 대본: 강의자 별도 관리(비공개)
- [개인 실기 진행지](lab.md)
- [공개 자료 안내](examples/README.md)
- [시험 blueprint](examples/exam_blueprint.md)
- [20점 rubric](examples/rubric.md)
- [starter 공개 구조](examples/starter/README.md)

## 이 폴더에 포함하지 않는 것

- 실제 학기 시험 문제와 정답
- 완성 구현 또는 정답 코드
- 비공개 평가 사례나 내부 채점 메모
- 학생별 변형 값, 학생 코드, 이름·학번·성적

위 항목은 이 공개 교안 밖의 승인된 시험 운영 위치에서만 관리한다.

## 완료 증거

- 최종 source 또는 공지된 제출 묶음과 commit SHA
- 구현 항목별 정상·경계·실패 검증표
- 상태·로그·화면을 연결한 개인 시연
- 지정 질문에 대한 개인 코드 흐름·장애 진단 설명
- 제출 완료 화면과 비밀·개인정보 미포함 확인

## 다음 단계

[전체 주차 색인](../README.md)으로 돌아가 학기 산출물과 공식 제출 기록을 정리한다.

## 공식 참고 자료

- [Activity lifecycle — Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Lifecycle-aware coroutines for Views — Android Developers](https://developer.android.com/topic/libraries/architecture/views/coroutines-views)
- [Content provider basics — Android Developers](https://developer.android.com/guide/topics/providers/content-provider-basics)
- [Bluetooth permissions — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)
- [Transfer BLE data — Android Developers](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)
