# Dev Log

## 목차

- [Entries](#entries)

## Entries

### 2026-09-02 — 오픈소스 AI 응용 15주 교재 초판 작성

- 원광대 수업계획서의 15주 주제를 공용 청사진으로 옮겨 `open_source_ai/weeks/weekNN_slug/` 15개 폴더를 만들었다. 각 폴더에 `README.md`, `slides.md`(Marp), `lab.md`, `examples/`(uv 프로젝트·템플릿)를 두고, 1·3·4·7·10·12주차에 `walkthrough.md`, 4·8·9·12·15주차에 평가 문서를 추가했다.
- 수업 시간 구조를 60분 블록 × 3(설명·시연 20분 + 실습 30분 + 휴식 10분)으로 확정하고 `open_source_ai/weeks/README.md`에 운영 기준·주차 목록·검증용 환경변수 기본값을 기록했다.
- 강의 대본 `lecture_script.md`와 실습 해답 `lab_solution.md` 15세트를 비공개 짝 저장소 `univ_scoring_works/teaching_materials_private/open_source_ai/weeks/`에 작성하고, `_shared/practice_operation.md`에 「60분 블록 수업 보정」 절을 추가했다.
- `open_source_ai/README.md`를 진입점 형식으로 바꾸고 `materials_plan.md`의 폴더 구조·제작 단계 상태·다음 작업을 갱신했다. 루트 `README.md` 교재 색인 문구를 갱신했다.
- 사이트: `site/catalog.json`의 `open-source-ai`를 `published`로 바꾸고 15개 chapter를 등록했다. `scripts/render-site.mjs`·`check-site.mjs`에 `open-source-ai → open_source_ai/weeks` 매핑을 추가하고 덱·슬라이드 수 상수를 빌드 결과로 갱신했다.
- 검수: 주차별 기술·형식 검수와 교육적 정합성 검수를 거쳤고 Python 예제는 문법 검사(`py_compile`)와 ruff 치명 오류 검사를 통과했다. 모델·GPU 실행은 기준 PC 실측 대기.
- `_forAI/` 문서 세트를 실제 구조·명령·규칙으로 채웠다.

### 2026-09-03 — 15주 자료 마무리와 전체 정합성 검증

- 미완성 주차의 교재·예제를 채우고 슬라이드 원고를 15주 모두 같은 형식으로 맞췄다. 최종 규모는 285개 파일, Markdown 19,349줄, Python 8,017줄이다.
- 검증 결과: 슬라이드 분 범위가 교시마다 0–20분으로 연속하고(15주 × 3교시 × 7구간 = 315구간), 실습 시간표가 교시마다 0–30분으로 연속한다. 상대 링크와 앵커 178개 문서 전수 통과, 슬라이드 raw HTML 0건, `theme: default` 주차당 1회, Python 67개 파일 문법 오류 0건, ruff 치명 오류 0건이다.
- 루브릭 8종의 배점 합계가 모두 100점임을 확인했다. 12주차 과제 루브릭에 누락된 합계 행을 추가했다.
- 예제 폴더에 남은 실행 산출물(`.ruff_cache/`, `__pycache__/`, `outputs/`)을 제거하고 `HF_HOME` 예시 경로 표기를 통일했다.
- `materials_plan.md`의 남은 초안 문구를 정리했다. 콘텐츠 ID를 주차 폴더 이름으로 대체하고, 과제 표의 학교별 성적 비율(%)을 공용 교재가 제공하는 문서 링크로 바꿨다.
- 사이트: `site/catalog.json`의 오픈소스 AI 요약을 `15개 주차 · 407장`으로 확정했다. `npm run build`와 `npm test`가 46개 덱·923장으로 통과한다(모바일 228 + 웹 288 + 오픈소스 AI 407).
- 강의 대본 15종의 구간 제목과 분 범위가 같은 주차 `slides.md`와 정확히 일치함을 전수 확인했다.
