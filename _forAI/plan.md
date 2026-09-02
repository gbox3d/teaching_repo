# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- 오픈소스 AI 응용 15주 초판(2026-09-02 작성)을 기준 PC(RTX 4070)에서 재현 검증해 개강 최소 2주 전 배포 가능 상태로 만든다.

## Near-term work

1. `environment_baseline_template.md`의 「오픈소스 AI 응용」 절 값(uv·Python·Ollama·PyTorch·CUDA·모델 ID·양자화·캐시 경로)을 담당 교수가 확정한다.
2. 기준 PC에서 각 주차 `examples/` uv 프로젝트의 `uv lock`을 생성해 커밋하고, 4·6·7·10·11·12주차 README의 실행시간·VRAM 기록 칸을 실측값으로 채운다.
3. 8주차 실기평가 비공개 패킷(문항·fixture·정답·채점 testcase)과 15주차 기말 검증 패킷을 `teaching_materials_private/open_source_ai/`에 작성한다.
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

- 모델 태그 변동: `qwen3:4b`, `bge-m3`, `Qwen/Qwen2.5-0.5B-Instruct` 등은 교재 작성 시점 기준이며 라이브러리에서 이름이 바뀌거나 사라질 수 있다. 환경 기준표에서 확정하고 예제는 환경변수로만 바꾼다.
- `transformers`·`peft`·`trl` API 변동: 10주차 LoRA 학습 스크립트는 `Trainer` 기반으로 썼으나 메이저 버전 변화에 취약하다. lock 확정 후 재실행 검증이 필요하다.
- Ollama `think` 옵션은 특정 버전 이상에서만 동작한다. 기준표의 Ollama 버전으로 확인한다.
- RTX 4070 실측(10주차 학습 시간·VRAM, 7주차 임베딩 시간)이 아직 없다. 30분 실습 분량 판단이 실측 후 바뀔 수 있다.
- 사이트 검증 스크립트의 슬라이드 수 고정 검사는 원고 수정마다 상수 갱신을 요구한다.
