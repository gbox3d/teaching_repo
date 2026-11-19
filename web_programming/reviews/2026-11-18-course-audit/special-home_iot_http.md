# 홈 IoT 특강 조사·검증

총괄이 기존 27개 파일을 읽고 수정 후 45개 파일을 확인했다. 정규 12~14주 이후 방학 연구 수업으로 유지하며 분량·차시 상한과 정규 시험 편입은 없다. 실제 보드·계정 없이 Node.js 24 기본 모듈로 실행한다.

## 수정

- 첫 단계 `00_about_help`와 읽기 전용 `/api/about`·`/api/help`를 추가했다. GET 소개 객체·도움말 6개를 확인한 뒤 상태 읽기와 PATCH로 진행한다.
- 여덟 실습 폴더에 README와 `requests.http`를 두었다. `@baseUrl`, REST Client 설치·Send Request, 인증 키 불필요, PATCH JSON 헤더와 예상 상태를 설명했다.
- README·lab·walkthrough·한영 슬라이드와 대시보드 진입 링크에 첫 단계를 반영했다. 한영 26장씩을 유지한다.
- 학생 HTML의 긴 동작 설명은 문서로 옮겼다. 화면에는 장치·버튼·상태와 기록 보관 범위만 남겼다. 기존 공용 CSS와 가상 거실 그림을 유지한다.
- 학생 app.js와 policy.js의 TODO는 유지했다. 서버 기능·자동 실행기는 제공 코드다.

## 실행 검증

[Chrome·HTTP 실행 기록](evidence/iot-browser.json), [375px 대시보드](evidence/iot-375.png).

| 대상 | 실제 확인 |
|---|---|
| requests.http 8개 | 원문 49요청을 파싱해 임시 Node 서버로 실행. about/help/state/PATCH 200, 밝기 101은 400 |
| 00 접속 | 소개 version v1, 도움말 6개, Offline 실패 후 버튼 복구 |
| ex01 | 상태 조회와 온도 표시 |
| ex02 | 전등 켜기·끄기, 밝기 65 |
| ex03 | 27°C 정지·29°C 작동, 기준 28°C |
| student | 버튼 세 개의 TODO 안내, 서버 상태 변경 없음 |
| reference | 상태 읽기·밝기 65·팬 기준 28 |
| automatic_student | 미완성 정책의 안내·중지, 시작 버튼 복구 |
| automatic | 단일 기준 작동, 히스테리시스 29 작동→27 유지→26 정지, Offline 실패·중지·재개, 관찰 JSON 다운로드 |
| 실제 서버 재시작 | 실행 중 Node 서버 종료·같은 포트 재시작, 자동 조회 복구, 온도 24·팬 정지로 초기화, 정상 500ms 대기 복귀 |
| 전체 화면 9개 | 375/1280px 가로 넘침 없음, 처리되지 않은 JS 예외 없음 |

`node --test examples/simulator/server.test.mjs`의 15개 시험이 통과했다. 새 about/help의 GET 전용·상태 비변경과 기존 CRUD·검증·호스트 제한·12건 로그·요청 예약·지연 응답·재시도·중지·미완성 정책을 포함한다. 기본 실패 대기 4/8/10초는 기존 자동 시험으로 확인했고 브라우저에서는 짧은 간격으로 실패·복구를 확인했다. 모든 JS 구문 검사와 UI·문서 문체 검사도 통과했다.

VS Code 확장 UI를 직접 조작한 것은 아니며 요청 원문의 실행을 검증했다. 실제 하드웨어·냉각 성능·다른 PC를 검증했다고 표시하지 않는다. 최종 덱 렌더·통합 링크·독립 심사는 총괄 검증에서 수행한다.

## 전수 파일 목록

- 루트 5개: README.md, lab.md, walkthrough.md, slides.md, slides_en.md
- examples: README.md
- 00_about_help·ex01·ex02·ex03·student·reference 각 4개: index.html, app.js, README.md, requests.http
- automatic 5개: index.html, policy.js, runner.js, README.md, requests.http
- automatic_student 4개: index.html, policy.js, README.md, requests.http
- simulator 3개: server.mjs, server.test.mjs, check_ui_copy.mjs
- simulator/public 3개: index.html, app.js, styles.css
