# Supabase 특강 조사·검증

총괄이 공개 교재 65개 파일을 확인했다. Supabase 구축은 강의자 실습부터 시작하는 분량 제한 없는 특강으로 유지한다. 정규 12~14주는 준비된 API를 호출하며 계정·SQL·편집 키 발급을 학생 필수 과제로 넣지 않는다.

## 수정

- 01 about → 02 help → 03 GET → 04 POST → 05 편집 → 06 HTTP 실험 → 07 완성 방명록의 폴더 구성을 유지했다. 각 폴더에 README를 추가하고 화면의 긴 설명을 옮겼다.
- 일곱 화면을 W3.CSS cdnjs 4.1.0과 폴더별 shared/examples.css로 정리했다. 기존 styles.css 경로는 import 호환 파일로 남겼다. 입력·버튼·결과와 짧은 상태만 화면에 둔다.
- 브라우저 config.example.js, REST Client .env, 정규 수업의 실행 중 설정 패널을 구분했다. walkthrough의 오래된 정규 수업 config.example.js 안내를 고쳤다.
- 한영 슬라이드 각 16장을 유지했다. HTTP/HTTPS·GitHub Pages·공개 키와 편집 키·태그 필터와 인증의 차이는 기존 설명을 보존했다.

## 실행 검증

[실행 기록](evidence/supabase-browser.json), [375px 완성 화면](evidence/supabase-375.png).

| 대상 | 실제 확인 |
|---|---|
| requests.http 7개 | 원문 27요청을 파싱하여 임시 API에 실행. about/help/GET/PATCH 200, POST 201, DELETE 204, 키 누락 401 |
| 01·02 | 안내 객체와 도움말 6개, Offline 실패 후 버튼 복구 |
| 03 | 정상 목록과 비어 있는 태그 |
| 04 | 등록·조회, HTML 모양 문자열의 텍스트 표시 |
| 05 | 선택·잘못된 키로 변경 불가·정상 수정·정상 삭제·키 입력 삭제·GET 재확인 |
| 06 | POST 201, 보호된 id 수정 400, 잘못된 JSON 안내 |
| 07 | 세 글 등록, 가운데 글 수정·삭제, 이웃 글 유지, 잘못된 키로 삭제 불가, Offline 시 입력 보존·조회 복구 |
| 전체 화면 7개 | Chrome 375/1280px, CDN 실제 로드, 가로 넘침·처리되지 않은 예외 없음 |

브라우저 테스트에서는 config.example.js 응답만 임시 로컬 API로 대체했다. 클라우드 쓰기 요청은 차단했다. 기존 HTTP 실험 자동 시험 5개와 한국어 UI·문서 검사가 통과했다. 공개 Supabase 서버의 실제 읽기는 [공통 읽기 기록](live-browser-read.json)에 분리했다.

VS Code 확장 UI 조작, 실제 Supabase 쓰기, GitHub Pages 업로드와 학생 실습 시간은 확인하지 않았다. 최종 덱 렌더·링크·독립 심사는 통합 단계에 포함한다.

## 전수 파일 목록

- 루트 5개: README.md, lab.md, walkthrough.md, slides.md, slides_en.md
- examples/README.md
- 일곱 폴더 각 8개: README.md, index.html, app.js, config.example.js, .env.example, requests.http, styles.css, shared/examples.css
- 06_http_lab 추가 3개: request.js, exercise.js, request.test.mjs

localfiles와 실제 .env는 공개 교재 목록에서 제외했다. 실제 편집 키나 DB 비밀번호를 읽거나 보고서에 기록하지 않았다.

