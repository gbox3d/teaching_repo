# C02: 9주차에 두 화면 hash SPA로 전환한다

작성일: 2026-11-18. 강의자의 수업의 독립 기획안이다. 다른 기획안은 읽지 않았다. 이 문서는 설계 제안이며 코드·교재 구현 결과가 아니다.

## 결정 기록

**결정: 7주는 W3.CSS 변환, 8주는 중간 실기, 9주 1차시는 README 축약과 두 화면 hash SPA 전환으로 구성한다.**
- 근거: 6주에 함수·이벤트·classList를 배운다. 9주에는 그 문법으로 기존 DOM을 보이고 감출 수 있다. 배열·객체·비동기 호출을 라우터에 섞지 않고, 10~14주에는 같은 방명록 영역의 데이터 처리만 확장한다.
- 대안: 9주의 Markdown 11개 예제와 세 페이지 발표를 그대로 유지하고 SPA를 특강으로 옮긴다. 이 대안은 문서 학습량과 교재 수정량에서 유리하다.
- 손익: README의 SVG·Mermaid·인용·정렬표 실습을 선택으로 돌리는 대신 주소·화면·메모리의 관계를 반복해서 관찰한다. SPA 자체가 REST의 선수 지식은 아니며, 선택한 이유는 두 화면을 오가도 입력과 목록이 유지되는 경험이다.
- 재검토: 9주 30분 실습을 초보자 5명으로 리허설해 4명 이상이 25분 안에 필수 수정과 동작 확인을 끝내지 못하면, 학기 시작 전 SPA 도입을 철회한다. 그 경우 아래 인계의 index 내부 방명록 영역을 기존 guestbook.html로 되돌리고 9주는 축약 README·발표 연습으로 쓴다. 학기 중 두 버전으로 학생을 나누지 않는다.

7주 2차시에 SPA까지 넣는 안은 채택하지 않는다. 기존 시간표의 CDN 교체·클래스 적용·폼 확인 30분을 줄여야 하고, 폼 코드를 직접 구현하지 않은 학생에게 화면 전환까지 동시에 요구하기 때문이다. 8주에 새 범위를 넣으면 공개 문제은행과 평가 준비가 어긋난다. 10~14주에 라우터를 새로 만들지 않으며, 프레임워크·번들러·History API·동적 HTML 로딩·중첩 경로는 정규 범위에서 제외한다.

## 저장소에서 확인한 유지 사항과 수정 사유

