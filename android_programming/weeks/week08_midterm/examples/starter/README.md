# 공개 리허설용 중립 starter 안내

이 디렉터리는 실제 시험 starter가 아니다. 공개 연습을 위한 **구조 안내만** 제공하며 source, fixture, 답안, testcase를 포함하지 않는다.

## 강의자가 별도 공개 연습 프로젝트에 준비할 역할

```text
practice/
 ├─ PracticeActivity 또는 PracticeFragment : XML View event·render
 ├─ PracticeViewModel                     : 상태와 coroutine 소유
 ├─ FakePracticeSource                    : 지연·빈 값·실패 재현
 └─ layout                                : status/progress/start/retry
```

파일명·package·리소스 id·버전은 실제 시험과 무관한 공개 연습용 `TBD`로 정한다.

## 학생이 시작 전에 관찰할 것

1. 변경 전 기준 앱이 실행되는가?
2. launcher 화면과 실제 편집 파일이 일치하는가?
3. TODO가 UI, state, async, collect, verification 중 어디에 속하는가?
4. fake source가 normal·empty·failure를 어떻게 선택하는가?
5. 제출에서 요구한 파일 범위가 무엇인가?

## 기대 관찰

- baseline은 답을 제공하지 않지만 실행 가능한 출발점을 제공한다.
- fake source는 네트워크·BLE·실물 장치 없이 경계와 실패를 반복 재현한다.
- 학생은 실제 시험과 다른 중립 요구를 통해 시간 관리와 검증 순서를 연습한다.

실제 시험 starter와 checksum/release는 비공개 패킷에서 별도로 배포·검증한다.
