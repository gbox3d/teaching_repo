# 4주차 구현 및 실행 검토

C01의 4-1·4-2를 반영했다. 수정 범위는 `weeks/week04_responsive_css/`와 이 보고서다. 공통 파일·다른 주차는 수정하지 않았고 커밋·푸시는 하지 않았다.

## 전수 조사 범위

기존 40개 파일을 모두 읽거나 그림으로 확인했다. 원고 6개, 비교 HTML·CSS 28개, 완성 HTML 3개·CSS 1개·보존 JS 1개·PNG 1개다. 비교 예제 13개와 선택 부록 ex14를 모두 보존했다.

| 파일 (`weeks/week04_responsive_css/` 기준) | 조사·수정 내용 |
|---|---|
| `README.md` | 60+30 시간표, 학생 수정 상한, 사전 배부·저장소 준비, 로컬 캡처와 수업 뒤 업로드, 다음 주 인계 수정. 전체 비교 목록 보존 |
| `lab.md` | 1일차 비교 2값·사이트 3값, 2일차 비교 2값·nav/media 3줄로 필수 실습 축소. 기존 제출 앵커 보존 |
| `walkthrough.md` | 필수 30분 순서와 전체 조립 시연을 구분. 실제 CSS·HTML·JS 전문 5개를 다시 대조 |
| `slides.md` | 차시별 시간 구간·필수·시연·선택·로컬 캡처·인계 수정. 기존 23장 보존 |
| `slides_en.md` | 한글과 같은 시간·지정값·완료 조건·폼 동작으로 수정. 기존 23장 보존 |
| `examples/README.md` | 모든 예제의 비교 설명과 선택값 보존. HTML에서 뺀 설명을 문서에 두고 제공 완성본의 역할 명시 |
| `examples/day1/ex01/index.html`, `styles.css` | 비교 라벨에서 긴 설명 제거. CSS 주석의 ‘모든 p가 회색’ 오류를 ‘1·4번 회색, 2번 .red 우선’으로 수정 |
| `examples/day1/ex02/index.html`, `styles.css` | block/inline 비교 구조·CSS 보존, 끝 설명 문단 제거 |
| `examples/day1/ex03/index.html`, `styles.css` | padding·border·margin 비교 보존, DevTools 설명을 화면에서 제거 |
| `examples/day1/ex04/index.html`, `styles.css` | 고정 폭과 최대 폭 비교 보존. 의도한 375px 넘침을 문서에 명시, 긴 실험 순서 제거 |
| `examples/day1/ex05/index.html`, `styles.css` | auto 여백의 네 경우 보존. 라벨 단축·설명 문단 제거 |
| `examples/day1/ex06/index.html`, `styles.css` | text-align 세 값과 상자 폭 보존. 설명 문단 제거 |
| `examples/day2/ex07/index.html`, `styles.css` | 부모·방향 다섯 경우 보존. 라벨 단축·설명 문단 제거 |
| `examples/day2/ex08/index.html`, `styles.css` | justify-content 다섯 경우와 선택 space-evenly 보존. 설명 문단 제거 |
| `examples/day2/ex09/index.html`, `styles.css` | align-items 네 경우와 100px 높이 보존. 설명 문단 제거 |
| `examples/day2/ex10/index.html`, `styles.css` | 300px 부모·80px 자식 여섯 개의 nowrap/wrap 보존. 설명 문단 제거 |
| `examples/day2/ex11/index.html`, `styles.css` | gap 0·16·32 비교 보존. 설명 문단 제거, 문서의 바깥 간격 설명 명확화 |
| `examples/day2/ex12/index.html`, `styles.css` | flex: 1 비교·선택 flex: 2 보존. 짧은 라벨만 화면에 유지 |
| `examples/day2/ex13/index.html`, `styles.css` | media 비교 보존. 라벨을 600px ‘이하’로 수정, 기기 모드 절차는 문서로 이동 |
| `examples/day2/ex14/index.html`, `styles.css` | 선택 position 예제 보존. 라벨 단축. relative가 흐름에서 빠진다는 잘못된 문서·한영 설명 수정 |
| `examples/day2/web-week04/index.html` | 학생 소개·취미 본문은 정당한 콘텐츠이므로 보존. 카드 세 곳·그림·메뉴 확인 |
| `examples/day2/web-week04/about.html` | 가상 정보·표·세 메뉴·CSS 연결 확인, HTML 보존 |
| `examples/day2/web-week04/guestbook.html` | 최신 3주차 정적 폼에 CSS link 한 줄을 더한 상태로 인계. 긴 쓰는 순서·후속 강의 설명을 제거하고 짧은 미저장 상태 유지 |
| `examples/day2/web-week04/styles.css` | 자체 CSS 유지. 제목 keep-all과 입력 border-box 보정 제공. 입력의 280px에 테두리를 포함하도록 문서와 일치 |
| `examples/day2/web-week04/app.js` | 2주차 보존 코드·구문 확인. HTML에서 연결하지 않으며 4주 실행 대상이 아님 |
| `examples/day2/web-week04/images/profile.png` | 400×400 프로필 그림 직접 확인. 정상 로드·alt 확인, 자산 보존 |