| 근거 파일 | 확인한 사실 | C02의 처리 |
|---|---|---|
| [수업 기준](../../weeks/README.md), [예제 지침](../../AGENTS.md) | HTML→CSS→JS→DOM 순서, showList(), 고전 for, 7·11주 60분+30분을 명시한다 | 순서와 API 이름을 유지하고 시간 모델을 아래 25개 정규 차시에 적용한다 |
| [1주 lab](../../weeks/week01_web_git/lab.md), [2주 lab](../../weeks/week02_github_pages/lab.md), [3주 lab](../../weeks/week03_semantic_html/lab.md) | 로컬 기록, push·Pages·branch, 세 페이지와 form이 각각 60분 실습이다 | 시작 파일을 제공하고 독립 실습의 편집 항목을 줄인다. Git·Pages를 처음 쓰는 1·2주는 교사의 60분 안에 조작 시연과 재시도를 넣는다 |
| [4주 README](../../weeks/week04_responsive_css/README.md), [5주 lab](../../weeks/week05_javascript_data/lab.md), [6주 lab](../../weeks/week06_dom_events/lab.md) | CSS 13개, JS 10개, DOM 6개 비교 예제를 전부 고친 뒤 조립한다 | 예제는 보존하되 수업 중 학생 수정은 차시당 1~2개와 누적 파일로 줄인다. 나머지는 시연·선택으로 표시한다 |
| [7주 README](../../weeks/week07_form_input/README.md), [7주 lab](../../weeks/week07_form_input/lab.md), [제공 JS](../../weeks/week07_form_input/examples/day2/web-week07/guestbook.js) | CDN 4.1.0, class와 id 구분, 같은 JS로 변환, 빈값 안내·textContent·reset·focus가 이미 있다 | 현재 구조와 필수 과제를 유지한다. 폼 JS 재작성이나 배열·라우터는 요구하지 않는다 |
| [9주 README](../../weeks/week09_readme_presentation/README.md), [9주 lab](../../weeks/week09_readme_presentation/lab.md) | Markdown 11개와 SVG·Mermaid, 화면 두 장, README, 배포까지 1차시에 있다. 2차시 발표는 42분이다 | 제목·공개 링크·실행 방법·화면 한 장만 필수로 남긴다. 발표 2분은 유지하고 인원에 맞춰 운영한다 |
| [9주 home JS](../../weeks/week09_readme_presentation/examples/day2/web-week09/app.js), [10주 방명록 JS](../../weeks/week10_array_list/examples/day2/web-week10/guestbook.js), [12주 방명록 JS](../../weeks/week12_fetch_json/examples/day2/web-week12/guestbook.js) | home의 count·countBox·#count와 방명록의 식별자가 겹친다. 별도 페이지에서는 문제가 없다 | 한 문서에 합치기 전에 home-count·homeCount·homeCountBox로 강의자 시작본을 정리한다. 모듈·클래스로 해결하지 않는다 |
| [10주 README](../../weeks/week10_array_list/README.md), [10주 lab](../../weeks/week10_array_list/lab.md), [11주 README](../../weeks/week11_object_localstorage/README.md) | 10주는 다음 주에 배열 저장·전체 지우기를 조립한다고 하지만, 11주의 필수 결과는 ex06 폼 복원이다 | 10주의 예고·선택 과제 문구를 고친다. 11주 전체 방명록은 강의자 제공 인계본이라고 모든 자료에 명시한다 |
| [11주 방명록 JS](../../weeks/week11_object_localstorage/examples/day2/web-week11/guestbook.js) | 저장 키가 guestbook이고 초기 JSON.parse에 오류 처리가 없다 | 제공 인계본에는 주차·별칭을 포함한 키와 손상 JSON 안내를 넣는다. 학생 필수 구현으로 추가하지 않는다 |
| [12주 lab](../../weeks/week12_fetch_json/lab.md), [13주 lab](../../weeks/week13_release_security/lab.md), [14주 lab](../../weeks/week14_project_presentation/lab.md) | 12·13주는 6개 예제와 조립, 14주는 수정·삭제 실습이다 | 14주의 목적은 유지한다. REST 단계별 수정과 제공 오류 처리의 경계를 분리해 30분 실습으로 재편한다 |
| [12주 requests.http](../../weeks/week12_fetch_json/examples/day2/web-week12/requests.http), [API 안내](../../tools/guestbook-api/README.md) | 완성본의 .http는 about→help→조회 순서지만, 12주 차시 흐름은 JSON·GET부터 시작한다. 공용 PATCH·DELETE·Pages 검증은 미완료로 기록되어 있다 | 접속·도움말을 정규 첫 실습으로 올린다. 공용 검증을 수업 준비의 통과 조건으로 두고 현재 완료했다고 쓰지 않는다 |
| [중간 W3.CSS 문항](../../weeks/week08_midterm/examples/w07_form_line/README.md), [기말 은행](../../weeks/week15_final_exam/examples/README.md) | W3.CSS는 제공 JS를 유지하는 문제다. 기말은 A~E 다섯 영역이다 | 중간 범위를 유지한다. SPA 새 문항을 추가하지 않고 기말 저장 문항을 ex06 수준과 맞춘다 |

기존 9~12주 방명록 HTML에도 W3.CSS CDN과 w3-* 클래스가 있다. 전면적인 스타일 복구가 필요한 상태로 보지 않는다. 바뀌는 부분은 SPA의 공통 외곽, 중복 식별자, 시간표와 실제 인계 설명이다. 5주·10주 일부 기본 예제의 Console 전용 결과는 현재 예제 지침과 맞도록 입력·버튼·결과 칸을 추가하되, Console 관찰도 함께 남긴다.

## 30차시의 시간과 학생 수정 범위

정규 25차시는 매회 강의·시연 60분과 독립 실습 30분이다. 강의 60분에는 개념 설명, 강의자 실행·오류 시연, 학생의 결과 예측을 넣고 독립 구현 시간을 숨겨 넣지 않는다. 8·15주 네 차시는 시험 준비·평가, 9주 2차시는 발표이므로 예외다. 30×90분은 2,700분, 총 45시간이다.

1·2주 설치·계정 확인은 사전 30~45분 예상이며 준비된 실습실 PC를 대안으로 둔다. 3주부터 파일 내려받기·주차 폴더 준비는 수업 전 5~10분, push·Pages 확인은 수업 후 5~10분 예상이다. 새 기능 구현을 숙제로 넘기지 않는다. 준비가 안 된 학생에게는 동일한 시작 ZIP을 제공한다. 게시 지연은 로컬 결과로 먼저 인정하고 다음 수업 시작에 공개 주소를 확인한다.

