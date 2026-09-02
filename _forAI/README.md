# _forAI Guide

## 목차

- [한 줄 요약](#한-줄-요약)
- [읽는 순서](#읽는-순서)
- [문서 역할](#문서-역할)
- [현재 스냅샷](#현재-스냅샷)
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

## 현재 스냅샷

- 확인일: `2026-09-02`
- 저장소 경로: `C:\works\coworks\teaching_repo`
- 대상 플랫폼: 공개 수업교재 저장소(GitHub `gbox3d/teaching_repo`) + GitHub Pages 슬라이드 도서관
- 교재: 모바일프로그래밍 15주, 웹프로그래밍 15주·특강 1, 오픈소스 AI 응용 15주
- 메인 엔트리포인트: `README.md`(교재 색인), `scripts/render-site.mjs`(빌드), `scripts/check-site.mjs`(검증), `site/catalog.json`(덱 목록)
- 비공개 짝 저장소: `C:\works\coworks\univ_scoring_works\teaching_materials_private\`(강의 대본·실습 해답)

## 유지 규칙

- 계획이 아닌 참고 정보는 `plan.md`가 아니라 `memo.md`에 둔다.
- 저장소 구조나 실행 명령이 바뀌면 `inventory.md`를 먼저 갱신한다.
- 작업 이력은 날짜를 붙여 `dev_log.md`에만 남긴다.
- 새 작업을 시작할 때는 `inventory.md`와 `memo.md`를 먼저 읽고, 실제 할 일은 `plan.md`에서 확인한다.
- 모든 문서에는 제목 바로 아래에 `## 목차` 섹션을 둔다.
- 사용자 동의 없이 git commit을 하지 않는다.
- 사용자 동의 없이 `_forAI/` 문서를 수정하지 않는다.
