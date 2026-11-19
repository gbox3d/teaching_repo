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

기준일은 2026-11-18이다. 아래 내용은 마지막 커밋 `5f701e7`에 커밋 안 된 변경(21시 기준 수정 450, 삭제 27, 새 파일 358. 새 파일은 `git status --porcelain`의 새 항목 221개를 `-uall`로 펼쳐 센 수)과 같은 날 만든 에이전트 지침을 더한 작업 트리 기준이다. 커밋된 상태와 다른 부분은 "미커밋"으로 표시했다. 커밋 여부는 사용자가 정한다(`plan.md`의 미커밋 변경 처리).

- 대상 플랫폼: 공개 수업교재 저장소(GitHub `gbox3d/teaching_repo`) + GitHub Pages 슬라이드 도서관
- 사이트: 58개 덱, 한글·영문 각 1,175장(Android 20개·378장, 웹 21개·371장, 오픈소스 AI 17개·426장). 같은 작업 트리에서 `npm run build`와 `npm test`(사이트 검사, 슬라이드 맞춤 시험, 웹 실습 시험)가 통과했다. 커밋된 상태만으로는 57개 덱·1,157장(웹 20개·353장)이고, 웹 hash SPA 특강 18장이 미커밋이다.
- 메인 엔트리포인트: `README.md`(교재 색인), `scripts/render-site.mjs`(빌드), `scripts/check-site.mjs`(검증), `site/catalog.json`(덱 목록)
- 비공개 짝 저장소: `univ_scoring_works/teaching_materials_private/`(강의 대본·실습 해답·평가 자료)

| 과목 | 지금 구조 | 미커밋 |
|---|---|---|
| 모바일프로그래밍(Android) | 1~3주 `StudentCard`, 4~10주 SmartIO, 11~15주 새 앱 RoomControl을 PC 시뮬레이터 WlEno와 AAR(`wleno-android-0.1.0.aar`)로 수업한다(커밋 `738c81f`). 옛 11~15주(연락처·BLE 보드)는 `specials/legacy_week11~15`의 보존 특강 1~5다 | WlEno 2.0.0에 맞춘 문서(`python main.py`, 연결·해제 때 상태 유지)와 11~15주 예제의 주소 오류 표시 지우기 |
| 웹프로그래밍 | 15주 방명록 확장(10주 배열, 11주 객체·JSON 저장, 12주 GET, 13주 POST, 14주 PATCH·DELETE, 15주 기말 실기). 커밋된 특강은 배열 심화, 지도, Supabase 방명록, 신시사이저, HTTP 홈 IoT 다섯 개다 | C01 전체 개편: 일반 27차시를 강의·시연 60분+실습 30분으로 통일, 12~14주 설정 패널 `shared/api-settings.js`, 15주 문제은행 재구성, hash SPA 특강 신설(특강 6개), 개편 기록 `reviews/2026-11-18-course-audit/` |
| 오픈소스 AI 응용 | 15주. 10~15주는 시뮬레이터 제어, 초소형 툴 호출 모델, 제어 LoRA, Streamlit 제어 화면, 챗봇 과제와 AI 성능 평가로 바뀌었다(커밋 `0b2048c`, `29a667a`). 사이트 특강은 `huggingface_hub`·`pytorch_basics`이고, 옛 10~13주 원고는 `specials/project_delivery/`(사이트 미등록)에 보존했다 | 10~13주 문서와 `materials_plan.md` 32개 파일을 WlEno 2.0.0에 맞춤 |
| 공용 도구 | `tools/wleno`(LAN 시뮬레이터, Android AAR 프로젝트), `tools/bleuno-control`(제어·평가 패키지), `tools/github-classroom-pc-reset` | `tools/wleno`를 모듈 7개·시험 35개·REST Client 예제로 다시 작성(2.0.0, `sim.py`·uv 설정 삭제), `tools/bleuno-control`의 프롬프트·설명 수정 |

검증하지 않은 것은 다음과 같다. 웹은 공용 PATCH·DELETE 권한과 예제의 Pages 실배포를 확인하지 않았다. Android는 새 11~15주 예제 빌드, AAR 재빌드, 실기기·학교 Wi-Fi 연결을 확인하지 않았다. 오픈소스 AI는 실습실 Windows·GPU에서 모델·학습 실행을 재현하지 않았다. 세 과목 모두 비공개 짝 저장소의 대본·해답을 새 구조에 맞췄는지 확인하지 않았다.

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