| 주·차시 | 목표·강의 및 시연 60분의 배분 | 학생이 실제로 수정하는 30분 작업 | 차시 결과 |
|---|---|---|---|
| 1-1 | URL·요청응답 15, 세 파일 20, DevTools 15, 오류 복구 10 | 열기 5, h1·소개·CSS 색 편집 15, 링크 오타 복구 5, 확인 5 | 소개 화면, 200·404 구분 |
| 1-2 | Git 상태 15, init·설정 15, add·commit·log 시연 20, 실습 안내 10 | 저장소 준비 5, 제목→문단→파일 연결의 세 commit 20, log·status 5 | commit 3개 |
| 2-1 | GitHub·remote 15, 첫 push 20, Pages 15, 장애 대응 10 | 준비된 세 파일 push 12, 제목 한 줄 수정·재push 8, Pages·기록 10 | 공개 URL와 변경 기록 |
| 2-2 | branch·switch 15, about 파일·링크 15, merge 20, 비교 10 | about 브랜치 5, about 문단·홈 링크 수정 10, commit·merge·push 10, 확인 5 | 두 페이지 연결 |
| 3-1 | 시맨틱 구조 20, 제목·링크 15, 이미지·alt 15, 예제 비교 10 | 제공 뼈대의 제목·소개 10, img 경로·alt 10, 목록 수정·검사 10 | 자기소개와 이미지 |
| 3-2 | table 10, label·입력 20, form·기본 제출 20, 메뉴 10 | 표 두 행 5, label/for·이름·메시지 폼 15, 세 nav 링크·확인 10 | 아직 저장하지 않는 방명록 폼 |
| 4-1 | 선택자 15, 박스모델 20, width·max-width 15, 예제 비교 10 | ex01 선택자·ex03 여백 10, 누적 CSS 카드 폭·여백 15, 확인 5 | 선택자와 박스 차이 |
| 4-2 | flex 20, gap·정렬 15, media 15, 조립 시연 10 | nav flex·gap 10, 600px media 규칙 10, 375·1280 검사 10 | 좁은 화면에서 접히는 메뉴 |
| 5-1 | script·defer 10, let·const 15, 문자열·숫자 15, 템플릿 문자열 10, 예측 10 | 별칭·숫자 값 10, 출력 문장 10, 화면과 Console 대조 10 | 값 수정에 따른 화면 변화 |
| 5-2 | 비교·if 15, function·return 20, querySelector·textContent 15, 조립 10 | greet 반환값 10, 시간 조건 10, 결과 DOM 연결·확인 10 | 조건에 맞는 인사말 |
| 6-1 | DOM·선택 15, click 20, 함수 밖 변수 15, 오류 읽기 10 | 버튼 응답 문장 10, 증가량 10, id 오류 재현·복구 10 | 클릭 횟수와 응답 문장 |
| 6-2 | classList 20, CSS와 동작 15, 함수 재사용 15, 조립 10 | 다크 모드 클래스 10, countUp 호출 연결 10, 두 버튼·375px 10 | 공통 함수를 호출하는 두 버튼 |
| 7-1 | CDN 10, ex01 15, 입력·버튼 15, 카드·메뉴 15, 확인 5 | CDN 5, 입력·버튼 10, 카드·메뉴 10, Network 5 | W3.CSS 범주 네 가지 적용 |
| 7-2 | 변환 전 실행 10, 제공 JS 10, 폼 10, 카드·메뉴 10, class/id 10, 검증 10 | CSS 링크 5, 클래스·색 13, 빈값·글 두 건·375px 7, 캡처 5 | 동작을 유지한 W3.CSS 방명록 |
| 8-1 | 예외: 문제 읽기·오류 시연 30 + 연습 60 | 서로 다른 은행 문제 3개를 각 15분, 확인·정리 15분 | 중간 범위의 개인 연습 |
| 8-2 | 예외: 안내 15 + 개인 실기 60 + 제출·장애 처리 15 | 공지한 문제의 코드·화면·설명 제출 | 1~7주 개인 실기 |
| 9-1 | README 링크·그림 10, 다중 페이지와 SPA 비교 10, hash·classList 전환 20, 최초 실행·탐색 10, 통합 시연 10 | README 링크·화면 경로 8, 메뉴 href·showView 분기와 호출 14, 직접주소·뒤로가기·폼 유지 8 | 두 화면 SPA와 축약 README |
| 9-2 | 예외: 안내 10 + 2분 발표·교체 70 + 피드백 10 | 홈→방명록→글 두 건→홈→뒤로→README 시연, 받은 피드백 한 항목 기록 | 1차 발표와 README 과제 |
| 10-1 | 배열·push·length 20, index·for 20, createElement·append 15, 안내 5 | ex04 입력을 배열에 추가 10, 반복 종료 조건 10, li 표시 문장 5, 확인 5 | 배열과 화면의 항목 대응 |
| 10-2 | 비우고 재그리기 20, showList 15, 삭제 틀 15, 통합 10 | 누적 guestbook.js의 push·showList 10, 제공 삭제 틀의 위치 10, 3개→가운데 삭제→2개 10 | SPA 안의 배열 방명록 |
| 11-1 | 실행 환경 10, 객체 15, 객체 배열 15, 필드 표시 15, 안내 5 | ex01 속성 8, ex02 인덱스 8, ex03 표시 필드 9, 대조 5 | 객체와 배열의 접근 구분 |
| 11-2 | 문자열 10, JSON 15, 폼 복원 15, origin 10, 시연·안내 10 | ex04 저장·삭제 8, ex05 JSON 8, ex06 이름·메시지 수정·복원 11, 캡처 3 | 새로고침 후 폼 복원 |
| 12-1 | 접속·about 15, help 10, URL·헤더·book_id 15, JSON·GET 15, 안내 5 | about/help Send Request 10, book_id·limit 수정 10, 응답과 화면 대조 10 | API 정보와 자기 글 GET 200 |
| 12-2 | await·응답 20, showList 연결 15, ok·catch 15, 재시도 10 | 제공 fetch의 URL·응답 전달 10, 이름·메시지 표시 순서 10, Offline·복구 10 | 같은 SPA에서 서버 목록 읽기 |
| 13-1 | GET/POST 15, headers·body 20, JSON 15, 입력 오류 10 | .http 메시지·book_id 편집 10, POST 본문 작성 10, 201·id·GET 대조 10 | 서버에 저장된 한 글 |
| 13-2 | submit 15, disabled·오류 15, 성공 후 GET 15, 통합·중복 확인 15 | name/message와 body 연결 10, 성공 후 loadMessages 호출 10, 재조회·다른 브라우저 10 | 폼 저장과 서버 재조회 |
| 14-1 | index/id 15, 편집 키 15, DELETE·204 15, 실제 변경 확인 15 | 자기 ID 지정·.http 10, 제공 삭제 코드의 URL·method 10, 틀린 키·GET 대조 10 | ID 하나의 삭제 검증 |
| 14-2 | PATCH 15, 기존 값 폼 표시 15, 응답 행 수·재조회 20, 안내 10 | 수정 대상·JSON body 연결 10, PATCH 후 GET 비교 10, CRUD·키 비우기·캡처 10 | 수정·삭제 가능한 온라인 방명록 |
| 15-1 | 예외: 범위·환경·문항 안내 30 + 연습 60 | 화면/목록/저장/REST 중 세 문항 각 15분, 결과 대조 15분 | 기말 개인 연습 |
| 15-2 | 예외: 안내 15 + 개인 실기 60 + 제출·장애 처리 15 | A~E 개인 답안, 코드 한 줄 구술, 자기 시험 공간 재조회 | 누적 개인 실기 |

