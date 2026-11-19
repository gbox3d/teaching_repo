# 5주차 전수 조사와 구현 기록

2026-11-18에 `weeks/week05_javascript_data/`의 기존 32개 파일을 조사하고, 개별 예제 README 10개와 제공 시작 파일 2개를 추가했다. 최종 조사 범위는 44개 파일이다. C01의 차시별 수정 상한을 적용했다. 이 기록에는 자체 평가 점수를 붙이지 않는다.

## 조사 범위

| 경로 | 확인한 내용과 조치 |
|---|---|
| `README.md` | 목표·준비·결과·시간·다음 주 인계를 60+30과 C01 필수 범위로 재작성 |
| `lab.md` | 학생 실습을 각 30분으로 제한. 값 4곳/오류 1건, 함수·조건·출력 각 1곳. 파일 받기·새 Git 설명·수업 중 업로드 제거 |
| `walkthrough.md` | 사전 준비와 제공 코드·학생 수정 구분. 완성 HTML·JS 전문은 실제 파일과 대조 |
| `slides.md`, `slides_en.md` | 기존 19장씩 유지. 60+30 시간·값·예제·제출·선택 범위를 한영 일치시킴 |
| `examples/README.md` | 10개 비교 예제의 필수/시연/선택 분리, 4→5→6주 파일별 인계 표 작성 |
| `examples/day1/ex01/{index.html,app.js,README.md}` | 실행 순서·반복 클릭, 화면 출력 추가. 설명을 README로 이동 |
| `examples/day1/ex02/{index.html,app.js,README.md}` | head/body/defer 실행 순서 유지. 실행 순서를 버튼으로 표시. 출력 지원은 제공 코드로 명시 |
| `examples/day1/ex03/{index.html,app.js,README.md}` | let·const·var 비교 보존. 각 값의 화면 표시 추가. a·b만 필수, var는 선택 |
| `examples/day1/ex04/{index.html,app.js,README.md}` | 입력에 label 연결, 문자열/숫자 계산 화면 결과 추가. parseInt 비교 선택화 |
| `examples/day1/ex05/{index.html,app.js,README.md}` | name·hour 수정 뒤 제공 버튼으로 인사 표시 |
| `examples/day2/ex06/{index.html,app.js,README.md}` | 비교 결과 버튼 출력. ==의 설명을 타입 변환 비교로 한정하고 선택화 |
| `examples/day2/ex07/{index.html,app.js,README.md}` | if 네 갈래 결과 화면 출력, 조건 순서 비교 유지 |
| `examples/day2/ex08/{index.html,app.js,README.md}` | return·undefined와 다른 인수 결과 화면 출력 |
| `examples/day2/ex09/{index.html,app.js,README.md}` | 화면의 긴 교수 설명 제거, 짧은 상태와 연결 label, 표준 한국어 문구. 다른 DOM 접근법 선택화 |
| `examples/day2/ex10/{index.html,app.js,README.md}` | 페이지 실행 순간의 날짜·시각을 버튼으로 표시. 새로 읽기는 새로고침임을 명시 |
| `examples/day2/start/{app.js,README.md}` | 세 곳만 바꾸는 제공 시작 JS. 독립 페이지가 아닌 교체용 파일임을 명시 |
| `examples/day2/web-week05/index.html` | script·greeting 카드와 메뉴·이미지 직접 확인. 기존 완성 코드 유지 |
| `examples/day2/web-week05/app.js` | greet·hello·message·DOM 출력과 6주 인계 이름 유지 |
| `examples/day2/web-week05/about.html` | 표·메뉴, 4주와 동일 내용 확인 |
| `examples/day2/web-week05/guestbook.html` | 최신 4주 파일 인계. 긴 ol 제거, 짧은 미저장 안내, native email 검증 유지 |
| `examples/day2/web-week05/styles.css` | 최신 4주 자체 CSS 인계. h1 keep-all과 입력 border-box 유지 |
| `examples/day2/web-week05/images/profile.png` | 400×400 프로필 아이콘을 직접 열어 확인. 기존 자산 보존 |

원고를 줄인 부분은 수업 중 개별 Raw 다운로드·Git 초기화·전체 app.js 재작성·모든 예제 의무 수정이다. 비교 개념과 실행 파일은 유지하고 각 예제 README에 기대 결과와 선택 조작을 기록했다.

## 차시별 근거

| 차시 | 강의·시연 | 학생 실습 | 제공 코드 |
|---|---|---|---|
| 5-1 | 준비 5 + 실행/defer 10 + let/const 15 + 숫자/문자열 15 + 템플릿 10 + 안내 5 = 60분 | ex03 a·b와 ex05 name·hour 4값 15분, 제공 버튼/const→let 오류 수정 10분, 확인 5분 | 버튼 리스너와 화면 출력 |
| 5-2 | 준비 5 + 비교/if 15 + 함수/return 20 + DOM 10 + 서버 5 + 안내 5 = 60분 | greet 반환·hello 조건·출력 각 1곳 18분, 9/15시 7분, 캡처 5분 | HTML 연결·카드, 함수 틀·현재 시각·message·로그·서버 |

