# 최종 학습 운영·문서 심사 — 8.9/10 통과

검토일은 2026-11-18이다. 심사자는 `final_judge_learning`이며 구현에 참여하지 않았다. 강의자가 정한 최종 기준 8/10 이상을 충족한다. 다른 최종 심사자의 점수·보고서는 읽지 않았으며, C01의 기획 점수 9.10을 구현 점수로 사용하지 않았다. 신시사이저 담당의 소스 동결과 최종 보고서 생성 뒤 판정했다. 교재 소스는 수정하지 않았다.

범위 주석: 7주차의 수업 분량·변환 전후 동작·7→9 파일 동일성 판단은 **2026-11-18 20:36:44 KST의 889개 파일 검사 기준본**에 한한다. 이후 20:41~20:43에 발견된 `ex03b_list` 4개 파일, 타임라인 방명록 및 관련 문서 변경은 출처 확인 중인 별도 변경으로 보존하며 이번 최종 점수에서 제외한다. 아래의 7주 관련 근거 링크는 현재 작업 파일을 가리키므로 기준본 이후 내용이 달라질 수 있다. 기존 **8.9/10**은 기준본을 평가한 점수이며, 이 추가 변경의 수업 분량·7→9 인계·현재 파일 전체의 정합을 보증하지 않는다.

## 판정과 점수

| 항목 | 배점 | 점수 | 판단 근거 |
|---|---:|---:|---|
| 수업 구성과 선수학습 연결 | 2 | 1.9 | 7주 W3.CSS 변환, 10주 배열, 11주 폼 저장, 12~14주 REST 확장이 실제 파일과 연결됨 |
| 90분 운영과 학생 작성량 | 2 | 1.7 | 일반 60+30, 시험·발표 예외, 제공 코드와 작은 수정 범위가 명시됨. 학생 집단의 수행 시간은 미실측 |
| 과제·문제은행·채점표 정합 | 2 | 1.8 | 중간·기말 각 20점, 기말 폼 한 객체와 REST 한 요청, 제공 기능 중복 채점 금지가 일치함 |
| 문서·예제·설정 설명의 일치 | 2 | 1.8 | 기본 저장부터 단계별 요청, 짧은 HTML, `.http`와 브라우저 설정 구분이 구현과 맞음 |
| 특강 분리와 연구 운영 | 2 | 1.7 | 6개 특강의 선수학습·실행 환경·기록·한계가 구분됨. 외부 서비스와 청취·학생 연구 시간은 별도 운영 확인 필요 |
| 합계 | 10 | **8.9** | **통과** |

정규 수업에 SPA·고급 배열·Supabase 구축을 억지로 추가하지 않고, 정규 과정에서 배운 기능을 특강에서 확장하도록 구성했다. 남은 확인은 교재 구현 실패와 구별한다. 특히 자동 실행 성공은 초보 학생의 제한 시간 내 완수를 입증하지 않는다.

## 조사 방식과 범위

[선정안](winner.md), [구현 지시](implementation.md), [공통 작업](common.md), 15개 주차 보고서와 6개 특강 보고서를 대조했다. 실제 주차 README의 목표·시간·필수 범위, lab의 분 단위 활동, walkthrough의 시작 파일·인계, 한영 슬라이드의 시간·제공·선택 안내, 시험 rubric과 시작 파일을 확인했다. 아래 표는 각 주차의 실제 원고 또는 코드 근거다.

담당자들의 전수 조사 기록과 별개로, 이 심사는 전체 파일 목록·문서 구조·HTML 문단·요청 파일을 조사하고 중요한 인계와 학생 활동을 직접 재현했다. 모든 889개 파일의 모든 행을 독립 심사자가 다시 읽었다거나 모든 예제를 다시 실행했다고 주장하지 않는다.

