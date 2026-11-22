# 웹프로그래밍 공용 교재

## 목차

- [범위](#범위)
- [진입점](#진입점)
- [학교 적용](#학교-적용)
- [운영 주의](#운영-주의)

## 범위

프로그래밍 경험이 거의 없는 학생을 기준으로 한 **입문 웹** 교재다. HTML·CSS·JavaScript를 중심으로 하고, Git·GitHub Pages는 2주차까지 배워 결과물을 올리는 데 쓴다.
4주차부터는 **매주 새 저장소**(`web-week04`, `web-week05` …)를 만들어 그 주 결과물을 올린다. 공개 주소는 `https://<아이디>.github.io/web-week05/` 모양이다.

1주차는 연습용 폴더 `week01`에서 URL·요청과 응답·DevTools와 로컬 Git(`init → add → commit`)을 익히고,
2주차에 `my-web`을 GitHub에 올려(push) Pages로 공개 주소를 만들고 브랜치와 merge까지 한다.
3주차에는 `my-web`을 이어 쓰고 4~7주차에는 전 주의 완성 파일을 새 주차 저장소에 옮겨 세 페이지 자기소개 사이트로 키운다. 시맨틱 HTML과 form(3주), CSS와 반응형(4주),
변수·`if`·함수(5주), DOM·이벤트(6주), CSS 응용(7주)을 다룬다. 7주차에는 반응형 메뉴와 최신순 타임라인을 방명록에 적용하고 9주 발표에 사용한다. 10주에는 배열 인덱스를 화면의 각 줄과 비교할 수 있도록 등록순 문자열 목록을 제공한다.
10주에는 배열로 방명록 목록을 그리고 11주에는 객체를 브라우저에 저장한다. 12주는 공개 API에서 받은 할 일과 날씨를 예제로 Promise와 `async`/`await`를 익힌다. 13주에는 방명록에 글을 등록하고 14주에는 그 글을 수정·삭제한다.
8주 중간 개인 실기, 9주 1차 과제 발표, 15주 기말 개인 실기가 들어 있다. 14주는 구현 수업이며 레포트는 별도 과제로 안내한다.

방명록 API는 강의자가 준비한다. 학생은 Supabase 계정·SQL·SDK 없이 `fetch`로 요청한다.
서버 구축·로그인 구현은 정규 범위 밖이다. 방학 연구 특강에서는 Supabase 공용 API 구축과 Node.js 홈 IoT 제어를 실험한다.
특강은 분량·차시 수를 제한하지 않으며, 구현·측정·검증을 단계별로 이어 간다. 지도와 신시사이저 실습 자료도 제공한다.
일반 27차시는 강의·시연 60분과 실습 30분이다. 8·15주 2차시의 실기와 9주 발표는 별도 시간표를 쓴다. 필수 수정·강의자 시연·선택 연습을 구분한다. 7주차에는 W3.CSS로 카드와 메뉴를 배치하고 방명록을 최신 글부터 읽는 피드로 구성한다. 11주차 2일차 필수 실습은 문자열·JSON·폼 저장이며, 완성 방명록은 시연과 이후 방명록 실습 자료로 제공한다.

정규 과정은 세 HTML 페이지를 이어 쓴다. SPA 직접 구현은 14주 완성본을 출발점으로 선택 특강에서 다룬다. 배열 심화도 별도 보강 특강이다. [수업 구성과 30차시 선정안](reviews/2026-11-18-course-audit/winner.md)에 변경 근거와 평가 결과를 기록했다.

## 진입점

- 15주 교재 색인: [`weeks/README.md`](weeks/README.md)
- 선택 특강: [`specials/README.md`](specials/README.md)
- 배열 심화 보강 특강: [`specials/array_advanced/`](specials/array_advanced/README.md)
- 14주 이후 SPA 전환 특강: [`specials/hash_spa/`](specials/hash_spa/README.md)
- 예제 공용 CSS: [`shared/README.md`](shared/README.md)
- 수업용 정적 웹 서버(Node.js): [`tools/static-server/`](tools/static-server/README.md)
- 강의자용 공용 방명록 API와 로컬 리허설: [`tools/guestbook-api/`](tools/guestbook-api/README.md)
- Supabase 공용 방명록 API 구축 특강: [`specials/supabase_guestbook/`](specials/supabase_guestbook/README.md)
- HTTP 홈 IoT 시뮬레이터 특강: [`specials/home_iot_http/`](specials/home_iot_http/README.md)
- 실습실 PC 의 GitHub 로그인 정리(Windows·macOS·Linux): [`../tools/github-classroom-pc-reset/`](../tools/github-classroom-pc-reset/README.md)
- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)
- 교재 사이트(HTML 슬라이드): <https://gbox3d.github.io/teaching_repo/webprg/>

각 주차 폴더에는 `README.md`, `slides.md`, `walkthrough.md`, `lab.md`, `examples/`가 있다.
강의 대본과 실습 해답은 강의자가 별도로 관리한다. 파일 세트와 실습 루틴은 [`weeks/README.md`](weeks/README.md#주차-폴더-구성)에 있다.

## 학교 적용

- 학교명·분반·실제 배점·시험·마감·LMS 정보는 학교 폴더에서 관리한다.
- 학교별 표지와 일정은 배포본에서 적용하고 공용 원고에 직접 넣지 않는다.

## 운영 주의

- **Git 설명은 2주차까지다(Pages 등록까지).** 3주차부터는 Git을 설명하지 않고 올리기 순서만 따른다([`weeks/README.md`](weeks/README.md#실습-루틴-3주차부터)).
- 학생 실습 30분에는 로컬 동작 확인과 캡처를 마친다. 3주 이후 새 저장소와 파일은 사전에 준비하고, push와 Pages 확인은 수업 뒤 정리로 분리한다. Git을 배우는 1~2주와 시험은 해당 시간표를 따른다.
- 공개 업로드 후 Pages 주소에서도 같은 동작을 확인한다. 배포 반영이 늦으면 로컬 화면과 GitHub **Commits** 탭을 증거로 남기고 다음 수업 준비 시간에 확인한다. 공용 API의 다른 브라우저 공유 확인은 로컬 모의 API 점검과 구분한다.
- 3~10주차는 작업 중 미리 보기를 `file://`(파일 더블클릭)로 해도 된다. 이 구간에는 미리 보기에 서버가 필요한 기능이 없다.
- 11주차에는 같은 origin에서 저장·새로고침·복원·삭제를 확인한다. localhost와 공개 주소의 데이터는 자동으로 공유되지 않는다. 11주 필수 제출은 폼 복원이며 전체 방명록 저장을 구현했다고 가정하지 않는다.
- 로컬 미리보기는 수업용 정적 서버 [`tools/static-server/server.mjs`](tools/static-server/README.md)로 한다(`node server.mjs` → `http://localhost:8000/`, 5주차에 처음 설명). 파일 상대 경로와 HTTP 요청을 확인하며, 11주 저장부터는 같은 localhost origin을 유지한다. Pages 게시 후에는 공개 HTTPS 주소에서도 확인한다.
  30분 실습 전에 로컬 미리보기 환경을 준비한다. 환경 설치가 막히면 조교가 같은 동작을 확인할 대체 정적 서버를 미리 준비한다.
- Git 인증은 **HTTPS + 브라우저 로그인**이 기본이다. 비밀번호나 토큰을 명령에 적지 않는다.
  공용 PC는 실습 끝에 자격 증명 관리자에서 `git:https://github.com`을 지운다(절차는 [`ta_setup_guide.md`](ta_setup_guide.md#공용-pc-운영)).
- 학생 PC의 정적 서버 실행 기준은 Node.js 24 이상이다. 학생 예제에는 npm 패키지를 설치하지 않는다.
- 정규 주차의 JavaScript는 클래식 `<script src="…" defer>`와 브라우저 기본 API를 사용한다. 11주차 저장 예제와 배열 심화 특강은 cdnjs CDN에서 W3.CSS를 불러와 화면을 구성한다. 연구 특강의 서버·제어 코드는 해당 자료의 구성을 따른다.
- 공개 저장소·캡처·예제에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`·`student01@example.com`이다.
- GitHub 화면과 무료 정책은 개강 전에 공식 문서와 새 실습 계정으로 다시 확인한다.
- 12주 필수 예제는 키 없이 JSONPlaceholder와 Open-Meteo를 호출한다. 13·14주 방명록은 강의자가 배부한 공개 키와 방명록 번호로 수업용 Supabase에 접속한다. [학생용 API 안내](tools/guestbook-api/student-guide.md)에서 주소와 요청 형식을 확인한다.
- 홈 IoT 특강은 학생 PC에서 Node.js 서버를 실행한다. 완료 확인은 `http://localhost:8014/`이며 GitHub Pages에서는 서버가 실행되지 않는다.
