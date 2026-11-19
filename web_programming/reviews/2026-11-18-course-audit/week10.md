# 10주 배열·목록 조사와 실행 기록

2026-11-18, C01 선정안에 맞춰 10주 담당이 기존 31개 파일과 추가 19개 파일을 확인했다. 최종 50개 파일은 문서 14, HTML 12, JS 11, CSS 9, PNG 3, SVG 1이다. 공통 파일·다른 주차·커밋·푸시는 수정하지 않았다.

## 수정 이유와 범위

기존 30분 설명·60분 실습, 모든 예제 값 수정, 수업 중 GitHub 저장소 생성·Pages 업로드가 C01과 맞지 않았다. ex01·02는 Console 전용이었고 여러 HTML에 긴 수업 설명이 있었다. ‘배열이 없으면 DOM 한 줄 삭제나 개수 계산이 불가능하다’는 설명과 ‘11주 전체 저장 방명록을 직접 구현하고 공개 주소에서만 확인한다’는 안내도 바로잡았다.

- 두 차시 모두 강의·시연 60분과 실습 30분으로 편성했다. 파일·저장소 준비는 수업 전, 업로드는 수업 뒤다.
- 1일차는 ex01 문자열 두 값과 ex02 for·본문 다섯 줄, 2일차는 등록 두 줄·삭제 두 줄을 필수 작성으로 한정했다.
- ex02 app.start.js/start.html과 방명록 guestbook.start.js/guestbook.start.html을 제공했다. 학생 TODO를 완성본 파일과 구분한다.
- 일곱 비교 예제 모두 화면에서 결과를 확인한다. ex01은 추가·초기화와 배열 출력, ex02는 고정 3회와 length 반복의 목록 비교, ex03은 생성한 첫 요소를 붙이는 버튼을 갖춘다.
- HTML의 장문은 폴더별 README로 옮겼다. W3.CSS는 cdnjs 4.1.0 CDN, 추가 스타일은 공통 CSS의 배포 사본이다. 라이브러리 파일은 저장하지 않았다.
- 7주 최종 홈·소개·JS·CSS·프로필 자산을 인계했다. 방명록에는 기존 폼·메뉴 ID를 유지하고 개수·빈 안내·배열 삭제를 더했다. 긴 문자열은 example-output으로 줄바꿈한다.
- 배열 심화는 특강, 11주는 객체·문자열·JSON·폼 저장 필수와 전체 방명록 제공 시연, 12~14주는 공용 API 호출로 연결한다.
- 한영 슬라이드는 기존 각 16장으로 유지했다. 시간표·필수 수정·선택 예제와 새 시작 파일 링크를 양쪽에 반영했다.

## 차시별 검증

| 차시 | 학생 수정 | 실제 확인 |
|---|---|---|
| 10-1 | 문자열 두 값, for·본문 다섯 줄 | 시작 TODO를 메모리에서 완성하면 app.js와 일치. 0·1·3개 배열과 아래 목록 개수 일치 |
| 10-2 | 직접 append를 push·showList 두 줄로 교체, 삭제 두 줄 | 시작 TODO를 완성하면 guestbook.js와 일치. 3→2→0개, 가운데 삭제 뒤 이웃 글 유지 |

실습 시간은 편성 기준이다. 실제 초보 학생의 30분 수행 시간을 실측한 것은 아니다.

## 브라우저 실행

[실행 기록](evidence/week10-browser.json), [오류 변형·복사 기록](evidence/week10-variants.json), [375px 긴 입력 화면](evidence/week10-375.png).

Chrome의 localhost 미리보기에서 HTML 12개를 375/1280px로 각각 실행했다. 정상 실행의 처리되지 않은 예외는 0건이다. W3.CSS 로드와 가로 넘침을 확인했고 홈·방명록 교재 PNG를 최신 화면으로 갱신해 직접 확인했다.

| 예제 | 동작·경계 확인 |
|---|---|
| ex01 | 초기 3개, 없는 인덱스 undefined, 추가·초기화·빈 문자열·새로고침 |
| ex02 | 초기 위 3·아래 4개, 5회 반복에도 중복 없음, 배열 0·1·3개, 다섯 줄 시작 틀 완성 |
| ex03 | 초기 2·3번, li1을 여러 번 붙여도 복제 없이 총 3개 |
| ex04 | 서로 다른 값·태그 모양 문자열·빈 문자열·120자, 배열과 목록 4개, 새로고침 0개 |
| ex05 | 비우지 않으면 3→6개, 비우면 5회 반복에도 3개 |
| ex06 | 빈 안내·추가·개수·텍스트 표시·빈 문자열·새로고침 |
| ex07 | 가운데 삭제·이웃 보존·전부 삭제·새로고침 초기 3개 |
| 시작/완성 방명록 | 빈 이름·공백 메시지·초점, native 이메일 형식 차단, 이메일 생략, 등록·폼 초기화·가운데 삭제·0개·새로고침 |
| 홈·내 정보 | 프로필 로드, 인사, 다크 모드 제목 대비, 세 페이지 메뉴 |

선택 문항의 코드 변형 11건도 임시 브라우저 응답에서 실행했다. `<`→`<=`, `let i`→`const i`, `createElement('<li>')`, push·append 생략, 템플릿 문자열 따옴표 변경, 비우기 생략, 최초/추가 후 showList 생략, splice 삭제 개수 2, 삭제 뒤 showList 생략이다. 예측한 목록·개수 또는 오류를 확인한 뒤 원본을 다시 읽어 복구했다. 추적 파일에 오류 변형이나 정답을 덮어쓰지 않았다.

ex02와 완성 웹 폴더를 임시 경로에 독립 복사하여 file URL로 실행했다. 로컬 CSS·JS 경로와 배열 목록·등록을 확인한 뒤 해당 임시 폴더만 제거했다. 실제 GitHub Pages 업로드는 수행하지 않았다.

## 정적 검증

- JS 11개 구문 검사 통과
- 로컬 파일 링크·HTML 자산 경로 131건, 누락 0건
- shared/examples.css 8개 사본이 공통 원본과 일치
- 7주 홈·내 정보·app.js·styles.css·profile.png의 5개 인계 파일 내용 일치
- 한영 각각 16장, 문서·UI 한국어 검사 통과
- 학생 TODO 완성 결과 두 파일과 제공 완성본의 전체 코드 일치

전체 사이트 빌드·렌더된 덱의 배치·다른 주차 교차 링크와 독립 평가는 총괄 통합 검증에 남겼다.

## 전수 파일 목록

경로 기준은 weeks/week10_array_list다.

- 루트 5개: README.md, lab.md, walkthrough.md, slides.md, slides_en.md
- examples/README.md
- day1/ex01·ex03·ex04 및 day2/ex05·ex06·ex07 각 4개: README.md, index.html, app.js, shared/examples.css
- day1/ex02 6개: README.md, index.html, app.js, start.html, app.start.js, shared/examples.css
- day2/web-week10 14개: README.md, index.html, about.html, app.js, styles.css, guestbook.html, guestbook.js, guestbook.start.html, guestbook.start.js, shared/examples.css, images/profile.png, images/site-map.svg, screenshots/home.png, screenshots/guestbook.png

텍스트 파일은 내용·실행 연결을 읽었고 SVG는 소스를, PNG는 브라우저 표시와 갱신 캡처를 확인했다. 실제 학생 개인정보·비공개 설정은 사용하지 않았다.