9주 새 학습은 Markdown 링크·이미지, hash 주소, location.hash, hashchange로 제한한다. 제목·항목·실행 안내는 제공 README 틀에서 본인 내용으로 고치며 별도 문법 시험을 하지 않는다. 10주 이후에도 함수 전체를 암기해 다시 쓰게 하지 않는다. 학생이 쓰는 줄, 제공된 오류 처리, 관찰만 하는 코드에 서로 다른 표시를 붙인다.

9주 발표 시간은 2분 발표+교체 20초 기준 최대 30명이다. 31명 이상이면 모두 같은 2분 영상과 README를 사전에 내고 수업에서는 조별 상호 시연·강의자 순회 확인을 한다. 해당 분반 전체에 같은 방식을 적용하고 내용·동작·설명 기준을 유지한다. 영상 준비는 별도 10~15분 추정이다.

## 방명록 파일의 인계 계약

아래 WNN은 해당 주차의 examples/day2/web-weekNN을 뜻한다. 1~3주는 기존 examples/day1·day2 경로를 쓴다. 학생 개인 변경을 우선 넘기며, 누락·오류가 있으면 같은 주 교재 대조본을 사용한다. 새 주에 앞 주 JavaScript를 이유 없이 전부 지우라는 지시는 없앤다.

| 주 | 시작 파일 | 학생 변경과 다음 주로 넘길 파일·기능 |
|---|---|---|
| 1 | week01의 day1 세 파일 | index.html·styles.css·app.js와 Git 기록. JS는 제공 상태 유지 |
| 2 | 1주 세 파일 → my-web | about.html·홈 링크 추가, 공개 주소와 브랜치 기록 |
| 3 | 2주 day2 | guestbook.html의 이름·메시지 폼, index/about/guestbook 공통 메뉴. 저장 기능 없음 |
| 4 | 3주 day2 → W04 | styles.css 반응형 규칙, 세 HTML의 클래스. 폼 구조 유지 |
| 5 | W04 → W05 | app.js 인사말, index.html 출력 자리. 방명록 폼은 그대로 |
| 6 | W05 → W06 | app.js 클릭·다크 모드·횟수. 방명록 처리는 아직 제공 전 |
| 7 | W06의 내용 + W07 guestbook.before.html·guestbook.js | guestbook.html CDN·클래스 변환. guestbook.js는 제공본, 글은 DOM에만 존재 |
| 8 | W07 보존, 별도 exam 폴더 | 시험 파일을 누적 사이트에 섞지 않고 W07을 9주에 넘김 |
| 9 | W07 + 신설 day1/12_hash_views/start의 통합 시작본 | W09 index.html의 home-view/guestbook-view, 새 navigation.js, 식별자를 정리한 app.js, 같은 guestbook.js, README·화면. about 내용은 홈 카드에 포함 |
| 10 | W09 → W10 | index.html 방명록 영역에 count·empty 추가, guestbook.js에 items·showList·삭제 틀. navigation.js 그대로 |
| 11 | W10 + 별도 ex01~ex06 | 학생 필수 제출은 ex06. 강의자가 W10 기반 객체 배열·저장 W11 인계본을 제공하고 차이표·시연을 동봉. 학생이 전체 저장을 구현했다고 기록하지 않음 |
| 12 | 제공 W11 → W12 | 같은 index.html에서 서버 목록 영역 사용, config.example.js·guestbook.js·requests.http. 11주 localStorage 키는 지우거나 서버로 옮기지 않음 |
| 13 | W12 → W13 | index.html 기존 이름·메시지 폼 재사용, submit.js 추가, requests.http POST 추가. GET·navigation.js 유지 |
| 14 | W13 → W14 | 키 입력·수정 폼, edit.js와 삭제 지원 파일, requests.http PATCH/DELETE. 서버 id로 대상 지정 |
| 15 | W14 보존, 별도 은행·exam 폴더 | 학습용 데이터와 시험용 book_id 분리. 시험 수정 내용을 W14에 자동 반영하지 않음 |

