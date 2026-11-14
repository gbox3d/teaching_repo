[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/specials/home_iot_http)

# HTTP 홈 IoT 시뮬레이터 연구 수업

Node.js로 가상 거실을 실행하고 브라우저의 fetch로 장치를 제어한다. 방학 중 학생들과 진행하는 연구 수업 자료이며, 수업 시간·차시 수·분량을 고정하지 않는다. 기초 요청부터 자동 제어와 통신 실패 복구까지 실험하고 결과를 기록한다.
실제 보드·센서·외부 계정 없이 학생 PC에서 실행한다. 정규 15주와 별도로 운영하며 정규 시험 범위에 넣지 않는다.

## 목차

- [학습 목표와 연구 단계](#학습-목표와-연구-단계)
- [준비와 실행](#준비와-실행)
- [화면과 상태](#화면과-상태)
- [HTTP API](#http-api)
- [관찰과 기록](#관찰과-기록)
- [수업 자료](#수업-자료)
- [도달 기준](#도달-기준)
- [운영 범위](#운영-범위)
- [공식 참고 자료](#공식-참고-자료)

## 학습 목표와 연구 단계

| 단계 | 다루는 내용 | 도달 기준 |
|---|---|---|
| 요청과 상태 | GET·PATCH, JSON, Network, 전등과 온도 | 요청 본문과 장치 상태의 관계를 설명한다 |
| 센서 기반 판단 | 온도 조회, 조건식, 선풍기 제어 | 같은 온도에서도 기준에 따라 동작이 달라짐을 확인한다 |
| 주기적 조회 | 완료 후 다음 요청 예약, 조회 간격 변경 | 요청이 겹치지 않는 것과 반응 지연을 관찰한다 |
| 제어 정책 비교 | 단일 기준과 26/29°C 히스테리시스 | 같은 입력 순서에서 상태 전환 횟수를 비교한다 |
| 통신 실패와 복구 | 서버 중단·재시작, 응답 제한, 재시도 대기 | 실패 중 요청 수와 복구 뒤 동작을 검증한다 |
| 후속 연구 | 기준 온도·조회 간격·입력 순서 변경 | 가설·변경 변수·관찰·해석과 한계를 기록한다 |

권장 선수학습은 정규 수업의 fetch·JSON·PATCH다. 기초 단계에서는 제공 예제를 따라 요청을 읽고 고친다. 자동 제어 단계에서는 정책 함수부터 직접 구현하고, 요청 예약과 실패 처리 코드를 차례로 분석한다.

## 준비와 실행

Node.js 24 이상, VS Code, Chrome이 필요하다. npm 패키지를 설치하지 않는다.
저장소를 내려받거나 강의자가 제공한 home_iot_http 폴더 전체를 준비한다. server.mjs만 따로 복사하면 화면과 예제가 없다.
현재 폴더: web_programming/specials/home_iot_http

```bash
node --version
node examples/simulator/server.mjs
```

브라우저에서 http://localhost:8014/를 연다. 대시보드의 링크로 기초 예제와 자동 제어 화면을 연다. 파일을 편집·저장한 뒤 해당 화면을 새로고침한다. 서버를 실행한 터미널은 그대로 둔다.
포트가 사용 중이면 명령 끝에 8015를 붙이고 브라우저 주소도 바꾼다. 종료는 터미널의 Ctrl+C다.

## 화면과 상태

| 주소 | 용도 |
|---|---|
| / | 가상 거실, 수동 제어, 모의 온도 설정, 최근 PATCH 기록 |
| /examples/ex01/ ~ ex03/ | 상태 읽기, 전등 제어, 버튼 한 번으로 온도 판단 |
| /examples/student/ | 기초 제어 함수 TODO 작성 |
| /examples/reference/ | 기초 요청을 연결한 실행 참고본 |
| /examples/automatic/ | 주기적 조회·단일 기준·히스테리시스·실패 복구 비교 |
| /examples/automatic_student/ | 자동 제어 정책 함수 TODO 작성 |

대시보드는 1초마다 GET으로 상태를 읽는다. 기초 예제는 버튼을 누를 때 한 번 요청한다.
자동 제어는 GET과 필요한 PATCH를 마친 뒤 다음 검사를 예약한다. 동시에 실행하는 자동 제어 화면은 하나로 제한해 서로 다른 정책이 장치를 덮어쓰지 않게 한다.

온도는 사용자가 슬라이더로 정하는 모의 값이다. 팬이 온도를 낮추는 물리 과정은 모델링하지 않는다. 따라서 이 자료로 냉각 성능이나 실제 실내 온도 안정성을 측정할 수는 없다.
상태와 서버 기록은 메모리에만 있으며 서버를 재시작하면 전등 꺼짐·밝기 60%·팬 정지·온도 24°C로 초기화된다.

## HTTP API

모든 주소는 현재 Node 서버 기준이다. PATCH의 헤더는 Content-Type: application/json이다.

| 메서드·주소 | 요청 본문 | 결과 |
|---|---|---|
| GET /api/state | 없음 | 전체 상태와 최근 제어 기록 |
| PATCH /api/devices/light | {"on":true,"brightness":40} | 전등 변경, 전체 상태 응답 |
| PATCH /api/devices/fan | {"on":true} | 팬 변경, 전체 상태 응답 |
| PATCH /api/environment | {"temperature":29} | 모의 온도 변경, 전체 상태 응답 |

전등은 on 또는 brightness 하나만 보내도 된다. 생략한 필드는 유지된다.
on은 불리언, brightness는 0~100 정수, temperature는 10~40 숫자다. 성공 응답은 200이다.
잘못된 값·JSON은 400, 없는 API는 404, 잘못된 메서드는 405, JSON이 아닌 본문은 415, 4096바이트를 넘는 본문은 413이다. 오류 응답은 error 필드에 안내 문장을 담는다.

## 관찰과 기록

대시보드는 최근 PATCH 12건만 보관하며 GET을 기록하지 않는다. 이 목록만으로 장시간 요청 수나 실패 횟수를 판단하지 않는다.
자동 제어 화면은 최근 관찰 30건을 표시하고 최근 500건을 JSON으로 다운로드한다. 새로고침 전에 저장한다. Network 탭의 Preserve log를 켜면 서버 중단과 복구 구간의 요청을 함께 볼 수 있다.

기록의 형식은 [연구 실습지](lab.md#연구-기록)에 있다. 화면·코드·Network 기록·관찰 JSON 중 주장을 뒷받침하는 자료를 남긴다. 캡처 수나 보고서 분량을 고정하지 않는다.

## 수업 자료

- [한글 슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- [연구 실습지](lab.md) · [따라하기](walkthrough.md)
- [예제 목록과 코드 연결](examples/README.md)
- [제공 서버](examples/simulator/server.mjs) · [자동 시험](examples/simulator/server.test.mjs)
- 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/home_iot_http/index.html

## 도달 기준

- HTTP 요청과 가상 장치의 상태 변화를 연결해 설명한다.
- 기초 제어 함수와 자동 제어 정책 함수를 직접 수정하고 결과를 확인한다.
- 같은 온도 순서에서 단일 기준과 히스테리시스의 상태 전환을 비교한다.
- 요청 완료 뒤 다음 검사를 예약하는 이유와 중지 동작을 설명한다.
- 서버 중단·복구 실험에서 실패 간격과 정상 간격의 차이를 관찰한다.
- 실제 온도 제어와 이 시뮬레이터의 차이를 연구 기록에 적는다.

이 자료의 실행 기준은 로컬 URL이다. GitHub Pages는 Node 서버를 실행하지 않는다.

## 운영 범위

서버는 127.0.0.1에만 연결하며 학생마다 독립된 상태로 실습한다. 외부 공개와 실제 가전 연결을 전제하지 않는다.
파일 준비와 Node 설치 뒤에는 인터넷 없이 실행할 수 있다. 연구 단계는 학생의 진행과 질문에 따라 반복하거나 확장한다.
검증 명령: node --test examples/simulator/server.test.mjs

## 공식 참고 자료

- [MDN: Fetch API](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [MDN: PATCH](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/PATCH)
- [MDN: 반복 조회와 재귀 setTimeout](https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval#ensure_that_execution_duration_is_shorter_than_interval_frequency)
- [MDN: AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
- [Node.js: HTTP](https://nodejs.org/api/http.html)
