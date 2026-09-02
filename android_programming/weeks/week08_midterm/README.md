# 8주차 — 중간 개인 실기

주간 질문: **제한 시간 안에 UI·생명주기·비동기 상태가 맞다는 것을 어떤 증거로 보여 줄 것인가?**

1–7주차의 Kotlin/XML View, Activity/Fragment 생명주기, ViewModel, coroutine, StateFlow를 개인이 통합하는 중간평가 주차다. 이 폴더에는 공개 가능한 구조·동형 연습·채점 기준만 있으며 실제 시험 문항, 정답, fixture, 숨은 테스트, 학생 데이터는 포함하지 않는다.

## 학습 목표

수강생은 공개 리허설 종료 시 다음을 수행할 수 있다.

1. 요구사항을 UI, lifecycle, coroutine, Flow, 검증 항목으로 분해한다.
2. event → ViewModel → state → render의 최소 구현 순서를 제한 시간 계획으로 작성한다.
3. normal·boundary·failure 경로를 각각 재현하고 화면·Logcat 증거를 남긴다.
4. 화면 회전과 STARTED/STOPPED 전환에서 상태 보존·collector 중복 여부를 확인한다.
5. 제출 파일, 실행 대상, commit id와 짧은 코드 설명을 스스로 점검한다.

## 2일 × 90분 흐름

| 일차 | 30분 설명·live demo | 60분 활동 |
|---|---|---|
| 1일차 | 공개 평가 구조, 요구사항 분해, 시간 배분 | 공개 동형 통합 연습과 자기 진단 |
| 2일차 | 실행·제출 검증, 오류 위치 좁히기 | 공개 검증 리허설 또는 별도 비공개 패킷의 개인 실기 |

실제 시험 시행일, 허용 자료·도구, 제출 방식과 문제는 해당 학기 LMS/비공개 시험 패킷을 최종 기준으로 한다.

## 선수 지식·준비

- 1–7주차 Kotlin/XML Views, ViewModel, lifecycle, coroutine, StateFlow
- 기준 Android 프로젝트 실행, Logcat filter, 화면 회전/백그라운드 전환
- 지정 저장 위치와 제출 채널: `TBD`(LMS 공지에서 확정)

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [공개 동형 연습](lab.md)
- [공개 시험 구조](exam_structure.md)
- [20점 채점표](rubric.md)
- [예제 경계 안내](examples/README.md)
- [중립 starter 안내](examples/starter/README.md)

## 공개·비공개 경계

공개 저장소에는 역량 영역, 시간 관리, 중립 상태 모델, 검증 절차와 rubric만 둔다. 실제 문제 문구·고유 입력·정답·fixture·숨은 testcase·학생 식별/점수는 비공개 시험 공간에서 관리한다.

## 완료 증거

- 60분 계획표와 실제 소요 비교
- normal·boundary·failure 실행 증거
- 회전/STOPPED 복귀와 collector 수 확인 기록
- 제출 전 체크리스트, 마지막 commit id, 1분 설명 메모
- [20점 rubric](rubric.md)에 따른 자기 채점

## 다음 주 연결

[9주차 Service와 1차 과제](../week09_services_project/README.md)에서 중간 앱의 비동기 상태 구조를 유지하면서 Android Service의 수명과 실행 thread를 구분한다.

## 공식 참고 자료

- [Android Developers — Guide to app architecture](https://developer.android.com/topic/architecture)
- [Android Developers — ViewModel overview](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Android Developers — lifecycle-aware coroutine](https://developer.android.com/topic/libraries/architecture/coroutines)
- [Android Developers — StateFlow and SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
