# HTTP 홈 IoT 연구 예제

## 목차

- [실행](#실행)
- [기초 비교 예제](#기초-비교-예제)
- [자동 제어 연구](#자동-제어-연구)
- [코드 연결](#코드-연결)
- [기록과 제공 서버](#기록과-제공-서버)

## 실행

특강 폴더 home_iot_http에서 node examples/simulator/server.mjs를 실행하고 http://localhost:8014/를 연다.
Node는 시뮬레이터의 HTTP API와 화면을 함께 제공한다. HTML을 더블클릭하거나 정적 서버만 실행하면 제어 API가 없다.

## 기초 비교 예제

| 파일 | 관찰할 동작 | 변경 변수 |
|---|---|---|
| [ex01/index.html](ex01/index.html) · [app.js](ex01/app.js) | GET으로 상태 객체 읽기 | 표시할 응답 필드 |
| [ex02/index.html](ex02/index.html) · [app.js](ex02/app.js) | PATCH로 전등 변경 | 밝기 20·65·90, 오류 값 101 |
| [ex03/index.html](ex03/index.html) · [app.js](ex03/app.js) | GET→온도 비교→팬 PATCH | 기준 온도 28·30 |
| [student/index.html](student/index.html) · [app.js](student/app.js) | 직접 구현하는 기초 제어 | TODO의 밝기 40%, 기준 27°C |
| [reference/index.html](reference/index.html) · [app.js](reference/app.js) | 기초 코드 실행 참고본 | 밝기 65%, 기준 28°C |

온도 슬라이더를 바꾼 뒤 온도 적용을 눌러야 서버 상태가 바뀐다. 기초 예제의 제어는 버튼을 누를 때 한 번 실행된다.

## 자동 제어 연구

| 파일 | 역할 |
|---|---|
| [automatic/index.html](automatic/index.html) | 단일 기준·히스테리시스, 간격 설정, 시작·중지, 기록 다운로드 |
| [automatic/policy.js](automatic/policy.js) | 온도와 현재 상태로 다음 팬 상태 결정 |
| [automatic/runner.js](automatic/runner.js) | GET·필요한 PATCH·완료 후 다음 검사, 실패 복구 |
| [automatic_student/index.html](automatic_student/index.html) | 학생 정책 실행 화면 |
| [automatic_student/policy.js](automatic_student/policy.js) | 단일 기준·상한/하한·상태 유지 TODO |

학생 화면은 제공 runner.js를 공유한다. 정책부터 구현하고 동작을 확인한 뒤 실행기의 중복 요청 방지·중지·재시도 코드를 분석한다.
자동 제어 탭은 하나만 시작한다. 여러 탭이 동시에 제어하면 서로의 정책이 상태를 덮어쓰므로 비교 실험 조건이 달라진다.

## 코드 연결

| 단계 | 입력 | 판단·처리 | 출력 |
|---|---|---|---|
| ex01 | GET 응답 | 객체 필드 읽기 | 온도·장치 상태 표시 |
| ex02 | 버튼과 밝기 값 | JSON 본문 작성 | 전등 PATCH |
| ex03 | 현재 온도 | 기준 이상인지 비교 | 팬 PATCH |
| 자동 정책 | 온도·현재 팬 상태·설정 | decideFan() | 다음 상태 true/false |
| 자동 실행기 | 정책 결과 | 현재 상태와 다르면 요청 | PATCH 또는 상태 유지 |
| 실패 처리 | 네트워크 실패·3초 제한 | 대기 증가, 최대 10초 | 다음 GET 재시도 |

자동 제어의 설정 간격은 요청 시작 간격이 아니라 검사 완료 후 대기 시간이다. GET이나 PATCH가 느려져도 같은 실행기 안에서 요청을 겹쳐 보내지 않는다.

## 기록과 제공 서버

대시보드는 최근 PATCH 12건만 기록한다. 자동 제어 화면은 최근 관찰 30건, JSON 다운로드는 최근 500건이다. 새로고침 전에 기록을 저장한다. GET 간격과 실패는 Network에서도 확인한다.
서버 재시작 시 장치·온도 상태가 초기화된다. 팬이 온도를 낮추는 물리 모델은 없으며 온도는 수동 입력이다.

- simulator/server.mjs: 상태·HTTP API·화면 파일 제공.
- simulator/public/: 기존 가상 거실 대시보드.
- simulator/server.test.mjs: API·접근 제한·UI 문구·자동 정책·요청 예약 시험.
- simulator/check_ui_copy.mjs: 화면 문구 검사기의 재사용 부분.

검증 명령: node --test examples/simulator/server.test.mjs (현재 폴더: home_iot_http)
