# Inventory

## 목차

- [Repository](#repository)
- [Top-level structure](#top-level-structure)
- [Entrypoints and key modules](#entrypoints-and-key-modules)
- [Build and validation commands](#build-and-validation-commands)
- [Tests](#tests)
- [Notes](#notes)

## Repository

- Name: `teaching_repo`
- Path: `C:\works\coworks\teaching_repo`
- Summary: 대학·학기와 무관하게 재사용하는 공개 수업교재(모바일·웹·오픈소스 AI)의 단일 기준. Markdown 원고를 Marp로 렌더해 GitHub Pages 슬라이드 도서관으로 배포한다.

## Top-level structure

```text
teaching_repo/
├─ README.md                          교재 색인·편집 원칙·라이선스 안내
├─ environment_baseline_template.md   학기별 실습환경 기준표(복사용, TBD는 교수 승인값)
├─ ta_lab_setup_guide.md              실습조교 공통 설치 목록
├─ _shared/README.md                  과목 공통 자산 승격 기준(아직 내용 없음)
├─ android_programming/               모바일프로그래밍 15주 (weeks/weekNN_*/)
├─ web_programming/                   웹프로그래밍 15주 + specials/kakao_aerial_map
├─ open_source_ai/                    오픈소스 AI 응용 15주 (weeks/weekNN_*/)
│  ├─ README.md · materials_plan.md · ta_setup_guide.md
│  └─ weeks/README.md                 운영 기준(60분 블록 × 3)·주차 목록·검증용 기본값
├─ site/                              도서관 정적 자산(index.html, assets/, catalog.json)
├─ scripts/render-site.mjs            catalog.json → dist/ 렌더(Marp core)
├─ scripts/check-site.mjs             dist/ 검증(덱·슬라이드 수, 링크, 안전성)
├─ .github/workflows/pages.yml        main push 시 build → check → Pages 배포
├─ package.json                       Node 24, @marp-team/marp-core
├─ .gitattributes                     `* text=auto eol=lf`
└─ .gitignore                         config.json, .env, dist/, export/, node_modules/
```

주차 폴더 공통 구성: `README.md`, `slides.md`(Marp), `lab.md`, `examples/`. 웹·안드로이드 1주차와 오픈소스 AI 1·3·4·7·10·12주차에 `walkthrough.md`. 평가 문서(`exam_structure.md`, `rubric.md`, `project_brief.md`, `assignment_brief.md` 등)는 평가 주차에만 있다.

## Entrypoints and key modules

- 사람이 읽는 진입점: `README.md` → 과목 `README.md` → `weeks/README.md` → 주차 `README.md`
- 빌드 진입점: `scripts/render-site.mjs` — `site/catalog.json`의 `courses[].chapters[]`를 순회하며 `sourcePath(course, chapter)`로 원고 위치를 결정한다. course.id ↔ 폴더 매핑: `android`→`android_programming/weeks`, `web`→`web_programming/{weeks,specials}`, `open-source-ai`→`open_source_ai/weeks`.
- 검증 진입점: `scripts/check-site.mjs` — 같은 `sourcePath` 매핑과 `EXPECTED` 상수(과목별 덱·슬라이드 수)로 `dist/`를 대조한다.
- 도서관 UI: `site/index.html` + `site/assets/library.js`가 `catalog.json`을 읽어 카드 목록을 그린다. 덱 페이지는 `site/assets/deck.{css,js}`.
- 비공개 짝 저장소: `C:\works\coworks\univ_scoring_works\teaching_materials_private\` — 같은 주차 폴더 구조로 `lecture_script.md`, `lab_solution.md`, `_shared/practice_operation.md`(실습 운영 대본)를 둔다.

## Build and validation commands

```powershell
npm ci
npm run build     # node scripts/render-site.mjs → dist/
npm test          # node scripts/check-site.mjs
```

- Node.js 24 이상이 필요하다(스크립트가 검사).
- `render-site.mjs`와 `check-site.mjs`의 `EXPECTED_DECKS`, `EXPECTED_SLIDES`, `EXPECTED[course]`는 **정확한 수**를 고정 검사한다. 슬라이드를 추가·삭제하면 두 파일의 상수를 함께 갱신해야 빌드가 통과한다.
- 원고 검사 규칙: `theme: default`는 파일당 정확히 1회, raw HTML은 줄 끝 `<br>`·`<code>`·HTML 주석만 허용, 상대 `.md` 링크는 GitHub blob URL로, 상대 자산은 `dist/decks/<course>/<chapter>/assets/`로 복사된다.

## Tests

- 자동 테스트는 `npm test`(사이트 검증)뿐이다. 교재 코드 예제의 단위 테스트는 각 주차 `examples/`에 있는 것만 있으며(웹 5·특강, 오픈소스 AI 13주차), 저장소 수준 러너는 없다.
- 오픈소스 AI 예제는 Python 문법 검사(`uv run --no-project python -m py_compile`, 67개 파일)와 `ruff check --select E9,F63,F7,F82` 치명 오류 검사까지 했고, 모델·GPU 실행은 기준 PC 실측 대기 상태다.
- `ruff`를 저장소 전체에 돌릴 때는 `--exclude open_source_ai/weeks/week08_midterm/examples/mock_exam/broken_project`를 붙인다. 그 폴더의 `pyproject.toml`은 8주차 모의 실기용으로 **일부러 깨뜨린** 파일이라 TOML 파싱이 실패한다.
- 문서 검증용 임시 스크립트(링크·앵커 검사, 슬라이드·실습 시간 합계 검사)는 저장소에 두지 않았다. 필요하면 `_forAI/memo.md`의 검증 항목을 보고 다시 만든다.

## Notes

- 강의 대본·실습 해답은 이 저장소에 두지 않는다(비공개 짝 저장소). 주차 README의 "강의 대본: 강의자 별도 관리(비공개)" 문구가 그 표시다.
- 수업 시간 구조가 과목마다 다르다: 모바일·웹은 주 2회 × 90분(설명 30 + 실습 60), 오픈소스 AI는 60분 블록 × 3(설명 20 + 실습 30 + 휴식 10).
- 오픈소스 AI 예제는 uv 프로젝트이며 `uv.lock`을 아직 커밋하지 않았다(환경 기준표 확정 후 기준 PC에서 생성).
- `dist/`는 빌드 산출물로 추적하지 않는다. `site/`가 원본이다.
