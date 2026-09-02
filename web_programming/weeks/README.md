# 주차별 강의 자료

## 운영 기준

- 15주, 주 2회 × 90분
- 매 수업: 설명·시연 30분 + 직접 해결 실습 60분
- 주당 합계: 이론·시연 60분 + 실습 120분
- 실습 순환: 문제 읽기 → 예상 → 구현 → 관찰 → 오류 설명 → 변형·확장
- 기본 문제를 먼저 완성하고 남는 시간에 확장 문제를 수행한다.

## 주차 폴더 구성

각 폴더는 같은 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 학습 목표, 1·2일차 흐름, 자료 안내, 완료 기준 |
| `slides.md` | Marp 호환 PT 원고. `---`가 슬라이드 구분자 |
| `lab.md` | 60분 실습 문제, 단계별 힌트, 검증, 확장 주제 |
| `examples/` | 브라우저에서 실행하거나 비교할 최소 예제와 starter |

PT 원고는 내용 변경 이력을 추적하기 위해 Markdown으로 관리한다. 필요할 때 Marp CLI 또는 VS Code Marp 확장으로 HTML, PDF, PPTX로 내보낼 수 있다.

## 주차 목록

| 주차 | 주제 | 폴더 |
|---:|---|---|
| 1 | 웹 실행 구조와 Git 상태 | [`week01_web_git`](week01_web_git/) |
| 2 | GitHub와 GitHub Pages | [`week02_github_pages`](week02_github_pages/) |
| 3 | 시맨틱 HTML과 form | [`week03_semantic_html`](week03_semantic_html/) |
| 4 | CSS와 반응형 UI | [`week04_responsive_css`](week04_responsive_css/) |
| 5 | JavaScript 데이터와 함수 | [`week05_javascript_data`](week05_javascript_data/) |
| 6 | DOM·event·브라우저 CRUD | [`week06_dom_crud`](week06_dom_crud/) |
| 7 | ES Module과 비동기 처리 | [`week07_async_modules`](week07_async_modules/) |
| 8 | 중간 개인 실기 | [`week08_midterm`](week08_midterm/) |
| 9 | 1차 과제와 풀스택 설계 | [`week09_architecture_project`](week09_architecture_project/) |
| 10 | Supabase 데이터 연결 | [`week10_supabase_data`](week10_supabase_data/) |
| 11 | Auth와 소유자 RLS | [`week11_auth_rls`](week11_auth_rls/) |
| 12 | 영속 CRUD와 관계 기능 | [`week12_persistent_crud`](week12_persistent_crud/) |
| 13 | 보안·접근성·릴리스 점검 | [`week13_release_security`](week13_release_security/) |
| 14 | 최종 프로젝트 발표 | [`week14_project_presentation`](week14_project_presentation/) |
| 15 | 기말 개인 실기 | [`week15_final_exam`](week15_final_exam/) |

## 자료 작성 원칙

- `slides.md`에는 60분 분량의 핵심 개념만 두고 긴 설명은 대본으로 분리한다.
- 예제는 한 번에 한 개념만 보여주는 최소 코드로 만든다.
- `lab.md`에는 정답 전체 대신 완료 조건, 관찰 항목과 단계별 힌트를 둔다.
- 모든 실습은 정상 경로와 최소 한 개의 실패·경계 경로를 확인한다.
- Supabase 예제는 publishable key만 사용하며 secret과 실제 계정 정보를 포함하지 않는다.
- 시험 폴더에는 문제 구조·starter·채점표만 두고 학기별 실제 문제와 정답은 별도 비공개 공간에서 관리한다.
