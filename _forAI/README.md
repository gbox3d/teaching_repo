# _forAI Guide

## 목차

- [한 줄 요약](#한-줄-요약)
- [읽는 순서](#읽는-순서)
- [에이전트 지침 위치](#에이전트-지침-위치)
- [문서 역할](#문서-역할)
- [현재 스냅샷](#현재-스냅샷)
- [강의 영상 작업](#강의-영상-작업)
- [유지 규칙](#유지-규칙)

## 한 줄 요약

이 디렉터리는 `teaching_repo` 작업을 이어받을 때 필요한 AI 작업 문맥을 정리해 두는 곳이다.

## 읽는 순서

이 폴더를 읽기 전에 저장소 루트의 [`AGENTS.md`](../AGENTS.md)를 먼저 읽는다. 과목 폴더 안의 일을 맡으면 그 과목의 `AGENTS.md`도 읽는다.

1. `README.md`
2. `inventory.md`
3. `memo.md`
4. `dev_log.md`
5. `plan.md`

## 에이전트 지침 위치

| 파일 | 내용 |
|---|---|
| [`AGENTS.md`](../AGENTS.md) | 저장소 지도, 공개 저장소 규칙, 사이트 빌드·검증, 여러 에이전트로 작업하는 방식(독립 검증 루브릭) |
| [`android_programming/AGENTS.md`](../android_programming/AGENTS.md) | Android 과목, `tools/wleno`, `tools/bleuno-control`의 범위·함께 고칠 곳·검증 |
| [`web_programming/AGENTS.md`](../web_programming/AGENTS.md) | 웹 과목의 범위·예제 작성 규칙·함께 고칠 곳·검증·결정 사항 |
| [`open_source_ai/AGENTS.md`](../open_source_ai/AGENTS.md) | 오픈소스 AI 과목의 수업·예제 규칙·함께 고칠 곳·검증 |
| 같은 폴더의 `CLAUDE.md` | `@AGENTS.md` 한 줄. Claude Code가 그 폴더의 `AGENTS.md`를 읽게 한다 |

## 문서 역할

- `inventory.md`: 저장소에 실제로 있는 구조, 엔트리포인트, 빌드/검증 명령을 기록한다.
- `plan.md`: 앞으로 진행할 개발 계획과 우선순위만 기록한다.
- `memo.md`: 프로토콜, 핀맵, 기본값, 디버깅 교훈 같은 참고 메모를 모은다.
- `dev_log.md`: 날짜별 작업 이력과 `_forAI` 정리 내역을 남긴다.
- `lecture-video.md`: 강의 편집·게시 작업의 재사용 스킬, 로컬 산출물, 단계별 완료 근거를 찾는 진입점이다.

## 현재 스냅샷

기준일은 2026-11-28이고 커밋 `d0ad054`(main, `origin/main`과 같다) 기준이다. `8cc49ea` 뒤에 다른 세션이 2026-11-24~25에 커밋 7개를 올렸다(웹 12·13주 개편, 오픈소스 AI 특강 `chatbot_rag_finetune`, `wleno` PyPI 배포). 목록은 `dev_log.md`에 있다.

- 대상 플랫폼: 공개 수업교재 저장소(GitHub `gbox3d/teaching_repo`) + GitHub Pages 슬라이드 도서관
- 사이트: 60개 덱, 한글·영문 각 1,219장(Android 20개·378장, 웹 21개·376장, 오픈소스 AI 19개·465장). `d0ad054`의 Pages 워크플로(`npm ci` → 빌드 → `npm test` → 배포)가 성공했다. 이 HEAD에서 로컬 빌드는 다시 돌리지 않았다. `f246e24`에서 특강 `chatbot_rag_finetune`(33장)이 더해졌고, 웹은 `e513180`에서 12주 덱이 1장 늘었다.
- 메인 엔트리포인트: `README.md`(교재 색인), `scripts/render-site.mjs`(빌드), `scripts/check-site.mjs`(검증), `site/catalog.json`(덱 목록)
- 비공개 짝 저장소: `univ_scoring_works/teaching_materials_private/`(강의 대본·실습 해답·평가 자료)

| 과목 | 지금 구조 | 2026-11-19 이후 변경 |
|---|---|---|
| 모바일프로그래밍(Android) | 1~3주 `StudentCard`, 4~10주 SmartIO, 11~15주 새 앱 RoomControl을 PC 시뮬레이터 WlEno와 AAR(`wleno-android-0.1.0.aar`)로 수업한다(커밋 `738c81f`). 옛 11~15주(연락처·BLE 보드)는 `specials/legacy_week11~15`의 보존 특강 1~5다 | WlEno 2.0.0에 맞춘 문서(`python main.py`, 연결·해제 때 상태 유지)와 11~15주 예제의 주소 오류 표시 지우기(`543ab2e`) |
| 웹프로그래밍 | 15주 방명록 확장(10주 배열, 11주 객체·JSON 저장, 12주 타이머와 공개 API GET, 13주 방명록 CRUD, 14주 수정·삭제 결과 확인, 15주 기말 실기). 특강은 배열 심화, 지도, Supabase 방명록, 신시사이저, HTTP 홈 IoT, hash SPA 여섯 개다. 13주는 Git 제외 `config.json`에서 주소·공개 키·`BOOK_ID`를 읽는다. 12주 선택 방명록·14·15주·hash SPA 04·Supabase 특강은 `config.example.js`(주소·`BOOK_ID`)를 읽고 공개 키를 처음 열 때 묻는 창으로 받아 localStorage에 둔다. 편집 키는 없어졌고 공용 공개 키로 모든 태그의 글을 수정·삭제할 수 있다 | C01 개편(`393c757`), W3.CSS 예제와 12·13주 실습 정리(`b1d2aa4`), 검토 기록 Git 제외(`116c8e8`). 설정 패널 삭제와 공개 키 localStorage·**공개 키 지우기**, 12주 타이머 예제 `ex01b`~`ex01d`(`8cc49ea`). 12주 공개 API(환율·타로·공휴일)와 13주 `week13_guestbook_crud`, 편집 키 폐지(`bd02eaa`). 12주 선택 예제 `ex07` 도시별 기온과 슬라이드의 전체 요청 주소(`e513180`) |
| 오픈소스 AI 응용 | 15주. 10~15주는 시뮬레이터 제어, 초소형 툴 호출 모델, 제어 LoRA, Streamlit 제어 화면, 챗봇 과제와 AI 성능 평가로 바뀌었다(커밋 `0b2048c`, `29a667a`). 사이트 특강은 `huggingface_hub`·`pytorch_basics`·`chatbot_rag_finetune`·`reasoning_tips`이고, 옛 10~13주 원고는 `specials/project_delivery/`(사이트 미등록)에 보존했다 | 10~13주 문서를 WlEno 2.0.0에 맞춤(`543ab2e`). 7주 GGUF 확인(`da9403b`), 기말 챗봇 평가셋 v1.1(`3b61866`), 9주 Streamlit 실행·빈 답변 처리(`9d42398`, `97aa3cd`), 추론 원문 관찰 복습 특강(`f5d0dc1`). 기말 챗봇 개선 특강(평가·RAG·LoRA·추론 버그, `f246e24`). 10주는 PyPI의 `wleno`를 `uv sync --locked`로 설치하고 학생용 ZIP을 릴리스에 올림(`378745a`, `b821770`, `d0ad054`) |
| 공용 도구 | `tools/wleno`(LAN 시뮬레이터 2.0.0, Android AAR 프로젝트), `tools/bleuno-control`(제어·평가 패키지), `tools/pyproject.toml`(두 폴더를 묶은 PyPI 패키지 `wleno` 0.1.0), `tools/github-classroom-pc-reset` | `tools/wleno`를 모듈 7개·시험 35개·REST Client 예제로 다시 작성(`sim.py`·uv 설정 삭제), `tools/bleuno-control`의 프롬프트·설명 수정(`543ab2e`). `wleno` 패키지와 PyPI 게시 워크플로(`b3f25da`). 릴리스 `wleno-v0.1.0`과 PyPI 게시 성공(2026-11-25) |

검증하지 않은 것은 다음과 같다. 웹은 공용 Supabase에 `enable-public-crud.sql`이 적용됐는지, 공개 키만으로 PATCH·DELETE가 되는지, Pages 화면에서의 조회를 확인하지 않았다. 13주 `config.json` 흐름의 브라우저 확인 기록도 이 저장소에 없다. Android는 새 11~15주 예제 빌드, AAR 재빌드, 실기기·학교 Wi-Fi 연결을 확인하지 않았다. 오픈소스 AI는 실습실 Windows·GPU에서 모델·학습 실행과 10주 ZIP의 PyPI 설치를 재현하지 않았다. 세 과목 모두 비공개 짝 저장소의 대본·해답을 새 구조에 맞췄는지 확인하지 않았다.

이전 통합 검증 기준(2026-11-14, 51개 덱·한글·영문 각 1,069장)과 과거 작업 로그의 장 수는 해당 시점 기록으로 보존한다.

## 강의 영상 작업

[강의 영상 인수인계](lecture-video.md)에서 시작한다. 재사용 절차와 검사기는 `myAISkills`의 `lecture-video-editing` 스킬이 정본이다. 영상과 LMS 증거는 공개 Git에 포함되지 않으며, 기존 작업 재개는 로컬 상태·최신 검증 보고서와 실제 산출물을 대조한다. 그 문서가 가리키는 Android 11주 예제는 2026-11-18 개편으로 `android_programming/specials/legacy_week11_content_provider/`로 옮겨졌다(`plan.md`의 공용 작업 참고).

## 유지 규칙

- 계획이 아닌 참고 정보는 `plan.md`가 아니라 `memo.md`에 둔다.
- 저장소 구조나 실행 명령이 바뀌면 `inventory.md`를 먼저 갱신한다.
- 작업 이력은 날짜를 붙여 `dev_log.md`에만 남긴다.
- 새 작업을 시작할 때는 `inventory.md`와 `memo.md`를 먼저 읽고, 실제 할 일은 `plan.md`에서 확인한다. `dev_log.md` 최신 날짜 이후의 `git log`와 `git status`도 본다.
- 과목 전용 규칙은 과목 `AGENTS.md`에, 저장소 공통 작업 규칙은 루트 `AGENTS.md`에 둔다. `_forAI`에는 같은 규칙을 다시 적지 않고 링크한다.
- `_forAI` 문서에 작업 PC의 절대 경로, 서버·장비 주소와 호스트 이름, 키 값을 쓰지 않는다.
- 모든 문서에는 제목 바로 아래에 `## 목차` 섹션을 둔다.
- 사용자 동의 없이 git commit을 하지 않는다.
- 사용자 동의 없이 `_forAI/` 문서를 수정하지 않는다.