| 주차 | 직접 대조한 근거 | 학습 운영 판정 |
|---:|---|---|
| 1 | [README](../../weeks/week01_web_git/README.md), [실습](../../weeks/week01_web_git/lab.md) | 제공 HTML·CSS·JS에서 제목·문단을 바꾸고 Git 3회 기록. 두 차시 60+30이며 전체 코드 작성 요구가 없음 |
| 2 | [README](../../weeks/week02_github_pages/README.md), [실습](../../weeks/week02_github_pages/lab.md) | GitHub·Pages·브랜치가 실제 수업 목표라 수업 중 Git 작업을 허용함. 이후 주차의 사전 준비 규칙과 구별됨 |
| 3 | [README](../../weeks/week03_semantic_html/README.md) | 제공 HTML의 글·alt·목록·표 내용을 수정. form은 정적이며 브라우저 이메일 검사와 JS 처리를 혼동하지 않음 |
| 4 | [실습](../../weeks/week04_responsive_css/lab.md) | 비교 13개 전체를 과제로 삼지 않고 ex01·03·07·08과 CSS 지정 값만 수정. 고정 폭 비교 예제의 넘침을 완성본 오류와 구별함 |
| 5 | [README](../../weeks/week05_javascript_data/README.md), [시작 JS](../../weeks/week05_javascript_data/examples/day2/start/app.js) | 값 4곳·오류 1건, 조건·함수·출력 각 1곳. 출력·이벤트 틀은 제공함 |
| 6 | [README](../../weeks/week06_dom_events/README.md), [카운터 시작 파일](../../weeks/week06_dom_events/examples/day1/ex03/app.start.js), [홈 시작 파일](../../weeks/week06_dom_events/examples/day2/web-week06/app.start.js) | 1일차 6줄, 2일차 연결 3줄과 CSS 2값이라는 설명이 실제 시작 파일과 맞음 |
| 7 | [실습](../../weeks/week07_form_input/lab.md) 기준본 5·47·53행, [변환 전](../../weeks/week07_form_input/examples/day2/web-week07/guestbook.before.html), [변환 후](../../weeks/week07_form_input/examples/day2/web-week07/guestbook.html) | 기준본의 CDN·클래스 변환이 학생 과제이고 폼 JS는 제공. 기준본에서 변환 전후 동일 JS·동작과 수업 분량을 확인했으며 이후 ex03b·타임라인 변경은 제외함 |
| 8 | [README](../../weeks/week08_midterm/README.md), [채점표](../../weeks/week08_midterm/rubric.md) | 1일차 두 문항 30분, 2일차 안내 30+실기 60. A4+B4+C5+D3+E4=20이며 W3.CSS를 평가함 |
| 9 | [과제 안내](../../weeks/week09_readme_presentation/project_brief.md) 36·55~58행 | SVG 글자만 필수, 좌표·Mermaid는 선택. 5+75+10과 30명 상한, 31명 이상 영상·표본·개인 설명 운영이 명시됨 |
| 10 | [README](../../weeks/week10_array_list/README.md), [for 시작 화면](../../weeks/week10_array_list/examples/day1/ex02/start.html), [방명록 시작 화면](../../weeks/week10_array_list/examples/day2/web-week10/guestbook.start.html) | 일반 for·push·splice까지 필수. 전체 목록 생성·검증 코드는 제공하고 고급 배열은 특강으로 넘김 |
| 11 | [실습](../../weeks/week11_object_localstorage/lab.md) 44~85행, [ex06 JS](../../weeks/week11_object_localstorage/examples/day2/ex06/app.js) | ex04 문자열→ex05 JSON→ex06 폼 저장 순서. 저장·불러오기·지우기와 새로고침 후 수동 복원 확인. ex07만 참고로 남고 ex08 이후 없음 |
| 12 | [README](../../weeks/week12_fetch_json/README.md) 5·30·36·40행, [실습](../../weeks/week12_fetch_json/lab.md) | 11주 필수 결과와 제공 방명록을 구분. about→help→GET 이후 URL·JSON·showList 3곳만 연결. 로컬 보관본과 저장 키를 유지함 |
| 13 | [실습](../../weeks/week13_release_security/lab.md), [방명록 JS](../../weeks/week13_release_security/examples/day2/web-week13/guestbook.js) 55~98행 | `.http`의 message 수정 후 POST 201·GET 200 비교. 폼 값·본문·재조회 세 구역만 학생 수정이며 방어 코드는 제공함 |
| 14 | [실습](../../weeks/week14_project_presentation/lab.md), [방명록 JS](../../weeks/week14_project_presentation/examples/day2/web-week14/guestbook.js) | DELETE·PATCH 각 세 구역. 서버 ID와 배열 인덱스, 204·빈 PATCH 배열과 실제 변경을 구별하며 레포트 검사 없음 |
| 15 | [README](../../weeks/week15_final_exam/README.md), [채점표](../../weeks/week15_final_exam/rubric.md) 7~20행, [저장 시작 파일](../../weeks/week15_final_exam/examples/w11_local_storage/app.js), [REST 시작 파일](../../weeks/week15_final_exam/examples/w14_rest_edit/app.js) | A3+B3+C4+D2+E3+URL3+구술2=20. 저장은 폼 한 객체, 수정은 PATCH 또는 DELETE 한 요청. POST 중복 출제·제공 기능 중복 채점을 금지함 |