## 차시별 운영과 변경량

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 4-1 | 준비 5, 선택자 15, 박스모델 15, max-width·margin 15, 비교 시연 5, 안내 5 | ex01·ex03 각 1값 10, 사이트 CSS 색·여백·폭 3값 15, 확인 5 |
| 4-2 | 준비 5, flex 부모·축 20, gap·정렬 10, media 15, 조립 시연 5, 안내 5 | ex07·ex08 방향·정렬 2값 10, 사이트 nav·media 3줄 12, 375/1280px 확인·캡처 8 |

1일차 필수값은 ex01 orange, ex03 32px, 사이트 제목 #365314·카드 padding 20px·body max-width 600px이다. 2일차는 ex07 column→row, ex08 center→flex-end와 사이트 gap 24px·media 700px·방향 row 비교 뒤 column 복원이다. nav·media는 기존 3줄의 값만 바꾸므로 5줄 상한 안에 있다.

완성 예시 CSS는 원래 600px 경계를 보존하고 학생 실습값 700px과 구별했다. 둘 다 375px에서는 세로, 1280px에서는 가로 메뉴다. ex02·04·05·06·09·10·11·12·13의 추가 수정과 전체 조립은 시연·선택이다. ex14는 선택 부록이다. 모든 비교 파일을 다시 입력하거나 전부 바꾸는 요구를 제거했다.

파일·새 저장소는 수업 전 준비하고 강의 첫 5분에 실행 상태만 확인한다. 30분 실습 안에서는 로컬 캡처로 완료한다. 업로드·Pages 확인은 수업 뒤 2주차 순서의 반복이며 Git을 새로 설명하지 않는다. 자체 CSS는 유지하고 W3.CSS를 7주차에 도입한다.

## 실제 실행 결과

2026-11-18, 설치된 Chrome을 Playwright headless로 실행했다. 기준 경로는 `http://localhost:8111/weeks/week04_responsive_css/examples/`다. 별도 설치·새 의존성·추적 테스트 파일은 추가하지 않았다.

