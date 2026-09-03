# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- 오픈소스 AI 응용 15주 초판(2026-09-02~03 작성, 문서·링크·코드 자동 검증 통과)을 기준 PC(RTX 4070)에서 재현 검증해 개강 최소 2주 전 배포 가능 상태로 만든다.

## Near-term work

1. 실습실 PC에 설치할 프로그램 버전(Python·uv·Ollama·PyTorch)과 수업에 쓸 모델 이름을 `environment_baseline_template.md`의 TBD 칸에 적는다. 교재는 `qwen3:8b` 등 기본값으로 이미 동작하므로, 바꿀 이유가 없으면 기본값을 그대로 적으면 된다.
2. RTX 4070이 있는 PC에서 각 주차 `examples/`를 한 번씩 실행한다. 그러면 `uv.lock`이 생기고(커밋한다), 학습 시간·VRAM·토큰 속도처럼 교재가 빈칸으로 둔 숫자를 채울 수 있다. Ollama가 없는 PC에서는 순수 Python 예제만 실행해 확인했다.
3. 8주차 실기평가 패킷(문항·fixture·정답·감독 체크), 15주차 기말·발표 패킷, 챕터 퀴즈 은행은 `teaching_materials_private/open_source_ai/`에 있다. 시행 전에 강의자가 한 번 읽고 값을 바꿀지 정한다.
4. 강의 대본 15개를 낭독 리허설해 20분 분량을 조정한다(구간을 바꾸면 `slides.md`도 같이).
5. `npm run build && npm test`가 통과한 상태로 main에 반영해 GitHub Pages에서 오픈소스 AI 덱 15개가 열리는지 확인한다.
6. `_shared/` 승격 후보 검토: Git 세 영역·PR 흐름(웹 1·2주차 ↔ 오픈소스 AI 2주차), 비밀정보·릴리스 점검(웹 13주차 ↔ 오픈소스 AI 13·14주차).
7. 학교 폴더 `univ_scoring_works/wku/subjects/opensw/materials.md`에 주차↔공용 모듈 매핑과 실제 배점·마감을 연결한다.

## Structure decisions

- 오픈소스 AI 응용은 `materials/` 챕터 구조 대신 다른 과목과 같은 `weeks/weekNN_slug/` 구조를 쓴다.
- 수업 시간 구조는 60분 블록 × 3(설명 20 + 실습 30 + 휴식 10)이며 자료는 "교시" 단위로 쓴다. 분반별 요일 배치는 학교 문서가 정한다.
- 강의 대본·해답은 비공개 짝 저장소에 같은 주차 폴더 이름으로 둔다.
- 평가 문서 파일명: 종합과제 `assignment_brief.md`·`assignment_rubric.md`(4·8·12·15주차), 실기 `exam_structure.md`·`exam_rubric.md`(8주차), 제안 `proposal_template.md`·`proposal_rubric.md`(9주차), 기말·발표 `final_review_rubric.md`·`presentation_rubric.md`(15주차).
- 예제 코드의 모델·서버는 환경변수 + 기본값으로 읽는다. 기본값 표는 `open_source_ai/weeks/README.md`가 단일 기준이다.

## Risks

- 모델 태그 변동: `qwen3:8b`, `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct` 등은 교재 작성 시점 기준이며 제공자가 같은 태그를 다른 빌드로 옮길 수 있다. 실제로 `qwen3:4b`가 생각 전용 빌드로 바뀌어 기본값을 `qwen3:8b`로 교체했다. 환경 기준표에서 확정하고 예제는 환경변수로만 바꾼다.
- `transformers`·`peft`·`trl` API 변동: 10주차 LoRA 학습 스크립트는 `Trainer` 기반으로 썼으나 메이저 버전 변화에 취약하다. lock 확정 후 재실행 검증이 필요하다.
- Ollama `think` 옵션은 특정 버전 이상에서만 동작한다. 기준표의 Ollama 버전으로 확인한다.
- RTX 4070 실측(10주차 학습 시간·VRAM, 7주차 임베딩 시간)이 아직 없다. 30분 실습 분량 판단이 실측 후 바뀔 수 있다.
- 사이트 검증 스크립트의 슬라이드 수 고정 검사는 원고 수정마다 상수 갱신을 요구한다.
