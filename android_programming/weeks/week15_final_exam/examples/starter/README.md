# 기말 실기 Starter — 공개 구조 안내

이 디렉터리는 **공개 placeholder**다. Gradle wrapper, Manifest, source, resource, 실제 TODO가 없으므로 빌드 가능한 Android 프로젝트가 아니다. 실제 시험 starter는 승인된 비공개 배포 위치에서 시험 운영 절차에 따라 제공한다.

## 예상 역할 지도

```text
exam-starter/
├─ README.md                  # 실행, 허용 수정, 제출 계약
├─ app/src/main/res/layout/   # XML View contract
├─ app/src/main/.../ui/       # event, render, UiState
├─ app/src/main/.../domain/   # use case 또는 지정 component 경계
└─ app/src/main/.../transport/# 제공 fake/BLE abstraction adapter
```

실제 패키지, 파일명, 수정 허용 범위, TODO, SDK/도구 버전은 시험 배포본이 권위 원본이다.

## 시험 시작 전 읽을 순서

1. 배포본 식별자와 무결성 확인 방법
2. 실행 환경과 최초 실행 절차
3. 수정 가능/금지 파일 범위
4. fake/real transport 선택 규칙
5. 로그·개인정보 마스킹 규칙
6. 제출 파일·commit·마감 계약

## 유지해야 할 공개 원칙

- Kotlin + XML View 기반
- 제공 abstraction을 통한 BLE 접근
- `Idle → Scanning → Connecting → Discovering → Ready → Disconnected/Error`
- 권한은 앱 대상/기기 조건을 고려하는 제공 policy 사용
- UUID·GPIO·message 계약은 시험 배포본이 고정하며 공개 placeholder가 추정하지 않음
- 학생 firmware 코딩·빌드·플래싱 제외

## 포함하지 않는 것

- 실제 시험 prompt나 TODO
- 정답 코드 또는 완성 구현
- 비공개 평가 사례
- 학생별 값과 학생 데이터

실제 starter를 이 공개 디렉터리에 복사하거나 시험 종료 후 정답과 함께 게시하지 않는다.