15주 전체에 README·lab·walkthrough·KO/EN 슬라이드·examples가 존재한다. 영문 슬라이드에서도 일반 60+30, 8주 30+60, 9주 5+75+10, 15주 시험 안내 30분을 확인했다. 11주·12주 인계와 15주 제공 코드 범위도 영어 원고에 반영되어 있다.

## 특강 6개 대조

| 특강과 실제 근거 | 판단 |
|---|---|
| [배열 심화](../../specials/array_advanced/README.md) | 10주 배열·11주 객체 이후 5개 폴더. 원본 변화·반환값·빈 배열·참조 비교를 다루며 정규 시험 제외 |
| [Hash SPA](../../specials/hash_spa/README.md) 3·38~42행 | 14주 이후 01 MPA→02 화면→03 hash→04 CRUD 통합. 전환 중 입력 보존과 새로고침 초기화를 구분하며 시간 상한 없음 |
| [Supabase](../../specials/supabase_guestbook/README.md) | 기존 공용 API 호출과 새 프로젝트 구축을 분리. 01 about→02 help→CRUD→07 완성본, `book_id`와 편집 권한, HTTP 화면·HTTPS API·Pages 역할 구분 |
| [홈 IoT](../../specials/home_iot_http/README.md) | Node 서버 8014와 Web UI에서 기초 요청·조건 제어·주기 조회·히스테리시스·통신 복구. 모의 온도이며 물리 냉각 성능 실험이 아님을 명시 |
| [Kakao 지도](../../specials/kakao_aerial_map/README.md) | 14주 이후 연구. 접속·help·relay 오류부터 시작하고 전용 Node 서버가 필요함. 110분은 도입 예이며 전체 상한이 아님 |
| [신시사이저](../../specials/synthesizer/README.md) 24·43~53행, [실습](../../specials/synthesizer/lab.md), [예제 안내](../../specials/synthesizer/examples/README.md) | 비교 10개, 연주기 실행 7개·조합기 포함 9개, 다른 score 스키마가 실제 파일과 일치. 정적 JSON GET과 REST를 구분하고 청취와 화면·예약 시각을 별도로 기록함 |

## 독립 확인 결과

실행 기준은 저장소 소스와 총괄이 실행한 `http://localhost:8111/`이다. 별도 Chrome headless 브라우저 컨텍스트를 사용했다. 공용 서버 쓰기나 배포는 수행하지 않았다.

| 직접 수행한 확인 | 결과 |
|---|---|
| 7→9 홈·소개·홈 JS·방명록 HTML/JS·CSS·프로필·보조 CSS의 SHA-256 | 기준본의 8개 모두 동일. 이후 7주 변경을 포함한 현재 파일의 동일성은 보증하지 않음 |
| 7주 ex04·ex05·완성본의 방명록 JS 비교 | 동일. 변환이 동작 변경 과제로 바뀌지 않음 |
| 10~14주 방명록의 W3.CSS·script 연결 | 고정 cdnjs 4.1.0 사용. 12~14는 제공 api-settings.js와 동작 guestbook.js |
| 11주 JS와 12주 guestbook.local.js 비교 | 줄끝 차이를 제외한 내용 동일. 보관본이 원래 저장 기능을 유지함 |
| 171개 HTML의 p/li 텍스트 자동 조사 | 160자를 넘는 문단 0개. 이 수치만으로 전체 문체 품질을 보증하지 않으며 실제 저장·방명록·SPA 화면도 확인함 |
| weeks·specials의 요청 파일 목록 | `.http` 39개. 정규 12~15주·REST 특강에 제공, 신시사이저는 정적 JSON GET 요청 |
| ex04 | 저장→새로고침→불러오기, 빈 문자열과 null, 삭제 통과 |
| ex05 | JSON 원문 2객체, 파싱 목록 2개, 삭제 후 빈 목록 통과 |
| ex06 | 새로고침 직후 빈 폼, 수동 복원, 저장 JSON, 자기 키 삭제와 다른 키 보존 통과 |
| 7주 변환 전·후와 9주 방명록 | 같은 입력 등록, `<b>문자</b>`를 태그 실행 없이 문자로 출력 |
| SPA 03 | 직접 hash 진입, 전환·뒤로·앞으로, 입력 보존, 새로고침 초기화, 미등록 경로 안내 통과 |
| 위 브라우저 7흐름 | 375px 문서 폭 유지, pageerror 0건 |
| 최종 보완된 11주 제공 방명록·12주 로컬 보관본 | setItem에 QuotaExceededError를 주입했을 때 실패 안내·입력 유지·목록 미증가, 정상 복구 후 한 행만 저장됨. 두 화면 모두 pageerror 0건 |