| 실행·검사 | 결과 |
|---|---|
| HTML 17개 × 375/1280px | 총 34개 경우 HTTP 200. ex04의 375px만 scrollWidth 648로 넘침. 고정 640px 비교 상자의 의도한 동작이며 나머지는 모두 뷰포트 폭과 일치 |
| ex01 | 기본 색·클래스 우선순위 확인. 필수 orange 적용 후 2·3번만 주황 |
| ex02 | as-block 세 개 block, as-inline 세 개 inline 확인 |
| ex03 | pad 두 상자의 16px→32px 필수 변경 확인 |
| ex04 | 고정 상자 640px 유지. 375px에서 최대 폭 상자는 359px로 축소 |
| ex05 | 1280px에서 상자 x 좌표 8·972·490·490으로 왼쪽·오른쪽·가운데 비교 확인 |
| ex06 | start·center·right 텍스트 정렬 확인 |
| ex07 | 다섯 부모의 flex 방향 확인. column→row 필수 변경 시 4번 자식의 y 좌표가 같아짐 |
| ex08 | 다섯 justify-content 값 확인. center→flex-end 필수 변경 확인 |
| ex09 | 네 align-items 값과 stretch 자식 높이 100px 확인 |
| ex10 | nowrap 여섯 자식은 50px 한 줄, wrap은 80px 셋씩 두 줄 확인 |
| ex11 | 부모 gap 기본·16px·32px 확인 |
| ex12 | 마지막 부모의 세 자식이 같은 폭으로 분배됨 확인 |
| ex13 | 601px 하늘색, 600px·375px 주황으로 포함 경계 확인 |
| ex14 | relative 원래 공간 유지, absolute 흐름 이탈 뒤 B가 부모 시작 위치로 이동함 확인 |
| 완성 사이트 메뉴 | 3페이지 × 두 폭에서 메뉴 방향 확인. 메뉴 세 링크를 각각 클릭하여 총 18회 이동 확인 |
| 지정 실습 CSS | 실제 제공 CSS에 lab의 최종값을 적용해 제목 색·padding·max-width·메뉴 방향·가로 넘침을 브라우저에서 확인 |
| label과 이메일 | 세 label 클릭 시 연결 입력에 포커스. abc 이메일은 typeMismatch로 제출 차단·입력 유지 |
| 유효한 제출 | 가상 이메일로 submit 후 기본 GET 재탐색·세 입력 초기화·글 추가/저장 없음 확인 |
| file URL | 같은 HTML을 파일 주소로 열어 잘못된 이메일 차단, 빈 이메일 제출·재탐색 확인 |
| 그림 | 로드 성공과 400×400 프로필 자산 시각 확인 |
| 브라우저 오류 | 검사 중 pageerror·requestfailed·HTTP 400 이상 응답 0건 |
| 로컬 링크 | HTML·Markdown의 상대 대상/앵커 185개 검사, 끊어진 대상 없음 |
| HTML 구조 | 17개 문서 태그 닫힘·중첩·중복 ID 검사 통과. 외부 HTML 표준 인증은 아님 |
| 전문 코드 | walkthrough의 HTML 3개·CSS·JS 전문이 실행 파일과 모두 일치 |
| JavaScript | 보존 app.js의 node --check 통과. 4주 HTML 17개 모두 script 0개 |
| 한영 슬라이드 | 기존 23장씩 유지. 기존 Marp·teaching 테마와 deck 자동 맞춤으로 임시 렌더한 46장 모두 본문/가로 넘침 없음. 최소 본문 크기 한글 26px·영문 24px |
| 문체·공백 | 한국어 UI·문서 검사 및 git diff --check 통과 |

375px 홈·방명록과 영문 덱 화면을 캡처하여 직접 확인했다. 임시 스크립트·검증 JSON·캡처·한영 렌더 파일은 저장소 밖 임시 폴더(`week04-*`)에 두었고 배포 자산에 추가하지 않았다.

## 남은 제한과 인계

- 학생의 실제 30분 수행 시간을 실측하지 않았다. C01의 필수 수정량을 기준으로 구성하고 지정 변경 동작을 재현했다.
- 개인 GitHub 업로드·실제 Pages 게시·학생 계정은 실행하지 않았다. 파일 URL과 localhost를 검증했다.
- 전체 과목 빌드·공통 테스트·독립 평가는 총괄 단계다. 이 보고서는 4주차 파일·브라우저·한영 임시 렌더 검증이다.
- 외부 참고 문서의 실시간 접속과 전면 HTML 표준 검증기를 실행하지 않았다.
- 5주 담당자에게 최신 guestbook.html과 styles.css를 전달했다. 5주에서는 about·guestbook·CSS·그림을 이어 쓰고 index의 JavaScript 연결·출력 및 app.js를 변경한다.