W09 시작본은 교재 W07과 같은 폼·목록 코드를 포함한다. 학생은 자신의 제목·소개·선택 색상을 옮기며, body 전체를 수동 병합하지 않는다. 강의자가 먼저 모든 id 중복과 전역 const/let 이름 충돌을 제거하고, 홈의 다크 모드 CSS를 홈 영역으로 한정한다. 이 사전 조립을 SPA 학생 성취로 세지 않는다. 10주부터 기존 방명록의 id는 유지한다.

정규 예제는 cdnjs의 https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css 를 계속 읽는다. 별도 라이브러리 사본은 만들지 않는다. 추가 CSS는 web_programming/shared/examples.css로 모으고, 배포용 시작 ZIP에는 동일한 추가 CSS만 shared/examples.css로 포함한다. 교재 상대 경로와 학생 ZIP의 ./shared/examples.css 경로를 각각 README에 적어 11주의 상위 폴더 의존을 숨기지 않는다. 9~14주 옛 guestbook.html·about.html 경로는 해당 주 index.html hash로 가는 짧은 안내 링크만 남기고 두 개의 동작하는 정본을 유지하지 않는다.

## SPA의 구현 범위와 주소 동작

| 항목 | 구현 계약 |
|---|---|
| 화면 수 | 홈(소개 카드 포함)과 방명록 두 영역. URL은 #home, #guestbook 두 개 |
| 학생 코드 | 두 a 요소의 href, showView의 location.hash 비교, 기존 classList.add/remove로 w3-hide 전환, hashchange 등록과 최초 showView 호출. 새 배열·객체·라우트 표 없음 |
| 제공 코드 | DOM 선택·접근성 보완·제목과 초점 갱신. 코드 읽기 표에 제공 범위라고 명시. home/guestbook script는 defer로 한 번씩 연결 |
| DOM 수명 | 화면 이동에서 영역을 삭제하거나 innerHTML로 갈아 끼우지 않음. 7주 글과 작성 중 입력은 화면 이동 후 유지, 9·10주 새로고침 때 사라짐 |
| 최초 진입 | hash가 없어도 showView를 한 번 호출해 홈 표시. #guestbook 직접 주소는 처음부터 방명록 표시 |
| 잘못된 hash | #unknown은 홈과 짧은 안내를 표시하며 홈 링크 제공. 임의 URL 문자열을 HTML로 넣지 않고 주소를 연쇄 변경하지 않음 |
| 뒤로·앞으로 | 링크의 기본 hash 이동을 사용하고 hashchange에서 같은 showView 실행. 클릭 리스너만으로 전환하지 않음 |
| 새로고침 | /web-week09/#guestbook는 서버에서 /web-week09/를 읽고 hash는 브라우저가 처리. 11주 이후 데이터 복원은 저장 기능이 맡음 |
| 경로 제한 | /web-week09/guestbook 같은 존재하지 않는 경로는 지원하지 않음. History API fallback·404.html 우회가 불필요한 hash 방식으로 통일 |
| REST와 관계 | showView에서 fetch·submit 리스너를 다시 등록하지 않음. GET은 시작 시 한 번·새로 불러오기·변경 성공 후에 실행. 화면 왕복이 POST를 만들지 않음 |
| 접근성 | 숨긴 영역은 Tab 순서에서 빠지고 메뉴는 실제 링크. 이동한 영역 제목의 focus와 document.title을 제공 코드로 갱신하고 375px·키보드 탐색 확인 |