파일 배부·새 저장소·Node.js 24 이상 준비는 사전 작업이다. 공개 업로드는 수업 뒤 10분 이내 정리이며 localhost 캡처로 수업 중 완료를 인정한다. Git 새 설명은 추가하지 않았다. var·==·parseInt·다른 DOM 접근법은 필수 구현·평가에서 제외한다.

## 실행 검증

Windows의 Node.js v24.18.0, Playwright의 Chrome headless, `http://localhost:8111/`에서 실행했다. 해당 서버의 기준 폴더는 `web_programming`이다. 수정한 소스를 브라우저에 주입한 경우는 원본 파일을 변경하지 않는 요청 override로 학생 수정과 오류를 재현했다.

| 예제·동작 | 실제 결과 |
|---|---|
| ex01 | 처음 A·C, 클릭 3회 뒤 B 3회 |
| ex02 | defer 존재 시 1:null→2:body→3:body. defer 제거 시 1:null→3:null→2:body. 제공 출력 버튼 정상 |
| ex03 | let·var 클릭 결과 1. const 클릭에서 의도한 Assignment to constant variable 오류와 값 0 유지. a=10, b=20 및 const→let 수정 후 11·21, 새 실행 오류 없음 |
| ex04 | 1·2 입력은 연결 12/합 3. 10·5 입력은 연결 105/합 15 |
| ex05 | 기본 student01·9시. 지정 값 수정 후 student02·15시 |
| ex06 | 출력 순서 true·false·true·false·false·true |
| ex07 | 9시는 미설정/오전/아침/아침, 12·15시는 모두 오후. 20시는 오후/오후/저녁/오후 |
| ex08 | return 없는 값 undefined, 나머지 인사 정상. greetLog를 return으로 바꾼 뒤 1번도 인사 반환 |
| ex09 | 버튼 뒤 네 표시 변경. `<b>3. 태그 문자</b>`는 문자이며 b 요소 0개. 없는 #out9 쓰기는 null 오류, 해당 줄 제거 후 복구. 키보드 Enter 실행 확인 |
| ex10 | 페이지를 읽을 때 담은 연·월·일·시·분·요일 표시 |
| 제공 시작 JS | 초기 출력은 출력 연결 전. 표시한 3곳을 수정한 코드가 완성 app.js와 개행 정규화 후 일치 |
| 완성 인사 | hour=9는 아침, 12·15는 오후. 실행 오류 없음 |
| 화면 폭 | ex01~ex10 각각 375/1280px 20회 실행, 가로 넘침 없음. 홈/소개/방명록도 두 폭에서 확인. 375px 메뉴 column, 1280px row |
| 정적 방명록 | label 클릭으로 email 포커스. invalid 이메일은 native typeMismatch로 제출 거절. 유효 제출은 같은 페이지 GET 탐색, query 없음, message가 비워져 미저장 확인 |
| 페이지 이동 | 홈→소개→방명록→홈, 직접 진입·새로고침·뒤로·앞으로 동작 확인 |

브라우저 검증 스크립트는 저장소 밖 임시 폴더의 `week05-browser.mjs`에 있다. 실행 결과 JSON과 홈 375/1280px 캡처는 같은 임시 폴더의 `week05-evidence/`에 있다. 두 홈 캡처는 직접 열어 검토했다. 임시 증거는 배포 자산에 포함하지 않았다.

## 정적 검사와 주차 인계

- JavaScript 12개 파일에 `node --check`를 실행했다. 구문 오류가 없다. ex03의 의도한 런타임 const 오류는 별도로 재현·수정 검증했다.
- 주차 Markdown/HTML의 로컬 링크·자산 경로 153개가 존재한다. 실습 앵커도 변경한 제목에 맞췄다.
- walkthrough의 HTML·JS 전체 코드 블록 2개가 실제 완성 파일과 일치한다.
- KO/EN은 각각 19장, `---` 구분선 20개로 기존 장수를 유지했다. 시간표·학생 수정량·예제 입력값·제출 기준을 대조했다.
- 한국어 UI 문구 검사와 문서 문체 검사 모두 종료 코드 0이다.
- 4주와 5주의 about·guestbook·styles는 개행 정규화 뒤 내용이 같고 프로필 그림도 동일하다. 그림 SHA-256은 `3dbf451ccc9d269aead36cd75f87432b2a8c0049640c490913df1c2a56768fca`다.
- 6주 담당에게 최신 정적 방명록·CSS와 greet/hello/#greeting 유지 사실을 전달했다.

## 남은 제한과 통합 담당 전달

초보 학생 3명의 30분 수행 실측, 실제 학생 계정의 Pages 업로드는 수행하지 않았다. 30분 상한은 C01 설계 기준이며 실측 통과로 표현하지 않는다. 전체 저장소 빌드·덱 배치 검사·통합 테스트는 총괄 담당의 통합 단계에서 실행한다. 이번 담당은 5주 소스와 이 보고서만 수정했으며 다른 과목·공통 파일은 수정하지 않았다. 커밋·푸시는 수행하지 않았다.
