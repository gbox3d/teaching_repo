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

### 2026-09-03 — 심층 검수와 기본 생성 모델 교체

- 주차별 심층 검수(사실 정확성·교육 정합성)에서 95건을 찾아 75건을 고쳤고, 주차 간 정합성에서 12건 중 8건을 고쳤다. 공식 문서 대조와 실제 실행으로 검증한 뒤 반박을 이겨낸 것만 반영했다.
- **기본 생성 모델을 `qwen3:4b`에서 `qwen3:8b`로 바꿨다.** Ollama 레지스트리에서 `qwen3:4b`의 model·template·params digest가 `qwen3:4b-thinking-2507-q4_K_M`과 동일함을 확인했다. 접미사 없는 이 태그는 생각 전용 빌드라 교재가 4주차에서 가르치는 `"think": false`가 동작하지 않는다. Qwen3에서 `0.6b`·`1.7b`·`8b`·`14b`·`32b`만 하이브리드이며 `4b`·`30b`·`235b`는 2507 갱신에서 instruct/thinking으로 갈렸다.
- 교체는 13개 주차의 공개·비공개 문서 106개 파일에 걸쳐 반영했다. 모델 크기(2.5 GB → 5.2 GB) 같은 확정값은 값으로, 실측치(tokens/s, VRAM 점유, 로드 시간)는 자리표시자와 "기준 PC 실측값으로 채운다" 안내로 바꿨다. 6·10주차는 Hugging Face 모델만 써서 대상이 아니었다.
- `weeks/README.md`에 「생성 모델 태그를 고를 때」 절을 추가했다. 하이브리드와 생각 전용 태그의 구분, 모델을 바꿀 때의 확인 절차를 기록했다.
- 13주차 예제 워크플로의 액션 버전을 올렸다(`actions/checkout@v5`, `astral-sh/setup-uv@v7`).
- 재검증: Python 67개 파일 문법 오류 0건, ruff 치명 오류 0건, 상대 링크·앵커 180개 문서 통과, 슬라이드 시간 배분과 실습 시간표 전 주차 통과, 루브릭 8종 합계 100점, `npm run build`·`npm test` 46개 덱·923장 통과.
- 검수 에이전트가 보고한 "저장소 파일이 CRLF"라는 관찰은 사실이 아니었다. `git ls-files --eol` 결과가 index·working tree 모두 `lf`이고 HEAD blob에 CR이 없다.
