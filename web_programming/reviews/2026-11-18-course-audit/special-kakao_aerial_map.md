# Kakao 지도·Canvas 특강 조사·검증

기존 23개와 추가 5개, 총 28개 공개 파일을 읽고 정규 14주 이후의 선택 연구 수업으로 연결했다. 완성 편집기 전체를 정규 90분 차시의 구현 과제로 편입하지 않는다.

## 수정

- 00_connection·01_relay_checks 폴더에 README와 `.http`를 추가했다. 서버의 GET /api/about·/api/help에서 시작하고 403·400·405를 비교한 뒤 완성 앱으로 이동한다.
- 서버 정보·설정 요청을 GET 전용으로 제한했다. 기존 SDK·relay 허용 범위와 Canvas 기능은 유지했다.
- 화면의 설명 문단은 문서로 옮기고, 긴 작업 기록이 모바일 패널을 밀지 않도록 보완했다.
- 실행 경로의 오래된 teaching_materials 접두어를 제거했다. Node.js 24·전용 서버·키 없는 로컬 이미지 실습과 GitHub Pages 제한을 명시했다.
- 공개 workspace 필드 protectedWidth/Height와 문서의 attributionWidth/Height 혼동을 수정했다. undo가 텍스트·그리기만 취소한다는 설명을 추가했다.
- 한영 슬라이드 각 30장을 유지했다. 서버가 검사하는 Host·요청 문맥 헤더를 브라우저 검증 목록에서 서버 목록으로 옮겼다.
- 기존 지도 자동 시험 25개를 루트 npm test에 포함했다.

## 검증

[Chrome 실행 기록](evidence/map-browser.json), [375px 화면](evidence/map-375.png).

실제 임시 Node 서버에서 `.http` 원문 6개 요청의 200·403·400·405를 확인했다. about/help/config에 POST를 보내 405를 확인했다. 실제 설정 대신 키 없는 테스트 환경 값을 사용했으며 저장소 config.json은 읽지 않았다.

Chrome에서 키 누락·SDK 연결 실패, 로컬 PNG 읽기, 문구·undo, 회전·밝기·초기화, 자유 그리기, PNG/JPEG 다운로드, 잘못된 파일의 이전 이미지 보존을 실행했다. 공개 API의 보호 명령 3개·미등록 명령 거부, AI actor 기록, Blob·Data URL, 이미지 읽기가 진행 중 선을 확정하지 않는 동작도 확인했다. 375/1280px와 80자 기록에서 가로 넘침이 없었다.

CanvasEditor에 합성 PNG를 넣고 회전 45도·밝기 50·대비 150·문구를 적용한 뒤, 좌하단 80×32 표지 픽셀과 240×160 출력 크기가 유지됨을 확인했다. 기존 자동 시험 25개, JS 구문 9개와 한국어 UI·문서 검사가 통과했다.

실제 Kakao 키·주소 검색·지도 이미지 전달·GPS 승인은 실행하지 않았다. 외부 지도 서비스와 계정의 실사용 검증은 강의 전 확인 사항이다. 자동 시험의 모의 지도 결과와 로컬 Canvas 결과를 실제 Kakao 연결 성공으로 취급하지 않는다.

2026-11-18 공식 [Web SDK StaticMap 문서](https://apis.map.kakao.com/web/documentation/)의 mapTypeId·SKYVIEW 예제와 [REST 정적 지도 문서](https://developers.kakao.com/docs/ko/kakaomap/rest-api)의 인증·이미지 응답·파라미터 목록을 다시 확인했다. REST 목록에는 SKYVIEW 선택 파라미터가 없다는 설명을 유지했다.

## 파일 목록

- 루트: README.md, lab.md, slides.md, slides_en.md
- examples: README.md
- 00_connection·01_relay_checks: README.md, requests.http 각 2개
- app: README.md, index.html, styles.css, config.example.json, package.json, server.mjs, static-map-relay.mjs
- app/js: main.js, map.js, static-map.js, image-loader.js, collaboration-bridge.js, editor-core.js, canvas-editor.js
- app/tests: collaboration-bridge.test.mjs, editor-core.test.mjs, map.test.mjs, static-map.test.mjs, static-map-relay.test.mjs

최종 덱 렌더·통합 링크·독립 심사는 총괄 검증에 포함한다.
