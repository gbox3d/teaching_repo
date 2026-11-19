# 웹프로그래밍 전체 교재 개편 기록

## 진행 상태

기획자 9명의 제안 중 C01을 평균 9.10/10으로 선정했다. 정규 15주와 특강 6개를 개편한 기준본은 총괄 9.0·학습 8.9·기술 9.3점으로 통과했다. 7주 타임라인 완성 뒤 해당 단원과 8~10주 인계, 15주 시험 자료를 다시 심사해 총괄 9.0·학습 8.9·기술 9.6점을 받았다.

- [최종 결과와 검증 범위](final.md)
- [요구와 공통 심사 기준](brief.md)
- [작업 계획](plan.md)
- [총괄 디렉터의 인계·시간·SPA 검증 기준](director.md)
- [파일별 조사 목록](inventory.json)
- [20:46 작업 폴더 파일 목록과 해시](inventory-final.json) · [후속 심사 시점까지의 변경 목록](evidence/followup-changes.json)
- [9개 안의 점수와 선정 결과](winner.md)
- [구현 작업 지시서](implementation.md)

## 독립 제안서

| 안 | 판단의 중심 | 제안서 |
|---|---|---|
| C01 | 정규 진행 보존과 실습·평가 정합 | [C01](proposal-C01.md) |
| C02 | 9주차의 작은 SPA 전환 | [C02](proposal-C02.md) |
| C03 | 10주 배열·목록과 SPA 비교 | [C03](proposal-C03.md) |
| C04 | 11주 저장·메모리 상태와 SPA 비교 | [C04](proposal-C04.md) |
| C05 | 12~13주 REST와 SPA 비교 | [C05](proposal-C05.md) |
| C06 | 14주 CRUD 통합과 SPA 비교 | [C06](proposal-C06.md) |
| C07 | 정규 기초와 방학 연구 연결 | [C07](proposal-C07.md) |
| C08 | 프로젝트 수행평가와 재현 절차 | [C08](proposal-C08.md) |
| C09 | 학생 작성 능력과 선수 지식 재배치 | [C09](proposal-C09.md) |

모든 안에는 15주 30차시 구성, 학생 수정 범위, 주차 인계, SPA 판단, 평가와 검증 계획이 있다. 세 독립 심사자의 평가는 별도로 기록한다.

## 선정 전 점검

정규 15주와 특강 5개에는 641개 파일이 있고 공통 문서·도구까지 657개다. 조사 보고서는 이 수에서 제외한다. 원고와 예제의 기능 검증은 선정안에 따라 주차별 담당자가 수행한다.

| 점검 | 결과 | 한계 |
|---|---|---|
| [구문·로컬 파일 연결](baseline-checks.json) | JavaScript 173개 구문 통과, HTML 로컬 자산 누락 없음 | 동작이나 수업 내용의 정합성을 보증하지 않음 |
| [브라우저 초기 표시](baseline-browser.json) | HTML 160개 로딩, 처리되지 않은 JS 예외 없음 | 외부 API는 빈 배열로 모의 응답, CDN 외 외부 요청 차단. 실제 API·상호작용 검증 아님 |
| 작은 화면 | 14개 화면에서 375px보다 큰 문서 폭 관찰 | 4주 반응형 비교처럼 의도된 차이와 실제 결함을 담당자가 구분 |
| [방명록 인계](baseline-handoffs.json) | 7·9~14주 방명록 CDN 유지 | SPA 합치기에는 10주 이후 count ID와 전역 변수의 충돌 검토 필요 |

기획안의 시간표는 교재와 코드에 근거한 추정이다. 실제 학생 집단의 수행 시간을 측정한 결과로 표시하지 않는다.

## 담당자별 구현·실행 기록

| 단원 | 보고서 | 단원 | 보고서 |
|---|---|---|---|
| 1주 웹·Git | [1주](week01.md) | 9주 README·발표 | [9주](week09.md) |
| 2주 GitHub·Pages | [2주](week02.md) | 10주 배열·목록 | [10주](week10.md) |
| 3주 HTML | [3주](week03.md) | 11주 객체·저장 | [11주](week11.md) |
| 4주 CSS | [4주](week04.md) | 12주 GET | [12주](week12.md) |
| 5주 JavaScript | [5주](week05.md) | 13주 POST | [13주](week13.md) |
| 6주 DOM·이벤트 | [6주](week06.md) | 14주 PATCH·DELETE | [14주](week14.md) |
| 7주 W3.CSS | [7주](week07.md) | 15주 기말 | [15주](week15.md) |
| 8주 중간 실기 | [8주](week08.md) | 공통 자료·도구·빌드 | [통합 기록](common.md) |

| 특강 | 보고서 |
|---|---|
| 배열 심화 | [조사·검증](special-array_advanced.md) |
| hash SPA | [조사·검증](special-hash_spa.md) |
| Supabase API 구축 | [조사·검증](special-supabase_guestbook.md) |
| HTTP 홈 IoT | [조사·검증](special-home_iot_http.md) |
| Kakao 지도·Canvas | [조사·검증](special-kakao_aerial_map.md) |
| 신시사이저 | [조사·검증](special-synthesizer.md) |

초기 목록은 rg 기준 657개였으며 최종 목록은 Git의 공개 추적·미추적 파일을 기준으로 한다. `.gitignore`·`.env.example` 같은 공개 설정 견본까지 포함하고 실제 .env·localfiles·조사 보고서는 제외한다. 파일별 해시는 최종 검증 대상으로 사용한 소스를 구분하기 위한 값이다.