실행 명령은 `node %TEMP%/learning-slide-check.mjs`, `node %TEMP%/learning-handoff.mjs`, `node %TEMP%/learning-html-check.mjs`, `node %TEMP%/learning-browser.mjs`, `node %TEMP%/learning-storage-failure.mjs`다. PowerShell에서는 `%TEMP%` 대신 `$env:TEMP`로 실행했다. 브라우저 결과는 임시 `learning-browser.json`에 남겼으며 공개 교재에 시험 스크립트나 데이터를 추가하지 않았다. 마지막 저장 실패 보완 후 두 JS의 일치와 11주 walkthrough의 JS 전문 일치도 다시 확인했다. 이 보완은 제공 방어 코드에 한정되어 학생 필수 작성량을 늘리지 않는다.

[12주 ex01 요청](../../weeks/week12_fetch_json/examples/day1/ex01/requests.http)과 [안내](../../weeks/week12_fetch_json/examples/day1/ex01/README.md)를 대조했다. REST Client는 같은 폴더의 `.env`를 `{{$dotenv ...}}`로 읽고, 브라우저는 제공 설정 패널에서 메모리에 값을 적용한다. 한쪽이 다른 쪽 설정을 불러온다는 설명은 없다. `apikey`, Send Request, 200·빈 배열·401·404와 새로고침 후 설정 재입력까지 설명한다.

## 결함 등급과 남은 확인

- 차단: 없음. 수업 시작이나 필수 과제 수행을 막는 결함을 발견하지 못했다.
- 중대: 없음. 시험 범위·20점 합계·11→12 인계·특강 분리의 불일치를 발견하지 못했다.
- 경미 1건 발견·수정 완료: 12주 ex01 안내는 처음에 방명록 조회를 하지 않는다고 설명하면서 REST Client 3번에서 about→help→GET 모두 실행하도록 안내했다. 총괄이 about만 필수, help·방명록 GET은 후속 예제의 참고 요청으로 고쳤다. 최신 README 15행을 다시 읽어 수정 완료를 확인했다. 남은 문서 결함으로 계산하지 않는다.

학생의 30분 실습, 8분 시험 문항, Pages·인증 지연을 포함한 실제 분반 운영 시간은 실측하지 않았다. 9주 31명 이상 영상 채점과 15주 개인 구술에는 강의자·감독자의 추가 운영 시간이 필요하며 현재 자료가 이를 명시한다. 첫 운영에서 실제 소요 시간과 미완료 항목을 기록해 다음 분반의 필수 수정량을 조정하는 것이 적절하다.

공용 Supabase 쓰기, 새로운 Pages 게시, 다른 기기 공유, 실제 REST Client 확장의 Send Request UI, Kakao 실키 서비스, 신시사이저 청취는 이 심사에서 확인하지 않았다. 로컬 브라우저 실행과 이 결과를 같은 것으로 적지 않는다.

## 통합 증거의 구분

총괄의 [소스 검사](evidence/source-checks.json)는 20:36:44 KST 기준 889파일·199JS·171HTML·로컬 HTML 참조 462개·설정 사본 22개에서 실패 0건이다. 이후 발견된 7주 ex03b·타임라인 변경을 이 검사 결과에 포함하지 않는다. [전체 덱 실행 기록](evidence/deck-browser.json)과 [최종 변경 6덱 재검사](evidence/deck-browser-selected.json), 각 주차·특강 보고서를 참조했다. 전체 빌드 58덱·1175장/언어, 웹 42개 KO/EN 덱·742장 배치 검사, 자동 시험 54개 통과는 총괄의 실행 결과이며 이 심사자가 다시 실행한 결과로 표시하지 않는다.

교재 구현의 학습 운영·문서 기준은 통과다. 이 판정은 다른 최종 심사자의 독립 점수를 대체하지 않는다.
