# 8주차 공개 예제 경계

이 폴더는 시험 답안이 아니라 공개 리허설용 중립 구조만 설명한다.

## 포함 자료

- [starter 안내](starter/README.md): 파일 역할과 TODO 범주
- [공개 동형 연습](../lab.md): 실제 시험과 다른 `Status Panel` 시나리오
- [공개 rubric](../rubric.md): 20점 공통 역량 기준

## 제외 자료

- 실제 시험 문제·고유 값·fixture
- 정답·부분 답안·모범 구현
- 자동/숨은 testcase와 채점 script
- 학생 이름·학번·코드·점수·제출 URL

## 복사 가능한 중립 상태 형태

```kotlin
sealed interface PracticeUiState {
    data object Idle : PracticeUiState
    data object Working : PracticeUiState
    data object Empty : PracticeUiState
    data class Success(val summary: String) : PracticeUiState
    data class Error(val message: String) : PracticeUiState
}
```

예상 관찰: exhaustive `when`으로 모든 공개 연습 상태를 구분할 수 있다. 이것은 실제 시험 상태/요구를 암시하지 않는 일반 패턴이다.

이 폴더는 독립적으로 빌드 가능한 Gradle 프로젝트를 제공하지 않는다. 기준 SDK·Lifecycle·coroutine 버전은 학기 환경표의 `TBD`다.
