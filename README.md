# 공용 수업교재

## 목차

- [목적](#목적)
- [온라인 교재 도서관](#온라인-교재-도서관)
- [로컬 빌드](#로컬-빌드)
- [읽는 순서](#읽는-순서)
- [교재 색인](#교재-색인)
- [실습조교 설치 목록](#실습조교-설치-목록)
- [공용 교재와 학교 운영자료의 경계](#공용-교재와-학교-운영자료의-경계)
- [편집 원칙](#편집-원칙)
- [라이선스](#라이선스)

## 목적

이 디렉터리는 대학과 학기에 관계없이 재사용할 수 있는 **수업교재의 단일 기준**이다.
슬라이드, 강의 대본, 실습지, 실행 예제와 범용 루브릭은 여기에서 관리한다.

학교 폴더에는 교재 복사본을 만들지 않는다. 학교·학기·분반·학사일정·평가 비율·LMS·성적처럼
그 강좌에만 해당하는 정보와, 이 공용 교재를 어떤 순서로 사용할지를 적은 매핑만 둔다.

## 온라인 교재 도서관

과목별 슬라이드는 [GitHub Pages 교재 도서관](https://gbox3d.github.io/teaching_repo/)에서 열람할 수 있다.

## 로컬 빌드

Node.js 24 환경에서 의존성을 설치하고 정적 사이트를 생성·검사한다.

```bash
npm ci
npm run build
npm test
```

생성 결과는 `dist/`에 저장된다.

## 읽는 순서

1. 이 문서에서 공용 교재와 학교 운영자료의 경계를 확인한다.
2. 실습실을 준비할 때 [`environment_baseline_template.md`](environment_baseline_template.md)를 학기용으로 복사해 버전을 확정한다.
3. 비전공 실습조교는 공통 [`설치 프로그램 목록`](ta_lab_setup_guide.md)을 확인한다.
4. 이어서 아래 [실습조교 설치 목록](#실습조교-설치-목록)에서 담당 과목 파일을 확인한다.
5. 과목별 내용은 아래 [교재 색인](#교재-색인)에서 연다.
6. 실제 수업 일정과 평가 방식은 강의자 공지를 따른다.

## 교재 색인

| 교재 | 기준 문서 | 현재 내용 |
|---|---|---|
| 모바일프로그래밍 | [`android_programming/README.md`](android_programming/README.md) | Android·Kotlin·XML View·BLE·ESP32-C3, 15주 자료 |
| 웹프로그래밍 | [`web_programming/README.md`](web_programming/README.md) | Git·HTML·CSS·JavaScript·GitHub Pages·Supabase, 15주 자료와 특강 |
| 오픈소스 AI 응용 | [`open_source_ai/README.md`](open_source_ai/README.md) | Python 격리환경·Ollama·Hugging Face·RAG·PEFT/LoRA 교재 제작 계획 |
| 과목 공통 자산 | [`_shared/README.md`](_shared/README.md) | 공통 템플릿과 재사용 모듈의 승격 기준 |

Java, 프로그래밍기초, AR/VR, Unreal 과목은 아직 공용 교재가 없다. 실제 교재 원고가 생길 때 이 색인에 추가한다.

## 실습조교 설치 목록

공통 목록을 먼저 보고 담당 과목에 필요한 프로그램만 설치한다.

| 범위 | 설치 목록 | 주요 프로그램 |
|---|---|---|
| 모든 과목 공통 | [`ta_lab_setup_guide.md`](ta_lab_setup_guide.md) | Git, VS Code, 브라우저 |
| 모바일프로그래밍 | [`android_programming/ta_setup_guide.md`](android_programming/ta_setup_guide.md) | Android Studio, SDK, Emulator |
| 웹프로그래밍 | [`web_programming/ta_setup_guide.md`](web_programming/ta_setup_guide.md) | Git, VS Code, Node.js, 브라우저 |
| 오픈소스 AI 응용 | [`open_source_ai/ta_setup_guide.md`](open_source_ai/ta_setup_guide.md) | Git, VS Code, uv, Ollama |

과목 안내서의 `TBD` 항목은 미비점이 아니라 교수 승인이 필요한 값이다. 조교가 임의 버전이나 장치 규약을 정하지 않는다.

## 공용 교재와 학교 운영자료의 경계

| 공용 교재에 둔다 | 학교 강좌 폴더에 둔다 |
|---|---|
| 개념 설명, 범용 슬라이드와 강의 대본 | 학교명, 과목코드, 분반, 강의실 |
| 재사용 가능한 실습지·starter·예제 | 학사일정, 휴강·보강, 실제 주차 배치 |
| 기술적으로 중립인 확인문제·루브릭 틀 | 평가 비율, 실제 시험문제, 마감과 제출 파일명 |
| 공식 참고자료, 버전·라이선스 기록 | 학교 내부 시스템(LMS 등) 사용법과 자동화 |
| 공통 설치 프로그램 목록 | 학생 제출물, 출석, 성적, CQI, 개인정보 |

학교 이름을 슬라이드에 직접 넣지 않는다. 학교별 표지나 공지는 배포본 생성 단계에서 덧붙인다.
LMS 업로드용 복사본은 배포 산출물이며 교재 정본으로 다시 편집하지 않는다.

## 편집 원칙

- 하나의 내용을 여러 과목에 복사하기 전에 `_shared/`로 승격할 수 있는지 확인한다.
- 두 과목에서 실제로 같은 학습목표와 설명을 사용할 때만 공통 모듈로 만든다.
- 과목별 학습 흐름이 다르면 억지로 합치지 않고 서로 링크한다.
- 학생용 starter와 교수자용 solution을 물리적으로 분리한다.
- 실제 비밀번호, 토큰, 학생정보와 학교 운영 데이터는 이 디렉터리에 넣지 않는다.
- 설치 버전은 교재 본문에 임의로 고정하지 않고 학기별 환경 기준표에서 확정한다.
- 공용 자산을 변경하면 이를 사용하는 각 강좌 운영 문서와의 호환 여부를 확인한다.

## 라이선스

이 저장소는 오픈소스가 아닙니다. 수업 수강과 개인 학습 목적의 열람·클론·로컬 실행만
허용되며, 무단 재배포·전재·상업적 이용을 금지합니다. 자세한 내용은 [LICENSE](LICENSE)를
확인하세요.
