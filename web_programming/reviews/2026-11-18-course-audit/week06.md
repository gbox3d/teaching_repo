# 6주차 조사·수정·검증 기록

2026-11-18에 `weeks/week06_dom_events/`의 기존 30개 파일과 추가 9개 파일을 조사했다. 적용 기준은 과목 AGENTS.md, implementation.md, C01의 6-1·6-2 행이다. karpathy-coding·ponytail·korean-copy-style 지침을 적용했다. 이 보고서는 실행한 범위와 제한을 기록하며 자체 평가 점수를 부여하지 않는다.

## 조사한 원고와 자산

| 파일 | 조사와 반영 |
|---|---|
| `README.md` | 기존 30+60과 예제 전부 수정 요구를 60+30으로 바꿈. 시작 틀·제공 코드·필수 변경·수업 전후 구분, 7주 W3.CSS 인계 보존 |
| `lab.md` | 1차시 ex03 여섯 줄, 2차시 CSS 두 값과 toggle·countUp 세 줄로 한정. 새로고침·두 폭·캡처 절차 일치 |
| `walkthrough.md` | Raw 다운로드·저장소 생성·전체 app.js 재작성을 수업 중 필수에서 제거. 실제 HTML·CSS·JS 전문과 일치하도록 갱신 |
| `slides.md`, `slides_en.md` | 각 15장 유지. 두 차시 60+30과 필수·시연 구분, 같은 시점·예제 경로·결과로 대조. 7주 W3.CSS·제공 JS 안내 보존 |
| `examples/README.md` | 여섯 예제·시작 틀·완성 폴더와 파일별 변경표 작성. 정적 방명록 설명을 HTML 밖으로 이동 |
| `examples/day1/ex01/{index.html,styles.css,app.js,README.md}` | 세 기존 소스를 읽고 원본 HTML/현재 DOM 차이 확인. 장문 화면 문구를 README로 이동 |
| `examples/day1/ex02/{index.html,styles.css,app.js,README.md}` | 세 기존 소스를 읽고 초기 실행/반복 클릭/새로고침 확인. 버튼 type 명시 |
| `examples/day1/ex03/{index.html,styles.css,app.js,app.start.js,README.md}` | count와 inside 비교는 보존. 여섯 줄 필수 시작 틀 추가, 설명은 README로 이동 |
| `examples/day2/ex04/{index.html,styles.css,app.js,README.md}` | add/remove 반복과 toggle 확인. 화면 설명 이동, 버튼 type 명시 |
| `examples/day2/ex05/{index.html,styles.css,app.js,README.md}` | body·card CSS와 toggle 확인. 고정된 “흰 배경” 문구를 “카드”로 수정, 설명 이동 |
| `examples/day2/ex06/{index.html,styles.css,app.js,README.md}` | 공유 countUp과 괄호 누락 비교 확인. 화면 설명 이동 |
| `examples/day2/web-week06/index.html`, `app.js`, `about.html` | 기존 개인 홈·소개와 greet·hello·#greeting 보존, 두 버튼과 왕복 링크 검사 |
| `examples/day2/web-week06/styles.css` | 5주 최종 CSS 인계. h1 keep-all·input/textarea border-box 유지, 다크 제목·메뉴 #a7c5ff와 푸터 #c8d4eb 추가 |
| `examples/day2/web-week06/guestbook.html` | 5주 최종본과 동일하게 맞춤. 긴 순서 목록 제거·짧은 미저장 문구 유지 |
| `examples/day2/web-week06/app.start.js`, `README.md` | 요소 선택·greet·hello·countUp·리스너 틀 제공, 학생 TODO 세 줄 표시 |
| `examples/day2/web-week06/images/profile.png` | 400×400 기본 프로필 그림을 직접 열어 확인. 홈에서 160px 표시·정상 로딩 확인, 자산 내용 유지 |

중괄호 경로는 해당 폴더의 각 파일을 모두 읽었다는 뜻이다. 새 파일은 예제별 README 7개와 app.start.js 2개다. 다른 주차와 공통 도구는 수정하지 않았다.

## 차시별 구현 범위

| 차시 | 60분 강의·시연 | 30분 학생 실습 | 제공 범위 |
|---|---|---|---|
| 6-1 | 준비 5, DOM·소스 15, click 15, 함수 밖 변수 15, 오류 시연 5, 안내 5 | ID 대조 5, countBox·count·리스너·증가·출력·닫기 여섯 줄 15, 3회·초기화 확인 10 | HTML·CSS·btn 선택, inside·console 비교는 강의자 완성 예제 |
| 6-2 | 준비 5, classList 15, 다크 모드 15, 함수 재사용 15, 시험 범위 5, 안내 5 | CSS 두 값 5, 두 리스너의 toggle·countUp 세 줄 10, 두 버튼·화면 폭 10, 캡처 5 | HTML·다크 CSS 선택자·요소 선택·greet·hello·countUp·리스너 틀 |