hashchange는 URL fragment가 바뀔 때 발생한다. pushState/replaceState로 hash를 바꾸는 별도 방식을 섞지 않는다. [MDN hashchange](https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event)
fragment가 서버로 전송되지 않는다는 규칙과 GitHub Pages의 정적 파일 호스팅을 근거로 위 hash 주소를 선택했다. 실제 배포 통과는 별도 브라우저 시험으로 확인한다. [MDN URI fragment](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment), [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
w3-hide는 화면 감추기 클래스다. 라우터에서 이미 배운 classList를 재사용하며 hidden 속성과 별도 CSS display 규칙을 혼합하지 않는다. [W3.CSS Display](https://www.w3schools.com/w3css/w3css_display.asp)

## REST·저장·평가의 수정 범위

12주 첫 폴더는 신설 day1/01_about, 다음은 02_help로 둔다. 특강의 01_about·02_help에서 요청 형식을 재사용하되 정규 학생은 Supabase 구축을 하지 않는다. 이후 기존 ex03 쿼리, ex04 목록, ex05·ex06 오류 예제를 연결한다. 13주·14주 각 요청 예제와 기말 REST 시작 폴더에도 자체 실행 가능한 requests.http와 짧은 README를 넣는다. 완성본에만 .http가 있는 현재 상태에서 단계별 배포로 바꾼다.

README는 VS Code REST Client(humao.rest-client) 설치, baseUrl·apikey·bookId 설정, 요청 위 Send Request, 응답 Status·Body 읽기를 순서대로 적는다. 추적 파일에는 로컬 예제값·자리표시자만 둔다. 실제 값은 Git 제외 로컬 환경값으로 받고 편집 키는 @prompt password로 입력한다. 브라우저의 공개 키는 식별용 공개 설정이고, secret/service_role은 학생 배포에 포함하지 않는다. API 키가 필요한 about/help에서도 apikey 헤더를 생략하지 않는다.

GET 200과 빈 배열, POST 201과 반환 id, PATCH 200과 변경 행 한 개, DELETE 204와 빈 본문을 분리한다. PATCH/DELETE는 book_id와 서버 id를 함께 지정하며 204에 response.json()을 호출하지 않는다. 잘못된 키의 PATCH 200 []·DELETE 204도 실제 변경 실패일 수 있으므로 GET으로 확인한다. 편집 키는 해당 방명록의 수정 권한이며 작성자 로그인 증명이 아니다. 키는 메모리에만 두고 화면·URL·localStorage·추적 파일에 남기지 않는다. 캡처는 Network 헤더 상세를 닫고 입력 칸을 비운 상태로 한다.

| 자료 | 변경 범위·유지 사항 |
|---|---|
| 1~6주 | 기존 예제와 경로 보존. 필수·시연·선택 구분, 60/30 시간표, Console 전용 기본 예제의 화면 결과 보강. branch는 2주에 배우고 3주의 추가 branch 실습은 선택 |
| 7주 | 현재 필수 예제와 W3.CSS 구현 평가 유지. 공통 CSS·다음 주 링크만 점검 |
| 9주 | 신설 12_hash_views에 시작본·대조본·README, W09 통합본. ex01~ex11은 삭제하지 않고 필수 링크·이미지 외는 참고. 기존 SVG·Mermaid는 정규 과제 채점에서 제외 |
| 10~14주 | WNN 완성본의 공통 SPA 외곽과 navigation.js 유지, 방명록 데이터 파일만 주차별 변경. standalone 비교 예제는 그대로 작은 화면으로 운영 |
| 11주·기말 저장 | ex04→ex05→ex06 유지. 기말 w11_local_storage는 폼 한 객체의 저장·불러오기·지우기를 평가하도록 README·시작본·채점표를 맞춤. 배열 전체 저장을 필수로 묻지 않음 |
| 8주 평가 | 시험일과 기존 은행 범위 유지. 60분 시험에 맞는 문항 수·제출 안내를 일치시킴. 7주 폼 JS 직접 구현을 추가하지 않음 |
| 9주 평가 | 기존 1차 과제 10점(발표 5·README 5) 유지. README는 주소·재현 설명·화면·경로 정확성으로 채점. 발표는 실제 동작·설명을 보며 router 암기 점수 없음 |
| 14·15주 평가 | 14주는 수정·삭제 실습 유지. 레포트는 별도 과제이며 검사주로 환원하지 않음. 기말 A~E 구조 유지, SPA는 제공 시작본으로 두며 시험용 API·태그·키를 별도 준비 |
| 한영 자료 | 각 주 README·lab·walkthrough·slides.md·slides_en.md·examples/README를 같은 변경표로 갱신. 용어 3열 표·절대 실습 주소·덱 주소·문제은행 출처·옛 경로 안내까지 확인 |
| 특강 5종 | 배열 심화·Supabase 구축·홈 IoT HTTP·지도·신시사이저를 정규 밖에 유지. 해당 기술을 SPA의 선수 조건으로 삼지 않음. 방학 연구의 분량·회차 상한 없음. 110분 등의 표시는 도입 예시로 유지 |

## 구현 순서와 검증

| 순서·담당 범위 | 구현할 일 | 다음 단계 통과 조건 |
|---|---|---|
| 1. 공통 담당 | 필수/시연/선택 표, 30차시 시간표, 평가 범위 확정. API 요청 계약·CSS 배포 경로 확정 | 문법 도입 주와 학생 수정 줄이 일치, 11주 인계 모순 제거 |
| 2. 9주 담당 | W07→W09 통합 시작본, home 식별자 정리, 두 화면 router, README 축약 | id·전역 선언 중복 없음, W07 빈값·글 추가 동작 유지, 초보 리허설 기준 충족 |
| 3. 1~8주 담당 | 기존 예제 보존과 실습 축소, 화면 결과, 시간표·중간 은행 정합 | 30분 독립 실습과 1~7주 시험 범위 일치 |
| 4. 10~11주 담당 | 같은 SPA에서 배열 목록, 제공 저장 인계본, ex06·기말 저장 범위 | 화면 왕복과 새로고침의 차이, 손상 JSON·origin 차이 확인 |
| 5. 12~14주 담당 | about/help→GET→POST→PATCH/DELETE 폴더·.http·화면 연결 | 로컬 API 자동 시험, 공개 HTTPS와 Pages에서 CRUD·권한·CORS 실제 확인 |
| 6. 평가·교재 담당 | 9주 rubric, 기말 시작본, 한영 슬라이드·공통 색인·링크 정리 | 학생 활동·교재·은행에 서로 다른 시작 파일이나 제출 조건 없음 |
| 7. 독립 검증 담당 | 웹프로그래밍 대상 링크·브라우저·시간 검증 후 저장소 공통 build/check/test | 직접 구현하지 않은 평가자 3명 모두 8/10 이상. 다른 과목·tools/wleno 수정 없이 실패 원인 분리 |

공통 명령은 저장소 [package.json](../../../package.json)의 npm run build, npm run check, npm test를 사용한다. npm test는 덱 검사와 test:labs를 포함한다. 이 기획 단계에서는 산출물을 만들거나 코드를 실행·수정하지 않았으며 해당 명령의 통과를 주장하지 않는다.

| 검증 장면 | 예상 실패·판정 | 복구 또는 대안 |
|---|---|---|
| 새 PC에서 시작 ZIP 실행 | 공통 CSS 404, 파일 위치 혼동 | README에 서버 root·실행 명령·실제 URL 명시. 교재는 node web_programming/tools/static-server/server.mjs web_programming 8111, 학생 ZIP은 그 폴더에서 node server.mjs . 8000으로 열어 대조 |
| 7주 변환 | id를 class처럼 바꿔 폼 중단, CDN 차단 | id·script·Network 확인. CDN 장애는 구조·동작까지만 기록하고 스타일 검증은 연결 복구 후 수행 |
| 9주 30분 리허설 | 최초 showView 누락, 두 화면 동시 표시, 라우터를 폼 이벤트에 중복 등록 | 초보자 5명의 도움 횟수·완료 시간 기록. 4명/25분 기준 미달이면 도입 철회, 복붙 완성본으로 통과 처리하지 않음 |
| SPA 경로·탐색 | /repo/#guestbook 직접 진입·새로고침, 홈↔방명록 뒤로/앞으로, #unknown 중 한 동작 실패 | localhost와 실제 Pages에서 모두 확인. 프로젝트 하위 경로의 CSS·script 상대 주소도 검사 |
| SPA 상태·키보드 | 왕복 뒤 입력·글 소실, 중복 글 등록, 숨은 입력에 Tab 진입 | DOM 교체와 리스너 중복을 제거. 왕복 5회 후 한 번 제출해 한 건만 생기는지 확인 |
| 11주 저장 | 같은 GitHub host의 주차별 키 충돌, 깨진 JSON, file:// 오판 | 키를 주차·별칭으로 구분, 오류 안내·해당 키만 지우기 제공. 같은 origin에서 재현하고 다른 port·브라우저의 별도 저장을 비교 |
| 12주 요청 | .http 성공을 브라우저 CORS 성공으로 오인, []를 무조건 오류로 처리 | REST Client와 브라우저 둘 다 검사. 잘못된 공개 키·Offline·없는 endpoint를 자기 공간에서 비교 |
| 13주 저장 | POST 성공 후 GET 실패를 보고 다시 POST해 중복 생성 | 저장 결과와 목록 결과를 분리, 실패 시 입력 보존, 먼저 GET 재시도. Slow 3G에서 disabled·왕복 후 버튼 복구 확인 |
| 14주 변경 | 인덱스를 id로 사용, 204 JSON 파싱, 잘못된 키에도 성공 문구 | 자기 글 세 개로 가운데 삭제·남은 글 수정. 정확한 id와 후속 GET 결과로만 판정 |
| 평가 환경 장애 | Pages 지연·공용 API 중단을 코드 실력으로 감점 | 로컬 화면·코드·Commits 증거 인정, 공용 공유 검증은 미완료로 남김. 사전 점검한 로컬 시험 API 또는 동일한 대체 문항을 분반 전체에 적용 |

자체 검토에서는 15주 30차시, 각 90분, 7·11주 60/30, 12주 접속·도움말 우선, 13주 저장·14주 수정삭제, 배열 심화의 정규 제외를 대조했다. 기존 파일과 코드의 정적 조사, 공식 문서의 주소 동작 확인까지 수행했다. 제안 파일의 문체·상대 링크는 별도 검사한다. 아직 학생 리허설·새 SPA의 브라우저 실행·공용 CRUD 검증은 수행하지 않았다.

남는 약점은 9주에서 Markdown 표현 범위를 줄여야 한다는 점과 강의자에게 통합 시작본 작성·검증 부담이 생긴다는 점이다. 9~14주 예제 외곽과 한영 자료 수정은 담당별 병렬 작업 후 통합 1회를 포함해 4~6인일로 추정하며, 실제 분량은 시작본 리허설 뒤 다시 산정한다. 이 비용이나 30분 진입 기준을 충족하지 못하면 SPA를 특강으로 옮기는 대안을 선택한다.
