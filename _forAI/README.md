# _forAI Guide

## 목차

- [한 줄 요약](#한-줄-요약)
- [읽는 순서](#읽는-순서)
- [문서 역할](#문서-역할)
- [현재 스냅샷](#현재-스냅샷)
- [강의 영상 작업](#강의-영상-작업)
- [유지 규칙](#유지-규칙)

## 한 줄 요약

이 디렉터리는 `teaching_repo` 작업을 이어받을 때 필요한 AI 작업 문맥을 정리해 두는 곳이다.

## 읽는 순서

1. `README.md`
2. `inventory.md`
3. `memo.md`
4. `dev_log.md`
5. `plan.md`

## 문서 역할

- `inventory.md`: 저장소에 실제로 있는 구조, 엔트리포인트, 빌드/검증 명령을 기록한다.
- `plan.md`: 앞으로 진행할 개발 계획과 우선순위만 기록한다.
- `memo.md`: 프로토콜, 핀맵, 기본값, 디버깅 교훈 같은 참고 메모를 모은다.
- `dev_log.md`: 날짜별 작업 이력과 `_forAI` 정리 내역을 남긴다.
- `lecture-video.md`: 강의 편집·게시 작업의 재사용 스킬, 로컬 산출물, 단계별 완료 근거를 찾는 진입점이다.

## 현재 스냅샷

- 교재·사이트 통합 검증의 마지막 기준일: `2026-11-14`(아래 결과를 이번 문서 정리에서 다시 빌드한 것은 아님)
- 현재 저장소 위치는 `git rev-parse --show-toplevel`로 확인한다. 과거 `D:\works\coworks\teaching_repo` 경로를 다른 머신에 강제하지 않는다.
- 대상 플랫폼: 공개 수업교재 저장소(GitHub `gbox3d/teaching_repo`) + GitHub Pages 슬라이드 도서관
- 교재: 모바일프로그래밍 15주(12~15주 BLE 보드 수업 + `android_programming/iot_sim/`), 웹프로그래밍 15주와 지도·신시사이저·Supabase·홈 IoT 특강, 오픈소스 AI 응용 15주
- 웹 개편: 12주 GET, 13주 POST, 14주 PATCH·DELETE, 15주 누적 복습·개인 실기. 레포트는 정규 14주 검사와 분리해 별도 공지한다.
- 연구 특강: 방학 중 실습·비교 실험으로 운영하며 분량·회차·총시간을 제한하지 않는다. 홈 IoT는 Node.js HTTP 시뮬레이터로 학생 PC에서 실습한다.
- Supabase: 강의자가 만든 공용 API를 학생 계정 없이 호출한다. 특강 예제 01~07은 각각 독립 폴더이며 06은 요청 실험, 07은 완성 방명록이다.
- 검증 경계: 공용 about·help GET과 로컬 브라우저 조회, 방명록 GET·POST는 확인했다. 공용 PATCH·DELETE 권한과 예제의 GitHub Pages 실배포는 미검증이며 비공개 평가 자료의 전체 개편도 남아 있다.
- 메인 엔트리포인트: `README.md`(교재 색인), `scripts/render-site.mjs`(빌드), `scripts/check-site.mjs`(검증), `site/catalog.json`(덱 목록)
- 최종 통합 검증 기준: 51개 덱, 한글·영문 각각 1,069장(Android 304·웹 339·오픈소스 AI 426). 과거 작업 로그의 장 수는 해당 시점 기록으로 보존한다.
- 비공개 짝 저장소: `univ_scoring_works/teaching_materials_private/`(강의 대본·실습 해답; 실제 체크아웃 위치 확인)

## 강의 영상 작업

[강의 영상 인수인계](lecture-video.md)에서 시작한다. 재사용 절차와 검사기는 `myAISkills`의 `lecture-video-editing` 스킬이 정본이다. 영상과 LMS 증거는 공개 Git에 포함되지 않으며, 기존 작업 재개는 로컬 상태·최신 검증 보고서와 실제 산출물을 대조한다.

## 유지 규칙

- 계획이 아닌 참고 정보는 `plan.md`가 아니라 `memo.md`에 둔다.
- 저장소 구조나 실행 명령이 바뀌면 `inventory.md`를 먼저 갱신한다.
- 작업 이력은 날짜를 붙여 `dev_log.md`에만 남긴다.
- 새 작업을 시작할 때는 `inventory.md`와 `memo.md`를 먼저 읽고, 실제 할 일은 `plan.md`에서 확인한다.
- 모든 문서에는 제목 바로 아래에 `## 목차` 섹션을 둔다.
- 사용자 동의 없이 git commit을 하지 않는다.
- 사용자 동의 없이 `_forAI/` 문서를 수정하지 않는다.