파일·저장소는 사전 준비, GitHub 업로드는 수업 뒤 10분 이내 정리다. 수업 중 캡처는 localhost 또는 파일 주소로 인정한다. 1~6주 자체 CSS를 유지하고 7주에 W3.CSS를 도입한다. 부모 body에 색을 넣어도 고유 color를 가진 제목·메뉴·푸터에는 상속되지 않는 이유를 lab·walkthrough·한영 슬라이드에 반영했다.

## Chrome 실행 근거

2026-11-18 20:08 KST에 설치된 Chrome `157.0.8103.38`을 Playwright `channel: chrome`, headless로 실행했다. 기준 주소는 `http://localhost:8111/weeks/week06_dom_events/examples/`다. 여섯 예제와 완성 홈·소개·방명록의 9페이지를 각각 375×900·1280×900에서 확인했다. 18번의 페이지·CSS·JS·이미지 로드가 정상이며 가로 넘침이 없었다. 정상 실행 중 pageerror는 0건이다.

| 예제 | 실제 동작 검증 |
|---|---|
| ex01 | 원본 응답은 원래 글자, DOM은 JS가 바꾼 글자. 임시 DOM 변경 뒤 새로고침하면 원복. 잘못된 ID 변형에서 null 오류를 재현하고 원본 복원 |
| ex02 | 처음 문구→세 번 클릭 후 클릭 문구→새로고침 후 첫 문구 |
| ex03 | 세 번 클릭 3회→새로고침 0회. console count 1·2·3, inside 1·1·1. 시작 틀에 lab의 여섯 줄만 추가해 동일 카운터 실행. count를 함수 안으로 옮기면 매번 1회 재현 |
| ex04 | add 두 번 후 on 하나, remove 두 번 후 없음, toggle 세 번 후 on, 새로고침 초기화 |
| ex05 | 두 번 클릭으로 dark 켜기·끄기, 카드 배경 rgb(34,34,34), 새로고침 초기화 |
| ex06 | A·B·A는 3회, 새로고침 0회. A의 countUp 괄호를 뺀 변형은 A 0회·B 1회 |
| 홈 완성본 | 인사·다크·인사는 3회와 새 문구. 다크 버튼 10회 추가 클릭은 13회. 새로고침은 0회·밝은 화면. Enter·Space도 각 한 번 증가 |
| 홈 시작 틀 | TODO 세 줄만 채워 인사·다크 버튼 2회와 dark class 확인. lab의 CSS 두 값 변경도 실제 계산 색으로 확인 |
| 홈 다크 색 | 375·1280 모두 h1/h2/nav a는 rgb(167,197,255), footer는 rgb(200,212,235). 스크린샷을 직접 열어 읽기·배치를 확인. 375 메뉴 column·1280 row |
| 소개·정적 방명록 | 실제 HTML 경로 왕복·뒤로·앞으로·새로고침 확인. 이메일 label 클릭은 입력 포커스. 잘못된 이메일은 탐색을 막고 메시지 유지. 유효 이메일은 같은 문서 GET, 입력 name 속성이 없어 쿼리 값·저장 없음, 다시 열린 메시지 빈값 |

오류 변형은 브라우저 응답만 임시 교체했으며 소스에 남기지 않았다. 예상된 null 오류 한 건과 정상 페이지 오류 0건을 구분했다. 화면 이미지와 JSON 결과는 저장소 밖 임시 폴더 `week06-audit/`에 있다. 홈 두 폭·ex01·ex04·방명록 스크린샷과 프로필 원본을 직접 열어 확인했다.

## 정적 검사와 인계

- JS 9개에 node --check 실행, 구문 오류 없음.
- 문서의 로컬 링크·anchor 145개 검사, 누락 없음.
- walkthrough의 HTML·CSS·JS 전문 세 블록과 실제 완성 파일 일치.
- HEAD와 현재 KO·EN 덱은 각각 15장으로 동일. 양 언어 강의/실습 합계·예제·완료 조건 대조.
- UI 문구 검사와 문서 문체 검사 0건. git diff --check에 공백 오류 없음.
- 5주 최종 guestbook과 6주 파일은 동일하고 5주 CSS는 6주 CSS의 변경 없는 앞부분이다. 7주 담당에게 최종 CSS와 홈·app·소개·프로필 유지, app.start는 실습 틀이며 다음 주 동작 파일이 아니라는 점을 전달했다.

## 남은 검증 범위

초보 학생의 실제 30분 수행 시간은 측정하지 않았다. 시간과 필수 수정량은 C01 설계에 맞춘 것이며 학습자 실측 통과로 기록하지 않는다. 실제 GitHub 저장소 생성·push·Pages 배포는 이번 작업에서 실행하지 않았다. 전체 빌드·공통 테스트·렌더된 한영 덱의 최종 화면 검사는 총괄 통합 단계에서 수행한다. 커밋·푸시는 하지 않았다.
