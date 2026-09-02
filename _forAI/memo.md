# Memo

## 목차

- [제품 기준선](#제품-기준선)
- [기본 설정값](#기본-설정값)
- [런타임 구조 메모](#런타임-구조-메모)
- [동작 규칙](#동작-규칙)
- [반복 금지](#반복-금지)

## 제품 기준선

- 빌드 환경: Node.js 24, `@marp-team/marp-core` 4.4.0(`package-lock.json` 고정). GitHub Actions `pages.yml`이 main push마다 build → check → Pages 배포.
- 배포 주소: <https://gbox3d.github.io/teaching_repo/>
- 줄바꿈: `.gitattributes`로 전 파일 LF. Windows에서 파일을 만들 때 CRLF·BOM이 섞이지 않게 한다.
- 실습 기준 PC(오픈소스 AI): Windows + RTX 4070(12 GB). GPU 없는 PC용 CPU·소형 모델 대체 경로를 항상 둔다.

## 기본 설정값

오픈소스 AI 응용 예제의 환경변수 기본값(교재 검증용, 실제 값은 환경 기준표가 확정):

| 환경변수 | 기본값 |
|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` |
| `OLLAMA_MODEL` | `qwen3:4b` (CPU 대체 `qwen3:0.6b`) |
| `OLLAMA_EMBED_MODEL` | `bge-m3` |
| `HF_TEXT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` |

Qwen3 계열은 thinking 출력이 섞이므로 Ollama API 호출에 `"think": false`를 넣는다.

수업 시간 구조:

| 과목 | 구조 |
|---|---|
| 모바일·웹 | 주 2회 × 90분, 매회 설명·시연 30분 + 실습 60분 |
| 오픈소스 AI | 60분 블록 × 3(1·2·3교시), 매 블록 설명·시연 20분 + 실습 30분 + 휴식 10분. 분반에 따라 2+1 또는 1+2로 이틀 배치 |

## 런타임 구조 메모

- `site/catalog.json`이 덱 목록의 단일 기준이다. 새 과목·주차를 공개하려면 (1) `catalog.json`에 chapter 추가, (2) `render-site.mjs`·`check-site.mjs`의 `sourcePath`에 폴더 매핑, (3) 두 스크립트의 `EXPECTED_*` 상수 갱신 순서로 한다.
- 슬라이드 수는 렌더된 HTML의 `<svg data-marpit-svg>` 개수로 센다. 원고의 `---` 줄 수와 다를 수 있으니(frontmatter 구분자 포함) 최종 값은 `npm run build` 출력으로 확정한다.
- `render-site.mjs`는 원고의 `<br>`(줄 끝)을 Markdown 줄바꿈 `\`로, `<code>`를 백틱으로 바꾼 뒤 남은 raw HTML이 있으면 빌드를 실패시킨다.
- 상대 `.md` 링크는 GitHub blob URL로 재작성되므로 원고에서 `lab.md#앵커` 링크를 써도 된다. 앵커 규칙은 GitHub 스타일(공백→`-`, 특수문자 제거, `—`가 빠지면 `--`가 남는다).

## 동작 규칙

- 공용 교재에 학교명·분반·학수번호·실제 날짜·성적 비율·LMS 이름을 넣지 않는다. 루브릭은 100점 상대 배점만 둔다.
- 소프트웨어 정확 버전을 본문에 고정하지 않는다. 버전은 `environment_baseline_template.md`를 학기용으로 복사해 확정한다.
- 전역 `pip install`을 쓰지 않는다. Python 예제는 uv 프로젝트(`pyproject.toml`, 의존성 버전 미고정)이며 `uv.lock`은 기준 PC에서 생성해 커밋한다.
- 비밀은 `.env.example`만 제공한다. 학생용 starter와 강의자용 해답을 물리적으로 분리한다.
- 모델 다운로드는 실습 시간에 하지 않는다(사전 캐시).
- 강의 대본(`lecture_script.md`)과 해답(`lab_solution.md`)은 `univ_scoring_works/teaching_materials_private/`에 둔다. 대본의 구간 제목·분 범위는 공개 `slides.md`와 같아야 한다.

## 반복 금지

- 슬라이드를 고친 뒤 `EXPECTED_SLIDES`를 안 고쳐 CI가 깨지는 일. 빌드 출력의 장 수로 두 스크립트를 함께 갱신한다.
- 다른 과목 표현("1일차", "90분", "30분 설명")을 오픈소스 AI 자료에 복사해 오는 일. 오픈소스 AI는 "교시", "20분·30분·10분"이다.
- 강의 대본을 공개 저장소에 커밋하는 일.
- `materials_plan.md` 초안의 `materials/` 챕터 구조를 되살리는 일. 주차 폴더 구조로 확정했다.
- 존재하지 않는 CLI 명령 이름(예: 버전에 따라 바뀐 Hugging Face 캐시 명령)을 본문에 고정하는 일. Python API로 쓰거나 `--help`로 확인하라고 안내한다.
